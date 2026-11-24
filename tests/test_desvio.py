"""Desvio automático dos obstáculos, pino de IK ("levar"), âncora do "fixar" e pés no apoio."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "extras" / "motionbricks"))
import obstaculo  # noqa: E402
import poses  # noqa: E402
from test_poses import NAMES, PARENTS, REST  # noqa: E402


@pytest.fixture
def sk():
    return poses.Skeleton(NAMES, PARENTS, REST)


def leg_frames(sk, ankles, bend=(0, 0, 1)):
    """Um quadro por ponto: a perna esquerda com o tornozelo em cada um, joelho para a frente."""
    frames = []
    for ankle in ankles:
        pose = poses.Pose(sk)
        pose.reach("LeftFoot", ankle, list(bend))
        frames.append(pose.array())
    return np.array(frames)


def test_sair_da_caixa_pela_face_mais_proxima_ou_por_cima():
    box = obstaculo.Box({"centro": [0, 0.5, 0], "tamanho": [1.0, 1.0, 1.0]})
    assert not box.exit([0.0, 1.2, 0.0]).any()                                # fora: nada a fazer
    side = box.exit([0.0, 0.5, 0.45], margin=0.01)
    assert side == pytest.approx([0, 0, 0.06])                                # sai pela face da frente
    low = box.exit([0.0, 0.05, 0.0])                                          # perto do chão, no meio
    assert low.any() and low[1] >= 0                                          # sai, e nunca por baixo
    lifted = box.exit([0.0, 0.92, 0.45], lift=True)
    assert lifted == pytest.approx([0, 0.08, 0])                              # o pé prefere passar por cima


def test_desvio_tira_a_canela_da_quina(sk):
    # Bloco à frente: o tornozelo fica antes da face e abaixo do topo, o joelho dobra por cima
    # do bloco, e a canela corta a quina. É a perna de trás subindo num bloco alto.
    boxes = obstaculo.load([{"nome": "bloco", "centro": [0.1, 0.25, 0.45], "tamanho": [0.6, 0.5, 0.5]}])
    ankles = [[0.1, 0.20, z] for z in np.linspace(0.06, 0.18, 12)]
    frames = leg_frames(sk, ankles)
    before = obstaculo.check(sk.world_positions(frames), NAMES, PARENTS, boxes)
    assert before["passou"] is False and before["obstaculos"][0]["penetracao_maxima_cm"] > 3
    fixed, report = poses.avoid(sk, frames, boxes)
    after = obstaculo.check(sk.world_positions(fixed), NAMES, PARENTS, boxes)
    assert after["passou"] is True
    assert report["LeftFoot"]["quadros"] > 0
    # A perna direita e o tronco não foram tocados; os ossos da esquerda não esticaram.
    world = sk.world_positions(fixed)
    assert np.allclose(fixed[:, sk.index["RightLeg"]], frames[:, sk.index["RightLeg"]])
    thigh = np.linalg.norm(world[:, sk.index["LeftShin"]] - world[:, sk.index["LeftLeg"]], axis=1)
    assert np.allclose(thigh, 0.45, atol=1e-6)


def test_desvio_some_nas_pontas_do_clipe(sk):
    # A perna corta a quina só no meio do clipe; o primeiro e o último quadro ficam como estavam.
    boxes = obstaculo.load([{"nome": "bloco", "centro": [0.1, 0.25, 0.45], "tamanho": [0.6, 0.5, 0.5]}])
    clear = [[0.1, 0.12, -0.20 + 0.01 * i] for i in range(10)]
    ankles = clear + [[0.1, 0.20, z] for z in np.linspace(0.06, 0.18, 8)] + clear[::-1]
    frames = leg_frames(sk, ankles)
    fixed, report = poses.avoid(sk, frames, boxes)
    assert report["LeftFoot"]["quadros"] > 0
    assert np.allclose(fixed[0], frames[0]) and np.allclose(fixed[-1], frames[-1])


def test_levar_com_nivelar_chega_na_orientacao_do_destino(sk):
    foot = sk.index["LeftFoot"]
    start = poses.Pose(sk)
    start.reach("LeftFoot", [0.1, 0.40, -0.25], [0, 0, 1])                    # pé no ar, atrás, ponta para baixo
    goal = poses.build_poses(sk, {"apoio": {"alcancar": [["LeftFoot", [0.1, 0.30, 0.20], [0, 0, 1]]],
                                            "pe_plano": ["LeftFoot"]}})["apoio"]
    frames = np.repeat(start.array()[None], 10, axis=0)
    pulled, report = poses.pull(sk, frames, ["LeftFoot"], goal.array(), hold=["LeftFoot"])
    assert report["LeftFoot"]["faltou_cm"] == 0.0
    world = sk.world_positions(pulled)
    assert np.allclose(world[-1, foot], [0.1, 0.30, 0.20], atol=1e-6)         # chegou no ponto
    goal_rot, _ = sk.fk(goal.pos, goal.rot)
    last_rot, _ = sk.fk(pulled[-1, :, :3], poses.quat_to_matrix(pulled[-1, :, 3:]))
    assert np.allclose(last_rot[foot], goal_rot[foot], atol=1e-5)             # e na orientação do destino
    first_rot, _ = sk.fk(frames[0, :, :3], poses.quat_to_matrix(frames[0, :, 3:]))
    early_rot, _ = sk.fk(pulled[2, :, :3], poses.quat_to_matrix(pulled[2, :, 3:]))
    assert np.allclose(early_rot[foot], first_rot[foot], atol=1e-5)           # antes de puxar, guarda a do começo


def test_fixar_usa_a_ancora_do_trecho_anterior(sk):
    foot = sk.index["LeftFoot"]
    landed = poses.Pose(sk)
    landed.reach("LeftFoot", [0.1, 0.20, 0.30], [0, 0, 1])                    # fim do trecho anterior: pé no chão
    still_up = poses.Pose(sk)
    still_up.reach("LeftFoot", [0.1, 0.30, 0.24], [0, 0, 1])                  # o que o modelo devolve: pé no ar
    frames = np.repeat(still_up.array()[None], 6, axis=0)
    loose, _ = poses.pin(sk, frames, ["LeftFoot"])
    assert sk.world_positions(loose)[-1, foot][1] == pytest.approx(0.30, abs=1e-6)   # sem âncora, preso no ar
    pinned, report = poses.pin(sk, frames, ["LeftFoot"], anchor=landed.array())
    assert np.allclose(sk.world_positions(pinned)[1:, foot], [0.1, 0.20, 0.30], atol=1e-6)
    assert report["LeftFoot"]["faltou_cm"] == 0.0


def test_pose_avisa_ponto_fora_de_alcance(sk):
    built = poses.build_poses(sk, {
        "perto": {"alcancar": [["LeftFoot", [0.1, 0.30, 0.20], [0, 0, 1]]]},
        "longe": {"altura": 0.5, "alcancar": [["LeftFoot", [0.1, 0.07, 0.30], [0, 0, 1]]]}})
    assert built["perto"].out_of_reach == {}
    assert built["longe"].out_of_reach["LeftFoot"] > 40                        # cm que faltaram


def test_pes_no_apoio_pega_pe_no_ar(sk):
    rest_ankle = float(sk.rest_world_pos[sk.index["LeftFoot"]][1])
    world = np.repeat(sk.rest_world_pos[None], 4, axis=0).copy()
    assert obstaculo.feet_on_support(world, NAMES, [], rest_ankle)["passou"] is True
    world[-1, sk.index["RightFoot"], 1] += 0.10                               # termina 10 cm acima do chão
    result = obstaculo.feet_on_support(world, NAMES, [], rest_ankle)
    assert result["passou"] is False
    assert result["fim"]["RightFoot"]["tornozelo_acima_do_apoio_cm"] == pytest.approx(10.0)
    # Em cima de uma caixa de 0,4 m, o apoio é o topo dela.
    boxes = obstaculo.load([{"centro": [0, 0.2, 0], "tamanho": [1.0, 0.4, 1.0]}])
    assert obstaculo.support_height(boxes, [0.1, rest_ankle + 0.4, 0.0]) == pytest.approx(0.4)
    assert obstaculo.support_height(boxes, [3.0, rest_ankle, 0.0]) == 0.0
    on_top = np.repeat(sk.rest_world_pos[None], 2, axis=0).copy()
    on_top[:, :, 1] += 0.4
    assert obstaculo.feet_on_support(on_top, NAMES, boxes, rest_ankle)["passou"] is True
