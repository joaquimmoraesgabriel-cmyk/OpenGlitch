"""Confere uma animação gerada pelo Kimodo e tira dela as poses-chave de um plano do gerar.py.

Só depende de numpy; roda em qualquer ambiente:

    python kimodo_para_plano.py --npz andar.npz --bvh andar.bvh --saida plano.json

O Kimodo gera movimento a partir de texto, no mesmo esqueleto SOMA de 77 juntas do
MotionBricks, mas não enxerga a cena e nem sempre faz o que o texto pede. Por isso ele entra
como RASCUNHO: daqui saem a conferência do rascunho e as poses-chave; quem gera a animação
final entre elas é o MotionBricks (gerar.py), com as conferências e correções de lá.

O caminho inteiro:

    1. kimodo_gen "texto" --duration 5 --bvh --output rascunho      (ambiente do Kimodo)
    2. este script, com --plano-base se houver obstáculos: lê o relatório. Se o rascunho não
       presta (não fez o pedido, pé escorregando, corpo dentro do obstáculo), gere outro.
    3. blender_cena.py --plano plano.json --bvh rascunho.bvh: olhar o rascunho na cena. Se
       alguma pose precisar de ajuste, ajuste no Blender e use blender_exportar.py
       (--ignorar Root) no lugar do plano deste script.
    4. gerar.py plano.json: o MotionBricks gera entre as poses-chave.

O que se usa do .npz do Kimodo é "posed_joints", a posição no mundo de cada junta em cada
quadro (metros, +Y para cima, +Z para a frente, +X para a esquerda: o mesmo espaço do plano).
Não se usa rotação: as proporções do esqueleto do Kimodo diferem um pouco das do MotionBricks,
e o gerar.py remonta as rotações pelas posições (poses.fit_positions). O .bvh só dá os nomes e
a hierarquia das juntas; a junta "Root" que o Kimodo põe acima do quadril é descartada.

Quadros-chave: com --quadros auto, um a cada --intervalo segundos, puxado para o instante mais
parado ali perto (pose de passagem lenta é melhor destino que pose no meio de um balanço). O
primeiro quadro é o início e o último é sempre destino. Cada destino recebe "tokens" para a
geração do MotionBricks durar o mesmo que o trecho do rascunho (o modelo aceita de 0,6 a 1,9 s).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obstaculo  # noqa: E402

DROP = ("Root",)
FPS = 30.0


def read_hierarchy(path: Path) -> tuple[list[str], list[int]]:
    """Nomes e pais das juntas de um BVH, na ordem do arquivo."""
    names: list[str] = []
    parents: list[int] = []
    stack: list[int] = []
    pending = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        word = line.split()
        if not word:
            continue
        if word[0] in ("ROOT", "JOINT"):
            pending = len(names)
            names.append(word[1])
            parents.append(stack[-1] if stack else -1)
        elif word[0] == "End":
            pending = -1                                   # ponta: não é junta
        elif word[0] == "{":
            stack.append(pending if pending is not None and pending >= 0 else -2)
        elif word[0] == "}":
            stack.pop()
        elif word[0] == "MOTION":
            break
    parents = [p if p != -2 else -1 for p in parents]
    return names, parents


def load(npz: Path, bvh: Path) -> tuple[np.ndarray, list[str], list[int]]:
    names, parents = read_hierarchy(bvh)
    keep = [i for i, n in enumerate(names) if n not in DROP]
    remap = {old: new for new, old in enumerate(keep)}

    def up(i: int) -> int:                                  # pai mais próximo que ficou
        p = parents[i]
        while p >= 0 and p not in remap:
            p = parents[p]
        return remap[p] if p >= 0 else -1

    names2, parents2 = [names[i] for i in keep], [up(i) for i in keep]
    world = np.asarray(np.load(npz)["posed_joints"], dtype=float)
    if world.ndim == 4:                                     # várias amostras num arquivo só
        world = world[0]
    if world.shape[1] != len(names2):
        raise SystemExit(f"o .npz tem {world.shape[1]} juntas e o .bvh, sem {DROP}, tem {len(names2)}")
    return world, names2, parents2


def check(world: np.ndarray, names: list[str], parents: list[int], boxes: list, tolerance: float) -> dict:
    """Mede o rascunho: quanto anda, se sobe, pés abaixo do chão, pés escorregando, obstáculos."""
    hips = world[:, names.index("Hips")]
    out: dict = {
        "quadros": int(len(world)), "segundos": round(len(world) / FPS, 2),
        "quadril_deslocamento_m": [round(float(v), 2) for v in hips[-1] - hips[0]],
        "quadril_altura_m": {"inicio": round(float(hips[0, 1]), 2), "fim": round(float(hips[-1, 1]), 2),
                             "minima": round(float(hips[:, 1].min()), 2), "maxima": round(float(hips[:, 1].max()), 2)},
    }
    feet = {}
    for side in ("Left", "Right"):
        toe, ankle = world[:, names.index(f"{side}ToeBase")], world[:, names.index(f"{side}Foot")]
        floor = np.array([obstaculo.support_height(boxes, p) for p in toe])
        low = toe[:, 1] - floor                                         # altura da ponta sobre o apoio
        planted = (low[1:] < 0.03) & (low[:-1] < 0.03)
        slide = np.linalg.norm((toe[1:] - toe[:-1])[:, [0, 2]], axis=1) * FPS      # m/s
        feet[f"{side}Foot"] = {
            "mais_alto_cm": round(float((ankle[:, 1]).max()) * 100, 1),
            "abaixo_do_apoio_cm": round(float(max(0.0, -low.min())) * 100, 1),
            "quadros_apoiado": int(planted.sum()),
            "escorrega_apoiado_cm_s": {"mediana": round(float(np.median(slide[planted])) * 100, 1),
                                       "p90": round(float(np.percentile(slide[planted], 90)) * 100, 1)} if planted.any() else None,
        }
    out["pes"] = feet
    if boxes:
        out["obstaculos"] = obstaculo.check(world, names, parents, boxes, tolerance=tolerance)
    return out


def pick_frames(world: np.ndarray, names: list[str], interval: float, window: float = 0.25) -> list[int]:
    """Um quadro a cada `interval` segundos, puxado para o mais parado dentro de `window`."""
    body = [i for i, n in enumerate(names) if not any(h in n for h in obstaculo.HIDE)]
    speed = np.linalg.norm(world[1:, body] - world[:-1, body], axis=2).mean(axis=1)
    speed = np.concatenate([speed, speed[-1:]])
    last = len(world) - 1
    count = max(1, int(round(last / (interval * FPS))))
    reach = int(round(window * FPS))
    frames = [0]
    for k in range(1, count):
        centre = int(round(k * last / count))
        lo, hi = max(frames[-1] + 18, centre - reach), min(last - 18, centre + reach)
        if lo > hi:
            continue
        frames.append(lo + int(speed[lo:hi + 1].argmin()))
    frames.append(last)
    return frames


def tokens_for(frames: int) -> int:
    """Duração da geração do MotionBricks mais próxima do trecho: quadros = tokens x 4 - 6."""
    return int(min(16, max(6, round((frames + 6) / 4))))


def build_plan(world: np.ndarray, names: list[str], frames: list[int], base: dict, anticipate: int | None) -> dict:
    plan = dict(base)
    labels = [f"q{f:03d}" for f in frames]
    plan["poses"] = {label: {"posicoes": {n: [round(float(v), 4) for v in world[f, i]] for i, n in enumerate(names)}}
                     for label, f in zip(labels, frames)}
    plan["inicio"] = {"pose": labels[0]}
    plan["destinos"] = [{"nome": label, "pose": label, "tokens": tokens_for(f - previous)}
                        for label, f, previous in zip(labels[1:], frames[1:], frames[:-1])]
    if anticipate is not None:
        plan["antecipar"] = anticipate
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Confere um rascunho do Kimodo e tira as poses-chave para o gerar.py.")
    parser.add_argument("--npz", type=Path, required=True, help="saída do kimodo_gen")
    parser.add_argument("--bvh", type=Path, required=True, help="o .bvh da mesma geração (nomes e hierarquia)")
    parser.add_argument("--saida", type=Path, required=True, help="plano a escrever")
    parser.add_argument("--quadros", default="auto", help="\"auto\" ou uma lista 0,35,70 (o primeiro é o início)")
    parser.add_argument("--intervalo", type=float, default=1.0, help="segundos entre poses-chave no modo auto")
    parser.add_argument("--plano-base", type=Path, help="plano de onde vêm os obstáculos e os demais campos")
    parser.add_argument("--antecipar", type=int, help="grava \"antecipar\" no plano (poses viram pontos de passagem)")
    parser.add_argument("--folga", type=float, default=0.03, help="penetração aceita, em metros")
    args = parser.parse_args()

    world, names, parents = load(args.npz, args.bvh)
    base = json.loads(args.plano_base.read_text(encoding="utf-8")) if args.plano_base else {}
    boxes = obstaculo.load(base.get("obstaculos"))
    report = check(world, names, parents, boxes, args.folga)

    frames = pick_frames(world, names, args.intervalo) if args.quadros == "auto" else [int(v) for v in args.quadros.split(",")]
    if len(frames) < 2 or frames != sorted(set(frames)) or frames[-1] >= len(world):
        raise SystemExit(f"quadros inválidos: {frames} (a animação tem {len(world)})")
    gaps = [b - a for a, b in zip(frames[:-1], frames[1:])]
    report["quadros_chave"] = frames
    report["trechos_fora_do_alcance"] = [[a, b] for a, b in zip(frames[:-1], frames[1:]) if not 18 <= b - a <= 58]
    plan = build_plan(world, names, frames, base, args.antecipar)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(plan, ensure_ascii=False) + "\n", encoding="utf-8")
    report["plano"] = str(args.saida)
    report["trechos_quadros"] = gaps
    args.saida.with_suffix(".rascunho.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("RASCUNHO " + json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
