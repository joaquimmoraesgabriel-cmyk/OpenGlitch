"""Converte um BVH em FBX com o Blender em segundo plano.

    blender -b --factory-startup --python bvh_para_fbx.py -- entrada.bvh saida.fbx

O FBX sai com a armadura e a animação, pronto para a Unity importar como
Humanoid (o esqueleto SOMA usa nomes no padrão Hips, Spine, LeftArm...). A
troca para o esqueleto do seu personagem é feita pelo retargeting Humanoid da
Unity, não aqui.

Imprime um JSON com o que foi gravado e com a posição de algumas juntas, para
conferir que a conversão não deitou nem escalou o esqueleto.
"""

import json
import os
import sys

import bpy


def main() -> None:
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 2:
        raise SystemExit("uso: blender -b --factory-startup --python bvh_para_fbx.py -- entrada.bvh saida.fbx")
    source, target = args

    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.preferences.addon_enable(module="io_anim_bvh")
    except Exception:
        pass  # em versões em que o importador já vem ligado
    # O BVH está em centímetros e Y para cima; a cena do Blender é em metros e Z para cima.
    bpy.ops.import_anim.bvh(filepath=source, global_scale=0.01, axis_forward="-Z", axis_up="Y",
                            rotate_mode="NATIVE", use_fps_scale=False, update_scene_fps=True,
                            update_scene_duration=True)
    armature = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    armature.name = "SOMA"
    scene = bpy.context.scene
    # A duração da cena nem sempre acompanha o clipe importado: use a da própria animação.
    # O nome da ação vira o nome do clipe na engine; sem isso ele chega como "Scene".
    clip_name = os.path.splitext(os.path.basename(target))[0]
    armature.animation_data.action.name = clip_name
    scene.name = clip_name
    start, end = armature.animation_data.action.frame_range
    scene.frame_start, scene.frame_end = int(round(start)), int(round(end))

    def world(bone: str, frame: int):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        head = armature.matrix_world @ armature.pose.bones[bone].head
        return [round(v, 4) for v in head]

    names = [b.name for b in armature.pose.bones]
    probe = [n for n in ("Hips", "Head", "LeftFoot", "RightHand") if n in names] or names[:1]
    first, last = scene.frame_start, scene.frame_end
    check = {n: {"primeiro": world(n, first), "ultimo": world(n, last)} for n in probe}

    bpy.ops.object.select_all(action="DESELECT")
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    bpy.ops.export_scene.fbx(
        filepath=target, use_selection=True, object_types={"ARMATURE"}, add_leaf_bones=False,
        bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=False, bake_anim_simplify_factor=0.0,
        axis_forward="-Z", axis_up="Y", apply_scale_options="FBX_SCALE_UNITS",
    )
    print("OG_RESULTADO " + json.dumps({
        "fbx": target, "ossos": len(names), "quadros": last - first + 1,
        "fps": scene.render.fps, "posicoes_no_blender_m_z_para_cima": check,
    }, ensure_ascii=False))


main()
