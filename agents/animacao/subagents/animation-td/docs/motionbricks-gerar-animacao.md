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

Testado numa máquina: geração a partir de poses próprias, ciclos em loop,
BVH, conversão para FBX, importação Humanoid na Unity e um personagem com
malha (X Bot do Mixamo) andando para a frente, para trás e de lado. Não
testado: movimentos difíceis (golpe, salto, queda). Obstáculos: um caso testado, subir num
bloco de 0,6 m; veja a seção de obstáculos.

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
5. **Gere**: `gerar.py` para um movimento com começo e fim (agachar, pegar
   algo, acenar); `gerar_ciclo.py` para o que se repete (parado, andar). Saem o
   BVH, o contato dos pés, o relatório e a tira de quadros.
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
  zero; `pe_afunda_cm` diz quanto o pé passa do chão; `deriva_por_apoio_cm` diz
  quanto cada ponto do pé anda enquanto deveria estar parado; a velocidade
  máxima denuncia um salto entre quadros.
- **Deslize se mede por altura, não pelo rótulo de contato.** O deslize
  acontece justamente nos quadros que o modelo não rotula como apoio. Andar
  para a frente ficou em 2 a 3 cm por passo na ponta do pé.
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

**O avatar do SOMA precisa vir de uma pose T.** O FBX de uma animação tem
como pose padrão o primeiro quadro dela. Se o avatar for criado a partir desse
arquivo, a Unity toma uma passada como se fosse a pose T: o avatar sai
"válido", nada avisa, e no personagem um pé afunda cerca de 5 cm e o outro não
encosta no chão. O jeito certo:

1. Gere o BVH da pose T: `gerar_ciclo.py --pose-t <pasta>/SOMA_PoseT.bvh`, e
   converta para FBX.
2. Importe esse FBX como Humanoid com `CreateFromThisModel`.
3. Em todo FBX de animação, use `avatarSetup = CopyFromOther` com
   `sourceAvatar` igual ao avatar da pose T.

Se o clipe andar em diagonal, corrija o `rotationOffset` do clipe na
importação até a velocidade média apontar na direção certa. O aviso de que a
rotação de `Neck2` é descartada é esperado: o SOMA tem dois ossos de pescoço e
o Humanoid usa um.

No teste, o avatar saiu válido, com 55 ossos humanoides mapeados sem ajuste
manual, e as posições do quadril, da cabeça e dos pés bateram com o relatório
do gerador. O eixo X vem espelhado, pela troca de mão entre o Blender e a
Unity; é esperado.

Para usar num personagem do jogo, o personagem também precisa ser Humanoid: o
clipe do SOMA toca no avatar dele pelo retargeting da engine. Confira por
captura; perna ou coluna torta costuma ser mapeamento do avatar.

## Ciclos em loop: andar, correr, ficar parado

Para um ciclo use `gerar_ciclo.py`, não `gerar.py`. Um destino de uma pose só
faz o personagem frear em cada destino: no teste a velocidade caía de 1,1 para
0,27 m/s, o tronco inclinava para trás e o pé deslizava 30 cm/s. O que resolve
é o que o próprio runtime do MotionBricks faz:

- **Destino em movimento** (`velocidade_alvo: [vx, vz]` no plano): o destino
  vira quatro poses iguais em que só a raiz avança. O modelo chega andando.
- **Transição antecipada** (`transicao_antecipada`): de cada geração entram só
  os quadros até alguns antes do fim, e a seguinte parte dali. A parte final,
  onde o modelo força a chegada na pose, fica de fora.
- **Duração fixa** (`tokens` em cada destino): quadros gerados = tokens × 4 − 6.
  O mínimo é 6 tokens, 18 quadros.
- **Recorte por período** (`periodo`): o gerador encadeia vários ciclos e
  recorta, da parte estável, o trecho em que o fim mais se parece com o começo.
- **Limpeza da emenda**: fecha o resto da diferença e suaviza só perto das
  emendas. Sem ela, cada emenda de geração tem um tranco de um quadro.
