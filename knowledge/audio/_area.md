---
title: Áudio
summary: A área do som do jogo: efeitos, música, vozes e a integração na engine. Jogo sem som bom parece barato.
---

## O que a área faz

Áudio cria e integra tudo o que se ouve no jogo. Reúne quatro funções: sound
designer (efeitos, ambientes, interface), compositor (trilha e música que
reage ao jogo), dublagem (vozes) e audio programmer (integração na engine). O
som dá peso: o mesmo golpe parece fraco ou devastador dependendo do áudio.

É uma das áreas que equipe pequena mais esquece. Também é uma das que mais
mudam a percepção de qualidade com pouco custo.

## Por que entra depois do Design

O Design define as ações do jogo, e cada ação e cada golpe pede som. O game
feel do combate depende do som de impacto. Por isso o Áudio parte da lista de
ações e das cenas já definidas e entrega os eventos sonoros para a Engenharia
integrar.

## Ordem de aprofundamento

1. Sound designer: efeitos e ambientes são o que o jogador mais ouve. Jogue sem
   música, só prestando atenção nos efeitos.
2. Audio programmer: o som precisa tocar na hora certa e com a distância
   certa. Para começar sozinho, o áudio nativo da engine basta.
3. Compositor, quando o jogo pede música que reage ao combate e à exploração.
4. Dublagem, só se o projeto precisa de voz. Muitos jogos pequenos usam só
   efeitos vocais curtos, e isso é um bom corte de escopo.

## Em equipe pequena

Som pronto mais o áudio nativo da engine resolve a maior parte. Cada som
baixado precisa ter a licença conferida, porque bancos gratuitos têm regras
diferentes por som.

## Ligações com outras áreas

- **Design**: a lista de ações e o tom do jogo definem o que precisa de som.
- **Animação**: golpes, passos e recuperações pedem som sincronizado com o
  momento do impacto.
- **Cinematics**: as cenas são sonorizadas com efeitos, ambiente, música e
  falas.
- **Engenharia**: integra os eventos e os parâmetros que o Áudio entrega.
- **Apoio**: QA testa o som; localização cuida das falas em outros idiomas.
