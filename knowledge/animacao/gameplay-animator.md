---
title: Animador de gameplay
summary: Anima o que o jogador controla (andar, correr, pular, golpear) de forma que os clipes se encaixem e respondam rápido ao controle.
---

## O que faz

Anima o que o jogador controla: andar, correr, pular, atirar, golpear, rolar e
morrer. As animações precisam encaixar umas nas outras e responder rápido ao
controle.

## O que entrega

- Ciclos em loop.
- Transições (parado, andando, correndo, parando).
- Ações: golpes, recarga, esquiva.
- Variações.

## Fundamentos

- Os 12 princípios da animação adaptados a jogos.
- Ciclos de locomoção: peso e contato do pé.
- Responsividade: antecipação longa demais deixa o controle com cara de lento.
- As animações têm de se conectar sem pulos.
- Em jogo de luta, cada personagem tem dezenas de golpes com timing exato; em tiro
  e survival pesam as animações de arma, locomoção e interação.

## Como validar

- Faça um ciclo de andar, um de correr, um pulo e um golpe e coloque num
  personagem jogável, ajustando até ficarem bons de controlar.
- Os ciclos fecham sem pulo e os pés não escorregam.
- A antecipação do golpe não faz o controle parecer lento.
- O design confirma que o controle ficou bom no playtest; se não, o timing volta
  para ajuste.

## Ligações com outras áreas

- O Design fornece as ações (mecânicas) e o combat designer revisa as animações
  de golpe.
- O animation TD liga os clipes em state machines e blend trees.
- O Áudio amarra som de passo e de impacto aos quadros da animação.
