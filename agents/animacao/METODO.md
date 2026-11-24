---
name: openglitch-animacao-metodo
description: Método de qualidade do agente Animação. Como decompor um clipe ou conjunto, o que pesquisar antes de animar, os sinais de animação genérica e o ciclo de captura, medição e correção.
---

# Método de qualidade: Animação

A skill diz o que você constrói. Este método diz como construir movimento que
pareça ter sido feito por alguém que entende de peso, timing e controle:
referência de movimento real, poses pensadas, curvas editadas e teste no
personagem jogável. Sem ele, o resultado sai da média do que você já viu, com
interpolação automática e tudo se mexendo ao mesmo tempo, e é isso que dá a
"cara de IA".

## Como usar este método

- **Tarefa avulsa, um clipe só ou um ajuste de timing**: siga só a "Versão
  curta".
- **Ciclo de locomoção, conjunto de ações do jogador, rig novo ou trabalho de
  projeto**: siga o método inteiro, na ordem das seções.
- A decomposição vem antes de abrir o Blender ou o Animator. A pesquisa vem antes
  de posar. A conferência vem antes de dizer que está pronto.
- Mostre ao usuário a decomposição e o que você vai pesquisar antes de começar.
  Ele pode cortar o que não importa para ele.
- O método não substitui o guia de estilo de movimento nem o brief. Em estilo
  exagerado, "bom" quer dizer pose clara e timing marcado, e não fidelidade ao
  movimento real.

## Ambiente ao vivo

Antes de animar, veja com o que você pode trabalhar. Se o seu cliente tem uma
ferramenta que executa código no Blender aberto e captura a tela dele, ou uma
que controla o editor da engine (o Unity CLI ou o servidor MCP da Unity),
use-a. Diga ao usuário, em uma linha, com o que você está trabalhando.

- **O script continua sendo a fonte.** Gere o rig e as animações por script em
  arquivo e execute-o dentro do Blender aberto. Animação criada só na cena
  aberta se perde quando o programa fecha.
- **Inspecione o rig real** antes de animar: nomes e hierarquia dos ossos,
  eixos, escala, restrições, quadros por segundo da cena. Não presuma a
  convenção de nomes.
- **Capture quadros-chave ao vivo.** Leve a linha do tempo a cada pose-chave e
  capture a viewport, de lado e de frente. Monte a tira de quadros a partir
  dessas capturas para ver antecipação, contato e assentamento.
- **Meça no objeto.** Leia de volta a posição dos pés por quadro, a duração do
  clipe e os valores do primeiro e do último quadro do loop, em vez de confiar
  no que o script pretendia.
- **Confira na engine aberta.** Importe o clipe, toque no personagem dentro do
  editor e capture. Eixos, escala e curvas mudam na importação; a rotação da
  raiz e a posição animada da raiz são os erros mais comuns.
- **Leia o console da engine** depois de importar e de montar o controlador de
  animação: clipe sem curva, osso não encontrado e avatar inválido aparecem lá.
- **Ajuste feito à mão volta para o script** antes de encerrar.
- **Tarefa longa não roda na cena aberta.** Bake, render e geração grande
  bloqueiam o programa: a ponte para de responder e o Blender pode fechar,
  levando o que o usuário não salvou. Rode em segundo plano, num processo
  separado, e use a cena aberta para inspecionar e conferir. Antes de qualquer
  trabalho pesado na cena aberta, peça ao usuário para salvar o arquivo dele.
- **Não destrua o que é do usuário.** Não apague ações, não renomeie ossos e
  não salve por cima de um arquivo existente sem perguntar.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, quatro verificações bastam:

1. **Uma referência de movimento.** Antes de posar, descreva em cinco linhas como
   o movimento é de verdade: quais quadros têm contato do pé, onde o peso se
   desloca, o que se move primeiro. Se você não sabe, delegue uma pesquisa curta.
2. **Poses-chave e timing.** Liste as poses principais com o número do quadro de
   cada uma e a taxa de quadros do projeto. Confira se a antecipação do golpe ou
   do pulo cabe no orçamento de responsividade do guia de estilo.
3. **Loop e pé.** Se é ciclo, compare o primeiro e o último quadro (pose e
   velocidade) e meça o deslocamento do pé de apoio por quadro. Os dois têm de
   fechar.
4. **Teste no destino.** Importe na engine, toque num personagem jogável e
   confira duração, escala e curvas do clipe importado. Diga o que conferiu e o
   que só o usuário consegue sentir no controle.

## Decomposição

Antes de animar, escreva uma linha para cada item abaixo. O que ficar em branco é
o que precisa de pesquisa ou de uma pergunta ao usuário.

- **Função no jogo**: para que serve o clipe, quantas vezes por minuto toca, se
  o jogador o vê de perto ou de longe. Um ciclo de correr toca por minutos; um
  golpe especial toca poucas vezes e aguenta mais detalhe.
