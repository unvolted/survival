"""AssetSpec and the build -> validate -> save .blend -> export FBX -> re-import check runner."""
import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Callable

import bpy

from . import collision, export, materials, meshbuild, paths, sockets, validate
from . import scene as rfscene


@dataclass
class AssetSpec:
    name: str                 # final Unreal asset name, e.g. SM_Build_LogWall_T1_Intact
    asset_id: str             # manifest asset_id, e.g. Build_LogWall_T1
    kind: str                 # manifest type: Modular | Buildable | Reference
    build: Callable[[], dict]  # -> {"parts": [...], "cut": [...], "ucx": [...], "sockets": [...]}
    bounds: tuple             # expected ((minx, miny, minz), (maxx, maxy, maxz)) in metres, pivot at origin
    budget: int               # triangle budget (brief: Topology and budgets)
    pivot: str                # where the pivot is, in words (manifest notes)
    notes: str = ""
    require_collision: bool = True
    sockets_expected: list = field(default_factory=list)  # filled from build()

    @property
    def blend_path(self):
        return paths.GREYBOX_BLEND_DIR / f"{self.asset_id}.blend"

    @property
    def fbx_path(self):
        return paths.EXPORT_FBX_DIR / f"{self.name}.fbx"


def build_in_scene(spec, collection=None):
    """Build the asset's objects in the current scene. Returns (render_ob, ucx_obs, socket_obs)."""
    mats = materials.greybox_palette()
    col = collection or rfscene.new_collection(spec.name)
    data = spec.build()
    ob = meshbuild.build_object(spec.name, data["parts"], mats, col)
    if data.get("cut"):
        meshbuild.boolean_difference(ob, data["cut"], col)
    meshbuild.recalc_normals(ob)
    meshbuild.box_uv(ob)
    for poly in ob.data.polygons:
        poly.use_smooth = False
    ucx = collision.add_ucx(ob, data.get("ucx", []), col)
    socks = data.get("sockets", [])
    spec.sockets_expected = socks
    sock_obs = [sockets.add_socket(ob, s, col) for s in socks]
    return ob, ucx, sock_obs


def run_asset(spec, export_files=True):
    paths.ensure_dirs()
    rfscene.reset_scene()
    ob, ucx, sock_obs = build_in_scene(spec)
    res = validate.validate_asset(spec, ob, ucx, sock_obs)
    tris = res["info"]["triangles"]
    result = {
        "name": spec.name, "asset_id": spec.asset_id, "kind": spec.kind, "pivot": spec.pivot,
        "notes": spec.notes, "budget": spec.budget, "blend": None, "fbx": None,
        "errors": list(res["errors"]), "info": res["info"],
    }
    if export_files:
        bpy.ops.wm.save_as_mainfile(filepath=str(spec.blend_path), compress=True)
        export.export_fbx(spec.fbx_path, [ob] + ucx + sock_obs, active=ob)
        result["blend"] = str(spec.blend_path.relative_to(paths.REPO_ROOT))
        result["fbx"] = str(spec.fbx_path.relative_to(paths.REPO_ROOT))
        fbx = validate.validate_fbx_roundtrip(spec.fbx_path, spec, tris, spec.sockets_expected)
        result["errors"] += fbx["errors"]
        result["info"].update(fbx["info"])
    return result


def print_table(results):
    print(f"{'asset':44} {'tris':>6} {'budget':>6} {'ucx':>4} {'size cm (x y z)':>24}  status")
    for r in results:
        i = r["info"]
        size = " ".join(f"{v:g}" for v in i.get("size_cm", ()))
        status = "OK" if not r["errors"] else "FAIL"
        print(f"{r['name']:44} {i.get('triangles', 0):6d} {r['budget']:6d} {i.get('ucx', 0):4d} {size:>24}  {status}")
        for e in r["errors"]:
            print(f"    ! {e}")


def main(specs, argv=None):
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="asset names to build (default: all)")
    ap.add_argument("--results", help="write a JSON list of results here")
    ap.add_argument("--no-export", action="store_true", help="validate only; write no files")
    args = ap.parse_args(argv)
    chosen = [s for s in specs if not args.only or s.name in args.only]
    results = [run_asset(s, export_files=not args.no_export) for s in chosen]
    print_table(results)
    if args.results:
        with open(args.results, "w") as fh:
            json.dump(results, fh, indent=1, default=str)
    failed = [r for r in results if r["errors"]]
    if failed:
        print(f"{len(failed)} asset(s) failed validation")
    return results, failed
