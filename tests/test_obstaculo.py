"""Conferência de obstáculos e poses por posição do componente do MotionBricks."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extras" / "motionbricks"))
import obstaculo  # noqa: E402
import poses  # noqa: E402
import tira  # noqa: E402
from test_poses import NAMES, PARENTS, REST  # noqa: E402


@pytest.fixture
def sk():
    return poses.Skeleton(NAMES, PARENTS, REST)


def test_caixa_mede_dentro_e_fora():
    box = obstaculo.Box({"nome": "bloco", "centro": [0, 0.5, 2.0], "tamanho": [1.0, 1.0, 1.0]})
    assert box.depth(np.array([0.0, 0.5, 2.0])) == pytest.approx(0.5)
    assert box.depth(np.array([0.0, 0.9, 2.0])) == pytest.approx(0.1)
    assert box.depth(np.array([0.0, 1.2, 2.0])) == 0.0
    assert box.distance(np.array([0.0, 1.2, 2.0])) == pytest.approx(0.2)
    assert box.distance(np.array([0.0, 0.9, 2.0])) == pytest.approx(-0.1)
    assert box.top() == pytest.approx(1.0)
    # Girada 45 graus, a quina avança: um ponto fora da caixa reta passa a estar dentro.
    turned = obstaculo.Box({"centro": [0, 0.5, 0], "tamanho": [1.0, 1.0, 1.0], "giro": 45})
    assert turned.depth(np.array([0.0, 0.5, 0.6])) > 0.05
    assert obstaculo.Box({"centro": [0, 0.5, 0], "tamanho": [1.0, 1.0, 1.0]}).depth(np.array([0.0, 0.5, 0.6])) == 0.0
    assert np.allclose(sorted(turned.corners()[:, 1]), [0, 0, 0, 0, 1, 1, 1, 1])


def test_obstaculos_errados_sao_recusados():
    with pytest.raises(ValueError, match="tamanho positivo"):
        obstaculo.Box({"centro": [0, 0, 0], "tamanho": [1, 0, 1]})
    with pytest.raises(ValueError, match="campos desconhecidos"):
        obstaculo.Box({"centro": [0, 0, 0], "tamanho": [1, 1, 1], "altura": 2})
    with pytest.raises(ValueError, match="mesmo nome"):
        obstaculo.load([{"nome": "a", "centro": [0, 0, 0], "tamanho": [1, 1, 1]},
                        {"nome": "a", "centro": [3, 0, 0], "tamanho": [1, 1, 1]}])


def test_andar_atraves_da_parede_e_pego(sk, tmp_path):
    frames = 40
    world = np.repeat(sk.rest_world_pos[None], frames, axis=0).copy()
    world[:, :, 2] += np.linspace(0.0, 3.0, frames)[:, None]            # anda 3 m para a frente
    marks = [{"nome": "antes", "inicio": 0, "fim": 14}, {"nome": "parede", "inicio": 15, "fim": 39}]
    wall = obstaculo.load([{"nome": "parede", "centro": [0, 1.0, 2.0], "tamanho": [2.0, 2.0, 0.3]}])
    result = obstaculo.check(world, NAMES, PARENTS, wall, marks)
    assert result["passou"] is False
    entry = result["obstaculos"][0]
    assert entry["penetracao_maxima_cm"] == pytest.approx(15.0, abs=1.5)   # meia espessura da parede
    assert entry["destinos_afetados"] == ["parede"]
    assert entry["trechos"][0][0] > 14 and entry["quadros_atravessando"] >= 3
    assert "Hips" in entry["onde"] or entry["ossos"]
    # A mesma caminhada com a parede fora do caminho passa.
    clear = obstaculo.load([{"nome": "parede", "centro": [3.0, 1.0, 2.0], "tamanho": [2.0, 2.0, 0.3]}])
    result = obstaculo.check(world, NAMES, PARENTS, clear, marks)
    assert result["passou"] is True and result["obstaculos"][0]["quadros_atravessando"] == 0
    assert result["apoios_no_fim"][1]["LeftFoot"]["obstaculo_mais_perto"] == "parede"
    out = tira.draw(tmp_path / "t.png", world, NAMES, PARENTS, marks, boxes=wall)
    from PIL import Image
    with Image.open(out) as img:
        greens = sum(1 for p in img.convert("RGB").getdata() if p == (40, 150, 70))
    assert greens > 200                                                  # a parede foi desenhada


def test_canela_atravessando_a_quina_e_pega(sk):
    # Joelho e tornozelo ficam fora da caixa; só o meio da canela passa por dentro.
    world = sk.rest_world_pos[None].copy()
    knee, ankle = sk.index["LeftShin"], sk.index["LeftFoot"]
    middle = (world[0, knee] + world[0, ankle]) / 2
    box = obstaculo.load([{"nome": "quina", "centro": list(middle), "tamanho": [0.2, 0.2, 0.2]}])
    assert box[0].depth(world[0, knee]) == 0.0 and box[0].depth(world[0, ankle]) == 0.0
    result = obstaculo.check(world, NAMES, PARENTS, box)
    assert result["passou"] is False and "LeftFoot" in result["obstaculos"][0]["ossos"]


def test_alcancar_leva_mao_e_pe_ao_ponto(sk):
    hand, foot = [0.3, 1.2, 0.35], [0.1, 0.5, 0.4]            # borda de um bloco e o topo dele
    pose = poses.build_poses(sk, {"apoio": {
        "lugar": [0.0, 0.0], "alcancar": [["LeftHand", hand], ["LeftFoot", foot, [0, 0, 1]]],
        "pe_plano": ["LeftFoot"]}})["apoio"]
    world = pose.world()
    assert np.allclose(world[sk.index["LeftHand"]], hand, atol=1e-6)
    assert np.allclose(world[sk.index["LeftFoot"]], foot, atol=1e-6)
    # O joelho dobra para a frente, como pedido, e os ossos não esticam.
    assert world[sk.index["LeftShin"]][2] > 0.1
    assert np.linalg.norm(world[sk.index["LeftShin"]] - world[sk.index["LeftLeg"]]) == pytest.approx(0.45)
    # Fora do alcance: o braço estica na direção do ponto e a função diz quanto faltou.
    far = poses.Pose(sk)
    missing = far.reach("LeftHand", [3.0, 1.55, 0.0])
    assert missing == pytest.approx(3.0 - 0.2 - 0.55, abs=1e-3)
    assert far.world()[sk.index["LeftHand"]][0] == pytest.approx(0.75, abs=1e-3)
    # lugar põe o quadril no ponto da cena, e a ponta continua no ponto do mundo pedido.
    moved = poses.build_poses(sk, {"la": {"lugar": [0.2, 1.5], "alcancar": [["LeftHand", [0.5, 1.2, 1.8]]]}})["la"]
    assert np.allclose(moved.world()[0], [0.2, 1.0, 1.5]) and np.allclose(moved.world()[sk.index["LeftHand"]], [0.5, 1.2, 1.8], atol=1e-6)
    with pytest.raises(ValueError, match="dois ossos"):
        poses.Pose(sk).reach("Spine1", [0, 2, 0])


def test_pose_por_posicoes_reproduz_a_pose(sk):
    original = poses.build_poses(sk, {"agachado": {
        "mirar": [["Hips", "Spine1", [0.1, 1, 0.3]], ["LeftArm", "LeftForeArm", [0.3, -1, 0.4]],
                  ["LeftForeArm", "LeftHand", [0, 0.2, 1]], ["LeftLeg", "LeftShin", [0, -0.45, 0.89]],
                  ["LeftShin", "LeftFoot", [0, -0.8, -0.6]], ["RightLeg", "RightShin", [0.2, -1, 0.1]]],
        "altura": -0.2}})["agachado"]
    original.pos[0, 0], original.pos[0, 2] = 0.7, 2.5                    # fora da origem
    world = original.world()
    targets = {name: list(world[i]) for i, name in enumerate(NAMES)}
    rebuilt = poses.build_poses(sk, {"do_blender": {"posicoes": targets}})["do_blender"]
    assert np.allclose(rebuilt.world(), world, atol=1e-6)
    array = rebuilt.array()
    assert np.allclose(np.linalg.norm(array[:, 3:], axis=1), 1.0)
    assert np.allclose(sk.world_positions(array), world, atol=1e-6)
    # Posições com outras proporções: os ossos não esticam e as direções são as pedidas.
    longer = {name: list(np.asarray(p) * 1.2) for name, p in targets.items()}
    scaled = poses.build_poses(sk, {"maior": {"posicoes": longer}})["maior"].world()
    a, b = sk.index["LeftForeArm"], sk.index["LeftHand"]
    assert np.linalg.norm(scaled[b] - scaled[a]) == pytest.approx(0.25)
    wanted = np.asarray(longer["LeftHand"]) - np.asarray(longer["LeftForeArm"])
    assert np.allclose((scaled[b] - scaled[a]) / 0.25, wanted / np.linalg.norm(wanted), atol=1e-6)
    with pytest.raises(ValueError, match="junta desconhecida"):
        poses.build_poses(sk, {"x": {"posicoes": {"Rabo": [0, 0, 0]}}})
