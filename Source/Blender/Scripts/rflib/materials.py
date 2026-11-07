"""Simple grey PBR (metal/roughness) materials for greybox. Unreal creates one material slot per
material on FBX import; final assets will bring their own M_/MI_ materials."""
import bpy

# key -> (material name, grey value (linear), roughness, metallic)
GREYBOX_PALETTE = {
    "Concrete": ("M_Greybox_Concrete", 0.50, 0.90, 0.0),   # ruin kit
    "Wood":     ("M_Greybox_Wood",     0.30, 0.80, 0.0),   # logs, planks, stakes
    "Metal":    ("M_Greybox_Metal",    0.55, 0.45, 1.0),   # plates, gate, cans
    "Soil":     ("M_Greybox_Soil",     0.18, 1.00, 0.0),   # dug pits and trenches
    "Rope":     ("M_Greybox_Rope",     0.80, 0.90, 0.0),   # wire, string, rope
    "Ref":      ("M_Greybox_Ref",      0.85, 0.70, 0.0),   # 180 cm reference figure
    "RefFront": ("M_Greybox_RefFront", 0.04, 0.70, 0.0),   # front markers (face/chest/toes)
}


def grey_material(name, value, roughness=0.8, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs["Base Color"].default_value = (value, value, value, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    mat.diffuse_color = (value, value, value, 1.0)   # viewport / FBX fallback colour
    mat.roughness = roughness
    mat.metallic = metallic
    return mat


def greybox_palette():
    """Return {key: bpy material} for every greybox material."""
    return {k: grey_material(n, v, r, m) for k, (n, v, r, m) in GREYBOX_PALETTE.items()}
