---
title: Vegetação densa no URP sem estourar a GPU
summary: Desenho instanciado de grama e árvores no URP, o que pesou de verdade numa floresta de teste (sombras, árvores completas de perto, SSAO, upscaler temporal) e o que resolveu.
tipo: original
fonte:
autor: openglitch (testes jardim-ao-vento e jardim-realista)
testado_em: Unity 6000.6.10f1, URP 17.6 Forward+, RTX 4050 de notebook, 1080p
---

Notas de um vale de 1 km com cerca de 12 mil árvores e centenas de milhares
de tufos de grama. Os números são de uma máquina e de um projeto: servem para
saber onde olhar, não como regra.

## Grama e flores instanciadas

- `Graphics.RenderMeshPrimitives` com um `StructuredBuffer` de instâncias e um
  `MaterialPropertyBlock` fixo por bloco e por tipo de planta. No shader basta
  `uint instanceID : SV_InstanceID` e o buffer, com alvo 4.5.
- Para rarear com a distância sem estalo: ordene as instâncias de cada bloco
  por um valor aleatório e desenhe só o começo da lista conforme a distância,
  usando no shader a mesma curva para encolher cada instância.
- `RenderMeshInstanced` exige `material.enableInstancing = true` e shader com
  `multi_compile_instancing`.

## Onde estava o custo

Ache o peso desligando um sistema por vez antes de otimizar.

- **Árvores completas de perto e sombras do nível médio** eram o gargalo na
  mata. Usar a malha simplificada só como sombra das árvores próximas e cortar
  a sombra do nível médio depois de cerca de 60 m levou a GPU de 49 ms para
  20 ms.
- **SSAO com normais** obriga a redesenhar toda a vegetação numa passagem
  extra. Desligar o SSAO e reduzir flores e alcance levou 37,8 milhões de
  triângulos e 20,8 ms para 13,6 milhões e 9,6 ms na mesma vista.
- **Luz principal avaliada duas vezes.** Shader próprio que chama a iluminação
  padrão e depois pega a luz principal de novo, para a translucidez, calcula a
  sombra suave duas vezes por pixel. Avaliar uma vez e reaproveitar tirou
  2,1 ms; baixar a qualidade da sombra suave tirou cerca de 1 ms.
- **Flores detalhadas em quantidade** pesaram mais que a grama: dezenas de
  milhares de tufos com centenas de triângulos cada.

## Upscaling: meça antes de adotar

- O upscaler temporal (STP) custou cerca de 6,7 ms de GPU e 2 a 4 ms de CPU
  nessa cena, em qualquer escala. A causa não foi isolada.
- O FSR 1, espacial, a 0,83 de escala com MSAA 2x ficou mais nítido que o
  filtro bilinear a 0,9 e cerca de 0,65 ms mais barato.
- Não tire o MSAA quando as folhas usam recorte por cobertura
  (alpha to coverage): o recorte fica duro.
- Para usar um upscaler temporal, a vegetação animada no shader precisa de uma
  passagem de vetores de movimento calculada com o vento do quadro anterior.

## Armadilhas de API desta versão

- `Object.GetInstanceID()` é erro de compilação: use `GetEntityId`.
- `GameObject.Find` não acha objeto inativo: percorra as raízes da cena.
- Uma feature de SSAO desligada, mas ainda na lista do renderer, quebra o
  pipeline no executável (tela preta), porque os recursos dela são retirados
  do build. Remova a feature ou deixe-a ativa.
- Malha regravada no lugar com `EditorUtility.CopySerialized` muda no asset,
  mas a tela continua com os dados antigos até reabrir o editor. Copie pela
  API da malha (`Clear`, `SetVertices`, `SetUVs`, `SetTriangles`).

## Como conferir

- Meça nos mesmos pontos antes e depois, na resolução alvo.
- Gere o executável e olhe a captura e o log: alguns erros só aparecem lá.
- Depois de regravar uma malha, pinte o atributo novo como cor no shader e
  capture, para confirmar que a GPU recebeu os dados.
