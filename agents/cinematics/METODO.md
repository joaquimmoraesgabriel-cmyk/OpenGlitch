---
name: openglitch-cinematics-metodo
description: Método de qualidade do agente Cinematics. Como decompor uma cena, o que pesquisar antes de decupar, os sinais de cinemática genérica e o ciclo de captura, cronometragem e correção.
---

# Método de qualidade: Cinematics

A skill diz o que você entrega. Este método diz como entregar uma cena que
pareça dirigida por alguém que conhece cinema: cada plano com motivo, câmera
que serve à emoção, cortes que seguem o conteúdo e luz que guia o olhar. Sem
ele, a cena sai da média das cutscenes que você já viu: câmera a meia
distância, cortes em ritmo igual e personagens parados explicando a história.

## Como usar este método

- **Tarefa avulsa ou cena curta**: siga só a "Versão curta".
- **Cena de história, abertura, clímax ou conjunto de cenas de um projeto**:
  siga o método inteiro, na ordem das seções.
- A decomposição vem antes de abrir a engine. A pesquisa vem antes de
  decupar. A conferência vem antes de dizer que está pronto.
- Mostre ao usuário a decomposição, o storyboard em texto e o que você vai
  pesquisar antes de montar a sequência. Ele pode cortar planos ou cenas.
- O método não substitui o brief: o roteiro, o estilo de imagem e a decisão
  entre tempo real e pré-renderizado vêm de lá. Em equipe pequena, a conta
  mais barata é poucas cenas, curtas e na engine. Se a cena não muda nada,
  proponha cortá-la antes de decupar.

## Ambiente ao vivo

Câmera, luz e ritmo só se julgam vendo. Antes de montar, veja com o que você
pode trabalhar: uma ferramenta que controla o editor da engine aberto (o Unity
CLI ou o servidor MCP da Unity) ou uma que executa código e captura a tela no
Blender aberto. Diga ao usuário, em uma linha, com o que você está trabalhando.

- **A sequência fica em arquivo.** Monte a cena por script ou por asset de
  sequência salvo no projeto, e não só mexendo no editor aberto, para poder
  refazer.
- **Inspecione a cena real** antes de posicionar câmeras: onde estão os
  personagens, a escala, a direção da luz principal, o que já existe na linha
  do tempo.
- **Capture pela câmera do plano**, e não pela câmera livre do editor. Um
  quadro por plano no início, no meio e no fim, na proporção de tela final.
- **Monte a tira de planos** com as capturas em ordem e confira a continuidade
  entre vizinhos: eixo de ação, direção do olhar, posição dos personagens.
- **Meça o tempo de cada plano** lendo a linha do tempo, em vez de confiar na
  duração que você planejou.
- **Confira luz e pós-processamento na captura**, com os efeitos ligados como
  no jogo. O que parece certo sem pós-processamento muda com ele.
- **Ajuste feito à mão volta para o arquivo da sequência** antes de encerrar.
- **Não destrua o que é do usuário.** Não mova nem apague câmeras, luzes e
  objetos que não são da sua cena sem perguntar.
- **O que só o usuário confere**: assistir a sequência em movimento e dizer se
  o ritmo e a emoção funcionam. Peça isso de forma específica.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, cinco verificações bastam:

1. **Uma frase de propósito.** Escreva o que muda na cena (informação, relação
   ou situação) e o que o espectador deve sentir ao final. Sem mudança, não há
   cena.
2. **Motivo por plano.** Faça uma tabela com um plano por linha: tamanho,
   ângulo, lente, movimento, duração e a razão de cada escolha. Dois planos
   com a mesma razão: um sai.
3. **Variação.** Confira a tabela: os planos não podem ter todos a mesma
   distância e a mesma altura, e as durações não podem ser todas iguais.
4. **Continuidade.** Marque o eixo de ação e o lado de cada personagem no
   quadro. Cruzar o eixo só com intenção declarada.
5. **Quadro e cronometragem.** Capture um quadro de cada plano, junte numa tira
   na ordem, meça a duração real de cada um e compare com a tabela. Diga o que
   conferiu e o que só dá para conferir assistindo.

## Decomposição

Antes de montar, escreva uma linha para cada item abaixo. O que ficar em
branco é o que precisa de pesquisa ou de uma pergunta ao usuário.

