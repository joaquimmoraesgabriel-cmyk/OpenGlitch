---
name: openglitch-arte-3d-metodo
description: Método de qualidade do agente Arte 3D. Como decompor um asset, o que pesquisar antes de modelar, os sinais de arte genérica e o ciclo de render e correção.
---

# Método de qualidade: Arte 3D

A skill diz o que você constrói. Este método diz como construir algo que
pareça ter sido feito por alguém que conhece o assunto: com referência real,
medidas plausíveis, construção coerente e marcas de uso. Sem ele, o resultado
sai da média do que você já viu, e é isso que dá a "cara de IA".

## Como usar este método

- **Tarefa avulsa ou asset pequeno**: siga só a "Versão curta".
- **Asset que o jogador vê de perto, personagem, cenário principal ou trabalho
  de projeto**: siga o método inteiro, na ordem das seções.
- A decomposição vem antes de abrir o Blender. A pesquisa vem antes de
  modelar. A conferência vem antes de dizer que está pronto.
- Mostre ao usuário a decomposição e o que você vai pesquisar antes de
  começar. Ele pode cortar o que não importa para ele.
- O método não substitui o brief: estilo, escopo e orçamento técnico vêm de lá.
  Em estilo low-poly ou estilizado, "detalhe" quer dizer forma, proporção e cor
  bem escolhidas, e não mais polígonos.

## Ambiente ao vivo

Antes de modelar, veja com o que você pode trabalhar. Se o seu cliente tem uma
ferramenta que executa código no Blender aberto e captura a tela dele (o
servidor MCP oficial do Blender, por exemplo), ou uma que controla o editor da
engine (o Unity CLI ou o servidor MCP da Unity), use-a. Diga ao usuário, em uma
linha, com o que você está trabalhando.

- **O script continua sendo a fonte.** Escreva o gerador em arquivo e execute-o
  dentro do Blender aberto, em vez de rodar o Blender em segundo plano. Assim o
  trabalho pode ser refeito com um comando e o usuário vê a cena mudar.
- **Olhe antes de supor.** Inspecione a cena real (objetos, unidades, coleções,
  materiais, modificadores) antes de criar ou alterar. Não presuma que a cena
  está vazia nem que as unidades são as que você espera.
- **Capture a cada etapa**, e não só no fim: depois do blockout, das formas
  médias, dos materiais e da luz. Erro visto cedo custa uma linha; visto no
  fim, custa a etapa.
- **Confira o objeto, não a intenção.** Depois de gerar, leia de volta as
  dimensões, a contagem de triângulos e os materiais do objeto que ficou na
  cena, e compare com a decomposição.
- **Consulte a documentação que a ferramenta traz** (a referência da API e o
  manual do Blender vêm com o servidor oficial) quando não tiver certeza de um
  operador ou de um parâmetro, em vez de tentar de memória.
- **Ajuste feito à mão na cena volta para o script** antes de você encerrar.
  O que só existe na cena aberta se perde quando o programa fecha.
- **Não destrua o que é do usuário.** A cena aberta pode ter trabalho dele:
  não apague, não renomeie e não salve por cima sem perguntar. Trabalhe numa
  coleção própria e diga qual.
- **Na engine**, importe, monte e capture pelo editor aberto, com a luz do
  jogo. É lá que se vê se a escala, os eixos e os materiais chegaram certos.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, quatro verificações bastam:

1. **Uma referência real.** Antes de modelar, descreva em cinco linhas como o
   objeto é de verdade: medidas aproximadas, de que é feito, como as partes se
   prendem umas às outras. Se você não sabe, delegue uma pesquisa curta.
2. **Escala.** Modele em metros e compare com uma pessoa de 1,75 m ou com uma
   porta de 2,10 m. Diga as medidas finais ao entregar.
3. **Três imperfeições.** Escolha três coisas que quebrem a perfeição: uma
   peça levemente torta, um desgaste onde a mão ou o pé encosta, uma variação
   de cor entre peças iguais.