- **Travar os pés** (`travar_pes: true`): prende no chão o ponto apoiado e
  ajusta a perna por IK.

Um ciclo de andar é uma pose-chave só (o contato do calcanhar) repetida a cada
passo duplo. Planos que funcionaram estão em `extras/motionbricks/planos/`:
`Parado`, `AndarFrente`, `AndarTras` e `AndarLado`. Parta deles.

Confira no relatório: a pose na emenda deve fechar em zero depois da limpeza, e
a aceleração na emenda deve ficar igual ou abaixo da do próprio ciclo. Acima
disso há tranco ao recomeçar.

## Andar de lado

O modelo arrasta os pés de lado quando o passo é lento. Com poses de pernas
abertas a 0,45 m/s, os pés nunca saíam do chão e escorregavam 25 a 47 cm por
apoio, em seis variações de pose, de destino e de duração.

O que funciona é um passo lateral apressado: duas poses por ciclo ("abre", com
o pé da frente no ar e aberto, e "fecha", com o de trás no ar vindo fechar), a
cerca de 1,2 m/s, em ciclo de 26 quadros. O pé da frente deriva menos de 1 cm
por apoio e o de trás cerca de 8 cm. O plano é o `AndarLado`.

- **Abaixo de cerca de 1 m/s o pé de trás volta a arrastar.** Para um andar de
  lado mais lento, toque o clipe em velocidade menor na engine em vez de gerar
  devagar.
- **Para o outro lado, espelhe o clipe** na importação Humanoid.
- Passo cruzado, agachado e três poses por ciclo não melhoraram o pé de trás.
- Conferido num personagem com malha (X Bot) na Unity 6: o clipe importou a
  1,2 m/s em linha reta, o espelhado serviu para a direita, e numa blend tree
  2D com parado, frente, trás, esquerda e direita o personagem andou de lado e
  na diagonal. Conferido por posição e por captura de tela, não assistindo: o
  pé de trás que deriva pode aparecer como um leve deslize.

## Obstáculos: subir, pular, apoiar

Testado numa máquina (RTX 4050, Blender 5.3) com oito animações de poses próprias, todas
partindo de parado: subir em bloco de 0,4 m, 0,6 m e 1,0 m (este com as mãos na borda), descer
de um bloco de 0,6 m, saltar um muro de 0,8 m com uma mão, passar por baixo de uma barra a
1,15 m, sentar numa caixa de 0,45 m e levantar dela. Os planos estão em
`extras/motionbricks/planos/obstaculos/` (`fazer.py` os escreve). Não testado: chegar
correndo, obstáculo girado, parede mais alta que o quadril.

O modelo **não enxerga a cena**. Ele só vê as poses pedidas, e o corpo passa por onde o
caminho entre elas for mais natural, inclusive por dentro de uma parede. Não existe
parâmetro que resolva isso; o que resolve é um ciclo de conferir e corrigir.

O que o modelo consegue quando as poses são boas: a cena de exemplo dele (`teste_cena.py`
roda sozinha e grava capturas) sobe numa caixa de 0,4 m, salta um muro de 0,8 m apoiando a
mão e abaixa para passar numa barra. Os Smart Primitives e clipes dessa cena têm licença só
de avaliação: servem para ver o teto de qualidade, não para um jogo.

### O ciclo

1. **Descreva o obstáculo no plano**, em medida real, em `"obstaculos"` (caixas).
2. **Monte as poses contando com ele.** `lugar` põe o quadril no ponto da cena, `altura`
   sobe o quadril, e `alcancar` leva o pé ou a mão ao ponto exato da superfície por IK.
   O tornozelo do esqueleto fica 7,2 cm acima da sola: pé em cima de um bloco de 0,6 m é
   `y = 0.672`.
3. **Confira só as poses**, sem gastar geração: `gerar.py plano.json --so-poses`. Sai um BVH
   com um quadro por pose, a tira com os obstáculos, se alguma pose já nasce dentro de um, e
   `"fora_de_alcance_cm"`: o `alcancar` que não chegou no ponto porque o quadril está alto ou
   longe demais. Corrija antes de gerar: ponta fora de alcance fica no ar, e o `fixar` a prende lá.
