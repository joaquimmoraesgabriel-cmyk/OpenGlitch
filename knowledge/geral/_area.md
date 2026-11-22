---
title: Visão geral
summary: O que é um jogo 3D cinematográfico e como esta base de conhecimento está organizada em áreas e pipelines.
---

## O que é um jogo 3D cinematográfico

É um jogo 3D que combina jogabilidade em tempo real com as disciplinas do
cinema: direção, atuação, câmera e edição. Exemplos de referência do guia são
God of War e The Last of Us. Séries 3D como Arcane usam quase os mesmos blocos
de equipe, mas entregam vídeo pré-renderizado; o jogo entrega assets que rodam
em tempo real, com o jogador no controle.

## As 8 áreas

O trabalho se divide em 8 áreas. Cada uma tem uma pasta de conhecimento e um
agente (a liderança é a exceção, veja abaixo).

1. **Liderança**: visão, produção, direção de arte, técnica e de animação.
2. **Design**: regras, combate, fases, história, interface.
3. **Arte 3D**: concept, personagens, cenários, props, texturas, luz, VFX e
   technical art.
4. **Animação**: rig, animação de gameplay e de cinematic, mocap, animação
   facial, animation TD, cloth e hair.
5. **Cinematics**: o lado "série": cenas, câmera, edição e acabamento.
6. **Engenharia**: gameplay, engine, IA, ferramentas, rede e build.
7. **Áudio**: efeitos, trilha, dublagem e integração na engine.
8. **Apoio**: QA, localização, marketing e comunidade.

## Liderança no OpenGlitch

A liderança não é um agente. O papel é dividido entre o usuário, o agente
Design (visão, pilares, escopo, produção) e os agentes das áreas (direção de
arte na Arte 3D, direção técnica na Engenharia, direção de animação na
Animação). Veja `lideranca/_area`.

## Como esta base está organizada

- `geral/`: panorama do projeto (fases, equipes, tamanho de equipe,
  ferramentas, escopo para equipe pequena, fontes gerais).
- `lideranca/`: os cinco papéis de liderança e quem os assume.
- `pipelines/`: os fluxos que atravessam várias áreas.
- Uma pasta por área (`design/`, `arte-3d/`, `animacao/` e as demais), com o
  conteúdo de cada função.

## Os pipelines

Dois fluxos atravessam as áreas e dizem quem entrega o quê a quem:

- **Personagem** (`pipelines/personagem`): do concept à engine.
- **Animação em jogo** (`pipelines/animacao-em-jogo`): da lista de ações ao
  playtest.

Quando o pedido envolve mais de uma área, comece pelo pipeline e entre na pasta
da área na etapa em que o trabalho acontece.

## Como usar

1. Descubra o tamanho da equipe e o escopo com o usuário
   (`geral/equipe-pequena-ou-solo`, `geral/tamanho-de-equipe`).
2. Descubra a fase do projeto (`geral/fases-do-projeto`).
3. Abra a pasta da área do pedido, ou o pipeline se o trabalho cruza áreas.
