---
title: Cloth, hair e physics
summary: Simula roupa, capa, cabelo e partes que balançam, e monta ragdolls, com ajustes para rodar leve.
---

## O que faz

Simula roupa, capa, cabelo, partes que balançam e ragdoll.

## O que entrega

- Configuração de tecido e cabelo.
- Jiggle bones.
- Ragdolls.
- Ajustes para rodar leve.

## Fundamentos

- Física básica: rigidbody e joints.
- Simulação de tecido.
- O truque de usar ossos com física simples no lugar de tecido completo.
- Ferramentas: Cloth e Hair do Blender; Cloth, Ragdoll Wizard e Joints da Unity;
  Chaos Cloth e Physics Asset da Unreal; Damped Transform do Unity Animation
  Rigging.

## Como validar

- Coloque uma capa e um rabo de cavalo num personagem andando e ajuste até
  não atravessarem o corpo.
- O ragdoll não torce em ângulos impossíveis.
- O custo da simulação cabe no orçamento do jogo.

## Ligações com outras áreas

- Usa o rig do rigger e as animações dos animadores como entrada.
- A Arte 3D (technical artist) cuida de shaders de cabelo e roupa e de LODs.
- A Engenharia ajuda quando o ragdoll muda o estado do personagem no jogo.
