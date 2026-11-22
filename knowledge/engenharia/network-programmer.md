---
title: Network programmer
summary: Programa o multiplayer: conexão, sincronização e como esconder o lag.
---

## O que faz

Programa o multiplayer: conexão, sincronização entre jogadores e como esconder o
lag.

## O que entrega

- Arquitetura cliente-servidor.
- Sincronização de estado.
- Predição no cliente.
- Compensação de lag.
- Proteção contra trapaça.

## Fundamentos

- **Servidor autoritativo**: o servidor tem a palavra final sobre o estado do
  jogo, e o cliente só envia comandos. Isso protege contra trapaça.
- **Predição e reconciliação**: o cliente aplica o comando na hora, sem esperar
  o servidor, e depois corrige quando o servidor responde com o estado real.
- **Interpolação**: os outros jogadores são mostrados com um pequeno atraso,
  suavizando o movimento entre as atualizações recebidas.
- **Compensação de lag**: o servidor leva em conta a latência de quem atirou
  ao decidir se o golpe acertou.
- **Biblioteca de rede**: Netcode for GameObjects ou Mirror na Unity, Replication
  na Unreal.
- **Escopo**: multiplayer custa muito e muda a arquitetura inteira. Quem
  trabalha sozinho deve evitar no primeiro jogo.

## Como validar

- Dois jogadores andam numa sala, com lag simulado, e o movimento fica suave.
- O servidor decide o estado: um cliente alterado não consegue mudar o resultado
  sozinho.
- Quando o servidor discorda da predição, a correção não aparece como
  teletransporte.
- O jogo continua jogável com perda de pacote e latência altas o suficiente para o
  público-alvo.

## Ligações com outras áreas

- O Design decide se o jogo é multiplayer e como as regras funcionam entre
  jogadores.
- O gameplay programmer escreve o controle de modo que possa ser predito e
  refeito.
- O ai-programmer define o que a IA roda no servidor.
- O build-devops cuida do build do cliente e do servidor.
- O QA testa com condições reais de rede.
