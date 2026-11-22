---
title: Tools programmer
summary: Cria ferramentas internas: editores de fase, importadores, janelas na engine e automações.
---

## O que faz

Cria ferramentas internas para acelerar o trabalho da equipe: editores de fase,
importadores, janelas na engine e automações.

## O que entrega

- Extensões do editor: janelas e inspetores na Unity.
- Importação e validação de assets.
- Debug dentro do jogo.
- Plugins para Blender e Maya.

## Fundamentos

- **Editor scripting da Unity**: `EditorWindow` (janelas próprias),
  `CustomEditor` (inspetores personalizados) e `ScriptableObject` (dados do jogo
  guardados como assets, ideais para designers ajustarem números).
- **Python do Blender (bpy)**: automatiza tarefas no Blender e permite
  escrever plugins, por exemplo para renomear malhas ou exportar.
- **UX básico**: uma ferramenta só ajuda se quem não programa consegue usar.
  Mensagem de erro clara, ação de correção e feedback do que foi feito.
- **Valor comercial**: um pacote para a Unity vende muito pela ferramenta de
  editor que vem junto.

## Como validar

- Uma janela na Unity lista todas as animações do projeto e mostra quais estão
  sem configuração.
- A ferramenta funciona num projeto novo, sem ajuste manual.
- Um designer usa a ferramenta sem ler o código.
- A varredura não trava o editor e o código de editor não entra no build.
- Os dados editados são salvos e voltam ao reabrir o projeto.

## Ligações com outras áreas

- Designers usam as ferramentas para ajustar números de combate, fases e
  missões sem programar.
- O technical artist da Arte 3D e o animation TD da Animação usam validadores
  de assets e scripts de Blender.
- O gameplay programmer expõe os dados que as ferramentas editam.
- O build-devops pode rodar as validações antes do build.
