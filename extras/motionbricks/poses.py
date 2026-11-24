"""Monta poses de um esqueleto por código, sem clipe nenhum. Só depende de numpy.

Uma pose é descrita por direções no espaço do personagem, e não por ângulos de
junta, que dependem dos eixos locais de cada osso e são fáceis de errar:

    {"mirar": [["LeftArm", "LeftForeArm", [0.2, -1, 0]]], "pes_no_chao": true}

quer dizer "gire o braço esquerdo até o osso que vai de LeftArm a LeftForeArm
apontar para baixo e um pouco para fora". Espaço do modelo SOMA: +Y para cima,
+Z para a frente do personagem, +X para o lado esquerdo dele. Metros.

Campos de uma pose:
  base         nome de outra pose já definida, ou "repouso" (padrão), a pose T
  mirar        lista de [junta, filho, [x, y, z]], aplicada na ordem dada;
               mire do tronco para as pontas (quadril, coxa, canela, braço, antebraço)
  pe_plano     lista de juntas que voltam à orientação de repouso no mundo,
               depois de mirar; use nos pés para a sola ficar no chão
  pes_no_chao  sobe ou desce o quadril até o pé mais baixo encostar no chão
  altura       soma este valor, em metros, à altura do quadril (um salto, por exemplo)
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


def build_poses(skeleton: Skeleton, specs: dict) -> dict[str, Pose]:
    """Monta as poses de um plano. Uma pose pode usar como base outra definida antes."""
    built: dict[str, Pose] = {"repouso": Pose(skeleton)}
    for name, spec in specs.items():
        if name == "repouso":
            raise ValueError("\"repouso\" é o nome da pose T do esqueleto; escolha outro")
        unknown = set(spec) - {"base", "mirar", "pe_plano", "pes_no_chao", "altura"}
        if unknown:
            raise ValueError(f"pose {name}: campos desconhecidos {sorted(unknown)}")
        base = spec.get("base", "repouso")
        if base not in built:
            raise ValueError(f"pose {name}: a base \"{base}\" precisa ser definida antes")
        pose = Pose(skeleton, built[base])
        for item in spec.get("mirar", []):
            if len(item) != 3:
                raise ValueError(f"pose {name}: cada item de mirar é [junta, filho, [x, y, z]]")
            pose.aim(item[0], item[1], item[2])
        for joint in spec.get("pe_plano", []):
            pose.keep_rest_orientation(joint)
        if spec.get("pes_no_chao"):
            pose.feet_on_ground()
        pose.pos[0, 1] += float(spec.get("altura", 0.0))
        built[name] = pose
    return built
