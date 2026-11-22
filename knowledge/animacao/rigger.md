---
title: Rigger
summary: Monta o esqueleto e os controles do animador e define como a malha deforma; entrega também o esqueleto de jogo leve.
---

## O que faz

Cria o esqueleto (ossos) e os controles que o animador move, e define como a
malha deforma quando os ossos se movem. Na etapa 6 do pipeline de personagem, é
o rigger quem pega o modelo texturizado e o deixa pronto para animar.

## O que entrega

- Esqueleto com nomes e hierarquia padronizados.
- Skinning e weight painting (quanto cada osso puxa da malha).
- Controles IK/FK.
- Rig de jogo leve, compatível com a engine, separado do rig de animação.

## Fundamentos

- Hierarquia de ossos, IK versus FK e constraints.
- Weight painting é a parte que mais dá trabalho.
- Rig de animação (cheio de controles, fica no Blender ou no Maya) é diferente do
  esqueleto de jogo (só os ossos de deformação, vai para a engine).
- Nomes de ossos compatíveis com o Humanoid da Unity facilitam o retargeting.
- Rigify (Blender) gera um rig completo a partir de uma metarig; AccuRig e Mixamo
  são rigs automáticos para testar rápido.
- O Unity Animation Rigging traz constraints de IK e Aim (Chain IK, Damped
  Transform, Multi-Aim, Twist Correction, Two Bone IK) para a engine.

## Como validar

- Rigue um braço simples com IK, depois um personagem inteiro com o Rigify.
- Gere o esqueleto de jogo a partir do rig e teste poses extremas (agachar, braço
  para cima): a malha não pode deformar de forma errada.
- O esqueleto de jogo tem só os ossos necessários, com nomes padronizados, e
  importa na engine sem erro.

## Ligações com outras áreas

- Recebe o modelo texturizado da Arte 3D (etapas 1 a 5 do pipeline de
  personagem).
- Entrega o personagem riggado para os animadores e para o animation TD.
- O rig facial é tratado em animação facial; roupa e cabelo em cloth/hair/physics.
