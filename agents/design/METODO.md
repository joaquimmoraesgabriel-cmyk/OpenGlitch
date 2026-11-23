---
name: openglitch-design-metodo
description: Método de qualidade do agente Design. Como decompor um jogo ou sistema, o que pesquisar antes de decidir, os sinais de design genérico e o ciclo de teste e correção.
---

# Método de qualidade: Design

A skill diz o que você escreve. Este método diz como escrever decisões de
design que tenham motivo, número e teste por trás: cada mecânica ligada a um
pilar, cada valor vindo de uma planilha, cada regra provada em partida. Sem
ele, o brief sai da média dos jogos que você já viu: uma lista de features do
gênero, com números redondos, e é isso que dá a "cara de IA". Como todos os
outros agentes leem o seu brief, o erro daqui se multiplica em todas as áreas.

## Como usar este método

- **Tarefa avulsa ou sistema pequeno** (uma mecânica, uma tabela de dano, um
  diálogo curto): siga só a "Versão curta".
- **Brief de jogo novo, core loop, combate, fases, narrativa ou interface de
  projeto**: siga o método inteiro, na ordem das seções.
- A decomposição vem antes de escrever o brief ou o GDD. A pesquisa vem antes
  de fixar regras e números. A conferência vem antes de publicar.
- Mostre ao usuário a decomposição e o que você vai pesquisar antes de
  começar. Ele pode cortar o que não importa e responder o que só ele sabe.
- Na **entrada rápida de projeto existente** o método não se aplica. Lá você
  lê o projeto, registra o que encontrou e marca a origem de cada informação;
  não decompõe, não pesquisa e não propõe mudar decisões já tomadas.

## Ambiente ao vivo

O design trabalha quase todo em documentos, mas a regra só se prova no jogo.
Veja o que está disponível: se o seu cliente consegue ler a pasta do projeto,
controlar o editor da engine aberto ou rodar um protótipo, use isso em vez de
decidir só no papel. Diga ao usuário com o que você está trabalhando.

- **Leia o projeto real** quando ele existir: cenas, scripts e dados mostram o
  jogo que foi feito, que pode ser diferente do que está descrito.
- **Leia os valores no lugar onde vivem.** Dano, vida, velocidade e tempos
  estão em arquivos de dados ou em campos da engine; balanceie a partir deles,
  e não de números lembrados.
- **Peça capturas e medições** ao agente que constrói, ou tire você mesmo
  quando tiver a ferramenta: a tela do jogo, a duração de uma ação, o tempo de
  uma fase.
- **Rode a simulação que der.** Uma planilha ou um script curto que simule a
  economia ou um combate responde mais do que uma discussão.
- **Você não altera o jogo.** Mesmo com acesso ao editor, mudar cena, código
  ou asset é dos outros agentes; você lê, mede e especifica.
- **O que só o usuário confere**: se é divertido. Peça que ele jogue um trecho
  específico e diga o que observar.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, quatro verificações bastam:

1. **Um pilar ou um objetivo.** Escreva em uma frase o que a mecânica ou o
   sistema precisa provocar no jogador. Se não ligar a nada que o usuário
   disse querer, pergunte a ele antes de detalhar.
2. **Regra, custo e recompensa.** Para cada mecânica, escreva o que o jogador
   faz, o que isso custa (tempo, recurso, risco) e o que ele ganha. Mecânica
   sem custo não tem decisão.
3. **Números numa planilha.** Todo valor (dano, vida, preço, tempo) entra em um
   CSV ou planilha com a fórmula que o gera. Marque cada valor como ponto de
   partida a ajustar no teste, não como resposta.
4. **Uma partida simulada.** Jogue a regra no texto: cinco a dez turnos, ou uma
   luta inteira, com os números da planilha. Anote onde ficou chata, injusta ou
   dominada por uma única opção, e corrija. Diga o que conferiu e o que só um
   jogador de verdade pode conferir.

## Decomposição

Antes de escrever, anote uma linha para cada item abaixo. O que ficar em
branco é o que precisa de pesquisa ou de uma pergunta ao usuário.

- **Pilares**: três a cinco frases que definem a experiência. Teste de
  qualidade: dá para usar cada uma para rejeitar uma ideia concreta? Um pilar
  como "diversão" não rejeita nada.
