"""Overview preview of the greybox kit, rendered from the EXPORTED FBX files (not the build scene),
so the picture also checks the exports: scale, pivots, and sockets. Attachments are mounted on their
host's SOCKET_ exactly as the game would (plate, barricades, gate leaves, pit cover, deadfall weight),
and one small room is assembled on the grid.

Run:  ~/.venv-blender/bin/python Source/Blender/Scripts/Greybox_Overview.py [--out path.png] [--samples N]
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import bpy                                   # noqa: E402
from mathutils import Matrix, Vector         # noqa: E402

from rflib import geo, meshbuild, paths      # noqa: E402
from rflib import scene as rfscene           # noqa: E402

ROW_RUIN, ROW_BUILD, ROW_TRAP = 12.0, 4.0, -4.0


def _base(name):
    return name.split(".")[0]


def import_asset(name, loc=(0, 0, 0), rot_z=0.0, matrix=None):
    """Import Export/FBX/<name>.fbx and place its root objects. Returns {base name: object}."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=str(paths.EXPORT_FBX_DIR / f"{name}.fbx"))
    new = [o for o in bpy.data.objects if o not in before]
    m = matrix if matrix is not None else (Matrix.Translation(Vector(loc)) @ Matrix.Rotation(math.radians(rot_z), 4, 'Z'))
    for o in new:
        if o.parent is None:
            o.matrix_world = m @ o.matrix_world
        if o.name.startswith("UCX_"):
            o.hide_render = True
    bpy.context.view_layer.update()
    return {_base(o.name): o for o in new}


def attach(host, socket, name, extra_rot_z=0.0):
    sm = host[socket].matrix_world.copy()
    return import_asset(name, matrix=sm @ Matrix.Rotation(math.radians(extra_rot_z), 4, 'Z'))


