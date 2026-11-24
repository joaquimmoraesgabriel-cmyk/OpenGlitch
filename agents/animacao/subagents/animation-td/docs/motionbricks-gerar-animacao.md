---
title: Gerar animação com o MotionBricks (opcional, GPU NVIDIA)
summary: O que o MotionBricks faz e não faz, como planejar poses de destino, o caminho até a Unity pelo BVH e pelo Blender, e os limites de licença dos clipes de exemplo.
tipo: referencia
fonte: https://github.com/NVlabs/motionbricks
autor: openglitch
testado_em: MotionBricks de novembro de 2026, RTX 4050 de notebook (6 GB), Windows, Blender 5.3
---

O MotionBricks é um modelo da NVIDIA que gera o movimento entre poses. No
OpenGlitch ele é um componente opcional: só existe se a pessoa instalou com
`python install.py --motionbricks`, e só roda em GPU NVIDIA. Chame
`motionbricks_info` para saber se está instalado e com que comandos.

O que está aqui vem da documentação oficial. O teste do gerador foi executado
numa máquina: uma caminhada de 3,2 s em duas gerações encadeadas, gravada em
BVH e convertida para FBX, com o esqueleto em pé, os pés no chão e o contato
dos pés alternando. Um plano com posições e giros próprios e a importação na
Unity ainda não foram testados. Rode o teste primeiro.

## O que ele é e o que não é

- **É um gerador de transição.** Recebe quatro poses de contexto (as mais
  recentes do personagem) e de uma a quatro poses de destino, e gera o
  movimento entre elas, a 30 quadros por segundo.
- **Não é texto para movimento.** Não existe "faça o personagem pular". Quem
  dirige decide quais poses de destino, onde e em que ordem.
- **Cada geração é curta**: de 18 a 58 quadros, cerca de 0,6 a 1,9 s. O modelo
  escolhe a duração.
- **Movimento longo é uma cadeia**: os quatro últimos quadros mostrados viram o
  contexto da geração seguinte.
- **Roda fora do jogo.** A geração usa TensorRT na GPU de quem produz. O jogo
  recebe os arquivos de animação prontos.

## De onde vêm as poses de destino

É o ponto que decide a qualidade. As poses precisam vir de algum lugar:

- **De clipes** no esqueleto SOMA: amostra-se um trecho e move-se só a raiz
  para colocá-lo na cena. É o que os exemplos oficiais fazem.
- **De poses próprias**, com o mesmo formato.
- **De outro modelo gerador de poses**, que a documentação cita como caminho
  possível.

Uma pose de destino define onde o personagem chega e para. Duas ou mais também
definem com que velocidade ele chega: use as quatro para o movimento continuar
fluindo, e uma só para ele parar.

## Como planejar

1. Liste os momentos do movimento em ordem (parado, anda, vira, para).
2. Para cada momento, escolha o clipe e o instante de onde sai a pose.
3. Dê a posição no chão e o giro de cada destino. Só a raiz se move; o corpo
   fica como foi amostrado.
4. Mantenha os destinos alcançáveis em até 1,9 s a partir do anterior. Destino
   longe demais dá passo esticado ou deslize.
5. Escreva isso no plano em JSON e rode o gerador.

O formato do plano está no cabeçalho de `extras/motionbricks/gerar.py`.

## Formato da saída

- Esqueleto SOMA, com as 30 juntas que o modelo prevê; a raiz é a primeira.
- Cada pose é uma transformação local por junta: posição XYZ em metros e
  quatérnio XYZW, com Y para cima e o chão em XZ.
- O gerador grava um BVH (centímetros e graus), um arquivo com a confiança de
  contato dos pés por quadro e um relatório com a duração de cada geração.

## Caminho até a Unity

1. **Gerar** o BVH com `gerar.py`, no ambiente do MotionBricks.
2. **Converter** para FBX com `bvh_para_fbx.py`, no Blender em segundo plano.
3. **Importar** na Unity com o rig do tipo Humanoid e conferir o mapeamento dos
   ossos na configuração do avatar.
4. **Aplicar** no personagem: o retargeting Humanoid da Unity leva a animação
   do esqueleto SOMA para o avatar do personagem.

Os passos 3 e 4 não foram testados pelo autor. Um personagem com outro
esqueleto sempre precisa de retargeting, como a documentação do modelo diz.

## Contato dos pés

A saída traz, por quadro, quatro valores de 0 a 1: calcanhar e ponta de cada
pé plantados no chão. Use para travar o pé com IK na engine onde o valor é
alto e tirar o deslize. Clipes carregados de arquivo não têm esse dado; só o
movimento gerado.

## Licenças: leia antes de usar num jogo

- **Código**: Apache 2.0.
- **Modelos**: NVIDIA Open Model Agreement. O repositório diz que permite uso
  comercial, nos termos do acordo. Leia o acordo.
- **Clipes de exemplo**: NVIDIA Sample Data Evaluation License. Só para
  avaliar e testar tecnologia da NVIDIA, em uso interno. Não podem ser
  distribuídos, e as obras derivadas deles também não.

Consequência prática: animação gerada a partir dos clipes de exemplo serve
para testar e aprender, não para entrar num jogo publicado. Para produção,
as poses precisam vir de clipes do próprio usuário ou de outra fonte com
licença adequada. O gerador grava esse aviso junto da saída. Isso não é
orientação jurídica: diga ao usuário para ler as licenças.

## Como conferir

- Rode `gerar.py --teste` antes do plano real. Se falhar, registre o erro com
  `report_problem`: o script só foi validado numa máquina.
- Leia o relatório: quadros por geração e posição da raiz no começo e no fim.
- No Blender, capture o esqueleto no primeiro e no último quadro e veja se
  está em pé e no lugar esperado.
- Na Unity, toque o clipe no avatar e capture: pé deslizando, braço torcido e
  raiz girada são os erros mais comuns do retargeting.

## Limites conhecidos

- A primeira execução de cada modelo monta o plano do TensorRT e leva alguns
  minutos; depois fica em cache.
- Os exemplos oficiais foram testados numa RTX 4090. O teste do OpenGlitch
  rodou numa RTX 4050 de notebook com 6 GB.
- Ocupa disco: cerca de 4,7 GB do repositório, 3,1 GB do ambiente e 0,7 GB do
  cache do TensorRT.
- O esqueleto SOMA carregado tem 77 juntas, com os dedos; o modelo prevê 30
  delas. No BVH, 32 juntas saem com canais de posição além dos de rotação.
- O modelo usa as proporções do esqueleto SOMA.
