"""Monta no Blender a cena de conferência: obstáculos, chão e o esqueleto com as poses ou a animação.

Roda DENTRO do Blender (testado no 5.3), sem janela:

    blender -b -P blender_cena.py -- --plano plano.json --bvh subir.poses.bvh --saida pasta --nome subir

ou, com o Blender aberto, pelo MCP: execute o arquivo com `sys.argv` montado do mesmo jeito.

O que faz:
  - importa o BVH (as poses-chave de `gerar.py --so-poses`, um quadro por pose, ou a animação
    gerada), em metros, com o eixo do personagem convertido para o do Blender;
  - cria uma caixa por obstáculo do plano, na coleção "Obstaculos", e o chão;
  - renderiza cada quadro pedido de lado e de três quartos, com o obstáculo, em
    <saida>/<nome>_q<quadro>_<vista>.png, e uma folha com todos;
  - salva <saida>/<nome>.blend, para abrir, olhar e ajustar as poses à mão.

Depois de ajustar as poses no Blender, `blender_exportar.py` leva tudo de volta para um plano.

Espaços: o plano usa o do MotionBricks (+Y para cima, +Z para a frente do personagem, +X para a
esquerda dele). No Blender, Z é para cima: (x, y, z) do plano vira (x, -z, y).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

COLLECTION = "Obstaculos"


def to_blender(p) -> Vector:
    return Vector((float(p[0]), -float(p[2]), float(p[1])))


def clear_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def add_obstacles(specs: list[dict]) -> list:
    collection = bpy.data.collections.new(COLLECTION)
    bpy.context.scene.collection.children.link(collection)
    material = bpy.data.materials.new("Obstaculo")
    material.diffuse_color = (0.25, 0.7, 0.35, 1.0)
    objects = []
    for spec in specs:
        mesh = bpy.data.meshes.new(spec.get("nome", "obstaculo"))
        size = spec["tamanho"]
        hx, hy, hz = size[0] / 2, size[2] / 2, size[1] / 2          # largura, fundo, altura
        verts = [(x, y, z) for x in (-hx, hx) for y in (-hy, hy) for z in (-hz, hz)]
        faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        mesh.from_pydata(verts, [], faces)
        mesh.materials.append(material)
        obj = bpy.data.objects.new(spec.get("nome", "obstaculo"), mesh)
        obj.location = to_blender(spec["centro"])
        obj.rotation_euler = (0.0, 0.0, math.radians(float(spec.get("giro", 0.0))))
        collection.objects.link(obj)
        objects.append(obj)
    return objects


def add_ground(size: float = 12.0):
    mesh = bpy.data.meshes.new("Chao")
    mesh.from_pydata([(-size, -size, 0), (size, -size, 0), (size, size, 0), (-size, size, 0)], [], [(0, 1, 2, 3)])
    material = bpy.data.materials.new("Chao")
    material.diffuse_color = (0.78, 0.78, 0.78, 1.0)
    mesh.materials.append(material)
    obj = bpy.data.objects.new("Chao", mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def import_bvh(path: Path):
    before = set(bpy.data.objects)
    bpy.ops.import_anim.bvh(filepath=str(path), global_scale=0.01, axis_forward="-Z", axis_up="Y",
                            frame_start=1, use_fps_scale=False, update_scene_fps=False,
                            update_scene_duration=True, rotate_mode="NATIVE")
    armature = next(o for o in bpy.data.objects if o not in before and o.type == "ARMATURE")
    armature.name = "Esqueleto"
    # A cena nova vem com 250 quadros: fica com os do BVH.
    start, end = armature.animation_data.action.frame_range
    bpy.context.scene.frame_start, bpy.context.scene.frame_end = int(round(start)), int(round(end))
    armature.show_in_front = True
    return armature


def add_body(armature, radius: float = 0.035):
    """Um boneco de palitos grossos preso aos ossos: é o que aparece na renderização."""
    material = bpy.data.materials.new("Corpo")
    material.diffuse_color = (0.85, 0.25, 0.2, 1.0)
    hidden = ("Thumb", "Index", "Middle", "Ring", "Pinky", "Eye", "Jaw")
    for bone in armature.data.bones:
        if any(h in bone.name for h in hidden) or bone.length < 0.02:
            continue
        thick = radius * (1.6 if bone.name in ("Hips", "Spine1", "Spine2", "Chest") else 1.0)
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=thick, depth=bone.length)
        obj = bpy.context.active_object
        obj.name = "corpo_" + bone.name
        obj.data.materials.append(material)
        obj.parent, obj.parent_type, obj.parent_bone = armature, "BONE", bone.name
        # Filho de osso fica na ponta dele, com Y ao longo do osso: recua meio comprimento e deita.
        obj.location = (0.0, -bone.length / 2, 0.0)
        obj.rotation_euler = (math.radians(90), 0.0, 0.0)
    head = armature.data.bones.get("Head")
    if head:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.1)
        obj = bpy.context.active_object
        obj.name = "corpo_cabeca"
        obj.data.materials.append(material)
        obj.parent, obj.parent_type, obj.parent_bone = armature, "BONE", "Head"
        obj.location = (0.0, -head.length + 0.09, 0.0)


def joint_positions(armature, frame: int) -> dict:
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()
    return {b.name: armature.matrix_world @ b.head for b in armature.pose.bones}


def render_views(armature, frames: list[int], out_dir: Path, name: str, resolution=(640, 480)) -> list[str]:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.image_settings.file_format = "PNG"
    camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    camera.data.lens = 35
    scene.collection.objects.link(camera)
    scene.camera = camera
    written = []
    # No Blender o personagem olha para -Y. "lado": câmera em +X; "quina": de frente e de lado.
    views = {"lado": Vector((5.0, 0.0, 0.3)), "quina": Vector((3.6, -3.6, 1.6))}
    for frame in frames:
        hips = joint_positions(armature, frame).get("Hips", Vector((0, 0, 1)))
        focus = Vector((hips.x, hips.y, max(0.9, hips.z * 0.75)))
        for view, offset in views.items():
            camera.location = focus + offset
            camera.rotation_euler = (focus - camera.location).to_track_quat("-Z", "Y").to_euler()
            path = out_dir / f"{name}_q{frame:03d}_{view}.png"
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            written.append(str(path))
    return written


def sheet(images: list[str], path: Path, columns: int, width: int = 320) -> None:
    """Junta as imagens numa folha: uma linha por vista, uma coluna por quadro."""
    views = len(images) // columns
    first = bpy.data.images.load(images[0])
    w, h = first.size
    height = int(width * h / w)
    import numpy as np
    canvas = np.ones((views * height, columns * width, 4), dtype=np.float32)
    for i, image_path in enumerate(images):
        image = bpy.data.images.load(image_path)
        image.scale(width, height)
        pixels = np.empty(width * height * 4, dtype=np.float32)
        image.pixels.foreach_get(pixels)
        column, row = i // views, i % views
        canvas[(views - 1 - row) * height:(views - row) * height, column * width:(column + 1) * width] = pixels.reshape(height, width, 4)
        bpy.data.images.remove(image)
    out = bpy.data.images.new("folha", columns * width, views * height)
    out.pixels.foreach_set(canvas.ravel())
    out.filepath_raw, out.file_format = str(path), "PNG"
    out.save()
    bpy.data.images.remove(out)


def main() -> None:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Monta a cena de conferência no Blender.")
    parser.add_argument("--plano", type=Path, required=True, help="plano com \"obstaculos\"")
    parser.add_argument("--bvh", type=Path, required=True, help="poses-chave ou animação gerada")
    parser.add_argument("--saida", type=Path, required=True)
    parser.add_argument("--nome", default="cena")
    parser.add_argument("--quadros", default="todos",
                        help="\"todos\", ou uma lista 1,5,9, ou \"cada:N\" para um a cada N quadros")
    parser.add_argument("--sem-render", action="store_true")
    args = parser.parse_args(argv)
    args.saida.mkdir(parents=True, exist_ok=True)

    plan = json.loads(args.plano.read_text(encoding="utf-8"))
    clear_scene()
    add_ground()
    add_obstacles(plan.get("obstaculos", []))
    armature = import_bvh(args.bvh)
    add_body(armature)
    scene = bpy.context.scene
    first, last = scene.frame_start, scene.frame_end
    if args.quadros == "todos":
        frames = list(range(first, last + 1))
    elif args.quadros.startswith("cada:"):
        frames = list(range(first, last + 1, int(args.quadros[5:])))
    else:
        frames = [int(v) for v in args.quadros.split(",")]
    images = [] if args.sem_render else render_views(armature, frames, args.saida, args.nome)
    blend = args.saida / f"{args.nome}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    if images:
        sheet(images, args.saida / f"{args.nome}_folha.png", columns=len(frames))
    print("CENA " + json.dumps({"blend": str(blend), "quadros": [first, last], "imagens": len(images),
                                "obstaculos": [o.name for o in bpy.data.collections[COLLECTION].objects]}))


if __name__ == "__main__":
    main()
