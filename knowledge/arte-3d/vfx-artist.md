---
title: VFX artist
summary: Cria efeitos como fogo, fumaça, explosões, magia, impactos e tiros, e dá peso ao combate com partículas, flipbooks e shaders de efeito.
---

## O que faz

Cria efeitos: fogo, fumaça, explosões, magia, impactos, tiros e chuva. Dá
"peso" ao combate.

## O que entrega

- **Sistemas de partículas**.
- **Flipbooks**.
- **Shaders de efeito**.
- **Efeitos sincronizados** com a animação e o som.

## Fundamentos

- **Ferramentas**: Niagara na Unreal ou VFX Graph no Unity.
- **Shaders básicos**, porque muito do efeito depende deles.
- **Timing**: antecipação, impacto e dissipação.
- **RealTimeVFX**, comunidade criada por devs da Riot, EA e Naughty Dog, com o
  thread Getting Started para iniciantes.
- **Economia visual**: o Game Art Tricks mostra como enganar o jogador gastando
  pouco.
- O Houdini é citado pelo guia como ferramenta de efeitos de estúdio.

## Como validar

- Faça o efeito de um golpe de espada: rastro, faísca no impacto e poeira no chão.
- Os três tempos (antecipação, impacto, dissipação) são claros e casam com a
  animação e com o som de impacto.
- O efeito aumenta o peso do golpe sem esconder o que está acontecendo.
- A quantidade de partículas não derruba a meta de FPS.

## Ligações com outras áreas

- **Combat designer** (Design) define o game feel; o efeito faz parte dele.
- **Animação** define os quadros de impacto com os quais o efeito sincroniza.
- **Áudio** faz o som de impacto que acompanha o efeito.
- **Engenharia** dispara o efeito no momento certo.
- O **technical artist** ajuda nos shaders e no custo de desempenho.
