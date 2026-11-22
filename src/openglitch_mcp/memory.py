"""PageIndex de memória: uma árvore de nós por partição.

Uma partição é a memória de um dono:
  <agente>/research/<subagente>   memória de pesquisa de um subagente (global)
  <agente>/work                   memória de trabalho do agente (por projeto)

Quem pode ler e escrever cada partição é decidido em `core.py`. Este módulo só
guarda e recupera. Cada partição tem `index.json` (títulos, resumos, fontes,
histórico) e um Markdown por nó em `nodes/`.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .util import (
    OGError, file_lock, now_iso, query_tokens, read_json, score_text, snippet,
    write_json_atomic, write_text_atomic,
)

MAX_CONTENT = 24_000
MAX_TITLE = 140
MAX_SUMMARY = 500
OPS = ("add", "update", "append", "correct", "remove")


def _clean_sources(raw: Any) -> list[dict]:
    out = []
    for item in raw or []:
        if isinstance(item, str):
            item = {"url": item}
        if not isinstance(item, dict):
            continue
        entry = {k: str(item[k])[:500] for k in ("ref_id", "url", "title") if item.get(k)}
        if entry:
            out.append(entry)
    return out[:40]


def _clean_images(raw: Any) -> list[dict]:
    out = []
    for item in raw or []:
        if not isinstance(item, dict) or not item.get("url") or not item.get("description"):
            raise OGError("Cada imagem precisa de `url` (o link original) e `description`.")
        out.append({"url": str(item["url"])[:1000], "description": str(item["description"])[:4000]})
    return out[:20]


class Partition:
    def __init__(self, base: Path, key: str, directory: Path):
        self.key = key
        self.dir = directory
        self._lock = base / ".lock"

    # ------------------------------------------------------------------ leitura

    def _index(self) -> dict:
        return read_json(self.dir / "index.json", None) or {"key": self.key, "next": 1, "nodes": {}}

    def active(self) -> dict[str, dict]:
        return {i: n for i, n in self._index()["nodes"].items() if n["status"] == "active"}

    def count(self) -> int:
        return len(self.active())

    def ref(self, node_id: str) -> str:
        return f"{self.key}#{node_id}"

    def content(self, node_id: str) -> str:
        path = self.dir / "nodes" / f"{node_id}.md"
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def outline(self, lines: list[str], indent: int = 0) -> None:
        nodes = self.active()
        children: dict[str | None, list[dict]] = {}
        for node in nodes.values():
            parent = node.get("parent") if node.get("parent") in nodes else None
            children.setdefault(parent, []).append(node)

        def walk(parent: str | None, level: int) -> None:
            for node in sorted(children.get(parent, []), key=lambda n: n["id"]):
                extra = []
                if node.get("sources"):
                    extra.append(f"{len(node['sources'])} fontes")
                if node.get("images"):
                    extra.append(f"{len(node['images'])} imagens")
                extra.append(f"atualizado {node['updated'][:10]}")
                lines.append(
                    f"{'  ' * level}- `{self.ref(node['id'])}` **{node['title']}**: "
                    f"{node['summary']} ({', '.join(extra)})"
                )
                walk(node["id"], level + 1)

        walk(None, indent)

    def read(self, node_id: str) -> str:
        node = self._index()["nodes"].get(node_id)
        if node is None:
            raise OGError(f"Nó `{self.ref(node_id)}` não existe. Use memory_tree para ver os ids.")
        lines = [f"# {node['title']}  `{self.ref(node_id)}`", f"Resumo: {node['summary']}"]
        if node["status"] != "active":
            lines.append(f"**Este nó foi removido** ({node['history'][-1].get('reason', 'sem motivo')}).")
        lines.append(f"Criado {node['created']}, atualizado {node['updated']}, revisão {node['revision']}.")
        if node.get("parent"):
            lines.append(f"Dentro de: `{self.ref(node['parent'])}`")
        if node.get("tags"):
            lines.append(f"Tags: {', '.join(node['tags'])}")
        lines += ["", self.content(node_id)]
        if node.get("sources"):
            lines += ["", "## Fontes"]
            for src in node["sources"]:
                label = src.get("title") or src.get("ref_id") or src.get("url", "")
                ref = f" (`{src['ref_id']}`)" if src.get("ref_id") and src.get("title") else ""
                url = f": {src['url']}" if src.get("url") and src.get("url") != label else ""
                lines.append(f"- {label}{ref}{url}")
        if node.get("images"):
            lines += ["", "## Imagens (link original e descrição)"]
            for img in node["images"]:
                lines.append(f"- {img['url']}\n  {img['description']}")
        corrections = [h for h in node["history"] if h["op"] == "correct"]
        if corrections:
            lines += ["", "## Correções registradas"]
            lines += [f"- {h['at']}: {h.get('reason', '')}" for h in corrections]
        return "\n".join(lines)

    def search(self, tokens: list[str]) -> list[tuple[float, str, dict, str]]:
        hits = []
        for node_id, node in self.active().items():
            body = self.content(node_id)
            images = " ".join(i["description"] for i in node.get("images", []))
            score = score_text(tokens, node["title"], node["summary"], body + " " + images,
                               " ".join(node.get("tags", [])))
            if score > 0:
                hits.append((score, self.ref(node_id), node, snippet(body, tokens)))
        return hits

    # ------------------------------------------------------------------ escrita

    def write(self, op: str, *, node_id: str = "", title: str = "", summary: str = "",
              content: str = "", parent: str = "", tags: list[str] | None = None,
              sources: Any = None, images: Any = None, reason: str = "", by: str = "") -> dict:
        if op not in OPS:
            raise OGError(f"Operação `{op}` não existe. Use uma de: {', '.join(OPS)}.")
        if len(content) > MAX_CONTENT:
            raise OGError(
                f"Conteúdo com {len(content)} caracteres; o limite por nó é {MAX_CONTENT}. "
                "Divida em nós menores, um assunto por nó."
            )
        with file_lock(self._lock):
            index = self._index()
            nodes = index["nodes"]
            now = now_iso()
            parent = parent.split("#")[-1].strip() if parent else ""
            if parent and (parent not in nodes or nodes[parent]["status"] != "active"):
                raise OGError(f"Nó pai `{parent}` não existe nesta memória.")

            if op == "add":
                if not title.strip() or not summary.strip() or not content.strip():
                    raise OGError("`add` precisa de title, summary e content.")
                node_id = f"{index['next']:04d}"
                index["next"] += 1
                node = {
                    "id": node_id, "title": title.strip()[:MAX_TITLE],
                    "summary": summary.strip()[:MAX_SUMMARY], "parent": parent or None,
                    "tags": [str(t)[:40] for t in (tags or [])][:12],
                    "sources": _clean_sources(sources), "images": _clean_images(images),
                    "status": "active", "created": now, "updated": now, "revision": 1,
                    "history": [{"op": "add", "at": now, "by": by}],
                }
                nodes[node_id] = node
                write_text_atomic(self.dir / "nodes" / f"{node_id}.md", content.strip() + "\n")
            else:
                node_id = node_id.split("#")[-1].strip()
                node = nodes.get(node_id)
                if node is None or node["status"] != "active":
                    raise OGError(
                        f"Nó `{node_id}` não existe nesta memória. `{op}` precisa do id de um nó "
                        "ativo; use `add` para criar um novo."
                    )
                if op in ("correct", "remove") and not reason.strip():
                    raise OGError(f"`{op}` precisa de `reason`: diga o que estava errado ou obsoleto.")
                if parent == node_id:
                    raise OGError("Um nó não pode ser pai dele mesmo.")
                self._keep_revision(node_id, node["revision"])
                event = {"op": op, "at": now, "by": by}
                if reason.strip():
                    event["reason"] = reason.strip()[:600]
                if op == "remove":
                    node["status"] = "removed"
                    for other in nodes.values():
                        if other.get("parent") == node_id:
                            other["parent"] = node.get("parent")
                else:
                    if op == "append":
                        if not content.strip():
                            raise OGError("`append` precisa de content.")
                        merged = self.content(node_id).rstrip() + "\n\n" + content.strip() + "\n"
                        if len(merged) > MAX_CONTENT:
                            raise OGError("O nó passaria do limite de tamanho. Crie um nó filho com `add`.")
                        write_text_atomic(self.dir / "nodes" / f"{node_id}.md", merged)
                    elif content.strip():
                        write_text_atomic(self.dir / "nodes" / f"{node_id}.md", content.strip() + "\n")
                    elif op == "correct":
                        raise OGError("`correct` precisa do content corrigido.")
                    if title.strip():
                        node["title"] = title.strip()[:MAX_TITLE]
                    if summary.strip():
                        node["summary"] = summary.strip()[:MAX_SUMMARY]
                    if parent:
                        node["parent"] = parent
                    if tags is not None:
                        node["tags"] = [str(t)[:40] for t in tags][:12]
                    if sources:
                        known = {(s.get("ref_id"), s.get("url")) for s in node["sources"]}
                        fresh = [s for s in _clean_sources(sources)
                                 if (s.get("ref_id"), s.get("url")) not in known]
                        node["sources"] = (node["sources"] + fresh)[:40]
                    if images:
                        known_img = {i["url"] for i in node["images"]}
                        node["images"] = (node["images"] + [
                            i for i in _clean_images(images) if i["url"] not in known_img])[:20]
                node["revision"] += 1
                node["updated"] = now
                node["history"].append(event)
            index["updated"] = now
            write_json_atomic(self.dir / "index.json", index)
            return {"ref": self.ref(node_id), "op": op, "title": node["title"],
                    "revision": node["revision"]}

    def _keep_revision(self, node_id: str, revision: int) -> None:
        current = self.dir / "nodes" / f"{node_id}.md"
        if current.is_file():
            target = self.dir / "nodes" / "_history" / f"{node_id}.r{revision}.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(current, target)


class MemoryStore:
    def __init__(self, base: Path):
        self.base = base

    def research(self, agent: str, subagent: str) -> Partition:
        return Partition(self.base, f"{agent}/research/{subagent}",
                         self.base / "agents" / agent / "research" / subagent)

    def work(self, agent: str, project: str) -> Partition:
        return Partition(self.base, f"{agent}/work",
                         self.base / "agents" / agent / "work" / project)


def search_partitions(partitions: list[Partition], query: str, limit: int = 8) -> str:
    tokens = query_tokens(query)
    if not tokens:
        raise OGError("Informe o que procurar.")
    hits = []
    for part in partitions:
        hits.extend(part.search(tokens))
    if not hits:
        return (
            f"Nada na memória para \"{query}\". Se a informação é necessária, "
            "é caso de delegar a pesquisa a um subagente."
        )
    hits.sort(key=lambda h: (-h[0], h[1]))
    lines = [f"# Memória: resultados para \"{query}\"", ""]
    for _, ref, node, snip in hits[: max(1, min(int(limit), 25))]:
        lines.append(f"- `{ref}` **{node['title']}** (atualizado {node['updated'][:10]})")
        lines.append(f"  {node['summary']}")
        if snip:
            lines.append(f"  Trecho: {snip}")
    lines += ["", "Leia o nó completo com memory_read(token, node)."]
    return "\n".join(lines)
