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

### Acrescentar um documento de conhecimento

É a contribuição mais útil e não exige programar. A base de conhecimento fica
em `knowledge/`, em Markdown. Cada arquivo e cada título `##` vira um nó que a
IA encontra pela árvore ou pela busca.

Exemplos do que cabe:

- **Métodos**: um passo a passo que funciona (como fazer blockout de uma fase,
  como configurar root motion, como montar uma planilha de balanceamento).
- **Exemplos trabalhados**: um caso do começo ao fim, com os valores usados e
  o resultado (um moveset com dados de frame, um script de exportação do
  Blender, a configuração de um Animator).
- **Receitas por ferramenta**: como fazer uma tarefa na Unity, na Unreal, no
  Blender ou em outro programa, com a versão em que você testou.
- **Erros comuns** e como se percebe cada um.

Como fazer:

1. Escolha a pasta da área (`knowledge/design/`, `knowledge/animacao/`...). Para
   um tema que não cabe em nenhuma, crie uma pasta nova com um `_area.md`.
2. Crie um arquivo `.md` com nome curto, minúsculo, sem acento, com hífens.
3. Comece com o cabeçalho:
   ```
   ---
   title: Blockout de uma fase em uma tarde
   summary: Passo a passo para sair do mapa 2D e chegar a uma fase jogável só com cubos.
   ---
   ```
   O `summary` é uma frase: é o que a IA lê para decidir se abre o documento.
4. Divida em seções `##` curtas e autocontidas. Cada seção precisa fazer
   sentido sozinha, porque a IA pode ler só ela.
5. Escreva para uma IA que vai executar: ordem dos passos, valores concretos,
   como conferir que deu certo. Diga a versão do programa quando importar.
6. Diga na proposta de onde veio a informação (experiência sua, documentação
   oficial, um artigo) e o que você testou.

Só entra conteúdo seu ou de fonte que permita redistribuir. Não copie trechos
de livros, cursos pagos ou artigos: explique com as suas palavras e cite a
fonte.

### Acrescentar ou corrigir uma referência

As referências são as páginas que os subagentes podem pesquisar. Ficam em
`agents/<agente>/subagents/<subagente>/references.json`.

- A fonte precisa ser gratuita, legal e ter texto legível (não só vídeo).
- Preencha `uso` dizendo que perguntas ela responde.
- Use `url_origem: "inferida"` para referências que não vieram do guia original.
- Confira que abre: `python -m openglitch_mcp.cli links`.
- Link que parou de funcionar: corrija o endereço e explique em `nota`.

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
