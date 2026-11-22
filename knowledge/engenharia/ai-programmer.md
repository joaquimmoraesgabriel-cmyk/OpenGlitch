---
title: AI programmer
summary: Programa o comportamento de inimigos e NPCs: ver, perseguir, atacar, fugir e agir em grupo.
---

## O que faz

Programa o comportamento de inimigos e NPCs: ver, perseguir, atacar, fugir e
agir em grupo.

## O que entrega

- Pathfinding.
- Sistemas de decisão: state machines, behavior trees e utility AI.
- Percepção: visão e audição.
- IA de grupo.

## Fundamentos

- **A\***: a base do pathfinding. Vem junto com a busca em largura e o Dijkstra,
  que ajudam a entender quando cada um serve.
- **Behavior trees**: estrutura de decisão em árvore, com nós de sequência,
  seletor e folhas de ação, boa para comportamento complexo e reutilizável.
- **State machines e utility AI**: a state machine é a opção mais simples;
  utility AI pontua as ações e escolhe a de maior valor.
- **Percepção**: o inimigo só reage ao que vê ou ouve, com alcance, cone de
  visão e memória do último ponto onde viu o alvo.
- **Princípio**: a IA de jogo precisa ser divertida, não perfeita. Um inimigo
  que avisa o que vai fazer e erra de propósito é melhor para o jogo do que
  um inimigo ótimo.

## Como validar

- Um inimigo patrulha, ouve um som, investiga e persegue quando vê o jogador.
- Três inimigos tentam cercar o jogador sem se bloquearem.
- O inimigo não sabe onde o jogador está sem ter percebido.
- O caminho encontrado contorna obstáculos e o custo não pesa no quadro.
- Quem joga entende o que o inimigo está fazendo e consegue reagir.

## Ligações com outras áreas

- O combat designer define o que cada inimigo faz, o telegraph dos ataques e
  como os inimigos se combinam num encontro.
- O level designer posiciona inimigos e define as áreas navegáveis.
- A Animação entrega as animações e a state machine que a IA aciona.
- O gameplay programmer fornece a física, o dano e os sistemas que a IA usa.
- O network programmer sincroniza a IA quando o jogo é multiplayer.
