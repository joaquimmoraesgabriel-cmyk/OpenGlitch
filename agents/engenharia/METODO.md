---
name: openglitch-engenharia-metodo
description: Método de qualidade do agente Engenharia. Como decompor um sistema, o que pesquisar antes de programar, os sinais de código genérico e o ciclo de compilar, testar, medir e corrigir.
---

# Método de qualidade: Engenharia

A skill diz o que você constrói. Este método diz como construir código que
funcione de verdade no jogo: pensado para o caso de uso, ajustável pelo design,
testado e medido. Sem ele, o resultado sai da média dos tutoriais, compila e
quebra na primeira situação que ninguém previu. É isso que dá a "cara de IA".

## Como usar este método

- **Tarefa avulsa ou correção pequena**: siga só a "Versão curta".
- **Sistema novo, controle, câmera, combate, IA, save, ferramenta de editor ou
  trabalho de projeto**: siga o método inteiro, na ordem das seções.
- A decomposição vem antes de abrir a engine ou criar o primeiro arquivo. A
  pesquisa vem antes de escrever. A conferência vem antes de dizer que está
  pronto.
- Mostre ao usuário a decomposição e o que você vai pesquisar antes de
  começar. Ele pode cortar o que não importa para ele.
- O método não substitui o brief: engine, plataforma, escopo e meta de FPS
  vêm de lá. Protótipo do Design pode ser simples, mas é executado.

## Ambiente ao vivo

Antes de programar, veja com o que você pode trabalhar. Se o seu cliente tem
uma ferramenta que controla o editor da engine aberto (o Unity CLI ou o
servidor MCP da Unity, por exemplo), use-a para compilar, ler o console, rodar
código e capturar a tela. Diga ao usuário, em uma linha, com o que você está
trabalhando.

- **Inspecione o projeto real** antes de escrever: versão da engine, pipeline
  de render, sistema de input, pacotes instalados, cenas e convenções de pasta.
  Uma API que você conhece pode ter mudado ou ficado obsoleta nesta versão;
  quando a versão é nova para você, delegue uma pesquisa curta em vez de
  confiar na memória.
- **Compile e leia o console depois de cada mudança**, e não só no fim. Erro e
  aviso novo se resolvem na hora.
- **Execute de verdade.** Rode o sistema no editor aberto, em modo de jogo ou
  por um teste, e leia o resultado. Código que compila e nunca rodou não está
  conferido.
- **Capture a tela do jogo** para conferir o que o código produz na cena, e
  compare dois quadros quando o que importa é movimento.
- **Meça com as ferramentas da engine** (tempo de quadro, triângulos, chamadas
  de desenho) antes e depois de otimizar, desligando uma coisa de cada vez
  para achar o que pesa.
- **Antes de cada rodada de medidas, confira as condições**: a resolução real
  da tela de jogo (leia o tamanho em pixels da câmera), o nível de qualidade
  ativo, e se a entrada do usuário está travada. Meça a base e a mudança na
  mesma sessão, nos mesmos pontos, e grave junto de cada número a resolução e
  o nível. Grave no projeto a posição e a direção de cada ponto de medida. Uma
  base que não bate com a rodada anterior é erro de medição, não custo novo.
- **O número final vem do executável**, não do editor. Gere o build, rode a
  mesma medição nele e leia o log: há erros que só aparecem lá.
- **O que você monta por ferramenta fica em arquivo.** Cena, prefab e
  configuração criados pelo editor precisam de um script de montagem ou de um
  asset salvo no projeto, para poderem ser refeitos.
- **Não destrua o que é do usuário.** Não apague assets, não troque
  configurações do projeto e não instale pacotes sem dizer o que e por quê; o
  que mudar nas configurações, liste ao entregar.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, cinco verificações bastam:

1. **Entrada, saída e caso de borda.** Antes de escrever, descreva em cinco
   linhas o que entra, o que sai e três situações extremas (valor zero,
   referência nula, duas chamadas no mesmo frame). Se não sabe como a API da
   engine se comporta nelas, delegue uma pesquisa curta.
2. **Valores fora do código.** Todo número que o design pode querer mudar
   (velocidade, dano, tempo) vai para um campo exposto ou arquivo de dados,
   com nome e unidade. Nenhum número solto na lógica.
3. **Compilar e executar.** Compile sem erros e sem avisos novos, e rode o
   código ao menos uma vez: em teste, em modo batch ou na cena.
