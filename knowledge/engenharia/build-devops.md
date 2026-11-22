---
title: Build engineer / DevOps
summary: Garante que o jogo compile, seja testado e chegue aos jogadores.
---

## O que faz

Garante que o jogo compile, seja testado e chegue aos jogadores.

## O que entrega

- Controle de versão com Git LFS (ou Perforce).
- Build automático (CI/CD).
- Testes automáticos.
- Publicação na Steam, itch.io ou Asset Store.

## Fundamentos

- **Git e Git LFS**: o Git guarda o histórico do código; o LFS guarda arquivos
  grandes (texturas, modelos, áudio) fora do histórico comum. Projetos de jogo
  precisam dele.
- **Perforce**: alternativa para projetos com muitos arquivos binários.
- **CI/CD com GitHub Actions**: a cada envio de código, uma máquina compila o
  projeto e roda os testes. O GameCI é a solução open source para jogos.
- **Processo de cada loja**: Steam, itch.io e Asset Store têm exigências e
  passos próprios de publicação.

## Como validar

- Um projeto Unity no GitHub com Git LFS.
- Um build automático para Windows a cada push.
- O build sai do repositório limpo, sem passo manual escondido.
- Os testes automáticos rodam no CI e um teste quebrado reprova o build.
- Os arquivos grandes estão no LFS e o repositório não incha.

## Ligações com outras áreas

- Todos os agentes entregam arquivos que entram no repositório; as regras de LFS
  e de pastas valem para a Arte 3D, a Animação e o Áudio.
- O QA testa os builds gerados.
- O Apoio cuida da página da loja e da divulgação.
- O tools-programmer pode adicionar validações que rodam antes do build.
