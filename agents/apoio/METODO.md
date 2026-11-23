---
name: openglitch-apoio-metodo
description: Método de qualidade do agente Apoio. Como decompor QA, localização e marketing, o que pesquisar antes de planejar, os sinais de trabalho genérico e o ciclo de conferência.
---

# Método de qualidade: Apoio

A skill diz o que você entrega. Este método diz como entregar planos de teste,
kits de localização e planos de divulgação que sirvam a este jogo e não a
qualquer jogo. Sem ele, o resultado sai do modelo médio de plano, de tradução
e de página de loja, e é isso que dá a "cara de IA".

## Como usar este método

- **Tarefa avulsa** (um bug report, uma lista de strings, um texto de loja):
  siga só a "Versão curta".
- **Plano de testes de uma entrega, kit de localização, página da loja,
  trailer, calendário ou trabalho de projeto**: siga o método inteiro, na
  ordem das seções.
- A decomposição vem antes de escrever o plano. A pesquisa vem antes de
  afirmar regra de loja, prazo ou prática de localização. A conferência vem
  antes de dizer que está pronto.
- Mostre ao usuário a decomposição e o que você vai pesquisar antes de
  começar. Ele pode cortar o que não importa para ele.
- O método não substitui o brief: plataformas, idiomas, data e orçamento vêm
  de lá. Em projeto solo, o usuário é o QA e o plano precisa caber no tempo dele.

## Ambiente ao vivo

Testar, localizar e divulgar dependem de ver o jogo como ele está. Veja o que
está disponível: uma ferramenta que controla o editor da engine aberto (o
Unity CLI ou o servidor MCP da Unity), a execução de testes automáticos, o
navegador para conferir a página da loja, e a pasta do projeto. Diga ao
usuário com o que você está trabalhando.

- **QA: execute, não suponha.** Rode os testes automáticos e os casos de teste
  no editor aberto, leia o console e capture a tela de cada falha. Um bug só é
  relatado depois de reproduzido.
- **QA: capture a evidência.** Passos, resultado esperado, resultado obtido,
  captura e trecho do log, tirados da execução real.
- **Localização: confira cada texto na tela em que aparece**, por captura, em
  cada idioma: texto cortado, sobreposto, fonte sem o caractere.
- **Localização: extraia os textos do projeto real**, e não de uma lista
  lembrada; texto escrito direto no código também conta.
- **Marketing: leia a página publicada** como um visitante, e confira os
  números (metas, datas, preços) contra a fonte.
- **Marketing: capturas e trechos do jogo saem do jogo rodando**, não de
  montagem.
- **Você não corrige o jogo.** Encontrou o problema: registre e encaminhe ao
  agente da área.
- **O que só o usuário confere**: jogar com teclado, mouse ou controle em tela
  cheia, e a decisão de publicar.

Sem nenhuma ferramenta ao vivo, trabalhe por script e arquivo, como descrito no
ciclo de conferência, e diga ao usuário que você não está vendo a cena dele.

## Versão curta

Para uma tarefa avulsa, quatro verificações bastam:

1. **Cobertura além do caminho feliz.** Para cada caso de teste ou sistema,
   escreva também um caso de borda: entrada vazia, valor máximo, ação repetida,
   interrupção no meio (pausar, fechar, perder o foco da janela).
2. **Reprodução.** Todo bug relatado foi reproduzido por você mais de uma vez
   e o texto traz passos numerados, esperado versus real, ambiente e
   evidência. Se não reproduziu, diga "intermitente" e quantas vezes tentou.
3. **Contexto e espaço.** Toda string tem id, contexto, limite de caracteres e
   variáveis explicadas. Confira o texto mais longo na tela em que aparece.
4. **Fonte do número.** Todo requisito de loja, prazo ou meta de wishlist tem a
   fonte citada. Sem fonte, está marcado como suposição.

## Decomposição

Antes de escrever o plano, uma linha para cada item que se aplica. O que ficar
em branco é o que precisa de pesquisa ou de uma pergunta ao usuário.

**QA**

