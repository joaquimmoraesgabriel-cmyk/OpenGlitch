---
title: Blender aberto pelo MCP e tarefas longas
summary: Tarefa demorada (bake, render) trava a ponte do Blender aberto e pode fechá-lo, perdendo o que não foi salvo. Como dividir o trabalho ou rodar em segundo plano.
tipo: original
fonte:
autor: openglitch (teste jardim-realista)
testado_em: Blender 5.3, extensão MCP 1.0.3
---

Trabalhar na cena aberta é bom para inspecionar e conferir. Para trabalho
pesado ela é frágil: uma chamada longa bloqueia o Blender inteiro. Visto num
teste, numa máquina.

## O que aconteceu

Uma chamada de execução de código com bake no Cycles de três materiais, numa
cena aberta com 174 objetos, estourou o tempo (cerca de 60 s). As chamadas
seguintes também falharam, a conexão caiu e o Blender fechou e reabriu sem o
servidor. As alterações não salvas do arquivo do usuário se perderam.

Causa provável: trabalho longo bloqueando a thread principal do Blender.

## Regra

- **Antes de qualquer trabalho pesado na cena aberta, peça ao usuário para
  salvar o arquivo dele.** É a única proteção contra perda.
- **Bake, render e geração grande rodam em segundo plano**, num processo
  separado (`blender -b --factory-startup --python script.py`), que não tem
  limite de tempo. No teste foi quatro vezes mais rápido do que na cena aberta.
- **A cena aberta fica para o que é rápido**: inspecionar, criar e ajustar
  objetos, capturar a viewport, conferir o resultado.

## Se precisar fazer na cena aberta

- Divida em chamadas curtas, com um orçamento de tempo por chamada (cerca de
  40 s) e folga para o limite.
- Grave o resultado de cada etapa em cache no disco; a chamada seguinte
  continua de onde a anterior parou.

## Detalhes úteis

- Em segundo plano não existe janela (`bpy.context.window`): use a cena do
  arquivo de fábrica para o bake.
- A ferramenta de renderizar a viewport para um caminho pode gravar numa pasta
  temporária da própria extensão e ignorar o caminho pedido: leia o caminho
  que ela devolve.
- Se a conexão cair, o usuário religa em Preferências, Add-ons, MCP, no botão
  de iniciar o servidor.

## Como conferir

- Depois de uma chamada demorada, faça uma chamada simples (listar objetos)
  para confirmar que a ponte ainda responde antes de seguir.
- Confira que o arquivo do usuário não foi salvo por cima.
