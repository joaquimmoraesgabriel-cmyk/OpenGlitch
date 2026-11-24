"""Confere uma animação contra os obstáculos da cena. Só depende de numpy.

O MotionBricks não recebe a geometria da cena: ele só vê as poses pedidas, e o
corpo passa por onde o caminho entre elas for mais natural, inclusive por dentro
de uma parede. Este módulo é o que pega isso: mede, quadro a quadro, quanto cada
osso entrou em cada obstáculo, e a que distância mãos e pés ficaram das
superfícies no fim de cada trecho.

Um obstáculo é uma caixa, no mesmo espaço das poses (+Y para cima, +Z para a
frente do personagem, +X para o lado esquerdo dele, metros):

    {"nome": "bloco", "centro": [0, 0.5, 1.5], "tamanho": [1.2, 1.0, 1.0], "giro": 0}

`centro` é o meio da caixa, `tamanho` é [largura em X, altura em Y, fundo em Z]
e `giro` são graus em volta de Y.
"""

from __future__ import annotations

import math

import numpy as np

HIDE = ("Thumb", "Index", "Middle", "Ring", "Pinky", "Eye", "Jaw")
ENDS = ("LeftHand", "RightHand", "LeftFoot", "RightFoot", "LeftToeBase", "RightToeBase")


class Box:
    def __init__(self, spec: dict):
        unknown = set(spec) - {"nome", "centro", "tamanho", "giro"}
        if unknown:
            raise ValueError(f"obstáculo: campos desconhecidos {sorted(unknown)}")
        self.name = str(spec.get("nome", "obstaculo"))
        self.center = np.asarray(spec["centro"], dtype=float)
        self.half = np.asarray(spec["tamanho"], dtype=float) / 2.0
        if self.center.shape != (3,) or self.half.shape != (3,) or (self.half <= 0).any():
            raise ValueError(f"obstáculo {self.name}: centro e tamanho são [x, y, z], com tamanho positivo")
        self.turn = float(spec.get("giro", 0.0))
        c, s = math.cos(math.radians(self.turn)), math.sin(math.radians(self.turn))
        self.rot = np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])  # local para mundo

    def local(self, points: np.ndarray) -> np.ndarray:
        return (np.asarray(points, dtype=float) - self.center) @ self.rot

    def depth(self, points: np.ndarray) -> np.ndarray:
        """Quanto cada ponto está dentro da caixa, em metros: zero fora, positivo dentro."""
        inside = self.half - np.abs(self.local(points))
        return np.clip(inside.min(axis=-1), 0.0, None)

    def distance(self, points: np.ndarray) -> np.ndarray:
        """Distância de cada ponto até a superfície da caixa: positiva fora, negativa dentro."""
        q = np.abs(self.local(points)) - self.half
        outside = np.linalg.norm(np.clip(q, 0.0, None), axis=-1)
        return outside + np.minimum(q.max(axis=-1), 0.0)

    def exit(self, point, margin: float = 0.0, lift: bool = False, lift_bias: float = 0.12) -> np.ndarray:
        """O menor deslocamento que tira um ponto de dentro da caixa (zero se já está fora).

        Sai pela face mais próxima, nunca por baixo. Com `lift`, sair por cima ganha mesmo
        custando até `lift_bias` metros a mais: é o pé, que passa por cima da quina em vez de
        ser empurrado para trás. `margin` é a folga além da superfície.
        """
        local = self.local(np.asarray(point, dtype=float))
        inside = self.half - np.abs(local)
        if (inside <= 0.0).any():
            return np.zeros(3)
        options = []                                     # (distância, eixo, sentido)
        for axis in (0, 2):
            options.append((float(inside[axis]), axis, 1.0 if local[axis] >= 0.0 else -1.0))
        up = float(self.half[1] - local[1])
        options.append((up - (lift_bias if lift else 0.0), 1, 1.0))
        _, axis, sign = min(options)
        distance = up if axis == 1 else float(inside[axis])
        move = np.zeros(3)
        move[axis] = sign * (distance + margin)
        return move @ self.rot.T

    def corners(self) -> np.ndarray:
        signs = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], dtype=float)
        return self.center + (signs * self.half) @ self.rot.T

    def top(self) -> float:
        return float(self.center[1] + self.half[1])


def load(specs) -> list[Box]:
    boxes = [Box(s) for s in (specs or [])]
    names = [b.name for b in boxes]
    if len(set(names)) != len(names):
        raise ValueError("obstáculos com o mesmo nome")
    return boxes


def check(world: np.ndarray, names: list[str], parents: list[int], boxes: list[Box], marks: list[dict] | None = None,
          tolerance: float = 0.03, samples: int = 5) -> dict:
    """Mede a penetração de cada osso em cada obstáculo ao longo da animação.

    world: (quadros, juntas, 3). Cada osso é testado em `samples` pontos entre a junta e o
    pai, para pegar uma canela que atravessa a quina sem que joelho nem tornozelo entrem.
    Dedos ficam de fora. `tolerance` é a penetração aceita, em metros: o esqueleto não tem
    espessura e mão e pé apoiados costumam entrar um pouco na superfície.
    """
    world = np.asarray(world, dtype=float)
    bones = [(i, p) for i, p in enumerate(parents) if p >= 0 and not any(h in names[i] for h in HIDE)]
    out: dict = {"folga_aceita_cm": round(tolerance * 100, 1), "obstaculos": [], "passou": True}
    if not boxes:
        return out
    weights = np.linspace(0.0, 1.0, samples)
    for box in boxes:
        worst, where, frames_in = 0.0, None, set()
        per_bone: dict[str, float] = {}
        for joint, parent in bones:
            points = world[:, parent, None, :] + (world[:, joint, None, :] - world[:, parent, None, :]) * weights[:, None]
            depth = box.depth(points).max(axis=1)                      # (quadros,)
            deepest = float(depth.max())
            if deepest > tolerance:
                per_bone[names[joint]] = round(deepest * 100, 1)
                frames_in.update(int(f) for f in np.nonzero(depth > tolerance)[0])
            if deepest > worst:
                worst, where = deepest, f"{names[joint]} no quadro {int(depth.argmax())}"
        frames = sorted(frames_in)
        entry = {"nome": box.name, "penetracao_maxima_cm": round(worst * 100, 1), "onde": where,
                 "quadros_atravessando": len(frames),
                 "trechos": _ranges(frames),
                 "ossos": dict(sorted(per_bone.items(), key=lambda kv: -kv[1])[:8])}
        if marks and frames:
            entry["destinos_afetados"] = [m["nome"] for m in marks
                                          if any(m["inicio"] <= f <= m["fim"] for f in frames)]
        out["obstaculos"].append(entry)
        if frames:
            out["passou"] = False
    if marks:
        index = {n: i for i, n in enumerate(names)}
        out["apoios_no_fim"] = []
        for mark in marks:
            pose = world[mark["fim"]]
            item = {"destino": mark["nome"]}
            for name in ENDS:
                if name not in index:
                    continue
                p = pose[index[name]]
                near = min(boxes, key=lambda b: abs(float(b.distance(p))))
                item[name] = {"altura_cm": round(float(p[1]) * 100, 1),
                              "obstaculo_mais_perto": near.name,
                              "distancia_cm": round(float(near.distance(p)) * 100, 1)}
            out["apoios_no_fim"].append(item)
    return out


def _ranges(frames: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for f in frames:
        if out and f == out[-1][1] + 1:
            out[-1][1] = f
        else:
            out.append([f, f])
    return out
