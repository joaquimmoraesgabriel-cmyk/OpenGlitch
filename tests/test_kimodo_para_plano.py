"""Rascunho do Kimodo: leitura da hierarquia, escolha de quadros e plano."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1] / "extras" / "motionbricks"
sys.path.insert(0, str(SCRIPTS))
import kimodo_para_plano as kp  # noqa: E402

BVH = """HIERARCHY
ROOT Root
{
  OFFSET 0 0 0
  JOINT Hips
  {
    OFFSET 0 100 0
    JOINT LeftFoot
    {
      OFFSET 10 -93 0
      JOINT LeftToeBase
      {
        OFFSET 0 -5 15
        End Site
        {
          OFFSET 0 0 5
        }
      }
    }
    JOINT RightFoot
    {
      OFFSET -10 -93 0
      JOINT RightToeBase
      {
        OFFSET 0 -5 15
        End Site
        {
          OFFSET 0 0 5
        }
      }
    }
  }
}
MOTION
Frames: 0
"""
NAMES = ["Hips", "LeftFoot", "LeftToeBase", "RightFoot", "RightToeBase"]


def draft(tmp_path: Path, frames: int = 91) -> tuple[Path, Path]:
    rest = np.array([[0, 1.0, 0], [0.1, 0.07, 0], [0.1, 0.02, 0.15], [-0.1, 0.07, 0], [-0.1, 0.02, 0.15]])
    world = np.repeat(rest[None], frames, axis=0)
    world[:, :, 2] += np.linspace(0.0, 1.5, frames)[:, None]          # anda 1,5 m para a frente
    bvh, npz = tmp_path / "r.bvh", tmp_path / "r.npz"
    bvh.write_text(BVH, encoding="utf-8")
    np.savez(npz, posed_joints=world)
    return npz, bvh


def test_hierarquia_descarta_root_e_pontas(tmp_path):
    npz, bvh = draft(tmp_path)
    world, names, parents = kp.load(npz, bvh)
    assert names == NAMES
    assert parents == [-1, 0, 1, 0, 3]
    assert world.shape == (91, 5, 3)


def test_quadros_cabem_no_motionbricks(tmp_path):
    world, names, _ = kp.load(*draft(tmp_path))
    frames = kp.pick_frames(world, names, 1.0)
    assert frames[0] == 0 and frames[-1] == 90
    assert all(18 <= b - a <= 58 for a, b in zip(frames[:-1], frames[1:]))
    assert kp.tokens_for(22) == 7 and kp.tokens_for(5) == 6 and kp.tokens_for(200) == 16


def test_script_escreve_plano_e_relatorio(tmp_path):
    npz, bvh = draft(tmp_path)
    base = tmp_path / "base.json"
    base.write_text(json.dumps({"obstaculos": [{"nome": "muro", "centro": [0, 0.5, 1.0], "tamanho": [1, 1, 0.2]}]}))
    out = tmp_path / "plano.json"
    subprocess.run([sys.executable, str(SCRIPTS / "kimodo_para_plano.py"), "--npz", str(npz), "--bvh", str(bvh),
                    "--saida", str(out), "--plano-base", str(base), "--quadros", "0,30,60,90"], check=True)
    plan = json.loads(out.read_text(encoding="utf-8"))
    assert plan["inicio"] == {"quadro_guia": 0}
    assert [d["quadro_guia"] for d in plan["destinos"]] == [30, 60, 90]
    assert plan["guia"]["modo"] == "inteiro" and "tokens" not in plan["destinos"][0]
    guide = np.load(plan["guia"]["arquivo"])
    assert [str(n) for n in guide["juntas"]] == NAMES and guide["posicoes"].shape == (91, 5, 3)
    assert plan["obstaculos"][0]["nome"] == "muro"
    report = json.loads(out.with_suffix(".rascunho.json").read_text(encoding="utf-8"))
    assert report["quadril_deslocamento_m"][2] == 1.5
    assert report["obstaculos"]["passou"] is False                     # o rascunho atravessa o muro


def test_refazer_entrega_o_trecho_ao_motionbricks(tmp_path):
    world, names, _ = kp.load(*draft(tmp_path))
    plan = kp.build_plan(world, names, [0, 30, 60, 90], {}, None, tmp_path / "g.npz", "inteiro", {2})
    assert [d.get("guia") for d in plan["destinos"]] == [None, "nao", None]
    assert plan["destinos"][1]["tokens"] == 9 and "tokens" not in plan["destinos"][0]


def test_encaixe_tira_o_rascunho_de_dentro_do_muro(tmp_path):
    world, names, parents = kp.load(*draft(tmp_path))
    world = world[:1].repeat(20, axis=0)                               # parado, com a ponta dos pés dentro do muro
    boxes = kp.obstaculo.load([{"nome": "muro", "centro": [0, 0.5, 0.2], "tamanho": [1, 1, 0.2]}])
    moved, report = kp.fit(world, names, parents, boxes, 0.3, 0.03)
    assert report["penetracao_maxima_cm"]["antes"] > 1 and report["penetracao_maxima_cm"]["depois"] == 0
    assert kp.obstaculo.check(moved, names, parents, boxes)["passou"]
