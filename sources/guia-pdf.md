# Guia: Equipes e estudo para um jogo 3D cinematográfico

Transcrição estruturada de `Guia Equipes e estudo para um jogo 3D cinematográfico.pdf` (33 páginas, Nov 22, 2026, @joaquim). Anotações `(p. N)` indicam a página de origem.

**Nota sobre URLs:** o PDF não imprime URLs no texto; elas existem como hiperlinks (anotações de link) sobre o texto citado. Todas as URLs abaixo foram extraídas desses hiperlinks, exatamente como estão no PDF, e associadas ao texto-âncora. Quando uma referência é citada no texto sem hiperlink, consta `URL: (não informada no PDF)`. Casos em que o link parece não coincidir com o texto-âncora estão marcados com `[ATENÇÃO]`.

---

# 1. Visão geral: séries e jogos 3D (p. 1)

Séries (tipo Arcane) e jogos 3D (tiro, sobrevivência, luta) usam quase os mesmos blocos de equipe. A diferença: a série entrega vídeo, o jogo entrega assets que rodam em tempo real.

## Pré-produção (as duas) (p. 1)
- Direção, roteiro, storyboard: definem a história e os planos.
- Concept art / direção de arte: personagens, cenários, estilo visual.
- Game design (só jogos): define o que o personagem faz (atirar, rolar, bloquear), e isso dita as animações necessárias.

## Criação dos assets 3D (p. 1)
- Modelador de personagem: esculpe e faz a malha (ZBrush, Maya, Blender).
- Modelador de ambiente e props: cenários, armas, veículos, objetos.
- Texture / material artist: pintura e materiais (Substance Painter).
- Rigger: monta o esqueleto e os controles que o animador move.
- Technical artist (TD): liga arte e código, otimiza e cria ferramentas. É muito importante em jogos.
- Cabelo, roupa e VFX: simulações de tecido, cabelo, fogo, fumaça, explosões.

## Animação (p. 1)
- Animador de personagem (keyframe): faz a atuação e o movimento à mão.
- Animador de combate / gameplay (jogos): ciclos de andar, correr, pular, golpes e recarga. Precisam encaixar e ter transições suaves.
- Mocap e cleanup: capturam o movimento de atores e limpam os dados.
- Animador de câmera / layout (série): enquadramento e movimentos de câmera.
- Cinematics (jogos): cenas de corte.

## Finalização (p. 2)
- Série: iluminação, render, composição (comp) e edição. O Arcane ainda tem uma camada 2D pintada à mão por cima do 3D.
- Jogos: engine (Unreal/Unity), programadores de gameplay, áudio, QA e produtores.

## Quantas pessoas (estimativas, variam muito) (p. 2)

| Tipo | Equipe total | Só 3D / animação |
|---|---|---|
| Indie | 1 a 20 | 1 a 5 (muitos acumulam funções) |
| Médio (AA) | 30 a 150 | 10 a 40 |
| AAA (tiro, luta, survival) | 200 a 1.000+ (com terceirizados) | 50 a 200+ (animadores ~15 a 60) |
| Série tipo Arcane | algumas centenas ao longo de anos | maioria da equipe |

Em jogo de luta os animadores são mais, porque cada personagem tem dezenas de golpes com timing exato. Em tiro e survival pesam as animações de arma, locomoção e interação. Grandes estúdios também terceirizam parte do trabalho (mocap, props, cutscenes).

# 2. Misturando série e jogo (p. 2)

Dá pra misturar: o resultado é o híbrido (tipo God of War ou The Last of Us), que usa o pipeline de jogo (engine em tempo real) mais as disciplinas de cinema (direção, atuação, câmera, edição).

- Série é linear e pré-renderizada: cada plano é montado e renderizado com qualidade máxima.
- Jogo é interativo e roda em tempo real: tudo precisa funcionar de qualquer ângulo, com o jogador no controle.
- Híbrido: jogabilidade em tempo real + cenas dirigidas como numa série.

## Fases do projeto (p. 2-3)
1. Conceito: ideia, público, referências, escopo. É o que mais define se o projeto vai dar certo.
2. Pré-produção: história, estilo visual, protótipo jogável e lista de tudo que precisa ser feito.
3. Vertical slice: um pedaço do jogo (uns 5 a 10 min) com qualidade final, pra provar que dá pra fazer. (p. 3)
4. Produção: a fase mais longa, quando a maior parte da equipe produz conteúdo.
5. Alpha: tudo existe, mas está quebrado.
6. Beta: foco em corrigir bugs e polir.
7. Lançamento e pós-lançamento: patches, DLCs, atualizações.

AAA leva de 3 a 6 anos. Indie leva de 1 a 3.

# 3. Equipes e o que cada uma faz (p. 3-5)

Um jogo 3D cinematográfico se divide em 8 áreas. Os guias de estudo de cada uma estão nas seções 8 a 15.

## 1. Liderança (p. 3)
- Diretor do jogo / criativo: a visão geral. Decide o que entra e o que sai.
- Produtor: prazos, orçamento, quem faz o quê. Resolve gargalos.
- Diretor de arte: define o visual e aprova toda a arte.
- Diretor técnico: decide as soluções técnicas e a engine.
- Diretor de animação: define o estilo de movimento e lidera os animadores.

## 2. Design (p. 3)
- Game designer: regras, mecânicas, progressão.
- Combat designer: golpes, armas, inimigos e o "feeling" do combate.
- Level designer: monta fases e mapas e guia o jogador.
- Narrative designer / roteirista: história, diálogos, missões.
- UX/UI designer: menus, HUD, tutorial.

## 3. Arte 3D (p. 3-4)
- Concept artist: desenha personagens, cenários, props.
- Character artist: modela e esculpe os personagens.
- Environment artist: cenários e terrenos.
- Props / hard-surface artist: armas, veículos, objetos.
- Texture / material artist: pele, metal, tecido (Substance Painter).
- Lighting artist: iluminação e atmosfera.
- VFX artist: fogo, fumaça, magia, impactos.
- Technical artist: faz a ponte entre arte e código. Otimiza, cria shaders e ferramentas. (p. 4)

## 4. Animação (p. 4)
- Rigger: monta o esqueleto e os controles de cada personagem.
- Animadores de gameplay: andar, correr, pular, atirar, golpear, morrer. As animações precisam se conectar sem "pulos".
- Animadores de cinematic: cenas com atuação mais cuidada, como numa série.
- Mocap team: dirige atores com trajes de captura de movimento. Depois vem o cleanup, a limpeza dos dados.
- Animação facial: expressões e sincronia labial.
- Animation programmer / animation TD: configura state machines, blend trees, IK e motion matching na engine.
- Cloth / hair / physics artist: roupa, cabelo, capas, físicas.

## 5. Cinematics (o lado "série") (p. 4)
- Diretor de cinematic: transforma o roteiro em cenas.
- Layout / câmera: enquadramento, movimento de câmera, ritmo.
- Animadores de cena: atuação plano a plano.
- Editor: montagem e ritmo.
- Iluminação e comp de cena: acabamento final.

Pode ser renderizado em tempo real na própria engine ou pré-renderizado, como no Arcane.

## 6. Engenharia (p. 4)
- Gameplay programmers: controles, combate, câmera, missões.
- Engine / graphics programmers: renderização, performance.
- AI programmers: comportamento de inimigos e NPCs.
- Tools programmers: ferramentas internas pro time.
- Network programmers: multiplayer.
- Build engineers / DevOps: compilam e distribuem as versões.

## 7. Áudio (p. 4-5)
- Sound designers: efeitos, passos, tiros.
- Compositor: trilha sonora.
- Dublagem: diretor de voz, atores, edição.
- Audio programmer: integra o som na engine. (p. 5)

## 8. Apoio (p. 5)
- QA: testam e reportam bugs.
- Localização: tradução e legendas.
- Marketing / comunidade / publisher: trailer, divulgação, lançamento.

# 4. Pipelines (p. 5)

## Pipeline de um personagem (do zero ao jogo)
1. Concept art
2. Blockout (forma bruta)
3. Escultura de alta resolução (ZBrush)
4. Retopologia (versão leve pra rodar no jogo)
5. UV e bake (transfere os detalhes pra versão leve)
6. Texturização
7. Rig e skinning (como a malha segue os ossos)
8. Animações (lista de movimentos necessários)
9. Exportação pra engine
10. Shaders, cabelo, roupa, LODs (versões simplificadas para longe)
11. Testes, ajustes, otimização

O guia de estudo de cada etapa está na seção 16.

## Pipeline de animação em jogo
1. Animation list: lista de todos os movimentos necessários.
2. Produção: mocap ou keyframe manual.
3. Cleanup e polimento.
4. Exportação pra engine.
5. Implementação: state machines, transições, blends, IK nos pés e mãos.
6. Playtest: ajusta o timing até o controle ficar bom.

# 5. Tamanho de equipe e ferramentas (p. 5-6)

Num AAA, a divisão aproximada é: arte 30 a 40%, engenharia 20 a 25%, design 10 a 15%, o resto é QA, áudio, produção e apoio. Os números abaixo são estimativas.

| Escala | Total de pessoas | Animadores |
|---|---|---|
| Indie | 1 a 20 | 0 a 3 |
| AA | 30 a 150 | 5 a 15 |
| AAA | 200 a 1.000+ | 15 a 60 |
| AAA cinematográfico | 300 a 1.000+ | 30 a 100 |

## Ferramentas comuns (p. 6)
- Modelagem e animação: Maya, Blender, 3ds Max, ZBrush, Houdini (efeitos)
- Texturas: Substance Painter e Designer
- Engines: Unreal Engine, Unity
- Controle de versão: Perforce, Git LFS
- Gestão: Jira, Trello, ShotGrid

(Nenhuma URL informada no PDF para estas ferramentas.)

# 6. Equipe pequena ou solo (p. 6)

Um jogo 3D com qualidade de série é inviável sozinho. O que dá pra fazer:
- Escopo pequeno: poucos personagens, poucas fases, uma mecânica principal bem feita.
- Comprar ou reaproveitar: assets prontos (Unity Asset Store, Fab, Quixel), animações do Mixamo, pacotes de animação.
- Estilo simples: low-poly ou estilizado reduz muito o trabalho de modelagem e textura.
- Cinematics: use a própria engine em vez de renderizar.
- Prioridade: jogabilidade primeiro. Visual caprichado só depois de o jogo ser divertido.
- Erro mais comum: aumentar o escopo no meio do caminho (scope creep). É o que mais mata projetos pequenos.

Liderança quase nunca é o primeiro emprego: os diretores de estúdio grande costumam ter de 8 a 15 anos na área que lideram. Sendo solo, você já ocupa os 5 cargos de liderança em escala pequena, e o melhor estudo é terminar jogos pequenos.

# 7. Fontes gratuitas gerais (p. 6-8)

Os livros mais famosos são pagos, mas cada área tem uma opção gratuita equivalente. Fontes específicas de cada cargo estão nos guias das seções 8 a 16.

## Documentários (p. 7)
- **Arcane: Bridging the Rift** — tipo: documentário (YouTube, canal do League of Legends). 5 episódios grátis, do pitch aos toques finais da série. URL: https://www.gamedeveloper.com/press-release/arcane-the-first-episode-of-bridging-the-rift-is-now-available
- **PsychOdyssey** (Double Fine, YouTube) — tipo: canal/documentário. Mais de 30 episódios sobre os bastidores do Psychonauts 2. "O melhor sobre liderança e produção." URL: (não informada no PDF)
- **Noclip** (YouTube) — tipo: canal/documentário. Documentários longos sobre como estúdios fizeram jogos (Doom, Hitman, Monster Hunter, Final Fantasy XIV). URL: (não informada no PDF)
- **GDC Classic Postmortems** — tipo: palestras. Criadores contando o que deu certo e errado em jogos clássicos. URL: (não informada no PDF)

## Cursos e aulas grátis (p. 7)
- **Pixar in a Box** (Khan Academy) — tipo: curso. Currículo gratuito sobre como a Pixar faz filmes (storytelling, modelagem, cenário, efeitos), com legenda em português. URL: https://pixar.com/pixar-in-a-box
- **Cursos gratuitos da Epic Developer Community** — tipo: curso. Mais de 20 cursos profissionais de Unreal (fundamentos, animação, jogos, C++). URL: https://www.unrealengine.com/news/free-professional-unreal-engine-courses-now-available-on-the-epic-developer-community
- **Unity Learn** — tipo: curso. Trilhas gratuitas de Unity, do zero ao avançado. URL: (não informada no PDF)
- **CS50's Introduction to Game Development** (Harvard) — tipo: curso. Gratuito, aulas no YouTube. URL: (não informada no PDF)

## Livros e documentos gratuitos (legalmente) (p. 7)
- **Game Programming Patterns** — tipo: livro online. Livro inteiro grátis no site. URL: https://gameprogrammingpatterns.com/contents.html
- **Guia do Scrum em português** — tipo: documento (PDF oficial). URL: https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR-3.0.pdf
- **gameanim.com** — tipo: site. O livro Game Anim é pago, mas o site tem o rig gratuito "AZRI", tutoriais e blog. URL: https://www.gameanim.com/
- **Gurney Journey** — autor: James Gurney — tipo: blog. Cor, luz e composição. URL: (não informada no PDF)
- **The Door Problem** (lizengland.com) — tipo: texto/site. Texto curto que explica o que cada cargo de um estúdio faz, usando o exemplo de uma porta. URL: (não informada no PDF; só o domínio lizengland.com aparece no texto)
- **Templates de GDD** — tipo: templates. Vários gratuitos no Notion e no itch.io. URL: (não informada no PDF)

## Palestras (p. 7)
- **GDC Vault (gratuitas)** — tipo: arquivo de palestras. Palestras selecionadas recentes e todo o arquivo antigo. Filtre por "Production & Team Leadership", "Visual Arts" ou "Animation Bootcamp". O canal da GDC no YouTube tem muitas das mesmas. URL: https://gdconf.com/gdc-vault

## Canais do YouTube por cargo (p. 8)

| Cargo | Canais |
|---|---|
| Diretor criativo | Game Maker's Toolkit, Masahiro Sakurai on Creating Games, Design Doc |
| Produtor | GDC (talks de produção), PsychOdyssey |
| Diretor de arte | Fortiche/Arcane docs, Proko, Blender Studio |
| Diretor técnico | Unreal Engine, Unity, Sebastian Lague, Acerola |
| Diretor de animação | Alan Becker, New Masters Academy, animadores de jogos no GDC |

(Nenhuma URL informada no PDF para estes canais.)

## Lado "série" (p. 8)
- **Blender Studio** — tipo: canal/curtas abertos. Os curtas abertos (Sprite Fright, Charge, Wing It!) são gratuitos no YouTube e mostram o pipeline de animação 3D. Os arquivos de produção completos ficam na assinatura paga. URL: (não informada no PDF)

