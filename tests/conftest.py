import re
from pathlib import Path

import pytest

from openglitch_mcp.core import App

ROOT = Path(__file__).resolve().parents[1]

BRIEF = "# Jogo de teste\n\n## Visão\n" + "Um jogo de ação em terceira pessoa com cenas dirigidas. " * 8


@pytest.fixture
def app(tmp_path):
    return App(ROOT, tmp_path)


def session_of(text: str) -> str:
    return re.search(r"session: `(ss_[\w-]+)`", text).group(1)


def ticket_of(text: str) -> str:
    return re.search(r"ticket: (tk_[\w-]+)", text).group(1)


def task_id_of(text: str) -> str:
    return re.search(r"Tarefa (T\d+)", text).group(1)


@pytest.fixture
def helpers():
    class H:
        session_of = staticmethod(session_of)
        ticket_of = staticmethod(ticket_of)
        task_id_of = staticmethod(task_id_of)
        brief = BRIEF

    return H


@pytest.fixture
def project(app):
    """Projeto com brief publicado e nenhum agente ativo."""
    design = session_of(app.activate_agent("design", "Jogo Teste"))
    app.publish_project_brief(design, BRIEF)
    app.finish_agent(design, "Brief publicado.", "Arte 3D pode começar.")
    return "jogo-teste"
