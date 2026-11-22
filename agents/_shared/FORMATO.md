# Formato dos agentes, subagentes e do conhecimento

Este arquivo é o contrato de dados do OpenGlitch. O servidor MCP lê estas pastas
ao iniciar; o validador (`python scripts/validate.py`) recusa o que fugir daqui.

## Pastas

```
agents/
  _shared/
    protocolo-agente.md        anexado à skill de todo agente que trabalha
    protocolo-subagente.md     anexado à skill de todo subagente
    roteador.md                devolvido pela ferramenta `start`
  <agente>/
    agent.json                 identidade, subagentes, referências compartilhadas
    SKILL.md                   como o agente trabalha e quando chama cada subagente
    subagents/<subagente>/
      SKILL.md                 como o subagente pesquisa
      references.json          as referências que ele pode pesquisar
knowledge/
  <area>/_area.md              visão da área (vira o nó-pai no PageIndex)
  <area>/<subtopico>.md        um documento por subtópico
pipelines/<nome>.json          fluxos entre agentes (ex.: personagem)
```

IDs são sempre minúsculos, sem acento, com hífen: `arte-3d`, `game-designer`.

## agent.json

```json
{
  "id": "design",
  "name": "Design",
  "kind": "worker",
  "summary": "Uma frase: o que este agente constrói.",
  "when_to_use": "Em que pedidos do usuário este agente é o certo.",
  "mandatory_first": false,
  "shared_references": [ { "...": "mesmo formato de references.json" } ],
  "subagents": [
    {
      "id": "game-designer",
      "name": "Game designer",
      "purpose": "Uma frase: que tipo de pergunta ele responde.",
      "knowledge_node": "design/game-designer"
    }
  ]
}
```

- `kind`: `worker` (constrói) ou `reader` (só lê memórias; não tem subagentes).
- `shared_references`: referências que valem para todos os subagentes do agente
  (a base da área e as fontes da liderança correspondente).
- `knowledge_node`: caminho do documento em `knowledge/`, sem `.md`.

## references.json

```json
{
  "agent": "design",
  "subagent": "game-designer",
  "references": [
    {
      "id": "game-design-concepts",
      "title": "Game Design Concepts",
      "author": "Ian Schreiber",
      "type": "curso",
      "url": "https://gamedesignconcepts.wordpress.com/",
      "url_origem": "corrigida",
      "pesquisavel": true,
      "uso": "Para que serve nesta pesquisa: que perguntas esta fonte responde bem.",
      "nota": "Opcional: avisos (link corrigido, site instável, licença)."
    }
  ]
}
```

- `type`: `site`, `blog`, `livro-online`, `livro`, `curso`, `documentacao`, `artigo`,
  `wiki`, `forum`, `palestra`, `video`, `ferramenta`, `banco-de-dados`.
- `url`: `https://...` completa, ou `null` quando não existe versão online legal.
- `url_origem`:
  - `pdf`: é o hiperlink do guia em PDF, sem alteração;
  - `dominio-pdf`: o guia cita só o domínio; virou `https://dominio/`;
  - `corrigida`: o hiperlink do guia apontava para o lugar errado (explique em `nota`);
  - `inferida`: o guia cita a fonte sem link; é a página oficial conhecida.
    Só use quando tiver certeza do endereço. Na dúvida, `url: null`.
- `pesquisavel`: `true` só se a página tem texto que a ferramenta consegue ler.
  Livro pago, canal do YouTube e vídeo de palestra são `false` (as ferramentas
  não leem vídeo), mesmo quando têm `url`.
- Uma referência com `pesquisavel: false` continua na lista: o subagente a cita
  como leitura recomendada, mas não tenta abrir.

O servidor só deixa o subagente abrir páginas dos domínios das referências
pesquisáveis dele (as próprias mais as `shared_references` do agente), links
encontrados dentro dessas páginas e URLs extras que o agente passar na delegação.

## SKILL.md do agente

Frontmatter com `name` (`openglitch-<agente>`) e `description`. Corpo, nesta ordem:

1. `# Agente <Nome>` e um parágrafo de papel.
2. `## O que você constrói`: os entregáveis concretos da área.
3. `## Como você trabalha`: o fluxo específico da área (o protocolo comum, com as
   ferramentas, é anexado pelo servidor; não repita a mecânica das ferramentas).
4. `## Conversa com o usuário`: o que precisa ser perguntado e decidido por ele.
5. `## Seus subagentes`: uma subseção `### <id>` por subagente com: para que
   serve, quando chamar, e dois ou três exemplos de tarefa de pesquisa bem
   formulada.
6. `## Pipelines`: em que etapas dos pipelines o agente entra e o que recebe e
   entrega em cada uma.
7. `## O que registrar na memória de trabalho`.
8. `## Limites`: o que é de outro agente.

## SKILL.md do subagente

Frontmatter com `name` (`openglitch-<agente>-<subagente>`) e `description`. Corpo:

1. `# Subagente pesquisador: <Nome>` e um parágrafo de papel (só pesquisa).
2. `## Domínio`: os temas que ele cobre.
3. `## Como pesquisar`: por qual referência começar para cada tipo de pergunta,
   o que cada fonte tem de melhor, quando vale pedir tabelas ou imagens.
4. `## O que extrair`: lista do que não pode faltar na entrega (números,
   definições, processos, exemplos, armadilhas).
5. `## Como organizar a memória`: árvore de tópicos sugerida para a memória dele.
6. `## Fora do domínio`: o que pertence a outro subagente.

O guia em PDF foi escrito para uma pessoa estudar. Nas skills, "como aprender"
vira o que o subagente precisa encontrar e explicar, e "pra praticar" vira o
teste que o agente usa para saber se o que construiu está certo.

## Documentos de conhecimento

`knowledge/<area>/<subtopico>.md`, com frontmatter `title` e `summary` (uma
frase; aparece na árvore do PageIndex). Corpo com seções `##`:

- `## O que faz`
- `## O que entrega`
- `## Fundamentos` (do "como aprender" do guia)
- `## Como validar` (do "pra praticar" do guia, como critério de aceite)
- `## Ligações com outras áreas`

Não liste as fontes no documento: o servidor gera o nó "Referências" a partir
do `references.json`. Cada `##` vira um nó do PageIndex; mantenha cada seção
autocontida e curta.
