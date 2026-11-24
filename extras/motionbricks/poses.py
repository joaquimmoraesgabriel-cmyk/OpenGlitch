"""Monta poses de um esqueleto por código, sem clipe nenhum. Só depende de numpy.

Uma pose é descrita por direções no espaço do personagem, e não por ângulos de
junta, que dependem dos eixos locais de cada osso e são fáceis de errar:

    {"mirar": [["LeftArm", "LeftForeArm", [0.2, -1, 0]]], "pes_no_chao": true}

quer dizer "gire o braço esquerdo até o osso que vai de LeftArm a LeftForeArm
apontar para baixo e um pouco para fora". Espaço do modelo SOMA: +Y para cima,
+Z para a frente do personagem, +X para o lado esquerdo dele. Metros.

Campos de uma pose:
  base         nome de outra pose já definida, ou "repouso" (padrão), a pose T
  lugar        [x, z] do quadril no chão, em metros. Use quando a pose tem lugar certo na
               cena (ao lado de um obstáculo): no destino, não use "posicao"
  mirar        lista de [junta, filho, [x, y, z]], aplicada na ordem dada;
               mire do tronco para as pontas (quadril, coxa, canela, braço, antebraço)
  alcancar     lista de [ponta, [x, y, z]] ou [ponta, [x, y, z], [dobra x, y, z]]: leva a mão
               ou o pé (LeftHand, RightFoot...) ao ponto dado no mundo, dobrando cotovelo ou
               joelho. É como apoiar a mão na borda de um bloco ou o pé em cima dele. O
               terceiro item diz para que lado a dobra aponta; sem ele, fica o lado atual.
               Se o ponto estiver fora do alcance, o membro estica na direção dele.
               Aplicado depois de mirar e antes de pe_plano.
  pe_plano     lista de juntas que voltam à orientação de repouso no mundo,
               depois de mirar; use nos pés para a sola ficar no chão
  pes_no_chao  sobe ou desce o quadril até o pé mais baixo encostar no chão
  altura       soma este valor, em metros, à altura do quadril (um salto, por exemplo)
  posicoes     {junta: [x, y, z]} com a posição de cada junta no mundo, em metros. É como
               entra uma pose feita no Blender (blender_exportar.py): o quadril vai para a
               posição dada e cada osso é girado até os filhos caírem onde foram pedidos.
               Aplicado antes de mirar. Uma pose assim já tem lugar e altura próprios:
               no destino, não use "posicao".
"""

from __future__ import annotations

import numpy as np

from bvh_writer import quat_to_matrix


