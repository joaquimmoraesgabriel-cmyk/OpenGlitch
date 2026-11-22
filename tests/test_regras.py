"""Regras que o servidor precisa garantir, independente do que a IA tente fazer."""

import pytest

from openglitch_mcp.cli import validate
from openglitch_mcp.util import OGError

TASK = "Quais são as fases de um ataque corpo a corpo e que faixas de frames usar? Vou montar o moveset."


def test_conteudo_valido(app):
    assert validate(app) == []
    workers = [a.id for a in app.registry.workers()]
    assert workers == ["design", "arte-3d", "animacao", "cinematics", "engenharia", "audio", "apoio"]
    assert sum(len(a.subagents) for a in app.registry.workers()) == 38
    assert app.registry.agent("leitor").kind == "reader"


def test_start_lista_agentes_e_pipelines(app):
    text = app.start("quero criar um jogo de luta")
    for agent_id in app.registry.agents:
        assert f"`{agent_id}`" in text
    assert "`personagem`" in text and "quero criar um jogo de luta" in text


# ------------------------------------------------------------- conhecimento


def test_pageindex_de_conhecimento(app):
    tree = app._knowledge_tree()
    assert "`design`" in tree and "`pipelines`" in tree
    assert "`design/combat-designer`" in app._knowledge_tree("design")
    doc = app._knowledge_read("design/game-designer")
    assert "Core loop" in doc and "design/game-designer#referencias" in doc
    assert "gamebalanceconcepts" in app._knowledge_read("design/game-designer#referencias")
    assert "pipelines/personagem" in app._knowledge_search("retopologia edge loops")
    with pytest.raises(OGError):
        app._knowledge_read("nao/existe")


# ------------------------------------------------- design primeiro, um por vez


def test_projeto_novo_so_nasce_com_design(app, helpers):
    with pytest.raises(OGError, match="design"):
        app.activate_agent("arte-3d", "Jogo Novo")
    design = helpers.session_of(app.activate_agent("design", "Jogo Novo"))
    with pytest.raises(OGError, match="não tem brief"):
        app.activate_agent("arte-3d", "Jogo Novo")
    with pytest.raises(OGError, match="Só um agente trabalha por vez"):
        app.activate_agent("design", "Jogo Novo")
    app.finish_agent(design, "Entrevista feita, brief ainda não publicado.")
    with pytest.raises(OGError, match="não tem brief"):
        app.activate_agent("arte-3d", "Jogo Novo")


def test_so_design_publica_brief(app, project, helpers):
    arte = helpers.session_of(app.activate_agent("arte-3d", project))
    with pytest.raises(OGError, match="Só o agente `design`"):
        app.publish_project_brief(arte, helpers.brief)


def test_um_agente_por_vez_e_takeover(app, project, helpers):
    text = app.activate_agent("arte-3d", project)
    assert "Brief (versão 1)" in text and "Arte 3D pode começar" in text
    with pytest.raises(OGError, match="arte-3d"):
        app.activate_agent("animacao", project)
    anim = helpers.session_of(app.activate_agent("animacao", project, takeover=True))
    with pytest.raises(OGError, match="encerrada"):
        app.memory_tree(helpers.session_of(text))
    app.finish_agent(anim, "Rig pronto.")
    assert "interrompido" in app.project_status(project)


def test_plano_de_agentes(app, project, helpers):
    with pytest.raises(OGError, match="começar pelo agente `design`"):
        app.plan_agents("Outro Jogo", ["arte-3d"], "personagem")
    app.plan_agents(project, ["arte-3d", "animacao"], "personagem jogável")
    arte = helpers.session_of(app.activate_agent("arte-3d", project))
    assert "Próximo agente do plano: `animacao`" in app.finish_agent(arte, "Modelo pronto.")
    anim = helpers.session_of(app.activate_agent("animacao", project))
    assert "plano de agentes do projeto foi concluído" in app.finish_agent(anim, "Animado.")


def test_modo_consulta_nao_precisa_de_projeto(app, helpers):
    text = app.activate_agent("animacao", mode="consulta")
    sess = helpers.session_of(text)
    assert "Modo consulta" in text
    with pytest.raises(OGError, match="memória de trabalho"):
        app.memory_write(sess, "add", title="x", summary="y", content="z")
    assert "T0001" in app.delegate_research(sess, "rigger", "Como estruturar o esqueleto de jogo para a Unity Humanoid?")


# ------------------------------------------------------- agente x subagente


