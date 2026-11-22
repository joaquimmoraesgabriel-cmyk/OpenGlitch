"""Utilidades compartilhadas: texto, busca, JSON atômico e trava de arquivo."""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import threading
import time
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


class OGError(Exception):
    """Erro esperado: a mensagem é mostrada à IA que chamou a ferramenta."""


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch)
    )


def normalize(text: str) -> str:
    return strip_accents(text).lower()


def slugify(text: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", normalize(text)).strip("-")
    return slug[:max_len].strip("-") or "sem-nome"


_STOPWORDS = frozenset(
    """a o as os um uma uns umas de do da dos das em no na nos nas por para pra pro
    com sem que e ou se como qual quais quando onde the of and to in for is are on
    with what how eu ele ela isso este esta esse essa ao aos mais menos ser sao""".split()
)


def query_tokens(query: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", normalize(query))
    kept = [t for t in tokens if t not in _STOPWORDS and len(t) > 1]
    return kept or tokens


def score_text(tokens: list[str], title: str, summary: str, body: str, tags: str = "") -> float:
    """Pontuação simples por termo: título pesa mais que resumo, que pesa mais que corpo."""
    if not tokens:
        return 0.0
    n_title, n_summary, n_tags, n_body = (
        normalize(title),
        normalize(summary),
        normalize(tags),
        normalize(body),
    )
    score = 0.0
    matched = 0
    for tok in tokens:
        hit = (
            6.0 * n_title.count(tok)
            + 3.0 * n_summary.count(tok)
            + 4.0 * n_tags.count(tok)
            + min(n_body.count(tok), 8) * 1.0
        )
        if hit:
            matched += 1
        score += hit
    if matched == 0:
        return 0.0
    # Favorece resultados que cobrem mais termos da pergunta.
    return score * (matched / len(tokens)) ** 2


def snippet(body: str, tokens: list[str], width: int = 220) -> str:
    flat = re.sub(r"\s+", " ", body).strip()
    if not flat:
        return ""
    n_flat = normalize(flat)
    pos = -1
    for tok in tokens:
        pos = n_flat.find(tok)
        if pos >= 0:
            break
    if pos < 0:
        return flat[:width] + ("..." if len(flat) > width else "")
    start = max(0, pos - width // 3)
    end = min(len(flat), start + width)
    return ("..." if start else "") + flat[start:end] + ("..." if end < len(flat) else "")


def first_paragraph(text: str, max_len: int = 220) -> str:
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block or block.startswith(("```", "|", "#")):
            continue
        flat = re.sub(r"\s+", " ", re.sub(r"^[-*\d.]+\s+", "", block))
        flat = re.sub(r"[*_`]", "", flat)
        return flat[: max_len - 3] + "..." if len(flat) > max_len else flat
    return ""


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Lê um frontmatter YAML simples (chave: valor em uma linha)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("\"'")
    body = text[end + 4 :]
    return meta, body.lstrip("\r\n")


def read_json(path: Path, default: Any = None) -> Any:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def write_json_atomic(path: Path, data: Any) -> None:
    write_text_atomic(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


_thread_lock = threading.RLock()


@contextmanager
def file_lock(lock_path: Path, timeout: float = 15.0) -> Iterator[None]:
    """Trava entre threads e entre processos (vários clientes no mesmo servidor de dados)."""
    with _thread_lock:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        fh = open(lock_path, "a+b")
        try:
            deadline = time.monotonic() + timeout
            while True:
                try:
                    _lock_handle(fh)
                    break
                except OSError:
                    if time.monotonic() > deadline:
                        raise OGError(
                            "Os dados do OpenGlitch estão em uso por outro processo. Tente de novo."
                        )
                    time.sleep(0.05)
            try:
                yield
            finally:
                _unlock_handle(fh)
        finally:
            fh.close()


if sys.platform == "win32":
    import msvcrt

    def _lock_handle(fh) -> None:
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)

    def _unlock_handle(fh) -> None:
        fh.seek(0)
        try:
            msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass

else:
    import fcntl

    def _lock_handle(fh) -> None:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _unlock_handle(fh) -> None:
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
