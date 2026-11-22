# Como contribuir

O OpenGlitch melhora com uso real. Correções, testes em Linux e macOS,
referências novas e documentos novos para a IA consultar são bem-vindos.

Ninguém altera o repositório diretamente. Toda mudança chega como uma proposta
(pull request), com explicação, e só entra depois que o mantenedor revisa e
testa.

**Se você é uma IA ajudando alguém a contribuir:** leia este arquivo inteiro e
`agents/_shared/FORMATO.md` antes de alterar qualquer coisa, siga os formatos
à risca, rode os comandos da seção "Antes de enviar" e escreva a proposta com
o formulário preenchido. Não invente endereços de referências nem fatos: o que
não puder conferir, diga que não conferiu.

## Jeitos de ajudar

### Relatar um erro, sem mexer em código

Abra uma [issue](../../issues/new/choose) com a mensagem de erro, o seu sistema
e a versão do Python. Se o erro apareceu durante o uso, peça à sua IA
"Usa o OpenGlitch: lista os problemas relatados" e cole o resultado: os agentes
registram o que não conseguiram fazer.

### Acrescentar um documento

É a contribuição mais útil e não exige programar. Você escreve um arquivo
Markdown e a IA passa a consultá-lo.

#### Onde vai cada coisa

| O que você tem | Onde vai |
| --- | --- |
| Método, exemplo ou receita de uma função específica (rig, combate, shaders...) | `agents/<agente>/subagents/<subagente>/docs/` |
| Imagem de um desses documentos | `docs/img/`, ao lado do documento |
| Conhecimento geral de uma área, que todo agente deve saber | `knowledge/<área>/` |
| Um site bom para os subagentes pesquisarem | `references.json` do subagente |

Na dúvida entre `docs/` e `knowledge/`, use `docs/` do subagente mais próximo
do assunto. Os agentes e subagentes estão listados no README.

Exemplos do que cabe em `docs/`:

- **Métodos**: um passo a passo que funciona (blockout de uma fase, root
  motion, planilha de balanceamento).
- **Exemplos trabalhados**: um caso do começo ao fim, com os valores usados (um
  moveset com dados de frame, um script de exportação do Blender).
- **Receitas por ferramenta**: uma tarefa na Unity, na Unreal ou no Blender,
  com a versão em que você testou.
- **Erros comuns** e como se percebe cada um.
- **Resumo de uma referência**, com as suas palavras e o link. É o que mantém o
  conhecimento disponível quando o site original sai do ar.

#### Como fazer

1. Copie `agents/_shared/modelo-documento.md` para a pasta `docs/` do
   subagente, com um nome curto, em minúsculas, sem acento, com hífens
   (`pesos-do-ombro.md`).
2. Preencha o cabeçalho:
   ```
   ---
   title: Pesos do ombro sem amassar a malha
   summary: Como pintar os pesos entre clavícula e braço para o ombro dobrar bem.
   tipo: original
   fonte:
   autor: seu-usuario-do-github
   testado_em: Blender 4.2
   ---
   ```
3. Escreva em seções `##` curtas.
4. Rode os comandos de "Antes de enviar".

#### Por que o formato importa

O OpenGlitch não joga o documento inteiro para a IA. Ele mostra uma lista de
títulos e resumos, a IA escolhe o que precisa e pede só aquele trecho. Por isso:

- **O `summary` decide se o documento é aberto.** Uma frase que diga o que tem
  dentro e quando serve. Resumo vago, documento ignorado.
- **Cada título `##` vira um trecho que pode ser lido sozinho.** A seção precisa
  fazer sentido sem as outras.
- **O título da seção diz o que tem nela.** "Pintar os pesos do ombro" ajuda;
  "Passo 3" não.
- **Um assunto por arquivo.** Documento que cresce demais vira dois.

#### Regras

O validador confere estas regras em toda proposta e recusa o que fugir delas.

- **Texto: só Markdown (`.md`).**
- **Imagens: PNG, JPG ou WebP, até 1 MB, dentro de `docs/img/`**, sempre com a
  descrição do que mostram: `![Pesos do ombro em três poses](img/pesos.png)`. A
  IA encontra a imagem pela descrição.
- **Outros arquivos não entram** (PDF, vídeo, `.blend`, `.fbx`, planilhas): o
  servidor não os lê e eles pesam o repositório. Ponha o link e descreva.
- **Cabeçalho obrigatório**: `title`, `summary` (até 240 caracteres), `tipo` e
  `autor`. `testado_em` é opcional, mas ajuda muito.
