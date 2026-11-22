---
title: Pipeline de personagem
summary: Do zero ao jogo: ficha, concept, blockout, escultura, retopologia, UV e bake, texturas, rig, animação e engine, com donos, entregas, validação e atalhos solo.
---

O pipeline de um personagem tem 8 etapas no guia (concept, blockout, escultura,
retopo mais UV e bake, texturas, rig e skinning, animação, engine). O
OpenGlitch acrescenta uma etapa 0, a ficha do personagem, que o Design
entrega. Cada etapa abaixo diz quem faz no guia, quem responde por ela no
OpenGlitch, o que recebe, o que entrega, o que precisa estar certo e como
validar.

## Etapa 0: Ficha do personagem

- **Quem faz**: não é uma etapa do guia. É o Design que define o personagem
  antes do concept.
- **No OpenGlitch**: agente `design`.
- **Recebe**: os pilares e o escopo do jogo.
- **Entrega**: a ficha do personagem: quem ele é, o que faz no jogo e que
  ações executa (atirar, rolar, bloquear, golpear). As ações viram a
  animation list.
- **Precisa estar certo**: as ações dizem o que a animação terá de entregar;
  uma ação esquecida aqui vira retrabalho na etapa 7.
- **Como validar**: a ficha responde às três perguntas (quem, papel, ações) e
  as ações cabem no escopo combinado.
- **Atalho solo**: a ficha escrita e um moodboard servem também como concept
  (veja a etapa 1).

## Etapa 1: Concept

- **Quem faz (guia)**: concept artist, aprovado pelo diretor de arte.
- **No OpenGlitch**: `arte-3d` / `concept-artist`.
- **Recebe**: a ficha do personagem e o estilo visual da art bible.
- **Entrega**: design do personagem, turnaround (frente, lado, costas),
  callouts de detalhes e materiais, paleta de cores.
- **Precisa estar certo**: perspectiva, forma, silhueta, anatomia, cor. Um
  personagem bom se reconhece só pela sombra.
- **Como validar**: 20 silhuetas rápidas; escolhe-se uma e faz-se o turnaround
  dela. O concept passa quando a silhueta é reconhecível sozinha.
- **Atalho solo**: se o usuário não desenha, monte um moodboard de
  referências e uma ficha escrita do personagem. Já serve como concept para
  modelar.

## Etapa 2: Blockout

- **Quem faz (guia)**: character artist.
- **No OpenGlitch**: `arte-3d` / `character-artist`.
- **Recebe**: o concept (ou o moodboard e a ficha).
- **Entrega**: forma bruta com primitivas (cubos, cilindros, esferas) nas
  proporções certas, usada para aprovar silhueta e escala antes do detalhe.
- **Precisa estar certo**: proporções e escala (altura em "cabeças"); o
  modelo comparado com o concept em vista frontal e lateral; escala testada
  cedo na engine.
- **Como validar**: blockout feito em 1 hora, importado na Unity ao lado de um
  cubo de 1 metro.
- **Atalho solo**: em estilo low-poly ou estilizado, o blockout pode já
  evoluir direto para o low-poly (veja `## Pipeline solo enxuto`).

## Etapa 3: Escultura (high-poly)

- **Quem faz (guia)**: character artist.
- **No OpenGlitch**: `arte-3d` / `character-artist`.
- **Recebe**: o blockout aprovado.
- **Entrega**: modelo de alta resolução com todo o detalhe (músculos, rugas,
  costuras, peças de roupa), que depois vira mapas na versão leve.
- **Precisa estar certo**: anatomia; escultura digital (Sculpt Mode do
  Blender ou ZBrush); trabalhar do grande para o pequeno (formas grandes,
  depois médias, depois detalhes).
- **Como validar**: esculpir uma cabeça simples e, depois, o personagem
  inteiro em estilo estilizado.
- **Atalho solo**: em estilo low-poly ou estilizado, pule a escultura (e o
  bake da etapa 4b) e modele direto o low-poly.

## Etapa 4a: Retopologia (low-poly)

- **Quem faz (guia)**: character artist, às vezes com o technical artist.
- **No OpenGlitch**: `arte-3d` / `character-artist`, com `technical-artist`.
- **Recebe**: a escultura high-poly e o orçamento técnico de polígonos.
- **Entrega**: malha leve e limpa, com o número de polígonos do orçamento
  técnico e edge loops onde o corpo dobra.
- **Por que importa**: a retopologia faz o modelo deformar de forma natural
  nos movimentos e simplifica o weight painting. Personagens animados
  precisam de edge loops em volta dos olhos, da boca e das articulações, que
  ferramentas automáticas nem sempre fazem bem.
- **Precisa estar certo**: quads; edge flow seguindo os músculos; poles bem
  posicionados; loops extras em cotovelo, joelho e ombro. Ferramentas: retopo
  do Blender (snap, shrinkwrap) ou ZRemesher.
- **Como validar**: dobrar o braço e o joelho com um rig simples. Onde
  amassar, adicione loops.
- **Atalho solo**: modelar direto o low-poly em estilo low-poly ou
  estilizado.

## Etapa 4b: UV e bake

