"""FBX export preset from the brief (Agent 2: Scale, orientation and export).

Scene: Metric, Unit Scale 1.0, 1 Blender unit = 1 m = 100 Unreal units. Transforms applied
(the pipeline builds geometry in place, so every mesh has identity transforms).
One FBX per asset with only that asset's objects selected: render mesh + UCX_ hulls + SOCKET_ empties.

The keyword set below is passed verbatim to bpy.ops.export_scene.fbx; the report lists it too.
"""
import bpy

FBX_STATIC_MESH_PRESET = dict(
    use_selection=True,                 # only the asset's own objects
    use_visible=False,
    use_active_collection=False,
    global_scale=1.0,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_UNITS',
    use_space_transform=True,
    bake_space_transform=False,
    axis_forward='-Z',
    axis_up='Y',
    object_types={'MESH', 'EMPTY'},     # EMPTY carries the SOCKET_ empties
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',            # Smoothing: Face
    use_subsurf=False,
    use_mesh_edges=False,
    use_tspace=False,
    use_triangles=True,                 # triangulate on export (quads/ngons kept in the .blend)
    use_custom_props=False,
    colors_type='NONE',
    add_leaf_bones=False,               # Add Leaf Bones: off
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    use_armature_deform_only=True,
    armature_nodetype='NULL',
    bake_anim=False,                    # static meshes carry no animation
    path_mode='AUTO',
    embed_textures=False,
    batch_mode='OFF',
)


def export_fbx(filepath, objects, active=None, preset=None):
    preset = dict(preset or FBX_STATIC_MESH_PRESET)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objects:
        o.hide_set(False)
        o.select_set(True)
    bpy.context.view_layer.objects.active = active or objects[0]
    result = bpy.ops.export_scene.fbx(filepath=str(filepath), **preset)
    if 'FINISHED' not in result:
        raise RuntimeError(f"FBX export failed: {filepath} -> {result}")
    return filepath


def preset_as_text(preset=None):
    preset = preset or FBX_STATIC_MESH_PRESET
    lines = []
    for k, v in preset.items():
        if isinstance(v, set):
            v = "{" + ", ".join(repr(x) for x in sorted(v)) + "}"
        else:
            v = repr(v)
        lines.append(f"{k}={v}")
    return lines
