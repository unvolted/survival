"""Validation: names, units, applied transforms, dimensions/pivot, manifold + outward normals,
triangle budget, materials/UVs, collision (convex, named, inside the mesh bounds), sockets,
and an FBX round trip (re-import the exported file and re-measure it)."""
import math
import re

import bmesh
import bpy
from mathutils import Vector

from . import scene as rfscene

TOL = 1e-4          # 0.1 mm on dimensions / socket positions
UCX_MARGIN = 0.01   # collision may exceed render bounds by at most 1 cm
NAME_RE = re.compile(r"^SM_[A-Z][A-Za-z0-9]*(_[A-Za-z0-9]+)*$")


def _bounds(points):
    xs, ys, zs = zip(*points)
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def _close(a, b, tol=TOL):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def _fmt(v):
    return "(" + ", ".join(f"{x:.4f}" for x in v) + ")"


def transform_errors(ob):
    errs = []
    if ob.location.length > 1e-6:
        errs.append(f"{ob.name}: location not zero {_fmt(ob.location)}")
    if any(abs(a) > 1e-6 for a in ob.rotation_euler):
        errs.append(f"{ob.name}: rotation not applied")
    if any(abs(s - 1.0) > 1e-6 for s in ob.scale):
        errs.append(f"{ob.name}: scale not applied {_fmt(ob.scale)}")
    if ob.parent is not None:
        errs.append(f"{ob.name}: mesh is parented to {ob.parent.name}")
    if ob.modifiers:
        errs.append(f"{ob.name}: unapplied modifiers {[m.name for m in ob.modifiers]}")
    return errs


def _shells(bm):
    """Connected face groups."""
    seen, shells = set(), []
    for f in bm.faces:
        if f.index in seen:
            continue
        stack, shell = [f], []
        seen.add(f.index)
        while stack:
            g = stack.pop()
            shell.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index)
                        stack.append(h)
        shells.append(shell)
    return shells


def _signed_volume(faces):
    vol = 0.0
    for f in faces:
        vs = [v.co for v in f.verts]
        for i in range(1, len(vs) - 1):
            vol += vs[0].dot(vs[i].cross(vs[i + 1])) / 6.0
    return vol


def topology_report(ob):
    """Manifold / normal checks on a mesh object. Returns (errors, info)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    bm.faces.index_update()
    errs = []
    non_manifold = [e for e in bm.edges if not e.is_manifold]
    if non_manifold:
        errs.append(f"{ob.name}: {len(non_manifold)} non-manifold edges")
    flipped_edges = [e for e in bm.edges if e.is_manifold and not e.is_contiguous]
    if flipped_edges:
        errs.append(f"{ob.name}: {len(flipped_edges)} edges between faces with opposite normals")
    loose = [v for v in bm.verts if not v.link_faces]
    if loose:
        errs.append(f"{ob.name}: {len(loose)} loose vertices")
    degenerate = [f for f in bm.faces if f.calc_area() < 1e-8]
    if degenerate:
        errs.append(f"{ob.name}: {len(degenerate)} zero-area faces")
    shells = _shells(bm)
    vols = [_signed_volume(s) for s in shells]
    inverted = [v for v in vols if v <= 0.0]
    if inverted:
        errs.append(f"{ob.name}: {len(inverted)} shell(s) with inward normals or no volume")
    info = {"shells": len(shells), "volume_m3": round(sum(vols), 5)}
    bm.free()
    return errs, info


def convex_errors(ob, eps=1e-5):
    """Every vertex must lie behind every triangle's plane (triangles, so non-planar ngons count)."""
    me = ob.data
    me.calc_loop_triangles()
    pts = [v.co for v in me.vertices]
    for tri in me.loop_triangles:
        a, b, c = (me.vertices[i].co for i in tri.vertices)
        n = (b - a).cross(c - a)
        if n.length < 1e-12:
            continue
        n.normalize()
        d = n.dot(a)
        if any(n.dot(p) - d > eps for p in pts):
            return [f"{ob.name}: not convex"]
    return []


