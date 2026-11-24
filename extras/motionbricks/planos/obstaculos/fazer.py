"""Planos das animações de obstáculo para o gerar.py do OpenGlitch (poses próprias).

    python fazer.py            grava todos os planos .json nesta pasta
    python fazer.py Nome ...   só os citados

Convenções: +Y cima, +Z frente, +X esquerda do personagem, metros. O tornozelo fica 7,2 cm acima
da sola e o punho uns 4 cm acima da superfície em que a mão apoia. Cada destino é um ponto de
passagem (antecipar), com o pé ou a mão levado ao ponto exato (levar) e o apoio fixado (fixar).
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PE = 0.072
MAO = 0.04


def bracos(esq: float = 0.0, dir: float = 0.0, abre: float = 0.16) -> list:
    """Braços soltos: valor positivo leva o braço para a frente, negativo para trás (0 = pendurado)."""
    out = []
    for lado, s, a in (("Left", 1.0, esq), ("Right", -1.0, dir)):
        z = 0.34 * a if a >= 0 else 0.22 * a
        out.append([f"{lado}Arm", f"{lado}ForeArm", [s * abre, -1.0, 0.02 + z]])
        out.append([f"{lado}ForeArm", f"{lado}Hand", [s * 0.08, -1.0 + 0.35 * max(a, 0.0), 0.15 + (0.75 * a if a >= 0 else 0.10 * a)]])
    return out


def tronco(inclina: float) -> list:
    return [["Hips", "Spine1", [0, 1, 0.6 * inclina]], ["Spine1", "Spine2", [0, 1, 0.9 * inclina]], ["Spine2", "Chest", [0, 1, inclina]]]


EM_PE = {"mirar": bracos()}


def pose(z, altura=0.0, inclina=0.0, esq=0.0, dir=0.0, alc=None, x=0.0, extra=None, planos=("LeftFoot", "RightFoot")):
    p = {"base": "em_pe", "lugar": [x, z], "mirar": tronco(inclina) + bracos(esq, dir) + (extra or [])}
    if altura:
        p["altura"] = altura
    if alc:
        p["alcancar"] = [[n, list(pt), [0, 0, 1]] if n.endswith("Foot") else [n, list(pt)] for n, pt in alc.items()]
    if planos:
        p["pe_plano"] = list(planos)
    return p


def dest(nome, tokens=8, antecipar=5, **campos):
    d = {"nome": nome, "pose": nome, "tokens": tokens}
    if antecipar:
        d["antecipar"] = antecipar
    d.update(campos)
    return d


# ------------------------------------------------------------------------------------ subir andando
def subir(h: float) -> dict:
    """Subir num bloco baixo (face em z = 1,0, topo em y = h) dando um passo para cima."""
    chao = {"RightFoot": (-0.1, PE, 0.572)}
    topo = {"LeftFoot": (0.1, h + PE, 1.18)}
    P = {"em_pe": EM_PE, "diante": {"base": "em_pe", "lugar": [0, 0.55]},
         "levanta_o_pe": pose(0.58, 0, 0.10, esq=-0.7, dir=0.9, alc={"LeftFoot": (0.1, h + 0.22, 0.90), **chao}),
         "pe_em_cima": pose(0.62, -0.03, 0.20, esq=-0.4, dir=0.9, alc={**topo, **chao}),
         "passa_o_peso": pose(1.00, 0.6 * h, 0.32, esq=0.3, dir=0.4, alc={**topo, "RightFoot": (-0.1, h - 0.10, 0.42)}),
         "traz_o_pe": pose(1.14, h - 0.10, 0.20, esq=0.8, dir=-0.4, alc={**topo, "RightFoot": (-0.1, h + 0.40, 0.82)}),
         "em_cima": {"base": "em_pe", "lugar": [0, 1.16], "altura": h}}
    D = [dest("levanta_o_pe", tokens=6, antecipar=4, fixar=["RightFoot"], nivelar=["LeftFoot"], levar=["LeftFoot"]),
         dest("pe_em_cima", tokens=6, antecipar=4, fixar=["RightFoot"], nivelar=["LeftFoot"], levar=["LeftFoot"]),
         dest("passa_o_peso", tokens=7, fixar=["LeftFoot"], nivelar=["RightFoot"]),
         dest("traz_o_pe", tokens=7, fixar=["LeftFoot"], nivelar=["RightFoot"]),
         dest("em_cima", tokens=8, antecipar=0, fixar=["LeftFoot"], nivelar=["RightFoot"], levar=["RightFoot"])]
    return {"_descricao": f"Subir num bloco de {h} m dando um passo para cima: levanta o pé esquerdo acima da quina, apoia em cima, passa o peso, traz o pé direito e fica em pé.",
            "obstaculos": [{"nome": "bloco", "centro": [0, h / 2, 1.6], "tamanho": [1.4, h, 1.2]}],
            "poses": P, "inicio": {"pose": "diante"}, "destinos": D}


# ------------------------------------------------------------------------------------ subir com as mãos
def subir_maos(h: float = 1.0) -> dict:
    """Subir num bloco alto (face em z = 1,0, topo em y = h) com as duas mãos na borda.

    O joelho não pode subir de frente: com o quadril colado na face, a coxa varre a quina. Por
    isso o corpo primeiro sobe apoiado nos braços, com a perna direita aberta para o lado e o
    joelho já acima do topo (como a perna de trás na barreira), e só então o pé vem para cima.
    """
    maos = {"LeftHand": (0.21, h + MAO, 1.10), "RightHand": (-0.21, h + MAO, 1.12)}
    chao = {"LeftFoot": (0.1, PE, 0.56), "RightFoot": (-0.1, PE, 0.46)}
    lado = [["RightLeg", "RightShin", [-0.90, -0.12, 0.35]], ["RightShin", "RightFoot", [0.20, -0.02, -0.97]]]
    lado_e = [["LeftLeg", "LeftShin", [0.82, -0.42, 0.20]], ["LeftShin", "LeftFoot", [-0.10, -0.30, -0.95]]]
    pe_d = {"RightFoot": (-0.16, h + PE, 1.18)}
    P = {"em_pe": EM_PE, "diante": {"base": "em_pe", "lugar": [0, 0.56]},
         "maos_na_borda": pose(0.62, -0.08, 0.40, alc={**maos, **chao}),
         "impulso": pose(0.80, h + 0.22 - 1.012, 1.00, alc={**maos, "LeftFoot": (0.10, h - 0.66, 0.76)}, extra=lado, planos=()),
         "pe_em_cima": pose(0.90, h + 0.27 - 1.012, 0.90, alc={**maos, **pe_d, "LeftFoot": (0.10, h - 0.63, 0.86)}, planos=("RightFoot",)),
         "passa_o_peso": pose(1.00, h + 0.58 - 1.012, 0.45, x=-0.10, esq=0.6, dir=0.3, alc={**pe_d}, extra=lado_e, planos=("RightFoot",)),
         "em_cima": {"base": "em_pe", "lugar": [-0.04, 1.158], "altura": h}}
    D = [dest("maos_na_borda", antecipar=4, fixar=["LeftFoot", "RightFoot"], levar=["LeftHand", "RightHand"]),
         dest("impulso", tokens=7, antecipar=4, fixar=["LeftHand", "RightHand"], levar=["RightFoot"]),
         dest("pe_em_cima", tokens=6, antecipar=4, fixar=["LeftHand", "RightHand"], nivelar=["RightFoot"], levar=["RightFoot"]),
         dest("passa_o_peso", tokens=7, fixar=["RightFoot"], levar=["LeftFoot"]),
         dest("em_cima", tokens=8, antecipar=0, fixar=["RightFoot"], levar=["LeftFoot"])]
    return {"_descricao": f"Subir num bloco de {h} m com as mãos na borda: mãos em cima, o corpo sobe nos braços com a perna direita aberta para o lado, o pé direito apoia em cima, o peso passa para ele, a outra perna vem e fica em pé.",
            "obstaculos": [{"nome": "bloco", "centro": [0, h / 2, 1.6], "tamanho": [1.4, h, 1.2]}],
            "poses": P, "inicio": {"pose": "diante"}, "destinos": D}


# ------------------------------------------------------------------------------------ descer
def descer(h: float = 0.6) -> dict:
    """Descer de um bloco (topo em y = h para z < 0; o chão começa em z = 0).

    Com um pé em cima e o outro no chão o quadril tem que estar baixo: a perna de cima dobra
    fundo, senão a de baixo não alcança o chão (e o pé ficaria preso no ar pelo "fixar").
    """
    topo = {"LeftFoot": (0.1, h + PE, -0.20)}
    chao = {"RightFoot": (-0.1, PE, 0.34)}
    P = {"em_pe": EM_PE, "na_borda": {"base": "em_pe", "lugar": [0, -0.222], "altura": h},
         "pe_para_fora": pose(-0.12, h - 0.14, 0.14, esq=0.8, dir=-0.3, alc={**topo, "RightFoot": (-0.1, h + 0.06, 0.20)}),
         "pe_no_chao": pose(0.08, -0.06, 0.34, esq=0.9, dir=0.4, alc={**topo, **chao}),
         "passa_o_peso": pose(0.30, -0.12, 0.16, esq=-0.3, dir=0.7, alc={**chao, "LeftFoot": (0.1, 0.36, 0.12)}),
         "no_chao": {"base": "em_pe", "lugar": [0, 0.318]}}
    D = [dest("pe_para_fora", tokens=7, antecipar=5, fixar=["LeftFoot"], nivelar=["RightFoot"]),
         dest("pe_no_chao", tokens=7, antecipar=4, fixar=["LeftFoot"], nivelar=["RightFoot"], levar=["RightFoot"]),
         dest("passa_o_peso", tokens=7, fixar=["RightFoot"], nivelar=["LeftFoot"]),
         dest("no_chao", tokens=8, antecipar=0, fixar=["RightFoot"], nivelar=["LeftFoot"], levar=["LeftFoot"])]
    return {"_descricao": f"Descer de um bloco de {h} m: o pé direito sai da borda, a perna de cima dobra fundo até ele chegar no chão, o peso passa para ele, o pé esquerdo desce e fica em pé.",
            "obstaculos": [{"nome": "bloco", "centro": [0, h / 2, -0.6], "tamanho": [1.4, h, 1.2]}],
            "poses": P, "inicio": {"pose": "na_borda"}, "destinos": D}


# ------------------------------------------------------------------------------------ saltar muro
def saltar_muro(h: float = 0.8, fundo: float = 0.25) -> dict:
    """Saltar por cima de um muro baixo (face em z = 0, fundo em z = `fundo`, topo em y = h) com a mão
    esquerda apoiada em cima: o corpo tomba para o lado da mão e as pernas passam pela direita.

    As pernas sobem PELO LADO, ainda antes do muro (pose "pernas_sobem"), e só então cruzam por
    cima: subindo de frente, o pé esquerdo, que fica junto do muro, entra nele.
    """
    mao = {"LeftHand": (0.38, h + MAO, 0.12)}

    def tomba(k):
        return [["Hips", "Spine1", [0.55 * k, 1, 0.20]], ["Spine1", "Spine2", [0.75 * k, 1, 0.25]], ["Spine2", "Chest", [0.90 * k, 1, 0.30]]]
    livre = [["RightArm", "RightForeArm", [-0.60, 0.10, 0.50]], ["RightForeArm", "RightHand", [-0.20, 0.55, 0.60]]]
    P = {"em_pe": EM_PE, "diante": {"base": "em_pe", "lugar": [0, -0.70]},
         "mao_no_muro": pose(-0.42, -0.16, 0.60, dir=-0.5, alc={**mao, "LeftFoot": (0.14, PE, -0.40), "RightFoot": (-0.1, PE, -0.678)}),
         "pernas_sobem": {"base": "em_pe", "lugar": [-0.06, -0.20], "altura": h + 0.18 - 1.012, "mirar": tomba(0.7) + livre,
                          "alcancar": [["LeftHand", list(mao["LeftHand"])],
                                       ["RightFoot", [-0.76, h + 0.08, -0.20], [0, 0, 1]], ["LeftFoot", [-0.30, h + 0.10, -0.40], [-0.5, 0.7, 0.3]]],
                          "pe_plano": ["LeftFoot", "RightFoot"]},
         "pernas_por_cima": {"base": "em_pe", "lugar": [-0.05, 0.14], "altura": h + 0.30 - 1.012, "mirar": tomba(1.0) + livre,
                             "alcancar": [["LeftHand", list(mao["LeftHand"])],
                                          ["RightFoot", [-0.70, h + 0.24, 0.40], [0, 0, 1]], ["LeftFoot", [-0.55, h + 0.22, 0.18], [-0.5, 0.7, 0.3]]],
                             "pe_plano": ["LeftFoot", "RightFoot"]},
         "pousa": pose(0.62, -0.16, 0.30, x=-0.02, esq=0.5, dir=0.7, alc={"RightFoot": (-0.12, PE, 0.74), "LeftFoot": (0.10, PE, 0.52)}),
         "do_outro_lado": {"base": "em_pe", "lugar": [-0.02, 0.718]}}
    D = [dest("mao_no_muro", tokens=7, antecipar=4, fixar=["RightFoot"], levar=["LeftHand", "LeftFoot"]),
         dest("pernas_sobem", tokens=6, antecipar=3, fixar=["LeftHand"], levar=["RightFoot", "LeftFoot"], levar_desde=0.2),
         dest("pernas_por_cima", tokens=6, antecipar=3, fixar=["LeftHand"], levar=["RightFoot", "LeftFoot"], levar_desde=0.0),
         dest("pousa", tokens=7, antecipar=3, levar=["RightFoot", "LeftFoot"]),
         dest("do_outro_lado", tokens=8, antecipar=0, fixar=["RightFoot"], levar=["LeftFoot"])]
    return {"_descricao": f"Saltar por cima de um muro de {h} m apoiando a mão esquerda: mão em cima, as pernas sobem pelo lado direito, cruzam por cima com o corpo tombado para a esquerda, pousa do outro lado e levanta.",
            "obstaculos": [{"nome": "muro", "centro": [0, h / 2, fundo / 2], "tamanho": [1.8, h, fundo]}],
            "poses": P, "inicio": {"pose": "diante"}, "destinos": D}


# ------------------------------------------------------------------------------------ abaixar sob a barra
def abaixar_barra(vao: float = 1.15) -> dict:
    """Passar por baixo de uma barra (em z = 0, a parte de baixo a `vao` metros do chão) abaixando o corpo.

    Cada destino é um passo: um pé avança (levar) e o outro fica de apoio (fixar). A cabeça vai
    uns 45 cm à frente do quadril quando o tronco deita, então o corpo já está todo abaixado no
    passo em que a cabeça chega na barra, e só sobe depois que o quadril passou.
    """
    def tronco_baixo(k):   # k = 1: tronco deitado; 0.5: meio caminho
        return [["Hips", "Spine1", [0, 1 - 0.45 * k, 0.83 * k]], ["Spine1", "Spine2", [0, 1 - 0.55 * k, 0.89 * k]],
                ["Spine2", "Chest", [0, 1 - 0.60 * k, 0.92 * k]], ["Chest", "Neck1", [0, 1 - 0.80 * k, 0.98 * k]],
                ["Neck1", "Head", [0, 1 - 0.92 * k, 1.00 * k]]]

    def passo(z, k, desce, esq_z, dir_z, e=0.4, d=0.4):
        return {"base": "em_pe", "lugar": [0, z], "altura": desce, "mirar": tronco_baixo(k) + bracos(e, d, abre=0.2),
                "alcancar": [["LeftFoot", [0.11, PE, esq_z], [0, 0, 1]], ["RightFoot", [-0.11, PE, dir_z], [0, 0, 1]]],
                "pe_plano": ["LeftFoot", "RightFoot"]}
    a = -0.18                      # tudo um pouco antes da barra: o agachamento atrasa em relação à pose
    z0 = -1.45 + a
    P = {"em_pe": EM_PE, "antes": {"base": "em_pe", "lugar": [0, z0]},
         "passo1": passo(-1.17 + a, 0.6, -0.16, -0.95 + a, z0 + 0.022, e=-0.3, d=0.6),
         "passo2": passo(-0.67 + a, 1.0, -0.36, -0.95 + a, -0.40 + a, e=0.6, d=-0.2),
         "passo3": passo(-0.13 + a, 1.0, -0.36, 0.15 + a, -0.40 + a, e=-0.2, d=0.6),
         "passo4": passo(0.34 + a, 0.85, -0.28, 0.15 + a, 0.50 + a, e=0.6, d=-0.3),
         "depois": {"base": "em_pe", "lugar": [0, 0.478 + a]}}
    D = [dest("passo1", tokens=6, antecipar=4, fixar=["RightFoot"], levar=["LeftFoot"]),
         dest("passo2", tokens=7, antecipar=4, fixar=["LeftFoot"], levar=["RightFoot"]),
         dest("passo3", tokens=7, antecipar=4, fixar=["RightFoot"], levar=["LeftFoot"]),
         dest("passo4", tokens=6, antecipar=4, fixar=["LeftFoot"], levar=["RightFoot"]),
         dest("depois", tokens=7, antecipar=0, fixar=["RightFoot"], levar=["LeftFoot"])]
    return {"_descricao": f"Passar por baixo de uma barra com {vao} m de vão: dois passos abaixando o tronco e dobrando os joelhos, passa por baixo, e levanta em dois passos do outro lado.",
            "obstaculos": [{"nome": "barra", "centro": [0, vao + 0.06, 0], "tamanho": [1.8, 0.12, 0.12]}],
            "poses": P, "inicio": {"pose": "antes"}, "destinos": D}


# ------------------------------------------------------------------------------------ sentar e levantar
def _sentado(h):
    """Sentado na caixa: quadril 10 cm acima do assento, pés no chão no mesmo lugar em que estão em pé."""
    maos = [["LeftArm", "LeftForeArm", [0.20, -0.85, 0.40]], ["LeftForeArm", "LeftHand", [-0.10, -0.35, 0.93]],
            ["RightArm", "RightForeArm", [-0.20, -0.85, 0.40]], ["RightForeArm", "RightHand", [0.10, -0.35, 0.93]]]
    return {"base": "em_pe", "lugar": [0, -0.30], "altura": h + 0.10 - 1.012, "mirar": tronco(0.10) + maos,
            "alcancar": [["LeftFoot", [0.1, PE, 0.072], [0, 0.4, 1]], ["RightFoot", [-0.1, PE, 0.072], [0, 0.4, 1]]],
            "pe_plano": ["LeftFoot", "RightFoot"]}


def _meio(h):
    return pose(-0.14, -0.30, 0.55, esq=0.6, dir=0.6, alc={"LeftFoot": (0.1, PE, 0.072), "RightFoot": (-0.1, PE, 0.072)})


def sentar(h: float = 0.45) -> dict:
    """Sentar numa caixa que está logo atrás (topo em y = h, de z = -0,75 a z = -0,12)."""
    P = {"em_pe": EM_PE, "diante": {"base": "em_pe", "lugar": [0, 0.05]}, "desce": _meio(h), "sentado": _sentado(h)}
    D = [dest("desce", antecipar=6, fixar=["LeftFoot", "RightFoot"]), dest("sentado", tokens=9, antecipar=0, fixar=["LeftFoot", "RightFoot"])]
    return {"_descricao": f"Sentar numa caixa de {h} m que está atrás: inclina o tronco, leva o quadril para trás e senta, mãos nas coxas.",
            "obstaculos": [{"nome": "caixa", "centro": [0, h / 2, -0.435], "tamanho": [0.9, h, 0.63]}],
            "poses": P, "inicio": {"pose": "diante"}, "destinos": D}


def levantar(h: float = 0.45) -> dict:
    P = {"em_pe": EM_PE, "sentado": _sentado(h), "sobe": _meio(h), "de_pe": {"base": "em_pe", "lugar": [0, 0.05]}}
    D = [dest("sobe", antecipar=6, fixar=["LeftFoot", "RightFoot"]), dest("de_pe", tokens=9, antecipar=0, fixar=["LeftFoot", "RightFoot"])]
    return {"_descricao": f"Levantar de uma caixa de {h} m: inclina o tronco para a frente, tira o quadril do assento e fica em pé.",
            "obstaculos": [{"nome": "caixa", "centro": [0, h / 2, -0.435], "tamanho": [0.9, h, 0.63]}],
            "poses": P, "inicio": {"pose": "sentado"}, "destinos": D}


PLANOS = {"SubirBloco04": lambda: subir(0.4), "SubirBloco06": lambda: subir(0.6), "SubirBloco10": lambda: subir_maos(1.0),
          "DescerBloco06": lambda: descer(0.6), "SaltarMuro08": lambda: saltar_muro(0.8), "AbaixarBarra": abaixar_barra,
          "SentarCaixa": sentar, "LevantarCaixa": levantar}

if __name__ == "__main__":
    for nome in (sys.argv[1:] or list(PLANOS)):
        (AQUI / f"{nome}.json").write_text(json.dumps(PLANOS[nome](), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("plano", nome)
