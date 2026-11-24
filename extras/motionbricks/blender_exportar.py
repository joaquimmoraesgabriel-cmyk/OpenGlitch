"""Leva as poses e os obstáculos de uma cena do Blender para um plano do gerar.py.

Roda DENTRO do Blender (testado no 5.3):

    blender -b cena.blend -P blender_exportar.py -- --saida plano.json

ou, com o Blender aberto, pelo MCP.

É a volta do caminho de blender_cena.py: depois de ajustar as poses contra os obstáculos
(girando ossos, com IK, do jeito que for), cada quadro com pose vira uma pose do plano.

O que sai:
  - "poses": uma por quadro, com "posicoes" = a posição no mundo de cada junta. Não se exporta
    rotação: os eixos dos ossos do Blender não são os do MotionBricks, e a posição das juntas
    diz a mesma coisa sem depender deles. O gerar.py remonta as rotações (poses.fit_positions).
  - "obstaculos": uma caixa por objeto da coleção "Obstaculos" (posição, tamanho e giro em
    volta do eixo vertical). Objeto inclinado nos outros eixos é recusado.
  - "inicio" e "destinos": os quadros na ordem, o primeiro como início.

Os nomes das poses vêm dos marcadores da linha do tempo, quando existem no quadro; senão,
"pose_<quadro>". Com --plano-base, os campos que este script não escreve (por exemplo
"folga_obstaculo") são mantidos do plano original.

Espaços: no Blender, Z é para cima e o personagem olha para -Y. No plano, (x, y, z) do Blender
vira (x, z, -y): +Y para cima, +Z para a frente, +X para a esquerda do personagem. Metros.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy

COLLECTION = "Obstaculos"


def to_plan(v) -> list[float]:
    return [round(float(v[0]), 4), round(float(v[2]), 4), round(-float(v[1]), 4)]


def find_armature(name: str | None):
    if name:
        return bpy.data.objects[name]
    armatures = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    if len(armatures) != 1:
        raise SystemExit(f"há {len(armatures)} esqueletos na cena: diga qual com --esqueleto")
    return armatures[0]


def export_obstacles() -> list[dict]:
    collection = bpy.data.collections.get(COLLECTION)
    out = []
    for obj in (collection.objects if collection else []):
        tilt = obj.rotation_euler
        if abs(tilt.x) > 1e-3 or abs(tilt.y) > 1e-3:
            raise SystemExit(f"obstáculo {obj.name}: só giro em volta do eixo vertical é aceito")
        size = [obj.dimensions.x, obj.dimensions.z, obj.dimensions.y]      # largura, altura, fundo
        spec = {"nome": obj.name, "centro": to_plan(obj.matrix_world.translation),
                "tamanho": [round(float(v), 4) for v in size]}
        if abs(tilt.z) > 1e-4:
            spec["giro"] = round(math.degrees(tilt.z), 2)
        out.append(spec)
    return out


def main() -> None:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Exporta poses e obstáculos do Blender para um plano.")
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--esqueleto", help="nome do objeto, se houver mais de um")
    parser.add_argument("--quadros", default="todos", help="\"todos\" ou uma lista 1,2,5")
    parser.add_argument("--plano-base", type=Path, help="plano de onde manter os demais campos")
    args = parser.parse_args(argv)

    armature = find_armature(args.esqueleto)
    scene = bpy.context.scene
    frames = (list(range(scene.frame_start, scene.frame_end + 1)) if args.quadros == "todos"
              else [int(v) for v in args.quadros.split(",")])
    markers = {m.frame: m.name for m in scene.timeline_markers}
    plan = json.loads(args.plano_base.read_text(encoding="utf-8")) if args.plano_base else {}
    old_names = [plan["inicio"].get("nome", "inicio")] + [d.get("nome") for d in plan.get("destinos", [])] \
        if plan.get("inicio") else []

    poses, order = {}, []
    for number, frame in enumerate(frames):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        label = markers.get(frame) or (old_names[number] if number < len(old_names) and old_names[number] else f"pose_{frame}")
        poses[label] = {"posicoes": {bone.name: to_plan(armature.matrix_world @ bone.head)
                                     for bone in armature.pose.bones}}
        order.append(label)
    if len(set(order)) != len(order):
        raise SystemExit("há poses com o mesmo nome: confira os marcadores")

    plan["poses"] = poses
    plan["inicio"] = {"pose": order[0]}
    plan["destinos"] = [{"nome": label, "pose": label} for label in order[1:]]
    plan["obstaculos"] = export_obstacles()
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("PLANO " + json.dumps({"arquivo": str(args.saida), "poses": order,
                                 "obstaculos": [o["nome"] for o in plan["obstaculos"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
