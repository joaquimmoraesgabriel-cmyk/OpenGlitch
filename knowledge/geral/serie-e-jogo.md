---
title: Série e jogo
summary: Diferenças entre série 3D, jogo e híbrido, os blocos de equipe que eles compartilham e a diferença entre tempo real e pré-renderizado.
---

## Série x jogo

Séries (tipo Arcane) e jogos 3D (tiro, sobrevivência, luta) usam quase os
mesmos blocos de equipe. A série entrega vídeo; o jogo entrega assets que
rodam em tempo real.

## Pré-produção (as duas)

- Direção, roteiro, storyboard: definem a história e os planos.
- Concept art e direção de arte: personagens, cenários, estilo visual.
- Game design (só jogos): define o que o personagem faz (atirar, rolar,
  bloquear), e isso dita as animações necessárias.

## Criação dos assets 3D

- Modelador de personagem: esculpe e faz a malha (ZBrush, Maya, Blender).
- Modelador de ambiente e props: cenários, armas, veículos, objetos.
- Texture / material artist: pintura e materiais (Substance Painter).
- Rigger: monta o esqueleto e os controles que o animador move.
- Technical artist (TD): liga arte e código, otimiza e cria ferramentas. É
  muito importante em jogos.
- Cabelo, roupa e VFX: simulações de tecido, cabelo, fogo, fumaça, explosões.

## Animação

- Animador de personagem (keyframe): atuação e movimento à mão.
- Animador de combate / gameplay (jogos): ciclos de andar, correr, pular,
  golpes e recarga. Precisam encaixar e ter transições suaves.
- Mocap e cleanup: capturam o movimento de atores e limpam os dados.
- Animador de câmera / layout (série): enquadramento e movimentos de câmera.
- Cinematics (jogos): cenas de corte.

## Finalização

- Série: iluminação, render, composição (comp) e edição. O Arcane ainda tem
  uma camada 2D pintada à mão por cima do 3D.
- Jogos: engine (Unreal ou Unity), programadores de gameplay, áudio, QA e
  produtores.

## Tempo real x pré-renderizado

- Série é linear e pré-renderizada: cada plano é montado e renderizado com
  qualidade máxima.
- Jogo é interativo e roda em tempo real: tudo precisa funcionar de qualquer
  ângulo, com o jogador no controle.
- Cutscenes de jogo podem ser renderizadas em tempo real na própria engine ou
  pré-renderizadas, como no Arcane.

## Híbrido

O híbrido (God of War, The Last of Us) usa o pipeline de jogo, com engine em
tempo real, mais as disciplinas de cinema: direção, atuação, câmera e edição.
É jogabilidade em tempo real com cenas dirigidas como numa série. Ao
dimensionar um projeto híbrido, some o trabalho de jogo (design, engenharia,
animação de gameplay) ao de cinema (cinematics).
