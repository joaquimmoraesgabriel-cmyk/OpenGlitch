---
title: Audio programmer
summary: Integra o som na engine: quando cada som toca, distância, oclusão, mixagem dinâmica e desempenho, com FMOD, Wwise ou áudio nativo.
---

## O que faz

Integra o som na engine. Define quando cada som toca, como ele soa conforme a
distância, a oclusão, a mixagem dinâmica e o desempenho.

## O que entrega

- **Integração com FMOD ou Wwise**.
- **Som 3D**.
- **Regras de mixagem e prioridade**.
- **Ferramentas** para os sound designers trabalharem sem depender de código.

## Fundamentos

- Áudio nativo da Unity: AudioSource e AudioMixer. Para começar sozinho, é
  suficiente.
- Um middleware: FMOD ou Wwise. O Wwise-101 tem 20 lições, 20 quizzes e 1
  exame. O FMOD tem licença Indie gratuita ou US$ 2.000 por título para
  orçamentos abaixo de US$ 600 mil, segundo o guia; confira em fmod.com/licensing.
- Áudio 3D: atenuação por distância e reverb por área.
- O artigo do Designing Sound sobre aprender middleware é de 2015, mas a lógica
  de comparação vale.

## Como validar

- Passos que mudam conforme o chão (madeira, pedra, grama).
- Música que muda quando o combate começa e volta quando termina.
- Um som 3D some gradualmente com a distância, e o reverb muda ao entrar numa
  área fechada.
- Há prioridade definida: com muitos sons ao mesmo tempo, os importantes
  (impacto, fala) continuam audíveis.
- O custo de áudio no desempenho foi medido numa máquina fraca.
- A licença do middleware escolhido foi conferida para o orçamento do projeto.

## Ligações com outras áreas

- Recebe do **sound designer**, do **compositor** e da **dublagem** os
  arquivos e a lista de eventos.
- A **Engenharia** chama os eventos no código do jogo.
- A **Animação** fornece os pontos em que passos e golpes devem soar.
- **QA** testa passos por chão, troca de música e desempenho do som.
