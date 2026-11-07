"""Custom collision: convex hulls named UCX_<MeshName>_00, _01 ... exported in the same FBX.

Unreal matches a UCX_ mesh to the render mesh whose node name follows the prefix, so the render
object must be named exactly like the asset (SM_...). UCX objects get identity transforms and no
material; Unreal ignores their materials."""
from . import geo, meshbuild


def ucx_name(mesh_name, index):
    return f"UCX_{mesh_name}_{index:02d}"


def add_ucx(render_ob, hulls, collection):
    """`hulls`: list of Parts or point lists. Each becomes one convex hull object."""
    out = []
    for i, h in enumerate(hulls):
        pts = h.verts if isinstance(h, geo.Part) else h
        part = geo.hull(pts, merge_coplanar=True)
        ob = meshbuild.build_object(ucx_name(render_ob.name, i), [part], {}, collection,
                                    require_material=False)
        meshbuild.recalc_normals(ob)
        ob.display_type = 'WIRE'
        ob.hide_render = True
        out.append(ob)
    return out
