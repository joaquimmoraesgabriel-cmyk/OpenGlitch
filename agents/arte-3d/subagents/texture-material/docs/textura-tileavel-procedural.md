---
title: Textura procedural que repete sem emenda
summary: Como gerar no Blender uma textura procedural perfeitamente tileável, mapeando o UV num toro de quatro dimensões, e quando o procedural puro não parece natural.
tipo: original
fonte:
autor: openglitch (teste jardim-realista)
testado_em: Blender 5.3
---

Ruído comum não repete: a borda direita não casa com a esquerda. O truque
abaixo dá emenda perfeita sem retoque. Visto num teste, numa máquina.

## A técnica

Em vez de amostrar o ruído no plano do UV, mapeie o UV num toro plano de
quatro dimensões e use ruído 4D:

```
( cos(2πu), sin(2πu), cos(2πv), sin(2πv) ) × R
```

No Blender, os nós Noise e Voronoi aceitam quatro dimensões (o vetor mais a
entrada W). Como `u` e `v` dão a volta completa num círculo, o valor em 0 é o
mesmo que em 1, nos dois sentidos.

- O raio `R` controla a escala do padrão.
- Raios diferentes em `u` e em `v` esticam o padrão e ele continua repetindo.
- Distorcer as coordenadas com outro ruído amostrado no mesmo toro (domain
  warp) mantém a repetição.

## Quando o procedural puro não basta

Uma rede uniforme de rachaduras (Voronoi) cobrindo uma pedra inteira parece
calçamento ou casco de tartaruga, não pedra natural. No teste, o que o usuário
aprovou como realista foi partir de uma base escaneada com licença livre e
somar camadas procedurais por cima: musgo, líquen e variação de cor.

Antes de baixar qualquer textura, confirme a licença na página da fonte e
diga ao usuário de onde ela vem.

## Como conferir

- Renderize a textura repetida duas vezes em cada direção: a emenda não pode
  aparecer.
- Olhe de longe: um padrão que se repete de forma visível precisa de uma
  camada de variação em escala maior.
- Olhe aplicada no objeto 3D, não só no plano: o que funciona no chão pode
  parecer artificial envolvendo uma pedra.
