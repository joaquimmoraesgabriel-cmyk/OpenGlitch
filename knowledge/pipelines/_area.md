---
title: Pipelines
summary: O que é um pipeline e os dois que existem na base: o de um personagem (do concept à engine) e o de animação em jogo.
---

## O que é um pipeline

Um pipeline é a sequência de etapas pela qual um asset passa até chegar ao
jogo. Cada etapa tem um responsável, recebe algo da etapa anterior e entrega
algo à seguinte. Ele atravessa várias áreas, por isso é descrito aqui e não
dentro de uma só pasta.

## Os dois pipelines

- **Personagem** (`pipelines/personagem`): concept, blockout, escultura,
  retopologia, UV e bake, texturas, rig e skinning, animação, engine. Inclui
  uma etapa 0 (a ficha do personagem, entregue pelo Design) e um pipeline solo
  enxuto.
- **Animação em jogo** (`pipelines/animacao-em-jogo`): animation list,
  produção, cleanup e polimento, exportação, implementação e playtest.

## Como usar

1. Descubra em que etapa o usuário está e o que a etapa anterior entregou.
2. Entre no documento da etapa: ele diz quem faz, o que recebe, o que entrega
   e como validar.
3. Consulte o agente e o subagente responsáveis indicados na etapa.
4. Só passe para a próxima etapa quando a validação da atual passar.

## Para equipe pequena

O pipeline de personagem tem uma versão enxuta (`## Pipeline solo enxuto` em
`pipelines/personagem`). Veja também `geral/equipe-pequena-ou-solo`.