- **Propósito dramático**: o que a cena muda e por que ela existe. Exemplo:
  "o jogador descobre que o aliado mentiu", e não "os dois conversam".
- **Sentir e saber**: o que o espectador deve sentir e o que deve saber ao
  final. São duas respostas: o saber é informação, o sentir é emoção.
- **Batidas da cena**: os momentos em que algo muda, na ordem. Exemplo:
  chegada, pergunta, silêncio, revelação, reação, saída.
- **Shot list**: um plano por linha, com número, duração em segundos, quem
  aparece e o que acontece. Os planos nascem das batidas, não o contrário.
- **Enquadramento e lente de cada plano**: tamanho do plano, ângulo, altura da
  câmera e distância focal. Exemplo: close a 85 mm no momento da revelação,
  plano geral a 24 mm na chegada. Os valores são ponto de partida a ajustar.
- **Movimento de câmera e motivo**: fixa, dolly, pan, tracking ou na mão, e o
  que o movimento revela ou enfatiza. Sem motivo, a câmera fica parada.
- **Bloqueio dos personagens**: onde cada um está no quadro, para onde olha e
  quando se move. Distância entre eles diz a relação deles.
- **Continuidade e eixo de ação**: de que lado do eixo cada câmera fica,
  direção do olhar, posição de props e figurino entre planos vizinhos.
- **Ritmo de corte**: onde segurar e onde cortar rápido, e o tipo de cada
  corte (na ação, no olhar, match cut, J-cut, L-cut). O ritmo segue a emoção.
- **Luz e cor**: luz principal, preenchimento e contraluz por plano, e o
  grading que carrega o clima. Deve ser coerente dentro da cena.
- **Som**: onde entram diálogo, música e efeitos e o que o áudio antecipa ou
  adia no corte. Peça o tempo de cada plano ao Áudio.
- **Tempo real ou pré-renderizado**: vem do brief. Muda o custo de cada
  mudança, a ferramenta (Sequencer, Timeline, compositor) e o que você pode
  prometer ao usuário.
- **Entrada e saída do gameplay**: de onde o jogador vem, quem controla durante
  a cena, se pode pular, e para onde a câmera volta.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que
você consiga aplicar: critérios, passos, valores, exemplos. Consulte a memória
antes; o que já foi pesquisado não se pesquisa de novo.

- **`cinematic-director`**: breakdown do roteiro, objetivo emocional,
  storyboard, animatic e quando não fazer cutscene. Pergunte, por exemplo, como
  escrever o objetivo emocional de uma cena em uma frase e como testar se o
  plano tem razão de existir.
- **`layout-camera`**: tamanhos de plano, ângulos, lentes, movimentos, regra
  dos 180°, eixo do olhar e câmeras virtuais. Pergunte, por exemplo, que lente e
  que tamanho de plano servem a um close de revelação e a um plano de
  estabelecimento, e como filmar uma conversa sem quebrar o eixo.
- **`scene-animator`**: atuação plano a plano, sincronia com a dublagem e
  montagem no Sequencer ou no Timeline. Pergunte, por exemplo, quais faixas uma
  cena precisa e como construir a pausa e o olhar de um personagem num close.
- **`editor`**: montagem, tipos de corte, ritmo e regra dos seis de Murch.
  Pergunte, por exemplo, quando usar corte no olhar ou L-cut e como decidir se
  um plano segura mais um segundo ou corta agora.
- **`lighting-comp`**: luz principal, preenchimento e contraluz, grading,
  pós-processamento e composição. Pergunte, por exemplo, como montar a luz de um
  close tenso e que ajustes de pós-processamento dão um clima quente ou frio.

Os subagentes pesquisam técnica de cinema e de cutscene. Fatos sobre o jogo ou
a cena em si (o que o roteiro pede, qual o estilo de imagem, que lente a
engine do usuário oferece) podem não estar nas referências deles. Nesse caso:
pergunte ao usuário se ele tem referência, inclua páginas confiáveis em
`extra_urls` ao delegar, ou declare o que você está supondo. Não apresente
suposição como fato.

## Sinais de trabalho genérico

Confira a cena contra esta lista. Cada item é uma marca de cinemática feita sem
referência.

- **Câmera que se move sem motivo**: dolly ou pan em plano em que nada é
  revelado nem enfatizado. Pergunte, para cada movimento, o que ele mostra.
