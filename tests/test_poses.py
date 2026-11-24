"""Construtor de poses e tira de quadros do componente do MotionBricks, num esqueleto de teste."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extras" / "motionbricks"))
import poses  # noqa: E402
import tira  # noqa: E402

NAMES = ["Hips", "Spine1", "Head", "LeftArm", "LeftForeArm", "LeftHand",
         "LeftLeg", "LeftShin", "LeftFoot", "RightLeg", "RightShin", "RightFoot"]
PARENTS = [-1, 0, 1, 1, 3, 4, 0, 6, 7, 0, 9, 10]
OFFSETS = [[0, 1.0, 0], [0, 0.3, 0], [0, 0.3, 0], [0.2, 0.25, 0], [0.3, 0, 0], [0.25, 0, 0],
           [0.1, -0.05, 0], [0, -0.45, 0], [0, -0.43, 0], [-0.1, -0.05, 0], [0, -0.45, 0], [0, -0.43, 0]]
REST = np.concatenate([np.array(OFFSETS, dtype=float), np.tile([0, 0, 0, 1.0], (len(NAMES), 1))], axis=1)


@pytest.fixture
def sk():
    return poses.Skeleton(NAMES, PARENTS, REST)


def direction(world, sk, a, b):
    v = world[sk.index[b]] - world[sk.index[a]]
    return v / np.linalg.norm(v)


def test_mirar_aponta_o_osso_e_carrega_os_filhos(sk):
    built = poses.build_poses(sk, {"braco_baixo": {"mirar": [["LeftArm", "LeftForeArm", [0, -1, 0]]]}})
    world = built["braco_baixo"].world()
    assert np.allclose(direction(world, sk, "LeftArm", "LeftForeArm"), [0, -1, 0], atol=1e-6)
    # O antebraço não foi mirado: continua reto em relação ao braço e desce junto.
    assert np.allclose(direction(world, sk, "LeftForeArm", "LeftHand"), [0, -1, 0], atol=1e-6)
    # O comprimento dos ossos não muda.
    assert np.linalg.norm(world[sk.index["LeftHand"]] - world[sk.index["LeftArm"]]) == pytest.approx(0.55)
    # Os quatérnios saem normalizados e reproduzem a mesma pose.
    array = built["braco_baixo"].array()
    assert np.allclose(np.linalg.norm(array[:, 3:], axis=1), 1.0)
    assert np.allclose(sk.world_positions(array), world, atol=1e-6)


def test_direcao_oposta_e_base(sk):
    built = poses.build_poses(sk, {
        "a": {"mirar": [["LeftArm", "LeftForeArm", [-1, 0, 0]]]},          # meia volta exata
        "b": {"base": "a", "mirar": [["LeftForeArm", "LeftHand", [0, 1, 0]]]},
    })
    assert np.allclose(direction(built["a"].world(), sk, "LeftArm", "LeftForeArm"), [-1, 0, 0], atol=1e-6)
    wb = built["b"].world()
    assert np.allclose(direction(wb, sk, "LeftArm", "LeftForeArm"), [-1, 0, 0], atol=1e-6)
    assert np.allclose(direction(wb, sk, "LeftForeArm", "LeftHand"), [0, 1, 0], atol=1e-6)


def test_agachar_com_pe_plano_e_pes_no_chao(sk):
    spec = {"agachado": {
        "mirar": [["LeftLeg", "LeftShin", [0, -0.45, 0.89]], ["LeftShin", "LeftFoot", [0, -0.8, -0.6]],
                  ["RightLeg", "RightShin", [0, -0.45, 0.89]], ["RightShin", "RightFoot", [0, -0.8, -0.6]]],
        "pe_plano": ["LeftFoot", "RightFoot"], "pes_no_chao": True}}
    pose = poses.build_poses(sk, spec)["agachado"]
    world = pose.world()
    rest_foot = sk.rest_world_pos[sk.index["LeftFoot"]][1]
    assert world[sk.index["LeftFoot"]][1] == pytest.approx(rest_foot, abs=1e-6)
    assert world[0][1] < sk.rest_world_pos[0][1] - 0.2          # o quadril desceu
    world_rot, _ = sk.fk(pose.pos, pose.rot)
    assert np.allclose(world_rot[sk.index["LeftFoot"]], sk.rest_world_rot[sk.index["LeftFoot"]], atol=1e-6)
    salto = poses.build_poses(sk, {"salto": {"altura": 0.4}})["salto"].world()
    assert salto[0][1] == pytest.approx(1.4)


def test_planos_errados_sao_recusados(sk):
    cases = [
        ({"x": {"mirar": [["Braco", "LeftForeArm", [0, 1, 0]]]}}, "junta desconhecida"),
        ({"x": {"mirar": [["LeftArm", "LeftForeArm", [0, 0, 0]]]}}, "direção inválida"),
        ({"x": {"base": "depois"}}, "definida antes"),
        ({"x": {"girar": []}}, "campos desconhecidos"),
        ({"repouso": {}}, "escolha outro"),
        ({"x": {"mirar": [["LeftArm", "LeftForeArm"]]}}, "cada item de mirar"),
    ]
    for spec, message in cases:
        with pytest.raises(ValueError, match=message):
            poses.build_poses(sk, spec)


def test_medidas_e_tira(sk, tmp_path):
    frames = 30
    world = np.repeat(sk.rest_world_pos[None], frames, axis=0).copy()
    world[:, :, 2] += np.linspace(0, 1.5, frames)[:, None]       # desliza 1,5 m com o pé "plantado"
    world[10, sk.index["LeftFoot"], 1] -= 0.05                    # um quadro com o pé afundado
    contacts = np.tile([1.0, 1.0, 0.0, 0.0], (frames, 1))
    rest_foot = float(sk.rest_world_pos[sk.index["LeftFoot"]][1])
    m = tira.measure(world, contacts, NAMES, 30.0, rest_foot)
    assert m["quadros"] == 30 and m["pe_afunda_cm"] == pytest.approx(5.0, abs=0.1)
    assert m["deslize_do_pe_plantado_cm_s"]["esquerdo"] == pytest.approx(155.2, abs=1.0)
    assert m["deslize_do_pe_plantado_cm_s"]["direito"] is None
    assert m["fracao_com_algum_pe_plantado"] == 1.0
    out = tira.draw(tmp_path / "t.png", world, NAMES, PARENTS, [{"nome": "andar", "inicio": 0, "fim": 29}])
    from PIL import Image
    with Image.open(out) as img:
        assert img.size[0] > 1000 and img.size[1] == 630
        assert len(set(img.convert("RGB").getdata())) > 3           # tem desenho, não só fundo
