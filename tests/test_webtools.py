"""As três ferramentas de pesquisa, sobre HTML de exemplo (sem rede)."""

import pytest

from openglitch_mcp import webtools
from openglitch_mcp.util import OGError

PAGE = """<!doctype html><html><head><title>Anatomia de um ataque</title></head><body>
<header><img src="/img/logo.png" width="400" height="400" alt="Logo do site"></header>
<nav><a href="/sobre">Sobre</a><a href="/capitulo-2">Capítulo 2</a></nav>
<article>
<h1>Anatomia de um ataque</h1>
<p>Todo ataque corpo a corpo tem três fases, e cada uma responde a uma pergunta de design
diferente. Entender as três é o primeiro passo para um combate que parece justo e pesado.</p>
<h2>Startup</h2>
<p>A antecipação avisa o adversário de que o golpe vem. Golpes leves têm antecipação curta;
golpes pesados têm antecipação longa, e é isso que permite reagir a eles. Veja o
<a href="/capitulo-2">capítulo sobre recovery</a> e a <a href="https://outro.example/frames">tabela externa</a>.</p>
<h2>Dados de frame</h2>
<table><caption>Golpes do personagem</caption>
<tr><th>Golpe</th><th>Startup</th><th>Recovery</th></tr>
<tr><td>Leve</td><td>4</td><td>8</td></tr>
<tr><td>Pesado | carregado</td><td>14</td><td>22</td></tr></table>
<table><tr><td>layout</td></tr></table>
<figure><img src="/img/linha-do-tempo.png" width="1200" height="600" alt="Linha do tempo do ataque">
<figcaption>As três fases em frames.</figcaption></figure>
<img src="/img/icone-seta.png" width="24" height="24" alt="">
<img src="/img/avatar-autor.jpg" width="400" height="400" alt="Foto do autor">
<img src="/img/faixa.png" width="1600" height="90" alt="Divisor">
<img src="/img/panorama.png" width="2400" height="400" alt="Panorama do cenário">
<img src="/img/diagrama.svg" width="64" height="64" alt="Diagrama pequeno">
<img data-src="/img/hitbox.png" srcset="/img/hitbox-400.png 400w, /img/hitbox-1600.png 1600w" alt="Hitbox e hurtbox">
<p>O recovery é o preço do golpe: enquanto ele dura o personagem não pode agir. Um recovery
longo num golpe forte é o que mantém o risco proporcional à recompensa no combate.</p>
</article>
<div class="related-posts"><img src="/img/outro-post.png" width="800" height="600" alt="Outro post"></div>
<h3>Related Posts</h3><div><img src="/img/mais-um.png" width="800" height="600" alt="Mais um post"></div>
<footer><img src="/img/rodape.png" width="800" height="400" alt="Parceiros"></footer>
</body></html>"""

URL = "https://referencia.example/combate/ataque"


@pytest.fixture(autouse=True)
def sem_rede(monkeypatch):
    monkeypatch.setattr(webtools, "fetch_html", lambda url: (url, PAGE))
    monkeypatch.setattr(webtools, "_probe_size", lambda url: (1600, 900))


def test_texto_so_o_corpo_do_artigo_com_titulos():
    page = webtools.extract_text(URL)
    text = page["text"]
    assert "## Startup" in text and "antecipação avisa" in text
    assert "Sobre" not in text and "Parceiros" not in text and "Logo do site" not in text
    assert "| Leve" not in text  # tabelas saem pela ferramenta de tabelas
    assert page["tables"] == 2 and page["title"] == "Anatomia de um ataque"


def test_texto_com_links_absolutos():
    page = webtools.extract_text(URL, include_links=True)
    assert "https://referencia.example/capitulo-2" in page["inline_links"]
    assert "https://outro.example/frames" in page["inline_links"]
    same_site = [link for _, link in page["page_links"]]
    assert "https://referencia.example/sobre" in same_site
    assert all("outro.example" not in link for link in same_site)


def test_tabelas_viram_markdown():
    page = webtools.extract_tables(URL)
    assert len(page["tables"]) == 1 and page["skipped"] == 1
    table = page["tables"][0]
    assert table["title"] == "Golpes do personagem" and table["rows"] == 2
    lines = table["markdown"].splitlines()
    assert lines[0] == "| Golpe | Startup | Recovery |"
    assert lines[1].count("---") == 3
    assert lines[2] == "| Leve | 4 | 8 |"
    assert lines[3] == "| Pesado \\| carregado | 14 | 22 |"


def test_imagens_filtra_icones_logos_e_banners():
    page = webtools.extract_images(URL)
    urls = [img["url"] for img in page["images"]]
    assert urls == ["https://referencia.example/img/linha-do-tempo.png",
                    "https://referencia.example/img/hitbox-1600.png"]
    first = page["images"][0]
    assert first["caption"] == "As três fases em frames." and first["section"] == "Dados de frame"
    assert (first["width"], first["height"]) == (1200, 600)
    assert page["images"][1]["width"] == 1600  # tamanho descoberto ao sondar o arquivo
    stats = page["stats"]
    assert stats["chrome"] == 4 and stats["small"] == 1 and stats["decorative"] == 2
    assert stats["banner"] == 1 and stats["svg"] == 1


def test_imagens_respeita_tamanho_minimo():
    page = webtools.extract_images(URL, min_width=1400, min_height=700)
    assert [i["url"] for i in page["images"]] == ["https://referencia.example/img/hitbox-1600.png"]


@pytest.mark.parametrize("url", [
    "http://127.0.0.1/", "http://localhost:8080/x", "http://10.0.0.5/", "http://192.168.1.1/",
    "http://169.254.169.254/latest/meta-data/", "http://[::1]/", "file:///c:/windows/win.ini",
    "ftp://example.com/x", "https://usuario:senha@example.com/",
])
def test_urls_internas_e_esquemas_recusados(url):
    with pytest.raises(OGError):
        webtools.check_public_url(url)
