"""Sockets: empties named SOCKET_<Name>, parented to the render mesh (identity parent inverse), so
their local transform is the socket transform Unreal creates on import ("SOCKET_" is stripped)."""
import math
import re

import bpy
from mathutils import Matrix

SOCKET_RE = re.compile(r"^SOCKET_[A-Z][A-Za-z0-9]*(_[A-Za-z0-9]+)*$")


class Socket:
    __slots__ = ("name", "loc", "rot")

    def __init__(self, name, loc, rot=(0.0, 0.0, 0.0)):
        """rot: XYZ Euler in degrees."""
        if not SOCKET_RE.match(name):
            raise ValueError(f"bad socket name {name!r}")
        self.name, self.loc, self.rot = name, tuple(loc), tuple(rot)


def add_socket(render_ob, sock, collection, size=0.25):
    e = bpy.data.objects.new(sock.name, None)
    e.empty_display_type = 'ARROWS'
    e.empty_display_size = size
    collection.objects.link(e)
    e.parent = render_ob
    e.matrix_parent_inverse = Matrix.Identity(4)
    e.location = sock.loc
    e.rotation_euler = tuple(math.radians(a) for a in sock.rot)
    return e