4. **Render e correção.** Renderize de pelo menos três ângulos, olhe as
   imagens procurando erros (peças atravessadas, faces faltando, coisas
   flutuando, escala errada) e corrija antes de entregar. Diga o que conferiu
   e o que não deu para conferir.

## Decomposição

Antes de modelar, escreva uma linha para cada item abaixo. O que ficar em
branco é o que precisa de pesquisa ou de uma pergunta ao usuário.

- **Função no jogo**: para que serve, a que distância o jogador vê, se ele
  toca, entra ou só passa. Isso decide quanto detalhe vale a pena.
- **Referência do mundo real**: o que é esse objeto fora do jogo, de que época
  e lugar, quem o construiu e com que ferramentas.
- **Medidas e escala**: altura, largura e profundidade em metros; tamanho das
  partes em relação ao corpo humano (altura de maçaneta, de degrau, de assento).
- **Construção**: de que partes é feito e como elas se juntam. Uma parede de
  toras tem encaixes nos cantos; um telhado tem estrutura por baixo das telhas;
  uma arma tem peças que se movem. Modele as partes como partes.
- **Silhueta**: o contorno de longe. Deve ser reconhecível em preto sólido.
- **Hierarquia de formas**: as formas grandes, depois as médias, depois os
  detalhes, nessa ordem. Detalhe sobre forma grande errada não salva o modelo.
- **Materiais**: de que é feita cada parte e como cada material responde à luz
  (áspero, liso, fosco, metálico).
- **História de uso**: há quanto tempo existe, quem usa, onde gasta, onde
  acumula sujeira, o que foi consertado.
- **Entorno**: no que está apoiado e o que há em volta. Objeto sem contato com
  o chão e sem vizinhos parece recortado.
- **Luz**: de onde vem, de que cor, que clima deve criar.
- **Orçamento técnico**: meta de triângulos, tamanho de textura, número de
  materiais, LODs. Vem do brief; se não houver, proponha e registre.
- **Destino**: engine, versão, pipeline de render, formato de exportação, se
  tem animação. Isso muda decisões de eixo, escala e hierarquia desde o início.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que
você consiga aplicar: medidas, ordem de passos, valores, exemplos. Consulte a
memória antes; o que já foi pesquisado não se pesquisa de novo.

- **`concept-artist`**: silhueta, linguagem de formas, paleta e como montar um
  turnaround. Pergunte, por exemplo, que formas comunicam "aconchegante" ou
  "ameaçador" e como testar uma silhueta.
- **`environment-artist`**: construção modular, composição da cena, set
  dressing e como jogos reais economizam em cenário. Pergunte como dividir um
  cenário em peças que encaixam e que truques dão riqueza gastando pouco.
- **`props-hard-surface`**: bordas, bevels, normais e a lógica de objetos
  fabricados. Pergunte como fazer as bordas pegarem luz e onde um objeto real
  tem chanfro, folga e parafuso.
- **`character-artist`**: proporção, anatomia, topologia que dobra e o fluxo de
  blockout a low-poly. Pergunte onde vão os loops de uma articulação e que
  proporções o estilo pede.
- **`texture-material`**: valores PBR de cada material, desgaste, sujeira e
  variação. Pergunte os valores de roughness e de cor de um material e onde ele
  gasta primeiro.
- **`lighting-artist`**: esquema de luz para o clima pedido, luz em tempo real
  ou bakeada, pós-processamento. Pergunte como iluminar a mesma cena para dois
  climas e o que cada escolha custa.
- **`vfx-artist`**: partículas, timing do efeito e como ele se junta à
  animação e ao som. Pergunte as fases de um efeito e a duração de cada uma.
- **`technical-artist`**: exportação, eixos e escala entre o programa e a
  engine, shaders, LODs e orçamento. Pergunte antes de exportar: é onde os
  erros mais caros aparecem.

