"""Turn Part lists into Blender mesh objects; exact booleans; box-projected UVs."""
import bmesh
import bpy


def build_object(name, parts, materials, collection, require_material=True):
    """One mesh object from many Parts. `materials` maps Part.mat keys to bpy materials."""
    verts, faces, face_mat_keys = [], [], []
    for p in parts:
        off = len(verts)
        verts.extend(p.verts)
        for f in p.faces:
            faces.append([i + off for i in f])
            face_mat_keys.append(p.mat)
    slots = []
    for k in face_mat_keys:
        if k not in slots:
            slots.append(k)
    if require_material and None in slots:
        raise ValueError(f"{name}: a part has no material")
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], faces)
    me.validate(clean_customdata=False)
    me.update()
    for k in slots:
        if k is not None:
            me.materials.append(materials[k])
    if slots and slots != [None]:
        for poly, k in zip(me.polygons, face_mat_keys):
            poly.material_index = slots.index(k)
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def recalc_normals(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


def boolean_difference(ob, cutter_parts, collection):
    """Subtract closed cutter shells from `ob` with the Exact solver and bake the result."""
    cutters = []
    # Cutters carry the host's first material: the Exact solver copies operand material slots onto
    # the result, and an empty slot would leave the cut faces without a material.
    host_mat = ob.data.materials[0] if ob.data.materials else None
    for i, cp in enumerate(cutter_parts):
        c = build_object(f"_cutter_{i}", [cp], {}, collection, require_material=False)
        if host_mat is not None:
            c.data.materials.append(host_mat)
        c.display_type = 'WIRE'
        c.hide_render = True
        mod = ob.modifiers.new(f"cut_{i}", 'BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.solver = 'EXACT'
        mod.object = c
        cutters.append(c)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = ob.evaluated_get(depsgraph)
    new_me = bpy.data.meshes.new_from_object(evaluated)
    old_me = ob.data
    ob.modifiers.clear()
    ob.data = new_me
    bpy.data.meshes.remove(old_me)
    new_me.name = ob.name
    for c in cutters:
        me = c.data
        bpy.data.objects.remove(c)
        bpy.data.meshes.remove(me)
    # Merge coplanar fragments the solver leaves behind, keeping material borders.
    bm = bmesh.new()
    bm.from_mesh(new_me)
    bmesh.ops.dissolve_limit(bm, angle_limit=1e-4, verts=list(bm.verts), edges=list(bm.edges),
                             delimit={'MATERIAL'})
    bm.to_mesh(new_me)
    bm.free()
    new_me.update()


def box_uv(ob, layer_name="UVMap", metres_per_tile=1.0):
    """Per-face planar projection on the dominant axis: 1 UV unit = `metres_per_tile` metres, so a
    world-grid or tiling material reads at true scale in Unreal."""
    s = 1.0 / metres_per_tile
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    uv = bm.loops.layers.uv.get(layer_name) or bm.loops.layers.uv.new(layer_name)
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for loop in f.loops:
            co = loop.vert.co
            if ax == 2:
                u, v = (co.x, co.y) if n.z >= 0 else (-co.x, co.y)
            elif ax == 1:
                u, v = (co.x, co.z) if n.y <= 0 else (-co.x, co.z)
            else:
                u, v = (co.y, co.z) if n.x >= 0 else (-co.y, co.z)
            loop[uv].uv = (u * s, v * s)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


def triangle_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)