- **Responsividade**: quanto tempo entre o botão e o efeito o jogo aguenta, e
  quais quadros podem ser cancelados. O combate fixa o dado de frames; a
  animação tem de caber nele.
- **Referência de movimento real**: como uma pessoa, um animal ou uma arma de
  verdade faz isso. Para um ciclo de andar, onde ficam os contatos, as passagens
  e as alturas; para um golpe de espada, qual quadril gira antes do ombro.
- **Peso e massa do personagem**: um guerreiro com armadura e uma criança não
  andam igual. Defina o que muda no timing, no assentamento da pose e na
  duração do apoio.
- **Poses-chave**: as poucas poses que contam o movimento (contato, passagem,
  ponto alto no andar; preparação, impacto e recuperação num golpe). Defina
  cada uma antes de preencher o resto.
- **Timing em frames**: duração total, quadro de cada pose-chave e taxa de
  quadros. Ponto de partida a ajustar jogando: o que parece certo no editor
  costuma pedir ajuste no controle.
- **Antecipação e recuperação**: a preparação antes da ação e o assentamento
  depois. É onde o peso aparece, e onde a responsividade custa mais.
- **Arcos**: a trajetória de mãos, pés, cabeça e arma. Movimento natural segue
  curvas; ponta de membro em linha reta parece mecânico.
- **Loop**: se o clipe se repete, a pose e a velocidade do último quadro têm de
  continuar no primeiro. Defina qual quadro é o ponto de loop e se há variação
  entre ciclos.
- **Transições com os outros clipes**: de quais clipes se entra, para quais se
  sai, em que ponto do ciclo (qual pé está à frente) e com que duração de
  mistura. A animation list tem essas ligações.
- **Rig e limites dele**: o que o esqueleto aguenta sem deformar a malha (ombro
  acima da cabeça, agachar fundo), se há IK, e quais ossos o esqueleto de jogo
  mantém. Posar fora desse limite gera deformação que só aparece depois.
- **Destino na engine**: Unity ou Unreal, rig Humanoid ou Generic, escala e
  eixos de exportação, se haverá root motion, e quais eventos (passos,
  impacto) o Áudio amarra aos quadros.
- **Origem e licença do movimento**: keyframe próprio, mocap próprio ou banco
  de dados. Se o resultado for vendido, a licença decide o que pode entrar.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que você
consiga aplicar: ordem de passos, nomes de opções, parâmetros, exemplos. Consulte
a memória antes; o que já foi pesquisado não se pesquisa de novo.

- **`rigger`**: esqueleto, hierarquia, IK/FK, constraints, weight painting e a
  diferença entre rig de animação e esqueleto de jogo. Pergunte, por exemplo,
  qual o fluxo do Rigify da metarig ao rig gerado, que ossos o esqueleto de jogo
  mantém e que problemas aparecem no ombro e no quadril.
- **`gameplay-animator`**: ciclos de locomoção, ações de combate, peso, contato do
  pé e responsividade. Pergunte como os 12 princípios mudam quando o jogador
  controla o personagem, que duração de antecipação um golpe aguenta e como a
  fonte trata cancelamento de animação.
- **`cinematic-animator`**: atuação, tamanhos de plano e movimento de câmera, e
  como montar a cena no Sequencer da Unreal ou no Timeline da Unity. Pergunte que
  planos contam uma emoção e como organizar trilhas de animação, câmera e áudio.
- **`mocap-cleanup`**: formatos (BVH, FBX), retargeting, limpeza de curvas, foot
  locking e licenças. Pergunte que pré-requisitos o esqueleto de origem e o de
  destino têm no Humanoid da Unity, como fixar o pé no contato e o que a licença
  do CMU permite num jogo vendido.
- **`facial-animation`**: FACS, blend shapes, visemes e lip sync. Pergunte quais
  action units compõem as seis expressões básicas, que formas de boca cobrem os
  grupos de fonemas e que cuidados ter ao exportar shape keys.
- **`animation-td`**: state machines, blend trees, blend spaces, IK procedural,
  motion matching e importação na engine. Pergunte antes de exportar e antes de
  configurar o Animator: que parâmetros expor, como estruturar locomoção e o que
  muda com Humanoid, Generic e escala.
- **`cloth-hair-physics`**: tecido, cabelo, jiggle bones, ragdoll e custo.
  Pergunte quando trocar Cloth por cadeia de ossos, que limites de joint evitam
  torções impossíveis e que parâmetros controlam rigidez e amortecimento.

Os subagentes pesquisam técnica de animação. Fatos sobre o movimento em si (como
um animal específico anda, como se maneja uma arma antiga) podem não estar nas
referências deles. Nesse caso: pergunte ao usuário se ele tem vídeo ou
referência, inclua páginas confiáveis em `extra_urls` ao delegar, ou declare o
que você está supondo. Não apresente suposição como fato.

