---
title: Compositor
summary: Cria a trilha sonora e faz a música reagir ao jogo (combate, tensão, exploração).
---

## O que faz

Cria a trilha sonora e faz a música reagir ao que acontece no jogo: combate,
tensão, exploração.

## O que entrega

- **Temas principais**.
- **Trilhas de cada área**.
- **Música adaptativa em camadas**.
- **Stingers**: trechos curtos que marcam um momento.
- **Loops**.

## Fundamentos

- Teoria musical básica: escalas, acordes, tonalidade e andamento.
- Uma DAW para produzir: Reaper, FL Studio ou Cakewalk.
- Música interativa: a música é dividida em camadas e estados, e o jogo
  decide quais tocam. O Wwise-201 é o curso de referência para isso, com
  material e quizzes gratuitos (só o exame é pago).

## Como validar

- Uma música com 3 camadas (exploração, tensão, combate) que troca dentro da
  engine, sem corte audível, e volta ao estado anterior quando o combate
  termina.
- O loop não tem emenda audível na repetição.
- Cada estado do jogo tem uma música ou camada definida, e a regra de
  transição está escrita.
- A música não cobre efeitos nem falas importantes: ouvida junto com os
  efeitos, a mixagem continua clara.

## Ligações com outras áreas

- O **Design** define os estados do jogo e o tom emocional de cada um.
- **Cinematics** pede música por cena e pontos de sincronia.
- O **audio programmer** implementa as transições e os parâmetros.
- A **Engenharia** dispara as mudanças de estado.
