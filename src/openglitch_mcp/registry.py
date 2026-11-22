"""Carrega agentes, subagentes e referências da pasta `agents/`."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from .util import OGError, parse_frontmatter, read_json

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_TYPES = {
    "site", "blog", "livro-online", "livro", "curso", "documentacao", "artigo", "wiki",
    "forum", "palestra", "video", "ferramenta", "banco-de-dados",
}
URL_ORIGINS = {"pdf", "dominio-pdf", "corrigida", "inferida"}
AGENT_ORDER = ["design", "arte-3d", "animacao", "cinematics", "engenharia", "audio", "apoio", "leitor"]


@dataclass
class Reference:
    id: str
    title: str
    type: str
    url: str | None
    url_origem: str
    pesquisavel: bool
    uso: str
    author: str | None = None
    nota: str | None = None
    shared: bool = False

    @property
    def host(self) -> str | None:
        if not self.url:
            return None
        return (urlsplit(self.url).hostname or "").lower() or None

    def render(self) -> str:
        head = f"- `{self.id}` **{self.title}**"
        if self.author:
            head += f", {self.author}"
        head += f" ({self.type})"
        if self.url and self.pesquisavel:
            head += f": {self.url}"
        elif self.url:
            head += f": {self.url} [não pesquisável pelas ferramentas]"
        else:
            head += " [sem versão online; só leitura recomendada]"
        lines = [head, f"  Uso: {self.uso}"]
        if self.nota:
            lines.append(f"  Nota: {self.nota}")
        return "\n".join(lines)


@dataclass
class Subagent:
    id: str
    name: str
    purpose: str
    knowledge_node: str
    skill: str = ""
    references: list[Reference] = field(default_factory=list)


@dataclass
class Agent:
    id: str
    name: str
    kind: str
    summary: str
    when_to_use: str
    mandatory_first: bool
    skill: str = ""
    shared_references: list[Reference] = field(default_factory=list)
    subagents: dict[str, Subagent] = field(default_factory=dict)

    def subagent(self, sub_id: str) -> Subagent:
        try:
            return self.subagents[sub_id]
        except KeyError:
            known = ", ".join(self.subagents) or "nenhum"
            raise OGError(
                f"O agente `{self.id}` não tem o subagente `{sub_id}`. Subagentes dele: {known}."
            ) from None

    def references_for(self, sub_id: str) -> list[Reference]:
        """Referências do subagente seguidas das compartilhadas que ele ainda não tem."""
        sub = self.subagent(sub_id)
        own_ids = {r.id for r in sub.references}
        return sub.references + [r for r in self.shared_references if r.id not in own_ids]


def _parse_reference(raw: dict, where: str, problems: list[str], shared: bool) -> Reference | None:
    missing = [k for k in ("id", "title", "type", "url_origem", "pesquisavel", "uso") if k not in raw]
    if missing or "url" not in raw:
        problems.append(f"{where}: referência sem os campos {missing or ['url']}: {raw.get('id', raw)}")
        return None
    ref = Reference(
        id=str(raw["id"]), title=str(raw["title"]), type=str(raw["type"]), url=raw["url"],
        url_origem=str(raw["url_origem"]), pesquisavel=bool(raw["pesquisavel"]),
        uso=str(raw["uso"]), author=raw.get("author"), nota=raw.get("nota"), shared=shared,
    )
    if not ID_RE.match(ref.id):
        problems.append(f"{where}: id de referência inválido: {ref.id}")
    if ref.type not in REF_TYPES:
        problems.append(f"{where}: {ref.id}: type desconhecido `{ref.type}`")
    if ref.url_origem not in URL_ORIGINS:
        problems.append(f"{where}: {ref.id}: url_origem desconhecida `{ref.url_origem}`")
    if ref.url is not None:
        parts = urlsplit(str(ref.url))
        if parts.scheme not in ("http", "https") or not parts.hostname:
            problems.append(f"{where}: {ref.id}: url precisa ser http(s) completa: {ref.url}")
    elif ref.pesquisavel:
        problems.append(f"{where}: {ref.id}: pesquisavel é true mas url é null")
    return ref


def _read_skill(path: Path, where: str, problems: list[str]) -> str:
    if not path.is_file():
        problems.append(f"{where}: falta {path.name}")
        return ""
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    if not meta.get("name") or not meta.get("description"):
        problems.append(f"{where}: {path.name} sem frontmatter name/description")
    return body.strip()


class Registry:
    def __init__(self, agents_dir: Path, knowledge_dir: Path | None = None):
        self.agents_dir = agents_dir
        self.knowledge_dir = knowledge_dir
        self.agents: dict[str, Agent] = {}
        self.problems: list[str] = []
        self._load()

    def _load(self) -> None:
        if not self.agents_dir.is_dir():
            raise OGError(f"Pasta de agentes não encontrada: {self.agents_dir}")
        found: dict[str, Agent] = {}
        for folder in sorted(p for p in self.agents_dir.iterdir() if p.is_dir()):
            if folder.name.startswith("_"):
                continue
            raw = read_json(folder / "agent.json")
            if raw is None:
                self.problems.append(f"{folder.name}: falta agent.json")
                continue
            agent = self._load_agent(folder, raw)
            if agent:
                found[agent.id] = agent
        order = {name: i for i, name in enumerate(AGENT_ORDER)}
        self.agents = dict(sorted(found.items(), key=lambda kv: (order.get(kv[0], 99), kv[0])))

    def _load_agent(self, folder: Path, raw: dict) -> Agent | None:
        where = folder.name
        for key in ("id", "name", "kind", "summary", "when_to_use"):
            if not raw.get(key):
                self.problems.append(f"{where}: agent.json sem `{key}`")
                return None
        if raw["id"] != folder.name:
            self.problems.append(f"{where}: id `{raw['id']}` difere do nome da pasta")
        if raw["kind"] not in ("worker", "reader"):
            self.problems.append(f"{where}: kind desconhecido `{raw['kind']}`")
        agent = Agent(
            id=raw["id"], name=raw["name"], kind=raw["kind"], summary=raw["summary"],
            when_to_use=raw["when_to_use"], mandatory_first=bool(raw.get("mandatory_first")),
            skill=_read_skill(folder / "SKILL.md", where, self.problems),
        )
        seen: set[str] = set()
        for item in raw.get("shared_references", []):
            ref = _parse_reference(item, f"{where}/shared", self.problems, shared=True)
            if ref and ref.id not in seen:
                seen.add(ref.id)
                agent.shared_references.append(ref)
        for item in raw.get("subagents", []):
            sub = self._load_subagent(folder, agent.id, item)
            if sub:
                agent.subagents[sub.id] = sub
        on_disk = folder / "subagents"
        if on_disk.is_dir():
            for sub_folder in on_disk.iterdir():
                if sub_folder.is_dir() and sub_folder.name not in agent.subagents:
                    self.problems.append(
                        f"{where}: pasta subagents/{sub_folder.name} não está no agent.json"
                    )
        if agent.kind == "worker" and not agent.subagents:
            self.problems.append(f"{where}: agente worker sem subagentes")
        return agent

    def _load_subagent(self, folder: Path, agent_id: str, item: dict) -> Subagent | None:
        where = f"{agent_id}/{item.get('id', '?')}"
        for key in ("id", "name", "purpose", "knowledge_node"):
            if not item.get(key):
                self.problems.append(f"{where}: subagente sem `{key}`")
                return None
        if not ID_RE.match(item["id"]):
            self.problems.append(f"{where}: id inválido")
        sub_dir = folder / "subagents" / item["id"]
        sub = Subagent(
            id=item["id"], name=item["name"], purpose=item["purpose"],
            knowledge_node=item["knowledge_node"],
            skill=_read_skill(sub_dir / "SKILL.md", where, self.problems),
        )
        refs = read_json(sub_dir / "references.json")
        if refs is None:
            self.problems.append(f"{where}: falta references.json")
            return sub
        if refs.get("agent") != agent_id or refs.get("subagent") != sub.id:
            self.problems.append(f"{where}: references.json com agent/subagent diferentes da pasta")
        seen: set[str] = set()
        for raw_ref in refs.get("references", []):
            ref = _parse_reference(raw_ref, where, self.problems, shared=False)
            if not ref:
                continue
            if ref.id in seen:
                self.problems.append(f"{where}: referência duplicada `{ref.id}`")
                continue
            seen.add(ref.id)
            sub.references.append(ref)
        if not any(r.pesquisavel for r in sub.references):
            self.problems.append(f"{where}: nenhuma referência pesquisável")
        if self.knowledge_dir is not None:
            doc = self.knowledge_dir / (sub.knowledge_node + ".md")
            if not doc.is_file():
                self.problems.append(f"{where}: knowledge_node sem documento: {sub.knowledge_node}")
        return sub

    def agent(self, agent_id: str) -> Agent:
        try:
            return self.agents[agent_id]
        except KeyError:
            raise OGError(
                f"Agente `{agent_id}` não existe. Agentes: {', '.join(self.agents)}."
            ) from None

    def workers(self) -> list[Agent]:
        return [a for a in self.agents.values() if a.kind == "worker"]

    def subagent_by_knowledge_node(self, node: str) -> tuple[Agent, Subagent] | None:
        for agent in self.agents.values():
            for sub in agent.subagents.values():
                if sub.knowledge_node == node:
                    return agent, sub
        return None
