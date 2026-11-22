---
title: Luz e comp
summary: Acabamento final da cena: luz que cria clima e guia o olhar, color grading, efeitos de lente e composição.
---

## O que faz

É o acabamento final. A luz cria clima e guia o olhar; a composição junta
camadas e corrige cor. Em tempo real, a "comp" vira pós-processamento.

## O que entrega

- **Luz de cada plano**.
- **Color grading**.
- **Efeitos de lente**.
- No pré-renderizado, a **imagem final composta**.

## Fundamentos

- Luz principal, preenchimento e contraluz.
- Color grading.
- Pós-processamento (engine) ou compositor do Blender (pré-renderizado).
- O caso Arcane: fundos pintados em 2D projetados sobre geometria 3D simples
  (projection mapping) dão profundidade sem gastar muito. Nos cenários, a
  equipe cria um set 3D e projeta matte painting nele, com linhas tremidas
  feitas à mão. As texturas foram pintadas à mão.

## Como validar

- Três gradings do mesmo plano: quente e nostálgico, frio e tenso, saturado e
  "videogame". Os três precisam passar emoções diferentes sem mudar o plano.
- A luz guia o olhar para o que importa no plano.
- A luz e o grading ficam coerentes entre os planos da mesma cena.
- Em tempo real, o pós-processamento roda sem derrubar o desempenho da cena.

## Ligações com outras áreas

- A luz base do cenário vem da **Arte 3D** (lighting artist); aqui a luz é
  refinada por plano.
- VFX e materiais da Arte 3D entram na imagem final.
- O pós-processamento em tempo real conversa com a **Engenharia** em
  desempenho.
