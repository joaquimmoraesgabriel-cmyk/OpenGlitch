"""Manutenção do conteúdo.

  python -m openglitch_mcp.cli validate   confere agentes, referências, pipelines e documentos
  python -m openglitch_mcp.cli index      grava knowledge/index.json (a árvore do PageIndex)
  python -m openglitch_mcp.cli links      abre cada referência pesquisável e diz quais falham
"""

from __future__ import annotations

import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import webtools
from .core import App
from .util import OGError, parse_frontmatter


def _root() -> Path:
    return Path(os.environ.get("OPENGLITCH_HOME") or Path(__file__).resolve().parents[2])


def validate(app: App) -> list[str]:
    problems = list(app.registry.problems)
    for path in sorted((app.root / "knowledge").rglob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(app.root).as_posix()
        if not meta.get("title") or not meta.get("summary"):
            problems.append(f"{rel}: frontmatter sem title ou summary")
        if "## " not in body:
            problems.append(f"{rel}: documento sem seções `##`")
    for pipe in app._pipelines():
        for agent_id in pipe.get("agent_sequence", []):
            if agent_id not in app.registry.agents:
                problems.append(f"pipeline {pipe['id']}: agente desconhecido `{agent_id}`")
        if pipe.get("knowledge_node") and pipe["knowledge_node"] not in app.knowledge.by_id:
            problems.append(f"pipeline {pipe['id']}: knowledge_node inexistente")
        for stage in pipe["stages"]:
            for owner in stage["owners"]:
                agent = app.registry.agents.get(owner["agent"])
                if agent is None:
                    problems.append(f"pipeline {pipe['id']} etapa {stage['id']}: agente `{owner['agent']}`")
                    continue
                for sub in owner.get("subagents", []):
                    if sub not in agent.subagents:
                        problems.append(
                            f"pipeline {pipe['id']} etapa {stage['id']}: `{owner['agent']}` não tem `{sub}`")
    for name in ("roteador.md", "protocolo-agente.md", "protocolo-subagente.md"):
        if not (app.root / "agents" / "_shared" / name).is_file():
            problems.append(f"agents/_shared/{name}: arquivo ausente")
    if not any(a.mandatory_first for a in app.registry.agents.values()):
        problems.append("nenhum agente com mandatory_first: true")
    return problems


def cmd_validate(app: App) -> int:
    problems = validate(app)
    workers = app.registry.workers()
    subs = sum(len(a.subagents) for a in workers)
    refs = sum(len(s.references) for a in workers for s in a.subagents.values())
    refs += sum(len(a.shared_references) for a in workers)
    print(f"{len(app.registry.agents)} agentes, {subs} subagentes, {refs} referências, "
          f"{len(app.knowledge.by_id)} nós de conhecimento, {len(app._pipelines())} pipelines.")
    for problem in problems:
        print(f"PROBLEMA: {problem}")
    print("OK" if not problems else f"{len(problems)} problemas.")
    return 1 if problems else 0


def cmd_index(app: App) -> int:
    target = app.root / "knowledge" / "index.json"
    app.knowledge.write_index(target)
    print(f"{len(app.knowledge.by_id)} nós gravados em {target}")
    return 0


def cmd_links(app: App) -> int:
    urls: dict[str, list[str]] = {}
    for agent in app.registry.workers():
        for ref in agent.shared_references:
            if ref.pesquisavel and ref.url:
                urls.setdefault(ref.url, []).append(f"{agent.id}/shared:{ref.id}")
        for sub in agent.subagents.values():
            for ref in sub.references:
                if ref.pesquisavel and ref.url:
                    urls.setdefault(ref.url, []).append(f"{agent.id}/{sub.id}:{ref.id}")

    def check(url: str) -> tuple[str, str]:
        try:
            got = webtools.fetch(url, first_bytes_only=32 * 1024)
            note = "" if webtools.host_of(got.url) == webtools.host_of(url) else f" -> {got.url}"
            kind = got.content_type or "?"
            return url, f"ok ({kind}){note}"
        except OGError as exc:
            return url, f"FALHA: {exc}"

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, urls))
    failures = 0
    for url, status in sorted(results):
        if status.startswith("FALHA") or "html" not in status.split(")")[0]:
            failures += 1
            print(f"{status}\n  {url}\n  usado em: {', '.join(urls[url])}")
    print(f"{len(urls)} URLs pesquisáveis conferidas; {failures} com problema ou que não são HTML.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    commands = {"validate": cmd_validate, "index": cmd_index, "links": cmd_links}
    if len(args) != 1 or args[0] not in commands:
        print(__doc__)
        return 2
    return commands[args[0]](App(_root()))


if __name__ == "__main__":
    raise SystemExit(main())
