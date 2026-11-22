---
title: Props e hard-surface artist
summary: Modela objetos duros como armas, veículos, robôs e máquinas, com bordas limpas, bevels corretos, versões high e low, normal maps e LODs.
---

## O que faz

Modela objetos duros: armas, veículos, robôs e máquinas. É central em jogo de
tiro.

## O que entrega

- **Modelos com bordas limpas** e bevels corretos.
- **Versões high e low** do objeto.
- **Normal maps** que levam o detalhe do high para o low.
- **LODs**.

## Fundamentos

- **Subdivisão** e **booleanas** como técnicas de modelagem.
- **Controle de normais**: smoothing groups e Weighted Normal.
- **Bevel** correto nas bordas.
- **Estudo de objetos reais**: o objeto é construído a partir de fotos e de
  referência.
- No Blender, as seções do manual que mais importam são Bevel, Boolean e
  Weighted Normal.
- As threads de hard surface e de normals do Polycount são a fonte prática do
  guia.
- Hard edges na borda de ilha de UV evitam costuras no normal map, o mesmo
  princípio do bake de personagem.

## Como validar

- Modele uma arma ou ferramenta real a partir de fotos, do blockout até a
  textura.
- As bordas estão limpas e o sombreamento não mostra artefatos em nenhum ângulo.
- O bevel é consistente e pega luz nas bordas.
- O normal map bakeado do high no low não mostra costuras na engine.
- As proporções batem com a referência fotográfica.
- Há LODs que reduzem polígonos mantendo a silhueta.

## Ligações com outras áreas

- O **texture artist** texturiza o objeto a partir dos mapas bakeados.
- O **technical artist** valida orçamento, escala e LODs na importação.
- **Animação** recebe a arma para animações de manuseio e recarga.
- **Design** define o papel da arma no combate; o diretor de arte aprova o visual.
