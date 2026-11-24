"""Gera uma animação com o MotionBricks a partir de um plano em JSON e grava em BVH.

Roda DENTRO do ambiente do MotionBricks (precisa de GPU NVIDIA):

    uv run --project <pasta do motionbricks> python gerar.py plano.json --saida pasta

O MotionBricks não é "texto para movimento". Ele preenche o movimento entre
quatro poses de contexto e de uma a quatro poses de destino, e cada geração
dura de 0,6 a 1,9 s. Movimento longo é uma cadeia de gerações: o plano lista os
destinos em ordem e este script encadeia, usando os quatro últimos quadros de
cada geração como contexto da seguinte.

As poses de destino vêm de clipes BVH no esqueleto SOMA. Os clipes de exemplo
que acompanham o MotionBricks têm licença só de avaliação interna: animação
feita a partir deles não pode ser distribuída. Para um jogo, use clipes seus
com --clipes.

Plano (posições em metros no chão, plano XZ; giro em graus em volta de Y):

    {
      "inicio":   {"clipe": "locomotion/idle/idle_loop_001__A268", "tempo": 0.5,
                   "posicao": [0, 0], "giro": 0},
      "destinos": [
        {"clipe": "locomotion/bs_1d_linear/Neutral_walk_forward_002__A057",
         "tempo": 1.8, "posicao": [0, 2.0], "giro": 0}
      ]
    }

`tempo` é o instante do clipe de onde saem as quatro poses. `posicao` é onde a
raiz da primeira dessas poses fica no chão. `giro` roda o clipe em relação à
direção que ele já tem.

Este script foi escrito a partir da documentação e dos exemplos oficiais
(docs/runtime_api.md e docs/examples) e ainda não foi executado contra o
MotionBricks pelo autor. Rode primeiro com --teste.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bvh_writer import write_bvh, write_contacts  # noqa: E402

AVISO_LICENCA = (
    "ATENÇÃO: as poses vieram dos clipes de exemplo do MotionBricks, que têm licença só de "
    "avaliação interna (NVIDIA Sample Data Evaluation License). Não distribua esta animação "
    "nem a use num jogo publicado. Para isso, gere a partir de clipes seus com --clipes."
)
PLANO_DE_TESTE = {
    "inicio": {"clipe": "locomotion/bs_1d_linear/Neutral_walk_forward_002__A057", "tempo": 1.0,
               "posicao": [0, 0], "giro": 0},
    "destinos": [
        {"clipe": "locomotion/bs_1d_linear/Neutral_walk_forward_002__A057", "tempo": 1.8},
        {"clipe": "locomotion/bs_1d_linear/Neutral_walk_forward_002__A057", "tempo": 3.4},
    ],
}


def quat_y(degrees: float) -> np.ndarray:
    half = math.radians(degrees) / 2.0
    return np.array([0.0, math.sin(half), 0.0, math.cos(half)])


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return np.array([
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    ])


def place_window(window: np.ndarray, position, turn_degrees: float) -> np.ndarray:
    """Move só a raiz das quatro poses: gira em volta de Y e leva a primeira pose à posição pedida.

    As demais juntas ficam como foram amostradas, como a documentação manda.
    """
    out = window.copy()
    pivot = out[0, 0, :3].copy()
    pivot[1] = 0.0
    turn = quat_y(turn_degrees)
    c, s = math.cos(math.radians(turn_degrees)), math.sin(math.radians(turn_degrees))
    for pose in out:
        rel = pose[0, :3] - pivot
        x, z = rel[0], rel[2]
        pose[0, 0] = c * x + s * z
        pose[0, 2] = -s * x + c * z
        pose[0, 1] = rel[1]
        if position is not None:
            pose[0, 0] += float(position[0])
            pose[0, 2] += float(position[1])
        else:
            pose[0, 0] += pivot[0]
            pose[0, 2] += pivot[2]
        pose[0, 3:7] = quat_mul(turn, pose[0, 3:7])
    return out


def run(plan: dict, out_dir: Path, clips_dir: Path | None, name: str) -> dict:
    import warp as wp
    from motionbricks.io.bvh import load_bvh
    from motionbricks.io.usd import load_skeleton_from_usd
    from motionbricks.io.utils import SOMA_SKELETON_PRIM_PATH, get_asset_file
    from motionbricks.model.contract import MODEL_POSES_PER_TOKEN, MODEL_SAMPLE_RATE
    from motionbricks.model.soma.contract import SOMA_N1_FP32_ONNX_PATH
    from motionbricks.model.soma.engine import MotionBricksSOMAEngine
    import motionbricks

    repo = Path(motionbricks.__file__).resolve().parents[1]
    samples_dir = repo / "assets" / "motions" / "soma"
    base = Path(clips_dir) if clips_dir else samples_dir
    uses_samples = clips_dir is None

    wp.init()
    wp.set_device("cuda:0")
    skeleton = load_skeleton_from_usd(
        get_asset_file("human", "soma_base_skel_minimal_no_root.usd"), SOMA_SKELETON_PRIM_PATH)
    clips: dict[str, object] = {}

    def clip_of(spec: dict):
        key = spec["clipe"]
        if key not in clips:
            path = base / (key if key.lower().endswith(".bvh") else key + ".bvh")
            clips[key] = load_bvh(str(path), skeleton)
        return clips[key]

    # Sem model_to_runtime, tudo fica no espaço do modelo SOMA: Y para cima, o mesmo do BVH.
    engine = MotionBricksSOMAEngine(SOMA_N1_FP32_ONNX_PATH)
    segments, contacts, report = [], [], []
    with engine, wp.ScopedStream(engine.stream):
        context = engine.create_input(skeleton)
        target = engine.create_input(skeleton)
        output = engine.create_output(skeleton)
        buffer = wp.empty_like(context.poses)

        def window(spec: dict, ending: bool) -> np.ndarray:
            clip = clip_of(spec)
            start = float(spec.get("tempo", 0.0))
            if ending:  # o contexto são as quatro poses que TERMINAM no tempo dado
                start -= (MODEL_POSES_PER_TOKEN - 1) / MODEL_SAMPLE_RATE
            for index in range(MODEL_POSES_PER_TOKEN):
                clip.sample(max(0.0, start + index / MODEL_SAMPLE_RATE), buffer[index],
                            root_offset=wp.transform_identity(), stream=engine.stream)
            engine.synchronize()
            sampled = buffer.numpy().astype(np.float64).reshape(MODEL_POSES_PER_TOKEN, -1, 7)
            return place_window(sampled, spec.get("posicao"), float(spec.get("giro", 0.0)))

        def to_device(poses: np.ndarray):
            return wp.array(poses.astype(np.float32), dtype=wp.transform, device=engine.device)

        context_poses = window(plan["inicio"], ending=True)
        for number, spec in enumerate(plan["destinos"], 1):
            target_poses = window(spec, ending=False)
            context.update_from_poses(to_device(context_poses), stream=engine.stream)
            target.update_from_poses(to_device(target_poses), stream=engine.stream)
            engine.generate_animation(context, target, output)
            engine.synchronize()
            frames = int(output.num_frames)
            poses = output.poses.numpy()[:frames].astype(np.float64).reshape(frames, -1, 7)
            feet = output.foot_contacts.numpy()[:frames]
            # Cada geração começa na última pose do contexto: não repita esse quadro.
            keep = slice(1, None) if segments else slice(None)
            segments.append(poses[keep])
            contacts.append(feet[keep])
            report.append({
                "destino": number, "clipe": spec["clipe"], "quadros": frames,
                "segundos": round(frames / MODEL_SAMPLE_RATE, 2),
                "raiz_inicio": [round(float(v), 3) for v in poses[0, 0, :3]],
                "raiz_fim": [round(float(v), 3) for v in poses[-1, 0, :3]],
            })
            context_poses = poses[-MODEL_POSES_PER_TOKEN:]

        names = list(skeleton.joint_names)
        parents = [skeleton.joint_parent(i) for i in range(skeleton.num_joints)]
        rest = skeleton.reference_local_transforms.numpy().reshape(-1, 7)

    motion = np.concatenate(segments, axis=0)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = write_bvh(out_dir / f"{name}.bvh", names, parents, rest, motion, fps=MODEL_SAMPLE_RATE)
    write_contacts(out_dir / f"{name}.contatos.json", np.concatenate(contacts, axis=0), fps=MODEL_SAMPLE_RATE)
    summary.update({
        "geracoes": report, "esqueleto": "SOMA", "espaco": "Y para cima, metros no modelo, centímetros no BVH",
        "poses_de": "clipes de exemplo do MotionBricks (somente avaliação)" if uses_samples else str(base),
        "pode_distribuir": False if uses_samples else "depende da licença dos seus clipes e do modelo",
    })
    (out_dir / f"{name}.relatorio.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if uses_samples:
        (out_dir / "LEIA-ME-LICENCA.txt").write_text(AVISO_LICENCA + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera uma animação com o MotionBricks e grava em BVH.")
    parser.add_argument("plano", nargs="?", help="arquivo JSON com início e destinos")
    parser.add_argument("--saida", default="saida_motionbricks", help="pasta de saída")
    parser.add_argument("--nome", default="animacao", help="nome base dos arquivos")
    parser.add_argument("--clipes", help="pasta com os SEUS clipes BVH no esqueleto SOMA")
    parser.add_argument("--teste", action="store_true", help="gera uma caminhada curta de exemplo")
    args = parser.parse_args()
    if not args.teste and not args.plano:
        parser.error("informe o arquivo do plano ou use --teste")
    plan = PLANO_DE_TESTE if args.teste else json.loads(Path(args.plano).read_text(encoding="utf-8"))
    if not plan.get("destinos"):
        parser.error("o plano precisa de pelo menos um destino")
    summary = run(plan, Path(args.saida), Path(args.clipes) if args.clipes else None, args.nome)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["pode_distribuir"] is False:
        print("\n" + AVISO_LICENCA, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
