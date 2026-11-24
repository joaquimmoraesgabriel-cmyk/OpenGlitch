---
title: Medir o tempo de GPU na Unity sem leituras falsas
summary: Como medir o tempo de GPU por script no editor e no build da Unity, e as armadilhas que dobram ou zeram a medida sem aviso.
tipo: original
fonte:
autor: openglitch (testes jardim-ao-vento e jardim-realista)
testado_em: Unity 6000.6.10f1, URP 17.6, D3D12, Unity CLI 1.0.1
---

Medida de desempenho só serve se for comparável com a anterior. Nos testes,
várias medidas saíram erradas por motivos que não tinham relação com o que
estava sendo medido. Visto numa máquina: confira na sua.

## Antes de cada rodada de medidas

- **Resolução real.** Leia o tamanho em pixels da câmera
  (`Camera.pixelWidth` e `pixelHeight`). `Screen.width` chamado por script no
  editor pode devolver 640x480. Uma janela de jogo em 4K dobrou o tempo de GPU
  sem ninguém perceber; uma janela pequena de 880x377 escondeu o custo.
- **Fixe a resolução**: `PlayModeWindow.SetCustomRenderingResolution(1920,
  1080, "nome")`.
- **Nível de qualidade.** A troca de qualidade dentro do jogo pode gravar a
  preferência. Aplique o nível da medida de forma explícita e devolva o do
  usuário depois.
- **Base na mesma sessão.** Meça sem o efeito novo e com ele na mesma rodada,
  nos mesmos pontos. Grave a resolução e o nível junto de cada medida.
- **Pontos fixos.** Grave as coordenadas e a direção da câmera de cada ponto de
  medida no projeto, para a rodada seguinte usar os mesmos.

## Como ler o tempo de GPU

- Ligue `PlayerSettings.enableFrameTimingStats = true` antes de entrar no modo
  de jogo. Sem isso, `FrameTimingManager.GetLatestTimings` devolve zero.
- Use `FrameTimingManager.CaptureFrameTimings` e `GetLatestTimings`. As
  propriedades antigas de tempo de quadro estão obsoletas.
- Os gravadores de GPU por passagem do URP não devolveram amostras no modo de
  jogo do editor. Para saber o que pesa, desligue um sistema por vez
  (vegetação, árvores, sombras, cada efeito) e compare o total.

## Armadilhas durante a medida

- **Entrada real chega ao jogo.** Com o editor rodando em segundo plano, o
  mouse e o teclado do usuário movem o jogador no meio da medida. Trave a
  entrada no controlador enquanto mede.
- **Trocar sombras em modo de jogo zera a leitura.** Depois de mudar o tipo de
  sombra da luz ou a resolução do mapa de sombras, o tempo de GPU vem perto de
  zero por alguns quadros. Descarte ou espere.
- **Editar script no disco tira o editor do modo de jogo.** Pare o jogo antes
  de editar e espere a recompilação terminar.
- **Valor gravado na cena vence o padrão do script.** Ao mudar um padrão,
  remonte a cena ou atualize o componente antes de medir.

## Editor e build

O editor soma custo próprio de CPU. Para um número final, gere o executável,
rode a mesma bancada nele e leia o log do jogo. O executável também mostra
erros que o editor esconde.

## Como conferir

- A base sem o efeito novo precisa bater com a da rodada anterior. Se não
  bater, o problema está na medição, não no efeito.
- Informe a mediana e o percentil 95 de cada ponto, não só a média.