4. **Veja no Blender**, de vários ângulos. Sem janela:
   `blender -b -P blender_cena.py -- --plano plano.json --bvh x.poses.bvh --saida pasta`.
   Com o Blender aberto, pelo servidor MCP: monte `sys.argv` do mesmo jeito e chame
   `blender_cena.main()`; a conferência vai para uma cena à parte, `OG_Conferencia`, e nada do
   arquivo aberto é apagado. `--vistas lado,quina,frente,tras,outro_lado,cima` escolhe os
   ângulos e `--zoom 1.5` aproxima a câmera. Se ajustar as poses lá (à mão ou com IK),
   `blender_exportar.py` leva de volta para um plano, com cada pose como posições de juntas.
5. **Gere** e leia o relatório inteiro, não só `"obstaculos"` (tabela abaixo).
6. **Corrija só o destino afetado** e gere de novo. Repita até passar.
7. **Confira a animação no Blender** com o mesmo `blender_cena.py`, agora com o BVH gerado
   e `--quadros` escolhidos. Número sozinho não mostra pose feia: foi olhando a imagem que
   apareceu o pé terminando 10 cm acima do bloco, com penetração 0,0 cm no relatório.

## Obstáculos: o que ler no relatório

| Campo | O que diz | Quando é defeito |
| --- | --- | --- |
| `obstaculos` | Penetração máxima, ossos, quadros e destino | `"passou": false` (mais que 3 cm) |
| `pes_no_apoio` | No primeiro e no último quadro, tornozelo acima do apoio e ponta do pé abaixo dele | `"passou": false`: pé no ar ou torto no fim |
| `fora_de_alcance_cm` | Pose em que o `alcancar` não chegou | Qualquer valor numa junta que depois é fixada |
| `geracoes[].levado` | Quanto faltou para o `levar` chegar | `faltou_cm` acima de 1: o quadril ainda não chegou; encurte o passo |
| `desvios` | Quanto o desvio automático mexeu em cada membro | Dezenas de centímetros: o caminho está errado, corrija a pose |
| `medidas` | Duração, velocidade máxima, pé afundando | Velocidade acima de uns 8 m/s é tranco |

## Obstáculos: sem parar em cada pose

Cada destino de uma pose só é uma parada: o modelo chega nela freando. O plano de exemplo
antigo (`planos/SubirBloco.json`, seis destinos) dura 9,03 s. Com os campos abaixo o mesmo
movimento ficou em 2,80 s, sem atravessar:

| Campo do destino | O que faz |
| --- | --- |
| `"tokens": 6` | Duração da geração: quadros = tokens x 4 - 6 (6 a 16) |
| `"antecipar": 4` | Usa a geração só até 4 quadros antes do fim; a pose vira ponto de passagem |
| `"velocidade": [0, 1.2]` | Destino em movimento: quatro poses com a raiz andando |
| `"levar": ["LeftFoot"]` | Pino de IK: a ponta chega no ponto e na orientação da pose de destino no último quadro usado. Sem isto, com `antecipar`, o pé chega baixo e o `fixar` seguinte o prende ali |
| `"levar_desde": 0.0` | De que fração do trecho o `levar` puxa (padrão 0,5). Com 0 a ponta vai quase em linha reta: use quando o caminho do modelo passa por dentro do obstáculo |

É o que o runtime do MotionBricks faz na cena de exemplo: transição antecipada, várias
poses-alvo e pinos de IK. Valores que funcionaram: 6 a 8 tokens e `antecipar` 3 a 5 por
destino, e o último destino sem `antecipar`, para terminar na pose.

## Obstáculos: desvio automático

