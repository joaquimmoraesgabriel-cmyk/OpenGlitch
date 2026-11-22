---
title: Cinematics
summary: A área "série" do jogo: transforma o roteiro em cenas, com câmera, atuação, edição e acabamento de luz e cor.
---

## O que a área faz

Cinematics é a parte "série" de um jogo 3D cinematográfico. Reúne cinco
funções: diretor de cinematic (transforma o roteiro em cenas), layout e câmera
(enquadramento, movimento e ritmo), animadores de cena (atuação plano a plano),
editor (montagem e ritmo) e iluminação e comp de cena (acabamento final).

## Tempo real ou pré-renderizado

A primeira decisão da área é como renderizar:

- **Tempo real, na engine**: mais barato, fácil de mudar, com o mesmo visual do
  jogo. É o que quase todo jogo faz hoje.
- **Pré-renderizado, em vídeo**: mais bonito, mas pesado e difícil de alterar.
  Sendo solo, quase nunca vale a pena.

Uma série como Arcane é linear e pré-renderizada: cada plano é montado e
renderizado com qualidade máxima. Um jogo roda em tempo real e precisa
funcionar de qualquer ângulo. O híbrido (God of War, The Last of Us) usa o
pipeline de jogo mais as disciplinas de cinema: direção, atuação, câmera e
edição.

## Regra de escopo

Cutscene é cara. Num jogo pequeno, faça poucas, curtas e na engine. Toda cena
precisa mudar algo; se não muda, é candidata a corte.

## Ordem de aprofundamento

1. Planos e câmera (guia de câmera da StudioBinder).
2. A regra dos seis, para saber quando cortar.
3. O Sequencer (Unreal) ou o Timeline (Unity).
4. O estilo Fortiche, se o visual desejado for parecido com o do Arcane.

## Ligações com outras áreas

- **Design**: o roteiro de cutscenes e os diálogos são a entrada do diretor de
  cinematic.
- **Arte 3D**: personagens, cenários e props que a câmera vê; a luz base do
  cenário.
- **Animação**: rigs, animação facial e mocap limpo alimentam as cenas; o
  animador de cinematic é a função que fica entre as duas áreas.
- **Engenharia**: ponto de entrada e saída da cutscene, pular cena e controle
  do jogador.
- **Áudio**: dublagem, música e efeitos seguem o tempo de cada plano.
- **Apoio**: QA testa as cenas; localização cuida de legendas.