- **Mesma distância e mesma altura**: todos os planos no mesmo tamanho e na
  altura dos olhos, sem um geral nem um close na tabela.
- **Cortes em intervalo regular**: durações quase iguais, como se o corte
  viesse de um metrônomo e não da cena.
- **Personagens parados no centro do quadro**: bloqueio sem movimento, sem
  distância que diga algo, sem relação com a regra dos terços.
- **Quebra de eixo sem intenção**: dois planos vizinhos em que o personagem
  troca de lado do quadro ou o olhar deixa de bater.
- **Luz plana**: o plano tem luz uniforme, sem luz principal, sem sombra e sem
  separação do fundo.
- **Cena que explica em diálogo o que podia mostrar**: fala que descreve o que
  a imagem poderia dar num plano.
- **Duração maior que o conteúdo**: planos que continuam depois de a
  informação ou a emoção já ter chegado.
- **Grading sem relação com a emoção**: o mesmo ajuste de cor em todas as
  cenas, ou um clima que contradiz o propósito da cena.
- **Entrada e saída abruptas**: a cena começa sem situar o jogador e termina
  sem devolver o controle com clareza.
- **Animação onde ninguém vê**: trabalho em corpo ou pés que a câmera não
  mostra, e atuação sem intenção legível onde a câmera mostra.

## Ciclo de conferência

Você não vê a tela nem ouve. O olho é o quadro capturado, o relógio é a medida
de duração e o ouvido é o usuário. Repita até passar.

1. **Storyboard em texto antes de montar.** Escreva cada plano quadro a quadro:
   o que está no enquadramento, onde estão os personagens, para onde a câmera
   vai. Mostre ao usuário e só então monte a sequência.
2. **Capture um quadro de cada plano.** Use a captura da engine ou do render, no
   primeiro quadro, no meio e no último de cada plano quando houver movimento.
3. **Monte uma tira com os planos em ordem** (uma imagem com os quadros
   lado a lado, via script) e olhe a tira inteira: variação de tamanho e de
   altura, posição dos personagens, lado do quadro.
4. **Procure erros de construção**: personagem atravessando cenário, câmera
   dentro de um objeto, plano sem personagem por erro de bloqueio, props em
   lugares diferentes entre planos.
5. **Cronometre cada plano.** Leia a duração da sequência (frames sobre a taxa
   de quadros) e compare com a shot list. Calcule a duração de cada corte e
   confira se o ritmo segue a emoção, e não um intervalo fixo.
6. **Confira a continuidade entre planos vizinhos**: lado do eixo, direção do
   olhar, posição e pose de props, luz e grading.
7. **Compare com a decomposição**: o propósito aparece, as batidas estão todas,
   cada plano tem motivo escrito, o som tem um lugar para cada tempo.
8. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
9. **Corrija e capture de novo.** Erro de causa desconhecida: investigue antes
   de contornar (imprima as transformações da câmera, isole o plano).
10. **Assista à sequência na engine.** Rode a sequência no Sequencer ou na
    Timeline com câmera, animação e áudio ligados, e confira que as faixas
    tocam de ponta a ponta. Teste a entrada e a saída do gameplay e o pular.
11. **Registre.** O que você conferiu por quadro, tira, relógio e execução vai
    em `verified`. O que só o usuário confere (sentir o ritmo, ouvir a mistura,
    ver a cena em movimento em tempo real, desempenho em outro aparelho) vai em
    `not_verified`. Erro que você contornou vai em `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- Cada cena tem um propósito escrito em uma frase e uma mudança identificável.
- A shot list e o storyboard em texto batem com o que está na sequência.
- Cada plano tem motivo para tamanho, lente e movimento, e a tira mostra
  variação de distância e de altura.
- Não há quebra de eixo sem intenção nem salto de continuidade entre planos
  vizinhos.
- As durações foram cronometradas e batem com a shot list, ou a diferença
  está dita.
- Os sinais de trabalho genérico foram conferidos; o que ficou foi escolha, e
  está dito por quê.
- A sequência foi assistida na engine, e a entrada e a saída do gameplay
  foram testadas.
- Script, arquivo da sequência e shot list estão salvos, e o usuário sabe onde.
- O usuário recebeu quadros, tira, durações, o que foi conferido e o que só
  ele pode conferir.
