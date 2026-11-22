---
title: QA (testes)
summary: Joga para quebrar o jogo e reporta bugs, travamentos, partes confusas e problemas de desempenho de forma que o programador consiga corrigir.
---

## O que faz

Joga para quebrar o jogo: procura bugs, travamentos, partes confusas e
problemas de desempenho. Reporta de um jeito que o programador consiga
corrigir.

## O que entrega

- **Bug reports** claros.
- **Planos de teste**.
- **Testes de regressão**.
- **Relatórios de desempenho** em máquinas diferentes.

## Fundamentos

- Escrever bom bug report é a habilidade principal. Os campos que as fontes
  citam: título, passos para reproduzir, esperado versus real, ambiente,
  severidade e evidências.
- Pensar como quem quer quebrar o jogo.
- Severidade é quão grave é o problema; prioridade é quão urgente é
  corrigi-lo. Os dois são diferentes: um bug leve pode ser urgente antes de
  um evento, e um grave e raro pode esperar.
- Em projeto solo o desenvolvedor é o próprio QA. Chamar amigos para jogar e
  observar sem ajudar mostra onde o jogador trava.

## Como validar

- Ache 5 bugs num jogo indie gratuito e escreva um report bem feito de cada
  um.
- Um bug report está bom quando outra pessoa reproduz o problema só lendo o
  texto, sem perguntar nada.
- Cada relatório traz severidade e prioridade separadas, com o motivo.
- No playtest, quem testa não recebe explicação, e o que a pessoa não entende
  sozinha é anotado como problema de regra ou de interface.
- O plano de teste lista o que se repete a cada versão (regressão) e as
  máquinas em que o desempenho foi medido.

## Ligações com outras áreas

- Valida as entregas de todos os agentes e devolve bugs a quem construiu.
- Roda o playtest da etapa 6 do pipeline de animação junto com o **Design**.
- Testa as regras e o balanceamento do **game designer**.
- Testa a integração de som com o **audio programmer** (passos, música).
- Testa o jogo traduzido (LQA) com a **localização**.