- **Quem faz (guia)**: character artist ou texture artist.
- **No OpenGlitch**: `arte-3d` / `character-artist` e `texture-material`.
- **Recebe**: o low-poly e o high-poly.
- **Entrega**: UVs (a malha "desembrulhada" em 2D) e mapas "bakeados" do
  high-poly para o low-poly: normal map, ambient occlusion, curvature.
- **Precisa estar certo**:
  - seams (cortes do UV) em lugares escondidos;
  - UV sem estiramento e com densidade de texel parecida;
  - cage e distância de projeção no bake;
  - hard edges sempre na borda de uma ilha de UV, senão aparecem costuras no
    normal map;
  - tangent space (MikkTSpace) compatível com a engine.
- **Como validar**: fazer o UV do low-poly, bakear o normal map da escultura e
  conferir na Unity se não aparecem costuras.
- **Atalho solo**: em estilo low-poly ou estilizado, pule o bake.

## Etapa 5: Texturas

- **Quem faz (guia)**: texture / material artist.
- **No OpenGlitch**: `arte-3d` / `texture-material`.
- **Recebe**: o low-poly com UV e os mapas do bake.
- **Entrega**: mapas PBR (base color, roughness, metallic, normal) ou
  texturas pintadas à mão, no estilo do jogo.
- **Precisa estar certo**: teoria PBR; Substance Painter ou alternativas
  (Blender, Material Maker). Para estilo Arcane, pinte luz e pinceladas na
  própria textura.
- **Como validar**: texturizar o personagem com 3 materiais bem diferentes
  (pele, tecido, metal).
- **Atalho solo**: cores chapadas ou pintadas à mão no lugar de PBR completo.

## Etapa 6: Rig e skinning

- **Quem faz (guia)**: rigger.
- **No OpenGlitch**: `animacao` / `rigger`.
- **Recebe**: o low-poly texturizado, com topologia que deforma bem.
- **Entrega**: esqueleto padronizado, weight painting (quanto cada osso puxa
  da malha), controles de animação e, separado, o esqueleto de jogo leve.
- **Precisa estar certo**: hierarquia de ossos, IK/FK, weight painting; nomes
  de ossos compatíveis com o Humanoid da Unity (facilita o retargeting).
- **Como validar**: rigar com Rigify, gerar o esqueleto de jogo e testar
  poses extremas (agachar, braço para cima).
- **Atalho solo**: rig automático (Rigify, AccuRig ou Mixamo) para testar
  rápido.

## Etapa 7: Animação

- **Quem faz (guia)**: animadores de gameplay e de cinematic, mocap e
  cleanup.
- **No OpenGlitch**: `animacao` / `gameplay-animator`, `cinematic-animator` e
  `mocap-cleanup`.
- **Recebe**: o personagem rigado e a animation list vinda da ficha da etapa
  0.
- **Entrega**: a animation list completa (parado, andar, correr, pular,
  golpes, reações, morte), ciclos em loop e transições.
- **Precisa estar certo**: os 12 princípios, ciclos de locomoção,
  responsividade, retargeting de mocap. O detalhe do pipeline está em
  `pipelines/animacao-em-jogo`.
- **Como validar**: os 4 movimentos básicos (parado, andar, correr, pulo) e 1
  golpe no personagem.
- **Atalho solo**: animações prontas para testar o jogo, trocando depois pelas
  próprias.

## Etapa 8: Engine

- **Quem faz (guia)**: technical artist, animation TD e programadores.
- **No OpenGlitch**: `arte-3d` / `technical-artist`, `animacao` /
  `animation-td` e o agente `engenharia`.
- **Recebe**: o personagem texturizado, rigado e animado.
- **Entrega**: FBX importado com escala certa, materiais e shaders
  configurados (pele, cabelo, roupa), LODs (versões mais leves para longe),
  Animator configurado e testes de desempenho.
- **Precisa estar certo**:
  - importação: escala e unidades (a Unity usa 1 unidade = 1 metro; o 3ds Max
    usa 1 unidade = 10 cm), tipo de rig Humanoid ou Generic, blend shapes;
  - LODs: se as malhas forem nomeadas `_LOD0`, `_LOD1`, `_LOD2`, a Unity cria
    o LOD Group sozinha na importação;
  - shaders e testes: shader graph, profiler, testar o personagem em cena real
    com a luz do jogo.
- **Como validar**: exportar o personagem final com 3 LODs, importar na Unity,
  configurar o Animator e medir o desempenho com 20 cópias na cena.
- **Atalho solo**: nenhum específico no guia; use os atalhos das etapas
  anteriores.

## Pipeline solo enxuto

Para um primeiro personagem jogável, dá para pular etapas sem perder muito:

- Estilo low-poly ou estilizado: modele direto o low-poly e pule escultura e
  bake (etapas 3 e 4b).
- Texturas simples: cores chapadas ou pintadas à mão no lugar de PBR
  completo.
- Rig automático: Rigify, AccuRig ou Mixamo para testar rápido.
- Animações prontas para testar o jogo, trocando depois pelas do usuário.

Sem desenho, troque o concept por moodboard e ficha escrita. Proponha esse
caminho ao usuário solo antes de propor o pipeline completo.
