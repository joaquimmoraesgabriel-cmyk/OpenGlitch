"""As três ferramentas de pesquisa dos subagentes: texto, tabelas e imagens.

- Texto: Trafilatura devolve só o corpo do artigo, em Markdown, com os títulos.
- Tabelas: BeautifulSoup acha cada <table> e pandas.read_html converte; saem em
  Markdown (| Coluna A | Coluna B |).
- Imagens: BeautifulSoup acha cada <img> e um filtro descarta ícones, logos,
  banners e SVGs pequenos. O arquivo só é baixado temporariamente para a IA
  olhar; o que se guarda é o link original e a descrição.

Toda URL passa por `check_public_url`: só http(s), sem credenciais, e o host
não pode resolver para endereço interno. Cada salto de redirecionamento é
verificado de novo.
"""

from __future__ import annotations

import io
import ipaddress
import re
import socket
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx

from .util import OGError

USER_AGENT = "Mozilla/5.0 (compatible; OpenGlitchResearch/1.0)"
TIMEOUT = httpx.Timeout(25.0, connect=10.0)
MAX_HTML_BYTES = 6 * 1024 * 1024
MAX_IMAGE_BYTES = 12 * 1024 * 1024
MAX_REDIRECTS = 5
VIEW_MAX_SIDE = 1280

_BAD_IMAGE_HINT = re.compile(
    r"(logo|icon|favicon|avatar|gravatar|sprite|banner|badge|emoji|button|btn|spinner|loader|"
    r"placeholder|pixel|tracking|advert|sponsor|social|share|profile|thumb-?nail-?small|"
    r"\bads?\b|1x1|spacer)",
    re.IGNORECASE,
)
_CHROME_TAGS = ("header", "nav", "footer", "aside", "form", "button")
_MD_LINK = re.compile(r"\[([^\]\n]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


# ---------------------------------------------------------------------- rede


def host_of(url: str) -> str:
    return (urlsplit(url).hostname or "").lower()


def clean_url(url: str) -> str:
    """Remove o fragmento e normaliza esquema e host."""
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, ""))


