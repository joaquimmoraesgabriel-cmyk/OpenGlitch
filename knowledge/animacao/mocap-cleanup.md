---
title: Mocap e cleanup
summary: Captura movimento de atores, limpa os dados e adapta ao esqueleto do jogo por retargeting.
---

## O que faz

Captura movimentos de atores e limpa os dados (tremedeira, pés escorregando),
adaptando ao esqueleto do jogo. Também pode partir de bancos de mocap prontos.

## O que entrega

- Animações capturadas limpas.
- Retargeting para cada personagem.
- Loops e transições feitos a partir dos takes.

## Fundamentos

- Formatos: BVH e FBX.
- Retargeting: no Blender, no Humanoid da Unity e no IK Retargeter da Unreal.
- Limpeza de curvas e foot locking.
- O CMU Graphics Lab Motion Capture Database tem 2.605 capturas em 6 categorias;
  o guia recomenda começar pelos sujeitos de número mais alto, e há versão em FBX.
- **Licença do CMU**: permite incluir os dados em produtos vendidos, mas proíbe
  revender os dados diretamente, mesmo convertidos. Pode ser usado dentro de um
  jogo, não para vender um pacote feito só com eles.
- Mixamo e pacotes de animação servem para testar rápido; confira os termos antes
  de distribuir.

## Como validar

- Baixe uma animação de mocap gratuita, faça retargeting para o personagem e
  corrija os pés.
- Os pés ficam fixos no chão durante o contato; não há tremedeira visível nas
  curvas.
- Os loops fecham e a origem e a licença de cada dado estão registradas.

## Ligações com outras áreas

- Usa o rig e os nomes de ossos do rigger.
- O animation TD liga os clipes limpos na state machine.
- Se o resultado for vendido como pacote, a licença do dado define o que pode
  ser incluído (é uma decisão de escopo do Design e do usuário).
