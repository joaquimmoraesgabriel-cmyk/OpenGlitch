"""Documentos locais de um subagente: `agents/<agente>/subagents/<sub>/docs/*.md`.

São material de pesquisa contribuído por pessoas, que vale mesmo quando uma
referência da web sai do ar. Cada arquivo tem cabeçalho obrigatório e é
dividido em seções `##`; a IA lê a lista de títulos e resumos e pede só a
seção que precisa.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from .pageindex import _split_sections
from .util import first_paragraph, parse_frontmatter, slugify

DOC_TYPES = ("original", "referencia")
IMAGE_TYPES = (".png", ".jpg", ".jpeg", ".webp")
MAX_IMAGE_BYTES = 1024 * 1024
MAX_SECTION_LINES = 80
MAX_DOC_BYTES = 60 * 1024
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_IMG_MD = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


@dataclass
class Section:
    slug: str
    title: str
    text: str

    @property
    def summary(self) -> str:
        return first_paragraph(self.text)


@dataclass
class LocalDoc:
    name: str
    title: str
    summary: str
    tipo: str
    fonte: str
    autor: str
    testado_em: str
    intro: str
    sections: list[Section] = field(default_factory=list)

    def header(self) -> str:
        if self.tipo == "referencia":
            kind = f"Tipo: referência. Resumo de {self.fonte}. Cite essa fonte ao usar."
        else:
            kind = "Tipo: original (escrito por quem contribuiu)."
        extra = f" Autor: {self.autor}." if self.autor else ""
        tested = f" Testado em: {self.testado_em}." if self.testado_em else ""
        return kind + extra + tested


def docs_dir(agents_dir: Path, agent: str, sub: str) -> Path:
    return agents_dir / agent / "subagents" / sub / "docs"


def load_docs(folder: Path) -> list[LocalDoc]:
    docs = []
    if not folder.is_dir():
        return docs
    for path in sorted(folder.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        intro, raw_sections = _split_sections(body)
        used: set[str] = set()
        sections = []
        for title, text in raw_sections:
            slug, n = slugify(title), 2
            while slug in used:
                slug = f"{slugify(title)}-{n}"
                n += 1
            used.add(slug)
            sections.append(Section(slug, title, text))
        docs.append(LocalDoc(
            name=path.stem, title=meta.get("title", path.stem),
            summary=meta.get("summary", "") or first_paragraph(body),
            tipo=meta.get("tipo", ""), fonte=meta.get("fonte", ""), autor=meta.get("autor", ""),
            testado_em=meta.get("testado_em", ""), intro=intro, sections=sections,
        ))
    return docs


def validate_docs(folder: Path, where: str) -> list[str]:
    """Regras que tornam um documento encontrável e seguro de distribuir."""
    problems: list[str] = []
    if not folder.is_dir():
        return problems
    for path in sorted(folder.iterdir()):
        rel = f"{where}/docs/{path.name}"
        if path.is_dir():
            if path.name != "img":
                problems.append(f"{rel}: só a subpasta `img` é aceita dentro de docs")
            continue
        if path.name == ".gitkeep":
            continue
        if path.suffix != ".md":
            problems.append(f"{rel}: só arquivos .md são aceitos (outros formatos: link e descrição)")
            continue
        if path.name.startswith("_"):
            continue
        if not NAME_RE.match(path.stem):
            problems.append(f"{rel}: nome em minúsculas, sem acento, com hífens")
        if path.stat().st_size > MAX_DOC_BYTES:
            problems.append(f"{rel}: documento grande demais; divida em dois")
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        for key in ("title", "summary", "tipo", "autor"):
            if not meta.get(key):
                problems.append(f"{rel}: cabeçalho sem `{key}`")
        if meta.get("tipo") and meta["tipo"] not in DOC_TYPES:
            problems.append(f"{rel}: `tipo` é `original` ou `referencia`")
        if meta.get("tipo") == "referencia":
            parts = urlsplit(meta.get("fonte", ""))
            if parts.scheme not in ("http", "https") or not parts.hostname:
                problems.append(f"{rel}: tipo referencia precisa de `fonte` com o link completo")
        if len(meta.get("summary", "")) > 240:
            problems.append(f"{rel}: `summary` com mais de 240 caracteres; use uma frase")
        _, sections = _split_sections(body)
        if not sections:
            problems.append(f"{rel}: divida o documento em seções `##`")
        for title, section in sections:
            if len(section.splitlines()) > MAX_SECTION_LINES:
                problems.append(f"{rel}: seção \"{title}\" com mais de {MAX_SECTION_LINES} linhas; divida")
        for alt, target in _IMG_MD.findall(body):
            if target.startswith(("http://", "https://")):
                continue
            if not alt.strip():
                problems.append(f"{rel}: imagem `{target}` sem descrição no texto alternativo")
            if not target.startswith("img/") or not (folder / target).is_file():
                problems.append(f"{rel}: imagem `{target}` precisa estar em docs/img/")
    img = folder / "img"
    if img.is_dir():
        for path in sorted(img.iterdir()):
            rel = f"{where}/docs/img/{path.name}"
            if path.name == ".gitkeep":
                continue
            if path.is_dir() or path.suffix.lower() not in IMAGE_TYPES:
                problems.append(f"{rel}: só imagens {', '.join(IMAGE_TYPES)}")
            elif path.stat().st_size > MAX_IMAGE_BYTES:
                problems.append(f"{rel}: imagem com mais de 1 MB")
            elif not NAME_RE.match(path.stem):
                problems.append(f"{rel}: nome em minúsculas, sem acento, com hífens")
    return problems
