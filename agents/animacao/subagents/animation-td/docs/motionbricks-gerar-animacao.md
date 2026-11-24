---
title: Gerar animação com o MotionBricks, do pedido até a Unity (opcional, GPU NVIDIA)
summary: O processo inteiro para criar uma animação com o MotionBricks a partir de poses próprias, conferir, converter para FBX e importar na Unity como Humanoid.
tipo: referencia
fonte: https://github.com/NVlabs/motionbricks
autor: openglitch
testado_em: MotionBricks de novembro de 2026, RTX 4050 de notebook (6 GB), Windows, Blender 5.3, Unity 6000.6.10f1
---

O MotionBricks é um modelo da NVIDIA que gera o movimento entre poses. No
OpenGlitch ele é opcional: só existe se a pessoa instalou com
`python install.py --motionbricks`, e só roda em GPU NVIDIA. Chame
`motionbricks_info` para saber se está instalado e pegar os comandos com os
caminhos desta máquina.

Testado numa máquina: geração a partir de poses próprias, BVH, conversão para
FBX e importação Humanoid na Unity. Não testado: aplicar num personagem com
malha e esqueleto diferente, e movimentos difíceis (golpe, salto, queda).

## O que ele é e o que não é

- **É um gerador de transição.** Recebe quatro poses de contexto (as mais
  recentes do personagem) e de uma a quatro poses de destino, e gera o
  movimento entre elas, a 30 quadros por segundo.
- **Não é texto para movimento.** Não existe "faça o personagem pular". Você
  dirige: decide as poses de destino, onde ficam e em que ordem.
- **Cada geração é curta**, de 0,6 a 1,9 s. Nos testes com uma pose de destino
  saiu sempre 1,67 s.
- **Movimento longo é uma cadeia**: os quatro últimos quadros de uma geração
  viram o contexto da seguinte.
- **Roda fora do jogo.** O jogo recebe os arquivos de animação prontos.

## O processo, do pedido à Unity

1. **Entenda o movimento** com o usuário: o que o personagem faz, quanto dura,
   se sai do lugar, se é loop, em que estado começa e termina.
2. **Quebre em poses-chave**, na ordem. Cada transição entre duas poses é uma
   geração de até 1,9 s. "Agachar e pegar algo do chão" vira: em pé, agachado,
   mão no chão, agachado, em pé.
3. **Veja o esqueleto**: rode o gerador com `--listar-juntas` para ter os nomes
   das juntas e a posição de repouso de cada uma.
4. **Escreva o plano** em JSON, com as poses, o início e os destinos.
5. **Gere** com `gerar.py`. Saem o BVH, o contato dos pés, o relatório e a tira
   de quadros.
6. **Confira** a tira e as medidas, corrija as poses e gere de novo. É normal
   repetir este passo algumas vezes.
7. **Converta** o BVH em FBX com `bvh_para_fbx.py`, no Blender em segundo plano.
8. **Importe na Unity** como Humanoid e confira o avatar e o clipe.
9. **Aplique no personagem** e confira por captura dentro da engine.
10. **Registre** na memória de trabalho o plano usado e onde estão os arquivos.

## Como escrever uma pose

Uma pose é descrita por direções, não por ângulos: "o osso que vai desta junta
até a filha aponta para lá". Espaço do personagem: **+Y para cima, +Z para a
frente, +X para o lado esquerdo dele**. A base é a pose de repouso, em T.

```json
"agachado": {
  "mirar": [
    ["Hips", "Spine1", [0, 1, 0.35]],
    ["LeftLeg", "LeftShin", [0.05, -0.45, 0.89]],
    ["LeftShin", "LeftFoot", [0, -0.8, -0.6]],
    ["RightLeg", "RightShin", [-0.05, -0.45, 0.89]],
    ["RightShin", "RightFoot", [0, -0.8, -0.6]]
  ],
  "pe_plano": ["LeftFoot", "RightFoot"],
  "pes_no_chao": true
}
```

- **`mirar`** é aplicado na ordem escrita. Vá do tronco para as pontas: quadril,
  coxa, canela; depois ombro, braço, antebraço. Mirar o pai depois do filho
  desfaz o filho.
- **O lado direito é o esquerdo com o X trocado de sinal.**
- **`pe_plano`** devolve o pé à orientação de repouso depois de dobrar a perna,
  para a sola ficar no chão.
- **`pes_no_chao`** ajusta a altura do quadril até o pé mais baixo encostar no
  chão. Use em quase toda pose apoiada.
