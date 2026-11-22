"""PageIndex de conhecimento: uma árvore de títulos e resumos sobre os documentos.

Não há vetores nem embeddings. A IA lê a árvore (títulos e resumos), escolhe o
nó pelo raciocínio e pede o conteúdo dele. A busca por termos é um atalho.

Nós:
  <area>                       pasta de `knowledge/` (título e resumo em `_area.md`)
  <area>#<secao>               seção `##` do `_area.md`
  <area>/<doc>                 um documento
  <area>/<doc>#<secao>         seção `##` do documento
  <area>/<doc>#referencias     gerado a partir do references.json do subagente
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .registry import Registry
from .util import (
    OGError, first_paragraph, parse_frontmatter, query_tokens, score_text, slugify, snippet,
    write_json_atomic,
)

AREA_ORDER = [
    "geral", "lideranca", "design", "arte-3d", "animacao", "cinematics", "engenharia",
    "audio", "apoio", "pipelines",
]
_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class Node:
    id: str
    title: str
    summary: str
    kind: str  # area | doc | section
    text: str = ""
    children: list["Node"] = field(default_factory=list)
    source: str = ""

    def to_dict(self) -> dict:
        data = {"id": self.id, "title": self.title, "summary": self.summary, "kind": self.kind}
        if self.source:
            data["source"] = self.source
        if self.children:
            data["children"] = [c.to_dict() for c in self.children]
        return data


def _split_sections(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Devolve o texto antes do primeiro `##` e a lista (título, texto) das seções."""
    matches = [m for m in _H2.finditer(body) if not _inside_code(body, m.start())]
    if not matches:
        return body.strip(), []
    intro = body[: matches[0].start()].strip()
    sections = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections.append((match.group(1).strip(), body[match.end() : end].strip()))
    return intro, sections


def _inside_code(body: str, pos: int) -> bool:
    return body.count("```", 0, pos) % 2 == 1


def _unique(slug: str, used: set[str]) -> str:
    base, n = slug, 2
    while slug in used:
        slug = f"{base}-{n}"
        n += 1
    used.add(slug)
    return slug


