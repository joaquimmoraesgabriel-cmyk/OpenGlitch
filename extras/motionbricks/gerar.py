"""Gera uma animação com o MotionBricks a partir de um plano em JSON e grava em BVH.

Roda DENTRO do ambiente do MotionBricks (precisa de GPU NVIDIA):

    uv run --project <pasta do motionbricks> python gerar.py plano.json --saida pasta --nome agachar

O MotionBricks não é "texto para movimento". Ele preenche o movimento entre
quatro poses de contexto e de uma a quatro poses de destino, e cada geração
dura de 0,6 a 1,9 s. Movimento longo é uma cadeia: o plano lista os destinos em
ordem e este script encadeia, usando os quatro últimos quadros de cada geração
como contexto da seguinte.

Plano com POSES PRÓPRIAS (o caminho para um jogo: nada vem de clipe de terceiros):

    {
      "poses": {
        "em_pe": {
          "mirar": [["LeftArm", "LeftForeArm", [0.16, -1, 0.02]],
                    ["RightArm", "RightForeArm", [-0.16, -1, 0.02]]],
          "pes_no_chao": true
        },
        "agachado": {
          "mirar": [["Hips", "Spine1", [0, 1, 0.35]],
                    ["LeftLeg", "LeftShin", [0.05, -0.45, 0.89]],
                    ["LeftShin", "LeftFoot", [0, -0.8, -0.6]],
                    ["RightLeg", "RightShin", [-0.05, -0.45, 0.89]],
                    ["RightShin", "RightFoot", [0, -0.8, -0.6]]],
          "pe_plano": ["LeftFoot", "RightFoot"],
          "pes_no_chao": true
        }
      },
      "inicio": {"pose": "em_pe"},
      "destinos": [
        {"nome": "agachar", "pose": "agachado"},
        {"nome": "levantar", "pose": "em_pe"},
        {"nome": "andar", "pose": "em_pe", "posicao": [0, 1.0]}
      ]
    }

Como descrever uma pose está em poses.py. Espaço: +Y para cima, +Z para a
frente do personagem, +X para o lado esquerdo dele, em metros. `posicao` é
[x, z] da raiz no chão e `giro` são graus em volta de Y. O início parte do
personagem parado na pose dada.

Um destino também pode vir de um CLIPE BVH no esqueleto SOMA:

    {"clipe": "locomotion/idle/idle_loop_001__A268", "tempo": 0.5, "posicao": [0, 2], "giro": 0}

OBSTÁCULOS. O modelo não enxerga a cena: quem pega um corpo atravessando uma parede é a
conferência depois de gerar. Liste as caixas no plano e o relatório traz, em "obstaculos",
quanto cada osso entrou em cada uma, em que quadros e em que destino, e a que distância
mãos e pés ficaram das superfícies no fim de cada destino. A tira desenha as caixas.

    "obstaculos": [{"nome": "bloco", "centro": [0, 0.5, 1.5], "tamanho": [1.2, 1.0, 1.0]}]

Se atravessou, acrescente uma pose intermediária no destino afetado e gere de novo.

Depois de gerar, braços e pernas que ainda ficaram dentro de um obstáculo são tirados de lá por
IK: o pé é empurrado para fora (de preferência por cima), o tornozelo sobe e/ou o joelho gira
para fora, que é como a perna passa por cima de uma borda; na mão, só o punho. A correção é
suavizada no tempo ("desvios" no relatório diz quanto, o giro do joelho e em quantos quadros).
Isso fecha raspões, como a ponta do pé ou a canela na quina; desvio grande é sinal de pose
ruim e se corrige na pose. Para desligar: "desviar": false no plano.

"fora_de_alcance_cm" (também em --so-poses) lista, por pose, o "alcancar" que não chegou no
ponto: com o quadril onde a pose o põe, o braço ou a perna não tem comprimento. A ponta fica
no ar e o "fixar" do trecho seguinte a prende ali; corrija a altura ou o lugar do quadril.

O relatório traz também "pes_no_apoio": no primeiro e no último quadro, quanto cada tornozelo
está acima do apoio (chão ou topo de caixa) e quanto a ponta do pé está abaixo dele. Pé que
termina no ar ou torto não aparece na medida de penetração. Animação que começa ou termina fora
do apoio de propósito (sentado, pendurado) usa "conferir_pes": false no plano.

SEM PARAR EM CADA POSE. Cada destino de uma pose só é uma parada: o modelo chega nela freando,
e uma cadeia de seis destinos sai lenta e em degraus. Três campos de cada destino evitam isso
(são os mesmos recursos do runtime do MotionBricks e do gerar_ciclo.py):

    "antecipar": 6          usa os quadros da geração só até 6 antes do fim e a seguinte parte
                            dali: o trecho final, em que o modelo força a chegada, fica de fora.
                            A pose vira um ponto de passagem: é quase alcançada, não parada.
    "tokens": 7             duração da geração: quadros = tokens x 4 - 6 (6 a 16 tokens). Pode
                            ser uma lista, e o modelo escolhe entre elas.
    "velocidade": [0, 1.2]  destino em movimento: quatro poses iguais com a raiz andando a essa
                            velocidade [x, z] em m/s. O personagem chega andando, não parando.

    "levar": ["LeftFoot"]   pino de IK: a mão ou o pé é puxado, da metade do trecho em diante,
                            para o ponto e a orientação que tem na pose de destino, e chega lá
                            no último quadro. Com "antecipar" o corpo não termina na pose; sem
                            isto o pé chega baixo e o "fixar" do trecho seguinte o congela ali.
                            Junta que também está em "nivelar" parte da orientação do primeiro
                            quadro e chega na da pose de destino (não fica congelada na do começo).
    "levar_desde": 0.0      de que fração do trecho em diante o "levar" puxa (padrão 0.5). Com 0
                            a ponta vai quase em linha reta de onde está até o ponto do destino:
                            use quando o caminho do modelo passa por dentro do obstáculo, como o
                            pé que avança por baixo do topo do muro antes de subir.

"antecipar" também pode vir no plano, valendo para todos os destinos que não tiverem o seu.
Com antecipação as emendas são suavizadas (só em volta delas), a menos que o plano traga
"suavizar_emendas": false. O relatório traz a duração total e os quadros usados de cada geração.

APOIOS. Num destino, "fixar": ["LeftFoot"] segura o pé (ou a mão) parado no mundo durante
aquele trecho, onde estava no começo dele, refazendo a perna por IK em cada quadro. Use para
o pé ou a mão que está apoiado num obstáculo enquanto o corpo se move: o modelo não sabe do
apoio e costuma baixar o pé para o chão. O relatório diz, em "fixado", quanto faltou para a
perna alcançar. A pose de destino deve ter a junta fixada no mesmo ponto, senão há um salto.
"nivelar": ["LeftFoot"] deixa o pé se mover, mas com a orientação que tinha no começo do
trecho: é para o pé que sobe e desce sem apontar a ponta para baixo e cortar a quina. Uma
pose também pode vir do Blender, posada contra o obstáculo: veja blender_exportar.py.

`tempo` é o instante de onde saem as quatro poses. Sem --clipes, os clipes são
os de exemplo do MotionBricks, com licença só de avaliação interna: animação
feita a partir deles não pode ser distribuída. Um plano só com poses próprias
não usa esses clipes.

Saída: <nome>.bvh, <nome>.contatos.json, <nome>.relatorio.json (duração de cada
geração, erro até a pose pedida e medidas) e <nome>.tira.png (o esqueleto
quadro a quadro, de lado e de frente). Use --listar-juntas para ver os nomes.

Testado numa RTX 4050 de notebook (6 GB), no Windows, com --teste e --teste-poses.
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
from poses import Skeleton, avoid, build_poses, pin, pull  # noqa: E402
import obstaculo  # noqa: E402
import tira  # noqa: E402

AVISO_LICENCA = (
    "ATENÇÃO: este plano usou clipes de exemplo do MotionBricks, que têm licença só de "
    "avaliação interna (NVIDIA Sample Data Evaluation License). Não distribua esta animação "
    "nem a use num jogo publicado. Para isso, use poses próprias ou clipes seus com --clipes."
)
WALK = "locomotion/bs_1d_linear/Neutral_walk_forward_002__A057"
PLANO_DE_TESTE = {
    "inicio": {"clipe": WALK, "tempo": 1.0, "posicao": [0, 0]},
    "destinos": [{"nome": "andar_1", "clipe": WALK, "tempo": 1.8},
                 {"nome": "andar_2", "clipe": WALK, "tempo": 3.4}],
}


def _lados(mirar_esquerdo):
    """Espelha as direções do lado esquerdo para o direito (troca o sinal de X)."""
    out = []
    for joint, child, (x, y, z) in mirar_esquerdo:
        out.append([joint, child, [x, y, z]])
        out.append([joint.replace("Left", "Right"), child.replace("Left", "Right"), [-x, y, z]])
    return out


PLANO_DE_TESTE_POSES = {
    "poses": {
        "em_pe": {"mirar": _lados([["LeftArm", "LeftForeArm", [0.16, -1, 0.02]],
                                   ["LeftForeArm", "LeftHand", [0.10, -1, 0.18]]]),
                  "pes_no_chao": True},
        "agachado": {"mirar": [["Hips", "Spine1", [0, 1, 0.35]]] + _lados([
            ["LeftLeg", "LeftShin", [0.05, -0.45, 0.89]], ["LeftShin", "LeftFoot", [0, -0.80, -0.60]],
            ["LeftArm", "LeftForeArm", [0.15, -0.5, 0.85]], ["LeftForeArm", "LeftHand", [0.0, -0.1, 1.0]]]),
            "pe_plano": ["LeftFoot", "RightFoot"], "pes_no_chao": True},
        "bracos_para_cima": {"base": "em_pe", "mirar": _lados([
            ["LeftArm", "LeftForeArm", [0.30, 1, 0.0]], ["LeftForeArm", "LeftHand", [0.12, 1, 0.05]]]),
            "pes_no_chao": True},
    },
    "inicio": {"pose": "em_pe"},
    "destinos": [{"nome": "agachar", "pose": "agachado"}, {"nome": "levantar", "pose": "em_pe"},
                 {"nome": "bracos_para_cima", "pose": "bracos_para_cima"},
                 {"nome": "andar_1m", "pose": "em_pe", "posicao": [0, 1.0]}],
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
    """Move só a raiz: gira em volta de Y e leva a primeira pose à posição pedida no chão.

    As demais juntas ficam como estão, como a documentação do MotionBricks manda. Sem
    `position`, a raiz fica onde estava.
    """
    out = window.copy()
    pivot = out[0, 0, :3].copy()
    pivot[1] = 0.0
    turn = quat_y(turn_degrees)
    c, s = math.cos(math.radians(turn_degrees)), math.sin(math.radians(turn_degrees))
    anchor = pivot if position is None else np.array([float(position[0]), 0.0, float(position[1])])
    for pose in out:
        rel = pose[0, :3] - pivot
        pose[0, 0] = c * rel[0] + s * rel[2] + anchor[0]
        pose[0, 2] = -s * rel[0] + c * rel[2] + anchor[2]
        pose[0, 1] = rel[1]
        pose[0, 3:7] = quat_mul(turn, pose[0, 3:7])
    return out


def smooth_seams(motion: np.ndarray, seams: list[int], sigma: float = 1.5, radius: float = 3.0) -> np.ndarray:
    """Gaussiana só em volta das emendas entre gerações (rotações de todas as juntas e a raiz)."""
    if not seams:
        return motion
    n = len(motion)
    k = np.arange(-4, 5)
    kernel = np.exp(-(k ** 2) / (2 * sigma ** 2))
    kernel /= kernel.sum()
    q = motion[:, :, 3:].copy()
    for f in range(1, n):  # o mesmo sinal ao longo do tempo, para a média fazer sentido
        flip = np.sum(q[f] * q[f - 1], axis=-1) < 0
        q[f, flip] *= -1
    pos = motion[:, 0, :3].copy()
    idx = np.clip(np.arange(n)[:, None] + k[None], 0, n - 1)
    sq = np.einsum("k,fkjc->fjc", kernel, q[idx])
    sp = np.einsum("k,fkc->fc", kernel, pos[idx])
    dist = np.min(np.abs(np.arange(n)[:, None] - np.array(seams)[None]), axis=1)
    w = np.exp(-(dist ** 2) / (2 * radius ** 2))
    out = motion.copy()
    mixed = q + w[:, None, None] * (sq - q)
    out[:, :, 3:] = mixed / np.linalg.norm(mixed, axis=-1, keepdims=True)
    out[:, 0, :3] = pos + w[:, None] * (sp - pos)
    return out


def check_plan(plan: dict) -> None:
    if not plan.get("inicio") or not plan.get("destinos"):
        raise SystemExit("o plano precisa de \"inicio\" e de pelo menos um item em \"destinos\"")
    for where, spec in [("inicio", plan["inicio"])] + [(f"destino {i}", d) for i, d in enumerate(plan["destinos"], 1)]:
        if ("pose" in spec) == ("clipe" in spec):
            raise SystemExit(f"{where}: informe \"pose\" ou \"clipe\", um dos dois")
        if "pose" in spec and spec["pose"] != "repouso" and spec["pose"] not in plan.get("poses", {}):
            raise SystemExit(f"{where}: a pose \"{spec['pose']}\" não está em \"poses\"")


def key_poses(plan, built, boxes, skeleton, names, parents, rest, out_dir: Path, name: str) -> dict:
    """Grava só as poses-chave do plano, sem gerar: um quadro por pose, do início ao último destino.

    É a conferência barata antes de gastar geração: a tira mostra cada pose ao lado dos
    obstáculos e o relatório diz se alguma pose já nasce dentro de um deles. O BVH abre no
    Blender (blender_cena.py) para ver e ajustar as poses contra a cena.
    """
    specs = [plan["inicio"], *plan["destinos"]]
    if any("clipe" in spec for spec in specs):
        raise SystemExit("--so-poses só vale para planos com poses próprias, sem \"clipe\"")
    frames = np.concatenate([
        place_window(built[spec["pose"]].array()[None], spec.get("posicao"), float(spec.get("giro", 0.0)))
        for spec in specs])
    labels = ["inicio"] + [spec.get("nome") or f"destino_{i}" for i, spec in enumerate(plan["destinos"], 1)]
    marks = [{"nome": label, "inicio": i, "fim": i} for i, label in enumerate(labels)]
    world = skeleton.world_positions(frames)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = write_bvh(out_dir / f"{name}.poses.bvh", names, parents, rest, frames, fps=1.0)
    summary.pop("juntas_com_posicao", None)
    index = {n: i for i, n in enumerate(names)}
    ends = [n for n in ("Hips", "Head", "HeadEnd", "LeftHand", "RightHand", "LeftFoot", "RightFoot") if n in index]
    summary.update({
        "poses": [{"quadro": i, "nome": label, "pose": spec["pose"],
                   "no_mundo_m": {n: [round(float(v), 3) for v in world[i, index[n]]] for n in ends}}
                  for i, (label, spec) in enumerate(zip(labels, specs))],
        "tira": tira.draw(out_dir / f"{name}.poses.png", world, names, parents,
                          [{"nome": "poses-chave", "inicio": 0, "fim": len(frames) - 1}],
                          columns=len(frames), boxes=boxes),
        "esqueleto": "SOMA", "espaco": "Y para cima, +Z para a frente, +X para a esquerda; metros",
    })
    # "alcancar" que não alcança: a ponta fica no ar em vez de no ponto, e o "fixar" a prende ali.
    short = {spec["pose"]: built[spec["pose"]].out_of_reach for spec in specs
             if getattr(built[spec["pose"]], "out_of_reach", None)}
    summary["fora_de_alcance_cm"] = short
    if boxes:
        summary["obstaculos"] = obstaculo.check(world, names, parents, boxes, marks,
                                                tolerance=float(plan.get("folga_obstaculo", 0.03)))
    (out_dir / f"{name}.poses.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def run(plan: dict, out_dir: Path, clips_dir: Path | None, name: str, list_joints: bool = False,
        only_poses: bool = False) -> dict:
    import warp as wp
    from motionbricks.io.bvh import load_bvh
    from motionbricks.io.usd import load_skeleton_from_usd
    from motionbricks.io.utils import SOMA_SKELETON_PRIM_PATH, get_asset_file
    from motionbricks.model.contract import MODEL_POSES_PER_TOKEN, MODEL_SAMPLE_RATE
    from motionbricks.model.soma.contract import SOMA_N1_FP32_ONNX_PATH
    from motionbricks.model.soma.engine import MotionBricksSOMAEngine
    import motionbricks

    wp.init()
    mb_skeleton = load_skeleton_from_usd(
        get_asset_file("human", "soma_base_skel_minimal_no_root.usd"), SOMA_SKELETON_PRIM_PATH)
    names = list(mb_skeleton.joint_names)
    parents = [mb_skeleton.joint_parent(i) for i in range(mb_skeleton.num_joints)]
    rest = mb_skeleton.reference_local_transforms.numpy().reshape(-1, 7).astype(np.float64)
    skeleton = Skeleton(names, parents, rest)
    if list_joints:
        hidden = ("Thumb", "Index", "Middle", "Ring", "Pinky")
        return {"juntas": [
            {"nome": n, "pai": names[parents[i]] if parents[i] >= 0 else None,
             "repouso_no_mundo_m": [round(float(v), 3) for v in skeleton.rest_world_pos[i]]}
            for i, n in enumerate(names) if not any(h in n for h in hidden)],
            "espaco": "+Y para cima, +Z para a frente, +X para o lado esquerdo do personagem"}

    check_plan(plan)
    built = build_poses(skeleton, plan.get("poses", {}))
    boxes = obstaculo.load(plan.get("obstaculos"))
    if only_poses:
        return key_poses(plan, built, boxes, skeleton, names, parents, rest, out_dir, name)
    repo = Path(motionbricks.__file__).resolve().parents[1]
    base = Path(clips_dir) if clips_dir else repo / "assets" / "motions" / "soma"
    uses_clips = any("clipe" in s for s in [plan["inicio"], *plan["destinos"]])
    uses_samples = uses_clips and clips_dir is None

    wp.set_device("cuda:0")
    clips: dict[str, object] = {}
    # Sem model_to_runtime, tudo fica no espaço do modelo SOMA: Y para cima, o mesmo do BVH.
    engine = MotionBricksSOMAEngine(SOMA_N1_FP32_ONNX_PATH)
    segments, contacts, report, marks = [], [], [], []
    total = 0
    with engine, wp.ScopedStream(engine.stream):
        context = engine.create_input(mb_skeleton)
        target = engine.create_input(mb_skeleton)
        output = engine.create_output(mb_skeleton)
        buffer = wp.empty_like(context.poses)

        def from_clip(spec: dict, ending: bool) -> np.ndarray:
            key = spec["clipe"]
            if key not in clips:
                path = base / (key if key.lower().endswith(".bvh") else key + ".bvh")
                clips[key] = load_bvh(str(path), mb_skeleton)
            start = float(spec.get("tempo", 0.0))
            if ending:  # o contexto são as quatro poses que TERMINAM no tempo dado
                start -= (MODEL_POSES_PER_TOKEN - 1) / MODEL_SAMPLE_RATE
            for index in range(MODEL_POSES_PER_TOKEN):
                clips[key].sample(max(0.0, start + index / MODEL_SAMPLE_RATE), buffer[index],
                                  root_offset=wp.transform_identity(), stream=engine.stream)
            engine.synchronize()
            return buffer.numpy().astype(np.float64).reshape(MODEL_POSES_PER_TOKEN, -1, 7)

        def window(spec: dict, as_context: bool) -> np.ndarray:
            if "clipe" in spec:
                poses = from_clip(spec, ending=as_context)
            else:
                pose = built[spec["pose"]].array()[None]
                # Contexto: quatro poses iguais, o personagem parado. Destino: uma pose, onde ele para,
                # ou, com "velocidade", quatro poses iguais com a raiz andando (chega em movimento).
                moving = (not as_context) and spec.get("velocidade") is not None
                poses = np.repeat(pose, MODEL_POSES_PER_TOKEN, axis=0) if (as_context or moving) else pose
            out = place_window(poses, spec.get("posicao"), float(spec.get("giro", 0.0)))
            if (not as_context) and spec.get("velocidade") is not None and "clipe" not in spec:
                vx, vz = (float(v) for v in spec["velocidade"])
                for k in range(len(out)):
                    out[k, 0, 0] += vx * k / MODEL_SAMPLE_RATE
                    out[k, 0, 2] += vz * k / MODEL_SAMPLE_RATE
            return out

        def to_device(poses: np.ndarray):
            return wp.array(poses.astype(np.float32), dtype=wp.transform, device=engine.device)

        context_poses = window(plan["inicio"], as_context=True)
        any_early = False
        for number, spec in enumerate(plan["destinos"], 1):
            goal = window(spec, as_context=False)
            context.update_from_poses(to_device(context_poses), stream=engine.stream)
            target.update_from_poses(to_device(goal), stream=engine.stream)
            tokens = spec.get("tokens")
            if tokens:
                from motionbricks.model.config import MotionBricksInferenceConfig
                allowed = (int(tokens),) if isinstance(tokens, (int, float)) else tuple(int(t) for t in tokens)
                engine.generate_animation(context, target, output, config=MotionBricksInferenceConfig(allowed_token_counts=allowed))
            else:
                engine.generate_animation(context, target, output)
            engine.synchronize()
            frames = int(output.num_frames)
            poses = output.poses.numpy()[:frames].astype(np.float64).reshape(frames, -1, 7)
            feet = output.foot_contacts.numpy()[:frames].astype(np.float64)
            # Transição antecipada: o fim da geração, onde o modelo força a parada na pose, fica de fora.
            early = int(spec.get("antecipar", plan.get("antecipar", 0)))
            if early > 0 and number < len(plan["destinos"]):
                used = max(8, frames - early)
                poses, feet = poses[:used], feet[:used]
                any_early = True
            pulled = None
            # O apoio é o do fim do trecho anterior, não o do primeiro quadro que o modelo devolve.
            previous = np.asarray(context_poses[-1], dtype=np.float64).reshape(-1, 7)
            level = list(spec.get("nivelar", []))
            if spec.get("levar"):
                # Junta levada e nivelada: sai da orientação do primeiro quadro e chega na do destino.
                both = [n for n in spec["levar"] if n in level]
                poses, pulled = pull(skeleton, poses, list(spec["levar"]), goal[0],
                                     start=float(spec.get("levar_desde", 0.5)), hold=both, anchor=previous)
                level = [n for n in level if n not in both]
            pinned = None
            if spec.get("fixar") or level:
                # O contexto da geração seguinte sai dos quadros já corrigidos.
                poses, pinned = pin(skeleton, poses, list(spec.get("fixar", [])), level, anchor=previous)
            # Cada geração começa na última pose do contexto: não repita esse quadro.
            keep = slice(1, None) if segments else slice(None)
            segments.append(poses[keep])
            contacts.append(feet[keep])
            label = spec.get("nome") or f"destino_{number}"
            begin, total = total, total + len(poses[keep])
            marks.append({"nome": label, "inicio": begin, "fim": total - 1})
            end_world = skeleton.world_positions(poses[-1])
            goal_world = skeleton.world_positions(goal[0])
            ends = [n for n in ("Hips", "Head", "LeftHand", "RightHand", "LeftFoot", "RightFoot") if n in skeleton.index]
            report.append({
                "nome": label, "de": spec.get("pose") or spec.get("clipe"), "quadros": frames,
                "quadros_usados": len(poses), "segundos": round(len(poses) / MODEL_SAMPLE_RATE, 2),
                "raiz_inicio": [round(float(v), 3) for v in poses[0, 0, :3]],
                "raiz_fim": [round(float(v), 3) for v in poses[-1, 0, :3]],
                "distancia_ate_a_pose_pedida_cm": {
                    n: round(float(np.linalg.norm(end_world[skeleton.index[n]] - goal_world[skeleton.index[n]])) * 100, 1)
                    for n in ends},
            })
            if pinned:
                report[-1]["fixado"] = pinned
            if pulled:
                report[-1]["levado"] = pulled
            context_poses = poses[-MODEL_POSES_PER_TOKEN:]

    motion = np.concatenate(segments, axis=0)
    feet = np.concatenate(contacts, axis=0)
    if any_early and plan.get("suavizar_emendas", True):
        motion = smooth_seams(motion, [m["inicio"] for m in marks[1:]])
    detours = None
    if boxes and plan.get("desviar", True):
        if plan.get("guardar_antes_do_desvio"):
            out_dir.mkdir(parents=True, exist_ok=True)
            np.save(out_dir / f"{name}.antes_do_desvio.npy", motion)
        motion, detours = avoid(skeleton, motion, boxes)
    world = skeleton.world_positions(motion)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = write_bvh(out_dir / f"{name}.bvh", names, parents, rest, motion, fps=MODEL_SAMPLE_RATE)
    write_contacts(out_dir / f"{name}.contatos.json", feet, fps=MODEL_SAMPLE_RATE)
    rest_foot = float(min(skeleton.rest_world_pos[skeleton.index[n]][1] for n in ("LeftFoot", "RightFoot")))
    summary.update({
        "geracoes": report,
        "medidas": tira.measure(world, feet, names, MODEL_SAMPLE_RATE, rest_foot),
        "tira": tira.draw(out_dir / f"{name}.tira.png", world, names, parents, marks, boxes=boxes),
        "esqueleto": "SOMA", "espaco": "Y para cima, metros no modelo, centímetros no BVH",
        "poses_de": ("clipes de exemplo do MotionBricks (somente avaliação)" if uses_samples
                     else (str(base) if uses_clips else "poses próprias do plano")),
        "usou_clipes_de_exemplo": uses_samples,
    })
    if boxes:
        summary["obstaculos"] = obstaculo.check(world, names, parents, boxes, marks,
                                                tolerance=float(plan.get("folga_obstaculo", 0.03)))
        summary["desvios"] = detours or {}
    summary["fora_de_alcance_cm"] = {n: p.out_of_reach for n, p in built.items() if getattr(p, "out_of_reach", None)}
    if plan.get("conferir_pes", True):
        summary["pes_no_apoio"] = obstaculo.feet_on_support(world, names, boxes or [], rest_foot)
    summary.pop("juntas_com_posicao", None)
    (out_dir / f"{name}.relatorio.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    notice = out_dir / "LEIA-ME-LICENCA.txt"
    if uses_samples:
        notice.write_text(AVISO_LICENCA + "\n", encoding="utf-8")
    return summary


def main() -> int:
    if not sys.stdout.isatty():
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Gera uma animação com o MotionBricks e grava em BVH.")
    parser.add_argument("plano", nargs="?", help="arquivo JSON com poses, início e destinos")
    parser.add_argument("--saida", default="saida_motionbricks", help="pasta de saída")
    parser.add_argument("--nome", default="animacao", help="nome base dos arquivos e do clipe")
    parser.add_argument("--clipes", help="pasta com os SEUS clipes BVH no esqueleto SOMA")
    parser.add_argument("--teste", action="store_true", help="caminhada curta a partir dos clipes de exemplo")
    parser.add_argument("--teste-poses", action="store_true", help="agachar, levantar e andar só com poses próprias")
    parser.add_argument("--listar-juntas", action="store_true", help="mostra as juntas do esqueleto e sai")
    parser.add_argument("--so-poses", action="store_true",
                        help="não gera: grava as poses-chave em <nome>.poses.bvh e confere contra os obstáculos")
    args = parser.parse_args()
    if args.listar_juntas:
        print(json.dumps(run({}, Path(args.saida), None, args.nome, list_joints=True), ensure_ascii=False, indent=1))
        return 0
    if args.teste:
        plan = PLANO_DE_TESTE
    elif args.teste_poses:
        plan = PLANO_DE_TESTE_POSES
    elif args.plano:
        plan = json.loads(Path(args.plano).read_text(encoding="utf-8"))
    else:
        parser.error("informe o arquivo do plano, ou use --teste, --teste-poses ou --listar-juntas")
    try:
        summary = run(plan, Path(args.saida), Path(args.clipes) if args.clipes else None, args.nome,
                      only_poses=args.so_poses)
    except ValueError as exc:
        raise SystemExit(f"plano inválido: {exc}") from None
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary.get("usou_clipes_de_exemplo"):
        print("\n" + AVISO_LICENCA, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