def check_public_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme not in ("http", "https"):
        raise OGError(f"URL recusada (só http e https): {url}")
    if parts.username or parts.password:
        raise OGError("URL recusada: não pode conter usuário e senha.")
    host = parts.hostname
    if not host:
        raise OGError(f"URL sem host: {url}")
    try:
        infos = socket.getaddrinfo(host, parts.port or (443 if parts.scheme == "https" else 80),
                                   proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise OGError(f"Não foi possível resolver o endereço `{host}`.") from None
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise OGError(f"URL recusada: `{host}` aponta para um endereço interno.")
    return url.strip()


@dataclass
class Fetched:
    url: str
    content: bytes
    content_type: str


def fetch(url: str, max_bytes: int = MAX_HTML_BYTES, accept: str = "text/html,*/*;q=0.8",
          first_bytes_only: int = 0) -> Fetched:
    current = check_public_url(url)
    headers = {"User-Agent": USER_AGENT, "Accept": accept, "Accept-Language": "en,pt-BR;q=0.8"}
    try:
        with httpx.Client(follow_redirects=False, timeout=TIMEOUT, headers=headers) as client:
            for _ in range(MAX_REDIRECTS + 1):
                with client.stream("GET", current) as resp:
                    if resp.status_code in (301, 302, 303, 307, 308):
                        target = resp.headers.get("location")
                        if not target:
                            raise OGError(f"Redirecionamento sem destino em {current}.")
                        current = check_public_url(urljoin(current, target))
                        continue
                    if resp.status_code >= 400:
                        raise OGError(
                            f"A página respondeu {resp.status_code} ({current}). "
                            "Registre como lacuna ou tente outra página da mesma referência."
                        )
                    declared = int(resp.headers.get("content-length") or 0)
                    if declared > max_bytes and not first_bytes_only:
                        raise OGError(f"Conteúdo grande demais ({declared} bytes) em {current}.")
                    chunks, total = [], 0
                    for chunk in resp.iter_bytes():
                        chunks.append(chunk)
                        total += len(chunk)
                        if first_bytes_only and total >= first_bytes_only:
                            break
                        if total > max_bytes:
                            raise OGError(f"Conteúdo grande demais (mais de {max_bytes} bytes) em {current}.")
                    ctype = resp.headers.get("content-type", "").split(";")[0].strip().lower()
                    return Fetched(url=current, content=b"".join(chunks), content_type=ctype)
            raise OGError(f"Redirecionamentos demais a partir de {url}.")
    except httpx.HTTPError as exc:
        raise OGError(f"Falha ao abrir {current}: {type(exc).__name__}.") from None


def fetch_html(url: str) -> tuple[str, str]:
    got = fetch(url)
    if got.content_type and not (
        "html" in got.content_type or "xml" in got.content_type or got.content_type.startswith("text/")
    ):
        raise OGError(
            f"{got.url} não é uma página de texto (tipo {got.content_type}). "
            "As ferramentas leem HTML; PDF e vídeo não são suportados."
        )
    encoding = None
    match = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", got.content[:4096], re.IGNORECASE)
    if match:
        encoding = match.group(1).decode("ascii", "ignore")
    for enc in (encoding, "utf-8", "cp1252"):
        if not enc:
            continue
        try:
            return got.url, got.content.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return got.url, got.content.decode("utf-8", "replace")


def _soup(html: str):
    from bs4 import BeautifulSoup

    return BeautifulSoup(html, "lxml")


# --------------------------------------------------------------------- texto


def _fallback_markdown(soup) -> str:
    root = soup.find("article") or soup.find("main") or soup.body or soup
    for tag in root.find_all(["script", "style", "noscript", *_CHROME_TAGS]):
        tag.decompose()
    lines = []
    for el in root.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre", "blockquote"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name[0] == "h" and el.name[1:].isdigit():
            lines.append("\n" + "#" * int(el.name[1]) + " " + text)
        elif el.name == "li":
            lines.append("- " + text)
        elif el.name == "pre":
            lines.append("```\n" + el.get_text() + "\n```")
        else:
            lines.append(text + "\n")
    return "\n".join(lines).strip()


def _page_links(soup, base_url: str, limit: int = 150) -> list[tuple[str, str]]:
    """Links da página no mesmo site: servem para ir de um índice ao capítulo certo."""
    base_host = host_of(base_url).removeprefix("www.")
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "mailto:", "javascript:", "tel:")):
            continue
        absolute = clean_url(urljoin(base_url, href))
        if urlsplit(absolute).scheme not in ("http", "https"):
            continue
        if host_of(absolute).removeprefix("www.") != base_host or absolute in seen:
            continue
        seen.add(absolute)
        label = re.sub(r"\s+", " ", a.get_text(" ", strip=True))[:90] or absolute
        out.append((label, absolute))
        if len(out) >= limit:
            break
    return out


def extract_text(url: str, include_links: bool = False) -> dict:
    import trafilatura

    final_url, html = fetch_html(url)
    soup = _soup(html)
    title = soup.title.get_text(strip=True) if soup.title else ""
    n_tables = len(soup.find_all("table"))
    n_images = len(soup.find_all("img"))
    links = _page_links(soup, final_url) if include_links else []

    text = None
    try:
        text = trafilatura.extract(
            html, url=final_url, output_format="markdown", include_links=include_links,
            include_tables=False, include_images=False, include_comments=False,
            favor_recall=True, deduplicate=True,
        )
    except Exception:  # a extração não pode derrubar a ferramenta
        text = None
    method = "trafilatura"
    if not text or len(text.strip()) < 200:
        fallback = _fallback_markdown(soup)
        if len(fallback) > len(text or ""):
            text, method = fallback, "fallback"
    text = (text or "").strip()

    inline_links = []
    if include_links and text:
        def absolutize(match: re.Match) -> str:
            target = urljoin(final_url, match.group(2))
            if urlsplit(target).scheme in ("http", "https"):
                inline_links.append(clean_url(target))
            return f"[{match.group(1)}]({target})"

        text = _MD_LINK.sub(absolutize, text)
    return {
        "url": final_url, "title": title, "text": text, "method": method,
        "tables": n_tables, "images": n_images, "page_links": links,
        "inline_links": inline_links,
    }


