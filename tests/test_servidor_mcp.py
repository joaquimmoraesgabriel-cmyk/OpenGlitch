"""Ponta a ponta: sobe o servidor por stdio e fala com ele como um cliente MCP."""

import os
import re
import sys
from pathlib import Path

import anyio
import pytest
from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TOOLS = {
    "start", "project_status", "plan_agents", "get_pipeline", "activate_agent", "finish_agent",
    "publish_project_brief", "knowledge_tree", "knowledge_read", "knowledge_search",
    "memory_tree", "memory_search", "memory_read", "memory_write", "delegate_research",
    "task_status", "research_begin", "research_text", "research_tables", "research_images",
    "research_view_image", "research_complete", "report_problem", "list_problems", "local_docs", "local_doc_read",
}


def text_of(result) -> str:
    return "\n".join(block.text for block in result.content if hasattr(block, "text"))


def test_fluxo_completo_por_mcp(tmp_path):
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "openglitch_mcp"],
        env={**os.environ, "OPENGLITCH_HOME": str(ROOT), "OPENGLITCH_DATA": str(tmp_path),
             "PYTHONIOENCODING": "utf-8"},
    )

    async def run() -> None:
        async with Client(params) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == EXPECTED_TOOLS

            start = text_of(await client.call_tool("start", {"user_message": "quero fazer um jogo de luta"}))
            assert "`design`" in start and "obrigatório no começo" in start

            refused = await client.call_tool("activate_agent", {"agent": "animacao", "project": "Luta"})
            assert refused.is_error and "design" in text_of(refused)

            activated = text_of(await client.call_tool("activate_agent", {"agent": "design", "project": "Luta"}))
            session = re.search(r"session: `(ss_[\w-]+)`", activated).group(1)
            assert "# Agente Design" in activated and "Protocolo comum dos agentes" in activated
            assert "sirlin-playing-to-win" in activated

            brief = "# Luta\n\n## Visão\n" + "Jogo de luta 1x1 com cenas dirigidas entre os rounds. " * 6
            published = text_of(await client.call_tool("publish_project_brief", {"session": session, "content": brief}))
            assert "versão 1" in published

            created = text_of(await client.call_tool("delegate_research", {
                "session": session, "subagent": "combat-designer", "memory_access": False,
                "task": "Quais são as fases de um ataque e que faixas de frames usar em golpe leve e pesado?",
            }))
            ticket = re.search(r"ticket: (tk_[\w-]+)", created).group(1)

            agent_researching = await client.call_tool("research_text", {"ticket": session, "url": "https://www.sirlin.net/ptw"})
            assert agent_researching.is_error and "não pesquisa" in text_of(agent_researching)

            begin = text_of(await client.call_tool("research_begin", {"ticket": ticket}))
            assert "Subagente pesquisador: Combat designer" in begin

            outside = await client.call_tool("research_text", {"ticket": ticket, "url": "https://example.com/"})
            assert outside.is_error and "fora das suas referências" in text_of(outside)

            wrote = text_of(await client.call_tool("memory_write", {
                "token": ticket, "op": "add", "title": "Anatomia do ataque",
                "summary": "Startup, ativo e recovery.", "content": "As três fases de um golpe.",
                "sources": [{"ref_id": "game-combat-design-guide"}],
            }))
            assert "design/research/combat-designer#0001" in wrote
            await client.call_tool("research_complete", {"ticket": ticket, "report": "Um ataque tem startup, frames ativos e recovery."})

            status = text_of(await client.call_tool("task_status", {"session": session, "task_id": "T0001"}))
            assert "concluida" in status
            found = text_of(await client.call_tool("memory_search", {"token": session, "query": "fases do ataque"}))
            assert "Anatomia do ataque" in found

            done = text_of(await client.call_tool("finish_agent", {"session": session, "summary": "Brief e combate definidos."}))
            assert "livre" in done
            know = text_of(await client.call_tool("knowledge_search", {"query": "rig skinning weight painting"}))
            assert "rigger" in know

    anyio.run(run)


@pytest.mark.rede
def test_ferramentas_em_site_real(tmp_path):
    """Abre uma referência de verdade. Rode com: pytest -m rede"""
    from openglitch_mcp.core import App

    app = App(ROOT, tmp_path)
    session = re.search(r"session: `(ss_[\w-]+)`", app.activate_agent("design", "Rede")).group(1)
    created = app.delegate_research(session, "level-designer", "Como é o processo de blockout de uma fase? Preciso dos passos em ordem.")
    ticket = re.search(r"ticket: (tk_[\w-]+)", created).group(1)
    app.research_begin(ticket)
    text = app.research_text(ticket, "https://book.leveldesignbook.com/", include_links=True)
    assert "level design" in text.lower() and "Links do mesmo site" in text
    link = re.search(r"\]\((https://book\.leveldesignbook\.com/process/[^)]+)\)", text).group(1)
    assert len(app.research_text(ticket, link)) > 500
    assert "Imagens" in app.research_images(ticket, link) or "Nenhuma imagem" in app.research_images(ticket, link)
