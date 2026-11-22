# OpenGlitch

Um PageIndex sobre criação de jogos 3D cinematográficos e uma equipe de agentes
de IA que o usam, servidos por MCP. Você conecta o Claude, o Codex ou outro
cliente MCP a este servidor; a IA analisa o seu pedido, assume o agente certo
(design, arte 3D, animação, cinematics, engenharia, áudio ou apoio) e trabalha
no seu jogo seguindo a skill daquele agente.

O conteúdo vem do guia `Guia Equipes e estudo para um jogo 3D cinematográfico.pdf`
(transcrito em `sources/guia-pdf.md`). O que no guia era "como estudar" virou o
modo de trabalhar dos agentes e as referências de pesquisa dos subagentes.

## Como funciona

```
usuário ──> IA ──start──> roteador: analisa o pedido e escolhe o agente
                 │
                 ├─ activate_agent ──> a IA vira o agente (skill + brief + memória)
                 │       │
                 │       ├─ consulta a memória (memory_search / memory_tree)
                 │       ├─ faltou algo: delegate_research ──> subagente (em paralelo)
                 │       │        └─ pesquisa nas referências dele:
                 │       │           research_text / research_tables / research_images
                 │       │           grava na própria memória e entrega o relatório
                 │       ├─ constrói (com as ferramentas do cliente)
                 │       └─ registra na memória de trabalho
                 └─ finish_agent ──> recado para o próximo agente
```

- **Agente constrói, subagente pesquisa.** O agente não abre as referências; o
  subagente não constrói, não escreve código e não fala com o usuário.
- **Todo projeto começa pelo Design**, que conversa com você até entender o jogo
  e publica o brief. Sem brief o servidor não ativa nenhum outro agente.
- **Um agente por vez** em cada projeto. Os subagentes dele podem pesquisar ao
  mesmo tempo que ele trabalha.
- **Na segunda vez não se pesquisa de novo**: o agente olha a memória antes de
  delegar.
- **O agente `leitor`** só lê. Serve para perguntar como o projeto está e para
  descobrir que agente, ou que sequência de agentes, atende um pedido.

## Agentes e subagentes

| Agente | Subagentes pesquisadores |
| --- | --- |
| `design` | game-designer, combat-designer, level-designer, narrative-designer, ux-ui-designer |
| `arte-3d` | concept-artist, character-artist, environment-artist, props-hard-surface, texture-material, lighting-artist, vfx-artist, technical-artist |
| `animacao` | rigger, gameplay-animator, cinematic-animator, mocap-cleanup, facial-animation, animation-td, cloth-hair-physics |
| `cinematics` | cinematic-director, layout-camera, scene-animator, editor, lighting-comp |
| `engenharia` | gameplay-programmer, engine-graphics, ai-programmer, tools-programmer, network-programmer, build-devops |
| `audio` | sound-designer, composer, voice-over, audio-programmer |
| `apoio` | qa, localization, marketing-publisher |
| `leitor` | nenhum: só lê as memórias |

A liderança do guia (diretor criativo, produtor, diretores de arte, técnico e de
animação) não é um agente. A visão e o escopo ficam com o `design` e com você; a
direção de arte, a técnica e a de animação ficam com os agentes dessas áreas. O
conteúdo está em `knowledge/lideranca/`.

## Memória

Cada memória é um PageIndex: uma árvore de nós com título, resumo, conteúdo,
fontes e histórico. O servidor decide quem acessa o quê:

| Quem | Lê | Escreve |
| --- | --- | --- |
| Subagente | Só a própria memória, e só se o agente ligou `memory_access` na tarefa | Só a própria memória |
| Agente | A memória de todos os seus subagentes e a sua memória de trabalho | Só a sua memória de trabalho |
| Leitor | Todas, de todos os agentes | Nada |

Um agente não vê a memória de outro. O que passa de um para o outro é o brief
do projeto e o recado de encerramento (`finish_agent`).

A memória de pesquisa dos subagentes vale para todos os projetos; a memória de
trabalho de cada agente é separada por projeto. Tudo fica em `memory/`, fora do
git.

## As três ferramentas de pesquisa

Só subagentes as usam, e só em páginas das próprias referências, em links
encontrados dentro delas ou em URLs que o agente incluiu na tarefa.

- **`research_text`**: o corpo do artigo em Markdown, com os títulos, sem menu
  nem rodapé (Trafilatura).
- **`research_tables`**: só as tabelas, convertidas para Markdown
  (BeautifulSoup acha cada `<table>`, `pandas.read_html` converte).
