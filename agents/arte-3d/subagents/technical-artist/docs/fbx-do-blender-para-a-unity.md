---
title: FBX do Blender para a Unity sem malha deitada
summary: Opções de exportação e de importação que evitam malha deitada, rotação de 90 graus na raiz e animação no eixo errado entre o Blender e a Unity.
tipo: original
fonte:
autor: openglitch (testes casinha-de-madeira, jardim-ao-vento e jardim-realista)
testado_em: Blender 5.3, Unity 6000.6.10f1, URP 17.6
---

O Blender usa Z para cima e a Unity usa Y para cima. A conversão pode ficar
nos vértices ou numa rotação do objeto, e cada escolha quebra uma coisa
diferente. Visto em três projetos de teste, numa só máquina: confira no seu.

## Malha estática: converta os vértices na exportação

Sintoma: a cena parece certa, mas a malha chega com a altura no eixo errado e
o objeto filho com rotação de 90 graus em X. Shaders que usam a altura no
espaço do objeto (vento de árvore, casca por altura) quebram.

Causa: sem `bake_space_transform`, o exportador põe a conversão de eixo no nó
do objeto e deixa os vértices no espaço do Blender.

Solução, no `bpy.ops.export_scene.fbx`:

- `axis_forward='-Z'`, `axis_up='Y'`
- `bake_space_transform=True`
- `use_triangles=True`
- `colors_type='LINEAR'` quando a cor de vértice carrega dados

Depois disso a malha chega com rotação identidade e Y para cima.

## Mapeamento de eixos

Conferido com uma sonda no terreno:

- Unity (x, y, z) = Blender (x, z, y)
- giro em Y na Unity = giro em Z no Blender com sinal trocado

Normais customizadas e três camadas de UV chegam como TexCoord0 a TexCoord2.
Cor de vértice em ponto flutuante exportada como LINEAR chega em 8 bits.

## Modelo animado: não use bakeAxisConversion

Sintoma: uma peça animada (uma porta) aparece deitada ou gira no eixo errado.

Causa: `ModelImporter.bakeAxisConversion=true` converte a malha, mas não as
curvas de animação.

Solução:

- importe com `bakeAxisConversion=false`, que mantém a conversão como rotação
  na raiz do modelo;
- não zere a rotação da raiz por script;
- para posicionar a peça (a dobradiça da porta), crie um objeto pai fixo no
  ponto certo e ponha o modelo animado dentro dele, porque o clipe também
  anima a posição da raiz.

## Como conferir

- Leia de volta os limites da malha importada: a maior dimensão vertical deve
  estar em Y.
- Registre no log as rotações da hierarquia do modelo.
- Capture a cena logo depois de importar, antes de montar o resto.
- Para um atributo suspeito (UV extra, cor de vértice), devolva-o como cor no
  shader e capture.
