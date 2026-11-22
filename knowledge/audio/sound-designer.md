---
title: Sound designer
summary: Cria os efeitos sonoros do jogo (passos, tiros, golpes, explosões, interface, ambientes) em camadas e variações.
---

## O que faz

Cria os efeitos sonoros: passos, tiros, golpes, explosões, interface e
ambientes. O som dá peso ao que acontece na tela.

## O que entrega

- **Biblioteca de efeitos** organizada por evento do jogo.
- **Variações**: por exemplo 5 versões do mesmo passo, para o som não cansar.
- **Ambientes em loop**.
- **Sons de interface**.

## Fundamentos

- Gravação, mesmo com celular, e edição em Audacity ou Reaper.
- Camadas: um tiro tem estalo, corpo, cauda e eco. Cada camada cumpre uma
  função e pode ser trocada separadamente para gerar variações.
- Jogar sem música, prestando atenção só nos efeitos, mostra o que o jogo
  comunica pelo som.
- Bancos de som prontos aceleram o trabalho: o Freesound é gratuito e a
  licença varia por som; a Sonniss libera um pacote gratuito por ano na época
  da GDC. A licença de cada som precisa estar anotada.

## Como validar

- Refaça todo o áudio de um vídeo de gameplay sem som. Se um evento visível
  ficou sem som, a lista de eventos está incompleta.
- Cada ação do jogo deve ser reconhecível só pelo som, com a música desligada.
- Um som que se repete muito tem variações suficientes para não soar igual
  duas vezes seguidas.
- Todo som tem origem e licença registradas, e a condição de crédito, quando
  existe, está cumprida.
- O som de impacto foi ouvido junto com a animação e o hitstop do golpe, e o
  golpe pesado soa mais pesado que o leve.

## Ligações com outras áreas

- Cada ação do **Design** e cada golpe do combat designer pede um evento
  sonoro.
- A **Animação** define o frame do impacto e do passo, que é o momento em que o
  som deve tocar.
- A **Engenharia** dispara os eventos; o audio programmer configura a mixagem.
- **Cinematics** recebe os efeitos e os ambientes das cenas.
