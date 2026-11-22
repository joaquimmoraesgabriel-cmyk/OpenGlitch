---
title: Texture e material artist
summary: Pinta e cria materiais (metal, pele, couro, ferrugem), realistas ou estilizados, e entrega mapas PBR, materiais procedurais e bibliotecas.
---

## O que faz

Pinta e cria materiais como metal, pele, couro e ferrugem, realistas ou
estilizados. Divide com o character artist a etapa de UV e bake.

## O que entrega

- **Mapas PBR**: base color, roughness, metallic e normal.
- **Texturas pintadas à mão**, no estilo do jogo, quando o estilo não é PBR.
- **Materiais procedurais**.
- **Bibliotecas reutilizáveis** de material.

## Fundamentos

- **Teoria PBR primeiro.** O PBR Guide (Adobe/Allegorithmic, gratuito desde
  2014) tem a parte 1 de teoria e a parte 2 de prática, e vale para qualquer
  software.
- **Ferramentas**: Substance Painter e Designer, ou alternativas gratuitas
  (Blender, Material Maker).
- **Estilo pintado**: para um estilo como o do Arcane, pinta-se luz e
  pinceladas na própria textura.
- **UV e bake que alimentam a textura**: seams em lugares escondidos; UV sem
  estiramento e com densidade de texel parecida; cage e distância de projeção
  no bake; hard edges na borda de ilha de UV, senão surgem costuras no normal
  map; tangent space MikkTSpace compatível com a engine. Os mapas bakeados são
  normal, AO e curvature.
- **Pipeline solo**: cores chapadas ou pintadas à mão no lugar de PBR completo.

## Como validar

- O mesmo objeto em 3 materiais bem diferentes: madeira nova, metal enferrujado,
  plástico gasto. Cada um se lê como o que é.
- O personagem texturizado com 3 materiais bem diferentes: pele, tecido e metal.
- O normal map bakeado, conferido na engine, não mostra costuras.
- Os valores de base color, roughness e metallic seguem a teoria do PBR Guide.
- No estilo pintado, a luz e as pinceladas da textura combinam com a art bible.

## Ligações com outras áreas

- O **character artist** entrega UVs e mapas bakeados.
- O **props artist** e o **environment artist** recebem materiais e texturas
  tileáveis.
- O **technical artist** configura o material e o shader na engine.
- O **lighting artist** define a luz sob a qual o material precisa ler bem.
- O **concept artist** passa os callouts de material e a paleta.
