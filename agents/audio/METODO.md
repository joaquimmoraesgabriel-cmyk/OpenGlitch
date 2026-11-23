---
name: openglitch-audio-metodo
description: Método de qualidade do agente Áudio. Como decompor o som de um jogo ou de um efeito, o que pesquisar antes de especificar, os sinais de áudio genérico e o ciclo de medição e correção.
---

# Método de qualidade: Áudio

A skill diz o que você entrega. Este método diz como entregar um som que pareça
pensado por quem conhece o ofício: com função clara, camadas, variação,
mixagem e licença conferida. Você não ouve, então sem método o resultado sai da
média do que você já leu sobre som, e o que falta é justamente o que o ouvido
do jogador percebe primeiro.

## Como usar este método

- **Tarefa avulsa ou som pequeno** (um efeito, um ajuste de volume, uma
  licença): siga só a "Versão curta".
- **Evento de combate, música do jogo, roteiro de voz, configuração de mixagem
  ou trabalho de projeto**: siga o método inteiro, na ordem das seções.
- A decomposição vem antes de especificar qualquer som. A pesquisa vem antes de
  escrever a especificação. A conferência vem antes de dizer que está pronto.
- Mostre ao usuário a decomposição e o que você vai pesquisar antes de
  começar. Ele pode cortar o que não importa para ele, como a voz.
- O método não substitui o brief: tom, escopo, plataformas e orçamento vêm de
  lá. Em jogo retrô, "detalhe" pode ser poucos sons bem escolhidos.

## Ambiente ao vivo

Você não ouve, mas pode medir e pode ver o áudio dentro do jogo. Veja o que
está disponível: uma ferramenta que controla o editor da engine aberto (o
Unity CLI ou o servidor MCP da Unity), ferramentas de linha de comando para
medir arquivos de som, e acesso à pasta do projeto. Diga ao usuário com o que
você está trabalhando.

- **Inspecione o projeto real**: que sistema de áudio ele usa (o nativo da
  engine ou um middleware), como estão os buses do mixer, que eventos já
  existem e como são nomeados.
- **Dispare os eventos no editor aberto** e leia o console: evento sem som,
  som sem evento e nome errado aparecem lá.
- **Leia de volta as configurações** do que você montou (volume do bus, curva
  de atenuação, formato de compressão, limite de vozes), em vez de confiar no
  que pretendia configurar.
- **Meça os arquivos** (duração, pico, loudness) e gere a imagem da forma de
  onda e do espectrograma para conferir cortes, emendas de loop e silêncio.
- **Meça o custo no jogo rodando**: memória e CPU do áudio com a cena cheia.
- **O que você monta fica em arquivo** no projeto, para poder ser refeito.
- **O que só o usuário confere**: como soa. Diga exatamente o que ele deve
  ouvir e em que momento do jogo.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, quatro verificações bastam:

1. **Função e evento.** Escreva em uma linha qual evento do jogo dispara o som e
   se ele informa, dá peso ou cria clima. Se não houver evento claro, pergunte
   ao usuário.
2. **Fonte e licença.** Anote de onde vem o som (criar, comprar, baixar) e,
   para cada arquivo, a licença, se permite uso comercial e se exige crédito.
   Som sem licença anotada não entra na lista.
3. **Variação e duração.** Para som repetido, especifique ao menos três
   variações e diga a duração e se tem cauda. Um arquivo só por evento
   frequente é o erro mais comum.
4. **Medição.** Meça duração, pico e loudness com `ffprobe` ou `ffmpeg`
   (filtro `ebur128`) e compare com o que você especificou. Diga o que mediu e
   o que só o usuário pode ouvir.

## Decomposição

Antes de especificar, escreva uma linha para cada item abaixo. O que ficar em
branco é o que precisa de pesquisa ou de uma pergunta ao usuário.

- **Evento que dispara**: qual ação ou estado do jogo toca o som (golpe leve,
  passo em pedra, abrir menu, entrar na área de combate) e em que frame da
  animação. Sem evento, não há som.
- **Função**: informar (acertou, errou, item coletado), dar peso (impacto do
  golpe pesado) ou criar clima (vento, sala vazia). Define o que priorizar.