def matrix_to_quat(m: np.ndarray) -> np.ndarray:
    """Matriz de rotação 3x3 para quatérnio XYZW."""
    trace = np.trace(m)
    if trace > 0:
        s = np.sqrt(trace + 1.0) * 2
        q = [(m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s, 0.25 * s]
    else:
        i = int(np.argmax(np.diag(m)))
        j, k = (i + 1) % 3, (i + 2) % 3
        s = np.sqrt(max(1.0 + m[i, i] - m[j, j] - m[k, k], 1e-12)) * 2
        q = [0.0, 0.0, 0.0, 0.0]
        q[i] = 0.25 * s
        q[j] = (m[j, i] + m[i, j]) / s
        q[k] = (m[k, i] + m[i, k]) / s
        q[3] = (m[k, j] - m[j, k]) / s
    q = np.asarray(q, dtype=float)
    return q / np.linalg.norm(q)


def rotation_between(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """A menor rotação que leva a direção `a` à direção `b`."""
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    v, c = np.cross(a, b), float(np.dot(a, b))
    if c < -1.0 + 1e-9:  # direções opostas: meia volta em torno de um eixo perpendicular
        axis = np.cross(a, [1.0, 0.0, 0.0])
        if np.linalg.norm(axis) < 1e-6:
            axis = np.cross(a, [0.0, 0.0, 1.0])
        axis /= np.linalg.norm(axis)
        return 2.0 * np.outer(axis, axis) - np.eye(3)
    if np.linalg.norm(v) < 1e-12:
        return np.eye(3)
    k = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + k + k @ k / (1.0 + c)


def _best_rotation(have: np.ndarray, want: np.ndarray) -> np.ndarray:
    """A rotação que melhor leva os vetores `have` aos vetores `want` (Kabsch).

    Se os vetores estiverem todos na mesma linha, a torção em volta dela fica indefinida:
    cai na menor rotação do primeiro.
    """
    a = have / np.linalg.norm(have, axis=1, keepdims=True)
    b = want / np.linalg.norm(want, axis=1, keepdims=True)
    u, s, vt = np.linalg.svd(b.T @ a)
    if s[1] < 1e-4:
        return rotation_between(have[0], want[0])
    d = np.sign(np.linalg.det(u @ vt))
    return u @ np.diag([1.0, 1.0, d]) @ vt


class Skeleton:
    """Hierarquia e pose de repouso: nomes, pais e (J, 7) com posição e quatérnio XYZW locais."""

    def __init__(self, names, parents, rest):
        self.names = [str(n) for n in names]
        self.parents = [int(p) for p in parents]
        self.rest = np.asarray(rest, dtype=float).reshape(len(self.names), 7)
        self.index = {n: i for i, n in enumerate(self.names)}
        self.rest_rot = quat_to_matrix(self.rest[:, 3:])
        self.rest_world_rot, self.rest_world_pos = self.fk(self.rest[:, :3], self.rest_rot)

    def joint(self, name: str) -> int:
        if name not in self.index:
            close = [n for n in self.names if name.lower() in n.lower()][:6]
            raise ValueError(f"junta desconhecida: {name}" + (f". Parecidas: {', '.join(close)}" if close else ""))
        return self.index[name]

    def fk(self, local_pos, local_rot):
        world_rot = np.empty((len(self.names), 3, 3))
        world_pos = np.empty((len(self.names), 3))
        for j, parent in enumerate(self.parents):
            if parent < 0:
                world_rot[j], world_pos[j] = local_rot[j], local_pos[j]
            else:
                world_rot[j] = world_rot[parent] @ local_rot[j]
                world_pos[j] = world_pos[parent] + world_rot[parent] @ local_pos[j]
        return world_rot, world_pos

    def world_positions(self, poses: np.ndarray) -> np.ndarray:
        """(F, J, 7) ou (J, 7) de poses locais para posições no mundo."""
        poses = np.asarray(poses, dtype=float)
        single = poses.ndim == 2
        frames = poses[None] if single else poses
        out = np.array([self.fk(p[:, :3], quat_to_matrix(p[:, 3:]))[1] for p in frames])
        return out[0] if single else out


class Pose:
    def __init__(self, skeleton: Skeleton, base: "Pose | None" = None):
        self.sk = skeleton
        self.pos = (base.pos if base else skeleton.rest[:, :3]).copy()
        self.rot = (base.rot if base else skeleton.rest_rot).copy()

    def aim(self, joint: str, child: str, direction) -> "Pose":
        j, c = self.sk.joint(joint), self.sk.joint(child)
        direction = np.asarray(direction, dtype=float)
        if direction.shape != (3,) or np.linalg.norm(direction) < 1e-9:
            raise ValueError(f"direção inválida para {joint}: {direction}")
        world_rot, world_pos = self.sk.fk(self.pos, self.rot)
        bone = world_pos[c] - world_pos[j]
        if np.linalg.norm(bone) < 1e-9:
            raise ValueError(f"{child} está no mesmo ponto que {joint}: não dá para mirar")
        new_world = rotation_between(bone, direction) @ world_rot[j]
        parent = self.sk.parents[j]
        self.rot[j] = (world_rot[parent].T if parent >= 0 else np.eye(3)) @ new_world
        return self

    def fit_positions(self, targets: dict) -> "Pose":
        """Gira os ossos, do tronco para as pontas, até as juntas caírem nas posições dadas.

        Com um filho só, o osso é mirado nele (a torção em volta do próprio eixo fica a do
        pai). Com dois ou mais, como quadril, peito e mão, a rotação que melhor encaixa
        todos os filhos dá também a torção. O comprimento dos ossos não muda: se as
        posições pedidas tiverem outras proporções, o encaixe é o mais próximo possível.
        """
        goal = {self.sk.joint(name): np.asarray(p, dtype=float) for name, p in targets.items()}
        for j, p in goal.items():
            if p.shape != (3,):
                raise ValueError(f"posição inválida para {self.sk.names[j]}: {p}")
        if 0 in goal:
            self.pos[0] = goal[0]
        children: dict[int, list[int]] = {}
        for j, parent in enumerate(self.sk.parents):
            if parent >= 0 and j in goal:
                children.setdefault(parent, []).append(j)
        for j in range(len(self.sk.names)):                 # os pais vêm antes dos filhos
            kids = children.get(j)
            if not kids:
                continue
            world_rot, world_pos = self.sk.fk(self.pos, self.rot)
            # A junta está onde a cadeia a deixou; os filhos são medidos a partir do pedido.
            origin = goal.get(j, world_pos[j])
            have = np.array([world_pos[k] - world_pos[j] for k in kids])
            want = np.array([goal[k] - origin for k in kids])
            keep = (np.linalg.norm(have, axis=1) > 1e-6) & (np.linalg.norm(want, axis=1) > 1e-6)
            have, want = have[keep], want[keep]
            if len(have) == 0:
                continue
            delta = _best_rotation(have, want) if len(have) > 1 else rotation_between(have[0], want[0])
            parent = self.sk.parents[j]
            self.rot[j] = (world_rot[parent].T if parent >= 0 else np.eye(3)) @ delta @ world_rot[j]
        return self

    def reach(self, end: str, target, bend=None) -> float:
        """Leva a ponta de um membro (mão ou pé) ao ponto dado, por IK de dois ossos.

        Devolve a distância que faltou, em metros: zero quando o ponto está ao alcance.
        """
        e = self.sk.joint(end)
        m = self.sk.parents[e]
        r = self.sk.parents[m] if m >= 0 else -1
        if r < 0:
            raise ValueError(f"{end} não é a ponta de um membro de dois ossos")
        target = np.asarray(target, dtype=float)
        if target.shape != (3,):
            raise ValueError(f"ponto inválido para {end}: {target}")
        _, world = self.sk.fk(self.pos, self.rot)
        upper, lower = np.linalg.norm(world[m] - world[r]), np.linalg.norm(world[e] - world[m])
        to_target = target - world[r]
        wanted = float(np.linalg.norm(to_target))
        if wanted < 1e-6:
            raise ValueError(f"o ponto pedido para {end} coincide com a raiz do membro")
        axis = to_target / wanted
        distance = float(np.clip(wanted, abs(upper - lower) + 1e-4, upper + lower - 1e-4))
        # Para que lado dobra: o pedido, ou o lado em que o cotovelo/joelho já está.
        hint = np.asarray(bend, dtype=float) if bend is not None else world[m] - world[r]
        side = hint - axis * float(np.dot(hint, axis))
        if np.linalg.norm(side) < 1e-6:                       # membro esticado: usa o lado de repouso
            rest = self.sk.rest_world_pos
            side = (rest[e] - rest[m]) - axis * float(np.dot(rest[e] - rest[m], axis))
            for other in ([0.0, 0.0, 1.0], [1.0, 0.0, 0.0]):   # qualquer lado perpendicular serve
                if np.linalg.norm(side) < 1e-6:
                    side = np.cross(axis, other)
        side /= np.linalg.norm(side)
        along = (upper ** 2 - lower ** 2 + distance ** 2) / (2 * distance)
        height = float(np.sqrt(max(upper ** 2 - along ** 2, 0.0)))
        middle = world[r] + axis * along + side * height
        end_point = world[r] + axis * distance
        self.aim(self.sk.names[r], self.sk.names[m], middle - world[r])
        self.aim(self.sk.names[m], self.sk.names[e], end_point - middle)
        return abs(wanted - distance) if wanted != distance else 0.0

    def keep_rest_orientation(self, joint: str) -> "Pose":
        j = self.sk.joint(joint)
        world_rot, _ = self.sk.fk(self.pos, self.rot)
        parent = self.sk.parents[j]
        self.rot[j] = (world_rot[parent].T if parent >= 0 else np.eye(3)) @ self.sk.rest_world_rot[j]
        return self

    def feet_on_ground(self, feet=("LeftFoot", "RightFoot")) -> "Pose":
        present = [f for f in feet if f in self.sk.index]
        if not present:
            return self
        _, world_pos = self.sk.fk(self.pos, self.rot)
        lowest = min(world_pos[self.sk.index[f]][1] for f in present)
        rest_height = min(self.sk.rest_world_pos[self.sk.index[f]][1] for f in present)
        self.pos[0, 1] += rest_height - lowest
        return self

    def array(self) -> np.ndarray:
        out = np.zeros((len(self.sk.names), 7))
        out[:, :3] = self.pos
        out[:, 3:] = [matrix_to_quat(m) for m in self.rot]
        return out

    def world(self) -> np.ndarray:
        return self.sk.fk(self.pos, self.rot)[1]


def stable_bend(skeleton: Skeleton, world_rot: np.ndarray, world_pos: np.ndarray, end: str) -> np.ndarray | None:
    """Para que lado o joelho dobra quando a perna está quase esticada: a frente do quadril.

    Com a perna esticada, o lado em que o joelho "já está" é ruído e o IK troca de lado de um
    quadro para o outro (um salto de vários m/s na canela). Para o braço, devolve None.
    """
    if not end.endswith("Foot"):
        return None
    e = skeleton.joint(end)
    m = skeleton.parents[e]
    r = skeleton.parents[m]
    axis = world_pos[e] - world_pos[r]
    axis /= max(float(np.linalg.norm(axis)), 1e-9)
    knee = world_pos[m] - world_pos[r]
    side = knee - axis * float(np.dot(knee, axis))
    forward = world_rot[0] @ skeleton.rest_world_rot[0].T @ np.array([0.0, 0.0, 1.0])
    return side if float(np.linalg.norm(side)) > 0.05 else forward


def avoid(skeleton: Skeleton, frames: np.ndarray, boxes: list, margin: float = 0.01) -> tuple[np.ndarray, dict]:
    """Tira mãos e pés de dentro dos obstáculos, depois de gerar.

    O modelo não enxerga a cena. As poses e o `fixar` resolvem o grosso; o que sobra costuma ser
    a ponta do pé raspando a quina por poucos centímetros. Aqui, em cada quadro, a ponta de cada
    membro (tornozelo com os dedos; punho) é empurrada para fora pela face mais próxima, o pé de
    preferência por cima, e o membro é refeito por IK. O empurrão é suavizado no tempo (nunca
    menor que o necessário), para não virar um tranco. Não mexe em quadril, joelho nem tronco:
    isso se corrige na pose. Devolve os quadros e, por membro, o maior desvio e em quantos quadros.
    """
    frames = np.asarray(frames, dtype=float).copy()
    limbs = {"LeftFoot": ("LeftFoot", "LeftToeBase", "LeftToeEnd"), "RightFoot": ("RightFoot", "RightToeBase", "RightToeEnd"),
             "LeftHand": ("LeftHand",), "RightHand": ("RightHand",)}
    count = len(frames)
    world = skeleton.world_positions(frames)
    kernel = np.exp(-(np.arange(-4, 5) ** 2) / (2 * 1.5 ** 2))
    kernel /= kernel.sum()

    def envelope(values: np.ndarray) -> np.ndarray:
        pad = np.pad(values, 3, mode="edge")
        widest = np.max(np.stack([pad[i:i + count] for i in range(7)]), axis=0)
        smooth = np.convolve(np.pad(widest, 4, mode="edge"), kernel, mode="valid")
        return np.maximum(smooth, values)

    report = {}
    for end, points in limbs.items():
        index = [skeleton.index[n] for n in points if n in skeleton.index]
        if end not in skeleton.index:
            continue
        push = np.zeros((count, 3))
        for f in range(count):
            best = np.zeros(3)
            for box in boxes:
                for j in index:
                    move = box.exit(world[f, j], margin, lift=end.endswith("Foot"))
                    if float(np.linalg.norm(move)) > float(np.linalg.norm(best)):
                        best = move
            push[f] = best
        if not push.any():
            continue
        smooth = np.stack([envelope(np.maximum(push[:, c], 0.0)) - envelope(np.maximum(-push[:, c], 0.0)) for c in range(3)], axis=1)
        j = skeleton.joint(end)
        moved = np.where(np.linalg.norm(smooth, axis=1) > 0.002)[0]
        for f in moved:
            pose = Pose(skeleton)
            pose.pos, pose.rot = frames[f, :, :3].copy(), quat_to_matrix(frames[f, :, 3:])
            world_rot, world_pos = skeleton.fk(pose.pos, pose.rot)
            keep = world_rot[j].copy()
            pose.reach(end, world_pos[j] + smooth[f], bend=stable_bend(skeleton, world_rot, world_pos, end))
            world_rot, _ = skeleton.fk(pose.pos, pose.rot)
            pose.rot[j] = world_rot[skeleton.parents[j]].T @ keep
            frames[f] = pose.array()
        report[end] = {"maior_desvio_cm": round(float(np.linalg.norm(push, axis=1).max()) * 100, 1), "quadros": int(len(moved))}
    return frames, report


def pull(skeleton: Skeleton, frames: np.ndarray, joints: list[str], goal: np.ndarray, start: float = 0.5) -> tuple[np.ndarray, dict]:
    """Leva mãos ou pés, aos poucos, ao lugar e à orientação que têm na pose de destino.

    frames: (F, J, 7) locais; goal: (J, 7), a pose de destino já colocada no mundo. Da fração
    `start` do trecho em diante cada junta de `joints` é puxada para o ponto do destino, com
    peso crescente, e chega nele no último quadro; o membro é refeito por IK de dois ossos.
    É o pino de IK do runtime do MotionBricks: com a geração cortada antes do fim (transição
    antecipada) o pé ainda não chegou em cima do bloco, e o trecho seguinte, que o fixa, o
    congelaria no lugar errado. Devolve os quadros e, por junta, quanto faltou no último quadro.
    """
    frames = np.asarray(frames, dtype=float).copy()
    target = Pose(skeleton)
    target.pos, target.rot = goal[:, :3].copy(), quat_to_matrix(goal[:, 3:])
    goal_rot, goal_pos = skeleton.fk(target.pos, target.rot)
    count = len(frames)
    report = {}
    for name in joints:
        j = skeleton.joint(name)
        short = 0.0
        for f in range(1, count):
            u = (f / max(count - 1, 1) - start) / max(1.0 - start, 1e-6)
            if u <= 0.0:
                continue
            w = min(1.0, u)
            w = w * w * (3.0 - 2.0 * w)
            pose = Pose(skeleton)
            pose.pos, pose.rot = frames[f, :, :3].copy(), quat_to_matrix(frames[f, :, 3:])
            world_rot, world_pos = skeleton.fk(pose.pos, pose.rot)
            now_rot = world_rot[j].copy()
            short = pose.reach(name, world_pos[j] + w * (goal_pos[j] - world_pos[j]),
                               bend=stable_bend(skeleton, world_rot, world_pos, name))
            # orientação: mistura a do quadro com a do destino (pelos quatérnios, com o mesmo sinal)
            qa, qb = matrix_to_quat(now_rot), matrix_to_quat(goal_rot[j])
            if float(np.dot(qa, qb)) < 0.0:
                qb = -qb
            q = qa + w * (qb - qa)
            world_rot, _ = skeleton.fk(pose.pos, pose.rot)
            pose.rot[j] = world_rot[skeleton.parents[j]].T @ quat_to_matrix((q / np.linalg.norm(q))[None])[0]
            frames[f] = pose.array()
        report[name] = {"faltou_cm": round(short * 100, 1)}
    return frames, report


def pin(skeleton: Skeleton, frames: np.ndarray, joints: list[str], level=()) -> tuple[np.ndarray, dict]:
    """Segura mãos ou pés parados no mundo ao longo de um trecho de animação.

    frames: (F, J, 7) locais. Cada junta de `joints` fica, em todos os quadros, na posição e
    na orientação que tinha no primeiro: o membro é refeito por IK de dois ossos em cada quadro.
    É o que mantém o pé de apoio em cima de um bloco enquanto o corpo sobe: o modelo não sabe
    que o pé está apoiado e, sem isso, costuma baixá-lo para o chão.
    As juntas de `level` ficam livres para se mover, mas guardam a orientação do primeiro
    quadro: é o pé que sobe e desce sem apontar a ponta para baixo, para não cortar a quina.
    Devolve os quadros corrigidos e, por junta, quanto faltou no pior quadro (o quadril pode
    ter ido longe demais para a perna alcançar) e quanto a junta se mexia antes da correção.
    """
    frames = np.asarray(frames, dtype=float).copy()
    first = Pose(skeleton)
    first.pos, first.rot = frames[0, :, :3].copy(), quat_to_matrix(frames[0, :, 3:])
    anchor_rot, anchor_pos = skeleton.fk(first.pos, first.rot)
    report = {}
    for name in joints:
        j = skeleton.joint(name)
        worst, moved = 0.0, 0.0
        for f in range(1, len(frames)):
            pose = Pose(skeleton)
            pose.pos, pose.rot = frames[f, :, :3].copy(), quat_to_matrix(frames[f, :, 3:])
            moved = max(moved, float(np.linalg.norm(pose.world()[j] - anchor_pos[j])))
            worst = max(worst, pose.reach(name, anchor_pos[j]))
            world_rot, _ = skeleton.fk(pose.pos, pose.rot)
            pose.rot[j] = world_rot[skeleton.parents[j]].T @ anchor_rot[j]
            frames[f] = pose.array()
        report[name] = {"faltou_cm": round(worst * 100, 1), "mexia_antes_cm": round(moved * 100, 1)}
    for name in level:
        j = skeleton.joint(name)
        for f in range(1, len(frames)):
            rot = quat_to_matrix(frames[f, :, 3:])
            world_rot, _ = skeleton.fk(frames[f, :, :3], rot)
            frames[f, j, 3:] = matrix_to_quat(world_rot[skeleton.parents[j]].T @ anchor_rot[j])
    return frames, report


def build_poses(skeleton: Skeleton, specs: dict) -> dict[str, Pose]:
    """Monta as poses de um plano. Uma pose pode usar como base outra definida antes."""
    built: dict[str, Pose] = {"repouso": Pose(skeleton)}
    for name, spec in specs.items():
        if name == "repouso":
            raise ValueError("\"repouso\" é o nome da pose T do esqueleto; escolha outro")
        unknown = set(spec) - {"base", "lugar", "mirar", "alcancar", "pe_plano", "pes_no_chao", "altura", "posicoes"}
        if unknown:
            raise ValueError(f"pose {name}: campos desconhecidos {sorted(unknown)}")
        base = spec.get("base", "repouso")
        if base not in built:
            raise ValueError(f"pose {name}: a base \"{base}\" precisa ser definida antes")
        pose = Pose(skeleton, built[base])
        if spec.get("posicoes"):
            pose.fit_positions(spec["posicoes"])
        if "lugar" in spec:
            if len(spec["lugar"]) != 2:
                raise ValueError(f"pose {name}: lugar é [x, z]")
            pose.pos[0, 0], pose.pos[0, 2] = float(spec["lugar"][0]), float(spec["lugar"][1])
        for item in spec.get("mirar", []):
            if len(item) != 3:
                raise ValueError(f"pose {name}: cada item de mirar é [junta, filho, [x, y, z]]")
            pose.aim(item[0], item[1], item[2])
        # A altura entra antes de alcançar: o ponto pedido é no mundo, com o quadril já no lugar.
        if spec.get("pes_no_chao"):
            pose.feet_on_ground()
        pose.pos[0, 1] += float(spec.get("altura", 0.0))
        for item in spec.get("alcancar", []):
            if len(item) not in (2, 3):
                raise ValueError(f"pose {name}: cada item de alcancar é [ponta, [x, y, z]] ou com a dobra no fim")
            pose.reach(item[0], item[1], item[2] if len(item) == 3 else None)
        for joint in spec.get("pe_plano", []):
            pose.keep_rest_orientation(joint)
        built[name] = pose
    return built
