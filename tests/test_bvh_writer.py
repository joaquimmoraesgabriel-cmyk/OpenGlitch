"""O gravador de BVH do componente opcional do MotionBricks, conferido por cinemática direta."""

import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "extras" / "motionbricks" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bvh = _load("bvh_writer")

NAMES = ["Hips", "Spine", "Head", "LeftUpLeg", "LeftLeg", "LeftFoot"]
PARENTS = [-1, 0, 1, 0, 3, 4]
REST = np.array([
    [0, 0.95, 0, 0, 0, 0, 1], [0, 0.20, 0.02, 0, 0, 0, 1], [0, 0.45, 0, 0, 0, 0, 1],
    [0.09, -0.05, 0, 0, 0, 0, 1], [0, -0.42, 0.01, 0, 0, 0, 1], [0, -0.43, 0, 0, 0, 0, 1],
], dtype=float)


def _quat(axis, degrees):
    half = math.radians(degrees) / 2
    axis = np.asarray(axis, dtype=float) / np.linalg.norm(axis)
    return np.concatenate([axis * math.sin(half), [math.cos(half)]])


def _poses(frames=40):
    rng = np.random.default_rng(7)
    poses = np.repeat(REST[None], frames, axis=0)
    for f in range(frames):
        t = f / (frames - 1)
        poses[f, 0, :3] = [0.5 * t, 0.95 + 0.03 * math.sin(6 * t), 2.0 * t]
        poses[f, 0, 3:] = _quat([0, 1, 0], 200 * t)            # passa de 180 graus: testa o unwrap
        poses[f, 1, 3:] = _quat([1, 0.2, 0.1], 25 * math.sin(4 * t))
        poses[f, 2, 3:] = _quat(rng.normal(size=3), 40 * t)
        poses[f, 3, 3:] = _quat([1, 0, 0], -70 * t)
        poses[f, 4, 3:] = _quat([1, 0, 0], 89.9999 * t)
        poses[f, 5, 3:] = _quat([0, 0, 1], 90 * t)              # chega ao travamento em Y? não: gira em Z
    poses[:, 4, 3:] = [_quat([0, 1, 0], 90 * f / (frames - 1)) for f in range(frames)]  # Y a 90: gimbal
    return poses


def _fk(parents, poses):
    world_r = np.empty(poses.shape[:2] + (3, 3))
    world_p = np.empty(poses.shape[:2] + (3,))
    local_r = bvh.quat_to_matrix(poses[:, :, 3:7])
    for j, parent in enumerate(parents):
        if parent < 0:
            world_r[:, j], world_p[:, j] = local_r[:, j], poses[:, j, :3]
        else:
            world_r[:, j] = world_r[:, parent] @ local_r[:, j]
            world_p[:, j] = world_p[:, parent] + np.einsum("fij,fj->fi", world_r[:, parent], poses[:, j, :3])
    return world_p


