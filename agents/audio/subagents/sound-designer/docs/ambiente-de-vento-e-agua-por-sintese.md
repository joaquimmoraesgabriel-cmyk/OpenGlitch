---
title: Ambiente de vento e água sintetizado por código
summary: Receita para gerar por código loops de vento, folhas, grama, riacho, cascata e lagoa, com as faixas de frequência usadas e como conferir sem ouvir.
tipo: original
fonte:
autor: openglitch (teste jardim-realista)
testado_em: Unity 6000.6.10f1, áudio nativo
---

Um ambiente de floresta sem gravações: cada som é ruído filtrado e modulado,
gerado por código e salvo como loop. Serve quando não há som pronto com
licença adequada ou quando o som precisa reagir ao jogo.

Origem e limite: esta receita saiu de um teste do OpenGlitch em que a pesquisa
nas referências não encontrou material sobre síntese. Os valores vieram do
conhecimento do agente e foram conferidos por medição (nível, espectro e
emenda do loop), não por ouvido. Trate como ponto de partida a ajustar ouvindo.

## Quando usar

- Ambiente contínuo (vento, vegetação, água), sem evento pontual.
- Projeto em que nenhum som de terceiros pode entrar, ou em que a licença dos
  bancos gratuitos não serve.
- Som que precisa mudar com o jogo: força do vento, distância da água,
  quantidade de árvores perto.

Não serve para sons com identidade marcada (voz, animais, impacto de objeto
específico): para esses, gravação ou banco de som.

## Camadas e faixas de frequência

Cada camada é um arquivo próprio, para poder variar volume, altura e filtro em
tempo real de forma independente.

- **Vento**: ruído grave contínuo, mais uma banda em 300 a 900 Hz cujo centro
  acompanha a rajada, um assobio estreito e baixo, e "ar" em 0,7 a 3,2 kHz.
  Sem a banda média o vento soa abafado.
- **Folhas**: ruído em banda por volta de 4 kHz multiplicado por um envelope de
  grãos curtos e aleatórios (6 a 38 ms), modulado por uma rajada lenta. A
  energia fica em 2 a 8 kHz.
- **Grama**: como as folhas, com a banda mais baixa (cerca de 2,3 kHz) e grãos
  mais longos (25 a 110 ms).
- **Riacho**: muitas bolhas curtas, cada uma um tom que sobe de altura e decai
  rápido, somadas a um chiado suave por volta de 1,7 kHz. O pico fica em 500 Hz
  a 1 kHz. Bolhas pequenas dão o agudo borbulhante; algumas maiores dão corpo.
- **Cascata**: ruído largo e forte, com graves, mais bolhas densas.
- **Lagoa**: bolhas raras e uma marola grave e lenta.

## Loop sem emenda

1. Gere o som com 1,5 s a mais do que a duração do loop.
2. Cruze o trecho extra do fim sobre o começo, com curvas de seno e cosseno
   (potência constante), e corte na duração final.
3. Use durações diferentes por camada (entre 24 e 40 s) e uma semente de
   aleatoriedade diferente para cada uma. Camadas com a mesma duração repetem
   juntas e a repetição aparece.

## Variação em tempo real

O loop sozinho soa como loop. O que esconde a repetição é a modulação no jogo:

- **Vento**: volume, altura e filtro passa-baixa seguem a força do vento e a
  rajada no ponto do ouvinte.
- **Folhas**: duas fontes, uma para cada lado, com a rajada amostrada em pontos
  diferentes; o volume segue a quantidade de árvores perto.
- **Grama**: volume pelo tipo de chão sob o ouvinte.
- **Água**: fonte 3D posicionada no ponto do riacho mais próximo do ouvinte, com
  atenuação logarítmica. A cascata é uma fonte fixa com alcance maior.

Vento, folhas e grama ficam em 2D, porque o ouvinte está dentro deles. Água
fica em 3D, porque indica um lugar e ajuda o jogador a se orientar.

## Formato

- Gerado como WAV mono, 44,1 kHz, 16 bits.
- Na engine, comprimido (Vorbis em qualidade média) e descomprimido ao carregar,
  porque são poucos loops pequenos.
- Volume de partida moderado por camada, entre -12 e -6 dB, para não cansar.

## Como conferir sem ouvir

- **Emenda**: o salto entre a última e a primeira amostra deve ser menor do que
  os saltos comuns dentro do próprio som.
- **Nível**: meça o volume médio de cada camada e compare entre elas. No teste
  o vento ficou em torno de -19 dBFS.
- **Espectro**: confira se a energia está na faixa esperada de cada camada. Um
  vento sem energia perto de 1 kHz está abafado; um riacho sem pico entre 500 Hz
  e 1 kHz não borbulha.
- **No jogo**: mova o ouvinte por lugares diferentes e leia os volumes de cada
  fonte; eles precisam mudar com o lugar.

O que só uma pessoa confere: se soa natural, se cansa depois de alguns
minutos, se o equilíbrio entre as camadas está bom. Peça isso ao usuário.

## Erros comuns

- Vento só com graves: soa como ronco. Falta a banda média.
- Riacho abafado: bolhas grandes demais ou poucas bolhas pequenas.
- Todas as camadas com a mesma duração: a repetição fica audível.
- Loop cortado sem cruzamento: clique na emenda.
- Água em 2D: o jogador perde a noção de onde ela está.
- Volume alto demais em som contínuo: cansa em minutos.
