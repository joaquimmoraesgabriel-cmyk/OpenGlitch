---
title: Engine e graphics programmer
summary: Programa como o jogo é desenhado: renderização, luz, sombras, shaders e desempenho.
---

## O que faz

Programa como o jogo é desenhado na tela: renderização, luz, sombras, shaders e
desempenho. Na etapa 8 do pipeline de personagem, junto com o technical artist e
o animation TD, põe o personagem na engine.

## O que entrega

- Pipeline de renderização.
- Shaders de base (pele, cabelo, água).
- Otimização: draw calls, culling e LOD.
- Ferramentas de profiling.
- Na etapa de engine do personagem: FBX importado com escala certa, materiais e
  shaders configurados (pele, cabelo, roupa), LODs, Animator configurado e
  testes de desempenho.

## Fundamentos

- **Matemática**: vetores, matrizes e trigonometria.
- **GPU**: como funciona o pipeline, com vertex shader (posição dos vértices) e
  fragment shader (cor de cada pixel).
- **Uma API gráfica**: OpenGL é a mais fácil e ensina o que vale para qualquer
  engine.
- **Profiler da engine**: ferramenta para achar o gargalo real antes de otimizar.
- **Importação na Unity**: a Unity usa 1 unidade como 1 metro, enquanto o 3ds Max
  usa 1 unidade como 10 cm. O tipo de rig (Humanoid ou Generic) e os blend shapes
  são configurados na importação.
- **LODs**: versões mais leves do modelo para quando ele está longe. Nomear as
  malhas como `_LOD0`, `_LOD1`, `_LOD2` faz a Unity criar o LOD Group sozinha na
  importação.
- **Shader Graph e teste em cena real**: o personagem é testado com a luz do
  jogo, não só no visualizador.

## Como validar

- Um triângulo em OpenGL, depois um cubo com textura e luz.
- Na Unity, um shader simples de água funcionando.
- O personagem final é exportado com 3 LODs, importado na Unity com a escala
  certa e com o Animator configurado.
- O desempenho é medido no profiler com 20 cópias do personagem na cena, e o
  resultado cabe na meta de FPS.
- Toda otimização tem a medida de antes e de depois.
- Os materiais (pele, cabelo, roupa) ficam corretos sob a luz do jogo.

## Ligações com outras áreas

- O technical artist da Arte 3D entrega o FBX, os materiais e os LODs; a
  Engenharia diz o que ajustar quando o desempenho não fecha.
- O animation TD da Animação entrega o rig e o Animator; a importação do rig
  (Humanoid ou Generic) é combinada com ele.
- O diretor de arte define o estilo que os shaders precisam respeitar.
- O orçamento técnico (polígonos, texturas, personagens por cena) define os
  limites para a equipe de arte.
- Cinematics depende da qualidade de render em tempo real.
