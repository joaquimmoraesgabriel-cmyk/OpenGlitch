"""Guia: um movimento de referência, quadro a quadro, que a animação final segue.

Só depende de numpy.

O problema que isto resolve: o gerar.py dá ao MotionBricks poses soltas, e o caminho entre
elas é o modelo que inventa. Se o caminho inventado passa por dentro do obstáculo, o desvio
automático empurra pés e joelhos depois, e o resultado é a perna abrindo para o lado. Quando
existe um movimento de referência com o caminho inteiro (um rascunho do Kimodo, uma captura,
uma animação feita no Blender), o caminho não precisa ser inventado.

Um guia é a posição no mundo de cada junta em cada quadro, a 30 quadros por segundo, no espaço
do plano (+Y para cima, +Z para a frente, +X para a esquerda, metros). Arquivo .npz com
"posicoes" (quadros, juntas, 3) e "juntas" (os nomes). Não se usa rotação: as proporções do
esqueleto de origem podem diferir, e as rotações são remontadas no esqueleto de destino.

Três usos, por trecho da animação (campo "guia" do destino no plano do gerar.py):

  "inteiro"  o trecho É o guia, passado para o esqueleto (retarget). O MotionBricks não gera
             nada ali. Dura o que o guia dura, sem o limite de 0,6 a 1,9 s.
  "pontas"   o MotionBricks gera o trecho; depois o quadril é levado ao do guia e mãos e pés
             aos pontos do guia, por IK. O tronco e a cabeça ficam os do modelo.
  "nao"      o MotionBricks gera sozinho entre a pose do começo e a do fim do trecho. É para o
             pedaço do guia que saiu ruim: as poses das pontas vêm do guia, o meio não.

Antes de qualquer uso o guia passa por plant(): o pé que está apoiado fica parado no mundo.
Movimento gerado por modelo quase sempre tem o pé apoiado escorregando alguns centímetros por
segundo, e isso vale para qualquer tipo de animação.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

import obstaculo
from poses import Pose, Skeleton, quat_to_matrix, stable_bend

FPS = 30.0
ENDS = ("LeftFoot", "RightFoot", "LeftHand", "RightHand")
TOES = {"LeftFoot": "LeftToeBase", "RightFoot": "RightToeBase"}


def save(path: Path, world: np.ndarray, names: list[str]) -> None:
    np.savez_compressed(path, posicoes=np.asarray(world, dtype=np.float32), juntas=np.array(names))


def load(path: Path, skeleton: Skeleton) -> np.ndarray:
    """Lê um guia e o devolve na ordem das juntas do esqueleto: (quadros, juntas, 3)."""
    data = np.load(path)
    names = [str(n) for n in data["juntas"]]
    missing = [n for n in skeleton.names if n not in names]
    if missing:
        raise SystemExit(f"guia {path}: faltam juntas do esqueleto, por exemplo {missing[:5]}")
    world = np.asarray(data["posicoes"], dtype=float)
    return world[:, [names.index(n) for n in skeleton.names]]


def contacts(world: np.ndarray, names: list[str], boxes: list, height: float = 0.045, speed: float = 0.35,
             shortest: int = 4) -> dict[str, np.ndarray]:
    """Por pé, em que quadros ele está apoiado: ponta baixa sobre o apoio e quase parada."""
    out = {}
    for foot, toe_name in TOES.items():
        if foot not in names or toe_name not in names:
            continue
        toe = world[:, names.index(toe_name)]
        floor = np.array([obstaculo.support_height(boxes, p) for p in toe])
        step = np.linalg.norm(np.diff(toe, axis=0), axis=1) * FPS
        moving = np.concatenate([step[:1], np.maximum(step[1:], step[:-1]), step[-1:]]) if len(step) else np.zeros(len(toe))
        on = (toe[:, 1] - floor < height) & (moving < speed)
        # apoio curto demais é ruído; buraco curto dentro de um apoio também
        for value, limit in ((False, 2), (True, shortest)):
            start = None
            for f in range(len(on) + 1):
                inside = f < len(on) and on[f] == value
                if inside and start is None:
                    start = f
                elif not inside and start is not None:
                    if f - start < limit and start > 0 and f < len(on):
                        on[start:f] = not value
                    start = None
        out[foot] = on
    return out


def plant(world: np.ndarray, names: list[str], boxes: list, blend: int = 4) -> tuple[np.ndarray, dict]:
    """Prende no mundo o pé apoiado. Devolve o guia corrigido e, por pé, o que mudou.

    Em cada apoio a ponta do pé fica no ponto mediano do apoio; o tornozelo guarda a posição que
    tinha em relação à ponta, então o calcanhar ainda levanta no fim do passo. A correção entra e
    sai em `blend` quadros, para o pé não dar um tranco ao pousar e ao sair.
    """
    world = np.asarray(world, dtype=float).copy()
    marks = contacts(world, names, boxes)
    report = {}
    for foot, on in marks.items():
        ankle, toe = names.index(foot), names.index(TOES[foot])
        chain = [ankle, toe] + [i for i, n in enumerate(names) if n == TOES[foot].replace("Base", "End")]
        shift = np.zeros((len(world), 3))
        weight = np.zeros(len(world))
        spans, worst = [], 0.0
        start = None
        for f in range(len(on) + 1):
            if f < len(on) and on[f]:
                start = f if start is None else start
                continue
            if start is None:
                continue
            anchor = np.median(world[start:f, toe], axis=0)
            floor = obstaculo.support_height(boxes, anchor)
            anchor[1] = max(anchor[1], floor)                   # ponta nunca abaixo do apoio
            for g in range(max(0, start - blend), min(len(world), f + blend)):
                w = 1.0 if start <= g < f else 1.0 - (min(abs(g - start), abs(g - (f - 1))) / (blend + 1.0))
                if w > weight[g]:
                    weight[g], shift[g] = w, anchor - world[g, toe]
            worst = max(worst, float(np.linalg.norm(world[start:f, toe] - anchor, axis=1).max()))
            spans.append([int(start), int(f - 1)])
            start = None
        for j in chain:
            world[:, j] += shift * weight[:, None]
        report[foot] = {"apoios": spans, "escorregava_ate_cm": round(worst * 100, 1)}
    return world, report


def contact_table(world: np.ndarray, names: list[str], boxes: list) -> np.ndarray:
    """Contato dos pés no formato do MotionBricks: calcanhar e ponta, esquerdo e direito."""
    marks = contacts(world, names, boxes)
    out = np.zeros((len(world), 4))
    for column, foot in ((0, "LeftFoot"), (2, "RightFoot")):
        if foot in marks:
            out[:, column] = out[:, column + 1] = marks[foot].astype(float)
    return out


def _set_ends(skeleton: Skeleton, pose: Pose, targets: np.ndarray, joints, weight: float = 1.0) -> None:
    """Leva mãos e pés aos pontos do guia por IK e aponta o pé para onde a ponta dele está."""
    for name in joints:
        if name not in skeleton.index:
            continue
        j = skeleton.index[name]
        world_rot, world_pos = skeleton.fk(pose.pos, pose.rot)
        keep = world_rot[j].copy()
        pose.reach(name, world_pos[j] + weight * (targets[j] - world_pos[j]),
                   bend=stable_bend(skeleton, world_rot, world_pos, name))
        world_rot, _ = skeleton.fk(pose.pos, pose.rot)
        pose.rot[j] = world_rot[skeleton.parents[j]].T @ keep       # a ponta guarda a orientação
        toe = TOES.get(name)
        if toe in skeleton.index and weight >= 1.0:
            direction = targets[skeleton.index[toe]] - targets[j]
            if np.linalg.norm(direction) > 1e-6:
                pose.aim(name, toe, direction)


def retarget(skeleton: Skeleton, world: np.ndarray) -> np.ndarray:
    """Guia (quadros, juntas, 3) para poses locais (quadros, juntas, 7) no esqueleto.

    As rotações saem das posições (Pose.fit_positions). Como as proporções podem diferir, pés e
    mãos são levados depois, por IK, exatamente aos pontos do guia: é ali que o erro aparece (pé
    acima do chão, mão fora do apoio); no cotovelo e no joelho ninguém vê um centímetro.
    """
    out = np.empty((len(world), len(skeleton.names), 7))
    for f, frame in enumerate(world):
        pose = Pose(skeleton)
        pose.fit_positions({n: frame[i] for i, n in enumerate(skeleton.names)})
        _set_ends(skeleton, pose, frame, ENDS)
        out[f] = pose.array()
    for j in range(len(skeleton.names)):                             # quatérnios sem troca de sinal
        for f in range(1, len(out)):
            if float(np.dot(out[f, j, 3:], out[f - 1, j, 3:])) < 0.0:
                out[f, j, 3:] *= -1.0
    return out


def resample(world: np.ndarray, count: int) -> np.ndarray:
    """Estica ou encolhe um trecho do guia para `count` quadros."""
    if len(world) == count:
        return world
    at = np.linspace(0.0, len(world) - 1.0, count)
    low = np.floor(at).astype(int)
    high = np.minimum(low + 1, len(world) - 1)
    t = (at - low)[:, None, None]
    return world[low] * (1.0 - t) + world[high] * t


def follow(skeleton: Skeleton, frames: np.ndarray, world: np.ndarray, joints=ENDS, hips: bool = True) -> tuple[np.ndarray, dict]:
    """Faz um trecho gerado seguir o guia: quadril no lugar do guia, mãos e pés nos pontos dele.

    frames: (F, J, 7) do MotionBricks; world: o trecho do guia, já com F quadros. Devolve os
    quadros e quanto, no pior quadro, cada ponta estava longe do guia antes da correção.
    """
    frames = np.asarray(frames, dtype=float).copy()
    before = skeleton.world_positions(frames)
    report = {"Hips": round(float(np.linalg.norm(before[:, 0] - world[:, 0], axis=1).max()) * 100, 1)}
    for name in joints:
        if name in skeleton.index:
            j = skeleton.index[name]
            report[name] = round(float(np.linalg.norm(before[:, j] - world[:, j], axis=1).max()) * 100, 1)
    for f in range(len(frames)):
        pose = Pose(skeleton)
        pose.pos, pose.rot = frames[f, :, :3].copy(), quat_to_matrix(frames[f, :, 3:])
        if hips:
            pose.pos[0] = world[f, 0]
        _set_ends(skeleton, pose, world[f], joints)
        frames[f] = pose.array()
    return frames, {"estava_longe_do_guia_cm": report}
