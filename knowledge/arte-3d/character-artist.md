---
title: Character artist
summary: Modela e esculpe os personagens e deixa o modelo pronto para rig e animação, do blockout à retopologia, UV e bake.
---

## O que faz

Modela e esculpe os personagens e deixa o modelo pronto para rig e animação.
Cuida das etapas de blockout, escultura high-poly, retopologia e, junto com o
texture artist, UV e bake.

## O que entrega

- **Blockout**: forma bruta com primitivas (cubos, cilindros, esferas) nas
  proporções certas, para aprovar silhueta e escala antes do detalhe.
- **Escultura high-poly**: modelo de alta resolução com todo o detalhe
  (músculos, rugas, costuras, peças de roupa).
- **Low-poly retopologizado**: malha leve e limpa, no número de polígonos do
  orçamento técnico, com edge loops onde o corpo dobra.
- **UVs**: a malha desembrulhada em 2D.
- **Mapas bakeados** do high para o low: normal map, AO e curvature.

## Fundamentos

- **Anatomia** é o que mais pesa no cargo.
- **Blockout**: proporções e escala (altura em cabeças); comparar o modelo com o
  concept em vista frontal e lateral; testar a escala na engine cedo.
- **Escultura**: Sculpt Mode do Blender ou ZBrush; trabalhar do grande para o
  pequeno (formas grandes, depois médias, depois detalhes).
- **Retopologia**: quads, edge flow seguindo os músculos, poles, loops em olhos,
  boca e articulações, loops extras em cotovelo, joelho e ombro. Ela faz o modelo
  deformar de forma natural e simplifica o weight painting. Ferramentas
  automáticas nem sempre acertam esses loops. No Blender: snap e shrinkwrap; no
  ZBrush: ZRemesher.
- **UV**: seams em lugares escondidos; UV sem estiramento e com densidade de
  texel parecida.
- **Bake**: cage e distância de projeção; hard edges sempre na borda de uma ilha
  de UV, senão aparecem costuras no normal map; tangent space (MikkTSpace)
  compatível com a engine.
- **Pipeline solo**: em estilo low-poly ou estilizado, modelar direto o low-poly
  e pular escultura e bake.

## Como validar

- Blockout em cerca de 1 hora, importado na engine ao lado de um cubo de 1 metro,
  com silhueta e proporção conferindo com o concept.
- Uma cabeça simples esculpida primeiro; depois um personagem estilizado inteiro.
- Retopologia testada dobrando o braço e o joelho com um rig simples; onde
  amassar, adicionar loops.
- UV do low-poly feito, normal map bakeado da escultura e conferido na engine,
  sem costuras visíveis.
- Versão low-poly colocada na engine.

## Ligações com outras áreas

- O **concept** é a entrada do blockout.
- O **texture artist** recebe UVs e mapas bakeados e divide com o character
  artist a etapa 4b.
- O **technical artist** ajuda na retopologia e no orçamento de polígonos.
- O **rigger** (Animação) recebe a malha com a topologia pensada para dobrar.
- O **animation TD** e Engenharia fecham a etapa de engine.
