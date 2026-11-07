"""Primitive builders. Each returns a Part: plain vertex and face lists plus a material key.

All sizes are metres. Every primitive is a closed shell; face winding is fixed afterwards by
meshbuild.recalc_normals, and validate checks that each shell ends up with outward normals.
"""
import math

import bmesh
from mathutils import Matrix, Vector


class Part:
    __slots__ = ("verts", "faces", "mat")

    def __init__(self, verts, faces, mat=None):
        self.verts = [Vector(v) for v in verts]
        self.faces = [tuple(f) for f in faces]
        self.mat = mat

    def transformed(self, matrix):
        return Part([matrix @ v for v in self.verts], self.faces, self.mat)

    def translated(self, offset):
        return self.transformed(Matrix.Translation(Vector(offset)))

    def bounds(self):
        xs, ys, zs = zip(*self.verts)
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def box(mn, mx, mat=None):
    x0, y0, z0 = mn
    x1, y1, z1 = mx
    assert x1 > x0 and y1 > y0 and z1 > z0, (mn, mx)
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (3, 0, 4, 7), (1, 2, 6, 5)]
    return Part(v, f, mat)


def _frame(direction, up=(0.0, 0.0, 1.0)):
    """Orthonormal frame (d, u, w) around an axis: u is the perpendicular closest to `up`."""
    d = Vector(direction).normalized()
    upv = Vector(up).normalized()
    if abs(d.dot(upv)) > 0.999:
        upv = Vector((1.0, 0.0, 0.0)) if abs(d.x) < 0.9 else Vector((0.0, 1.0, 0.0))
    u = (upv - d * upv.dot(d)).normalized()
    w = u.cross(d).normalized()
    return d, u, w


def cylinder(p0, p1, radius, segments=12, mat=None, up=(0.0, 0.0, 1.0)):
    """Prism with flat (cut) ends. Vertices sit on the circle; with segments divisible by 4 there
    are vertices on +-u and +-w, so the bounding box equals the diameter exactly."""
    p0, p1 = Vector(p0), Vector(p1)
    d, u, w = _frame(p1 - p0, up)
    ring = []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments
        ring.append(math.cos(a) * w + math.sin(a) * u)
    verts = [p0 + radius * r for r in ring] + [p1 + radius * r for r in ring]
    n = segments
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(reversed(range(n))))
    faces.append(tuple(range(n, 2 * n)))
    return Part(verts, faces, mat)


def stake(base, tip, half_width, mat=None, up=(0.0, 0.0, 1.0)):
    """Sharpened stick: square pyramid from a base centre to a tip."""
    base, tip = Vector(base), Vector(tip)
    d, u, w = _frame(tip - base, up)
    h = half_width
    verts = [base + h * (-u - w), base + h * (-u + w), base + h * (u + w), base + h * (u - w), tip]
    faces = [(3, 2, 1, 0), (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
    return Part(verts, faces, mat)


def prism(profile, axis, a0, a1, mat=None):
    """Extrude a closed 2D polygon (no self-intersections) along an axis from a0 to a1.

    axis 'X': profile points are (y, z); 'Y': (x, z); 'Z': (x, y)."""
    def lift(p, a):
        if axis == 'X':
            return (a, p[0], p[1])
        if axis == 'Y':
            return (p[0], a, p[1])
        return (p[0], p[1], a)

    n = len(profile)
    verts = [lift(p, a0) for p in profile] + [lift(p, a1) for p in profile]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return Part(verts, faces, mat)


def torus(center, major_radius, minor_radius, major_segments=8, minor_segments=4,
          normal=(0.0, 1.0, 0.0), mat=None):
    c = Vector(center)
    nrm, e1, e2 = _frame(normal, (1.0, 0.0, 0.0) if abs(normal[0]) < 0.9 else (0.0, 0.0, 1.0))
    verts = []
    for i in range(major_segments):
        t = 2.0 * math.pi * i / major_segments
        radial = math.cos(t) * e1 + math.sin(t) * e2
        for j in range(minor_segments):
            p = 2.0 * math.pi * j / minor_segments
            verts.append(c + (major_radius + minor_radius * math.cos(p)) * radial
                         + minor_radius * math.sin(p) * nrm)
    faces = []
    M, N = major_segments, minor_segments
    for i in range(M):
        for j in range(N):
            a = i * N + j
            b = ((i + 1) % M) * N + j
            c2 = ((i + 1) % M) * N + (j + 1) % N
            d2 = i * N + (j + 1) % N
            faces.append((a, b, c2, d2))
    return Part(verts, faces, mat)


def hull(points, mat=None, merge_coplanar=False):
    """Convex hull of a point set as a Part (closed, convex)."""
    bm = bmesh.new()
    for p in points:
        bm.verts.new(Vector(p))
    res = bmesh.ops.convex_hull(bm, input=list(bm.verts), use_existing_faces=False)
    junk = list({g for g in res["geom_interior"] + res["geom_unused"] if isinstance(g, bmesh.types.BMVert)})
    junk += [v for v in bm.verts if not v.link_faces and v not in junk]
    if junk:
        bmesh.ops.delete(bm, geom=junk, context='VERTS')
    if merge_coplanar:
        bmesh.ops.dissolve_limit(bm, angle_limit=1e-4, verts=list(bm.verts), edges=list(bm.edges))
    bm.verts.index_update()
    verts = [v.co.copy() for v in bm.verts]
    faces = [tuple(v.index for v in f.verts) for f in bm.faces]
    bm.free()
    return Part(verts, faces, mat)


def rot_z(deg, about=(0.0, 0.0, 0.0)):
    about = Vector(about)
    return Matrix.Translation(about) @ Matrix.Rotation(math.radians(deg), 4, 'Z') @ Matrix.Translation(-about)
