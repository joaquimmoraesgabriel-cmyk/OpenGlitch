"""Guia: pé apoiado preso, retarget por posições e trecho gerado seguindo o guia."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extras" / "motionbricks"))
import guia  # noqa: E402
import obstaculo  # noqa: E402
import poses  # noqa: E402

NAMES = ["Hips", "Spine1", "Head", "LeftArm", "LeftForeArm", "LeftHand", "RightArm", "RightForeArm", "RightHand",
         "LeftLeg", "LeftShin", "LeftFoot", "LeftToeBase", "RightLeg", "RightShin", "RightFoot", "RightToeBase"]
PARENTS = [-1, 0, 1, 1, 3, 4, 1, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15]
OFFSETS = [[0, 1.0, 0], [0, 0.3, 0], [0, 0.3, 0], [0.2, 0.25, 0], [0.3, 0, 0], [0.25, 0, 0],
           [-0.2, 0.25, 0], [-0.3, 0, 0], [-0.25, 0, 0],
           [0.1, -0.05, 0], [0, -0.45, 0], [0, -0.43, 0], [0, -0.05, 0.15],
           [-0.1, -0.05, 0], [0, -0.45, 0], [0, -0.43, 0], [0, -0.05, 0.15]]
REST = np.concatenate([np.array(OFFSETS, dtype=float), np.tile([0, 0, 0, 1.0], (len(NAMES), 1))], axis=1)


@pytest.fixture
def sk():
    return poses.Skeleton(NAMES, PARENTS, REST)


def walk(sk, frames=40):
    """O esqueleto de repouso deslizando para a frente, com o pé esquerdo escorregando no chão."""
    world = np.repeat(sk.rest_world_pos[None], frames, axis=0).copy()
    left = [sk.index[n] for n in NAMES if n.startswith("Left") and ("Foot" in n or "Toe" in n)]
    world[:, left, 2] += np.linspace(0.0, 0.04, frames)[:, None]          # 3 cm/s: apoiado, mas escorrega
    return world


def test_pe_apoiado_fica_parado(sk):
    world = walk(sk)
    fixed, report = guia.plant(world, NAMES, [])
    toe = sk.index["LeftToeBase"]
    assert np.ptp(world[:, toe, 2]) == pytest.approx(0.04)
    assert np.ptp(fixed[:, toe, 2]) < 1e-9
    assert report["LeftFoot"]["apoios"] == [[0, 39]]
    assert report["LeftFoot"]["escorregava_ate_cm"] == pytest.approx(2.0, abs=0.1)


def test_pe_no_ar_nao_e_preso(sk):
    world = walk(sk)
    foot = [sk.index[n] for n in NAMES if n.startswith("Left") and ("Foot" in n or "Toe" in n)]
    world[10:30, foot, 1] += 0.2                                          # passo: pé no ar
    marks = guia.contacts(world, NAMES, [])["LeftFoot"]
    assert marks[:9].all() and not marks[11:29].any() and marks[31:].all()


def test_pe_em_cima_da_caixa_conta_como_apoiado(sk):
    world = np.repeat(sk.rest_world_pos[None], 12, axis=0).copy()
    world[:, :, 1] += 0.5
    box = obstaculo.load([{"nome": "bloco", "centro": [0, 0.25, 0], "tamanho": [2, 0.5, 2]}])
    assert guia.contacts(world, NAMES, box)["LeftFoot"].all()
    assert not guia.contacts(world, NAMES, [])["LeftFoot"].any()


def test_retarget_poe_pes_e_maos_no_guia(sk):
    pose = poses.Pose(sk)
    pose.aim("LeftArm", "LeftForeArm", [0.3, -1, 0.4])
    pose.aim("RightLeg", "RightShin", [0, -1, 0.5])
    pose.pos[0] += [0.2, -0.1, 1.0]
    world = np.stack([sk.rest_world_pos, pose.world()])
    out = guia.retarget(sk, world)
    back = sk.world_positions(out)
    for name in guia.ENDS:
        assert np.linalg.norm(back[:, sk.index[name]] - world[:, sk.index[name]], axis=1).max() < 1e-3
    assert np.allclose(back[:, 0], world[:, 0])


def test_seguir_leva_quadril_e_pontas_ao_guia(sk):
    target = poses.Pose(sk)
    target.aim("LeftLeg", "LeftShin", [0, -1, 0.6])
    target.pos[0] += [0.0, -0.05, 0.3]
    world = np.repeat(target.world()[None], 5, axis=0)
    frames = np.repeat(poses.Pose(sk).array()[None], 5, axis=0)          # o modelo ficou em pé, parado
    out, report = guia.follow(sk, frames, world)
    back = sk.world_positions(out)
    assert np.allclose(back[:, 0], world[:, 0])
    assert np.linalg.norm(back[:, sk.index["LeftFoot"]] - world[:, sk.index["LeftFoot"]], axis=1).max() < 1e-3
    assert report["estava_longe_do_guia_cm"]["Hips"] == pytest.approx(30.4, abs=0.1)


def test_esticar_trecho_do_guia():
    world = np.arange(5, dtype=float).reshape(5, 1, 1) * np.ones((1, 2, 3))
    assert guia.resample(world, 9)[:, 0, 0] == pytest.approx(np.linspace(0, 4, 9))
    assert guia.resample(world, 5) is world


def test_guia_salvo_volta_na_ordem_do_esqueleto(sk, tmp_path):
    world = walk(sk, 6)
    order = list(reversed(range(len(NAMES))))
    guia.save(tmp_path / "g.npz", world[:, order], [NAMES[i] for i in order])
    assert np.allclose(guia.load(tmp_path / "g.npz", sk), world, atol=1e-6)