# ------------------------------------------------------------------- tabelas


def _cell(value) -> str:
    text = "" if value is None else str(value)
    if text in ("nan", "NaN", "None", "<NA>"):
        text = ""
    return re.sub(r"\s+", " ", text).replace("|", "\\|").strip()


def dataframe_to_markdown(df, max_rows: int = 200) -> str:
    columns = []
    for col in df.columns:
        if isinstance(col, tuple):
            parts = [str(p) for p in col if str(p) and not str(p).startswith("Unnamed")]
            deduped = [p for i, p in enumerate(parts) if i == 0 or p != parts[i - 1]]
            columns.append(" / ".join(deduped))
        else:
            columns.append("" if str(col).startswith("Unnamed") else str(col))
    if all(re.fullmatch(r"\d+", c or "0") for c in columns) and len(df) > 1:
        # Tabela sem cabeçalho: a primeira linha vira o cabeçalho.
        columns = [_cell(v) for v in df.iloc[0].tolist()]
        df = df.iloc[1:]
    lines = ["| " + " | ".join(_cell(c) or " " for c in columns) + " |",
             "|" + "|".join(" --- " for _ in columns) + "|"]
    for row in df.head(max_rows).itertuples(index=False):
        lines.append("| " + " | ".join(_cell(v) for v in row) + " |")
    if len(df) > max_rows:
        lines.append(f"\n(tabela cortada: {len(df) - max_rows} linhas a mais na página)")
    return "\n".join(lines)


def _table_title(table) -> str:
    if table.caption and table.caption.get_text(strip=True):
        return table.caption.get_text(" ", strip=True)
    heading = table.find_previous(["h1", "h2", "h3", "h4", "h5", "h6"])
    return heading.get_text(" ", strip=True) if heading else ""


def extract_tables(url: str, max_tables: int = 20) -> dict:
    import pandas as pd

    final_url, html = fetch_html(url)
    soup = _soup(html)
    tables_out, skipped = [], 0
    for table in soup.find_all("table"):
        if table.find("table"):
            continue  # tabela de layout: as internas são tratadas na vez delas
        rows = table.find_all("tr")
        if len(rows) < 2 or max((len(r.find_all(["td", "th"])) for r in rows), default=0) < 2:
            skipped += 1
            continue
        for br in table.find_all("br"):
            br.replace_with(" ")
        for img in table.find_all("img"):
            img.replace_with(img.get("alt", ""))
        try:
            frames = pd.read_html(io.StringIO(str(table)), flavor="lxml")
        except (ValueError, ImportError):
            skipped += 1
            continue
        if not frames:
            skipped += 1
            continue
        df = frames[0].dropna(how="all").dropna(axis=1, how="all")
        if df.empty:
            skipped += 1
            continue
        tables_out.append({
            "title": _table_title(table), "rows": len(df), "columns": len(df.columns),
            "markdown": dataframe_to_markdown(df),
        })
        if len(tables_out) >= max_tables:
            break
    return {"url": final_url, "tables": tables_out, "skipped": skipped}


# ------------------------------------------------------------------- imagens


def _int_attr(value) -> int | None:
    if value is None:
        return None
    match = re.match(r"\s*(\d+)", str(value))
    return int(match.group(1)) if match else None


def _best_src(img) -> str | None:
    best, best_width = None, -1
    for attr in ("srcset", "data-srcset"):
        for candidate in (img.get(attr) or "").split(","):
            bits = candidate.strip().split()
            if not bits:
                continue
            width = _int_attr(bits[1]) if len(bits) > 1 and bits[1].endswith("w") else 0
            if (width or 0) > best_width:
                best, best_width = bits[0], width or 0
    for attr in ("data-src", "data-original", "data-lazy-src", "src"):
        value = img.get(attr)
        if value and not value.startswith("data:"):
            return best if best_width > 0 and best else value
    return best


def _probe_size(url: str) -> tuple[int, int] | None:
    """Lê só o começo do arquivo para descobrir largura e altura."""
    from PIL import ImageFile

    try:
        got = fetch(url, max_bytes=MAX_IMAGE_BYTES, accept="image/*", first_bytes_only=96 * 1024)
    except OGError:
        return None
    parser = ImageFile.Parser()
    try:
        parser.feed(got.content)
        if parser.image:
            return parser.image.size
    except Exception:
        return None
    return None