- **`base`** parte de outra pose já definida, para mudar só o que difere.
- **`altura`** soma metros à altura do quadril, para um salto.
- No SOMA a coxa chama `LeftLeg` e a canela `LeftShin`.

Em cada destino, `posicao` é `[x, z]` da raiz no chão e `giro` são graus em
volta do eixo vertical. O início parte do personagem parado na pose dada.

## Erros de pose que aparecem na tira

- **Braço ou perna para o lado errado**: sinal de X ou de Z trocado.
- **Membro torcido**: a direção está certa, mas o osso girou em torno do
  próprio eixo. Mirar não controla esse giro; mude a ordem ou aproxime a
  direção aos poucos, partindo de uma pose base mais próxima.
- **Pé no ar ou enterrado**: faltou `pes_no_chao` ou `pe_plano`.
- **Passo esticado ou deslize**: o destino está longe demais para 1,9 s.
  Ponha um destino intermediário.
- **Braços abrindo no meio do caminho**: duas mudanças grandes ao mesmo tempo
  (andar e baixar os braços, por exemplo). Separe em dois destinos.

## Como conferir

Você não assiste à animação. Seus olhos são a tira de quadros e os números.

- **Abra a tira** (`<nome>.tira.png`): oito quadros por geração, de lado e de
  frente; vermelho é o lado esquerdo, azul o direito. Veja se cada pose final é
  a que você quis e se o caminho até ela faz sentido.
- **Leia o relatório**: `distancia_ate_a_pose_pedida_cm` deve ficar perto de
  zero; `pe_afunda_cm` diz quanto o pé passa do chão; o deslize do pé plantado
  diz se ele escorrega; a velocidade máxima denuncia um salto entre quadros.
- **Referência do teste**: pé afundando 2,3 cm e deslize de 7 a 8 cm/s numa
  sequência de agachar, levantar e andar 1 m. Bem acima disso, revise o plano.
- **O que só o usuário confere**: peso, ritmo e naturalidade, assistindo no
  personagem. Peça isso de forma específica.

## Converter e importar na Unity

Converta com o Blender em segundo plano; o conversor imprime a posição de
algumas juntas no primeiro e no último quadro, para conferir.

Na Unity, importe o FBX como Humanoid por script e leia o resultado:

```csharp
var importer = (ModelImporter)AssetImporter.GetAtPath(path);
importer.animationType = ModelImporterAnimationType.Human;
importer.avatarSetup = ModelImporterAvatarSetup.CreateFromThisModel;
importer.importAnimation = true;
importer.SaveAndReimport();
var avatar = AssetDatabase.LoadAllAssetsAtPath(path).OfType<Avatar>().First();
// avatar.isValid e avatar.isHuman precisam ser verdadeiros
```

No teste, o avatar saiu válido, com 55 ossos humanoides mapeados sem ajuste
manual, e as posições do quadril, da cabeça e dos pés bateram com o relatório
do gerador. O eixo X vem espelhado, pela troca de mão entre o Blender e a
Unity; é esperado.

Para usar num personagem do jogo, o personagem também precisa ser Humanoid: o
clipe do SOMA toca no avatar dele pelo retargeting da engine. Confira por
captura; perna ou coluna torta costuma ser mapeamento do avatar.

## Contato dos pés

A saída traz, por quadro, quatro valores de 0 a 1: calcanhar e ponta de cada
pé plantados no chão. Use para travar o pé com IK na engine onde o valor é alto.

## Licenças: leia antes de usar num jogo

- **Poses próprias do plano**: são do usuário. É o caminho para um jogo ou um
  pacote à venda.
- **Clipes de exemplo do MotionBricks**: licença só de avaliação interna.
  Animação feita a partir deles não pode ser distribuída. O gerador avisa
  quando um plano os usa.
- **Modelos**: NVIDIA Open Model Agreement. O repositório diz que permite uso
  comercial, nos termos do acordo. Diga ao usuário para ler o acordo antes de
  vender o resultado; isto não é orientação jurídica.

## Limites conhecidos

- A primeira execução de cada modelo monta o plano do TensorRT e leva alguns
  minutos; depois fica em cache.
- Ocupa cerca de 8,5 GB de disco.
- Poses simples (agachar, erguer os braços, andar) saíram plausíveis. Golpe,
  salto e queda não foram testados.
- O modelo usa as proporções do esqueleto SOMA.