def _read_back(path):
    """Leitor mínimo de BVH: devolve nomes, pais e as poses locais (metros, XYZW)."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    names, parents, offsets, channels, stack, in_end = [], [], [], [], [], False
    i = 0
    while lines[i].strip() != "MOTION":
        tok = lines[i].split()
        if tok and tok[0] in ("ROOT", "JOINT"):
            names.append(tok[1]); parents.append(stack[-1] if stack else -1)
            stack.append(len(names) - 1); offsets.append(None); channels.append([])
        elif tok[:2] == ["End", "Site"]:
            in_end = True
        elif tok and tok[0] == "OFFSET" and not in_end:
            offsets[stack[-1]] = [float(v) for v in tok[1:4]]
        elif tok and tok[0] == "CHANNELS":
            channels[stack[-1]] = tok[2:]
        elif tok and tok[0] == "}":
            if in_end:
                in_end = False
            else:
                stack.pop()
        i += 1
    frames = int(lines[i + 1].split()[1])
    frame_time = float(lines[i + 2].split()[2])
    data = np.array([[float(v) for v in row.split()] for row in lines[i + 3:i + 3 + frames]])
    poses = np.zeros((frames, len(names), 7))
    col = 0
    for j, chans in enumerate(channels):
        poses[:, j, :3] = np.array(offsets[j]) / 100.0
        rot = np.repeat(np.eye(3)[None], frames, axis=0)
        for chan in chans:
            values = data[:, col]; col += 1
            if chan.endswith("position"):
                poses[:, j, "XYZ".index(chan[0])] = values / 100.0
            else:
                axis = np.eye(3)["XYZ".index(chan[0])]
                step = bvh.quat_to_matrix(np.array([_quat(axis, v) for v in values]))
                rot = rot @ step  # mesma composição do leitor do MotionBricks: na ordem listada
        poses[:, j, 3:] = [0, 0, 0, 1]
        poses[:, j, 3:] = _matrix_to_quat(rot)
    return names, parents, poses, frame_time


def _matrix_to_quat(m):
    w = np.sqrt(np.clip(1 + m[:, 0, 0] + m[:, 1, 1] + m[:, 2, 2], 1e-12, None)) / 2
    return np.stack([(m[:, 2, 1] - m[:, 1, 2]) / (4 * w), (m[:, 0, 2] - m[:, 2, 0]) / (4 * w),
                     (m[:, 1, 0] - m[:, 0, 1]) / (4 * w), w], axis=1)


def test_bvh_preserva_as_posicoes_no_mundo(tmp_path):
    poses = _poses()
    summary = bvh.write_bvh(tmp_path / "a.bvh", NAMES, PARENTS, REST, poses, fps=30)
    assert summary["quadros"] == 40 and summary["juntas"] == 6
    assert summary["juntas_com_posicao"] == ["Hips"]
    names, parents, read, frame_time = _read_back(tmp_path / "a.bvh")
    assert names == NAMES and parents == PARENTS
    assert frame_time == pytest.approx(1 / 30, abs=1e-6)
    error = np.abs(_fk(PARENTS, read) - _fk(PARENTS, poses)).max()
    assert error < 1e-4, f"erro máximo de {error * 1000:.3f} mm"


def test_bvh_canais_sem_saltos_e_juntas_que_se_movem(tmp_path):
    poses = _poses()
    poses[:, 1, 1] += np.linspace(0, 0.05, poses.shape[0])  # a coluna estica 5 cm
    summary = bvh.write_bvh(tmp_path / "b.bvh", NAMES, PARENTS, REST, poses)
    assert summary["juntas_com_posicao"] == ["Hips", "Spine"]
    text = (tmp_path / "b.bvh").read_text(encoding="utf-8")
    assert "CHANNELS 6 Xposition Yposition Zposition Yrotation Xrotation Zrotation" in text
    assert text.count("End Site") == 2  # Head e LeftFoot
    names, parents, read, _ = _read_back(tmp_path / "b.bvh")
    assert np.abs(_fk(PARENTS, read) - _fk(PARENTS, poses)).max() < 1e-4
    yaw = bvh.unwrap_degrees(bvh.matrix_to_euler(bvh.quat_to_matrix(poses[:, 0, 3:7])))
    assert np.abs(np.diff(yaw, axis=0)).max() < 30  # sem volta de 360 no meio da curva


def test_bvh_recusa_entrada_errada(tmp_path):
    poses = _poses()
    with pytest.raises(ValueError, match="poses precisa ser"):
        bvh.write_bvh(tmp_path / "c.bvh", NAMES, PARENTS, REST, poses[:, :3])
    with pytest.raises(ValueError, match="depois do pai"):
        bvh.write_bvh(tmp_path / "c.bvh", NAMES, [-1, 2, 1, 0, 3, 4], REST, poses)
    with pytest.raises(ValueError, match="repetidos"):
        bvh.write_bvh(tmp_path / "c.bvh", ["A"] * 6, PARENTS, REST, poses)


def test_contatos(tmp_path):
    bvh.write_contacts(tmp_path / "c.json", np.array([[1, 0.5, 0, 0], [0, 0, 1, 0.25]]))
    data = json.loads((tmp_path / "c.json").read_text(encoding="utf-8"))
    assert data["colunas"][0] == "calcanhar_esquerdo" and data["quadros"][1] == [0.0, 0.0, 1.0, 0.25]
