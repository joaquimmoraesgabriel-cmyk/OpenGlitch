---
title: Pipeline de animação em jogo
summary: As 6 etapas da animação em jogo, da animation list ao playtest, com os donos de cada uma no OpenGlitch.
---

Seis etapas levam um movimento da ideia até um controle que responde bem. A
etapa 7 do pipeline de personagem (`pipelines/personagem`) usa este fluxo.

## Etapa 1: Animation list

- **O que é**: a lista de todos os movimentos necessários.
- **Dono**: o agente `design` define as ações (o que o personagem faz); o
  agente `animacao` organiza a lista.
- **Recebe**: a ficha do personagem e as mecânicas.
- **Entrega**: a lista completa, com o que é mocap e o que é keyframe.
- **Como validar**: cada ação das regras do jogo tem uma linha na lista.

## Etapa 2: Produção

- **O que é**: mocap ou keyframe manual.
- **Dono**: `animacao`, com `mocap-cleanup` e `gameplay-animator`.
- **Recebe**: a animation list.
- **Entrega**: as animações brutas de cada item da lista.
- **Como validar**: cada item da lista tem uma versão produzida.

## Etapa 3: Cleanup e polimento

- **Dono**: `animacao`.
- **Recebe**: as animações brutas.
- **Entrega**: animações limpas, que se conectam sem "pulos", com transições
  suaves.
- **Como validar**: ciclos fecham em loop e as transições não mostram saltos.

## Etapa 4: Exportação

- **O que é**: levar as animações para a engine.
- **Dono**: `animacao` / `animation-td`.
- **Recebe**: as animações polidas.
- **Entrega**: os arquivos exportados para a engine.
- **Como validar**: as animações abrem na engine sem perder timing nem
  escala.

## Etapa 5: Implementação

- **O que é**: state machines, transições, blends, IK nos pés e nas mãos.
- **Dono**: `animacao` / `animation-td`, com `engenharia` /
  `gameplay-programmer`.
- **Recebe**: as animações exportadas e as mecânicas.
- **Entrega**: o personagem controlável com as animações ligadas.
- **Como validar**: o personagem troca de estado pelo controle sem saltos, e
  os pés e as mãos se ajustam ao ambiente.

## Etapa 6: Playtest

- **O que é**: ajustar o timing até o controle ficar bom.
- **Dono**: `design`, com apoio de `apoio` / `qa`.
- **Recebe**: o personagem controlável.
- **Entrega**: ajustes de timing devolvidos às etapas anteriores.
- **Como validar**: quem testa joga sem explicação e o controle responde
  bem. Se o timing estiver ruim, volte à etapa 3 ou 5.
