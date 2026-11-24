#!/usr/bin/env python3
"""Instalador do OpenGlitch. Só usa a biblioteca padrão do Python.

    python install.py              instala e registra em todos os clientes encontrados
    python install.py --dry-run    mostra o que faria, sem alterar nada
    python install.py --clients claude-code,codex
    python install.py --uninstall  remove o registro dos clientes
    python install.py --motionbricks   instala também o MotionBricks (só com GPU NVIDIA)

O que faz:
  1. cria o ambiente virtual `.venv` nesta pasta e instala o servidor;
  2. confere o conteúdo (agentes, referências, base de conhecimento);
  3. registra o servidor MCP `openglitch` nos clientes de IA que achar:
     Claude Code, aplicativo Claude (chat), Codex e Cursor.

Todo arquivo de configuração alterado ganha uma cópia `.bak-openglitch` antes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "openglitch"
MIN_PYTHON = (3, 11)
IS_WINDOWS = sys.platform == "win32"
# Conexão lenta com o pypi.org é comum. As variáveis valem também para o pip que roda por
# dentro, ao montar o pacote; as opções de linha de comando não chegam até ele.
NET_ENV = {"PIP_DEFAULT_TIMEOUT": "120", "PIP_RETRIES": "10", "UV_HTTP_TIMEOUT": "300"}
HOME = Path.home()


def say(text: str = "") -> None:
    print(text, flush=True)


def venv_python() -> Path:
    return ROOT / ".venv" / ("Scripts/python.exe" if IS_WINDOWS else "bin/python")


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    kwargs["env"] = {**os.environ, **NET_ENV, **(kwargs.get("env") or {})}
    return subprocess.run(cmd, text=True, capture_output=True, **kwargs)


# --------------------------------------------------------------- instalação


def install_server(dry: bool) -> bool:
    py = venv_python()
    if dry:
        say(f"  criaria o ambiente em {py.parent.parent} e instalaria o pacote")
        return True
    if not py.is_file():
        say("  criando o ambiente virtual (.venv)...")
        done = run([sys.executable, "-m", "venv", str(ROOT / ".venv")])
        if done.returncode != 0:
            say(f"  ERRO ao criar o ambiente:\n{done.stderr.strip()}")
            return False
    say("  instalando dependências (pode levar alguns minutos)...")
    run([str(py), "-m", "pip", "install", "--quiet", "--upgrade", "pip"])
    done = run([str(py), "-m", "pip", "install", "--quiet", "-e", str(ROOT)])
    if done.returncode != 0:
        offline = "timed out" in done.stderr or "Could not find a version" in done.stderr
        already = run([str(py), "-c", "import openglitch_mcp, mcp, trafilatura, pandas"]).returncode == 0
        if offline and already:
            # Reinstalação sem rede: o servidor já está instalado e funciona; só não foi atualizado.
            say("  Sem conexão com o pypi.org agora. O servidor já estava instalado e segue como "
                "está; rode o instalador de novo mais tarde para atualizar as dependências.")
        else:
            say(f"  ERRO na instalação:\n{done.stderr.strip()[-1500:]}")
            if offline:
                say("  Parece falha de conexão com o pypi.org. Rode o instalador de novo: ele "
                    "continua de onde parou.")
            return False
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    check = run([str(py), "-m", "openglitch_mcp.cli", "validate"], env=env, encoding="utf-8")
    last = (check.stdout or "").strip().splitlines()
    say("  conteúdo: " + (last[0] if last else "sem resposta"))
    if check.returncode != 0:
        say("  ERRO: a conferência do conteúdo falhou:\n" + (check.stdout or check.stderr)[-1500:])
        return False
    return True


# ------------------------------------------------------------ configurações


def backup(path: Path) -> None:
    if path.is_file():
        shutil.copyfile(path, path.with_name(path.name + ".bak-openglitch"))


def server_entry() -> dict:
    return {"command": str(venv_python()), "args": ["-m", "openglitch_mcp"]}


def edit_json_config(path: Path, remove: bool, dry: bool) -> str:
    """Põe ou tira `mcpServers.openglitch` de um arquivo JSON, preservando o resto."""
    data: dict = {}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig") or "{}")
        except json.JSONDecodeError:
            return f"não alterado: {path} não é um JSON válido"
        if not isinstance(data, dict):
            return f"não alterado: {path} tem formato inesperado"
    servers = data.setdefault("mcpServers", {})
    if remove:
        if NAME not in servers:
            return "não estava registrado"
        del servers[NAME]
    else:
        if servers.get(NAME) == server_entry():
            return f"já registrado ({path})"
        servers[NAME] = server_entry()
    if dry:
        return f"alteraria {path}"
    backup(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ("removido de " if remove else "registrado em ") + str(path)


def find_claude_cli() -> str | None:
    found = shutil.which("claude")
    if found:
        return found
    for candidate in (HOME / ".local" / "bin" / ("claude.exe" if IS_WINDOWS else "claude"),
                      HOME / ".claude" / "local" / ("claude.exe" if IS_WINDOWS else "claude")):
        if candidate.is_file():
            return str(candidate)
    return None


def client_claude_code(remove: bool, dry: bool) -> str | None:
    cli = find_claude_cli()
    config = HOME / ".claude.json"
    if not cli and not config.is_file():
        return None
    if not cli:
        return edit_json_config(config, remove, dry)
    if dry:
        return f"usaria `{cli} mcp {'remove' if remove else 'add'}` (escopo de usuário)"
    run([cli, "mcp", "remove", NAME, "-s", "user"])
    if remove:
        return "removido (escopo de usuário)"
    done = run([cli, "mcp", "add", "--scope", "user", NAME, "--", str(venv_python()),
                "-m", "openglitch_mcp"])
    if done.returncode != 0:
        return "falhou pelo comando claude; " + edit_json_config(config, remove, dry)
    return "registrado (escopo de usuário: vale em qualquer pasta)"


def claude_desktop_configs() -> list[Path]:
    """O aplicativo guarda a configuração em lugares diferentes conforme a instalação."""
    name = "claude_desktop_config.json"
    if IS_WINDOWS:
        local = Path(os.environ.get("LOCALAPPDATA", HOME / "AppData" / "Local"))
        roaming = Path(os.environ.get("APPDATA", HOME / "AppData" / "Roaming"))
        store = [d / name for d in (local / "Claude-Data").glob("*") if d.is_dir()]
        if store:  # versão da Microsoft Store
            return store
        return [roaming / "Claude" / name] if (roaming / "Claude").is_dir() else []
    if sys.platform == "darwin":
        folder = HOME / "Library" / "Application Support" / "Claude"
    else:
        folder = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config")) / "Claude"
    return [folder / name] if folder.is_dir() else []


def client_claude_desktop(remove: bool, dry: bool) -> str | None:
    configs = claude_desktop_configs()
    if not configs:
        return None
    return "; ".join(edit_json_config(path, remove, dry) for path in configs)


def client_cursor(remove: bool, dry: bool) -> str | None:
    folder = HOME / ".cursor"
    return edit_json_config(folder / "mcp.json", remove, dry) if folder.is_dir() else None


def client_codex(remove: bool, dry: bool) -> str | None:
    folder = HOME / ".codex"
    if not folder.is_dir():
        return None
    path = folder / "config.toml"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    block = re.compile(rf"(?ms)^\[mcp_servers\.{NAME}\][^\[]*")
    command = str(venv_python()).replace("'", "")
    section = f"[mcp_servers.{NAME}]\ncommand = '{command}'\nargs = [\"-m\", \"openglitch_mcp\"]\n"
    had = bool(block.search(text))
    stripped = block.sub("", text).rstrip()
    if remove:
        if not had:
            return "não estava registrado"
        new = stripped + "\n" if stripped else ""
    else:
        new = (stripped + "\n\n" if stripped else "") + section
        if had and section.strip() in text:
            return f"já registrado ({path})"
    if dry:
        return f"alteraria {path}"
    backup(path)
    path.write_text(new, encoding="utf-8")
    return ("removido de " if remove else "registrado em ") + str(path)



# -------------------------------------------------------------- MotionBricks

MOTIONBRICKS_REPO = "https://github.com/NVlabs/motionbricks.git"
MOTIONBRICKS_NOTICE = """
  O MotionBricks é da NVIDIA e tem licenças próprias. Leia antes de usar:
    - código: Apache 2.0
    - modelos: NVIDIA Open Model Agreement
    - clipes de exemplo: NVIDIA Sample Data Evaluation License, só para avaliar e
      testar, em uso interno. Animação feita a partir deles NÃO pode ser
      distribuída nem entrar num jogo publicado.
  Detalhes em https://github.com/NVlabs/motionbricks#license