4. **Um teste que falha.** Rode um teste da regra principal e confirme que ele
   falha quando você quebra a regra de propósito.
5. **Registro.** Diga o que rodou e o resultado, e o que não deu para conferir.

## Decomposição

Antes de programar um sistema, escreva uma linha para cada item abaixo. O que
ficar em branco é o que precisa de pesquisa ou de uma pergunta ao usuário.

- **O que o jogador faz com ele**: a ação em palavras do jogo. "Esquivar" é o
  jogador apertar um botão perto de um golpe e sobreviver por pouco.
- **Entradas e saídas**: o que recebe (input, eventos, dados) e o que devolve
  (movimento, dano, evento, save), com nome, tipo e unidade.
- **Estados e transições**: os estados possíveis e o que leva de um a outro.
  No chão, no ar, esquivando, atordoado, morto; diga quais transições são
  proibidas, como pular enquanto está morto.
- **Dados e donos**: quais dados o sistema usa, onde ficam (ScriptableObject,
  arquivo, componente) e quem escreve neles. Cada dado tem um dono só.
- **Dependências com outros sistemas**: com quem ele conversa e por qual
  canal (evento, interface, referência). Combate depende de vida e animação.
- **Casos de borda**: valor nulo, objeto destruído no meio da ação, dois
  eventos no mesmo frame, FPS muito baixo, save de versão antiga, inventário
  cheio, alvo que sai do alcance.
- **Parâmetros do design**: os números que o designer vai ajustar, com valor
  inicial (ponto de partida a ajustar), faixa, unidade e onde mudar sem tocar
  no código.
- **Meta de desempenho**: custo permitido por frame, por instância e de
  memória, derivado da meta de FPS do brief (ou proposto e registrado).
- **Plataforma e engine**: PC, console, celular ou web; versão da engine;
  pipeline de render.
- **Como será testado**: o que tem teste automático, o que se valida jogando,
  e que cena e conteúdo real entram na medição.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que
você consiga aplicar: nomes de API, passos, valores de partida, exemplos de
código. Consulte a memória antes; o que já foi pesquisado não se pesquisa de
novo.

- **`gameplay-programmer`**: game loop, fixed update, componentes, eventos,
  state machines, física e feeling de controle. Pergunte como separar a
  física em passo fixo da renderização, que valores de partida usar para coyote
  time e input buffering e quando uma state machine vale mais que flags.
- **`engine-graphics`**: renderização, shaders, importação, LODs, culling e
  profiling. Pergunte como importar o modelo sem erro de escala e de rig, o
  que cada contador do profiler indica e que gargalo um sintoma de queda de
  FPS costuma esconder.
- **`ai-programmer`**: pathfinding, state machines, behavior trees, utility AI,
  percepção e grupo. Pergunte qual técnica serve ao comportamento pedido e o
  custo dela, como tratar interrupção de um nó e como vários inimigos dividem
  posições ao redor do jogador.
- **`tools-programmer`**: editor scripting, ScriptableObject, validação de
  assets, debug no jogo e Python do Blender. Pergunte a API para varrer assets
  e desenhar uma janela, como expor parâmetros com validação para o designer e
  como rodar a ferramenta em modo batch.
- **`network-programmer`**: servidor autoritativo, predição, reconciliação,
  interpolação e lag. Chame só se o brief pede multiplayer. Pergunte o fluxo de
  mensagens e como simular lag e perda de pacote nos testes.
- **`build-devops`**: Git, LFS, CI/CD, GameCI, testes automáticos e
  publicação. Pergunte o `.gitattributes` e o `.gitignore` do projeto, os
  passos de um workflow que compila e roda testes a cada push e o que cada
  loja exige.

Os subagentes pesquisam técnica geral. Fatos do projeto do usuário (versão
exata da engine, plugin que ele usa, limite do aparelho dele, API que mudou
numa versão recente) podem não estar nas referências. Nesse caso: pergunte ao
usuário, inclua a documentação oficial em `extra_urls` ao delegar, ou declare o
que você está supondo. Não apresente suposição como fato.

## Sinais de trabalho genérico

Confira o código contra esta lista. Cada item é uma marca de código escrito sem
referência e sem uso real.