## Brasil (p. 8)
- **Criar Jogos** — tipo: curso. Considerado o maior curso gratuito de desenvolvimento de games, com quase 5 mil certificados desde 2022. URL: https://catracalivre.com.br/educacao/curso-gratuito-de-como-criar-games-oferece-800-vagas/
- **SENAC e Unity Learn** — tipo: cursos gratuitos com certificado. URL: https://guiadoscursos.com/cursos-gratuitos-games-2026-unity-senac-certificado/
- **Abragames, BIG Festival e gamescom latam** — tipo: eventos e networking. URL: (não informada no PDF)
- **Marco Legal dos Jogos** — tipo: notícia/legislação. Regulamentado em 14 de outubro de 2026. Prevê o Rouanet Games, com orientação, cursos e oficinas pra preparar projetos e buscar patrocínio pela Lei Rouanet. URL: https://www.educamaisbrasil.com.br/educacao/noticias/marco-legal-dos-jogos-eletronicos-e-regulamentado-no-brasil

## Avisos (p. 8)
- Sites que oferecem PDF de livros pagos "de graça" costumam ser piratas e às vezes trazem vírus. Veja se a biblioteca do seu IF tem acesso aos livros pagos.
- A maioria do material está em inglês. O tradutor automático do Chrome resolve bem.
- Sites em texto envelhecem: alguns deixam de ser atualizados ou saem do ar.

---

# 8. Guia de estudo: Liderança (p. 8-11)

Liderança se aprende fazendo: comece por Produtor e Diretor criativo, que são os que mais fazem um projeto solo terminar.

## Diretor criativo (Game Director) (p. 9)
**O que faz:** guarda a visão do jogo. Decide a experiência central, o que entra e o que sai, e mantém todo mundo na mesma direção.

**O que entrega:**
- Pilares do jogo: 3 a 5 frases que definem a experiência (ex.: "combate pesado e brutal"). Toda decisão é testada contra eles.
- Pitch / one-pager: o jogo explicado em uma página.
- GDD: o documento vivo com mecânicas, história e escopo.
- Decisões de corte: o que fica de fora pra caber no prazo.

**Como aprender:** analisar jogos e anotar por que uma parte funciona; escrever pilares e pitch pros próprios projetos; dar e receber feedback e aprender a dizer "não" pra ideias boas que não cabem.

**Pra praticar:** game jams (Global Game Jam, jams do itch.io). Em 48h você define a visão, corta escopo e entrega.

**Fontes:**
- **A Arte de Game Design** — autor: Jesse Schell (tem em português) — tipo: livro. URL: (não informada no PDF)
- **Criatividade S.A.** — autor: Ed Catmull (Pixar) — tipo: livro. URL: (não informada no PDF)
- **Game Maker's Toolkit** — tipo: canal YouTube. URL: (não informada no PDF)
- **Masahiro Sakurai on Creating Games** — tipo: canal YouTube. URL: (não informada no PDF)
- **Noclip** — tipo: canal YouTube. URL: (não informada no PDF)

## Produtor (p. 9)
**O que faz:** faz o jogo sair. Cuida de prazos, orçamento, prioridades e de quem faz o quê. Destrava gargalos e protege a equipe do caos.

**O que entrega:** cronograma e marcos (vertical slice, alpha, beta), backlog priorizado, orçamento, gestão de riscos (o que pode atrasar e o plano B) e reuniões curtas de alinhamento.

**Como aprender:** metodologias ágeis (Scrum, Kanban); estimar tarefas e comparar depois com o tempo real; ferramentas como Trello, Notion, HacknPlan (feito pra games) e Jira.

**Pra praticar:** planeje seu próximo projeto em sprints de 1 a 2 semanas e registre o quanto atrasou. Em projeto de escola em grupo, assuma a organização das tarefas.

**Fontes:**
- **The Game Production Toolbox** — autor: Heather Chandler — tipo: livro. (Da autora há também o **Manual de Produção de Jogos Digitais** em português.) URL: (não informada no PDF)
- **Agile Game Development** — autor: Clinton Keith — tipo: livro. URL: (não informada no PDF)
- **Advanced Agile Game Development Practices** — tipo: palestra no GDC Vault. URL: https://gdcvault.com/free/gdc-17/?&media=as
- **Sangue, Suor e Pixels** — autor: Jason Schreier — tipo: livro. URL: (não informada no PDF)
- **Guia do Scrum em português** — tipo: documento PDF. URL: https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR-3.0.pdf
- **Atlassian Agile Coach** — tipo: site. Texto no PDF: "(atlassian.com/agile)". URL: atlassian.com/agile (domínio como aparece no texto; sem hiperlink)
- **Postmortems no Game Developer** — tipo: site/artigos. Texto no PDF: "(gamedeveloper.com)". URL: gamedeveloper.com (domínio como aparece no texto; sem hiperlink)

## Diretor de arte (p. 10)
**O que faz:** define o visual do jogo inteiro e garante que tudo pareça do mesmo mundo.

**O que entrega:** style guide / art bible (paleta, formas, materiais, proporções), moodboards, paintovers (pinta por cima do trabalho dos artistas pra corrigir) e aprovação dos assets.

**Como aprender:** fundamentos (forma, cor, luz, composição, silhueta); escrever o style guide de jogos e séries que você gosta; saber o básico do pipeline 3D.

**Pra praticar:** escolha um estilo (ex.: estilizado tipo Arcane, low-poly) e monte uma art bible de 5 páginas pro seu projeto.

**Fontes:**
- **Color and Light** — autor: James Gurney — tipo: livro. URL: (não informada no PDF)
- **Gurney Journey** — autor: James Gurney — tipo: blog. URL: (não informada no PDF)
- **Framed Ink** — autor: Marcos Mateu-Mestre — tipo: livro. URL: (não informada no PDF)
- **Palestra de direção de arte de Diablo 2: Resurrected** — tipo: palestra, GDC Vault grátis. URL: https://gdcvault.com/free/?&media=v
- **Palestra de direção de arte de Street Fighter V** — tipo: palestra, GDC Vault grátis. URL: https://gdcvault.com/free/gdc-17/?&media=as [ATENÇÃO: o hiperlink sobre "Street Fighter V" é o mesmo da palestra de Agile (gdc-17/?&media=as); pode não ser o link específico]
- **Arcane: Bridging the Rift** — tipo: documentário. URL: (não informada neste trecho; ver seção 7)
- **Breakdowns no 80.lv** — tipo: site. Texto no PDF: "80.lv". URL: (não informada neste trecho)

## Diretor técnico (p. 10)
**O que faz:** decide como o jogo vai ser construído: engine, arquitetura, ferramentas, performance. Avalia o que é possível e quanto custa.

**O que entrega:** escolha de engine, arquitetura do código e padrões da equipe, orçamento técnico (polígonos, texturas, personagens por cena, meta de FPS), pipeline de assets e avaliação de riscos técnicos.