Depois de gerar, braços e pernas que ficaram dentro de uma caixa são tirados de lá por IK
(`poses.avoid`): o pé é empurrado para fora, de preferência por cima; o tornozelo sobe; o
joelho gira para fora em volta da linha quadril-tornozelo, que é como uma perna passa por
cima de uma borda. Pé parado no apoio não é levantado. A correção é suavizada no tempo e some
no primeiro e no último quadro. Fecha raspões de pé e de canela na quina. Não mexe em quadril,
tronco nem cabeça: isso é pose. `"desviar": false` desliga.

## Obstáculos: o que corrige cada defeito

| Defeito | Causa | Correção |
| --- | --- | --- |
| Pé de apoio afunda no obstáculo no meio do trecho | O modelo não sabe que o pé está apoiado e o baixa para o chão | `"fixar": ["LeftFoot"]` no destino |
| Ponta do pé corta a quina ao subir | O arco do pé passa pela quina | Pose intermediária com o pé acima e antes da quina; o desvio automático fecha o resto |
| Ponta do pé entra no topo ao descer | O pé aponta para baixo no ar | `"nivelar": ["LeftFoot"]`: guarda a orientação do começo do trecho |
| Salto no fim de um trecho com `fixar` | A pose de destino tem a junta em outro ponto | Ponha a junta fixada no mesmo ponto na pose de destino, e a pose final com os pés onde eles já estão |
| Pé termina no ar (`pes_no_apoio`) | `alcancar` fora de alcance, ou `levar` que não chegou | Baixe o quadril da pose; encurte o passo |
| Pé pousa com a ponta para baixo | `nivelar` sozinho num pé que vinha do ar | `levar` e `nivelar` juntos: parte da orientação do começo e chega na do destino. Se o pé vinha torto do ar, só `levar` |
| Joelho ou canela varre a quina num bloco na altura do quadril | Com o quadril colado na face, a coxa não tem por onde subir de frente | Suba primeiro o corpo nos braços e traga a perna PELO LADO (coxa aberta, joelho já acima do topo), como a perna de trás na barreira |
| Pé avança por baixo do topo do muro e só depois sobe | É o caminho que o modelo escolhe | Deixe o pé acima do topo na pose anterior e use `"levar_desde": 0.0` |
| Cabeça raspa a barra | O agachamento atrasa em relação à pose pedida | Deixe o corpo todo abaixado um passo ANTES da barra (a cabeça vai uns 45 cm à frente do quadril) e só levante depois que o quadril passou |
| Passos escorregando ao andar abaixado | Pose com os dois pés relativos ao quadril | Um destino por passo: `fixar` no pé de apoio, `levar` no pé que avança |
| Perna de trás roça a face do obstáculo | Pose com o pé ou o quadril perto demais | Afaste o pé e recue o quadril na pose daquele destino |

`fixar` não é remendo: a cena de exemplo do próprio MotionBricks aplica IK nas poses-alvo
pelo mesmo motivo.

Folga para a malha: o esqueleto não tem espessura. Para a cabeça, gere também contra uma
barra engrossada em 8 cm de cada lado (`"tamanho"` maior no plano); se passar, o crânio passa.

## Obstáculos: limites do que saiu

- **Tudo parte de parado e termina parado.** São ações inteiras, de 1,6 a 3,1 s. Chegar
  andando ou correndo pede um contexto em movimento e não foi tentado.
- **A folga de 3 cm é do esqueleto**, que não tem espessura. Com malha, pé, canela e coxa
  podem encostar onde o esqueleto passou. Confira com o personagem.
- **Só caixas**, com giro em volta do eixo vertical.
- **A animação vale para aquela altura.** Encaixar num obstáculo de outra altura dentro do
  jogo (detectar, alinhar, esticar) é trabalho na engine e não existe aqui.
- **O desvio automático resolve pé, canela e joelho**, não quadril, tronco, cabeça ou cotovelo.

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
- Poses simples e ciclos de andar para a frente e para trás saíram bem. Andar
  de lado só funciona apressado. Golpe, salto e queda não foram testados.
- Não há animação de virar: girando o personagem pelo controle, os pés deslizam.
- O modelo usa as proporções do esqueleto SOMA.