Os subagentes pesquisam técnica de arte. Fatos sobre o objeto em si (como se
constrói uma cabana de toras, que medidas tem uma espada) podem não estar nas
referências deles. Nesse caso: pergunte ao usuário se ele tem referência,
inclua páginas confiáveis em `extra_urls` ao delegar, ou declare o que você
está supondo. Não apresente suposição como fato.

## Sinais de trabalho genérico

Confira o modelo contra esta lista. Cada item é uma marca de arte feita sem
referência.

- **Simetria perfeita** em tudo que na vida real é montado à mão ou cresce.
- **Peças idênticas repetidas**: toras, tábuas, telhas, pedras e folhas todas
  do mesmo tamanho, na mesma rotação, com a mesma cor.
- **Tudo novo e limpo**: sem desgaste nas quinas, sem sujeira nos cantos, sem
  marca onde se pisa ou se pega.
- **Bordas vivas**: aresta de 90 graus sem bevel não pega luz e denuncia o
  modelo. Objeto real quase sempre tem quina arredondada.
- **Proporção genérica**: porta, janela, degrau e móvel sem relação com o
  corpo humano.
- **Construção impossível**: peças que se atravessam em vez de se encaixar,
  telhado sem apoio, coisas que não parariam em pé.
- **Detalhe uniforme**: a mesma densidade de detalhe em toda parte. O olho
  precisa de áreas de descanso e de pontos de interesse.
- **Material chapado**: um valor de cor e um de roughness por material, sem
  variação.
- **Cor saturada demais** e sem relação entre as partes; ausência de uma paleta.
- **Objeto flutuando** ou enterrado: sem contato com o chão, sem sombra de
  contato, sem transição entre o objeto e o terreno.
- **Luz plana**: tudo igualmente iluminado, sem direção e sem sombra.
- **Decoração sem motivo**: elemento que ninguém teria posto ali. Cada coisa
  na cena precisa de uma razão.

## Ciclo de conferência

Você não vê a tela, então o olho é o render. Repita até passar.

1. **Capture.** Renderize ou tire prints de frente, de trás, dos lados, de
   cima, em três quartos e de perto nas áreas importantes. Inclua uma imagem
   com uma referência de escala (uma figura humana ou um cubo de 1 m). Na
   engine, capture da altura dos olhos do jogador.
2. **Procure erros de construção**: peças que se atravessam, faces faltando ou
   invertidas, vãos, coisas flutuando, objetos fora do lugar ou deitados.
3. **Compare com a decomposição**: as medidas batem, a silhueta lê, os
   materiais estão nas partes certas.
4. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
5. **Confira o orçamento**: triângulos, materiais e texturas contra a meta. Se
   passou, diga em quanto e de onde vem o excesso.
6. **Corrija e capture de novo.** Erro de causa desconhecida: investigue antes
   de contornar (imprima as transformações, isole a peça).
7. **Confira no destino.** O que parece certo no Blender pode chegar errado na
   engine: escala, eixos, materiais e animação mudam na importação. Capture
   também dentro da engine, com a luz do jogo.
8. **Registre.** O que você conferiu por imagem vai em `verified`. O que não
   deu para conferir (jogar com teclado e mouse, desempenho em outro aparelho)
   vai em `not_verified`. Erro que você contornou vai em `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- As medidas estão em metros e foram comparadas com a escala humana.
- Não há erro de construção visível nas capturas.
- Os sinais de trabalho genérico foram conferidos; o que ficou foi escolha, e
  está dito por quê.
- O asset está dentro do orçamento, ou o excesso foi comunicado.
- Foi conferido no destino (engine), e não só no programa de modelagem.
- A geração pode ser repetida: o script ou o arquivo-fonte está salvo e o
  usuário sabe onde.
- O usuário recebeu as capturas, as medidas, o que foi conferido e o que não foi.