def test_agente_nao_pesquisa(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    for call in (app.research_begin, lambda t: app.research_text(t, "https://www.sirlin.net/ptw"),
                 lambda t: app.research_tables(t, "https://www.sirlin.net/ptw")):
        with pytest.raises(OGError, match="O agente não pesquisa"):
            call(design)


def test_delegacao_valida_subagente_e_referencias(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    with pytest.raises(OGError, match="não tem o subagente"):
        app.delegate_research(design, "rigger", TASK)
    with pytest.raises(OGError, match="Referências desconhecidas"):
        app.delegate_research(design, "combat-designer", TASK, reference_ids=["nao-existe"])
    with pytest.raises(OGError, match="vaga demais"):
        app.delegate_research(design, "combat-designer", "combate")


def test_memoria_do_subagente_com_acesso_desligado(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    created = app.delegate_research(design, "combat-designer", TASK, memory_access=False)
    ticket, task_id = helpers.ticket_of(created), helpers.task_id_of(created)
    begin = app.research_begin(ticket)
    assert "Acesso DESLIGADO" in begin and "Subagente pesquisador: Combat designer" in begin
    assert "Protocolo comum dos subagentes" in begin
    for call in (lambda: app.memory_tree(ticket), lambda: app.memory_search(ticket, "ataque"),
                 lambda: app.memory_read(ticket, "0001")):
        with pytest.raises(OGError, match="desligou o acesso"):
            call()
    with pytest.raises(OGError, match="ainda não atualizou"):
        app.research_complete(ticket, "Resposta: as fases são startup, ativo e recovery. " * 2)
    written = app.memory_write(
        ticket, "add", title="Anatomia do ataque", summary="Fases startup, ativo e recovery.",
        content="Startup: antecipação. Ativo: a hitbox existe. Recovery: o personagem fica exposto.",
        sources=[{"ref_id": "game-combat-design-guide", "url": "https://gamedesignskills.com/game-design/combat-design/"}],
        images=[{"url": "https://exemplo.test/diagrama.png", "description": "Linha do tempo com as três fases."}],
    )
    assert "design/research/combat-designer#0001" in written
    app.research_complete(ticket, "Resposta: as fases são startup, ativo e recovery. " * 2, gaps="Sem valores para tiro.")
    with pytest.raises(OGError, match="já foi concluída"):
        app.memory_write(ticket, "add", title="a", summary="b", content="c")
    status = app.task_status(design, task_id)
    assert "concluida" in status and "design/research/combat-designer#0001" in status
    assert "Sem valores para tiro" in status
    node = app.memory_read(design, "design/research/combat-designer#0001")
    assert "Recovery" in node and "diagrama.png" in node and "game-combat-design-guide" in node


def test_memoria_do_subagente_com_acesso_ligado(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    first = helpers.ticket_of(app.delegate_research(design, "combat-designer", TASK))
    app.research_begin(first)
    app.memory_write(first, "add", title="Hitstop", summary="Pausa curta no impacto.", content="Congela os dois personagens por poucos frames.")
    app.research_complete(first, "Hitstop é a pausa no impacto que dá peso ao golpe. " * 2)

    second = helpers.ticket_of(app.delegate_research(design, "combat-designer", TASK, memory_access=True))
    begin = app.research_begin(second)
    assert "Acesso LIGADO" in begin and "Hitstop" in begin
    assert "Hitstop" in app.memory_search(second, "hitstop impacto")
    app.memory_write(second, "correct", node="0001", content="Congela atacante e alvo por 3 a 8 frames.", reason="Faltava a faixa de frames.")
    read = app.memory_read(second, "0001")
    assert "3 a 8 frames" in read and "Faltava a faixa de frames" in read and "revisão 2" in read
    # O subagente só enxerga a própria partição.
    with pytest.raises(OGError, match="não tem acesso"):
        app.memory_read(second, "design/research/game-designer#0001")
    with pytest.raises(OGError, match="só escreve em"):
        app.memory_write(second, "update", node="design/research/game-designer#0001", content="x")
    with pytest.raises(OGError, match="só escreve em"):
        app.memory_write(second, "update", node="design/work#0001", content="x")


def test_isolamento_entre_subagentes_e_agentes(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    t_combat = helpers.ticket_of(app.delegate_research(design, "combat-designer", TASK, memory_access=True))
    t_level = helpers.ticket_of(app.delegate_research(design, "level-designer", "Como guiar o jogador sem seta na tela? Preciso das técnicas com exemplos.", memory_access=True))
    app.research_begin(t_combat)
    app.research_begin(t_level)
    app.memory_write(t_combat, "add", title="Telegraph", summary="Aviso do ataque.", content="O inimigo anuncia o golpe.")
    app.memory_write(t_level, "add", title="Landmarks", summary="Pontos de referência.", content="Uma torre visível guia o jogador.")
    assert "Telegraph" not in app.memory_tree(t_level) and "Landmarks" in app.memory_tree(t_level)
    assert "Landmarks" not in app.memory_tree(t_combat)

    # O agente vê os dois; e tem a memória de trabalho, que os subagentes não veem.
    tree = app.memory_tree(design)
    assert "Telegraph" in tree and "Landmarks" in tree
    app.memory_write(design, "add", title="Decisão: combate corpo a corpo", summary="Sem armas de fogo.", content="Pilar: combate pesado.")
    assert "design/work" not in app.memory_tree(t_combat)
    # O agente não escreve na memória de pesquisa.
    with pytest.raises(OGError, match="só escreve em"):
        app.memory_write(design, "update", node="design/research/combat-designer#0001", content="x")
    app.finish_agent(design, "Combate definido.")

    # Outro agente não vê nada do design.
    arte = helpers.session_of(app.activate_agent("arte-3d", project))
    arte_tree = app.memory_tree(arte)
    assert "Telegraph" not in arte_tree and "Decisão" not in arte_tree
    with pytest.raises(OGError, match="não tem acesso"):
        app.memory_read(arte, "design/work#0001")
    with pytest.raises(OGError, match="não tem acesso"):
        app.memory_read(arte, "design/research/combat-designer#0001")
    # Um ticket do design não serve para o subagente escrever em arte-3d.
    with pytest.raises(OGError):
        app.memory_write(t_combat, "add", title="x", summary="y", content="z", parent="arte-3d/research/rigger#0001")
    app.finish_agent(arte, "Nada feito.")

    # O leitor lê tudo e não escreve.
    leitor = helpers.session_of(app.activate_agent("leitor", project))
    all_tree = app.memory_tree(leitor)
    assert "Telegraph" in all_tree and "Landmarks" in all_tree and "Decisão: combate" in all_tree
    assert "Pilar: combate pesado" in app.memory_read(leitor, "design/work#0001")
    assert "design/work" in app.memory_tree(leitor, scope="design/work")
    with pytest.raises(OGError, match="não escreve"):
        app.memory_write(leitor, "add", title="x", summary="y", content="z")
    with pytest.raises(OGError, match="só lê memórias"):
        app.delegate_research(leitor, "combat-designer", TASK)
    # O leitor não bloqueia o projeto.
    app.activate_agent("animacao", project)


def test_urls_fora_das_referencias_sao_recusadas(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    created = app.delegate_research(design, "combat-designer", TASK, reference_ids=["sirlin-playing-to-win"])
    ticket = helpers.ticket_of(created)
    with pytest.raises(OGError, match="research_begin"):
        app.research_text(ticket, "https://www.sirlin.net/ptw")
    assert "use só elas" in app.research_begin(ticket)
    for url in ("https://example.com/artigo", "https://www.evozon.com/combat-system-design/",
                "http://127.0.0.1:8000/", "file:///etc/passwd", "https://sirlin.net.evil.example/x"):
        with pytest.raises(OGError, match="fora das suas referências"):
            app.research_text(ticket, url)
    with pytest.raises(OGError, match="research_images listou"):
        app.research_view_image(ticket, "https://www.sirlin.net/qualquer.png")


def test_operacoes_de_memoria(app, project, helpers):
    design = helpers.session_of(app.activate_agent("design", project))
    app.memory_write(design, "add", title="Pilares", summary="Três pilares.", content="Combate pesado.")
    app.memory_write(design, "add", title="Pilar 1", summary="Combate.", content="Detalhe.", parent="0001")
    app.memory_write(design, "append", node="design/work#0001", content="Exploração curta.")
    assert "Exploração curta" in app.memory_read(design, "design/work#0001")
    with pytest.raises(OGError, match="precisa de `reason`"):
        app.memory_write(design, "remove", node="0002")
    app.memory_write(design, "remove", node="0002", reason="Fundido no nó de pilares.")
    tree = app.memory_tree(design, scope="work")
    assert "Pilares" in tree and "Pilar 1" not in tree
    assert "foi removido" in app.memory_read(design, "design/work#0002")
    with pytest.raises(OGError, match="não existe"):
        app.memory_write(design, "update", node="0009", content="x")
    with pytest.raises(OGError, match="Operação"):
        app.memory_write(design, "apagar", node="0001")


def test_pipeline(app):
    assert "`personagem`" in app.get_pipeline()
    text = app.get_pipeline("personagem")
    assert "## 6. Rig e skinning" in text and "`animacao` (rigger)" in text
    assert "design -> arte-3d -> animacao -> engenharia" in text


def test_problemas_relatados(app, project, helpers):
    arte = helpers.session_of(app.activate_agent("arte-3d", project))
    with pytest.raises(OGError, match="kind"):
        app.report_problem(arte, "Exportar o FBX do personagem", "Rodei o Blender em segundo plano", kind="falhou")
    out = app.report_problem(
        arte, "Exportar o FBX do personagem", "Rodei blender --background --python exportar.py",
        kind="bloqueou", error="blender: command not found", software="Blender")
    assert "P0001" in out and "diga isso ao usuário" in out
    ticket = helpers.ticket_of(app.delegate_research(
        arte, "character-artist", "Como fazer retopologia para um personagem que dobra bem? Preciso dos loops."))
    app.research_begin(ticket)
    app.report_problem(ticket, "A referência recusou o acesso", "Abri a página com research_text", error="403")
    done = app.finish_agent(arte, "Modelo low-poly escrito.", not_verified="Script de exportação escrito, não rodado.")
    assert "Aviso" not in done
    listed = app.list_problems(project)
    assert "P0001" in listed and "command not found" in listed and "em Blender" in listed
    assert "arte-3d/character-artist" in listed
    assert "Problemas relatados: 2" in app.project_status(project)
    nxt = app.activate_agent("animacao", project)
    assert "Feito SEM conferir: Script de exportação escrito, não rodado." in nxt
    assert "Aviso: você não disse" in app.finish_agent(helpers.session_of(nxt), "Rig feito.")
    assert "Nenhum problema" in app.list_problems("outro-projeto")