def validate_asset(spec, render_ob, ucx_obs, socket_obs):
    """In-Blender checks for one built asset. Returns dict(errors=[...], info={...})."""
    errs = list(rfscene.check_units())
    info = {}
    # names
    if not NAME_RE.match(render_ob.name) or render_ob.name != spec.name:
        errs.append(f"bad mesh name {render_ob.name!r} (expected {spec.name!r})")
    # transforms
    errs += transform_errors(render_ob)
    # dimensions + pivot (bounds are relative to the pivot at the origin)
    verts = [v.co.copy() for v in render_ob.data.vertices]
    mn, mx = _bounds(verts)
    info["bounds_min"], info["bounds_max"] = tuple(mn), tuple(mx)
    info["size_cm"] = tuple(round((b - a) * 100.0, 2) for a, b in zip(mn, mx))
    emn, emx = spec.bounds
    if not (_close(mn, emn) and _close(mx, emx)):
        errs.append(f"bounds {_fmt(mn)}..{_fmt(mx)} != expected {_fmt(emn)}..{_fmt(emx)}")
    # topology
    t_errs, t_info = topology_report(render_ob)
    errs += t_errs
    info.update(t_info)
    # triangles
    tris = sum(len(p.vertices) - 2 for p in render_ob.data.polygons)
    info["triangles"] = tris
    if tris > spec.budget:
        errs.append(f"{tris} triangles > budget {spec.budget}")
    # materials + UVs
    mats = [m for m in render_ob.data.materials]
    info["materials"] = [m.name if m else None for m in mats]
    if not mats or any(m is None for m in mats):
        errs.append("missing material slot")
    else:
        used = {p.material_index for p in render_ob.data.polygons}
        if max(used) >= len(mats):
            errs.append("face uses a material index without a slot")
    if not render_ob.data.uv_layers:
        errs.append("no UV layer")
    # collision
    info["ucx"] = len(ucx_obs)
    if spec.require_collision and not ucx_obs:
        errs.append("no UCX_ collision")
    for i, u in enumerate(ucx_obs):
        if u.name != f"UCX_{spec.name}_{i:02d}":
            errs.append(f"bad collision name {u.name}")
        errs += transform_errors(u)
        ue, _ = topology_report(u)
        errs += ue
        errs += convex_errors(u)
        umn, umx = _bounds([v.co for v in u.data.vertices])
        if any(a < b - UCX_MARGIN for a, b in zip(umn, mn)) or any(a > b + UCX_MARGIN for a, b in zip(umx, mx)):
            errs.append(f"{u.name} extends more than 1 cm outside the mesh bounds")
    # sockets
    info["sockets"] = [s.name for s in socket_obs]
    expected = [s.name for s in spec.sockets_expected]
    if sorted(expected) != sorted(info["sockets"]):
        errs.append(f"sockets {info['sockets']} != expected {expected}")
    for s in socket_obs:
        if s.parent is not render_ob:
            errs.append(f"{s.name} not parented to {render_ob.name}")
        if any(abs(v - 1.0) > 1e-6 for v in s.scale):
            errs.append(f"{s.name}: scale not 1")
    return {"errors": errs, "info": info}


def validate_fbx_roundtrip(fbx_path, spec, expected_tris, expected_sockets):
    """Re-import the exported FBX into an empty scene and re-measure it in world space."""
    rfscene.reset_scene()
    bpy.ops.import_scene.fbx(filepath=str(fbx_path))
    objs = {o.name: o for o in bpy.context.scene.objects}
    errs, info = [], {}
    ob = objs.get(spec.name)
    if ob is None or ob.type != 'MESH':
        return {"errors": [f"FBX: mesh {spec.name} not found (objects: {sorted(objs)})"], "info": info}
    mw = ob.matrix_world
    pts = [mw @ v.co for v in ob.data.vertices]
    mn, mx = _bounds(pts)
    info["fbx_bounds_min"], info["fbx_bounds_max"] = tuple(mn), tuple(mx)
    emn, emx = spec.bounds
    if not (_close(mn, emn) and _close(mx, emx)):
        errs.append(f"FBX bounds {_fmt(mn)}..{_fmt(mx)} != expected {_fmt(emn)}..{_fmt(emx)}")
    info["fbx_object_scale"] = tuple(round(s, 6) for s in ob.matrix_world.to_scale())
    non_tri = [p for p in ob.data.polygons if len(p.vertices) != 3]
    if non_tri:
        errs.append(f"FBX: {len(non_tri)} faces not triangulated")
    tris = len(ob.data.polygons)
    info["fbx_triangles"] = tris
    if tris != expected_tris:
        errs.append(f"FBX triangles {tris} != Blender {expected_tris}")
    if not ob.data.materials or any(m is None for m in ob.data.materials):
        errs.append("FBX: missing material")
    info["fbx_materials"] = [m.name for m in ob.data.materials if m]
    ucx = sorted(n for n in objs if n.startswith(f"UCX_{spec.name}_"))
    info["fbx_ucx"] = len(ucx)
    if spec.require_collision and not ucx:
        errs.append("FBX: no UCX_ hulls")
    for n in ucx:
        u = objs[n]
        upts = [u.matrix_world @ v.co for v in u.data.vertices]
        umn, umx = _bounds(upts)
        if any(a < b - UCX_MARGIN for a, b in zip(umn, emn)) or any(a > b + UCX_MARGIN for a, b in zip(umx, emx)):
            errs.append(f"FBX: {n} outside mesh bounds")
    for s in expected_sockets:
        e = objs.get(s.name)
        if e is None or e.type != 'EMPTY':
            errs.append(f"FBX: socket {s.name} missing")
            continue
        loc = e.matrix_world.translation
        if not _close(loc, s.loc):
            errs.append(f"FBX: {s.name} at {_fmt(loc)} != {_fmt(s.loc)}")
        want = Vector(tuple(math.radians(a) for a in s.rot))
        got = e.matrix_world.to_euler()
        if not _close([math.cos(a) for a in got] + [math.sin(a) for a in got],
                      [math.cos(a) for a in want] + [math.sin(a) for a in want], 1e-4):
            errs.append(f"FBX: {s.name} rotation {tuple(math.degrees(a) for a in got)} != {s.rot}")
    extra = sorted(n for n in objs if not (n == spec.name or n.startswith("UCX_") or n.startswith("SOCKET_")))
    if extra:
        errs.append(f"FBX: unexpected objects {extra}")
    return {"errors": errs, "info": info}
