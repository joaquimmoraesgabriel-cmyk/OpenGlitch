---
title: Lighting artist
summary: Ilumina as cenas para criar clima e guiar o olhar sem pesar no desempenho, com luz, sombras, GI e pós-processamento.
---

## O que faz

Ilumina as cenas para criar clima e guiar o olhar do jogador sem pesar no
desempenho.

## O que entrega

- **Iluminação de cada área** do jogo.
- **Sombras** e **GI** (luz rebatida).
- **Pós-processamento**.
- **Luz das cutscenes**.

## Fundamentos

- **Cor e luz da fotografia e do cinema**: o Gurney Journey e o livro Color and
  Light explicam cor e luz em pintura, e valem para cena 3D.
- **Luz em tempo real contra luz bakeada**: a escolha muda o custo de
  desempenho e o que a luz permite.
- **Estudo de luz de filmes e séries**: o Arcane é um ótimo exemplo.
- **Pipelines das engines**: o guia de iluminação HDRP da Unity (e-book
  gratuito) e a documentação de iluminação da Unreal (Lumen e
  pós-processamento).
- O mesmo espaço muda de clima só com a luz.

## Como validar

- Ilumine a mesma cena de 3 jeitos: dia feliz, noite de terror e pôr do sol
  melancólico. Cada versão deve passar o clima pedido apenas com luz, cor e
  pós-processamento.
- O olhar vai para onde o design da fase quer.
- A cena roda dentro da meta de FPS com a luz escolhida.
- Os materiais continuam legíveis sob cada luz.

## Ligações com outras áreas

- **Design** define o clima desejado de cada fase e momento da história.
- **Cinematics** usa a luz base nas cutscenes e faz o acabamento final do plano.
- O **environment artist** entrega a cena a ser iluminada.
- O **texture artist** define materiais que precisam ler bem sob a luz.
- O **technical artist** mede o custo de desempenho da iluminação.