def extract_images(url: str, min_width: int = 300, min_height: int = 300,
                   max_results: int = 30, max_probes: int = 12) -> dict:
    final_url, html = fetch_html(url)
    soup = _soup(html)
    found, seen = [], set()
    stats = {"total": 0, "small": 0, "chrome": 0, "decorative": 0, "svg": 0, "banner": 0,
             "unknown_size": 0}
    probes = 0
    for img in soup.find_all("img"):
        stats["total"] += 1
        src = _best_src(img)
        if not src:
            continue
        absolute = urljoin(final_url, src)
        if urlsplit(absolute).scheme not in ("http", "https") or absolute in seen:
            continue
        seen.add(absolute)
        if img.find_parent(_CHROME_TAGS):
            stats["chrome"] += 1
            continue
        hint = " ".join([
            " ".join(img.get("class") or []), img.get("id") or "", img.get("alt") or "",
            urlsplit(absolute).path,
        ])
        if _BAD_IMAGE_HINT.search(hint):
            stats["decorative"] += 1
            continue
        width, height = _int_attr(img.get("width")), _int_attr(img.get("height"))
        is_svg = urlsplit(absolute).path.lower().endswith(".svg")
        if is_svg and not (width and height and width >= min_width and height >= min_height):
            stats["svg"] += 1
            continue
        figure = img.find_parent("figure")
        in_content = bool(figure or img.find_parent(["article", "main"]))
        if (width is None or height is None) and not is_svg and probes < max_probes:
            probes += 1
            size = _probe_size(absolute)
            if size:
                width, height = size
        if width is not None and height is not None:
            if width < min_width or height < min_height:
                stats["small"] += 1
                continue
            if width / max(height, 1) > 5 or height / max(width, 1) > 5:
                stats["banner"] += 1
                continue
        elif not in_content:
            stats["unknown_size"] += 1
            continue
        caption = ""
        if figure and figure.find("figcaption"):
            caption = figure.find("figcaption").get_text(" ", strip=True)
        heading = img.find_previous(["h1", "h2", "h3", "h4"])
        found.append({
            "url": absolute, "alt": (img.get("alt") or "").strip(), "caption": caption,
            "section": heading.get_text(" ", strip=True) if heading else "",
            "width": width, "height": height,
        })
        if len(found) >= max_results:
            break
    return {"url": final_url, "images": found, "stats": stats}


def view_image(url: str) -> dict:
    """Baixa a imagem para um arquivo temporário, devolve uma cópia reduzida e apaga o arquivo."""
    from PIL import Image

    got = fetch(url, max_bytes=MAX_IMAGE_BYTES, accept="image/*")
    if "svg" in got.content_type or urlsplit(got.url).path.lower().endswith(".svg"):
        labels = re.findall(r"<text[^>]*>(.*?)</text>", got.content.decode("utf-8", "replace"), re.S)
        labels = [re.sub(r"<[^>]+>|\s+", " ", t).strip() for t in labels]
        return {"url": got.url, "svg": True, "labels": [t for t in labels if t][:200]}
    with tempfile.TemporaryDirectory(prefix="openglitch-img-") as tmp:
        path = Path(tmp) / "imagem"
        path.write_bytes(got.content)
        try:
            with Image.open(path) as im:
                im.load()
                original = im.size
                if im.mode not in ("RGB", "L"):
                    rgba = im.convert("RGBA")
                    canvas = Image.new("RGB", rgba.size, (255, 255, 255))
                    canvas.paste(rgba, mask=rgba.split()[-1])
                    im = canvas
                im.thumbnail((VIEW_MAX_SIDE, VIEW_MAX_SIDE))
                buffer = io.BytesIO()
                im.convert("RGB").save(buffer, format="JPEG", quality=85)
        except Exception:
            raise OGError(f"{got.url} não é uma imagem que dê para abrir.") from None
    return {"url": got.url, "svg": False, "width": original[0], "height": original[1],
            "jpeg": buffer.getvalue()}