def label(text, loc, size=0.42, mat=None, align='CENTER'):
    cu = bpy.data.curves.new(f"lbl_{text}", 'FONT')
    cu.body = text
    cu.size = size
    cu.align_x = align
    cu.align_y = 'TOP'
    ob = bpy.data.objects.new(f"lbl_{text}", cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (loc[0], loc[1], 0.005)
    if mat:
        cu.materials.append(mat)
    return ob


def ground_material():
    mat = bpy.data.materials.new("Preview_Ground")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    fx, fy = nt.nodes.new("ShaderNodeMath"), nt.nodes.new("ShaderNodeMath")
    fx.operation = fy.operation = 'FLOOR'
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = 'ADD'
    mod = nt.nodes.new("ShaderNodeMath")
    mod.operation = 'FLOORED_MODULO'
    mod.inputs[1].default_value = 2.0
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = 'RGBA'
    mix.inputs["A"].default_value = (0.30, 0.31, 0.30, 1)
    mix.inputs["B"].default_value = (0.25, 0.26, 0.25, 1)
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    nt.links.new(sep.outputs["X"], fx.inputs[0])
    nt.links.new(sep.outputs["Y"], fy.inputs[0])
    nt.links.new(fx.outputs[0], add.inputs[0])
    nt.links.new(fy.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], mod.inputs[0])
    nt.links.new(mod.outputs[0], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.95
    return mat


def build_ground(holes):
    """1 m checker ground (top at z=0) with holes where below-ground pieces sit."""
    col = bpy.context.scene.collection
    g = meshbuild.build_object("Preview_Ground", [geo.box((-14, -16, -0.02), (64, 32, 0), "g")],
                               {"g": ground_material()}, col)
    if holes:
        meshbuild.boolean_difference(g, [geo.box((a[0], a[1], -0.5), (b[0], b[1], 0.5)) for a, b in holes], col)
    return g


def render(out=None, samples=64, resolution=(2400, 1200)):
    out = Path(out) if out else paths.PREVIEWS_DIR / "Greybox_Overview.png"
    rfscene.reset_scene()
    sc = bpy.context.scene
    dark = bpy.data.materials.new("Preview_Label")
    dark.diffuse_color = (0.95, 0.95, 0.95, 1)
    dark.use_nodes = True
    dark.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1)

    def L(text, x, y):
        label(text, (x, y), mat=dark)

    def H(text, y):
        label(text, (-2.6, y + 1.2), size=0.55, mat=dark, align='RIGHT')

    # Row 1: ruin kit ------------------------------------------------------------------
    y = ROW_RUIN
    H("SM_Ruin_*", y)
    import_asset("SM_Ref_Human_180", (-1.5, y + 0.3, 0)); L("Ref_Human_180", -1.5, y - 0.5)
    for name, x, lx in [("SM_Ruin_Wall_400", 0, 2), ("SM_Ruin_Wall_200", 5.5, 6.5), ("SM_Ruin_Wall_100", 9.5, 10),
                        ("SM_Ruin_Wall_Corner", 12.2, 12.2), ("SM_Ruin_Wall_Window_400", 14, 16),
                        ("SM_Ruin_Wall_Door_400", 19, 21), ("SM_Ruin_Wall_Collapsed_400", 24, 26)]:
        import_asset(name, (x, y, 0)); L(name[8:], lx, y - (0.5 if name != "SM_Ruin_Wall_Corner" else 1.2))
    # floor tiles have their top at walking level (z=0); shown on a 20 cm lift so the slab is visible
    import_asset("SM_Ruin_Floor_400", (29, y, 0.2)); L("Floor_400 (lifted 20 cm)", 31, y - 0.5)
    import_asset("SM_Ruin_Roof_400", (34, y, 0)); L("Roof_400", 36, y - 0.5)
    import_asset("SM_Ruin_Stairs_300", (39, y, 0)); L("Stairs_300", 39.5, y - 0.5)
    import_asset("SM_Ruin_RubblePile_01", (42.5, y + 1.0, 0)); L("RubblePile_01", 42.5, y - 0.5)
    # assembled room on the grid: floor, 4 walls, 4 corners, all lifted 20 cm onto the floor slab
    rx, ry, rz = 46.0, y, 0.2
    import_asset("SM_Ruin_Floor_400", (rx, ry, rz))
    door = import_asset("SM_Ruin_Wall_Door_400", (rx, ry, rz))
    import_asset("SM_Ruin_Wall_400", (rx, ry + 4, rz))
    import_asset("SM_Ruin_Wall_Collapsed_400", (rx, ry, rz), 90)
    import_asset("SM_Ruin_Wall_Window_400", (rx + 4, ry, rz), 90)
    for cx, cy in ((0, 0), (4, 0), (0, 4), (4, 4)):
        import_asset("SM_Ruin_Wall_Corner", (rx + cx, ry + cy, rz))
    attach(door, "SOCKET_BarricadeBack", "SM_Build_BarricadeDoor_T1_Intact")
    import_asset("SM_Ref_Human_180", (rx + 2.0, ry - 0.6, 0))  # standing in the doorway
    L("Room on the 100 cm grid", rx + 2, y - 1.2)

    # Row 2: line buildables --------------------------------------------------------------
    y = ROW_BUILD
    H("SM_Build_* lines", y)
    import_asset("SM_Ref_Human_180", (-1.5, y + 0.3, 0)); L("Ref_Human_180", -1.5, y - 1.2)
    import_asset("SM_Build_Log_T1_Intact", (0, y, 0)); L("Build_Log", 2, y - 1.2)
    import_asset("SM_Build_LogWall_T1_Intact", (5, y, 0)); L("Build_LogWall", 7, y - 1.2)
    import_asset("SM_Build_SpikedWall_T1_Intact", (10, y, 0)); L("Build_SpikedWall", 12, y - 1.2)
    lw = import_asset("SM_Build_LogWall_T1_Intact", (15, y, 0))
    attach(lw, "SOCKET_PlateMount", "SM_Build_MetalPlate_T3_Intact")
    L("LogWall + MetalPlate_T3", 17, y - 1.2)
    import_asset("SM_Build_BarbedWire_T1_Intact", (20, y, 0)); L("Build_BarbedWire", 22, y - 1.2)
    gate = import_asset("SM_Build_WeldedGate_T1_Intact", (25, y, 0))
    attach(gate, "SOCKET_HingeLeft", "SM_Build_WeldedGate_Leaf_T1_Intact", extra_rot_z=-70)
    attach(gate, "SOCKET_HingeRight", "SM_Build_WeldedGate_Leaf_T1_Intact")
    L("WeldedGate + 2 Leaf", 27, y - 1.2)
    import_asset("SM_Build_FireRing_T1_Intact", (30, y, 0)); L("Build_FireRing", 32, y - 1.2)
    import_asset("SM_Build_Watchtower_T1_Intact", (37.5, y + 0.8, 0)); L("Build_Watchtower", 37.5, y - 1.2)

    # Row 3: placed pieces, traps, barricades -----------------------------------------------
    y = ROW_TRAP
    H("SM_Build_* placed", y)
    import_asset("SM_Ref_Human_180", (-1.5, y + 0.3, 0)); L("Ref_Human_180", -1.5, y - 1.4)
    import_asset("SM_Build_SpikePit_T1_Intact", (1.5, y, 0)); L("Build_SpikePit", 1.5, y - 1.4)
    pit = import_asset("SM_Build_SpikePit_T1_Intact", (5.0, y, 0))
    attach(pit, "SOCKET_Cover", "SM_Build_SpikePit_Cover_T1_Intact"); L("SpikePit + Cover", 5.0, y - 1.4)
    import_asset("SM_Build_NoiseTrap_T1_Intact", (9.5, y, 0)); L("Build_NoiseTrap", 9.5, y - 1.4)
    df = import_asset("SM_Build_Deadfall_T1_Intact", (13.5, y, 0))
    attach(df, "SOCKET_WeightArmed", "SM_Build_Deadfall_Weight_T1_Intact"); L("Deadfall + Weight", 13.5, y - 1.4)
    import_asset("SM_Build_Snare_T1_Intact", (16.5, y, 0)); L("Build_Snare", 16.7, y - 1.4)
    dw = import_asset("SM_Ruin_Wall_Door_400", (18.5, y, 0))
    attach(dw, "SOCKET_BarricadeFront", "SM_Build_BarricadeDoor_T1_Intact"); L("Door + BarricadeDoor", 20.5, y - 1.4)
    ww = import_asset("SM_Ruin_Wall_Window_400", (23.5, y, 0))
    attach(ww, "SOCKET_BarricadeFront", "SM_Build_BarricadeWindow_T1_Intact"); L("Window + BarricadeWindow", 25.5, y - 1.4)
    import_asset("SM_Build_MetalPlate_T3_Intact", (30.5, y, 0)); L("Build_MetalPlate_T3", 30.5, y - 1.4)
    import_asset("SM_Build_WeldedGate_Leaf_T1_Intact", (33.5, y, 0)); L("WeldedGate_Leaf", 34.4, y - 1.4)
    import_asset("SM_Build_Deadfall_Weight_T1_Intact", (38.0, y, 0)); L("Deadfall_Weight", 38.0, y - 1.4)
    import_asset("SM_Build_SpikePit_Cover_T1_Intact", (41.5, y, 0)); L("SpikePit_Cover", 41.5, y - 1.4)

    build_ground([((0.4, ROW_TRAP - 1.1), (2.6, ROW_TRAP + 1.1)), ((3.9, ROW_TRAP - 1.1), (6.1, ROW_TRAP + 1.1)),
                  ((30.0, ROW_BUILD - 0.6), (34.0, ROW_BUILD + 0.6))])

    # light, camera, render
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", 'SUN'))
    sun.data.energy = 4.0
    sun.data.angle = math.radians(4)
    sun.rotation_euler = (math.radians(48), math.radians(-18), math.radians(-35))
    sc.collection.objects.link(sun)
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.6, 0.66, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.8
    sc.world = world
    cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 60.0
    target = Vector((21.4, 5.2, 1.0))
    el, az = math.radians(52), 0.0
    cam.location = target + 90.0 * Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    cam.data.clip_end = 300
    cam.rotation_euler = (target - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.collection.objects.link(cam)
    sc.camera = cam
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = resolution
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = str(out)
    bpy.ops.render.render(write_still=True)
    print(f"preview written: {out}")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--res", type=int, nargs=2, default=(2400, 1200))
    a = ap.parse_args()
    render(a.out, a.samples, tuple(a.res))
