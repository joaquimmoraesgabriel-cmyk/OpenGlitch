"""Roda a cena de exemplo do MotionBricks (a "academia") sozinha e grava o que aconteceu.

Serve para ver o teto de qualidade do modelo com poses bem feitas, antes de montar
obstáculos próprios: o personagem anda por pontos de passagem, entra nos Smart
Primitives da cena (pulo, salto por cima, barra) e este script grava capturas da
janela e a pose de cada quadro.

Roda DENTRO do ambiente do MotionBricks e abre uma janela (precisa de monitor):

    uv run --project <pasta do motionbricks> python teste_cena.py --saida pasta

Os Smart Primitives e clipes da cena de exemplo têm licença só de avaliação: o que
sai daqui é para avaliar o modelo, não para um jogo.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np


def _argumentos(parser):
    parser.add_argument("--repo", type=Path, required=True, help="pasta do repositório do MotionBricks")
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--correr", action="store_true", help="usa a velocidade máxima do modo")
    parser.add_argument("--pontos", type=str, default="-3,0;10,0;10,4;-3,4;-3,8;10,8;10,12;-3,12;-3,16;10,16",
                        help="pontos de passagem x,y no chão da cena (Z para cima), separados por ;")
    parser.add_argument("--quadros", type=int, default=6000)
    parser.add_argument("--captura-a-cada", type=int, default=6)
    return parser


def main() -> None:
    args_previos, _ = _argumentos(argparse.ArgumentParser(add_help=False)).parse_known_args()
    sys.path.insert(0, str(args_previos.repo))
    import os
    os.chdir(args_previos.repo)

    import newton.examples
    import warp as wp
    from PIL import Image

    import app.scene_preview as sp
    from app.utils.cli import create_gl_parser
    from app.utils.input import InputFrame

    # O Newton lê a linha de comando com o analisador dele; os argumentos daqui entram no mesmo.
    viewer, args = newton.examples.init(_argumentos(create_gl_parser()))
    args.repo, args.saida = args.repo.resolve(), args.saida.resolve()
    args.saida.mkdir(parents=True, exist_ok=True)
    preview = sp.ScenePreview(viewer, args.repo / "assets/scenes/soma_gym.scene.json")
    waypoints = [np.array([float(v) for v in p.split(",")], dtype=np.float32) for p in args.pontos.split(";")]
    state = {"i": 0, "move": np.zeros(3, dtype=np.float32)}

    class Entrada:
        def poll(self):
            return InputFrame(movement=(0.0, 1.0), camera_orbit=(0.0, 0.0), use_max_speed=args.correr)

        def close(self):
            pass

        def __getattr__(self, name):          # botões e modos: nada apertado
            return lambda *a, **k: False

    preview._input.close()
    preview._input = Entrada()
    sp.camera_relative_movement = lambda facing, movement: state["move"].copy()
    preview._requested_locomotion_mode = lambda: None
    preview._interaction_pressed = lambda: False

    log, poses = [], []
    frame = 0
    while viewer.is_running() and frame < args.quadros and state["i"] < len(waypoints):
        session = preview._scene_session
        character = session.character
        ground = np.asarray(character.character_ground_position, dtype=np.float32)
        delta = waypoints[state["i"]] - ground[:2]
        if np.linalg.norm(delta) < 0.6:
            state["i"] += 1
            continue
        direction = delta / np.linalg.norm(delta)
        state["move"] = np.array([direction[0], direction[1], 0.0], dtype=np.float32)
        preview.camera_facing = state["move"].copy()
        with wp.ScopedStream(character.engine.stream):
            preview.step()
            preview.render()
            pose = character.current_pose.numpy().copy()
            if frame % args.captura_a_cada == 0:
                pixels = viewer.get_frame().numpy()
                Image.fromarray(pixels[..., :3]).save(args.saida / f"q{frame:05d}.jpg", quality=80)
        machine = session.state_machine
        log.append({"quadro": frame, "t": round(float(preview.time), 3), "chao": [round(float(v), 3) for v in ground],
                    "ponto": state["i"], "interagindo": bool(machine.is_interacting),
                    "primitivo": getattr(preview._active_interaction, "name", None) if machine.is_interacting else None})
        poses.append(pose)
        frame += 1

    np.save(args.saida / "poses.npy", np.stack(poses))
    (args.saida / "registro.json").write_text(json.dumps(log), encoding="utf-8")
    print("QUADROS", frame, "PONTOS", state["i"], "POSE", poses[0].shape, poses[0].dtype)
    preview.close()
    viewer.close()


if __name__ == "__main__":
    main()
