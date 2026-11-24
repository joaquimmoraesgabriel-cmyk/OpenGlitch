"""Grava uma sequência de poses em BVH. Só depende de numpy.

Formato de entrada, o mesmo que o MotionBricks usa para o esqueleto SOMA:
cada pose é uma transformação local por junta, com posição XYZ em metros e
quatérnio XYZW, a raiz no índice zero, espaço Y para cima.

O BVH sai em centímetros e graus, com as rotações na ordem Y, X, Z
(q = qy * qx * qz). O leitor do MotionBricks e o Blender compõem os canais na
ordem em que são listados.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROTATION_CHANNELS = "Yrotation Xrotation Zrotation"
POSITION_CHANNELS = "Xposition Yposition Zposition"
POSITION_TOLERANCE_M = 1e-3
END_SITE_CM = 5.0


def quat_to_matrix(q: np.ndarray) -> np.ndarray:
    """Quatérnios XYZW (..., 4) para matrizes de rotação (..., 3, 3)."""
    q = q / np.linalg.norm(q, axis=-1, keepdims=True)
    x, y, z, w = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    m = np.empty(q.shape[:-1] + (3, 3), dtype=np.float64)
    m[..., 0, 0] = 1 - 2 * (y * y + z * z)
    m[..., 0, 1] = 2 * (x * y - z * w)
    m[..., 0, 2] = 2 * (x * z + y * w)
    m[..., 1, 0] = 2 * (x * y + z * w)
    m[..., 1, 1] = 1 - 2 * (x * x + z * z)
    m[..., 1, 2] = 2 * (y * z - x * w)
    m[..., 2, 0] = 2 * (x * z - y * w)
    m[..., 2, 1] = 2 * (y * z + x * w)
    m[..., 2, 2] = 1 - 2 * (x * x + y * y)
    return m


def matrix_to_euler(m: np.ndarray) -> np.ndarray:
    """Matrizes (..., 3, 3) para ângulos em graus (..., 3) na ordem Y, X, Z, com R = Ry Rx Rz.

    Y vem primeiro para o giro em volta do eixo vertical ter a volta inteira: é o movimento
    mais comum de um personagem, e na posição do meio ele ficaria limitado a 90 graus.
    """
    sx = np.clip(-m[..., 1, 2], -1.0, 1.0)
    x = np.arcsin(sx)
    locked = np.abs(sx) > 1.0 - 1e-7
    y = np.where(locked, np.arctan2(-m[..., 2, 0], m[..., 0, 0]), np.arctan2(m[..., 0, 2], m[..., 2, 2]))
    z = np.where(locked, 0.0, np.arctan2(m[..., 1, 0], m[..., 1, 1]))
    return np.degrees(np.stack([y, x, z], axis=-1))


def unwrap_degrees(angles: np.ndarray) -> np.ndarray:
    """Tira saltos de 360 graus ao longo do tempo, para as curvas não darem volta."""
    return np.degrees(np.unwrap(np.radians(angles), axis=0))


def _children(parents: list[int]) -> list[list[int]]:
    kids: list[list[int]] = [[] for _ in parents]
    for index, parent in enumerate(parents):
        if parent >= 0:
            kids[parent].append(index)
    return kids


def write_bvh(path, joint_names, parents, rest_local, poses, fps: float = 30.0) -> dict:
    """Grava o BVH e devolve um resumo.

    Args:
        path: arquivo de saída.
        joint_names: nome de cada junta; a raiz é a de índice zero.
        parents: índice do pai de cada junta, -1 para a raiz.
        rest_local: pose de referência, (J, 7), posição em metros e quatérnio XYZW.
        poses: (F, J, 7), transformações locais por quadro.
        fps: quadros por segundo.
    """
    names = [str(n) for n in joint_names]
    parents = [int(p) for p in parents]
    rest = np.asarray(rest_local, dtype=np.float64).reshape(len(names), 7)
    poses = np.asarray(poses, dtype=np.float64)
    if poses.ndim != 3 or poses.shape[1:] != (len(names), 7):
        raise ValueError(f"poses precisa ser (quadros, {len(names)}, 7); veio {poses.shape}")
    if parents[0] != -1 or any(p < 0 for p in parents[1:]):
        raise ValueError("a raiz precisa ser a junta de índice zero e a única sem pai")
    if any(p >= i for i, p in enumerate(parents) if i):
        raise ValueError("cada junta precisa vir depois do pai dela")
    if len(set(names)) != len(names):
        raise ValueError("nomes de junta repetidos")

    frames = poses.shape[0]
    # Juntas cuja posição local muda no tempo ganham canais de posição; as outras só giram.
    drift = np.abs(poses[:, :, :3] - rest[None, :, :3]).max(axis=(0, 2))
    with_position = [i == 0 or drift[i] > POSITION_TOLERANCE_M for i in range(len(names))]
    eulers = unwrap_degrees(matrix_to_euler(quat_to_matrix(poses[:, :, 3:7])))
    kids = _children(parents)

    lines = ["HIERARCHY"]

    def emit(index: int, depth: int) -> None:
        pad = "  " * depth
        lines.append(f"{pad}{'ROOT' if index == 0 else 'JOINT'} {names[index]}")
        lines.append(pad + "{")
        offset = rest[index, :3] * 100.0
        lines.append(f"{pad}  OFFSET {offset[0]:.6f} {offset[1]:.6f} {offset[2]:.6f}")
        if with_position[index]:
            lines.append(f"{pad}  CHANNELS 6 {POSITION_CHANNELS} {ROTATION_CHANNELS}")
        else:
            lines.append(f"{pad}  CHANNELS 3 {ROTATION_CHANNELS}")
        if kids[index]:
            for child in kids[index]:
                emit(child, depth + 1)
        else:
            # Ponta de cadeia: dá comprimento ao osso na direção em que ele já vinha.
            direction = rest[index, :3]
            norm = np.linalg.norm(direction)
            tip = direction / norm * END_SITE_CM if norm > 1e-6 else np.array([0.0, END_SITE_CM, 0.0])
            lines.extend([f"{pad}  End Site", pad + "  {",
                          f"{pad}    OFFSET {tip[0]:.6f} {tip[1]:.6f} {tip[2]:.6f}", pad + "  }"])
        lines.append(pad + "}")

    emit(0, 0)
    order: list[int] = []

    def walk(index: int) -> None:
        order.append(index)
        for child in kids[index]:
            walk(child)

    walk(0)
    lines += ["MOTION", f"Frames: {frames}", f"Frame Time: {1.0 / fps:.8f}"]
    for frame in range(frames):
        row: list[str] = []
        for index in order:
            if with_position[index]:
                row += [f"{v:.6f}" for v in poses[frame, index, :3] * 100.0]
            row += [f"{v:.6f}" for v in eulers[frame, index]]
        lines.append(" ".join(row))

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return {
        "arquivo": str(path), "quadros": frames, "fps": fps, "segundos": round(frames / fps, 3),
        "juntas": len(names),
        "juntas_com_posicao": [names[i] for i, flag in enumerate(with_position) if flag],
    }


def write_contacts(path, foot_contacts, fps: float = 30.0) -> None:
    """Grava a confiança de contato dos pés por quadro: calcanhar e ponta, esquerdo e direito."""
    values = np.asarray(foot_contacts, dtype=np.float64).reshape(-1, 4)
    data = {
        "fps": fps,
        "colunas": ["calcanhar_esquerdo", "ponta_esquerda", "calcanhar_direito", "ponta_direita"],
        "juntas_soma": ["LeftFoot", "LeftToeBase", "RightFoot", "RightToeBase"],
        "quadros": [[round(float(v), 4) for v in row] for row in values],
    }
    Path(path).write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")
