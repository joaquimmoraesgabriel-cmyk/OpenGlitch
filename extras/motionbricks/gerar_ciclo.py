"""Gera um ciclo em loop com o MotionBricks, só com poses próprias, e mede a emenda.

Reaproveita poses.py, bvh_writer.py e tira.py do OpenGlitch (extras/motionbricks) e
acrescenta ao gerar.py de lá:

1. Duração fixa por geração: "tokens" (6 a 16) em cada destino. Quadros gerados =
   tokens * 4 - 6, a 30 fps (6 -> 18, 10 -> 34, 12 -> 42, 14 -> 50).
2. Destino parado ("parar": true): quatro poses iguais, o modelo chega com velocidade zero.
3. Destino em movimento ("velocidade_alvo": [vx, vz] m/s, no destino ou no plano): quatro
   poses iguais em que só a raiz avança, como o adjust_target_pose_speed do runtime do
   MotionBricks. O modelo chega à pose andando, em vez de frear nela.
4. Transição antecipada ("transicao_antecipada": E no plano): de cada geração ficam só os
   quadros até E antes do fim, e a próxima geração parte dali, como o
   transition_early_by_frames do runtime. A parte final, onde a correção de pontas puxa
   o movimento para a pose pedida, não entra no clipe.
5. Recorte do loop, de dois jeitos:
   - "candidato": true num destino (com "segmentos_no_ciclo"): o ciclo vai da pose de um
     destino à mesma pose, alguns destinos depois; a emenda já fecha na pose.
   - "periodo": P quadros no plano: procura na parte estável da cadeia o trecho de P
     quadros cujo fim mais se parece com o começo (pose e velocidade).
6. Limpeza do ciclo, como em cleanup de mocap: fecha o resíduo da emenda distribuindo a
   diferença ao longo do ciclo e suaviza (gaussiana circular, só perto das emendas entre
   gerações e do ponto de loop). O relatório traz as medidas antes e depois.

Rodar dentro do ambiente do MotionBricks:

    uv run --project <repo do motionbricks> python gerar_ciclo.py plano.json --saida pasta --nome Nome
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
from poses import Skeleton, build_poses  # noqa: E402
import tira  # noqa: E402
from gerar import place_window  # noqa: E402

FPS = 30.0
ESCONDER = ("Thumb", "Index", "Middle", "Ring", "Pinky", "Eye", "Jaw")


# ---------------------------------------------------------------- quatérnios XYZW
def qmul(a, b):
    ax, ay, az, aw = np.moveaxis(a, -1, 0)
    bx, by, bz, bw = np.moveaxis(b, -1, 0)
    return np.stack([aw * bx + ax * bw + ay * bz - az * by,
                     aw * by - ax * bz + ay * bw + az * bx,
                     aw * bz + ax * by - ay * bx + az * bw,
                     aw * bw - ax * bx - ay * by - az * bz], axis=-1)


def qinv(q):
    out = q.copy()
    out[..., :3] *= -1
    return out


def qnorm(q):
    return q / np.linalg.norm(q, axis=-1, keepdims=True)


def qpow(q, t):
    """q elevado a t (fração da rotação), q com w >= 0."""
    q = np.where(q[..., 3:4] < 0, -q, q)
    w = np.clip(q[..., 3], -1.0, 1.0)
    ang = 2 * np.arccos(w)
    s = np.sqrt(np.maximum(1 - w * w, 1e-12))
    axis = q[..., :3] / s[..., None]
    half = ang * t / 2
    out = np.concatenate([axis * np.sin(half)[..., None], np.cos(half)[..., None]], axis=-1)
    small = ang < 1e-8
    out[small] = [0, 0, 0, 1]
    return out


def yaw_of(quat_xyzw: np.ndarray) -> float:
    x, y, z, w = quat_xyzw
    fz = np.array([2 * (x * z + w * y), 2 * (y * z - w * x), 1 - 2 * (x * x + y * y)])
    return math.degrees(math.atan2(fz[0], fz[2]))


# ---------------------------------------------------------------- medidas
def relativas(world: np.ndarray, keep: list[int]) -> np.ndarray:
    rel = world[:, keep, :].copy()
    rel[:, :, 0] -= world[:, :1, 0]
    rel[:, :, 2] -= world[:, :1, 2]
    return rel


def medir_emenda(world: np.ndarray, motion: np.ndarray, names: list[str], keep: list[int]) -> dict:
    """Último quadro contra o primeiro (pose relativa à raiz no chão) e velocidade dos dois lados."""
    rel = relativas(world, keep)
    pose_diff = np.linalg.norm(rel[-1] - rel[0], axis=1) * 100
    v_ini = (rel[1] - rel[0]) * FPS
    v_fim = (rel[-1] - rel[-2]) * FPS
    vel_diff = np.linalg.norm(v_fim - v_ini, axis=1) * 100
    # aceleração na emenda tratando o ciclo como circular: q[N-1] -> q[0]=q[N] -> q[1]
    acel = np.linalg.norm(rel[1] - 2 * rel[0] + rel[-2], axis=1) * FPS * FPS * 100
    acel_dentro = np.linalg.norm(np.diff(rel, n=2, axis=0), axis=2) * FPS * FPS * 100
    root_v_ini = (world[1, 0, [0, 2]] - world[0, 0, [0, 2]]) * FPS
    root_v_fim = (world[-1, 0, [0, 2]] - world[-2, 0, [0, 2]]) * FPS
    desloc = world[-1, 0, [0, 2]] - world[0, 0, [0, 2]]
    dur = (len(world) - 1) / FPS
    return {
        "pose_dif_max_cm": round(float(pose_diff.max()), 2),
        "pose_dif_max_junta": names[keep[int(pose_diff.argmax())]],
        "pose_dif_media_cm": round(float(pose_diff.mean()), 2),
        "altura_quadril_dif_cm": round(float((world[-1, 0, 1] - world[0, 0, 1]) * 100), 2),
        "giro_raiz_dif_graus": round(yaw_of(motion[-1, 0, 3:]) - yaw_of(motion[0, 0, 3:]), 2),
        "velocidade_dif_max_cm_s": round(float(vel_diff.max()), 1),
        "velocidade_dif_max_junta": names[keep[int(vel_diff.argmax())]],
        "velocidade_dif_media_cm_s": round(float(vel_diff.mean()), 1),
        "aceleracao_na_emenda_max_cm_s2": round(float(acel.max())),
        "aceleracao_dentro_do_ciclo_p95_cm_s2": round(float(np.percentile(acel_dentro.max(axis=1), 95))),
        "aceleracao_dentro_do_ciclo_max_cm_s2": round(float(acel_dentro.max())),
        "raiz_vel_inicio_m_s": [round(float(v), 3) for v in root_v_ini],
        "raiz_vel_fim_m_s": [round(float(v), 3) for v in root_v_fim],
        "deslocamento_xz_m": [round(float(v), 3) for v in desloc],
        "velocidade_media_xz_m_s": [round(float(v / dur), 3) for v in desloc],
        "duracao_s": round(dur, 3),
        "quadros": int(len(world)),
    }


def pe_por_quadro(world: np.ndarray, contacts: np.ndarray, names: list[str]) -> dict:
    idx = {n: i for i, n in enumerate(names)}
    out = {}
    for lado, side, col_c, col_p in (("esquerdo", "Left", 0, 1), ("direito", "Right", 2, 3)):
        foot, toe = idx[f"{side}Foot"], idx[f"{side}ToeBase"]
        v_c = np.linalg.norm(np.diff(world[:, foot][:, [0, 2]], axis=0), axis=1) * FPS
        v_p = np.linalg.norm(np.diff(world[:, toe][:, [0, 2]], axis=0), axis=1) * FPS
        pc, pp = contacts[1:, col_c] > 0.5, contacts[1:, col_p] > 0.5
        out[lado] = {
            "quadros_com_calcanhar_plantado": int(pc.sum()),
            "deslize_calcanhar_cm_s": round(float(v_c[pc].mean()) * 100, 1) if pc.any() else None,
            "quadros_com_ponta_plantada": int(pp.sum()),
            "deslize_ponta_cm_s": round(float(v_p[pp].mean()) * 100, 1) if pp.any() else None,
            "altura_min_tornozelo_cm": round(float(world[:, foot, 1].min()) * 100, 1),
            "altura_min_dedos_cm": round(float(world[:, toe, 1].min()) * 100, 1),
        }
        # mesma medida da Unity (analisar_registro.py): cada ponto só conta enquanto está até
        # 1,5 cm acima do próprio mínimo; deriva do primeiro ao último quadro (ciclo circular)
        n = len(world) - 1
        for ponto, rot in ((foot, "tornozelo"), (toe, "dedos")):
            y = world[:n, ponto, 1]
            baixo = y < y.min() + 0.015
            if baixo.all() or not baixo.any():
                continue
            ini = int(np.argmin(baixo))  # começa num quadro "alto" para não cortar um apoio
            derivas = []
            k = 0
            while k < n:
                i = (ini + k) % n
                if baixo[i]:
                    comeco = k
                    while k < n and baixo[(ini + k) % n]:
                        k += 1
                    a_, b_ = ini + comeco, ini + k - 1
                    pa = world[a_ % n, ponto] + (world[n, 0] - world[0, 0]) * (a_ // n)
                    pb = world[b_ % n, ponto] + (world[n, 0] - world[0, 0]) * (b_ // n)
                    derivas.append(round(float(np.linalg.norm((pb - pa)[[0, 2]])) * 100, 1))
                k += 1
            out[lado][f"deriva_{rot}_no_chao_cm"] = derivas
    return out


# ---------------------------------------------------------------- limpeza do ciclo
def fechar_e_suavizar(cycle: np.ndarray, centros: list[int], direcao, sigma: float, raio_peso: float):
    """cycle: (N+1, J, 7), o último quadro deveria ser o primeiro deslocado no chão.

    1. Fecha o resíduo: cada rotação local recebe uma fração t/N da diferença entre o
       primeiro e o último quadro; a altura da raiz também. O deslocamento no chão fica só
       na direção do plano (tira a deriva para o lado).
    2. Suaviza, tratando o ciclo como circular, com peso só perto dos centros (emendas).
    Devolve (N+1, J, 7) com o último quadro igual ao primeiro, deslocado no chão.
    """
    cyc = cycle.copy()
    n = len(cyc) - 1
    t = (np.arange(n + 1) / n)[:, None, None]
    # 1. rotações
    q = qnorm(cyc[:, :, 3:])
    resid = qmul(q[0], qinv(q[n]))  # leva o último ao primeiro
    corr = qpow(np.broadcast_to(resid, q.shape).copy(), np.broadcast_to(t[..., 0], q.shape[:2]))
    q = qnorm(qmul(corr, q))
    cyc[:, :, 3:] = q
    # raiz: deslocamento desejado e resíduo periódico
    p = cyc[:, 0, :3].copy()
    d = p[n] - p[0]
    if direcao == "parado":
        d_chao = np.zeros(3)
    elif direcao is not None:
        u = np.array([direcao[0], 0.0, direcao[1]], dtype=float)
        u /= np.linalg.norm(u)
        d_chao = u * float(np.dot(d, u))
    else:
        d_chao = np.array([d[0], 0.0, d[2]])
    trend = p[0] + np.outer(np.arange(n + 1) / n, d_chao)
    e = p - trend
    e -= np.outer(np.arange(n + 1) / n, e[n] - e[0])  # fecha o resíduo
    # 2. suavização circular (frames 0..n-1 são únicos)
    uq, ue = q[:n], e[:n]
    k = np.arange(-4, 5)
    kern = np.exp(-(k ** 2) / (2 * sigma ** 2))
    kern /= kern.sum()
    sq = np.zeros_like(uq)
    se = np.zeros_like(ue)
    for i in range(n):
        idx = (i + k) % n
        nb = uq[idx]
        sign = np.sign(np.sum(nb * uq[i][None], axis=-1, keepdims=True))
        sign[sign == 0] = 1
        sq[i] = np.tensordot(kern, nb * sign, axes=(0, 0))
        se[i] = kern @ ue[idx]
    sq = qnorm(sq)
    dist = np.array([[min((i - c) % n, (c - i) % n) for c in centros] for i in range(n)]).min(axis=1)
    w = np.exp(-(dist ** 2) / (2 * raio_peso ** 2))[:, None]
    uq2 = qnorm(uq + w[..., None] * (sq - uq))
    ue2 = ue + w * (se - ue)
    out = np.empty_like(cyc)
    out[:n, :, :3] = cyc[:n, :, :3]
    out[:n, :, 3:] = uq2
    out[:n, 0, :3] = trend[:n] + ue2
    out[n] = out[0]
    out[n, 0, :3] = out[0, 0, :3] + d_chao
    return out


# ---------------------------------------------------------------- IK de perna
def ik_perna(pose: np.ndarray, skeleton: Skeleton, lado: str, alvo: np.ndarray) -> None:
    """Leva o tornozelo de `lado` ("Left"/"Right") ao ponto `alvo` (mundo), em `pose` (J, 7),
    por IK de dois ossos com o joelho no plano original; o pé mantém a orientação no mundo."""
    from poses import rotation_between, matrix_to_quat
    from bvh_writer import quat_to_matrix

    idx, pais = skeleton.index, skeleton.parents
    H, K, A = idx[f"{lado}Leg"], idx[f"{lado}Shin"], idx[f"{lado}Foot"]
    wr, wp_ = skeleton.fk(pose[:, :3], quat_to_matrix(pose[:, 3:]))
    h, k, a = wp_[H], wp_[K], wp_[A]
    l1, l2 = np.linalg.norm(k - h), np.linalg.norm(a - k)
    dvec = alvo - h
    d = np.clip(np.linalg.norm(dvec), abs(l1 - l2) + 1e-4, l1 + l2 - 1e-4)
    u = dvec / np.linalg.norm(dvec)
    v = (k - h) - np.dot(k - h, u) * u
    v /= max(np.linalg.norm(v), 1e-9)
    cos_a = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    k_novo = h + l1 * (cos_a * u + math.sqrt(max(0.0, 1 - cos_a * cos_a)) * v)
    a_novo = h + d * u
    giro_h = rotation_between(k - h, k_novo - h)
    r_h = giro_h @ wr[H]
    r_k_tmp = giro_h @ wr[K]
    r_k = rotation_between(giro_h @ (a - k), a_novo - k_novo) @ r_k_tmp
    pose[H, 3:] = matrix_to_quat(wr[pais[H]].T @ r_h)
    pose[K, 3:] = matrix_to_quat(r_h.T @ r_k)
    pose[A, 3:] = matrix_to_quat(r_k.T @ wr[A])


# ---------------------------------------------------------------- foot lock
DIAG: dict = {}  # diagnóstico do foot lock: (quadro, tipo, peso, correção cm, excesso sobre a perna esticada cm)
def travar_pes(ciclo: np.ndarray, contatos: np.ndarray, skeleton: Skeleton, rampa: int = 2,
               tol_calcanhar: float = 0.02, tol_ponta: float = 0.015, vel_max: float = 0.8,
               vel_max_calcanhar: float = 0.8) -> np.ndarray:
    # vel_max_calcanhar = 2,0 foi testado: o tornozelo direito não melhorou (9,5 cm) e a trava
    # passou a criar um pico de aceleração (6.183 contra 4.578 cm/s2). Ficou 0,8.
    """Prende o pé apoiado no chão (XZ), como no cleanup de mocap.

    Usa o contato previsto pelo MotionBricks: com o calcanhar apoiado, o ponto preso é o
    tornozelo; com só a ponta apoiada, é a base dos dedos. Em cada intervalo de apoio o ponto
    fica na posição média dele no intervalo; a perna (coxa e canela) é ajustada por IK de dois
    ossos, com o joelho no plano original, e o pé mantém a orientação que tinha no mundo.
    Entrada e saída do travamento em rampa de `rampa` quadros. O ciclo é tratado como
    circular: (N+1, J, 7), o último quadro é o primeiro deslocado.
    """
    from poses import rotation_between, matrix_to_quat
    from bvh_writer import quat_to_matrix

    n = len(ciclo) - 1
    desloc = ciclo[n, 0, :3] - ciclo[0, 0, :3]
    # três cópias do ciclo, para os apoios que atravessam a emenda
    tri = np.concatenate([ciclo[:n], ciclo[:n], ciclo[:n]], axis=0)
    for c in range(3):
        tri[c * n:(c + 1) * n, 0, :3] += desloc * (c - 1)
    cont = np.concatenate([contatos[:n]] * 3, axis=0)
    out = tri.copy()
    idx = skeleton.index
    pais = skeleton.parents

    for lado, col_c, col_p in (("Left", 0, 1), ("Right", 2, 3)):
        H, K, A, T = idx[f"{lado}Leg"], idx[f"{lado}Shin"], idx[f"{lado}Foot"], idx[f"{lado}ToeBase"]
        w_all = np.array([skeleton.fk(p[:, :3], quat_to_matrix(p[:, 3:]))[1] for p in tri])
        # rótulo por quadro: 2 = calcanhar apoiado (trava tornozelo), 1 = só ponta (trava dedos), 0 = no ar.
        # Pela altura real do tornozelo e dos dedos: o rótulo de contato do modelo deixava de fora
        # justamente os quadros em que o pé escorregava.
        y_a, y_t = w_all[:, A, 1], w_all[:, T, 1]

        def vel_xz(j):  # velocidade no chão, centrada, em m/s
            p = w_all[:, j][:, [0, 2]]
            v = np.zeros(len(p))
            v[1:-1] = np.linalg.norm(p[2:] - p[:-2], axis=1) * FPS / 2
            v[0], v[-1] = v[1], v[-2]
            return v
        # baixo E quase parado: a ponta do pé no ar passa rente ao chão no balanço, mas rápida
        # o calcanhar do modelo chega ao chão ainda andando: limite de velocidade maior para ele
        calc = (y_a < y_a.min() + tol_calcanhar) & (vel_xz(A) < vel_max_calcanhar)
        ponta = (y_t < y_t.min() + tol_ponta) & (vel_xz(T) < vel_max)
        rot = np.where(calc, 2, np.where(ponta, 1, 0))
        alvo = np.full((len(tri), 2), np.nan)
        peso = np.zeros(len(tri))
        i = 0
        while i < len(tri):
            if rot[i] == 0:
                i += 1
                continue
            j = i
            while j + 1 < len(tri) and rot[j + 1] == rot[i]:
                j += 1
            ponto = A if rot[i] == 2 else T
            trava = w_all[i:j + 1, ponto][:, [0, 2]].mean(axis=0)
            for f in range(i, j + 1):
                corr = trava - w_all[f, ponto][[0, 2]]
                alvo[f] = w_all[f, A][[0, 2]] + corr
                borda = min(f - i, j - f)
                peso[f] = min(1.0, (borda + 1) / (rampa + 1)) if (j - i) > 2 * rampa else 0.5
            i = j + 1
        for f in range(len(tri)):
            if peso[f] <= 0 or np.isnan(alvo[f, 0]):
                continue
            pos, rotm = out[f, :, :3], quat_to_matrix(out[f, :, 3:])
            wr, wp_ = skeleton.fk(pos, rotm)
            h, k, a = wp_[H], wp_[K], wp_[A]
            meta = a.copy()
            meta[[0, 2]] = a[[0, 2]] + peso[f] * (alvo[f] - a[[0, 2]])
            l1, l2 = np.linalg.norm(k - h), np.linalg.norm(a - k)
            dvec = meta - h
            if f >= n and f < 2 * n:
                DIAG.setdefault(lado, []).append((f - n, int(rot[f]), round(float(peso[f]), 2),
                                                  round(float(np.linalg.norm(alvo[f] - a[[0, 2]])) * 100, 1),
                                                  round(float(np.linalg.norm(dvec) - (l1 + l2)) * 100, 1)))
            d = np.clip(np.linalg.norm(dvec), abs(l1 - l2) + 1e-4, l1 + l2 - 1e-4)
            u = dvec / np.linalg.norm(dvec)
            v = (k - h) - np.dot(k - h, u) * u
            v /= max(np.linalg.norm(v), 1e-9)
            cos_a = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
            k_novo = h + l1 * (cos_a * u + math.sqrt(max(0.0, 1 - cos_a * cos_a)) * v)
            a_novo = h + d * u
            r_h = rotation_between(k - h, k_novo - h) @ wr[H]
            r_k_tmp = rotation_between(k - h, k_novo - h) @ wr[K]
            r_k = rotation_between(r_k_tmp @ np.linalg.inv(wr[K]) @ (a - k), a_novo - k_novo) @ r_k_tmp
            r_a = wr[A]  # o pé mantém a orientação no mundo
            loc_h = wr[pais[H]].T @ r_h
            loc_k = r_h.T @ r_k
            loc_a = r_k.T @ r_a
            out[f, H, 3:] = matrix_to_quat(loc_h)
            out[f, K, 3:] = matrix_to_quat(loc_k)
            out[f, A, 3:] = matrix_to_quat(loc_a)
            if f >= n and f < 2 * n:
                _, wp_novo = skeleton.fk(out[f, :, :3], quat_to_matrix(out[f, :, 3:]))
                DIAG.setdefault(lado + "_erro_cm", []).append(
                    (f - n, round(float(np.linalg.norm(wp_novo[A] - meta)) * 100, 2),
                     round(float(np.linalg.norm(wp_novo[K] - k_novo)) * 100, 2)))
    return out[n:2 * n + 1].copy()  # a cópia do meio; o último quadro é o primeiro da terceira


# ---------------------------------------------------------------- geração
def run(plan: dict, out_dir: Path, name: str) -> dict:
    import warp as wp
    from motionbricks.io.usd import load_skeleton_from_usd
    from motionbricks.io.utils import SOMA_SKELETON_PRIM_PATH, get_asset_file
    from motionbricks.model.config import MotionBricksInferenceConfig
    from motionbricks.model.contract import MODEL_POSES_PER_TOKEN
    from motionbricks.model.soma.contract import SOMA_N1_FP32_ONNX_PATH
    from motionbricks.model.soma.engine import MotionBricksSOMAEngine

    for spec in [plan["inicio"], *plan["destinos"]]:
        if "clipe" in spec:
            raise SystemExit("este gerador só aceita poses próprias: tire o \"clipe\" do plano")

    wp.init()
    mb_skeleton = load_skeleton_from_usd(
        get_asset_file("human", "soma_base_skel_minimal_no_root.usd"), SOMA_SKELETON_PRIM_PATH)
    names = list(mb_skeleton.joint_names)
    parents = [mb_skeleton.joint_parent(i) for i in range(mb_skeleton.num_joints)]
    rest = mb_skeleton.reference_local_transforms.numpy().reshape(-1, 7).astype(np.float64)
    skeleton = Skeleton(names, parents, rest)
    built = build_poses(skeleton, plan.get("poses", {}))
    keep = [i for i, n in enumerate(names) if not any(h in n for h in ESCONDER)]
    early = int(plan.get("transicao_antecipada", 0))

    wp.set_device("cuda:0")
    engine = MotionBricksSOMAEngine(SOMA_N1_FP32_ONNX_PATH)
    segments, contacts, marks, report = [], [], [], []
    total = 0
    with engine, wp.ScopedStream(engine.stream):
        context = engine.create_input(mb_skeleton)
        target = engine.create_input(mb_skeleton)
        output = engine.create_output(mb_skeleton)

        def window(spec: dict, as_context: bool) -> np.ndarray:
            pose = built[spec["pose"]].array()[None]
            vel = spec.get("velocidade_alvo", plan.get("velocidade_alvo")) if not as_context else None
            static = as_context or bool(spec.get("parar")) or vel is not None
            poses = np.repeat(pose, MODEL_POSES_PER_TOKEN, axis=0) if static else pose
            poses = place_window(poses, spec.get("posicao"), float(spec.get("giro", 0.0)))
            if vel is not None and not spec.get("parar"):
                for k in range(len(poses)):
                    poses[k, 0, 0] += float(vel[0]) * k / FPS
                    poses[k, 0, 2] += float(vel[1]) * k / FPS
                # "apoio": o destino deixa de ser um bloco rígido. O pé de apoio fica parado
                # no chão e o outro anda ao dobro da velocidade (IK de perna), como num passo.
                apoio = spec.get("apoio")
                if apoio:
                    livre = "Right" if apoio == "Left" else "Left"
                    w0 = skeleton.world_positions(poses[0])
                    a_apoio = w0[skeleton.index[f"{apoio}Foot"]].copy()
                    a_livre = w0[skeleton.index[f"{livre}Foot"]].copy()
                    for k in range(1, len(poses)):
                        passo = np.array([float(vel[0]), 0.0, float(vel[1])]) * 2 * k / FPS
                        ik_perna(poses[k], skeleton, apoio, a_apoio)
                        ik_perna(poses[k], skeleton, livre, a_livre + passo)
            return poses

        def to_device(poses: np.ndarray):
            return wp.array(poses.astype(np.float32), dtype=wp.transform, device=engine.device)

        context_poses = window(plan["inicio"], as_context=True)
        for number, spec in enumerate(plan["destinos"], 1):
            tokens = spec.get("tokens")
            opcoes = {}
            if tokens:
                opcoes["allowed_token_counts"] = (int(tokens),)
            if not plan.get("corrigir_pontas", True):
                opcoes["correct_generated_diff"] = False
            config = MotionBricksInferenceConfig(**opcoes) if opcoes else None
            goal = window(spec, as_context=False)
            context.update_from_poses(to_device(context_poses), stream=engine.stream)
            target.update_from_poses(to_device(goal), stream=engine.stream)
            engine.generate_animation(context, target, output, config=config)
            engine.synchronize()
            frames = int(output.num_frames)
            poses = output.poses.numpy()[:frames].astype(np.float64).reshape(frames, -1, 7)
            feet = output.foot_contacts.numpy()[:frames].astype(np.float64)
            last = number == len(plan["destinos"])
            cut = frames if (last or not early) else frames - early
            end_world = skeleton.world_positions(poses[-1])
            goal_world = skeleton.world_positions(goal[0])
            poses, feet = poses[:cut], feet[:cut]
            junction = total - 1 if segments else 0
            ks = slice(1, None) if segments else slice(None)
            segments.append(poses[ks])
            contacts.append(feet[ks])
            total += len(poses[ks])
            label = spec.get("nome") or f"destino_{number}"
            marks.append({"nome": label, "inicio": junction, "fim": total - 1,
                          "candidato": bool(spec.get("candidato"))})
            report.append({
                "nome": label, "pose": spec["pose"], "tokens": tokens, "quadros_gerados": frames,
                "quadros_usados": cut, "erro_ate_a_pose_no_fim_cm": round(float(np.abs(end_world - goal_world).max()) * 100, 2),
            })
            context_poses = poses[-MODEL_POSES_PER_TOKEN:]

    motion = np.concatenate(segments, axis=0)
    feet = np.concatenate(contacts, axis=0)
    world = skeleton.world_positions(motion)
    out_dir.mkdir(parents=True, exist_ok=True)
    rest_foot = float(min(skeleton.rest_world_pos[skeleton.index[n]][1] for n in ("LeftFoot", "RightFoot")))
    juncoes = [m["inicio"] for m in marks[1:]]

    write_bvh(out_dir / f"{name}_cadeia.bvh", names, parents, rest, motion, fps=FPS)
    tira.draw(out_dir / f"{name}_cadeia.tira.png", world, names, parents, marks)
    rel = relativas(world, keep)
    spd = np.linalg.norm(np.diff(rel, axis=0), axis=2) * FPS * 100
    acc = np.linalg.norm(np.diff(rel, n=2, axis=0), axis=2) * FPS * FPS * 100
    (out_dir / f"{name}_cadeia.perfil.json").write_text(json.dumps({
        "juntas": [names[i] for i in keep], "limites_das_geracoes": juncoes + [total - 1],
        "vel_media_cm_s": [round(float(v), 1) for v in spd.mean(axis=1)],
        "vel_max_cm_s": [round(float(v), 1) for v in spd.max(axis=1)],
        "vel_max_junta": [names[keep[int(j)]] for j in spd.argmax(axis=1)],
        "acel_max_cm_s2": [round(float(v)) for v in acc.max(axis=1)],
        "acel_max_junta": [names[keep[int(j)]] for j in acc.argmax(axis=1)],
        "raiz_vel_m_s": [[round(float(v), 3) for v in r] for r in np.diff(world[:, 0, [0, 2]], axis=0) * FPS],
    }, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- escolha do trecho do ciclo
    if "periodo" in plan:
        per = int(plan["periodo"])
        skip = int(plan.get("ignorar_geracoes", 2))
        first = marks[skip]["inicio"] if skip < len(marks) else 0
        best = None
        for i in range(first, total - per - 1):
            pd = np.linalg.norm(rel[i + per] - rel[i], axis=1).mean() * 100
            vd = np.linalg.norm((rel[i + per + 1] - rel[i + per]) - (rel[i + 1] - rel[i]), axis=1).mean() * FPS * 100
            cost = pd + 0.05 * vd
            if best is None or cost < best[0]:
                best = (cost, i)
        a, b = best[1], best[1] + per
        escolha = {"modo": "periodo", "quadros_na_cadeia": [a, b], "custo": round(float(best[0]), 3)}
    else:
        n_seg = int(plan.get("segmentos_no_ciclo", 1))
        cands = []
        for k, m in enumerate(marks):
            if m["candidato"] and k - n_seg + 1 >= 0:
                a, b = marks[k - n_seg + 1]["inicio"], m["fim"]
                em = medir_emenda(world[a:b + 1], motion[a:b + 1], names, keep)
                cands.append((em["velocidade_dif_max_cm_s"], a, b, m["nome"]))
        if not cands:
            raise SystemExit("nenhum destino marcado com \"candidato\": true")
        _, a, b, nome_c = min(cands)
        escolha = {"modo": "candidato", "destino": nome_c, "quadros_na_cadeia": [a, b]}

    bruto = motion[a:b + 1].copy()
    antes = medir_emenda(world[a:b + 1], bruto, names, keep)
    centros = sorted({0, *[(j - a) % (b - a) for j in juncoes if a < j < b]})
    ciclo = fechar_e_suavizar(bruto, centros, plan.get("direcao"),
                              sigma=float(plan.get("suavizar_sigma", 1.5)),
                              raio_peso=float(plan.get("suavizar_raio", 3.0)))
    ciclo[:, 0, 0] -= ciclo[0, 0, 0]
    ciclo[:, 0, 2] -= ciclo[0, 0, 2]
    ciclo_feet = feet[a:b + 1].copy()
    pes_antes = pe_por_quadro(skeleton.world_positions(ciclo), ciclo_feet, names)
    if plan.get("travar_pes"):
        ciclo = travar_pes(ciclo, ciclo_feet, skeleton)
    ciclo_world = skeleton.world_positions(ciclo)
    depois = medir_emenda(ciclo_world, ciclo, names, keep)
    mudanca = np.linalg.norm(relativas(ciclo_world, keep) - relativas(skeleton.world_positions(bruto), keep), axis=2) * 100

    summary = write_bvh(out_dir / f"{name}.bvh", names, parents, rest, ciclo, fps=FPS)
    write_contacts(out_dir / f"{name}.contatos.json", ciclo_feet, fps=FPS)
    tira.draw(out_dir / f"{name}.tira.png", ciclo_world, names, parents,
              [{"nome": f"{name} (ciclo)", "inicio": 0, "fim": len(ciclo) - 1}], columns=12)
    summary.pop("juntas_com_posicao", None)
    summary.update({
        "clipe": name,
        "ciclo": escolha,
        "emendas_de_geracao_dentro_do_ciclo": centros[1:],
        "emenda_antes_da_limpeza": antes,
        "emenda_depois_da_limpeza": depois,
        "limpeza_mexeu_na_pose_cm": {"max": round(float(mudanca.max()), 2), "media": round(float(mudanca.mean()), 2)},
        "medidas_do_ciclo": tira.measure(ciclo_world, ciclo_feet, names, FPS, rest_foot),
        "pes_no_ciclo": pe_por_quadro(ciclo_world, ciclo_feet, names),
        "pes_antes_do_travamento": pes_antes if plan.get("travar_pes") else None,
        "diagnostico_foot_lock": {k: [list(x) for x in v] for k, v in DIAG.items()},
        "geracoes": report,
        "esqueleto": "SOMA",
        "poses_de": "poses próprias do plano",
        "usou_clipes_de_exemplo": False,
    })
    (out_dir / f"{name}.relatorio.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                                    encoding="utf-8")
    return summary


def gravar_pose_t(caminho: Path) -> None:
    """BVH de 2 quadros parados na pose de repouso (T) do SOMA: base do avatar na Unity."""
    import warp as wp
    from motionbricks.io.usd import load_skeleton_from_usd
    from motionbricks.io.utils import SOMA_SKELETON_PRIM_PATH, get_asset_file

    wp.init()
    sk = load_skeleton_from_usd(get_asset_file("human", "soma_base_skel_minimal_no_root.usd"), SOMA_SKELETON_PRIM_PATH)
    names = list(sk.joint_names)
    parents = [sk.joint_parent(i) for i in range(sk.num_joints)]
    rest = sk.reference_local_transforms.numpy().reshape(-1, 7).astype(np.float64)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps(write_bvh(caminho, names, parents, rest, np.repeat(rest[None], 2, axis=0), fps=FPS), ensure_ascii=False))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) == 3 and sys.argv[1] == "--pose-t":
        gravar_pose_t(Path(sys.argv[2]))
        return 0
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plano")
    parser.add_argument("--saida", required=True)
    parser.add_argument("--nome", required=True)
    args = parser.parse_args()
    plan = json.loads(Path(args.plano).read_text(encoding="utf-8-sig"))
    summary = run(plan, Path(args.saida), args.nome)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
