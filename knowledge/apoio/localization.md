---
title: Localização
summary: Adapta o jogo para outras línguas e culturas: tradução, fontes, tamanho do texto, cores e símbolos, e o teste do jogo traduzido.
---

## O que faz

Adapta o jogo para outras línguas e culturas. Cobre tradução, piadas,
referências, fontes, tamanho do texto na tela, cores e símbolos.

## O que entrega

- **Textos traduzidos e revisados**.
- **Kit de localização**: contexto, glossário e guia de estilo.
- **Teste do jogo traduzido** (LQA).
- **Página da loja traduzida**.

## Fundamentos

- Preparar o jogo desde o início: todo texto em arquivo separado, nada no
  código e nada dentro de imagem.
- UTF-8 e fontes com acento e com os caracteres de cada idioma.
- Interface que aguenta textos maiores: reservar espaço extra, porque a
  tradução costuma ocupar mais espaço que o original.
- Contexto para o tradutor: uma frase solta pode ter várias traduções.
- O pacote Localization da Unity organiza strings e a troca de idioma.
- Lançar com português do Brasil e inglês desde o primeiro dia já coloca o
  jogo à frente de muito indie estrangeiro.

## Como validar

- O jogo roda em português e inglês, com troca de idioma no menu.
- Nenhum texto está no código nem em imagem: trocar o idioma muda tudo o que o
  jogador lê.
- Nenhum texto fica cortado ou sobreposto na interface, em nenhum idioma.
- Acentos e caracteres especiais aparecem corretos em todas as fontes usadas.
- Cada string da planilha tem id, contexto e limite de caracteres, e o
  glossário foi aplicado.
- A página da loja existe em cada idioma do jogo.

## Ligações com outras áreas

- Depende dos textos do **Design**: diálogos do narrative designer e interface
  do UX/UI designer.
- A **Engenharia** monta a arquitetura que permite trocar idioma.
- O **Áudio** (dublagem) segue as regras de gravação em vários idiomas.
- **QA** executa o LQA.
- O **marketing** usa a página da loja traduzida.