- **O que precisa funcionar**: as promessas do brief (jogar do início ao fim,
  salvar e carregar, trocar de cena) em ordem de importância para o jogador.
- **Casos de teste por sistema**: movimento, combate, inventário, menu, save,
  som. Cada caso com passos, dado de entrada e resultado esperado.
- **Casos de borda**: carregar um save de versão antiga, inventário cheio,
  pausar durante a animação, trocar de resolução, desconectar o controle.
- **Plataformas e ambiente**: sistemas, placas de vídeo, resolução, controle ou
  teclado, versão do build. Só liste as máquinas que o usuário tem.
- **Critério de aceite**: o que significa "passou" para cada sistema, em
  linguagem verificável (sem crash em 30 minutos, carrega em menos de N
  segundos, ponto de partida a ajustar).
- **Severidade e prioridade**: a escala usada e a regra para cada nível,
  separadas, com um exemplo de jogo para cada.

**Localização**

- **Inventário de textos**: tudo o que o jogador lê: diálogo, interface,
  legenda, item, conquista, erro, loja, tutorial por imagem.
- **Contexto de cada string**: quem fala, em que tela, o que o botão faz.
  "Fire" pode ser disparar ou demitir.
- **Variáveis e plurais**: `{0}`, nomes de jogador, números, plural e gênero.
  Frase montada por colagem não traduz bem.
- **Expansão do texto na interface**: o espaço que cada texto tem e o quanto
  ele cresce em cada idioma. O percentual é ponto de partida a ajustar.
- **Fontes e caracteres**: acentos, símbolos de cada idioma, UTF-8 de ponta a ponta.
- **Glossário e guia de estilo**: nomes próprios, termos de regra, tom de voz,
  tratamento (você, tu) por idioma.

**Marketing**

- **Para quem é o jogo**: o jogador alvo, descrito por jogos que ele já joga e
  onde ele fala sobre jogos.
- **Gancho em uma frase**: o que o jogo tem que os vizinhos de gênero não têm.
- **O que mostrar nos primeiros segundos do trailer**: a ação do jogo, não o
  logotipo.
- **Página da loja**: título curto, descrição, capsule art, capturas e GIFs,
  etiquetas, requisitos, em cada idioma.
- **Calendário**: demo, festival, lançamento, com datas que dependem de regra
  da loja.
- **Metas de wishlist**: número, data e fonte. Sem fonte, é suposição.

## Pesquisa obrigatória

Para cada lacuna da decomposição, delegue ao subagente certo. Peça fatos que
você consiga aplicar: campos, regras, prazos, tamanhos, exemplos. Consulte a
memória antes; o que já foi pesquisado não se pesquisa de novo.

- **`qa`**: modelo de bug report, plano de teste, regressão, severidade e
  prioridade, relatório de desempenho. Pergunte, por exemplo, que campos o
  relatório precisa para o programador reproduzir, que erros comuns tornam um
  report inútil e quando severidade e prioridade divergem.
- **`localization`**: arquitetura de textos, UTF-8, fontes, espaço na
  interface, kit de localização, LQA e o pacote Localization da Unity.
  Pergunte, por exemplo, quanto espaço extra reservar e como tratar plural.
- **`marketing-publisher`**: página da Steam, wishlists, trailer, festivais,
  regras do Steamworks, publisher e programas do Brasil. Pergunte, por
  exemplo, o que a página precisa para converter visita em wishlist, que
  prazos valem para demo e festival e como funciona o Rouanet Games.

Os subagentes pesquisam as referências da área. Fatos sobre este jogo (o
público real, as plataformas do usuário, o texto que existe) e regras que mudam
com o tempo (taxas, prazos, tamanhos de imagem de uma loja) podem não estar
nelas. Nesse caso: pergunte ao usuário, inclua a documentação oficial em
`extra_urls` ao delegar, ou declare o que você está supondo. Não apresente
suposição como fato, e confira requisito de loja na documentação oficial, não
só em blog.

## Sinais de trabalho genérico

Confira o material contra esta lista. Cada item é uma marca de trabalho feito
sem referência.