"""


def data_dir() -> Path:
    return Path(os.environ.get("OPENGLITCH_DATA") or HOME / ".openglitch")


def nvidia_gpu() -> str | None:
    smi = shutil.which("nvidia-smi")
    if not smi:
        return None
    done = run([smi, "--query-gpu=name,memory.total", "--format=csv,noheader"])
    lines = [line.strip() for line in (done.stdout or "").splitlines() if line.strip()]
    return lines[0] if done.returncode == 0 and lines else None


def install_motionbricks(dry: bool) -> bool:
    """Componente opcional: baixa o MotionBricks oficial e prepara o ambiente dele."""
    gpu = nvidia_gpu()
    if not gpu:
        say("  Nenhuma GPU NVIDIA encontrada (o comando nvidia-smi não respondeu).")
        say("  O MotionBricks usa TensorRT e só roda em GPU NVIDIA. O OpenGlitch continua")
        say("  funcionando sem ele; a animação segue por script, clipes prontos ou mocap.")
        return False
    say(f"  GPU: {gpu}")
    missing = []
    if not shutil.which("git"):
        missing.append("Git: https://git-scm.com/downloads")
    elif run(["git", "lfs", "version"]).returncode != 0:
        missing.append("Git LFS: https://git-lfs.com/")
    if not shutil.which("uv"):
        missing.append("uv: https://docs.astral.sh/uv/getting-started/installation/")
    if missing:
        say("  Falta instalar antes:")
        for item in missing:
            say(f"    - {item}")
        return False
    say(MOTIONBRICKS_NOTICE)
    base = data_dir() / "motionbricks"
    repo = base / "repo"
    if dry:
        say(f"  baixaria {MOTIONBRICKS_REPO} para {repo} (alguns GB) e rodaria git lfs pull e uv sync")
        return True
    base.mkdir(parents=True, exist_ok=True)
    git = ["git", "-C", str(repo)]
    # Se uma tentativa anterior parou no meio, o repositório existe mas está incompleto:
    # os passos abaixo retomam de onde parou em vez de baixar tudo de novo.
    steps = ([git + ["fetch", "origin"]] if (repo / ".git").is_dir()
             else [["git", "-c", "filter.lfs.smudge=", "-c", "filter.lfs.required=false",
                    "clone", MOTIONBRICKS_REPO, str(repo)]])
    steps += [git + ["lfs", "fetch"], git + ["checkout", "-f", "HEAD"], git + ["lfs", "checkout"],
              ["uv", "sync", "--project", str(repo)]]
    # Um download por vez: em conexão instável os arquivos grandes do TensorRT são cortados
    # quando vários baixam juntos. O que já baixou fica em cache entre as tentativas.
    sync_env = {"UV_CONCURRENT_DOWNLOADS": "1", "UV_HTTP_TIMEOUT": "600"}
    for step in steps:
        label = " ".join(s for s in step if not s.startswith("filter.") and s != "-c")
        for attempt in range(1, 7):
            say(f"  {label[:70]} ... (pode demorar)" + (f" tentativa {attempt}" if attempt > 1 else ""))
            done = subprocess.run(step, text=True, env={**os.environ, **NET_ENV, **sync_env})
            if done.returncode == 0:
                break
            time.sleep(10)
        else:
            say("  ERRO neste passo depois de 6 tentativas. O OpenGlitch em si está instalado; só o")
            say("  MotionBricks ficou de fora. Se foi falha de rede, rode o mesmo comando de novo:")
            say("  ele retoma de onde parou.")
            return False
    (base / "instalado.json").write_text(
        json.dumps({"repo": str(repo), "gpu": gpu}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    test = f'uv run --project "{repo}" python "{ROOT / "extras" / "motionbricks" / "gerar.py"}" --teste --saida "{base / "teste"}"'
    say("  MotionBricks instalado. Para testar (a primeira vez monta o plano do TensorRT e leva minutos):")
    say("    " + test)
    return True

CLIENTS = {
    "claude-code": ("Claude Code (terminal e aba Code)", client_claude_code),
    "claude-desktop": ("Aplicativo Claude (chat)", client_claude_desktop),
    "codex": ("Codex", client_codex),
    "cursor": ("Cursor", client_cursor),
}


def manual_help() -> None:
    say("\nPara registrar à mão em outro cliente MCP, use este servidor stdio:")
    say(f"  comando:    {venv_python()}")
    say("  argumentos: -m openglitch_mcp")


def main() -> int:
    if not sys.stdout.isatty():  # saída capturada (por uma IA, por exemplo): sempre UTF-8
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Instala o OpenGlitch e registra nos clientes de IA.")
    parser.add_argument("--clients", default="all",
                        help="lista separada por vírgula: " + ", ".join(CLIENTS) + " (padrão: all)")
    parser.add_argument("--dry-run", action="store_true", help="só mostra o que faria")
    parser.add_argument("--uninstall", action="store_true", help="remove o registro dos clientes")
    parser.add_argument("--motionbricks", action="store_true",
                        help="instala também o MotionBricks, gerador de movimento da NVIDIA (só GPU NVIDIA)")
    args = parser.parse_args()

    if sys.version_info < MIN_PYTHON:
        say(f"O OpenGlitch precisa de Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} ou mais novo; "
            f"este é o {sys.version.split()[0]}. Instale em https://www.python.org/downloads/")
        return 1
    wanted = list(CLIENTS) if args.clients == "all" else [c.strip() for c in args.clients.split(",")]
    unknown = [c for c in wanted if c not in CLIENTS]
    if unknown:
        say(f"Cliente desconhecido: {', '.join(unknown)}. Opções: {', '.join(CLIENTS)}")
        return 2

    say(f"OpenGlitch em {ROOT}" + (" (simulação: nada será alterado)" if args.dry_run else ""))
    if not args.uninstall:
        say("\n1. Servidor")
        if not install_server(args.dry_run):
            return 1

    say("\n2. Clientes de IA" if not args.uninstall else "\nRemovendo o registro")
    registered = 0
    for key in wanted:
        label, handler = CLIENTS[key]
        result = handler(args.uninstall, args.dry_run)
        if result is None:
            say(f"  {label}: não encontrado neste computador")
        else:
            registered += 1
            say(f"  {label}: {result}")

    if args.motionbricks and not args.uninstall:
        say("\n3. MotionBricks (opcional)")
        install_motionbricks(args.dry_run)

    if args.uninstall:
        say("\nRegistro removido. A pasta e a memória (~/.openglitch) continuam no lugar.")
        return 0
    if not registered:
        say("\nNenhum cliente de IA foi encontrado.")
        manual_help()
        return 0
    say("\nPronto. Agora:")
    say("  1. Feche o cliente de IA por completo e abra de novo (no aplicativo Claude para")
    say("     Windows: botão direito no ícone da bandeja, Sair).")
    say("  2. Numa conversa nova, peça: \"Usa o OpenGlitch: quero criar um jogo ...\"")
    say(f"\nA memória dos agentes fica em {HOME / '.openglitch'}. Não mova nem apague esta pasta")
    say(f"({ROOT}): os clientes apontam para ela.")
    manual_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
