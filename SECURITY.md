# Segurança

## Como relatar uma falha

Não abra uma issue pública para falha de segurança. Use o relato privado do
GitHub: na página do repositório, aba **Security**, botão **Report a
vulnerability**. Só o mantenedor vê o relato.

Diga o que acontece, como reproduzir e que versão (o commit) você usou. Espere
uma resposta em até duas semanas; o projeto é mantido por uma pessoa.

## O que o OpenGlitch faz no seu computador

Saber isso ajuda a avaliar o risco antes de instalar.

- **Roda localmente.** O servidor é um programa Python que o seu cliente de IA
  inicia. Ele não tem servidor central, não envia telemetria e não pede conta.
- **Acessa a internet só para ler páginas das referências**, quando um
  subagente pesquisa. Cada subagente só abre páginas dos domínios das próprias
  referências, links encontrados dentro delas e URLs que o agente incluiu na
  tarefa.
- **Não abre endereços internos.** Toda URL é verificada: só `http` e `https`,
  sem usuário e senha, e o servidor recusa endereços de rede local, de
  loopback e de metadados de nuvem, inclusive depois de um redirecionamento.
- **Se identifica como ferramenta** ao abrir páginas e não contorna bloqueio
  de site.
- **Grava só na pasta `.openglitch`** da sua pasta de usuário (memória dos
  agentes, projetos, sessões e o registro de problemas). Imagens são baixadas
  para uma pasta temporária e apagadas em seguida.
- **Não executa comandos nem edita os arquivos do seu jogo.** Quem faz isso é a
  IA, com as ferramentas e as permissões do seu cliente.
- **O instalador altera a configuração dos clientes de IA** para registrar o
  servidor, e salva uma cópia de cada arquivo antes (`.bak-openglitch`).

## Riscos que você deve conhecer

- **Conteúdo da web pode tentar dar ordens à IA** (injeção de prompt). As
  skills mandam tratar todo texto pesquisado como dado, e o servidor limita
  onde o subagente navega, mas nenhuma dessas medidas é garantia. Revise o que
  a IA propõe antes de aprovar ações no seu computador.
- **As credenciais internas (`session` e `ticket`) organizam o trabalho, não
  protegem contra um programa malicioso** que já esteja rodando na sua conta.
- **A memória fica em texto simples** no seu disco. Não peça aos agentes para
  guardar senhas, chaves ou dados pessoais.
- **Referências são sites de terceiros.** O projeto não controla o conteúdo
  deles nem garante que continuem no ar.

## Versões com correção

Só a versão mais recente da `main` recebe correções.