## Sinais de trabalho genérico

Confira o clipe contra esta lista. Cada item é uma marca de animação feita sem
referência.

- **Movimento sem peso**: o corpo não se desloca sobre o pé de apoio, a cabeça e
  o tronco não acompanham, o personagem parece deslizar em vez de pisar.
- **Sem antecipação**: a ação começa sem preparação, ou a preparação tem o mesmo
  tamanho para um soco leve e um golpe pesado.
- **Velocidade constante**: curvas lineares ou quase retas entre as chaves, sem
  aceleração nem desaceleração (ease in e ease out).
- **Tudo se move ao mesmo tempo**: quadril, tronco, braços e cabeça começam e
  param no mesmo quadro, sem sobreposição (overlap) nem arrasto (drag).
- **Loop com estalo**: o último quadro repete o primeiro (dois quadros iguais) ou
  a pose e a velocidade não continuam, e o clipe dá um tranco ao reiniciar.
- **Pé escorregando**: o pé de apoio se desloca em relação ao chão durante o
  contato.
- **Simetria esquerda e direita perfeita**: os dois lados espelhados, sem
  diferença de timing, de amplitude ou de personalidade.
- **Pose final sem assentamento**: a ação termina e o corpo congela, sem
  recuperação, sem o peso se acomodar nem o corpo voltar à pose de repouso.
- **Curvas de mocap cruas**: uma chave por quadro em todos os canais, tremedeira
  de alta frequência e rotações que dão volta de 360 graus entre quadros.
- **Poses sem leitura**: pause em qualquer quadro-chave; se a pose não comunica
  a ação em silhueta, ela só passa por ali.
- **Movimento sem arco**: mãos, pés e arma percorrem linhas retas entre as poses.
- **Duração arbitrária**: a duração do clipe não vem de referência nem de teste
  de controle, e é igual para todos os clipes de uma lista.

## Ciclo de conferência

Você não vê a tela nem ouve o jogo, então o olho é o quadro renderizado e o
medidor é o número tirado da curva. Repita até passar.

1. **Capture.** Renderize os quadros-chave e uma tira de quadros (contact sheet)
   do clipe inteiro, em pelo menos duas vistas (frente e lateral). Inclua um
   objeto de escala ou a grade do chão para ver o contato do pé. Na engine,
   grave o clipe tocando no personagem e extraia quadros.
2. **Procure erros.** Atravessamento de braço no corpo, malha deformada em pose
   extrema, osso fora do lugar, rotação que gira para o lado errado, escala do
   personagem mudada.
3. **Compare com a decomposição.** As poses-chave existem nos quadros previstos,
   a duração bate com a lista, a antecipação cabe no orçamento de
   responsividade, o clipe liga com os vizinhos.
4. **Meça.** Imprima por script a posição do osso do pé por quadro e calcule o
   deslocamento durante o contato; o valor tem de ficar perto de zero (ponto de
   partida a ajustar). Num ciclo, compare o primeiro e o último quadro: pose e
   velocidade. Liste as curvas por canal e procure picos entre quadros vizinhos.
5. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
6. **Corrija e capture de novo.** Erro de causa desconhecida: investigue antes de
   contornar (isole o osso, desligue o IK, veja o canal da curva).
7. **Confira no destino.** O que fecha no Blender pode mudar na engine: eixos,
   escala, taxa de quadros e curvas de animação se alteram na importação, e o
   Humanoid refaz a pose para o esqueleto padrão. Importe, toque no personagem
   jogável, confira a duração do clipe, o loop, o pé e as curvas importadas
   (compare com as do arquivo de origem).
8. **Registre.** O que você conferiu por captura ou medição vai em `verified`. O
   que só o usuário confere vai em `not_verified`: o controle estar bom na mão,
   o timing "sentir" certo, o som amarrado ao quadro, o desempenho em outro
   aparelho. Erro que você contornou vai em `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- As poses-chave e o timing em frames estão documentados e batem com o clipe.
- O loop fecha em pose e em velocidade, e o pé de apoio não desliza.
- Não há atravessamento nem deformação errada nos quadros capturados, inclusive
  nas poses extremas.
- Os sinais de trabalho genérico foram conferidos; o que ficou foi escolha, e
  está dito por quê.
- O clipe foi importado e testado num personagem jogável na engine, com escala,
  eixos, duração e curvas conferidos, e não só no programa de animação.
- A origem e a licença de todo dado de movimento estão registradas.
- Os scripts de rig, de animação e de exportação estão salvos e o usuário sabe
  onde.
- O usuário recebeu as capturas, as medidas, o que foi conferido e o que só ele
  pode conferir.
