---
title: Animation TD
summary: Faz as animações funcionarem dentro do jogo e decide qual toca e quando, com state machines, blends, IK e motion matching.
---

## O que faz

Faz as animações funcionarem dentro do jogo e decide qual toca e quando. É o
coração de um pacote de animação. Participa da etapa 8 (engine) do pipeline de
personagem, junto com a Arte 3D e a Engenharia.

## O que entrega

- Animator Controllers (Unity) ou Animation Blueprints (Unreal).
- Blend spaces e blend trees.
- IK de pés e mãos.
- Motion matching.
- Ferramentas para os animadores.

## Fundamentos

- State machines e blend trees.
- IK procedural.
- Motion matching.
- C# (Unity) ou C++ e Blueprints (Unreal).
- Importação: tipo de rig Humanoid ou Generic, escala e unidades (a Unity usa 1
  unidade = 1 metro), blend shapes, e LODs nomeados `_LOD0`, `_LOD1`, `_LOD2`.
- O conteúdo de exemplo da Epic costuma ter licença ligada à Unreal; para um
  produto na Unity, o mais seguro é usar só para estudo.

## Como validar

- Monte a locomoção completa (parado, andar, correr, virar) com IK nos pés
  subindo escada.
- Depois, um motion matching simples.
- As transições não deixam o controle lento e os pés não atravessam nem flutuam
  nos degraus.
- O personagem importado tem a escala certa e o Animator configurado.

## Ligações com outras áreas

- A Engenharia (gameplay programmer) controla os parâmetros que alimentam
  os blends.
- O technical artist da Arte 3D cuida de shaders, LODs e desempenho.
- Recebe os clipes dos animadores, do mocap e do rigger.
- No playtest, o Design diz se o controle ficou bom.
