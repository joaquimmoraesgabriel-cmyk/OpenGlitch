---
title: Engenharia
summary: A área que escreve o código do jogo e monta a base técnica: engine, arquitetura, desempenho, IA, ferramentas, rede e build.
---

## O que a área faz

Engenharia decide como o jogo é construído e o escreve. Reúne seis funções:
gameplay programmer (controle, câmera, combate, sistemas), engine e graphics
programmer (renderização, shaders, desempenho), AI programmer (comportamento de
inimigos e NPCs), tools programmer (ferramentas de editor), network programmer
(multiplayer) e build engineer / DevOps (controle de versão, build e
publicação). Em equipe pequena, uma pessoa faz quase tudo isso e também assume
o papel de diretor técnico.

O diretor técnico escolhe a engine, define a arquitetura do código e os padrões
da equipe, fixa o orçamento técnico (polígonos, texturas, personagens por cena,
meta de FPS), define o pipeline de assets e avalia os riscos técnicos.

## Base comum

Todo cargo parte da mesma base: C# para Unity (documentação da Microsoft, com
versão em português), C++ para Unreal ou engine própria, e Git (o livro Pro
Git, gratuito e traduzido). A engenharia tem o melhor material escrito
gratuito entre todas as áreas.

Duas regras valem para qualquer função. Primeiro, medir antes de otimizar: o
profiler mostra o gargalo real, e a otimização é validada comparando antes e
depois. Segundo, os sistemas ganham testes, e o que depende de sensação (controle,
câmera) é validado jogando.

## Ordem de aprofundamento

1. Game Programming Patterns.
2. Catlike Coding: Basics e Movement.
3. Editor scripting da Unity, que pesa muito para quem vende pacote para a
   Unity.
4. Pro Git e GameCI.

Gráficos, IA e rede ficam para quando um projeto precisar. Quem trabalha sozinho
deve evitar multiplayer no primeiro jogo.

## Ligações com outras áreas

- **Design**: as mecânicas viram sistemas; a Engenharia entrega protótipos para
  testar regras e expõe parâmetros para os designers ajustarem.
- **Arte 3D**: o orçamento técnico limita polígonos e texturas; o technical
  artist e a Engenharia fecham a importação, os shaders e os LODs na engine.
- **Animação**: as state machines, transições, blends e IK são implementadas junto
  com o animation TD.
- **Cinematics**: a Engenharia entrega a base de timeline e câmera que eles usam.
- **Áudio**: integração dos arquivos de som e do áudio no jogo.
- **Apoio**: QA testa os builds; a publicação passa pelo processo das lojas.
