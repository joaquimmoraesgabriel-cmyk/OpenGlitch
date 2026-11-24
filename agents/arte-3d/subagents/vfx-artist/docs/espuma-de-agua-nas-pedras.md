---
title: Espuma de água só em volta das pedras
summary: Por que a espuma guiada por profundidade ou por stencil sai errada num riacho, e como um mapa de distância das pedras gerado na montagem da cena resolve.
tipo: original
fonte:
autor: openglitch (teste jardim-realista)
testado_em: Unity 6000.6.10f1, URP 17.6
---

Espuma convincente aparece onde a pedra fura a água e deixa um rastro rio
abaixo. As duas abordagens mais diretas falham. Visto num teste, numa máquina.

## O que não funciona

- **Só a profundidade da cena.** A profundidade não diz o que é pedra e o que é
  barranco: um degrau de terra é igual a uma pedra. O resultado são linhas
  brancas nas margens e a corredeira inteira branca.
- **Stencil marcado pela pedra.** O stencil só cobre os pixels em que a pedra
  está atrás da água, então a espuma toma a forma da face submersa: placas
  lisas com bordas retas, seguindo o polígono.

## O que funciona: mapa de distância

1. **Na montagem da cena**, gere uma textura vista de cima com a distância até
   a borda das pedras que furam a superfície (topo acima do nível da água e
   base abaixo).
2. **No shader da água**, use o mapa para:
   - um anel de espuma em volta de cada pedra;
   - o rastro, amostrando o mapa um pouco rio acima;
   - uma renda (Voronoi) que corre com a velocidade da água;
   - ruído para quebrar a regularidade.
3. **Dose**: anel fino, renda discreta, opacidade baixa. Anel largo e quase
   opaco com furos regulares parece plástico.

Tamanho de referência: uma textura de 2048 pontos com um canal de 8 bits cobre
um vale de 1 km a 0,5 m por ponto, em cerca de 4 MB.

## Profundidade da água numa rampa

Medir a espessura da água pela diferença de altura entre a superfície e o
fundo zera numa rampa, e a água some. Use a distância até o plano da água ao
longo da normal da superfície, que funciona também em corredeira e cascata.

## Como conferir

- Capture o riacho de cima e de perto: a espuma só pode estar junto às pedras,
  com as margens limpas.
- Capture a garganta ou o trecho mais inclinado: é onde a espuma costuma virar
  faixa branca.
- Meça o custo com a água ligada e desligada na vista mais pesada.
- Tela magenta na captura é erro de compilação do shader. A consulta de
  mensagens do shader só mostra o erro depois que a variante compila:
  renderize uma vez antes de confiar em "sem mensagens".
