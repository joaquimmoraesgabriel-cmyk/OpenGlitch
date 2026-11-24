"""Desenha uma tira de quadros do esqueleto, de lado e de frente, e mede o movimento.

É o jeito de conferir uma animação sem assistir: a IA olha a imagem e os números.
Depende de numpy e Pillow.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

HIDE = ("Thumb", "Index", "Middle", "Ring", "Pinky", "Eye", "Jaw")


def measure(world: np.ndarray, contacts: np.ndarray | None, names: list[str], fps: float,
            rest_foot_height: float) -> dict:
    """Medidas que denunciam problema: pé afundando ou deslizando, salto entre quadros."""
    index = {n: i for i, n in enumerate(names)}
    feet = [index[n] for n in ("LeftFoot", "RightFoot") if n in index]
    out: dict = {"quadros": int(len(world)), "segundos": round(len(world) / fps, 2)}
    if len(world) > 1:
        speed = np.linalg.norm(np.diff(world, axis=0), axis=2) * fps
        frame, joint = np.unravel_index(speed.argmax(), speed.shape)
        out["velocidade_maxima_m_s"] = round(float(speed.max()), 2)
        out["onde"] = f"{names[int(joint)]} no quadro {int(frame) + 1}"
    out["quadril_altura_min_max_m"] = [round(float(world[:, 0, 1].min()), 3), round(float(world[:, 0, 1].max()), 3)]
    if feet:
        lowest = float(world[:, feet, 1].min())
        out["pe_mais_baixo_m"] = round(lowest, 3)
        out["pe_afunda_cm"] = round(max(0.0, rest_foot_height - lowest) * 100, 1)
    if contacts is not None and len(feet) == 2 and len(world) > 1:
        slide = []
        for foot, column in zip(feet, (0, 2)):
            v = np.linalg.norm(np.diff(world[:, foot][:, [0, 2]], axis=0), axis=1) * fps
            planted = contacts[1:, column] > 0.5
            slide.append(round(float(v[planted].mean()) * 100, 1) if planted.any() else None)
        out["deslize_do_pe_plantado_cm_s"] = {"esquerdo": slide[0], "direito": slide[1]}
        out["fracao_com_algum_pe_plantado"] = round(float((contacts[:, [0, 2]].max(axis=1) > 0.5).mean()), 2)
    return out


def draw(path, world: np.ndarray, names: list[str], parents: list[int], segments: list[dict],
         columns: int = 8, scale: float = 150.0) -> str:
    """Grava um PNG com `columns` quadros por segmento, em duas linhas: de lado e de frente.

    segments: [{"nome": ..., "inicio": quadro, "fim": quadro}]. Vermelho é o lado esquerdo
    do personagem, azul o direito. Cada figura é centrada no quadril; quando o personagem
    se desloca, a posição dele à frente (z) vai escrita em cima de cada quadro.
    """
    from PIL import Image, ImageDraw

    hidden = {i for i, n in enumerate(names) if any(h in n for h in HIDE)}
    bones = [(i, p) for i, p in enumerate(parents) if p >= 0 and i not in hidden]
    head = names.index("Head") if "Head" in names else None
    cell_w, cell_h, margin = 210, 300, 150
    img = Image.new("RGB", (columns * cell_w + margin, len(segments) * 2 * cell_h + 30), "white")
    pen = ImageDraw.Draw(img)

    def figure(pose, cx, base, axis, origin):
        def xy(p):
            return cx + (p[axis] - origin) * scale, base - p[1] * scale
        pen.line([(cx - 95, base), (cx + 95, base)], fill=(175, 175, 175), width=1)
        for i, parent in bones:
            color = (40, 40, 40)
            if names[i].startswith("Left"):
                color = (200, 60, 40)
            elif names[i].startswith("Right"):
                color = (40, 80, 200)
            pen.line([xy(pose[parent]), xy(pose[i])], fill=color, width=3)
        if head is not None:
            hx, hy = xy(pose[head])
            pen.ellipse([hx - 9, hy - 22, hx + 9, hy - 4], outline=(40, 40, 40), width=2)

    for row, seg in enumerate(segments):
        a, b = int(seg["inicio"]), int(seg["fim"])
        frames = np.linspace(a, b, columns).round().astype(int)
        travel = float(np.ptp(world[a:b + 1, 0, 2]))
        for view, (axis, label) in enumerate(((2, "lado"), (0, "frente"))):
            top = (row * 2 + view) * cell_h
            base = top + cell_h - 20
            pen.text((6, top + 30), f"{seg['nome']}\n{label}\n{(b - a + 1) / 30:.2f} s", fill=(0, 0, 0))
            for col, frame in enumerate(frames):
                cx = margin + col * cell_w + cell_w // 2
                figure(world[frame], cx, base, axis, world[frame, 0, axis])
                note = f"q{frame - a}"
                if travel > 0.2:  # o desenho acompanha o quadril: o deslocamento vai escrito
                    note += f"  z={world[frame, 0, 2]:.2f} m"
                pen.text((cx - 40, top + 4), note, fill=(110, 110, 110))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    return str(path)