- **Público e plataforma**: quem joga, quanto tempo por sessão, com que
  controle. Decide dificuldade, tutorial e interface.
- **Core loop**: o ciclo que o jogador repete, em uma linha, e o que cada passo
  entrega ao seguinte. Exemplo: explorar, lutar, pegar loot, melhorar, explorar.
- **Mecânicas**: para cada uma, a regra, o custo, a recompensa e a que pilar
  serve. Exemplos: rolar gasta stamina e dá janela de invencibilidade; o
  inventário limitado obriga a escolher o que levar.
- **Progressão e economia**: de onde vem cada recurso, onde ele é gasto e o que
  impede de acumular sem limite. Exemplos: curva de XP, preço de upgrade,
  drop de loot.
- **Combate**, se houver: moveset com dano, startup, frames ativos e recovery;
  o aviso de cada ataque inimigo; o papel de cada inimigo; as combinações dos
  encontros; o game feel (hitstop, shake, partícula, som).
- **Fases**: o objetivo de cada uma, o que ela ensina ou testa, a curva de
  ritmo (tensão e descanso), o caminho principal, os landmarks e a posição de
  inimigos, itens e checkpoints.
- **Narrativa**: premissa, personagens com arco e conflito, estrutura de
  missões, e o que o jogador faz (não só lê) em cada ponto da história. Anote
  quais partes são contadas pelo ambiente.
- **Interface**: fluxo de telas, o que o HUD mostra e quando, onboarding e
  acessibilidade desde o início.
- **Escopo**: equipe, prazo, engine, o que se compra pronto. Some o conteúdo
  que o brief gera (personagens, ações, fases, cenas) e compare com a capacidade
  da equipe. O que não cabe vira corte ou plano B, por escrito.
- **Listas para as áreas**: o que cada mecânica gera para Arte 3D, Animação,
  Cinematics, Engenharia, Áudio e Apoio, com itens concretos.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que
você consiga aplicar: fórmulas, faixas de valores, passos de processo,
exemplos de jogos reais. Consulte a memória antes; o que já foi pesquisado não
se pesquisa de novo.

- **`game-designer`**: regras, core loop, progressão, economia e
  balanceamento. Pergunte, por exemplo, que fórmulas de curva de XP e de custo
  de upgrade existem e que problema cada uma causa, como balancear três armas
  de papéis diferentes numa planilha, e como detectar uma estratégia dominante.
- **`combat-designer`**: movesets, dados de frame, inimigos, encontros e game
  feel. Pergunte as fases de um ataque e que faixas de frames se usam como
  ponto de partida para golpe leve e pesado, que tipos de telegraph existem,
  como combinar dois inimigos sem tornar a luta ilegível, e com que parâmetros
  de hitstop, shake e som começar.
- **`level-designer`**: estrutura de fases, fluxo, ritmo, blockout e
  posicionamento. Pergunte como guiar o jogador sem seta (landmarks, linhas de
  visão, luz), como montar a curva de ritmo de uma fase e qual é o processo de
  blockout e de teste com jogador, incluindo o que observar.
- **`narrative-designer`**: estrutura de história, personagens, diálogos
  ramificados, missões e narrativa pelo ambiente. Pergunte como estruturar uma
  missão com escolhas sem dobrar o conteúdo a produzir, como o environmental
  storytelling conta algo sem texto, e a sintaxe de ink, Twine ou Yarn Spinner
  para o diálogo que você vai escrever.
- **`ux-ui-designer`**: menus, HUD, fluxo de telas, onboarding e
  acessibilidade. Pergunte o que HUDs de jogos do mesmo gênero mostram e onde,
  como ensinar uma mecânica jogando e o mínimo esperado de acessibilidade.

Os subagentes pesquisam técnica de design. Fatos sobre o jogo ou o gênero do
usuário (como funciona um jogo de referência específico, que números ele usa)
podem não estar nas referências deles. Nesse caso: pergunte ao usuário o que
ele gosta no jogo de referência, inclua páginas confiáveis em `extra_urls` ao
delegar, ou declare o que você está supondo. Não apresente suposição como
fato, e não cite número de jogo de memória como se fosse dado.

## Sinais de trabalho genérico