- **Fonte real do som**: o que o objeto ou a ação é no mundo. Um golpe de
  espada contra gibão pede metal, tecido e couro; uma porta de carvalho pede
  madeira pesada e dobradiça. Isso guia o que gravar, comprar ou sintetizar.
- **Camadas**: as partes do som e a função de cada uma. Um tiro tem estalo,
  corpo, cauda e eco; um golpe tem ataque, impacto e reação do material.
- **Variações**: quantas versões, e o que muda entre elas (altura, camada
  trocada, ataque). Passo e golpe frequente pedem mais; evento raro pode ter
  uma. Cerca de cinco por passo é ponto de partida a ajustar.
- **Duração e cauda**: tempo total, ataque e fim. Cauda longa em evento rápido
  suja a mixagem; cauda curta em explosão a deixa fraca.
- **Espaço e distância**: som 2D ou 3D, curva de atenuação, reverb da área
  (caverna, corredor, campo aberto), se pode ser abafado por parede.
- **Prioridade na mixagem**: o que precisa ser ouvido sempre (fala, impacto) e o
  que cede (ambiente, passo longe). Defina o bus e o limite de vozes
  simultâneas.
- **Música e reação ao jogo**: estados (exploração, tensão, combate), o que
  muda entre eles, tipo de transição (no compasso, com stinger, com fade) e
  onde o silêncio é escolha.
- **Voz**: haverá fala, só esforços vocais ("hm!", "ah!") ou nada. Idioma,
  quem grava, contexto de cada fala e tamanho máximo.
- **Formato e orçamento de memória**: formato (WAV na produção, Vorbis ou
  similar na entrega), taxa de amostragem, mono ou estéreo, carregar na memória
  ou fazer streaming. Vem do brief e das plataformas; se não houver, proponha e
  registre.
- **Destino**: engine e versão, áudio nativo ou FMOD/Wwise, nome exato dos
  eventos que a Engenharia vai disparar.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que
você consiga aplicar: camadas, valores, passos, condições de licença. Consulte
a memória antes; o que já foi pesquisado não se pesquisa de novo.

- **`sound-designer`**: camadas, variações, ambientes em loop, sons de interface
  e bancos de som com licença. Pergunte, por exemplo, que camadas compõem um
  golpe pesado e uma explosão, como gerar variações de um passo e que
  condições de uso comercial cada banco gratuito impõe.
- **`composer`**: música interativa, teoria básica, transições, stingers e
  loops. Pergunte, por exemplo, como estruturar camadas de exploração, tensão e
  combate, onde cortar a transição e o que faz um loop de poucos compassos
  cansar.
- **`voice-over`**: roteiro com contexto, esforços vocais, gravação e dublagem
  em vários idiomas. Pergunte, por exemplo, que campos cada fala precisa para o
  ator gravar fora de ordem e como padronizar volume e nomes de arquivo.
- **`audio-programmer`**: eventos, som 3D, buses, prioridade, desempenho,
  áudio nativo, FMOD e Wwise. Pergunte, por exemplo, que parâmetros controlam
  atenuação e reverb por área, como trocar passo por tipo de chão e quais as
  condições de licença do middleware para o orçamento do projeto.

Os subagentes pesquisam técnica de áudio. Fatos sobre o jogo em si (qual é o
som de um material específico, que referência o usuário tem em mente) podem não
estar nas referências deles. Nesse caso: pergunte ao usuário se ele tem
referência, inclua páginas confiáveis em `extra_urls` ao delegar, ou declare o
que você está supondo. Não apresente suposição como fato. Licenças mudam: a
condição de cada som e de cada middleware vem da página da fonte, não da
memória.

## Sinais de trabalho genérico

Confira a especificação e os arquivos contra esta lista. Cada item é uma marca
de áudio feito sem referência.

- **Um único arquivo por evento repetido**: passo, golpe ou clique de interface
  sem variação. Conte os arquivos por evento na lista.
- **Som sem camadas**: o efeito é um arquivo só, sem separação de ataque,
  corpo e cauda, e por isso não dá para variar nem ajustar.
- **Tudo no mesmo volume**: os picos e a loudness dos eventos são quase
  iguais, sem hierarquia entre golpe leve, golpe pesado, ambiente e fala.