- **Plano de teste só com o caminho feliz**: sem borda, interrupção, save antigo
  ou entrada inválida.
- **Caso de teste sem resultado esperado**, ou só "funciona corretamente".
- **Bug sem passos para reproduzir**, sem ambiente ou sem versão do build.
- **Tradução literal sem contexto**: string sem id, sem tela, sem limite de
  caracteres, com variável não explicada.
- **Texto que estoura a interface**: cortado ou sobreposto em algum idioma.
- **Texto dentro de imagem** ou fixo no código, ou caractere quebrado na fonte.
- **Descrição de loja que serve para qualquer jogo**: adjetivos ("épico",
  "imersivo") sem dizer o que o jogador faz.
- **Gancho que não cabe em uma frase** ou que descreve o gênero inteiro.
- **Plano de comunidade sem canal nem nome**: "divulgar nas redes".
- **Trailer que começa com logotipos** ou com tela de título; gameplay só depois
  de vários segundos.
- **Meta de wishlist sem fonte** ou sem data; número de blog tratado como regra.
- **Calendário e glossário ausentes**: prazos de loja não checados, termo de regra traduzido de duas formas.

## Ciclo de conferência

Você não vê a tela nem ouve o jogo, então o olho é a captura e a medição.
Repita até passar.

1. **Capture e execute.** Rode os casos de teste por script, linha de comando
   ou build e registre resultado, versão e ambiente de cada um. Capture a tela
   de cada string em cada idioma e os logs do jogo.
2. **Procure erros.** Leia os logs e o console do build atrás de exceção,
   aviso de fonte ausente e chave de texto não encontrada. Procure texto
   cortado nas capturas.
3. **Compare com a decomposição.** Cada item do que precisa funcionar tem caso
   de teste; cada texto do inventário tem string; cada linha do marketing tem
   fonte ou está marcada como suposição.
4. **Passe a lista de sinais de trabalho genérico** e anote o que aparece.
5. **Reproduza antes de relatar.** Repita cada bug, de preferência a partir de
   um estado limpo, e só então escreva o report. Dê o estado inicial exato.
6. **Confira cada string onde aparece.** Para cada idioma, abra a tela e meça o
   texto mais longo contra o espaço disponível. Se puder, force um texto de
   pseudo-localização (mais longo, com acentos) para achar estouro.
7. **Leia a loja como estranho.** Releia a descrição e a lista de capturas e
   pergunte: dá para saber o que o jogador faz? O trailer mostra ação nos
   primeiros segundos? Confira cada número (tamanho de imagem, prazo, meta)
   contra a documentação oficial.
8. **Corrija e repita.** Erro de causa desconhecida: investigue antes de
   contornar.
9. **Confira no destino.** Teste no build que o jogador receberia, na
   plataforma do usuário, e não só no editor. Idioma, fonte e interface mudam
   do editor para o build.
10. **Registre.** O que você conferiu por execução, captura ou fonte vai em
    `verified`. O que só o usuário pode conferir (sentir o jogo, ouvir o som,
    ler a tradução como falante nativo, testar em máquina que você não tem)
    vai em `not_verified`. Erro que você contornou vai em `report_problem`.

## Critérios de pronto

- Cada linha da decomposição foi respondida, por pesquisa, pelo usuário ou
  declarada como suposição.
- O plano cobre caminho feliz, bordas e regressão, e cada caso tem resultado
  esperado.
- Cada bug relatado foi reproduzido e outra pessoa consegue reproduzi-lo só
  lendo.
- Cada string tem id, contexto e limite, e nenhuma estoura a interface nos
  idiomas do jogo.
- A página da loja foi lida como alguém que não conhece o jogo e diz o que o
  jogador faz.
- Todo número de marketing e todo requisito de loja têm fonte ou estão marcados
  como suposição.
- Os sinais de trabalho genérico foram conferidos; o que ficou foi escolha, e
  está dito por quê.
- Foi conferido no build do destino, e não só no editor.
- O usuário recebeu os arquivos, os resultados e a lista do que só ele confere.
