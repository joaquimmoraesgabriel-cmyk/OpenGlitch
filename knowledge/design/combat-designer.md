---
title: Combat designer
summary: Cria o combate (golpes, armas, inimigos e a sensação de cada ataque), central em jogos de luta, tiro e ação.
---

## O que faz

Cria o combate: golpes, armas, inimigos e o "feeling" de cada ataque. É
central em jogo de luta, tiro e ação.

## O que entrega

- **Moveset**: os golpes, cada um com dano, startup e recovery.
- **Design de inimigos**: o que cada um faz e como avisa antes de atacar.
- **Encontros**: combinações de inimigos.
- **Ajuste de game feel**: hitstop, screen shake, partículas e som do impacto.

## Fundamentos

- O combate é o jogo fazendo perguntas (o comportamento dos inimigos), dando
  ferramentas para responder (os ataques do jogador) e mudando as perguntas a
  cada luta.
- Um ataque quase nunca é divertido na primeira versão. O que falta costuma
  ser game feel.
- Jogar com atenção e contar frames: startup, frames ativos e recovery de cada
  golpe.
- Reparar no que o inimigo avisa antes de atacar. O aviso é o que torna o
  ataque justo de enfrentar.
- Em jogo de luta e multiplayer, balanceamento e leitura do adversário
  seguem princípios próprios.

## Como validar

- O combate mínimo está pronto quando existe um personagem com 3 golpes e 1
  inimigo com 2 ataques, e a luta é justa depois de ajustes.
- Justa quer dizer que o jogador consegue ler cada ataque do inimigo pelo aviso
  e responder com uma ferramenta que ele tem.
- Com 2 inimigos juntos, a luta continua legível e justa. Se não, a
  combinação ou o espaço precisa mudar.
- Cada golpe tem startup e recovery definidos e o custo de errar é visível.
- Os golpes têm peso: hitstop, shake, partícula e som estão ajustados, e o
  golpe sem eles seria percebido como fraco.

## Ligações com outras áreas

- O moveset e os ataques dos inimigos viram a **animation list** da Animação.
- Os números de dano e vida vêm do balanceamento do game designer.
- O level designer posiciona os encontros e dá o espaço da arena.
- Hitstop, shake e câmera de impacto dependem de Engenharia; partículas e som
  dependem de VFX e Audio.
- A IA dos inimigos é implementada por Engenharia.