**Como aprender:** programação sólida (C# pra Unity, C++ ou Blueprints pra Unreal); padrões de projeto e otimização (profiler, draw calls, LODs); o básico de arte 3D e animação.

**Pra praticar:** faça o mesmo protótipo pequeno nas duas engines e compare. Depois otimize uma cena pesada até ela rodar bem.

**Fontes:**
- **Game Programming Patterns** — tipo: livro online grátis. URL: https://gameprogrammingpatterns.com/contents.html
- **Game Engine Architecture** — autor: Jason Gregory — tipo: livro. URL: (não informada no PDF)
- **Cursos gratuitos de Unreal** — tipo: curso. URL: https://www.unrealengine.com/news/free-professional-unreal-engine-courses-now-available-on-the-epic-developer-community
- **Unity Learn** — tipo: curso. URL: (não informada no PDF)
- **CS50 Game Development** — tipo: curso. URL: (não informada no PDF)
- **Catlike Coding** — tipo: site/tutoriais. URL: (não informada neste trecho; ver Engenharia)
- **Red Blob Games** — tipo: site. URL: (não informada neste trecho; ver Engenharia)
- **LearnOpenGL** — tipo: site/livro online. URL: (não informada neste trecho; ver Engenharia)
- **GPU Gems** (site da NVIDIA) — tipo: livro online. URL: (não informada no PDF)

## Diretor de animação (p. 10-11)
**O que faz:** define como os personagens se movem (realista ou exagerado), aprova as animações e garante que fiquem bonitas e boas de jogar.

**O que entrega:** guia de estilo de movimento (peso, timing, exagero, personalidade), animation list, decisão do que é mocap e do que é keyframe, e revisão das animações junto com o combat designer.

**Como aprender:** os 12 princípios da animação; a diferença do jogo pra série (no jogo a animação precisa responder rápido ao controle); state machines, blend spaces, IK, motion matching. (p. 11)

**Pra praticar:** anime um ciclo de andar, um pulo e um golpe, coloque num personagem jogável e ajuste até ficar bom de controlar.

**Fontes:**
- **Manual de Animação (The Animator's Survival Kit)** — autor: Richard Williams — tipo: livro. URL: (não informada no PDF)
- **Game Anim** — autor: Jonathan Cooper (líder em Assassin's Creed e Mass Effect; a 2ª edição tem mocap e motion matching) — tipo: livro. URL: https://www.routledge.com/Game-Anim-Video-Game-Animation-Explained/Cooper/p/book/9780367707651
- **Conteúdo gratuito da Epic sobre State Machines e Motion Matching** — tipo: conteúdo de aprendizado. URL: https://www.unrealengine.com/learning/januarys-epic-learning-content-nanite-metahuman-pcg-and-more
- **The Orange Duck** (theorangeduck.com) — tipo: site/blog. URL: (não informada como hiperlink; domínio theorangeduck.com no texto)
- **Alan Becker** — tipo: canal YouTube. URL: (não informada no PDF)
- **Animation Mentor** — tipo: curso pago. URL: (não informada no PDF)
- **iAnimate** — tipo: curso pago. URL: (não informada no PDF)

---

# 9. Guia de estudo: Design (p. 11-14)

Design é a área mais fácil de começar sozinho: dá pra praticar com papel, protótipo simples e até jogo de tabuleiro. Em equipe pequena, um mesmo designer faz quase tudo isso.

## Game designer (p. 11)
**O que faz:** cria as regras do jogo (o que o jogador pode fazer, como ganha, perde e evolui) e cuida do balanceamento.

**O que entrega:** GDD e documentos de cada mecânica; core loop (ex.: explorar → lutar → pegar loot → melhorar → explorar); planilhas de balanceamento (dano, vida, preço, XP); protótipos.

**Como aprender:** analisar jogos e escrever o core loop deles; planilha (Excel ou Google Sheets) pra balanceamento; protótipos feios testados com outras pessoas.

**Pra praticar:** mude uma regra de um jogo simples (jogo da velha, Uno) e veja como o jogo muda. Depois faça isso num protótipo digital.

**Fontes (texto, grátis):**
- **Game Design Concepts** — autor: Ian Schreiber — tipo: curso em formato de blog (curso inteiro de game design). URL: https://www.gbgames.com/2010/07/05/free-game-design-course-game-balance-concepts/ [ATENÇÃO: o hiperlink sobre "Game Design Concepts" aponta para um post do gbgames.com sobre "free game design course: Game Balance Concepts"]
- **Game Balance Concepts** — autor: Ian Schreiber (cofundador da Global Game Jam) — tipo: curso grátis em blog focado só em balanceamento. URL: (não informada como hiperlink separado; ver link acima)
- **Lost Garden** — autor: Daniel Cook — tipo: blog/ensaios. URL: (não informada no PDF)
- **raphkoster.com** — autor: Raph Koster — tipo: blog/ensaios sobre sistemas, motivação e diversão. URL: raphkoster.com (domínio como aparece no texto)
- **Game Developer (gamedeveloper.com), seção Design** — tipo: site, milhares de artigos e postmortems. URL: gamedeveloper.com (domínio como aparece no texto)

## Combat designer (p. 12)
**O que faz:** cria o combate: golpes, armas, inimigos e o "feeling" de cada ataque. Central em jogo de luta, tiro e ação.

**O que entrega:** moveset (golpes com dano, startup e recovery); design de inimigos; encontros (combinações de inimigos); ajuste de game feel (hitstop, screen shake, partículas, som do impacto).

**Como aprender:** pense o combate como o jogo fazendo perguntas (comportamento dos inimigos), dando ferramentas pra responder (ataques do jogador) e mudando as perguntas a cada luta. Um ataque quase nunca é divertido na primeira versão: precisa de game feel. Jogue com atenção, conte frames e repare no que o inimigo "avisa" antes de atacar.

**Pra praticar:** um personagem com 3 golpes e 1 inimigo com 2 ataques. Ajuste até a luta ficar justa. Depois coloque 2 inimigos juntos.

**Fontes (texto, grátis):**
- **Sirlin.net / Playing to Win** — autor: David Sirlin (designer-chefe do Street Fighter HD Remix) — tipo: livro grátis no site + artigos de balanceamento multiplayer. "Obrigatório pra jogo de luta." URL: https://www.sirlin.net/ptw
- **Combat System Design** — autor/fonte: Evozon — tipo: artigo (boas práticas e lista de recursos; cita "Anatomy of a Successful Attack" de Ben Ruiz). URL: https://www.evozon.com/combat-system-design/
- **Série de Bart Vossen no Game Developer** — tipo: artigos (level design, design de inimigos e IA em combate corpo a corpo). URL: https://gamedeveloper.com/design/enemy-design-and-enemy-ai-for-melee-combat-systems
- **Game Combat Design Guide** — tipo: guia (visão geral da área). URL: https://gamedesignskills.com/game-design/combat-design/
- **Anatomy of a Successful Attack** — autor: Ben Ruiz — tipo: artigo (citado dentro do Combat System Design). URL: (não informada no PDF)

## Level designer (p. 12-13)
**O que faz:** monta fases e mapas, decide por onde o jogador anda, onde ficam inimigos e segredos, e guia o jogador sem seta na tela.

**O que entrega:** planta/mapa 2D; blockout/greybox (fase só com cubos); ritmo da fase (tensão e descanso); posicionamento de inimigos, itens e checkpoints.

**Como aprender:** desenhe de memória o mapa de uma fase que você gosta e anote por que funciona; estude fluxo (caminho principal, landmarks, linhas de visão); faça blockout na engine (ProBuilder na Unity, Modeling na Unreal).

**Pra praticar:** uma fase só com cubos cinza, de 5 a 10 minutos. Peça pra alguém jogar sem explicar nada e observe onde a pessoa se perde.

**Fontes (texto, grátis):**
- **The Level Design Book** — autor: Robert Yang — tipo: livro online, projeto sem fins lucrativos (processo, ritmo, escopo, combate, estudos de fases reais, ex.: Undead Burg, Dark Souls 1). "O melhor recurso grátis." URL: https://book.leveldesignbook.com/
- **E-book de level design da Unity** — autor: level designers profissionais — tipo: e-book. URL: https://unity.com/resources/introduction-to-level-design-in-game-development-and-in-unity
- **Cyberpunk 2077 Quest Design Wiki** (seção "Level design 101") — tipo: wiki. URL: https://cyberpunk-2077-quest-design.gitbook.io/cyberpunk-2077-design-wiki/generic-game-design/design-basics/level-design-101

## Narrative designer / roteirista (p. 13)
**O que faz:** cria história, personagens, diálogos e missões, e faz tudo funcionar dentro da jogabilidade.

**O que entrega:** bíblia do mundo (lore, facções, lugares, regras); fichas de personagem; roteiro de cutscenes e diálogos com ramificações; estrutura de missões.

**Como aprender:** fundamentos de roteiro (3 atos, arco de personagem, conflito); ferramentas gratuitas ink, Twine e Yarn Spinner; environmental storytelling (muito usado em survival).

**Pra praticar:** uma história interativa curta (~5 minutos) com 2 ou 3 escolhas que mudam o final, em Twine ou ink.

**Fontes (texto, grátis):**
- **Emily Short's Interactive Storytelling** — autor: Emily Short — tipo: blog (o mais respeitado sobre narrativa em jogos; inclui o guia "Self-Training in Narrative Design"). URL: https://emshort.blog/self-training-in-narrative-design
- **Tutorial do ink (inkle)** — tipo: tutorial (feito pra iniciantes completos). URL: https://www.inklestudios.com/ink/web-tutorial/
- **Documentação do Twine** — tipo: documentação. URL: (não informada no PDF)
- **Documentação do Yarn Spinner** — tipo: documentação. URL: (não informada no PDF)

## UX/UI designer (p. 13-14)
**O que faz:** cuida do que o jogador vê e usa pra entender o jogo: menus, HUD, ícones, tutoriais.

**O que entrega:** wireframes, fluxo de telas, mockups e guia de estilo da UI, tutorial/onboarding, opções de acessibilidade (legenda, daltonismo, remapeamento).

**Como aprender:** princípios de UX (hierarquia visual, legibilidade, feedback); Figma (gratuito); estudar e copiar telas de muitos jogos.

**Pra praticar:** redesenhe no Figma o menu ou HUD de um jogo confuso e explique em 3 linhas o que melhorou.

**Fontes (texto, grátis):**
- **Game UI Database** (gameuidatabase.com) — tipo: banco de referências (mais de 55 mil telas e 1.700 vídeos de 1.341 jogos, grátis e sem anúncios). URL: https://gamefromscratch.com/the-game-ui-database/ [ATENÇÃO: o hiperlink aponta para um artigo do gamefromscratch.com sobre o Game UI Database, não para gameuidatabase.com; o domínio gameuidatabase.com aparece só no texto]
- **Blog da Celia Hodent** (celiahodent.com) — autora: Celia Hodent — tipo: blog (UX de jogos e psicologia do jogador). URL: celiahodent.com (domínio como aparece no texto)
- **Game Accessibility Guidelines** (gameaccessibilityguidelines.com) — tipo: site/guia. URL: gameaccessibilityguidelines.com (domínio como aparece no texto) (p. 14)
- **Laws of UX** (lawsofux.com) — tipo: site. URL: lawsofux.com (domínio como aparece no texto) (p. 14)

## Por onde começar (Design) (p. 14)
1. Game Design Concepts (base de tudo)
2. The Level Design Book (já cobre combate e ritmo)
3. A área do seu tipo de jogo: luta → Sirlin.net; tiro/ação → artigos de combat design; história → Emily Short + ink

---

# 10. Guia de estudo: Arte 3D (p. 14-17)

Arte 3D é a área com mais material gratuito em texto, quase tudo em forma de "breakdowns" (o artista mostra passo a passo como fez). A base pra todos os cargos: Blender (gratuito) e o Manual do Blender (docs.blender.org).

- **Manual do Blender** — tipo: documentação. URL: docs.blender.org (domínio como aparece no texto; sem hiperlink)

## Concept artist (p. 14)
**O que faz:** desenha personagens, cenários, armas e criaturas antes de alguém modelar.

**O que entrega:** sketches de exploração; turnaround (frente, lado, costas); callouts de detalhes; pinturas de cenário com clima e luz.

**Como aprender:** perspectiva, forma, silhueta, cor e luz, anatomia, design de formas.

**Pra praticar:** 20 silhuetas rápidas do mesmo personagem, escolha a melhor e faça o turnaround.

**Fontes:**
- **Drawabox** — tipo: curso/lições gratuitas baseadas em exercícios, inspiradas em concept artists e designers industriais (leva de 5 meses a 2 anos). URL: https://drawabox.com/
- **Gurney Journey** — tipo: blog. URL: (não informada no PDF)

## Character artist (p. 14)
**O que faz:** modela e esculpe os personagens e deixa o modelo pronto pra rig e animação.

**O que entrega:** escultura high-poly, low-poly retopologizado, UVs, mapas "bakeados" (normal, AO) e texturas.

**Como aprender:** anatomia (o que mais pesa); escultura e retopologia; topologia que dobra bem nas articulações.

**Pra praticar:** uma cabeça simples, depois um personagem estilizado inteiro, com versão low-poly colocada na engine.

**Fontes:**
- **80.lv** — tipo: site (breakdowns de personagens). URL: (não informada neste trecho)
- **Polycount** — tipo: fórum e wiki (o wiki teve períodos fora do ar). URL: (não informada no PDF)
- **Manual do Blender** (Sculpt Mode, Retopology) — tipo: documentação. URL: (não informada no PDF)

## Environment artist (p. 15)
**O que faz:** constrói cenários bonitos e otimizados.

**O que entrega:** kits modulares (paredes, pisos, portas que encaixam), terrenos, vegetação, set dressing e a cena montada na engine.

**Como aprender:** modelagem modular, texturas "tileáveis", composição de cena, otimização (LODs, instâncias).

**Pra praticar:** recrie um cômodo real da sua casa usando só peças modulares.

**Fontes:**
- **80.lv** — tipo: site. URL: (não informada neste trecho)
- **Game Art Tricks** — tipo: artigo ou vídeo (como jogos famosos "enganam" o jogador pra parecer bonitos gastando pouco). URL: https://simonschreibt.de/game-art-tricks/
- **The Level Design Book** — tipo: livro online. URL: https://book.leveldesignbook.com/ (mesma da seção Level designer)

## Props / hard-surface artist (p. 15)
**O que faz:** modela objetos "duros": armas, veículos, robôs, máquinas. Central em jogo de tiro.

**O que entrega:** modelos com bordas limpas, bevels corretos, versões high e low, normal maps e LODs.

**Como aprender:** subdivisão, booleanas, controle de normais e smoothing groups, estudo de objetos reais.

**Pra praticar:** modele uma arma ou ferramenta real a partir de fotos, do blockout até a textura.

**Fontes:**
- **Polycount** (threads de hard surface e normals) — tipo: fórum. URL: (não informada no PDF)
- **80.lv** — tipo: site. URL: (não informada neste trecho)
- **Manual do Blender** (Bevel, Boolean, Weighted Normal) — tipo: documentação. URL: (não informada no PDF)

## Texture / material artist (p. 15)
**O que faz:** pinta e cria materiais (metal, pele, couro, ferrugem) realistas ou estilizados.

**O que entrega:** mapas PBR (base color, roughness, metallic, normal), materiais procedurais, bibliotecas reutilizáveis.

**Como aprender:** teoria do PBR primeiro; depois Substance Painter/Designer ou alternativas gratuitas (Blender, Material Maker).

**Pra praticar:** o mesmo objeto em 3 materiais (madeira nova, metal enferrujado, plástico gasto).

**Fontes:**
- **The PBR Guide** — autor: Adobe/Allegorithmic (gratuito desde 2014; parte 1 teoria, parte 2 prática, vale pra qualquer software) — tipo: guia. URL: https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2
- **Documentação do Substance** — tipo: documentação. URL: (não informada no PDF)

## Lighting artist (p. 16)
**O que faz:** ilumina as cenas pra criar clima e guiar o olhar sem pesar no desempenho.

**O que entrega:** iluminação de cada área, sombras, GI (luz rebatida), pós-processamento e luz das cutscenes.

**Como aprender:** cor e luz da fotografia e do cinema; luz em tempo real vs. "bakeada"; estudar a luz de filmes e séries (o Arcane é ótimo exemplo).

**Pra praticar:** ilumine a mesma cena de 3 jeitos: dia feliz, noite de terror, pôr do sol melancólico.

**Fontes:**
- **Guia de iluminação HDRP da Unity** — tipo: e-book gratuito. URL: https://unity.com/resources/lighting-hdrp-guide
- **Documentação de iluminação da Unreal** (Lumen, pós-processamento) — tipo: documentação. URL: (não informada no PDF)
- **Gurney Journey** — tipo: blog. URL: (não informada no PDF)

## VFX artist (p. 16)
**O que faz:** cria efeitos: fogo, fumaça, explosões, magia, impactos, tiros, chuva. Dá "peso" ao combate.

**O que entrega:** sistemas de partículas, flipbooks, shaders de efeito e efeitos sincronizados com animação e som.

**Como aprender:** Niagara (Unreal) ou VFX Graph (Unity); shaders básicos; timing (antecipação, impacto, dissipação).

**Pra praticar:** o efeito de um golpe de espada: rastro, faísca no impacto, poeira no chão.

**Fontes:**
- **RealTimeVFX** — tipo: comunidade/fórum (criada por devs da Riot, EA e Naughty Dog; thread "Getting Started" pra iniciantes). URL: https://realtimevfx.com/t/getting-started-in-real-time-vfx-start-here
- **E-book de VFX da Unity** (edição Unity 6) — tipo: e-book gratuito. URL: https://unity.com/resources/creating-advanced-vfx-unity6
- **Game Art Tricks** — tipo: artigo/vídeo. URL: https://simonschreibt.de/game-art-tricks/ (mesma de Environment artist)

## Technical artist (TD) (p. 16-17)
**O que faz:** ponte entre arte e programação: shaders, ferramentas, scripts, otimização e "por que esse asset não funciona na engine".

**O que entrega:** shaders, ferramentas de pipeline (exportação, validação), orçamento técnico e documentação pros artistas.

**Como aprender:** shaders (HLSL/GLSL ou shader graph), scripting (Python pro Blender, C# pra Unity), profiling e o básico do pipeline de arte.

**Pra praticar:** um shader de dissolver (personagem "desmancha" ao morrer) e um script Python que exporta todos os modelos de uma pasta.

**Fontes:**
- **The Book of Shaders** — tipo: livro online gratuito, com editor ao vivo. URL: https://thebookofshaders.com/
- **Unity for Technical Artists** — tipo: e-book gratuito de 91 páginas. URL: https://80.lv/articles/unity-released-a-free-book-for-technical-artists
- **Game Art Tricks** (palestra sobre RenderDoc e NSight) — tipo: palestra. URL: https://simonschreibt.de/game-art-tricks/ (hiperlink dado em outras ocorrências; nesta ocorrência o texto não tem hiperlink)
- **Catlike Coding** — tipo: site/tutoriais. URL: https://catlikecoding.com/unity/tutorials/ (hiperlink dado na seção Engenharia)
- **Riot Tech Blog** (technology.riotgames.com) — tipo: blog. URL: technology.riotgames.com (domínio como aparece no texto)

## Por onde começar (Arte 3D, sendo solo) (p. 17)
1. Blender básico + Manual do Blender
2. PBR Guide
3. Game Art Tricks (ensina a "trapacear" bem)
4. Unity for Technical Artists

Personagem detalhado, hard surface avançado e VFX podem ser comprados prontos no começo.

---

# 11. Guia de estudo: Animação (p. 17-20)

Animação é o centro do seu pacote de animação pra Unity. O que serve direto pra esse projeto está marcado com [pacote].

## Rigger (p. 17)
**O que faz:** cria o esqueleto (ossos) e os controles do animador, e define como a malha deforma.

**O que entrega:** esqueleto com nomes e hierarquia padronizados; skinning/weight painting; controles IK/FK; rig de jogo leve e compatível com a engine.

**Como aprender:** hierarquia de ossos, IK vs. FK, constraints; weight painting (o que mais dá trabalho); diferença entre rig de animação (cheio de controles, fica no Blender/Maya) e esqueleto de jogo (só os ossos, vai pra engine).

**Pra praticar:** rigue um braço simples com IK, depois um personagem inteiro com o Rigify do Blender.

**Fontes:**
- **Manual do Blender** (Armatures, Rigging, Rigify) — tipo: documentação. URL: (não informada no PDF)
- **[pacote] Unity Animation Rigging** — tipo: documentação/pacote Unity (rigs de deformação e de interação com IK/Aim; constraints Chain IK, Damped Transform, Multi-Aim, Twist Correction, Two Bone IK). URL: https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html
- **gameanim.com** — rig AZRI gratuito pra Maya — tipo: site/ferramenta. URL: https://www.gameanim.com/

## Animador de gameplay (p. 17-18)
**O que faz:** anima o que o jogador controla (andar, correr, pular, atirar, golpear, rolar, morrer). As animações precisam encaixar e responder rápido.

**O que entrega:** ciclos em loop, transições (parado → andando → correndo → parando), ações (golpes, recarga, esquiva), variações.

**Como aprender:** os 12 princípios adaptados a jogos; ciclos de locomoção (peso, contato do pé); responsividade (antecipação longa demais fica "lenta" no controle).

**Pra praticar:** ciclo de andar, correr, um pulo e um golpe num personagem jogável, ajustados até ficar gostoso de controlar.

**Fontes:**
- **Os 12 princípios da animação em jogos** — tipo: artigo (capítulo gratuito do Game Anim, com exemplos de Cuphead e Shadow of the Colossus). URL: https://www.gamedeveloper.com/production/the-12-principles-of-animation-in-video-games
- **[pacote] Blog gameanim.com** — autor: Jonathan Cooper (animou em The Last of Us 2, Uncharted 4, Assassin's Creed 3 e Mass Effect) — tipo: blog. Posts citados: "The Combat Of Assassin's Creed", "The Art And Animation Of Celeste", "Half-Life: Alyx – AnimGraph", "The Five Fundamentals Of Video Game Animation". URL: https://www.gameanim.com/page/7/

## Animador de cinematic (p. 18)
**O que faz:** anima as cenas de história com atuação caprichada, como numa série.

**O que entrega:** animação plano a plano, atuação corporal e facial sincronizada com a dublagem, cenas no sequenciador (Sequencer na Unreal, Timeline na Unity).

**Como aprender:** atuação (intenção, pausa, olhar, peso emocional), linguagem de câmera, ferramentas de cinematic da engine.

**Pra praticar:** anime um personagem "falando" um áudio de 10 segundos (o desafio do 11 Second Club).

**Fontes:**
- **gameanim.com: "Creating a Deeper Emotional Connection: The Cinematography of God of War"** — tipo: artigo/blog. URL: https://www.gameanim.com/page/4/
- **Blog da StudioBinder** — tipo: blog. URL: (não informada neste trecho)
- **Documentação do Sequencer** — tipo: documentação. URL: (não informada neste trecho)
- **Documentação do Timeline** — tipo: documentação. URL: (não informada no PDF)
- **11 Second Club** (desafio) — tipo: desafio/site. URL: (não informada no PDF)

## Mocap + cleanup (p. 18-19)
**O que faz:** captura movimentos de atores e limpa os dados (tremedeira, pés escorregando), adaptando ao esqueleto do jogo.

**O que entrega:** animações capturadas limpas, retargeting pra cada personagem, loops e transições a partir dos takes.

**Como aprender:** formatos (BVH, FBX), retargeting, limpeza de curvas, foot locking.

**Pra praticar:** baixe uma animação de mocap gratuita, faça retargeting pro seu personagem e corrija os pés.

**Fontes:**
- **[pacote] CMU Graphics Lab Motion Capture Database** — tipo: banco de dados de mocap (2.605 capturas em 6 categorias; comece pelos sujeitos de número mais alto; há versão em FBX). URL: https://mocap.cs.cmu.edu/resources.php
- **Versão em FBX do CMU Mocap** — tipo: dataset. URL: https://data.4tu.nl/datasets/0448aab2-3332-449f-a8e2-d208cb58c7df
- **Documentação de retargeting do Blender** — tipo: documentação. URL: (não informada no PDF)
- **Documentação de retargeting da Unity (Humanoid)** — tipo: documentação. URL: (não informada no PDF)
- **Documentação de retargeting da Unreal (IK Retargeter)** — tipo: documentação. URL: (não informada no PDF)

**Atenção pro pacote (p. 19):** a licença do CMU permite incluir os dados em produtos vendidos, mas proíbe revender os dados diretamente, mesmo convertidos. Dá pra usar dentro de um jogo, não pra vender um pacote feito só com eles. (Hiperlink sobre "licença do CMU": https://paperswithcode.com/dataset/cmu-motion-capture)

## Animação facial (p. 19)
**O que faz:** expressões, olhar e lip sync.

**O que entrega:** rig facial (ossos ou blend shapes), visemes (poses de fonemas), expressões base, animação facial das cenas.

**Como aprender:** FACS (divide qualquer expressão em movimentos de músculos); blend shapes/shape keys; formas da boca pra cada som.

**Pra praticar:** 6 expressões básicas num rosto simples, depois o personagem falando uma frase.

**Fontes:**
- **FACS na Wikipedia** (action units, uso como pesos de blend shapes) — tipo: enciclopédia. URL: https://en.wikipedia.org/wiki/Facial_Action_Coding_System
- **iMotions: FACS Visual Guidebook** — tipo: guia/blog. URL: https://imotions.com/blog/facial-expression-pictures/
- **Manual do Blender** (Shape Keys) — tipo: documentação. URL: (não informada no PDF)

## Animation TD / animation programmer (p. 19-20)
**O que faz:** faz as animações funcionarem dentro do jogo e decide qual toca e quando. É o coração de um pacote de animação.

**O que entrega:** Animator Controllers / Animation Blueprints, blend spaces, IK de pés e mãos, motion matching, ferramentas pros animadores.

**Como aprender:** state machines e blend trees, IK procedural, motion matching, C# (Unity) ou C++/Blueprints (Unreal).

**Pra praticar:** locomoção completa (parado, andar, correr, virar) com IK nos pés subindo escada; depois um motion matching simples.

**Fontes:**
- **[pacote] The Orange Duck** (theorangeduck.com) — autor: Daniel Holden (animação e machine learning na Epic, ex-Ubisoft La Forge) — tipo: blog (artigos sobre motion matching, blending e springs, e uma implementação simples de Motion Matching). URL: (sem hiperlink; domínio theorangeduck.com no texto)
- **[pacote] Motion Matching na Unreal** — tipo: documentação (a melhor explicação escrita do conceito, útil mesmo pra quem usa Unity). URL: https://dev.epicgames.com/documentation/unreal-engine/motion-matching-in-unreal-engine
- **[pacote] Game Animation Sample Project** (Epic, gratuito, atualizado pra UE 5.8, com documentação escrita) — tipo: projeto de exemplo. URL: https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8
- **Documentação de animação da Unity** (Animator, Blend Trees, Humanoid) — tipo: documentação. URL: (não informada no PDF)
- **Unity Animation Rigging** — tipo: documentação. URL: https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html (hiperlink dado em Rigger)

**Atenção (p. 20):** a Epic permite usar e fazer retargeting das animações do Sample, mas o conteúdo da Epic costuma ter licença ligada à Unreal. Leia a licença antes de usar num produto pra Unity; o mais seguro é usar só pra estudar.

## Cloth / hair / physics (p. 20)
**O que faz:** simula roupa, capa, cabelo, partes que balançam e ragdoll.

**O que entrega:** configuração de tecido e cabelo, jiggle bones, ragdolls, ajustes pra rodar leve.

**Como aprender:** física básica (rigidbody, joints), simulação de tecido, o truque de usar ossos com física simples no lugar de tecido completo.

**Pra praticar:** capa e rabo de cavalo num personagem andando, ajustados até não atravessarem o corpo.

**Fontes:**
- **Manual do Blender** (Cloth, Hair) — tipo: documentação. URL: (não informada no PDF)
- **Documentação da Unity** (Cloth, Ragdoll Wizard, Joints) — tipo: documentação. URL: (não informada no PDF)
- **Documentação da Unreal** (Chaos Cloth, Physics Asset) — tipo: documentação. URL: (não informada no PDF)
- **Damped Transform do Unity Animation Rigging** — tipo: documentação. URL: https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html (hiperlink dado em Rigger)

## Por onde começar (Animação, pensando no pacote) (p. 20)
1. Os 12 princípios em jogos (artigo grátis do Game Anim)
2. Manual do Blender: Rigify
3. Documentação de animação da Unity + Animation Rigging
4. Motion Matching da Unreal + The Orange Duck

Pro pacote, a origem das animações é o ponto mais importante: mocap seu, keyframe seu ou dados com licença que permita revenda.

---

# 12. Guia de estudo: Cinematics (p. 20-22)

Cinematics é a parte "série" do jogo, e a primeira decisão é como renderizar:
- Tempo real (na engine): mais barato, fácil de mudar, mesmo visual do jogo. É o que quase todo jogo faz hoje.
- Pré-renderizado (vídeo): mais bonito, mas pesado e difícil de alterar. Sendo solo, quase nunca vale a pena.

## Diretor de cinematic (p. 20-21)
**O que faz:** transforma o roteiro em cenas: o que o público vê, em que ordem, com que emoção, e como a cena se liga ao gameplay.

**O que entrega:** breakdown do roteiro (objetivo emocional de cada cena); storyboard/animatic; direção de atuação pra mocap, dublagem e animadores; aprovação final.

**Como aprender:** linguagem cinematográfica (planos, ângulos, ritmo, ponto de vista); toda cena precisa mudar algo; saber quando não fazer cutscene.

**Pra praticar:** faça o storyboard de uma cena de 1 minuto de uma série, plano a plano. Depois crie uma sua.

**Fontes:**
- **gameanim.com: "Creating a Deeper Emotional Connection: The Cinematography of God of War"** — tipo: artigo. URL: https://www.gameanim.com/page/4/
- **Virtual Production Field Guide** (Epic) — tipo: PDF grátis de 98 páginas, acessível a quem tem noção básica de cinema. URL: https://www.cartoonbrew.com/tech/epic-games-has-created-the-ultimate-guide-to-virtual-production-177529.html
- **Virtual Production Field Guide, volume 2** (158 páginas) — tipo: PDF. URL: https://www.cgchannel.com/tag/vpfg

## Layout / câmera (p. 21)
**O que faz:** posiciona e move a câmera em cada plano (enquadramento, lente, movimento, ritmo) e posiciona os personagens (blocking).

**O que entrega:** layout de cada plano, movimentos de câmera (dolly, pan, tracking, câmera na mão), previz.

**Como aprender:** tipos de plano, ângulos e movimentos; regra dos 180°, regra dos terços, eixo do olhar; lentes; Cine Camera (Unreal) e Cinemachine (Unity).

**Pra praticar:** a mesma conversa entre 2 personagens de 3 jeitos (plano/contraplano, plano-sequência, câmera na mão).

**Fontes:**
- **StudioBinder: Ultimate Guide to Camera Shots** — tipo: guia (tamanhos, enquadramento, movimentos, cheat-sheet e shot list pra baixar). URL: https://studiobinder.com/blog/ultimate-guide-to-camera-shots/
- **Documentação de cinematics da Unreal** (Cine Camera Actor) — tipo: documentação. URL: https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematics-and-movie-making-in-unreal-engine
- **Documentação do Cinemachine** — tipo: documentação. URL: (não informada no PDF)

## Animador de cena (p. 21)
Detalhado na seção 11 (Animador de cinematic). Dica que vem da série: anime pra câmera, não pro mundo. Se a câmera está num close do rosto, ninguém vê os pés.

(Referências: ver Animação > Animador de cinematic.)

## Editor (p. 21-22)
**O que faz:** monta os planos e decide quando cortar, controlando ritmo e emoção.

**O que entrega:** montagem de cada cena, ritmo geral das cinematics, transição entre cutscene e gameplay.

**Como aprender:** corte na ação, corte no olhar, match cut, J-cut e L-cut; quando segurar e quando cortar rápido; o Sequencer como editor dentro da engine.

**Pra praticar:** monte os mesmos planos em duas versões, uma calma e uma tensa.

**Fontes:**
- **StudioBinder: The Rule of Six** — tipo: artigo (regra do editor Walter Murch: emoção 51%, história 23%, ritmo 10%, eye-trace 7%...). URL: https://www.studiobinder.com/blog/walter-murch-rule-of-six/
- **The Walter Murch-opedia** — tipo: artigo/site. URL: https://jonnyelwyn.co.uk/film-and-video-editing/the-walter-murch-opedia/
- **Sequencer (Unreal)** — tipo: documentação. URL: https://dev.epicgames.com/documentation/unreal-engine/using-cinematics-and-sequencer-in-unreal-engine-for-maya-users
- **Documentação do Timeline (Unity)** — tipo: documentação. URL: (não informada no PDF)

## Luz e comp (p. 22)
**O que faz:** acabamento final. A luz cria clima e guia o olhar; a composição junta camadas e corrige cor. Em tempo real, "comp" vira pós-processamento.

**O que entrega:** luz de cada plano, color grading, efeitos de lente e, no pré-renderizado, a imagem final composta.

**Como aprender:** luz principal, preenchimento e contraluz; color grading; pós-processamento ou compositor do Blender.

**Pra praticar:** 3 gradings do mesmo plano: quente e nostálgico, frio e tenso, saturado e "videogame".

**O caso Arcane:**
- Fundos pintados em 2D projetados sobre geometria 3D simples (projection mapping) dão profundidade sem gastar muito (RedShark News).
- Nos cenários, a equipe cria um set 3D e projeta matte painting nele, com linhas tremidas feitas à mão (80.lv).
- As texturas foram realmente pintadas à mão.

**Fontes:**
- **RedShark News** (pipeline da Fortiche e shaders próprios) — tipo: artigo. URL: https://redsharknews.com/why-netflixs-arcane-looks-so-good-how-fortiche-ramped-up-the-animation-pipeline
- **80.lv: artigo sobre Arcane (fundos: arte tradicional + 3D)** — tipo: artigo (citado como "(80.lv)" no caso Arcane). URL: https://80.lv/articles/arcane-artists-show-how-they-combine-traditional-art-3d-for-backgrounds
- **80.lv: Ekko em Substance e Blender** — tipo: artigo. URL: https://80.lv/articles/3d-artist-recreates-arcane-s-ekko-with-substance-3d-blender
- **Tese "Creating Fortiche-Inspired Environment"** — tipo: tese (PDF grátis, recria o estilo na Unreal Engine 5). URL: https://reposit.haw-hamburg.de/bitstream/20.500.12738/16175/1/MA_Creating_Fortiche-Inspired_Environment.pdf
- **Manual do Blender** (Compositor) — tipo: documentação. URL: (não informada no PDF)
- **Post Process da Unreal e da Unity** — tipo: documentação. URL: (não informada no PDF)

## Por onde começar (Cinematics) (p. 22)
1. StudioBinder (planos + câmera)
2. Rule of Six (quando cortar)
3. Sequencer ou Timeline
4. Tese do estilo Fortiche, se quiser o visual tipo Arcane

Regra de escopo: cutscene é caro. Num jogo pequeno, faça poucas, curtas e na engine.

---

# 13. Guia de estudo: Engenharia (p. 22-25)

Engenharia tem o melhor material escrito gratuito. A base pra todos os cargos (p. 22-23):
- **C# (Unity):** documentação da Microsoft (learn.microsoft.com), com versão em português. URL: learn.microsoft.com (domínio como aparece no texto)
- **C++ (Unreal ou engine própria):** learncpp.com, indicado pelo LearnOpenGL. URL: https://learnopengl.com/Introduction [ATENÇÃO: o hiperlink sobre "learncpp.com" aponta para learnopengl.com/Introduction, não para learncpp.com]
- **Git:** o livro Pro Git, grátis em git-scm.com/book, com tradução pra português. URL: git-scm.com/book (como aparece no texto; sem hiperlink)

## Gameplay programmer (p. 23)
**O que faz:** programa o que o jogador sente: controle, câmera, combate, pulo, inventário, missões.

**O que entrega:** controlador do personagem, câmera, combate, vida e dano, armas, inventário, missões, save, e ferramentas pros designers ajustarem números sem mexer no código.

**Como aprender:** game loop e update vs. fixed update; componentes, eventos, state machines; física de jogo (rigidbody, colisão, raycast); "feeling" (coyote time, input buffering, aceleração).

**Pra praticar:** controlador de terceira pessoa (andar, correr, pular, esquivar, câmera que não atravessa parede) e um ataque com hitbox.

**Fontes:**
- **Game Programming Patterns** (capítulos Game Loop, State, Component, Observer) — tipo: livro online. URL: https://gameprogrammingpatterns.com/contents.html
- **Catlike Coding** (Basics e Movement) — tipo: site/tutoriais. URL: https://catlikecoding.com/unity/tutorials/
- **Fix Your Timestep!** (Gaffer On Games) — tipo: artigo clássico sobre atualizar a física. URL: https://gafferongames.com/post/fix_your_timestep/

## Engine / graphics programmer (p. 23)
**O que faz:** programa como o jogo é desenhado: renderização, luz, sombras, shaders, desempenho.

**O que entrega:** pipeline de renderização, shaders de base (pele, cabelo, água), otimização (draw calls, culling, LOD), ferramentas de profiling.

**Como aprender:** vetores, matrizes e trigonometria; como a GPU funciona (vertex e fragment shaders); uma API gráfica (OpenGL é a mais fácil); profiler da engine.

**Pra praticar:** um triângulo em OpenGL, depois um cubo com textura e luz. Na Unity, um shader de água simples.

**Fontes:**
- **LearnOpenGL** — tipo: livro online gratuito "pra sempre", com PDF da edição impressa. URL: https://learnopengl.com/
- **The Book of Shaders** — tipo: livro online. URL: https://thebookofshaders.com/ (hiperlink dado em Technical artist)
- **Catlike Coding** (Rendering e Advanced Rendering) — tipo: site/tutoriais. URL: https://catlikecoding.com/unity/tutorials/
- **Real-Time Rendering** — tipo: lista de livros gratuitos (como Ray Tracing Gems II). URL: https://www.realtimerendering.com/books.html

## AI programmer (p. 23-24)
**O que faz:** programa o comportamento de inimigos e NPCs: ver, perseguir, atacar, fugir, agir em grupo.

**O que entrega:** pathfinding, sistemas de decisão (state machines, behavior trees, utility AI), percepção (visão, audição), IA de grupo.

**Como aprender:** A* (a base); Behavior Trees; IA de jogo precisa ser divertida, não perfeita.

**Pra praticar:** um inimigo que patrulha, ouve, investiga e persegue; depois 3 inimigos que tentam cercar.

**Fontes:**
- **Red Blob Games** (A*, Breadth First, Dijkstra) — tipo: site/tutoriais. URL: https://www.redblobgames.com/pathfinding/
- **Red Blob Games: implementação em Python e C++** (licença Apache 2.0, uso comercial liberado) — tipo: código/tutorial. URL: https://redblobgames.com/pathfinding/a-star/implementation.html
- **Game AI Pro** — tipo: livro online (todos os capítulos gratuitos, casos reais de jogos comerciais). URL: https://www.gameaipro.com/
- **Pathfinding Demystified** — autor: Gabriel Gambetta — tipo: artigo/série. URL: https://gabrielgambetta.com/path1.html

## Tools programmer (p. 24)
**O que faz:** cria ferramentas internas: editores de fase, importadores, janelas na engine, automações.

**O que entrega:** extensões do editor (janelas e inspetores na Unity), importação e validação de assets, debug dentro do jogo, plugins pra Blender/Maya.

**Como aprender:** editor scripting da Unity (EditorWindow, CustomEditor, ScriptableObject); Python do Blender (bpy); UX básico.

**Pra praticar:** uma janela na Unity que lista todas as animações do projeto e mostra quais estão sem configuração.

**Fontes:**
- **Documentação de Editor Scripting da Unity** — tipo: documentação. URL: (não informada no PDF)
- **Documentação da API Python do Blender** (docs.blender.org/api) — tipo: documentação. URL: docs.blender.org/api (como aparece no texto; sem hiperlink)
- **Unity for Technical Artists** — tipo: e-book. URL: https://80.lv/articles/unity-released-a-free-book-for-technical-artists (hiperlink dado em Technical artist)

Pro seu pacote, este cargo pesa muito: um pacote pra Unity vende muito pela ferramenta de editor que vem junto.

## Network programmer (p. 24-25)
**O que faz:** programa o multiplayer: conexão, sincronização e como esconder o lag.

**O que entrega:** arquitetura cliente-servidor, sincronização, predição no cliente, compensação de lag, proteção contra trapaça.

**Como aprender:** servidor autoritativo; predição, reconciliação, interpolação; uma biblioteca de rede (Netcode for GameObjects ou Mirror na Unity, Replication na Unreal).

**Pra praticar:** 2 jogadores andando numa sala, com lag simulado.

**Fontes:**
- **Fast-Paced Multiplayer** — autor: Gabriel Gambetta — tipo: artigo/série (arquitetura, predição e reconciliação, interpolação, compensação de lag e demo ao vivo). URL: https://www.gabrielgambetta.com/client-server-game-architecture.html
- **Gaffer On Games** — autor: Glenn Fiedler (nome do autor não consta no PDF) — tipo: blog (física em rede; o autor agora escreve em mas-bandwidth.com, mas os artigos continuam valendo). URL: https://gafferongames.com/post/ (mas-bandwidth.com: sem hiperlink)

Sendo solo, evite multiplayer no primeiro jogo. (p. 25)

## Build engineer / DevOps (p. 25)
**O que faz:** garante que o jogo compile, seja testado e chegue aos jogadores.

**O que entrega:** controle de versão (Git LFS ou Perforce), build automático (CI/CD), testes automáticos, publicação na Steam, itch.io ou Asset Store.

**Como aprender:** Git e Git LFS; CI/CD com GitHub Actions; processo de cada loja.

**Pra praticar:** projeto Unity no GitHub com LFS e build automático pra Windows a cada push.

**Fontes:**
- **Pro Git** (git-scm.com/book) — tipo: livro online gratuito, com tradução pra português. URL: git-scm.com/book (como aparece no texto; sem hiperlink)
- **GameCI** — tipo: CI open source pra jogos, gratuito pra sempre. URL: https://github.com/game-ci
- **GameCI 1: Intro to GitHub Actions for Unity** — tipo: tutorial passo a passo (inclusive deploy WebGL pelo GitHub Pages). URL: https://davidmfinol.github.io/gameci-1_intro.html

## Por onde começar (Engenharia) (p. 25)
1. Game Programming Patterns
2. Catlike Coding: Basics + Movement
3. Editor scripting da Unity (pro pacote)
4. Pro Git + GameCI

Gráficos, IA e rede ficam pra quando um projeto precisar.

---

# 14. Guia de estudo: Áudio (p. 25-27)

Jogo sem som bom parece "barato", e áudio é uma das áreas que indie mais esquece.

## Sound designer (p. 25-26)
**O que faz:** cria os efeitos sonoros (passos, tiros, golpes, explosões, UI, ambientes). O som dá peso: o mesmo golpe parece fraco ou devastador dependendo do áudio.

**O que entrega:** biblioteca de efeitos, variações (5 versões do mesmo passo), ambientes em loop, sons de UI.

**Como aprender:** gravação (até com celular) e edição (Audacity, Reaper); camadas (um tiro tem estalo, corpo, cauda, eco); jogar sem música só prestando atenção nos efeitos.

**Pra praticar:** refaça todo o áudio de um vídeo de gameplay sem som.

**Fontes:**
- **Designing Sound** — tipo: site/blog (cerca de 2.000 posts, Creative Commons). URL: https://designingsound.org/
- **Guia de som de armas de Chuck Russom** (Medal of Honor e God of War), dentro do Designing Sound — tipo: artigo. URL: https://cdm.link/?p=10910 [ATENÇÃO: hiperlink aponta para cdm.link, não para designingsound.org]
- **Entrevista com Ben Minto** (diretor de som de Star Wars Battlefront), dentro do Designing Sound — tipo: entrevista. URL: (não informada no PDF)
- **freesound.org** (confira a licença de cada som) — tipo: banco de sons gratuito. URL: freesound.org (como aparece no texto; sem hiperlink)
- **Pacote anual gratuito da Sonniss** (na época da GDC) — tipo: banco de sons gratuito. URL: (não informada no PDF)

## Compositor (p. 26)
**O que faz:** cria a trilha sonora e faz ela reagir ao jogo (combate, tensão, exploração).

**O que entrega:** temas principais, trilhas de cada área, música adaptativa em camadas, stingers, loops.

**Como aprender:** teoria musical básica; uma DAW (Reaper, FL Studio, Cakewalk); música interativa.

**Pra praticar:** uma música com 3 camadas (exploração, tensão, combate) trocando dentro da engine.

**Fontes:**
- **musictheory.net** — tipo: lições interativas gratuitas. URL: musictheory.net (como aparece no texto; sem hiperlink)
- **Wwise-201** — tipo: certificação de música interativa (material e quizzes gratuitos, só o exame é pago; mais de 300 páginas passo a passo com jogo e arquivos de música). URL: https://www.audiokinetic.com/courses/wwise201
- **Material/quizzes gratuitos do Wwise-201** — tipo: material. URL: https://thesoundarchitect.co.uk/?p=16784
- **Wwise-201 certification (300+ páginas passo a passo)** — tipo: material. URL: https://www.cras.edu/wwise-201-certification-video-games/

## Dublagem (voice over) (p. 26)
**O que faz:** grava as vozes: diretor de voz, atores e edição (limpar, cortar, padronizar volume).

**O que entrega:** roteiro de gravação com contexto de cada fala, gravações editadas e nomeadas, "esforços" (gritos, golpes, respiração, morte).

**Como aprender:** básico de gravação (microfone, sala sem eco, ganho); dar contexto ao ator, porque em jogo as falas são gravadas soltas; organização dos arquivos.

**Pra praticar:** 10 falas de um personagem gravadas, editadas e colocadas no jogo com legenda.

**Fontes:**
- **Designing Sound** (posts de gravação e diálogo) — tipo: site/blog. URL: https://designingsound.org/ (hiperlink dado em Sound designer)
- **IGDA Best Practices for Game Localization** (parte de gravação de voz em várias línguas) — tipo: PDF/guia. URL: https://www.igda.org/resources/best-practices/ (hiperlink dado em Localização)

Sendo solo, muitos indies não usam voz ou só usam efeitos curtos ("hm!", "ah!"). É um bom corte de escopo.

## Audio programmer (p. 26-27)
**O que faz:** integra o som na engine: quando cada som toca, distância, oclusão, mixagem dinâmica, desempenho.

**O que entrega:** integração com FMOD ou Wwise, som 3D, regras de mixagem e prioridade, ferramentas pros sound designers.

**Como aprender:** AudioSource e AudioMixer da Unity; um middleware (FMOD ou Wwise); áudio 3D (atenuação, reverb por área).

**Pra praticar:** passos que mudam conforme o chão (madeira, pedra, grama) e música que muda quando o combate começa. (p. 27)

**Fontes:**
- **Wwise-101** — tipo: curso (20 lições, 20 quizzes, 1 exame). URL: https://www.audiokinetic.com/courses/wwise101
- **FMOD** — tipo: middleware (licença Indie grátis ou US$2.000 por título, pra orçamentos abaixo de US$600 mil). URL: https://fmod.com/studio
- **FMOD licensing** — tipo: página de licenciamento (confira as condições em fmod.com/licensing). URL: https://fmod.com/licensing
- **Designing Sound: Learning Audio Middleware Online** (de 2015, mas a lógica vale) — tipo: artigo. URL: https://designingsound.org/2015/01/26/learning-audio-middleware-online-where-to-start/

Pra começar solo, o áudio nativo da Unity já dá conta.

---

# 15. Guia de estudo: Apoio (p. 27-28)

Jogo com bug ou sem divulgação não vende, mesmo sendo bom. Estas três funções são as que mais aparecem nas avaliações ruins.

## QA (testes) (p. 27)
**O que faz:** joga pra quebrar o jogo (bugs, travamentos, partes confusas, desempenho) e reporta de um jeito que o programador consiga corrigir.

**O que entrega:** bug reports claros, planos de teste, testes de regressão, relatórios de desempenho em máquinas diferentes.

**Como aprender:** escrever bom bug report (a habilidade principal); pensar como quem quer quebrar o jogo; diferença entre severidade (quão grave) e prioridade (quão urgente).

**Pra praticar:** ache 5 bugs num jogo indie gratuito e escreva um report bem feito de cada um.

**Fontes:**
- **Sloperama FAQ 75: How To Write A Game Bug Report** — autor: (professor de QA de games na University of Southern California; nome não consta no PDF) — tipo: artigo/FAQ. URL: https://sloperama.com/advice/faq75.html
- **Bugnet: How to write good bug reports** — tipo: artigo (título, passos pra reproduzir, esperado vs. real, ambiente, severidade, evidências). URL: https://bugnet.io/blog/how-to-write-good-bug-reports-for-game-development
- **Kelina Cowell: Bug Reports Developers Don't Ignore** — autora: Kelina Cowell — tipo: artigo. URL: https://kelinacowellqa.github.io/Manual-QA-Portfolio-Kelina-Cowell/articles/how-to-write-bug-reports.html

Sendo solo, você é seu próprio QA e joga "do jeito certo". Chame amigos pra jogar e observe sem ajudar.

## Localização (p. 27-28)
**O que faz:** adapta o jogo pra outras línguas e culturas: tradução, piadas, referências, fontes, tamanho do texto na tela, cores e símbolos.

**O que entrega:** textos traduzidos e revisados, kit de localização (contexto, glossário, guia de estilo), teste do jogo traduzido (LQA), página da loja traduzida.

**Como aprender:** preparar o jogo desde o início (todo texto em arquivo separado, nada no código ou na imagem); UTF-8, fontes com acento, interface que aguenta textos maiores; pacote Localization da Unity. (p. 28)

**Pra praticar:** deixe seu jogo em português e inglês, com troca de idioma no menu.

**Fontes:**
- **IGDA: Best Practices for Game Localization** — tipo: PDF gratuito (culturalização, arquitetura do produto, gravação de voz, QA linguístico). URL: https://www.igda.org/resources/best-practices/
- **Game Developer: 9 game localization best practices** — tipo: artigo (espaço extra na UI, UTF-8, kit de localização). URL: https://gamedeveloper.com/production/9-game-localization-best-practices
- **Pacote Localization da Unity** — tipo: documentação/pacote. URL: (não informada no PDF)

Sua vantagem: lançar com PT-BR e inglês desde o primeiro dia já te coloca na frente de muito indie gringo.

## Marketing / comunidade / publisher (p. 28)
**O que faz:** faz as pessoas saberem que o jogo existe e quererem comprar. O publisher financia e/ou divulga o jogo em troca de parte da receita.

**O que entrega:** página na Steam (ou Asset Store, no caso do pacote), trailer e capturas, wishlists, festivais (Steam Next Fest), comunidade (Discord), contato com imprensa e criadores.

**Como aprender:** gênero e gancho (o marketing começa na escolha do jogo); algoritmo da Steam (wishlists, festivais, demo); capsule art e trailer que mostram o gameplay nos primeiros segundos.

**Pra praticar:** crie a página da loja do próximo projeto cedo e acompanhe as wishlists.

**Fontes:**
- **How To Market A Game** — autor: Chris Zukowski — tipo: blog (o mais seguido por indies sobre Steam; ideia central: a primeira decisão de marketing é o jogo que você escolhe fazer; referência: jogos com potencial costumam juntar mais de 150 wishlists nas primeiras 2 semanas; ele tem uma aula gratuita sobre montar a página na Steam). URL: https://unitycodemonkey.com/howtomarketagame.php [ATENÇÃO: o hiperlink sobre "How To Market A Game" aponta para unitycodemonkey.com, não para o blog do Zukowski]
- **Hiperlink sobre "a primeira decisão de marketing é o jogo que você escolhe fazer"** — URL: https://unity.com/vn/blog/tips-strategies-for-marketing-indie-games
- **Hiperlink sobre "mais de 150 wishlists nas primeiras 2 semanas"** — URL: https://medium.com/@info_46369/how-my-first-game-got-700-wishlists-in-its-first-2-weeks-fe7190b4791e
- **Documentação do Steamworks** (partner.steamgames.com/doc) — tipo: documentação (regras oficiais de página, festivais, demos e lançamento). URL: partner.steamgames.com/doc (como aparece no texto; sem hiperlink)
- **[pacote] Documentação de publisher da Unity Asset Store** — tipo: documentação (requisitos de qualidade e documentação pra vender pacotes; "leia antes de começar"). URL: (não informada no PDF)
- **Brasil: Abragames, BIG Festival, gamescom latam e o Rouanet Games** (seção 7) — tipo: eventos/programa. URL: ver seção 7 (somente o Marco Legal tem hiperlink)

---

# 16. Guia de estudo: pipeline de um personagem (p. 28-32)

O pipeline do quadro "Equipes de um jogo 3D cinematográfico" tem 8 etapas: Concept → Blockout → Escultura → Retopo + UV/bake → Texturas → Rig + skinning → Animação → Engine. Abaixo, cada etapa com quem faz, o que entrega, como aprender e fontes gratuitas. (p. 28-29)

Uma referência que cobre o pipeline inteiro: **3D Artist's Handbook** — tipo: wiki gratuito no GitHub sobre o fluxo de personagem (topologia, retopologia, bake, texturização). URL: https://sidney-eliot.github.io/3d-artists-handbook/theory/topology-and-retopology

## Etapa 1: Concept (p. 29)
**Quem faz:** concept artist, aprovado pelo diretor de arte.
**O que entrega:** design do personagem, turnaround (frente, lado, costas), callouts de detalhes e materiais, paleta de cores.
**Como aprender:** perspectiva, forma, silhueta, anatomia, cor. Um personagem bom se reconhece só pela sombra.
**Pra praticar:** 20 silhuetas rápidas, escolha uma e faça o turnaround dela.
**Fontes:**
- **Drawabox** — tipo: curso. URL: https://drawabox.com/
- **Gurney Journey** — tipo: blog. URL: (não informada no PDF)

**Atalho solo:** se não desenha, monte um moodboard de referências e uma ficha escrita do personagem. Já serve como "concept" pra modelar.

## Etapa 2: Blockout (p. 29)
**Quem faz:** character artist.
**O que entrega:** forma bruta com primitivas (cubos, cilindros, esferas) nas proporções certas, usada pra aprovar silhueta e escala antes do detalhe.
**Como aprender:** proporções e escala (altura em "cabeças"); comparar o modelo com o concept em vista frontal e lateral; testar escala na engine cedo.
**Pra praticar:** blockout do seu personagem em 1 hora, importado na Unity ao lado de um cubo de 1 metro.
**Fontes:**
- **Manual do Blender** (Modeling) — tipo: documentação. URL: (não informada no PDF)
- **Breakdowns de personagens no 80.lv** — tipo: site. URL: (não informada neste trecho)

## Etapa 3: Escultura (high-poly) (p. 29-30)
**Quem faz:** character artist.
**O que entrega:** modelo de alta resolução com todo o detalhe (músculos, rugas, costuras, peças de roupa), que depois vira mapas na versão leve.
**Como aprender:** anatomia; escultura digital (Sculpt Mode do Blender ou ZBrush); trabalhar do grande pro pequeno (formas grandes, depois médias, depois detalhes).
**Pra praticar:** esculpa uma cabeça simples, depois o personagem inteiro em estilo estilizado.
**Fontes:**
- **Manual do Blender** (Sculpting) — tipo: documentação. URL: (não informada no PDF)
- **Blender Studio: Stylized Character Workflow** — tipo: curso (parte dos vídeos é aberta). URL: https://studio.blender.org/training/stylized-character-workflow/5e5406a786994e6b58c7e54b
- **80.lv** — tipo: site. URL: (não informada neste trecho)

## Etapa 4a: Retopologia (low-poly) (p. 30)
**Quem faz:** character artist (às vezes com o technical artist).
**O que entrega:** malha leve e limpa, com o número de polígonos do orçamento técnico e edge loops onde o corpo dobra.
**Por que importa:** a retopologia faz o modelo deformar de forma natural nos movimentos e simplifica o weight painting. Personagens animados precisam de edge loops em volta dos olhos, da boca e das articulações, que ferramentas automáticas nem sempre fazem bem. (Hiperlinks nesses trechos: https://en.wikipedia.org/wiki/Retopology e https://help.maxon.net/zbr/en-us/Content/html/user-guide/3d-modeling/topology/Retopo/01-retopo.html)
**Como aprender:** quads, edge flow seguindo os músculos, poles, loops extras em cotovelo, joelho e ombro; ferramentas de retopo do Blender (snap, shrinkwrap) ou ZRemesher.
**Pra praticar:** retopologize sua escultura e teste dobrando o braço e o joelho com um rig simples. Onde amassar, adicione loops.
**Fontes:**
- **Blender Studio: Live Retopology** — tipo: post gratuito (loops essenciais e edge flow). URL: https://studio.blender.org/blog/live-retopology-at-bcon22
- **Guia de topologia de Michael VL** — tipo: wiki (padrões de redirecionar loops, vale pra qualquer software). URL: https://michael-vl.github.io/learning-wiki/blender/topology/
- **3D Artist's Handbook: topologia** — tipo: wiki. URL: https://sidney-eliot.github.io/3d-artists-handbook/theory/topology-and-retopology
- **Manual do Blender** (Retopology) — tipo: documentação. URL: (não informada no PDF)
- **Referências de apoio no texto (retopologia / ZBrush):** https://en.wikipedia.org/wiki/Retopology ; https://help.maxon.net/zbr/en-us/Content/html/user-guide/3d-modeling/topology/Retopo/01-retopo.html

## Etapa 4b: UV e bake (p. 30)
**Quem faz:** character artist ou texture artist.
**O que entrega:** UVs (a malha "desembrulhada" em 2D) e mapas "bakeados" do high-poly pro low-poly: normal map, ambient occlusion, curvature.
**Como aprender:** seams (cortes do UV) em lugares escondidos; UV sem estiramento e com densidade de texel parecida; cage e distância de projeção no bake; hard edges sempre na borda de uma ilha de UV (senão aparecem costuras no normal map); tangent space (MikkTSpace) compatível com a engine.
**Pra praticar:** faça o UV do seu low-poly, bake o normal map da escultura e confira na Unity se não aparecem costuras.
**Fontes:**
- **Manual do Blender: Seams** — tipo: documentação (fluxo: marcar seams, desembrulhar, ajustar e repetir). URL: https://www.blender.org/manual/en/modeling/meshes/uv/unwrapping/seams.html
- **The Toolbag Baking Tutorial** (Marmoset) — tipo: tutorial (o guia de bake mais recomendado, mesmo pra quem não usa o Toolbag). URL: https://www.marmoset.co/posts/toolbag-baking-tutorial/
- **This is normal 2: Baking normal maps** — tipo: artigo (explica as costuras de bake). URL: https://typhen.artstation.com/blog/BDr6/this-is-normal-2-baking-normal-maps
- **Baking Maps for Games Reading List** — tipo: lista de leituras, com foco em Unity. URL: https://camille_meehan.artstation.com/blog/LYbj/baking-maps-for-games-reading-list

## Etapa 5: Texturas (p. 30-31)
**Quem faz:** texture / material artist.
**O que entrega:** mapas PBR (base color, roughness, metallic, normal) ou texturas pintadas à mão, no estilo do jogo.
**Como aprender:** teoria PBR; Substance Painter ou alternativas (Blender, Material Maker); pra estilo Arcane, pintar luz e pinceladas na própria textura.
**Pra praticar:** texture o personagem com 3 materiais bem diferentes (pele, tecido, metal).
**Fontes:**
- **The PBR Guide** — tipo: guia gratuito. URL: https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2
- **80.lv: Ekko estilo Arcane em Substance e Blender** — tipo: artigo. URL: https://80.lv/articles/3d-artist-recreates-arcane-s-ekko-with-substance-3d-blender

## Etapa 6: Rig e skinning (p. 31)
**Quem faz:** rigger.
**O que entrega:** esqueleto padronizado, weight painting (quanto cada osso puxa da malha), controles de animação e, separado, o esqueleto de jogo leve.
**Como aprender:** hierarquia de ossos, IK/FK, weight painting; nomes de ossos compatíveis com o Humanoid da Unity (facilita o retargeting).
**Pra praticar:** rigue o personagem com Rigify, gere o esqueleto de jogo e teste poses extremas (agachar, braço pra cima).
**Fontes:**
- **Manual do Blender** (Rigging, Rigify) — tipo: documentação. URL: (não informada no PDF)
- **Unity Animation Rigging** — tipo: documentação. URL: https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html
- **Rig AZRI gratuito em gameanim.com** — tipo: ferramenta/rig. URL: https://www.gameanim.com/ (hiperlink dado na seção 7)

## Etapa 7: Animação (p. 31)
**Quem faz:** animadores de gameplay e de cinematic, mocap e cleanup.
**O que entrega:** a animation list completa (parado, andar, correr, pular, golpes, reações, morte), ciclos em loop, transições.
**Como aprender:** 12 princípios, ciclos de locomoção, responsividade, retargeting de mocap (detalhes na seção 11).
**Pra praticar:** os 4 movimentos básicos (parado, andar, correr, pulo) e 1 golpe no seu personagem.
**Fontes:**
- **Os 12 princípios em jogos** — tipo: artigo. URL: https://www.gamedeveloper.com/production/the-12-principles-of-animation-in-video-games
- **CMU Mocap** (atenção à licença, veja a seção 11) — tipo: banco de dados. URL: https://mocap.cs.cmu.edu/resources.php
- **gameanim.com** — tipo: site/blog. URL: https://www.gameanim.com/ (hiperlink dado na seção 7)

## Etapa 8: Engine (exportação, shaders, LODs, testes) (p. 31-32)
**Quem faz:** technical artist, animation TD e programadores.
**O que entrega:** FBX importado com escala certa, materiais e shaders configurados (pele, cabelo, roupa), LODs (versões mais leves pra longe), Animator configurado, testes de desempenho.
**Como aprender:**
- Importação: escala e unidades (a Unity usa 1 unidade = 1 metro; o 3ds Max usa 1 unidade = 10 cm), tipo de rig Humanoid ou Generic, blend shapes. Veja Importing Models na Unity.
- LODs: se você nomear as malhas como `_LOD0`, `_LOD1`, `_LOD2`, a Unity cria o LOD Group sozinha na importação.
- Shaders e testes: shader graph, profiler, testar o personagem em cena real com luz do jogo.

**Pra praticar:** exporte o personagem final com 3 LODs, importe na Unity, configure o Animator e meça o desempenho com 20 cópias na cena.
**Fontes:**
- **Unity: Importing Models** — tipo: documentação. URL: https://docs.unity3d.com/es/current/Manual/ImportingModelFiles.html (nota: caminho "es" = versão em espanhol da documentação)
- **Unity: Import a mesh with LOD settings** — tipo: documentação. URL: https://docs.unity3d.com/Manual/importing-lod-meshes.html
- **Unity for Technical Artists** — tipo: e-book. URL: https://80.lv/articles/unity-released-a-free-book-for-technical-artists
- **Catlike Coding** (shaders) — tipo: site/tutoriais. URL: https://catlikecoding.com/unity/tutorials/ (hiperlink dado na seção 13)

## Pipeline solo enxuto (p. 32)
Pra um primeiro personagem jogável, dá pra pular etapas sem perder muito:
- Estilo low-poly ou estilizado: modele direto o low-poly e pule escultura e bake (etapas 3 e 4b).
- Texturas simples: cores chapadas ou pintadas à mão no lugar de PBR completo.
- Rig automático: Rigify, AccuRig ou Mixamo pra testar rápido.
- Animações prontas pra testar o jogo, trocando depois pelas suas.

---

# 17. Resumo: o que priorizar sendo solo (p. 32-33)

Pra um dev solo com foco num pacote de animação pra Unity, quatro áreas têm prioridade alta: Liderança, Design, Animação e Engenharia.

| Área | Prioridade | Por quê |
|---|---|---|
| 1. Liderança | Alta | Produção e escopo definem se o projeto termina |
| 2. Design | Alta | É o que torna o jogo ou o pacote útil |
| 3. Arte 3D | Média | Dá pra comprar ou reaproveitar no começo |
| 4. Animação | Alta | É o centro do pacote |
| 5. Cinematics | Baixa | Caro, dá pra cortar |
| 6. Engenharia | Alta | Ferramentas de editor e sistemas |
| 7. Áudio | Média | Som pronto + áudio nativo da engine |
| 8. Apoio | Média | Marketing desde cedo, QA com amigos |

## Ordem de estudo da liderança (p. 33)
1. Produtor primeiro: é o que mais faz projeto solo terminar.
2. Diretor criativo (pilares e escopo) junto com o primeiro.
3. A área técnica ou artística que você mais curte (provavelmente animação).
4. O básico das outras, o suficiente pra tomar decisões.

Um jogo pequeno terminado ensina mais do que um jogo grande abandonado.

---

## Índice de referências por área e subtópico

(URL = hiperlink do PDF; "(não informada no PDF)" quando só o nome é citado; domínios sem hiperlink aparecem como no texto.)

| Área | Subtópico | Referência | Tipo | URL |
|---|---|---|---|---|
| Geral (seção 7) | Documentários | Arcane: Bridging the Rift | documentário | https://www.gamedeveloper.com/press-release/arcane-the-first-episode-of-bridging-the-rift-is-now-available |
| Geral (seção 7) | Documentários | PsychOdyssey (Double Fine) | canal YouTube | (não informada no PDF) |
| Geral (seção 7) | Documentários | Noclip | canal YouTube | (não informada no PDF) |
| Geral (seção 7) | Documentários | GDC Classic Postmortems | palestras | (não informada no PDF) |
| Geral (seção 7) | Cursos e aulas | Pixar in a Box | curso | https://pixar.com/pixar-in-a-box |
| Geral (seção 7) | Cursos e aulas | Cursos gratuitos da Epic Developer Community | curso | https://www.unrealengine.com/news/free-professional-unreal-engine-courses-now-available-on-the-epic-developer-community |
| Geral (seção 7) | Cursos e aulas | Unity Learn | curso | (não informada no PDF) |
| Geral (seção 7) | Cursos e aulas | CS50's Introduction to Game Development | curso | (não informada no PDF) |
| Geral (seção 7) | Livros e documentos | Game Programming Patterns | livro online | https://gameprogrammingpatterns.com/contents.html |
| Geral (seção 7) | Livros e documentos | Guia do Scrum em português | documento PDF | https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR-3.0.pdf |
| Geral (seção 7) | Livros e documentos | gameanim.com (rig AZRI) | site | https://www.gameanim.com/ |
| Geral (seção 7) | Livros e documentos | Gurney Journey (James Gurney) | blog | (não informada no PDF) |
| Geral (seção 7) | Livros e documentos | The Door Problem (lizengland.com) | texto | (não informada no PDF; só o domínio lizengland.com no texto) |
| Geral (seção 7) | Livros e documentos | Templates de GDD (Notion, itch.io) | templates | (não informada no PDF) |
| Geral (seção 7) | Palestras | GDC Vault (gratuitas) | arquivo de palestras | https://gdconf.com/gdc-vault |
| Geral (seção 7) | Canais por cargo | Game Maker's Toolkit, Masahiro Sakurai on Creating Games, Design Doc, GDC, PsychOdyssey, Fortiche/Arcane docs, Proko, Blender Studio, Unreal Engine, Unity, Sebastian Lague, Acerola, Alan Becker, New Masters Academy | canais YouTube | (não informada no PDF) |
| Geral (seção 7) | Lado série | Blender Studio (curtas Sprite Fright, Charge, Wing It!) | canal/curtas | (não informada no PDF) |
| Geral (seção 7) | Brasil | Criar Jogos | curso | https://catracalivre.com.br/educacao/curso-gratuito-de-como-criar-games-oferece-800-vagas/ |
| Geral (seção 7) | Brasil | SENAC e Unity Learn | cursos | https://guiadoscursos.com/cursos-gratuitos-games-2026-unity-senac-certificado/ |
| Geral (seção 7) | Brasil | Abragames, BIG Festival, gamescom latam | eventos | (não informada no PDF) |
| Geral (seção 7) | Brasil | Marco Legal dos Jogos / Rouanet Games | notícia/legislação | https://www.educamaisbrasil.com.br/educacao/noticias/marco-legal-dos-jogos-eletronicos-e-regulamentado-no-brasil |
| Liderança | Diretor criativo | A Arte de Game Design (Jesse Schell) | livro | (não informada no PDF) |
| Liderança | Diretor criativo | Criatividade S.A. (Ed Catmull) | livro | (não informada no PDF) |
| Liderança | Diretor criativo | Game Maker's Toolkit | canal YouTube | (não informada no PDF) |
| Liderança | Diretor criativo | Masahiro Sakurai on Creating Games | canal YouTube | (não informada no PDF) |
| Liderança | Diretor criativo | Noclip | canal YouTube | (não informada no PDF) |
| Liderança | Produtor | The Game Production Toolbox (Heather Chandler) / Manual de Produção de Jogos Digitais | livro | (não informada no PDF) |
| Liderança | Produtor | Agile Game Development (Clinton Keith) | livro | (não informada no PDF) |
| Liderança | Produtor | Advanced Agile Game Development Practices | palestra GDC Vault | https://gdcvault.com/free/gdc-17/?&media=as |
| Liderança | Produtor | Sangue, Suor e Pixels (Jason Schreier) | livro | (não informada no PDF) |
| Liderança | Produtor | Guia do Scrum em português | documento PDF | https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-PortugueseBR-3.0.pdf |
| Liderança | Produtor | Atlassian Agile Coach | site | atlassian.com/agile (sem hiperlink) |
| Liderança | Produtor | Postmortems no Game Developer | site | gamedeveloper.com (sem hiperlink) |
| Liderança | Diretor de arte | Color and Light (James Gurney) | livro | (não informada no PDF) |
| Liderança | Diretor de arte | Gurney Journey | blog | (não informada no PDF) |
| Liderança | Diretor de arte | Framed Ink (Marcos Mateu-Mestre) | livro | (não informada no PDF) |
| Liderança | Diretor de arte | Palestra de direção de arte de Diablo 2: Resurrected (GDC Vault) | palestra | https://gdcvault.com/free/?&media=v |
| Liderança | Diretor de arte | Palestra de direção de arte de Street Fighter V (GDC Vault) | palestra | https://gdcvault.com/free/gdc-17/?&media=as [possível mismatch] |
| Liderança | Diretor de arte | Arcane: Bridging the Rift | documentário | (ver seção 7) |
| Liderança | Diretor de arte | Breakdowns no 80.lv | site | (não informada no PDF) |
| Liderança | Diretor técnico | Game Programming Patterns | livro online | https://gameprogrammingpatterns.com/contents.html |
| Liderança | Diretor técnico | Game Engine Architecture (Jason Gregory) | livro | (não informada no PDF) |
| Liderança | Diretor técnico | Cursos gratuitos de Unreal | curso | https://www.unrealengine.com/news/free-professional-unreal-engine-courses-now-available-on-the-epic-developer-community |
| Liderança | Diretor técnico | Unity Learn | curso | (não informada no PDF) |
| Liderança | Diretor técnico | CS50 Game Development | curso | (não informada no PDF) |
| Liderança | Diretor técnico | Catlike Coding | site | (ver Engenharia: https://catlikecoding.com/unity/tutorials/) |
| Liderança | Diretor técnico | Red Blob Games | site | (ver Engenharia: https://www.redblobgames.com/pathfinding/) |
| Liderança | Diretor técnico | LearnOpenGL | site | (ver Engenharia: https://learnopengl.com/) |
| Liderança | Diretor técnico | GPU Gems (NVIDIA) | livro online | (não informada no PDF) |
| Liderança | Diretor de animação | The Animator's Survival Kit / Manual de Animação (Richard Williams) | livro | (não informada no PDF) |
| Liderança | Diretor de animação | Game Anim (Jonathan Cooper) | livro | https://www.routledge.com/Game-Anim-Video-Game-Animation-Explained/Cooper/p/book/9780367707651 |
| Liderança | Diretor de animação | Conteúdo gratuito da Epic sobre State Machines e Motion Matching | conteúdo | https://www.unrealengine.com/learning/januarys-epic-learning-content-nanite-metahuman-pcg-and-more |
| Liderança | Diretor de animação | The Orange Duck | blog | theorangeduck.com (sem hiperlink) |
| Liderança | Diretor de animação | Alan Becker | canal YouTube | (não informada no PDF) |
| Liderança | Diretor de animação | Animation Mentor | curso pago | (não informada no PDF) |
| Liderança | Diretor de animação | iAnimate | curso pago | (não informada no PDF) |
| Design | Game designer | Game Design Concepts (Ian Schreiber) | curso em blog | https://www.gbgames.com/2010/07/05/free-game-design-course-game-balance-concepts/ [possível mismatch] |
| Design | Game designer | Game Balance Concepts (Ian Schreiber) | curso em blog | (hiperlink não separado; ver linha acima) |
| Design | Game designer | Lost Garden (Daniel Cook) | blog | (não informada no PDF) |
| Design | Game designer | raphkoster.com | blog | raphkoster.com (sem hiperlink) |
| Design | Game designer | Game Developer, seção Design | site | gamedeveloper.com (sem hiperlink) |
| Design | Combat designer | Sirlin.net / Playing to Win (David Sirlin) | livro online | https://www.sirlin.net/ptw |
| Design | Combat designer | Combat System Design (Evozon) | artigo | https://www.evozon.com/combat-system-design/ |
| Design | Combat designer | Anatomy of a Successful Attack (Ben Ruiz) | artigo | (não informada no PDF) |
| Design | Combat designer | Série de Bart Vossen no Game Developer | artigos | https://gamedeveloper.com/design/enemy-design-and-enemy-ai-for-melee-combat-systems |
| Design | Combat designer | Game Combat Design Guide | guia | https://gamedesignskills.com/game-design/combat-design/ |
| Design | Level designer | The Level Design Book (Robert Yang) | livro online | https://book.leveldesignbook.com/ |
| Design | Level designer | E-book de level design da Unity | e-book | https://unity.com/resources/introduction-to-level-design-in-game-development-and-in-unity |
| Design | Level designer | Cyberpunk 2077 Quest Design Wiki (Level design 101) | wiki | https://cyberpunk-2077-quest-design.gitbook.io/cyberpunk-2077-design-wiki/generic-game-design/design-basics/level-design-101 |
| Design | Narrative designer / roteirista | Emily Short's Interactive Storytelling | blog | https://emshort.blog/self-training-in-narrative-design |
| Design | Narrative designer / roteirista | Tutorial do ink (inkle) | tutorial | https://www.inklestudios.com/ink/web-tutorial/ |
| Design | Narrative designer / roteirista | Documentação do Twine | documentação | (não informada no PDF) |
| Design | Narrative designer / roteirista | Documentação do Yarn Spinner | documentação | (não informada no PDF) |
| Design | UX/UI designer | Game UI Database | banco de referências | https://gamefromscratch.com/the-game-ui-database/ [possível mismatch; texto cita gameuidatabase.com] |
| Design | UX/UI designer | Blog da Celia Hodent | blog | celiahodent.com (sem hiperlink) |
| Design | UX/UI designer | Game Accessibility Guidelines | site | gameaccessibilityguidelines.com (sem hiperlink) |
| Design | UX/UI designer | Laws of UX | site | lawsofux.com (sem hiperlink) |
| Arte 3D | Base (todos os cargos) | Manual do Blender | documentação | docs.blender.org (sem hiperlink) |
| Arte 3D | Concept artist | Drawabox | curso | https://drawabox.com/ |
| Arte 3D | Concept artist | Gurney Journey | blog | (não informada no PDF) |
| Arte 3D | Character artist | 80.lv (breakdowns de personagens) | site | (não informada no PDF) |
| Arte 3D | Character artist | Polycount | fórum/wiki | (não informada no PDF) |
| Arte 3D | Character artist | Manual do Blender (Sculpt Mode, Retopology) | documentação | (não informada no PDF) |
| Arte 3D | Environment artist | 80.lv | site | (não informada no PDF) |
| Arte 3D | Environment artist | Game Art Tricks | artigo/vídeo | https://simonschreibt.de/game-art-tricks/ |
| Arte 3D | Environment artist | The Level Design Book | livro online | https://book.leveldesignbook.com/ |
| Arte 3D | Props / hard-surface artist | Polycount (hard surface e normals) | fórum | (não informada no PDF) |
| Arte 3D | Props / hard-surface artist | 80.lv | site | (não informada no PDF) |
| Arte 3D | Props / hard-surface artist | Manual do Blender (Bevel, Boolean, Weighted Normal) | documentação | (não informada no PDF) |
| Arte 3D | Texture / material artist | The PBR Guide (Adobe/Allegorithmic) | guia | https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2 |
| Arte 3D | Texture / material artist | Documentação do Substance | documentação | (não informada no PDF) |
| Arte 3D | Lighting artist | Guia de iluminação HDRP da Unity | e-book | https://unity.com/resources/lighting-hdrp-guide |
| Arte 3D | Lighting artist | Documentação de iluminação da Unreal (Lumen, pós-processamento) | documentação | (não informada no PDF) |
| Arte 3D | Lighting artist | Gurney Journey | blog | (não informada no PDF) |
| Arte 3D | VFX artist | RealTimeVFX | comunidade | https://realtimevfx.com/t/getting-started-in-real-time-vfx-start-here |
| Arte 3D | VFX artist | E-book de VFX da Unity (Unity 6) | e-book | https://unity.com/resources/creating-advanced-vfx-unity6 |
| Arte 3D | VFX artist | Game Art Tricks | artigo/vídeo | https://simonschreibt.de/game-art-tricks/ |
| Arte 3D | Technical artist (TD) | The Book of Shaders | livro online | https://thebookofshaders.com/ |
| Arte 3D | Technical artist (TD) | Unity for Technical Artists | e-book | https://80.lv/articles/unity-released-a-free-book-for-technical-artists |
| Arte 3D | Technical artist (TD) | Game Art Tricks (palestra RenderDoc e NSight) | palestra | https://simonschreibt.de/game-art-tricks/ |
| Arte 3D | Technical artist (TD) | Catlike Coding | site | https://catlikecoding.com/unity/tutorials/ |
| Arte 3D | Technical artist (TD) | Riot Tech Blog | blog | technology.riotgames.com (sem hiperlink) |
| Animação | Rigger | Manual do Blender (Armatures, Rigging, Rigify) | documentação | (não informada no PDF) |
| Animação | Rigger | Unity Animation Rigging | documentação | https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html |
| Animação | Rigger | gameanim.com (rig AZRI) | site/rig | https://www.gameanim.com/ |
| Animação | Animador de gameplay | Os 12 princípios da animação em jogos | artigo | https://www.gamedeveloper.com/production/the-12-principles-of-animation-in-video-games |
| Animação | Animador de gameplay | Blog gameanim.com (Jonathan Cooper) | blog | https://www.gameanim.com/page/7/ |
| Animação | Animador de cinematic | gameanim.com: The Cinematography of God of War | artigo | https://www.gameanim.com/page/4/ |
| Animação | Animador de cinematic | Blog da StudioBinder | blog | (não informada no PDF; ver Cinematics) |
| Animação | Animador de cinematic | Documentação do Sequencer / Timeline | documentação | (não informada neste trecho; ver Cinematics) |
| Animação | Animador de cinematic | 11 Second Club | desafio | (não informada no PDF) |
| Animação | Mocap + cleanup | CMU Graphics Lab Motion Capture Database | banco de dados | https://mocap.cs.cmu.edu/resources.php |
| Animação | Mocap + cleanup | CMU Mocap versão FBX | dataset | https://data.4tu.nl/datasets/0448aab2-3332-449f-a8e2-d208cb58c7df |
| Animação | Mocap + cleanup | Licença do CMU (hiperlink) | dataset/licença | https://paperswithcode.com/dataset/cmu-motion-capture |
| Animação | Mocap + cleanup | Documentação de retargeting do Blender / Unity (Humanoid) / Unreal (IK Retargeter) | documentação | (não informada no PDF) |
| Animação | Animação facial | FACS na Wikipedia | enciclopédia | https://en.wikipedia.org/wiki/Facial_Action_Coding_System |
| Animação | Animação facial | iMotions: FACS Visual Guidebook | guia/blog | https://imotions.com/blog/facial-expression-pictures/ |
| Animação | Animação facial | Manual do Blender (Shape Keys) | documentação | (não informada no PDF) |
| Animação | Animation TD / programmer | The Orange Duck (Daniel Holden) | blog | theorangeduck.com (sem hiperlink) |
| Animação | Animation TD / programmer | Motion Matching na Unreal | documentação | https://dev.epicgames.com/documentation/unreal-engine/motion-matching-in-unreal-engine |
| Animação | Animation TD / programmer | Game Animation Sample Project (Epic) | projeto de exemplo | https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8 |
| Animação | Animation TD / programmer | Documentação de animação da Unity (Animator, Blend Trees, Humanoid) | documentação | (não informada no PDF) |
| Animação | Animation TD / programmer | Unity Animation Rigging | documentação | https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html |
| Animação | Cloth / hair / physics | Manual do Blender (Cloth, Hair) | documentação | (não informada no PDF) |
| Animação | Cloth / hair / physics | Documentação da Unity (Cloth, Ragdoll Wizard, Joints) | documentação | (não informada no PDF) |
| Animação | Cloth / hair / physics | Documentação da Unreal (Chaos Cloth, Physics Asset) | documentação | (não informada no PDF) |
| Animação | Cloth / hair / physics | Damped Transform (Unity Animation Rigging) | documentação | https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html |
| Cinematics | Diretor de cinematic | gameanim.com: The Cinematography of God of War | artigo | https://www.gameanim.com/page/4/ |
| Cinematics | Diretor de cinematic | Virtual Production Field Guide (Epic), vol. 1 | PDF | https://www.cartoonbrew.com/tech/epic-games-has-created-the-ultimate-guide-to-virtual-production-177529.html |
| Cinematics | Diretor de cinematic | Virtual Production Field Guide, vol. 2 | PDF | https://www.cgchannel.com/tag/vpfg |
| Cinematics | Layout / câmera | StudioBinder: Ultimate Guide to Camera Shots | guia | https://studiobinder.com/blog/ultimate-guide-to-camera-shots/ |
| Cinematics | Layout / câmera | Documentação de cinematics da Unreal (Cine Camera Actor) | documentação | https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematics-and-movie-making-in-unreal-engine |
| Cinematics | Layout / câmera | Documentação do Cinemachine | documentação | (não informada no PDF) |
| Cinematics | Animador de cena | (remete a Animação > Animador de cinematic; sem fontes próprias) | n/a | n/a |
| Cinematics | Editor | StudioBinder: The Rule of Six | artigo | https://www.studiobinder.com/blog/walter-murch-rule-of-six/ |
| Cinematics | Editor | The Walter Murch-opedia | artigo | https://jonnyelwyn.co.uk/film-and-video-editing/the-walter-murch-opedia/ |
| Cinematics | Editor | Sequencer (Unreal) | documentação | https://dev.epicgames.com/documentation/unreal-engine/using-cinematics-and-sequencer-in-unreal-engine-for-maya-users |
| Cinematics | Editor | Documentação do Timeline (Unity) | documentação | (não informada no PDF) |
| Cinematics | Luz e comp | RedShark News (pipeline da Fortiche) | artigo | https://redsharknews.com/why-netflixs-arcane-looks-so-good-how-fortiche-ramped-up-the-animation-pipeline |
| Cinematics | Luz e comp | 80.lv: Arcane, arte tradicional + 3D nos fundos | artigo | https://80.lv/articles/arcane-artists-show-how-they-combine-traditional-art-3d-for-backgrounds |
| Cinematics | Luz e comp | 80.lv: Ekko em Substance e Blender | artigo | https://80.lv/articles/3d-artist-recreates-arcane-s-ekko-with-substance-3d-blender |
| Cinematics | Luz e comp | Tese "Creating Fortiche-Inspired Environment" | tese PDF | https://reposit.haw-hamburg.de/bitstream/20.500.12738/16175/1/MA_Creating_Fortiche-Inspired_Environment.pdf |
| Cinematics | Luz e comp | Manual do Blender (Compositor) | documentação | (não informada no PDF) |
| Cinematics | Luz e comp | Post Process da Unreal e da Unity | documentação | (não informada no PDF) |
| Engenharia | Base (todos os cargos) | Documentação da Microsoft para C# | documentação | learn.microsoft.com (sem hiperlink) |
| Engenharia | Base (todos os cargos) | learncpp.com | site | https://learnopengl.com/Introduction [possível mismatch; texto cita learncpp.com] |
| Engenharia | Base (todos os cargos) | Pro Git | livro online | git-scm.com/book (sem hiperlink) |
| Engenharia | Gameplay programmer | Game Programming Patterns (Game Loop, State, Component, Observer) | livro online | https://gameprogrammingpatterns.com/contents.html |
| Engenharia | Gameplay programmer | Catlike Coding (Basics e Movement) | site | https://catlikecoding.com/unity/tutorials/ |
| Engenharia | Gameplay programmer | Fix Your Timestep! (Gaffer On Games) | artigo | https://gafferongames.com/post/fix_your_timestep/ |
| Engenharia | Engine / graphics programmer | LearnOpenGL | livro online | https://learnopengl.com/ |
| Engenharia | Engine / graphics programmer | The Book of Shaders | livro online | https://thebookofshaders.com/ |
| Engenharia | Engine / graphics programmer | Catlike Coding (Rendering, Advanced Rendering) | site | https://catlikecoding.com/unity/tutorials/ |
| Engenharia | Engine / graphics programmer | Real-Time Rendering (lista de livros gratuitos) | livros | https://www.realtimerendering.com/books.html |
| Engenharia | AI programmer | Red Blob Games (A*, BFS, Dijkstra) | site | https://www.redblobgames.com/pathfinding/ |
| Engenharia | AI programmer | Red Blob Games: implementação Python/C++ | código | https://redblobgames.com/pathfinding/a-star/implementation.html |
| Engenharia | AI programmer | Game AI Pro | livro online | https://www.gameaipro.com/ |
| Engenharia | AI programmer | Pathfinding Demystified (Gabriel Gambetta) | artigo | https://gabrielgambetta.com/path1.html |
| Engenharia | Tools programmer | Documentação de Editor Scripting da Unity | documentação | (não informada no PDF) |
| Engenharia | Tools programmer | Documentação da API Python do Blender | documentação | docs.blender.org/api (sem hiperlink) |
| Engenharia | Tools programmer | Unity for Technical Artists | e-book | https://80.lv/articles/unity-released-a-free-book-for-technical-artists |
| Engenharia | Network programmer | Fast-Paced Multiplayer (Gabriel Gambetta) | artigo/série | https://www.gabrielgambetta.com/client-server-game-architecture.html |
| Engenharia | Network programmer | Gaffer On Games | blog | https://gafferongames.com/post/ |
| Engenharia | Build engineer / DevOps | Pro Git | livro online | git-scm.com/book (sem hiperlink) |
| Engenharia | Build engineer / DevOps | GameCI | CI open source | https://github.com/game-ci |
| Engenharia | Build engineer / DevOps | GameCI 1: Intro to GitHub Actions for Unity | tutorial | https://davidmfinol.github.io/gameci-1_intro.html |
| Áudio | Sound designer | Designing Sound | blog | https://designingsound.org/ |
| Áudio | Sound designer | Guia de som de armas de Chuck Russom | artigo | https://cdm.link/?p=10910 [possível mismatch] |
| Áudio | Sound designer | Entrevista com Ben Minto (Designing Sound) | entrevista | (não informada no PDF) |
| Áudio | Sound designer | freesound.org | banco de sons | freesound.org (sem hiperlink) |
| Áudio | Sound designer | Pacote anual gratuito da Sonniss | banco de sons | (não informada no PDF) |
| Áudio | Compositor | musictheory.net | lições interativas | musictheory.net (sem hiperlink) |
| Áudio | Compositor | Wwise-201 | certificação/curso | https://www.audiokinetic.com/courses/wwise201 |
| Áudio | Compositor | Material gratuito do Wwise-201 | material | https://thesoundarchitect.co.uk/?p=16784 |
| Áudio | Compositor | Wwise-201 certification (300+ páginas) | material | https://www.cras.edu/wwise-201-certification-video-games/ |
| Áudio | Dublagem (voice over) | Designing Sound (gravação e diálogo) | blog | https://designingsound.org/ |
| Áudio | Dublagem (voice over) | IGDA Best Practices for Game Localization | PDF/guia | https://www.igda.org/resources/best-practices/ |
| Áudio | Audio programmer | Wwise-101 | curso | https://www.audiokinetic.com/courses/wwise101 |
| Áudio | Audio programmer | FMOD | middleware | https://fmod.com/studio |
| Áudio | Audio programmer | FMOD licensing | licenciamento | https://fmod.com/licensing |
| Áudio | Audio programmer | Designing Sound: Learning Audio Middleware Online | artigo | https://designingsound.org/2015/01/26/learning-audio-middleware-online-where-to-start/ |
| Apoio | QA (testes) | Sloperama FAQ 75: How To Write A Game Bug Report | artigo | https://sloperama.com/advice/faq75.html |
| Apoio | QA (testes) | Bugnet: How to write good bug reports | artigo | https://bugnet.io/blog/how-to-write-good-bug-reports-for-game-development |
| Apoio | QA (testes) | Kelina Cowell: Bug Reports Developers Don't Ignore | artigo | https://kelinacowellqa.github.io/Manual-QA-Portfolio-Kelina-Cowell/articles/how-to-write-bug-reports.html |
| Apoio | Localização | IGDA: Best Practices for Game Localization | PDF | https://www.igda.org/resources/best-practices/ |
| Apoio | Localização | Game Developer: 9 game localization best practices | artigo | https://gamedeveloper.com/production/9-game-localization-best-practices |
| Apoio | Localização | Pacote Localization da Unity | documentação | (não informada no PDF) |
| Apoio | Marketing / comunidade / publisher | How To Market A Game (Chris Zukowski) | blog | https://unitycodemonkey.com/howtomarketagame.php [possível mismatch] |
| Apoio | Marketing / comunidade / publisher | Dica de marketing indie (hiperlink sobre "a primeira decisão de marketing...") | artigo | https://unity.com/vn/blog/tips-strategies-for-marketing-indie-games |
| Apoio | Marketing / comunidade / publisher | Hiperlink sobre "mais de 150 wishlists nas primeiras 2 semanas" | artigo | https://medium.com/@info_46369/how-my-first-game-got-700-wishlists-in-its-first-2-weeks-fe7190b4791e |
| Apoio | Marketing / comunidade / publisher | Documentação do Steamworks | documentação | partner.steamgames.com/doc (sem hiperlink) |
| Apoio | Marketing / comunidade / publisher | Documentação de publisher da Unity Asset Store | documentação | (não informada no PDF) |
| Pipeline de personagem | Referência geral | 3D Artist's Handbook | wiki GitHub | https://sidney-eliot.github.io/3d-artists-handbook/theory/topology-and-retopology |
| Pipeline de personagem | Etapa 1: Concept | Drawabox | curso | https://drawabox.com/ |
| Pipeline de personagem | Etapa 1: Concept | Gurney Journey | blog | (não informada no PDF) |
| Pipeline de personagem | Etapa 2: Blockout | Manual do Blender (Modeling) | documentação | (não informada no PDF) |
| Pipeline de personagem | Etapa 2: Blockout | Breakdowns de personagens no 80.lv | site | (não informada no PDF) |
| Pipeline de personagem | Etapa 3: Escultura | Manual do Blender (Sculpting) | documentação | (não informada no PDF) |
| Pipeline de personagem | Etapa 3: Escultura | Blender Studio: Stylized Character Workflow | curso | https://studio.blender.org/training/stylized-character-workflow/5e5406a786994e6b58c7e54b |
| Pipeline de personagem | Etapa 3: Escultura | 80.lv | site | (não informada no PDF) |
| Pipeline de personagem | Etapa 4a: Retopologia | Blender Studio: Live Retopology | post | https://studio.blender.org/blog/live-retopology-at-bcon22 |
| Pipeline de personagem | Etapa 4a: Retopologia | Guia de topologia de Michael VL | wiki | https://michael-vl.github.io/learning-wiki/blender/topology/ |
| Pipeline de personagem | Etapa 4a: Retopologia | 3D Artist's Handbook: topologia | wiki | https://sidney-eliot.github.io/3d-artists-handbook/theory/topology-and-retopology |
| Pipeline de personagem | Etapa 4a: Retopologia | Manual do Blender (Retopology) | documentação | (não informada no PDF) |
| Pipeline de personagem | Etapa 4a: Retopologia | Hiperlinks de apoio no texto (Wikipedia Retopology) | enciclopédia | https://en.wikipedia.org/wiki/Retopology |
| Pipeline de personagem | Etapa 4a: Retopologia | Hiperlinks de apoio no texto (ZBrush docs Retopo) | documentação | https://help.maxon.net/zbr/en-us/Content/html/user-guide/3d-modeling/topology/Retopo/01-retopo.html |
| Pipeline de personagem | Etapa 4b: UV e bake | Manual do Blender: Seams | documentação | https://www.blender.org/manual/en/modeling/meshes/uv/unwrapping/seams.html |
| Pipeline de personagem | Etapa 4b: UV e bake | The Toolbag Baking Tutorial (Marmoset) | tutorial | https://www.marmoset.co/posts/toolbag-baking-tutorial/ |
| Pipeline de personagem | Etapa 4b: UV e bake | This is normal 2: Baking normal maps | artigo | https://typhen.artstation.com/blog/BDr6/this-is-normal-2-baking-normal-maps |
| Pipeline de personagem | Etapa 4b: UV e bake | Baking Maps for Games Reading List | lista de leituras | https://camille_meehan.artstation.com/blog/LYbj/baking-maps-for-games-reading-list |
| Pipeline de personagem | Etapa 5: Texturas | The PBR Guide | guia | https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2 |
| Pipeline de personagem | Etapa 5: Texturas | 80.lv: Ekko estilo Arcane em Substance e Blender | artigo | https://80.lv/articles/3d-artist-recreates-arcane-s-ekko-with-substance-3d-blender |
| Pipeline de personagem | Etapa 6: Rig e skinning | Manual do Blender (Rigging, Rigify) | documentação | (não informada no PDF) |
| Pipeline de personagem | Etapa 6: Rig e skinning | Unity Animation Rigging | documentação | https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.0/manual/index.html |
| Pipeline de personagem | Etapa 6: Rig e skinning | Rig AZRI (gameanim.com) | rig | https://www.gameanim.com/ |
| Pipeline de personagem | Etapa 7: Animação | Os 12 princípios em jogos | artigo | https://www.gamedeveloper.com/production/the-12-principles-of-animation-in-video-games |
| Pipeline de personagem | Etapa 7: Animação | CMU Mocap | banco de dados | https://mocap.cs.cmu.edu/resources.php |
| Pipeline de personagem | Etapa 7: Animação | gameanim.com | site | https://www.gameanim.com/ |
| Pipeline de personagem | Etapa 8: Engine | Unity: Importing Models | documentação | https://docs.unity3d.com/es/current/Manual/ImportingModelFiles.html |
| Pipeline de personagem | Etapa 8: Engine | Unity: Import a mesh with LOD settings | documentação | https://docs.unity3d.com/Manual/importing-lod-meshes.html |
| Pipeline de personagem | Etapa 8: Engine | Unity for Technical Artists | e-book | https://80.lv/articles/unity-released-a-free-book-for-technical-artists |
| Pipeline de personagem | Etapa 8: Engine | Catlike Coding (shaders) | site | https://catlikecoding.com/unity/tutorials/ |