- **Sem atenuação por distância**: som 3D com curva padrão ou sem curva, tocando
  igual de perto e de longe.
- **Música em loop curto com emenda audível**: o fim não casa com o início em
  altura, andamento ou fase da cauda, e a repetição aparece em minutos.
- **Silêncio nunca usado**: música ou ambiente o tempo todo, sem pausa antes de
  um momento importante nem queda depois de um combate.
- **Som que não combina com o tamanho ou o material**: espada com som de
  graveto, porta de pedra com som de madeira leve, criatura grande com som agudo.
- **Evento sem som ou som sem evento**: ação do Design sem linha na lista, ou
  arquivo que nenhum evento usa.
- **Licença não conferida**: arquivo sem fonte, sem licença ou sem a condição de
  crédito anotada.
- **Voz sem contexto**: fala sem personagem, emoção, cena ou tamanho máximo, e
  volumes diferentes entre falas do mesmo personagem.

## Ciclo de conferência

Você não ouve nem vê a tela. Seus olhos são a medição e as imagens que os
arquivos geram. Repita até passar.

1. **Meça e renderize.** Para cada arquivo, meça duração, pico e loudness
   integrada (`ffprobe`, `ffmpeg -af ebur128` ou `astats`) e gere imagens da
   forma de onda e do espectrograma (`ffmpeg` com `showwavespic` e
   `showspectrumpic`). Na engine, registre os valores dos buses e das curvas
   de atenuação, e meça o uso de CPU e de memória do áudio.
2. **Procure erros técnicos**: corte seco no início ou no fim (forma de onda não
   começa nem termina em zero), pico acima de 0 dBFS, silêncio longo no começo
   do arquivo, canal vazio, taxa de amostragem fora do orçamento, arquivo
   mono onde devia ser estéreo ou o contrário, emenda de loop com salto na
   forma de onda.
3. **Compare com a decomposição**: a duração e a cauda batem, o número de
   variações é o especificado, o bus e a prioridade estão certos.
4. **Liste cada evento do jogo e seu som.** Cruze a lista de ações do Design e as
   cenas de Cinematics com a lista de eventos, e a lista de eventos com os
   arquivos. Evento sem som e arquivo sem evento são erros.
5. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
6. **Confira a licença de cada arquivo** na página da fonte: licença, uso
   comercial, crédito exigido. Registre a data em que conferiu.
7. **Corrija e meça de novo.** Erro de causa desconhecida: investigue antes de
   contornar (isole o arquivo, toque um evento por vez, confira o nome do
   evento no código).
8. **Confira no destino.** O que está certo no arquivo pode soar errado na
   engine: compressão, volume do bus, curva de atenuação, voz cortada pelo
   limite de vozes. Dispare cada evento no jogo e leia o log; confira que o
   nome do evento e os parâmetros combinam com o que a Engenharia chama.
9. **Registre.** O que você conferiu por medição e por lista vai em `verified`.
   O que não deu para conferir vai em `not_verified`: como o som soa, se o
   golpe pesado parece pesado, se a música emociona, se o loop incomoda, se a
   mixagem está clara com tudo tocando, se a voz tem a emoção certa. Só o
   usuário confere isso, ouvindo no jogo; peça a ele que ouça e diga
   exatamente o que escutar, por exemplo "jogue um minuto de combate sem
   música e diga se cada golpe se distingue". Erro que você contornou vai em
   `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- Todo evento do jogo tem uma linha na lista, e todo arquivo tem um evento.
- Os eventos frequentes têm variações, e o número está na lista.
- Duração, pico e loudness de cada arquivo foram medidos e estão dentro do
  esperado ou o desvio foi comunicado.
- Há hierarquia de volume e prioridade definida entre impacto, fala, música e
  ambiente.
- Os loops foram conferidos na forma de onda e sem salto na emenda.
- Todo som tem fonte, licença e condição de crédito conferidas na página da
  fonte.
- Os sinais de trabalho genérico foram conferidos; o que ficou é escolha dita.
- Foi conferido no destino (engine ou jogo), e não só nos arquivos.
- O usuário recebeu as medições, a lista de eventos, o que foi conferido e o
  que só ele pode ouvir, com instrução de como ouvir.
