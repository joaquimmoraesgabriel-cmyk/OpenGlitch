---
title: Level designer
summary: Monta fases e mapas, decide por onde o jogador anda e guia o jogador pelo espaço, sem seta na tela.
---

## O que faz

Monta fases e mapas. Decide por onde o jogador anda, onde ficam inimigos e
segredos, e guia o jogador sem seta na tela.

## O que entrega

- **Planta ou mapa 2D** da fase.
- **Blockout (greybox)**: a fase só com cubos.
- **Ritmo da fase**: onde há tensão e onde há descanso.
- **Posicionamento** de inimigos, itens e checkpoints.

## Fundamentos

- Desenhar de memória o mapa de uma fase de que se gosta e anotar por que ela
  funciona.
- Fluxo: caminho principal, landmarks e linhas de visão são o que orienta o
  jogador.
- Blockout na engine: ProBuilder na Unity, Modeling na Unreal.
- Estudar fases reais com mapa e análise, como Undead Burg em Dark Souls 1.

## Como validar

- Existe uma fase só com cubos cinza, com 5 a 10 minutos de duração.
- Alguém joga sem receber explicação. O ponto onde a pessoa se perde mostra
  onde o fluxo falhou; ajuste o espaço (landmark, linha de visão, forma), não
  a pessoa.
- O caminho principal é achado sem seta e sem instrução.
- O ritmo tem trechos de tensão e trechos de descanso, e o jogador nota a
  diferença.
- Cada inimigo, item e checkpoint está num lugar que o mapa justifica.

## Ligações com outras áreas

- O game designer define as regras e o core loop que a fase precisa sustentar.
- O combat designer define os encontros que o level designer posiciona.
- O blockout é a base do cenário que a Arte 3D produz depois.
- O blockout e o mapa orientam a câmera e o enquadramento em Cinematics.
- Engenharia implementa checkpoints, gatilhos e carregamento da fase.