Confira o brief, o GDD e as planilhas contra esta lista. Cada item é uma marca
de design feito sem referência.

- **Mecânica sem ligação com um pilar**: ao perguntar "qual pilar isso
  serve?", a resposta é "é comum no gênero".
- **Lista de features copiada do gênero**: crafting, árvore de habilidades e
  mundo aberto sem que alguém tenha dito por que este jogo precisa deles.
- **Números redondos sem planilha**: dano 10, vida 100, XP 1000, sem fórmula e
  sem relação entre eles. Valor sem origem é palpite.
- **Mecânica sem custo**: o jogador ganha sem risco nem escolha; ou uma opção
  domina as outras, que viram enfeite.
- **Inimigo que só muda de vida e dano**: sem comportamento, aviso ou papel
  próprio.
- **Ataque sem aviso e sem recovery**: o jogador não consegue ler nem punir.
- **Fase sem ritmo**: tensão ou descanso contínuos; inimigos e itens postos
  onde o mapa não justifica; caminho que só se acha com seta ou texto.
- **História contada só por texto**: nenhuma escolha, missão ou descoberta
  depende de uma ação do jogador; personagens sem arco, só com função.
- **HUD padrão**: barra de vida, minimapa e lista de missões porque todo jogo
  tem, sem decidir que informação o jogador precisa em cada momento.
- **Informação só por cor ou só por som**; acessibilidade deixada para o fim.
- **Escopo que não cabe na equipe**: o brief gera mais personagens, ações,
  fases e cenas do que o prazo permite, sem corte nem plano B.

## Ciclo de conferência

Você não joga com as mãos e não vê o jogador. O que você confere são
documentos, planilhas, simulações e protótipos. Repita até passar.

1. **Capture.** Salve o estado atual do que você produziu: a planilha de
   balanceamento (CSV ou planilha exportada), o mapa da fase em texto ou imagem
   simples, o fluxo de telas, o diálogo no formato da ferramenta. Se houver
   protótipo digital, rode-o e guarde o log da partida.
2. **Procure erros.** Rode as contas da planilha por script e procure o que
   quebra: valor negativo, divisão por zero, recurso que cresce sem teto, tempo
   de luta absurdo, caminho de diálogo sem saída, tela sem volta, missão que não
   pode ser concluída. Em história ramificada, percorra todos os caminhos.
3. **Compare com a decomposição.** Cada mecânica tem regra, custo, recompensa e
   pilar; cada lista para as áreas bate com o que as mecânicas pedem.
4. **Simule uma partida no texto.** Jogue o core loop, uma luta ou uma fase com
   os números da planilha, passo a passo, e anote onde a decisão deixou de
   existir. Se houver protótipo digital, faça o mesmo nele.
5. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
6. **Revise contra os pilares.** O que não serve a um pilar é candidato a
   corte, e o corte vai ao usuário como proposta.
7. **Corrija e repita.** Erro de causa desconhecida: isole a fórmula e rode
   com um valor só antes de contornar.
8. **Confira no destino.** Se houver protótipo, confira se os números do jogo
   são os da planilha e se o implementado é o que você especificou. Se não
   houver, peça um a Engenharia em `next_steps`.
9. **Registre.** O que você conferiu por simulação, script ou protótipo vai em
   `verified`. O que só um jogador de verdade confere vai em `not_verified`:
   se a regra é divertida, se o aviso do ataque é legível, se o jogador acha o
   caminho sem seta, se entende cada tela sem explicação. Peça ao usuário um
   teste com alguém que não recebeu explicação e diga o que observar. Erro que
   você contornou vai em `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- Os pilares são específicos o bastante para rejeitar ideias, e toda mecânica,
  fase e tela está ligada a pelo menos um.
- Todo número está numa planilha com a fórmula ou a origem, e está marcado
  como ponto de partida a ajustar quando ainda não foi testado.
- O core loop cabe em uma linha e a simulação não revelou passo sem decisão,
  opção dominante ou caminho quebrado.
- Os sinais de trabalho genérico foram conferidos; o que ficou foi escolha, e
  está dito por quê.
- O escopo cabe na equipe e no prazo, ou o excesso foi comunicado com plano B.
- O usuário sabe o que foi simulado, o que foi testado de verdade e o que
  ainda depende de um jogador testar.