class KnowledgeIndex:
    def __init__(self, knowledge_dir: Path, registry: Registry | None = None):
        self.dir = knowledge_dir
        self.registry = registry
        self.roots: list[Node] = []
        self.by_id: dict[str, Node] = {}
        self.build()

    def build(self) -> None:
        self.roots, self.by_id = [], {}
        if not self.dir.is_dir():
            return
        order = {name: i for i, name in enumerate(AREA_ORDER)}
        folders = sorted(
            (p for p in self.dir.iterdir() if p.is_dir() and not p.name.startswith(".")),
            key=lambda p: (order.get(p.name, 99), p.name),
        )
        for folder in folders:
            node = self._build_area(folder)
            if node:
                self.roots.append(node)
        for root in self.roots:
            self._register(root)

    def _register(self, node: Node) -> None:
        self.by_id[node.id] = node
        for child in node.children:
            self._register(child)

    def _build_area(self, folder: Path) -> Node | None:
        area_id = folder.name
        area_file = folder / "_area.md"
        meta, body = ({}, "")
        if area_file.is_file():
            meta, body = parse_frontmatter(area_file.read_text(encoding="utf-8"))
        intro, sections = _split_sections(body)
        area = Node(
            id=area_id, title=meta.get("title", area_id), kind="area", text=intro,
            summary=meta.get("summary") or first_paragraph(body),
            source=f"knowledge/{area_id}/_area.md" if area_file.is_file() else "",
        )
        used: set[str] = set()
        for title, text in sections:
            area.children.append(
                Node(id=f"{area_id}#{_unique(slugify(title), used)}", title=title,
                     summary=first_paragraph(text), kind="section", text=text, source=area.source)
            )
        docs = sorted(p for p in folder.glob("*.md") if p.name != "_area.md")
        for doc in self._order_docs(area_id, docs):
            area.children.append(self._build_doc(area_id, doc))
        return area if (area.children or area.text) else None

    def _order_docs(self, area_id: str, docs: list[Path]) -> list[Path]:
        """Na área de um agente, segue a ordem dos subagentes no agent.json."""
        if not self.registry or area_id not in self.registry.agents:
            return docs
        wanted = [s.knowledge_node.split("/")[-1] for s in self.registry.agents[area_id].subagents.values()]
        rank = {name: i for i, name in enumerate(wanted)}
        return sorted(docs, key=lambda p: (rank.get(p.stem, 99), p.stem))

    def _build_doc(self, area_id: str, path: Path) -> Node:
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        doc_id = f"{area_id}/{path.stem}"
        intro, sections = _split_sections(body)
        doc = Node(
            id=doc_id, title=meta.get("title", path.stem), kind="doc", text=intro,
            summary=meta.get("summary") or first_paragraph(body),
            source=f"knowledge/{area_id}/{path.name}",
        )
        used: set[str] = set()
        for title, text in sections:
            doc.children.append(
                Node(id=f"{doc_id}#{_unique(slugify(title), used)}", title=title,
                     summary=first_paragraph(text), kind="section", text=text, source=doc.source)
            )
        owner = self.registry.subagent_by_knowledge_node(doc_id) if self.registry else None
        if owner and "referencias" not in used:
            agent, sub = owner
            refs = agent.references_for(sub.id)
            text = (
                f"Referências de pesquisa do subagente `{sub.id}` (agente `{agent.id}`). "
                "Só o subagente abre estas páginas; o agente delega a pesquisa.\n\n"
                + "\n".join(r.render() for r in refs)
            )
            doc.children.append(
                Node(id=f"{doc_id}#referencias", title="Referências", kind="section", text=text,
                     summary=f"{len(refs)} fontes que o subagente {sub.id} usa para pesquisar.",
                     source=f"agents/{agent.id}/subagents/{sub.id}/references.json")
            )
        return doc

    # ------------------------------------------------------------------ consulta

    def get(self, node_id: str) -> Node:
        node = self.by_id.get(node_id.strip().strip("/"))
        if node is None:
            close = [i for i in self.by_id if node_id.strip().lower() in i][:8]
            hint = f" Parecidos: {', '.join(close)}." if close else ""
            raise OGError(
                f"Nó `{node_id}` não existe no PageIndex de conhecimento.{hint} "
                "Use knowledge_tree para ver os ids."
            )
        return node

    def tree(self, node_id: str = "", depth: int = 2) -> str:
        depth = max(1, min(int(depth), 4))
        if node_id:
            start = self.get(node_id)
            lines = [f"# {start.title}  `{start.id}`", start.summary, ""]
            nodes = start.children
            if not nodes:
                return "\n".join(lines + ["(sem filhos: use knowledge_read para o conteúdo)"])
        else:
            lines = ["# PageIndex de conhecimento: jogos 3D cinematográficos", ""]
            nodes = self.roots
        for node in nodes:
            self._outline(node, 0, depth, lines)
        lines += ["", "Leia um nó com knowledge_read(node). Aprofunde com knowledge_tree(node, depth)."]
        return "\n".join(lines)

    def _outline(self, node: Node, level: int, depth: int, lines: list[str]) -> None:
        summary = f": {node.summary}" if node.summary else ""
        lines.append(f"{'  ' * level}- `{node.id}` **{node.title}**{summary}")
        if level + 1 < depth:
            for child in node.children:
                self._outline(child, level + 1, depth, lines)
        elif node.children:
            lines.append(f"{'  ' * (level + 1)}({len(node.children)} nós dentro)")

    def read(self, node_id: str) -> str:
        node = self.get(node_id)
        parts = [f"# {node.title}  `{node.id}`"]
        if node.source:
            parts.append(f"Fonte: {node.source}")
        if node.kind == "section":
            parts += ["", node.text]
        elif node.kind == "doc":
            if node.text:
                parts += ["", node.text]
            for child in node.children:
                parts += ["", f"## {child.title}  `{child.id}`", "", child.text]
        else:
            parts += ["", node.summary]
            if node.text:
                parts += ["", node.text]
            for child in node.children:
                if child.kind == "section":
                    parts += ["", f"## {child.title}  `{child.id}`", "", child.text]
            docs = [c for c in node.children if c.kind == "doc"]
            if docs:
                parts += ["", "## Documentos desta área", ""]
                parts += [f"- `{d.id}` **{d.title}**: {d.summary}" for d in docs]
        return "\n".join(parts).strip()

    def search(self, query: str, limit: int = 8) -> str:
        tokens = query_tokens(query)
        if not tokens:
            raise OGError("Informe o que procurar.")
        scored = []
        for node in self.by_id.values():
            body = node.text
            if node.kind != "section":
                body = node.text + " " + " ".join(c.title for c in node.children)
            score = score_text(tokens, node.title, node.summary, body)
            if node.kind == "section":
                parent = self.by_id.get(node.id.split("#")[0])
                if parent:
                    score += 0.5 * score_text(tokens, parent.title, "", "")
            if score > 0:
                scored.append((score, node))
        if not scored:
            return (
                f"Nada encontrado para \"{query}\" no PageIndex de conhecimento. "
                "Tente outros termos ou navegue com knowledge_tree."
            )
        scored.sort(key=lambda item: (-item[0], item[1].id))
        limit = max(1, min(int(limit), 25))
        lines = [f"# Resultados para \"{query}\"", ""]
        for score, node in scored[:limit]:
            lines.append(f"- `{node.id}` **{node.title}** ({node.kind})")
            lines.append(f"  {snippet(node.text or node.summary, tokens)}")
        lines += ["", "Leia o nó completo com knowledge_read(node)."]
        return "\n".join(lines)

    def write_index(self, path: Path) -> None:
        write_json_atomic(path, {
            "name": "OpenGlitch: criação de jogos 3D cinematográficos",
            "node_count": len(self.by_id),
            "tree": [root.to_dict() for root in self.roots],
        })
