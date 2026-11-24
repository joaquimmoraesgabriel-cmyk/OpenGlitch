---
title: Controlar a Unity aberta pelo Unity CLI
summary: O que funcionou e o que tropeçou ao compilar, rodar C#, capturar a tela e montar cenas na Unity aberta pelo Unity CLI, a partir de um terminal no Windows.
tipo: original
fonte:
autor: openglitch (testes jardim-ao-vento e jardim-realista)
testado_em: Unity 6000.6.10f1, Unity CLI 1.0.1, Windows PowerShell 5.1
---

O Unity CLI deixa um agente compilar, executar código no editor aberto, ler o
console e capturar a tela. Notas práticas de dois projetos de teste; os
comandos mudam com a versão, então confira a ajuda da sua.

## Executar C# no editor

- No PowerShell 5.1, aspas duplas dentro de um argumento somem ao chamar um
  executável. Passe o código por arquivo (`script eval --file`) em vez de
  escrevê-lo na linha de comando.
- Depois de uma atualização que recompila, espere o estado de recompilação
  terminar antes da próxima chamada. Chamar antes devolve erro de editor não
  disponível.

## Modo de jogo

- Editar um script no disco durante o modo de jogo faz o editor recompilar e
  sair dele. Pare o jogo, edite, espere ficar pronto e entre de novo.
- Com o modo de jogo iniciado pelo CLI, o editor continua rodando em segundo
  plano e recebe o mouse e o teclado do usuário.

## Capturas

- A captura pela câmera, com largura e altura pedidas, renderiza na resolução
  real. A captura da tela só amplia a janela de jogo como ela está.
- Capture pelo ponto de vista do jogador e, para comparar antes e depois, da
  mesma posição e direção.

## Montagem que se repete

- O que for montado no editor precisa de um script de montagem chamado por um
  item de menu, para a cena poder ser refeita com um comando.
- Texto de shader ou de script regravado em modo texto no Windows pode trocar
  os fins de linha e fazer o controle de versão marcar o arquivo inteiro como
  alterado. Preserve o fim de linha original do arquivo.
- Atualizar arquivos com o editor em modo de jogo pode não reimportar um
  shader: force a importação do arquivo antes de concluir que a mudança não
  teve efeito.

## Como conferir

- Console sem erros e sem avisos novos depois de cada mudança.
- Uma captura depois de cada etapa de montagem.
- Ao final, um executável gerado e rodado, com o log do jogo lido.