- **`research_images`** e **`research_view_image`**: só as imagens de conteúdo.
  O filtro (BeautifulSoup) descarta ícones, logos, avatares, banners, SVGs
  pequenos e tudo abaixo do tamanho mínimo (300 px por padrão). A imagem é
  baixada temporariamente para a IA olhar e descrever; fica guardado só o link
  original e a descrição.

O servidor se identifica como ferramenta ao abrir páginas. Sites que recusam
acesso automatizado não são contornados: a referência fica marcada como não
pesquisável. PDF e vídeo também não são lidos.

## Instalação

Precisa de Python 3.11 ou mais novo.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```

## Conectar um cliente

O servidor fala MCP por stdio. O comando é o Python do ambiente virtual com
`-m openglitch_mcp`. Troque `D:\OpenGlitch` pelo caminho da pasta.

**Claude Code**

```powershell
claude mcp add openglitch -- D:\OpenGlitch\.venv\Scripts\python.exe -m openglitch_mcp
```

**Claude Desktop** (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "openglitch": {
      "command": "D:\\OpenGlitch\\.venv\\Scripts\\python.exe",
      "args": ["-m", "openglitch_mcp"]
    }
  }
}
```

**Codex** (`~/.codex/config.toml`)

```toml
[mcp_servers.openglitch]
command = "D:\\OpenGlitch\\.venv\\Scripts\\python.exe"
args = ["-m", "openglitch_mcp"]
```

Variáveis de ambiente opcionais: `OPENGLITCH_DATA` (onde ficam `memory/` e
`state/`; o padrão é a pasta do projeto) e `OPENGLITCH_HOME` (onde estão
`agents/` e `knowledge/`).

## Como pedir

- "Usa o OpenGlitch: quero criar um jogo de ação em terceira pessoa com cenas
  tipo série." A IA assume o `design` e começa a entrevista.
- "Usa o OpenGlitch e seja o agente de animação: monta a animation list do
  protagonista."
- "Usa o OpenGlitch: como está o projeto?" A IA assume o `leitor`.
- "Usa o OpenGlitch: quero o primeiro personagem jogável." A IA monta a
  sequência do pipeline de personagem e segue um agente de cada vez.
- "Usa o OpenGlitch, agente de engenharia em modo consulta: qual a diferença
  entre state machine e behavior tree?"

## Ferramentas MCP

| Grupo | Ferramentas |
| --- | --- |
| Roteamento | `start`, `project_status`, `plan_agents`, `get_pipeline` |
| Agente | `activate_agent`, `finish_agent`, `publish_project_brief` |
| Conhecimento | `knowledge_tree`, `knowledge_read`, `knowledge_search` |
| Memória | `memory_tree`, `memory_search`, `memory_read`, `memory_write` |
| Delegação | `delegate_research`, `task_status` |
| Subagente | `research_begin`, `research_text`, `research_tables`, `research_images`, `research_view_image`, `research_complete` |

## Pastas

```
agents/      skills e referências: um agente por pasta, um subagente por subpasta
  _shared/   roteador, protocolos comuns e o contrato de formato (FORMATO.md)
knowledge/   o PageIndex de conhecimento, em Markdown (index.json é a árvore gerada)
pipelines/   fluxos entre agentes (personagem, animação em jogo)
src/         o servidor MCP
tests/       testes das regras, das ferramentas e do fluxo por MCP
sources/     transcrição do guia em PDF
memory/      criada em uso: memórias e projetos (fora do git)
state/       criada em uso: sessões e tarefas (fora do git)
```

## Manutenção do conteúdo

```powershell
.\.venv\Scripts\python.exe -m openglitch_mcp.cli validate
```

```powershell
.\.venv\Scripts\python.exe -m openglitch_mcp.cli index
```

```powershell
.\.venv\Scripts\python.exe -m openglitch_mcp.cli links
```

`validate` confere agentes, referências, pipelines e documentos. `index` regrava
`knowledge/index.json`. `links` abre cada referência pesquisável e lista as que
falham. Para acrescentar um agente, um subagente ou uma referência, siga
`agents/_shared/FORMATO.md` e rode `validate`.

## Limites conhecidos

- As permissões valem por credencial: o agente tem um `session` e cada
  subagente um `ticket` de uma tarefa. Um cliente sem subagentes nativos
  executa a pesquisa na mesma conversa, alternando de papel com o ticket.
- Várias referências do guia são livros pagos, canais de vídeo ou PDFs. Elas
  continuam listadas como leitura recomendada, mas os subagentes não as abrem.
- Alguns links do guia estavam errados ou fora do ar e foram corrigidos; cada
  correção está explicada no campo `nota` da referência.