- **Arquitetura copiada sem necessidade**: Singleton, Service Locator, injeção
  de dependência ou ECS completo num jogo pequeno, só porque apareceu num
  tutorial. Cada padrão precisa responder a um problema que existe neste
  projeto.
- **Valores mágicos**: números soltos no código (`speed = 7.5f`,
  `if (hp < 30)`) em vez de campos expostos ou dados que o design ajusta.
  Procure literais numéricos na lógica de gameplay.
- **Tudo num só script**: uma classe que lê input, move, ataca, toca som e
  atualiza a interface. Arquivo longo com várias responsabilidades.
- **Sem tratamento de casos de borda**: nenhuma checagem de nulo, de objeto
  destruído, de divisão por zero, de lista vazia ou de chamada duplicada no
  mesmo frame.
- **Otimização antes de medir**: object pool, cache ou código obscuro sem
  número de profiler, ou sem o antes e o depois.
- **Acoplamento direto**: sistema que busca outro por `Find`, por nome de
  objeto ou por referência cruzada, de modo que apagar um quebra os outros.
- **Código que compila e nunca foi executado**: sem log, teste ou cena rodada.
  Compilar prova só a sintaxe.
- **Sem teste**: dano, inventário, save ou máquina de estados sem teste.
- **Dependência do FPS**: movimento ou tempo por frame em vez de por tempo,
  física no update comum, comportamento diferente a 30 e a 144 FPS.

## Ciclo de conferência

Você não vê a tela nem sente o controle, então o olho é o log, o teste e o
profiler. Repita até passar.

1. **Capture.** Compile e guarde a saída. Rode a engine em modo batch quando
   houver (por exemplo, `-batchmode -nographics` na Unity) para executar os
   testes e a cena sem janela. Guarde o log e, se houver tela, capturas dos
   painéis de debug.
2. **Procure erros.** Leia o log do compilador e o console da engine: erros,
   exceções, avisos novos, referências nulas, assets faltando. Compare a
   contagem de avisos com a de antes da sua mudança.
3. **Compare com a decomposição**: estados e transições existem e as proibidas
   realmente não acontecem; as entradas e saídas batem com o que foi escrito;
   cada parâmetro do design está exposto com unidade.
4. **Rode os testes automáticos** (edit mode e play mode, ou o equivalente) e
   escreva os que faltam para os casos de borda listados. Para cada caso de
   borda, force a situação e confira o resultado, não apenas a ausência de
   exceção.
5. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
6. **Meça.** Abra o profiler com a cena real, o personagem final e várias
   cópias, e registre tempo de frame, CPU, GPU, draw calls e memória. Compare
   com a meta da decomposição. Se for otimizar, meça antes e depois com a mesma
   cena e diga o ganho. Medida em cena vazia não vale.
7. **Confira com o designer em mente.** Mude cada parâmetro exposto para um
   valor bem diferente, sem editar código, e confirme que o comportamento muda
   e que valor inválido é rejeitado ou limitado.
8. **Corrija e repita.** Erro de causa desconhecida: investigue antes de
   contornar (log com contexto, teste que reproduz).
9. **Confira no destino.** Rode o build da plataforma-alvo, feito do
   repositório limpo, e não só o editor. O que funciona no editor pode falhar
   no build: código removido por stripping, caminho de arquivo, inicialização.
10. **Registre.** O que você rodou e mediu vai em `verified`, com o número ou o
    log. O que não deu para conferir vai em `not_verified`: sensação de
    controle e câmera, dificuldade da IA, desempenho em outro aparelho, rede
    real. Só o usuário confere isso jogando. Erro contornado vai em
    `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- O projeto compila sem erros e sem avisos novos.
- Os testes passam e cobrem a regra principal e os casos de borda listados.
- O código foi executado: o log ou a cena rodada mostra o sistema funcionando,
  sem exceção.
- Não há valor mágico na lógica de gameplay; o designer ajusta os parâmetros
  sem mexer no código, e isso foi conferido.
- Os sinais de trabalho genérico foram conferidos; o que ficou foi escolha, e
  está dito por quê.
- O desempenho foi medido com conteúdo real e está na meta, ou o excesso foi
  comunicado com a causa.
- Foi conferido no destino (build), e não só no editor.
- O build sai do repositório limpo e o usuário sabe onde ficam arquivos e
  parâmetros.
- O usuário recebeu o que foi feito, o que foi medido e o que só ele consegue
  conferir jogando.
