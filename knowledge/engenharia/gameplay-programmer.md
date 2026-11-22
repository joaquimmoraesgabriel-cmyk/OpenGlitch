---
title: Gameplay programmer
summary: Programa o que o jogador sente: controle, câmera, combate, pulo, inventário, missões e save.
---

## O que faz

Programa o que o jogador sente ao jogar: controle do personagem, câmera,
combate, pulo, inventário e missões.

## O que entrega

- Controlador do personagem.
- Câmera.
- Combate, vida e dano, armas.
- Inventário e missões.
- Save.
- Ferramentas para os designers ajustarem números sem mexer no código.

## Fundamentos

- **Game loop**: o laço que lê input, atualiza o mundo e desenha. Entender a
  diferença entre update (a cada quadro) e fixed update (passo de tempo fixo,
  usado pela física) evita movimento que muda com o FPS.
- **Componentes, eventos e state machines**: componentes dividem o
  comportamento em peças; eventos desacoplam sistemas; state machines
  organizam os estados do personagem (parado, andando, pulando, atacando) sem
  um monte de flags booleanas.
- **Física de jogo**: rigidbody, colisão e raycast. O ataque com hitbox e a
  câmera que não atravessa parede dependem disso.
- **Feeling**: coyote time (tolerância para pular logo depois de sair da
  borda), input buffering (guardar o comando pedido um instante antes de ser
  possível) e aceleração (como a velocidade sobe e desce). São parâmetros
  ajustados no teste de jogo.

## Como validar

- Existe um controlador de terceira pessoa que anda, corre, pula e esquiva.
- A câmera segue o personagem e não atravessa parede.
- Existe um ataque com hitbox que causa dano onde deveria.
- O movimento tem o mesmo resultado em FPS diferentes.
- Coyote time, input buffering e aceleração são parâmetros que o designer muda
  sem alterar o código, e a mudança aparece no jogo.
- Os sistemas de dano, inventário, missões e save têm testes automáticos.
- Quem joga sem explicação entende o controle e não sente o personagem
  desobediente.

## Ligações com outras áreas

- O Design define as mecânicas e joga os protótipos; o timing é ajustado até o
  controle ficar bom.
- A Animação entrega as animações; as state machines, transições, blends e IK
  são implementadas junto com o animation TD.
- O combat designer fornece os valores de golpe (startup, ativo, recovery, dano).
- O Áudio entrega os sons de impacto que o combate dispara.
- O network programmer adapta o controle quando o jogo é multiplayer.