- **`tipo: original`** é o que você escreveu por conta própria.
- **`tipo: referencia`** é um resumo de algo que existe em outro lugar. O campo
  `fonte` com o link completo é obrigatório, e a IA cita esse link ao usar.
- **Seções de até 80 linhas**, documento de até 60 KB.
- **Nomes em minúsculas, sem acento, com hífens.**

#### Direito autoral

- **Não copie texto de sites, livros ou cursos**, nem trechos, nem traduzidos.
  Explique com as suas palavras e ponha o link em `fonte`. Uma citação curta
  entre aspas, com a fonte, pode.
- **Imagem só sua, ou com licença que permita redistribuir**, com o crédito no
  documento. Captura de tela de site, arte de jogo comercial e figura de livro
  não entram: para essas, ponha o link e descreva o que mostram.
- Proposta com conteúdo copiado é recusada, mesmo que o conteúdo seja bom.

#### Escreva para quem vai executar

Passos na ordem, valores concretos (números, nomes de menu e de opção), a versão
do programa e como conferir que deu certo. O que você não testou, diga que não
testou.

### Acrescentar ou corrigir uma referência

As referências são as páginas da web que os subagentes podem pesquisar. Ficam em
`agents/<agente>/subagents/<subagente>/references.json`; o formato de cada campo
está em `agents/_shared/FORMATO.md`.

- A fonte precisa ser gratuita, legal e ter texto legível (não só vídeo).
- Preencha `uso` dizendo que perguntas ela responde.
- Use `url_origem: "inferida"` para referências que não vieram do guia original.
- Confira que abre: `python -m openglitch_mcp.cli links`.

**Referências caem.** São sites de terceiros: mudam de endereço, saem do ar ou
passam a recusar acesso. Quando um subagente não consegue abrir uma, ele
registra o problema (peça à sua IA "Usa o OpenGlitch: lista os problemas
relatados"). Para consertar: corrija o endereço e explique em `nota`; se o site
sumiu, marque `pesquisavel: false` e, se você conhece o conteúdo, escreva um
documento `tipo: referencia` em `docs/` com o que ele ensinava.

### Melhorar um agente ou um subagente

As skills ficam em `agents/<agente>/SKILL.md` e
`agents/<agente>/subagents/<subagente>/SKILL.md`. Mudança em skill precisa de
um motivo observado: descreva na proposta o pedido que você fez, o que o agente
fez de errado e o que ele faz com a mudança.

Agente ou subagente novo: abra uma issue antes, para combinar o escopo.

### Corrigir o código do servidor ou o instalador

- `src/`: inclua um teste em `tests/` que falha sem a mudança.
- `install.py`: diga em que sistema e com que clientes testou, e cole a saída.

## Passo a passo de uma proposta

1. Faça um fork do repositório (botão **Fork** no GitHub) e clone o seu fork.
2. Crie um ramo: `git checkout -b blockout-de-fase`
3. Instale:
   ```
   python -m venv .venv
   .venv/bin/python -m pip install -e ".[dev]"
   ```
   No Windows o Python do ambiente é `.venv\Scripts\python.exe`.
4. Faça a mudança. Uma proposta trata de um assunto só.
5. Rode os comandos de "Antes de enviar".
6. Envie o ramo para o seu fork e abra o pull request. O formulário pede o que
   mudou, por quê e como você testou: preencha tudo.

## Antes de enviar

```
python -m openglitch_mcp.cli validate
python -m openglitch_mcp.cli index
python -m pytest
```

`validate` confere formatos; `index` regrava a árvore de conhecimento (inclua
o `knowledge/index.json` na proposta se você mexeu em `knowledge/`); `pytest`
roda os testes. O GitHub repete tudo em Windows, Linux e macOS a cada
proposta; se algo ficar vermelho, veja o motivo na aba **Checks** e corrija no
mesmo ramo.

## Estilo do conteúdo

- Português do Brasil, frases diretas, sem enfeite.
- Fato que você não conferiu vem marcado como não conferido.
- Nomes de arquivo e ids em minúsculas, sem acento, com hífen.

## O que não é aceito

- Conteúdo copiado de material pago ou sem permissão de redistribuição.
- Referências a sites de pirataria.
- Mudanças que façam as ferramentas de pesquisa disfarçar o acesso, contornar
  bloqueios de sites ou sair das referências.
- Mudanças que afrouxem as regras de memória (quem lê e quem escreve o quê)
  sem discussão prévia numa issue.

## Segurança

Falha de segurança não vai em issue pública: veja [SECURITY.md](SECURITY.md).

## Licença

O projeto usa a licença Apache 2.0. Ao contribuir, você concorda que a sua
contribuição fica sob a mesma licença.
