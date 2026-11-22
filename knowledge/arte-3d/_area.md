---
title: Arte 3D
summary: A área que define o visual do jogo e produz os assets 3D: concept, personagens, cenários, props, materiais, luz, efeitos e a ponte técnica com a engine.
---

## O que a área faz

Arte 3D define como o jogo se parece e produz o que roda na tela. Reúne a
direção de arte e oito funções: concept artist, character artist, environment
artist, props e hard-surface artist, texture e material artist, lighting
artist, VFX artist e technical artist. O diretor de arte define o visual do
jogo inteiro e garante que tudo pareça do mesmo mundo.

É a área com mais material gratuito em texto, quase tudo em forma de
breakdowns, em que o artista mostra passo a passo como fez. A base para todos os
cargos é o Blender, que é gratuito, e o Manual do Blender.

## Direção de arte

O diretor de arte entrega o style guide ou art bible (paleta, formas, materiais,
proporções), moodboards, paintovers (pintar por cima do trabalho dos artistas
para corrigir) e a aprovação dos assets. Os fundamentos são forma, cor, luz,
composição e silhueta, mais o básico do pipeline 3D.

O exercício do guia: escolher um estilo (por exemplo estilizado tipo Arcane ou
low-poly) e montar uma art bible de 5 páginas para o projeto. A art bible está
pronta quando outra pessoa consegue dizer, só por ela, se um asset novo pertence
ao jogo.

## Pipeline de personagem

Do zero ao jogo, com os donos de cada etapa:

0. Ficha do personagem: Design.
1. Concept: concept artist.
2. Blockout: character artist.
3. Escultura high-poly: character artist.
4a. Retopologia: character artist, às vezes com o technical artist.
4b. UV e bake: character artist ou texture artist.
5. Texturas: texture e material artist.
6. Rig e skinning: Animação (rigger).
7. Animação: Animação.
8. Engine (exportação, shaders, LODs, testes): technical artist, animation TD e
   programadores.

Um primeiro personagem jogável pode usar o pipeline solo enxuto: modelar direto
o low-poly em estilo simples e pular escultura e bake, usar cores chapadas ou
pintadas à mão no lugar de PBR completo, rig automático para testar e animações
prontas até trocar pelas do projeto.

## Por onde começar sendo solo

1. Blender básico e o Manual do Blender.
2. The PBR Guide.
3. Game Art Tricks, que ensina a economizar bem.
4. Unity for Technical Artists.

Personagem muito detalhado, hard surface avançado e VFX podem ser comprados
prontos no começo.

## Ligações com outras áreas

- **Design**: o brief define o estilo visual e as listas de personagens,
  cenários e props. O blockout do level designer é a base do environment artist.
- **Animação**: recebe a malha com topologia para dobrar bem; o rigger e o
  animation TD fecham as etapas 6 e 8 do personagem.
- **Cinematics**: a luz e o visual das cenas vêm desta área; o enquadramento é de
  Cinematics.
- **Engenharia**: define a engine, a meta de FPS e o orçamento técnico junto com
  o technical artist.
- **Áudio**: o efeito visual do impacto trabalha junto com o som de impacto.
- **Apoio**: QA valida desempenho e aparência nas plataformas.
