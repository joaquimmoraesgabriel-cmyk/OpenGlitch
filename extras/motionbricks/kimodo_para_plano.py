"""Confere uma animação gerada pelo Kimodo e tira dela as poses-chave de um plano do gerar.py.

Só depende de numpy; roda em qualquer ambiente:

    python kimodo_para_plano.py --npz andar.npz --bvh andar.bvh --saida plano.json

O Kimodo gera movimento a partir de texto, no mesmo esqueleto SOMA de 77 juntas do
MotionBricks, mas não enxerga a cena e nem sempre faz o que o texto pede. Por isso ele entra
como RASCUNHO: daqui saem a conferência do rascunho e as poses-chave; quem gera a animação
final entre elas é o MotionBricks (gerar.py), com as conferências e correções de lá.

O caminho inteiro:

    1. kimodo_gen "texto" --duration 5 --bvh --num_samples 3 --output rascunho   (ambiente do Kimodo)
    2. este script, com --plano-base (obstáculos) e --encaixar: lê o relatório. Se o rascunho
       não fez o pedido, gere outro; não conserte.
    3. blender_cena.py --plano plano.json --bvh rascunho.bvh: olhar o rascunho na cena.
    4. gerar.py plano.json: encaixado, com os pés presos e fora dos obstáculos.

O plano sai com "guia" (veja guia.py): o rascunho inteiro, quadro a quadro, que a animação
segue. O que se usa do .npz do Kimodo é "posed_joints", a posição no mundo de cada junta
(metros, +Y para cima, +Z para a frente, +X para a esquerda: o mesmo espaço do plano). Não se
usa rotação: as proporções do esqueleto do Kimodo diferem um pouco, e as rotações são
remontadas pelas posições. O .bvh só dá os nomes e a hierarquia; a junta "Root" que o Kimodo
põe acima do quadril é descartada.

--modo inteiro (padrão): a animação é o rascunho corrigido. --refazer 2,3 entrega esses trechos
ao MotionBricks, que gera entre a pose do começo e a do fim deles: é para o pedaço ruim do
rascunho. Os trechos são definidos por --quadros: "auto" põe um corte a cada --intervalo
segundos, no instante mais parado ali perto; um trecho refeito precisa ter de 18 a 58 quadros.

--encaixar 0.4 procura, até 0,4 m em X e Z, o lugar do rascunho na cena que menos atravessa os
obstáculos e deixa os pés apoiados no começo e no fim. --apoio Hips:cadeira acrescenta um
apoio que não é pé (quem termina sentado).
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
    report_feet = obstaculo.feet_on_support(world, names, boxes, float(min(world[0, names.index(f"{s}Foot"), 1] for s in ("Left", "Right"))), tolerance=0.05)
    out["pes_no_apoio_comeco_e_fim"] = report_feet["passou"]
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


def fit(world: np.ndarray, names: list[str], parents: list[int], boxes: list, reach: float, tolerance: float,
        rests: list[tuple[str, str, int]] = ()) -> tuple[np.ndarray, dict]:
    """Encaixa o rascunho na cena: procura o deslocamento [x, z], até `reach` metros, em que o
    corpo menos atravessa os obstáculos e os pés começam e terminam apoiados.

    O modelo imagina o obstáculo do texto ("sobe numa caixa") num lugar que ninguém sabe qual é.
    Posto a olho, um erro de 10 cm põe o joelho da perna de apoio dentro da face da caixa, e a
    correção automática abre a perna para o lado. Aqui a posição é medida: para cada
    deslocamento soma-se, quadro a quadro, a penetração mais funda, com multa se algum pé
    começa ou termina fora do apoio (no ar, ou com a ponta enterrada).

    `rests` são apoios que o movimento tem de ter além dos pés: (junta, caixa, quadro), por
    exemplo ("Hips", "cadeira", -1) para quem termina sentado. Sem isso, o lugar que menos
    atravessa a cadeira é longe dela. A junta tem de ficar a até 15 cm da superfície da caixa.
    """
    by_name = {box.name: box for box in boxes}
    for joint, box, _ in rests:
        if joint not in names or box not in by_name:
            raise SystemExit(f"apoio {joint}:{box}: junta ou obstáculo desconhecido")
    main = [i for i, n in enumerate(names) if not any(h in n for h in obstaculo.HIDE)]
    bones = [(i, parents[i]) for i in main if parents[i] >= 0]
    child, parent = np.array([b[0] for b in bones]), np.array([b[1] for b in bones])
    weights = np.linspace(0.0, 1.0, 4)[:, None]
    points = world[:, parent, None, :] + (world[:, child, None, :] - world[:, parent, None, :]) * weights
    rest_ankle = float(min(world[0, names.index(f"{s}Foot"), 1] for s in ("Left", "Right")))

    def score(shift: np.ndarray) -> tuple[float, float, bool]:
        moved = points + shift
        depth = np.max([box.depth(moved) for box in boxes], axis=0).max(axis=(1, 2))       # por quadro
        feet = obstaculo.feet_on_support(world + shift, names, boxes, rest_ankle, tolerance=0.05)["passou"]
        far = sum(max(0.0, abs(float(by_name[box].distance(world[frame, names.index(joint)] + shift))) - 0.15)
                  for joint, box, frame in rests)
        return float(depth.sum()) + (0.0 if feet else 1000.0) + 1000.0 * far, float(depth.max()), feet and far == 0.0

    best = None
    for step, span, centre in ((0.05, reach, np.zeros(3)), (0.01, 0.05, None)):
        centre = best[1] if centre is None else centre
        for dx in np.arange(-span, span + 1e-9, step):
            for dz in np.arange(-span, span + 1e-9, step):
                shift = centre + np.array([dx, 0.0, dz])
                total, deepest, feet = score(shift)
                # empate: o menor deslocamento
                key = (round(total, 4), float(np.linalg.norm(shift)))
                if best is None or key < best[0]:
                    best = (key, shift, deepest, feet)
    before = score(np.zeros(3))
    report = {"deslocamento_m": [round(float(best[1][0]), 2), round(float(best[1][2]), 2)],
              "penetracao_maxima_cm": {"antes": round(before[1] * 100, 1), "depois": round(best[2] * 100, 1)},
              "apoios_certos": {"antes": before[2], "depois": best[3]}}
    return world + best[1], report


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


def build_plan(world: np.ndarray, names: list[str], frames: list[int], base: dict, anticipate: int | None,
               guide_file: Path, mode: str, free: set[int]) -> dict:
    """Plano com guia: cada destino aponta um quadro do rascunho, e o trecho até ele segue o
    rascunho (`mode`) ou, se estiver em `free`, é refeito pelo MotionBricks entre as duas poses."""
    import guia
    guia.save(guide_file, world, names)
    plan = dict(base)
    plan["guia"] = {"arquivo": str(guide_file), "modo": mode}
    plan["inicio"] = {"quadro_guia": frames[0]}
    plan["destinos"] = []
    for number, (f, previous) in enumerate(zip(frames[1:], frames[:-1]), 1):
        spec = {"nome": f"q{f:03d}", "quadro_guia": f}
        if number in free:
            spec["guia"] = "nao"
        if number in free or mode == "pontas":
            spec["tokens"] = tokens_for(f - previous)
        plan["destinos"].append(spec)
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
    parser.add_argument("--modo", choices=("inteiro", "pontas"), default="inteiro",
                        help="inteiro: a animação é o rascunho, corrigido; pontas: o MotionBricks gera e "
                             "quadril, mãos e pés seguem o rascunho")
    parser.add_argument("--refazer", default="", help="trechos (1 = até o primeiro destino) que o MotionBricks "
                                                      "refaz sozinho, por exemplo 2,3: o pedaço ruim do rascunho")
    parser.add_argument("--encaixar", type=float, default=0.0,
                        help="procura, até tantos metros, o lugar do rascunho na cena que menos atravessa os "
                             "obstáculos e deixa os pés apoiados (0 = não mexe)")
    parser.add_argument("--apoio", default="", help="com --encaixar: apoios além dos pés, JUNTA:caixa[:quadro], "
                                                    "por exemplo Hips:cadeira para quem termina sentado")
    parser.add_argument("--folga", type=float, default=0.03, help="penetração aceita, em metros")
    args = parser.parse_args()

    world, names, parents = load(args.npz, args.bvh)
    base = json.loads(args.plano_base.read_text(encoding="utf-8")) if args.plano_base else {}
    boxes = obstaculo.load(base.get("obstaculos"))
    fitted = None
    if args.encaixar > 0 and boxes:
        rests = []
        for item in filter(None, args.apoio.split(",")):
            part = item.split(":")
            rests.append((part[0], part[1], int(part[2]) if len(part) > 2 else -1))
        world, fitted = fit(world, names, parents, boxes, args.encaixar, args.folga, rests)
    report = check(world, names, parents, boxes, args.folga)
    if fitted:
        report["encaixe"] = fitted

    frames = pick_frames(world, names, args.intervalo) if args.quadros == "auto" else [int(v) for v in args.quadros.split(",")]
    if len(frames) < 2 or frames != sorted(set(frames)) or frames[-1] >= len(world):
        raise SystemExit(f"quadros inválidos: {frames} (a animação tem {len(world)})")
    gaps = [b - a for a, b in zip(frames[:-1], frames[1:])]
    report["quadros_chave"] = frames
    free = {int(v) for v in args.refazer.split(",") if v.strip()}
    report["trechos_fora_do_alcance"] = [[a, b] for n, (a, b) in enumerate(zip(frames[:-1], frames[1:]), 1)
                                         if (n in free or args.modo == "pontas") and not 18 <= b - a <= 58]
    plan = build_plan(world, names, frames, base, args.antecipar, args.saida.with_suffix(".guia.npz"), args.modo, free)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    report["plano"] = str(args.saida)
    report["trechos_quadros"] = gaps
    args.saida.with_suffix(".rascunho.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("RASCUNHO " + json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
