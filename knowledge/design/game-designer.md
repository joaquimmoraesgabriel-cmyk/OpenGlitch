---
title: Game designer
summary: Cria as regras do jogo (o que o jogador faz, como ganha, perde e evolui) e cuida do balanceamento.
---

## O que faz

Cria as regras do jogo: o que o jogador pode fazer, como ganha, como perde e
como evolui. Também cuida do balanceamento, para que nenhuma opção seja
obviamente a melhor nem inútil.

## O que entrega

- **GDD** e um documento para cada mecânica.
- **Core loop**: o ciclo que o jogador repete. Exemplo: explorar → lutar →
  pegar loot → melhorar → explorar.
- **Planilhas de balanceamento**: dano, vida, preço, XP.
- **Protótipos** para testar as regras.

## Fundamentos

- Ler um jogo e escrever o core loop dele: é o exercício que revela como as
  mecânicas se sustentam.
- Planilha (Excel ou Google Sheets) como ferramenta de balanceamento: os
  números vivem na planilha antes de irem para o jogo.
- Protótipo feio testado com outras pessoas. Uma regra só se prova no teste;
  no papel ela é uma hipótese.

## Como validar

- Mude uma regra e observe como o jogo muda. Em jogos simples (jogo da velha,
  Uno) o efeito aparece na hora; num protótipo digital, repita com a regra que
  está em dúvida.
- O core loop está certo quando dá para descrevê-lo em uma linha e cada passo
  leva naturalmente ao seguinte.
- A planilha está útil quando mudar um número nela diz, antes do teste, o que
  deve acontecer no jogo.
- Quem testa não deve receber explicação. O que a pessoa não entende sozinha
  é um problema de regra ou de interface.

## Ligações com outras áreas

- As ações que as regras permitem viram a **animation list** da Animação.
- Cada mecânica vira um sistema para o **gameplay programmer**.
- O combat designer detalha as regras de combate; o level designer distribui
  os desafios nas fases.
- QA testa as regras e o balanceamento.
