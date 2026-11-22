---
title: Technical artist
summary: Faz a ponte entre arte e programação com shaders, ferramentas de pipeline, orçamento técnico e a importação de assets na engine.
---

## O que faz

É a ponte entre arte e programação: shaders, ferramentas, scripts, otimização e
o diagnóstico de "por que esse asset não funciona na engine". Em jogos o cargo
é muito importante.

## O que entrega

- **Shaders**.
- **Ferramentas de pipeline**: exportação e validação.
- **Orçamento técnico**: polígonos, texturas, personagens por cena, meta de FPS.
- **Documentação para os artistas**.
- **Etapa 8 do personagem**: FBX importado com escala certa, materiais e shaders
  configurados (pele, cabelo, roupa), LODs, Animator configurado e testes de
  desempenho.

## Fundamentos

- **Shaders**: HLSL ou GLSL, ou shader graph.
- **Scripting**: Python para o Blender, C# para o Unity.
- **Profiling** e o básico do pipeline de arte.
- **Importação no Unity**: 1 unidade = 1 metro (o 3ds Max usa 1 unidade = 10 cm);
  tipo de rig Humanoid ou Generic; blend shapes.
- **LODs**: malhas nomeadas `_LOD0`, `_LOD1`, `_LOD2` fazem o Unity criar o LOD
  Group sozinho na importação.
- **Teste**: o personagem em cena real, com a luz do jogo, medido no profiler.
- **Captura de frame**: RenderDoc e NSight, mostrados na palestra do Game Art
  Tricks.
- Fontes de estudo: The Book of Shaders, Unity for Technical Artists (e-book
  gratuito de 91 páginas), Catlike Coding e o Riot Tech Blog.

## Como validar

- Um shader de dissolver em que o personagem "desmancha" ao morrer, com o limiar
  controlável.
- Um script Python que exporta todos os modelos de uma pasta, com escala e nomes
  corretos.
- O personagem final exportado com 3 LODs, importado na engine, com o Animator
  configurado.
- Desempenho medido com 20 cópias do personagem na cena e dentro da meta.
- A escala importada confere com o cubo de 1 metro.

## Ligações com outras áreas

- O **character artist** recebe ajuda na retopologia e no orçamento de polígonos.
- O **texture artist** e o **lighting artist** dependem dos materiais, shaders e
  perfis que ele configura.
- O **animation TD** (Animação) configura o Animator na etapa 8.
- **Engenharia** define a meta de FPS e recebe o orçamento técnico.
- O **VFX artist** usa os shaders de efeito.
