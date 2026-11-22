# Como contribuir

O OpenGlitch foi testado principalmente no Windows. Testes em Linux e macOS,
correções e referências novas são bem-vindos.

Ninguém altera o repositório diretamente. Toda mudança chega como uma proposta
(pull request), com explicação, e só entra depois que o mantenedor revisa e
testa.

## Achou um erro e não quer mexer no código

Abra uma [issue](../../issues/new/choose) com a mensagem de erro, o seu sistema
e a versão do Python. Já ajuda muito.

## Quer mandar uma correção

1. Faça um fork do repositório (botão **Fork** no GitHub) e clone o seu fork.
2. Crie um ramo para a mudança: `git checkout -b corrige-instalador-linux`
3. Instale e rode os testes:
   ```
   python -m venv .venv
   .venv/bin/python -m pip install -e ".[dev]"     # no Windows: .venv\Scripts\python.exe
   .venv/bin/python -m pytest
   .venv/bin/python -m openglitch_mcp.cli validate
   ```
4. Faça a mudança. Uma proposta trata de um assunto só.
5. Envie o ramo para o seu fork e abra o pull request. O formulário pede o que
   mudou, por quê e como você testou: preencha tudo.

O GitHub roda os testes sozinho em Windows, Linux e macOS a cada proposta. Se
algum ficar vermelho, veja o motivo na aba **Checks** e corrija no mesmo ramo.

## O que cada tipo de mudança pede

- **Código do servidor** (`src/`): um teste em `tests/` que falha sem a mudança.
- **Agente, subagente ou referência** (`agents/`): siga
  `agents/_shared/FORMATO.md` e rode `validate`. Referência nova precisa ser
  gratuita e legal; diga no campo `uso` o que ela responde.
- **Base de conhecimento** (`knowledge/`): cite de onde veio a informação na
  proposta e rode `python -m openglitch_mcp.cli index`.
- **Instalador** (`install.py`): diga em que sistema e com que clientes testou,
  e cole a saída.

## Regras das ferramentas de pesquisa

O servidor se identifica como ferramenta ao abrir páginas e respeita a recusa
dos sites. Propostas que disfarcem o acesso, contornem bloqueios ou leiam
conteúdo pago não são aceitas.

## Licença

Ao contribuir, você concorda que a sua contribuição fica sob a licença do
projeto (Apache 2.0).
