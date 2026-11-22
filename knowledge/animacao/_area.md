---
title: Animação
summary: A área que dá movimento ao jogo: estilo de movimento, rig, animação de gameplay e de cena, mocap, rosto, implementação na engine e física de roupa e cabelo.
---

## O que a área faz

Animação define como os personagens se movem e faz esse movimento funcionar no
jogo. Reúne sete funções: rigger (esqueleto e skinning), animador de gameplay,
animador de cinematic, mocap e cleanup, animação facial, animation TD (a
animação dentro da engine) e cloth/hair/physics (roupa, cabelo e física). A
liderança é a do diretor de animação: define o estilo de movimento (realista ou
exagerado), aprova as animações e garante que fiquem bonitas e boas de jogar.

No jogo a animação precisa responder rápido ao controle. É a diferença para uma
série, em que o movimento só precisa ficar bonito na tela. Em equipe pequena, uma
pessoa faz quase tudo isso.

## O que o diretor de animação entrega

- **Guia de estilo de movimento**: peso, timing, exagero e personalidade.
- **Animation list**: todos os movimentos necessários.
- **Decisão do que é mocap e do que é keyframe.**
- **Revisão das animações** junto com o combat designer.

Fundamentos: os 12 princípios da animação; a diferença do jogo para a série;
state machines, blend spaces, IK e motion matching. Para validar: anime um ciclo
de andar, um pulo e um golpe, coloque num personagem jogável e ajuste até ficar
bom de controlar.

## Pipelines

No **pipeline de personagem**, a Arte 3D entrega o modelo texturizado. A
Animação faz a etapa 6 (rig e skinning) e a etapa 7 (animação), e participa da
etapa 8 (engine) com a importação e o Animator configurado.

No **pipeline de animação em jogo**: animation list, produção (mocap ou
keyframe), cleanup e polimento, exportação para a engine, implementação (state
machines, transições, blends, IK nos pés e mãos) e playtest, em que o timing é
ajustado até o controle ficar bom.

Para um primeiro personagem jogável, use rig automático (Rigify, AccuRig ou
Mixamo) e animações prontas para testar, trocando depois pelas suas. Se o
resultado será vendido como pacote, a origem das animações é o ponto mais
importante: mocap próprio, keyframe próprio ou dados com licença que permita
revenda.

## Ordem de aprofundamento

1. Os 12 princípios em jogos.
2. Rigify e rigging no Blender.
3. Documentação de animação da Unity e Animation Rigging.
4. Motion matching da Unreal e The Orange Duck.

## Ligações com outras áreas

- **Design**: a lista de ações das mecânicas vira a animation list; o combat
  designer revisa as animações de golpe; o playtest diz se o controle ficou bom.
- **Arte 3D**: entrega o modelo texturizado para o rig; o technical artist
  participa da exportação e da importação na engine.
- **Engenharia**: o gameplay programmer controla os parâmetros dos blends e
  das state machines.
- **Cinematics**: as cenas usam a animação de atuação e o sequenciador da engine.
- **Áudio**: os eventos de passos e impactos ficam amarrados aos quadros da
  animação; a dublagem guia a animação facial.
