#!/usr/bin/env python3
"""Check ROOTFALL file names and the asset manifest against the handoff contract.

Plain Python 3 (no Unreal needed), read-only. Run from anywhere:

    python3 Unreal/ROOTFALL/Scripts/check_naming.py            # Unreal content + manifest
    python3 Unreal/ROOTFALL/Scripts/check_naming.py --all      # also Concept/ and Export/

Exit code 0 = no errors, 1 = errors found (warnings never fail the run).

Rules (Design/ROOTFALL_Brief.md, "Handoff contract"):
  * Names are PascalCase words joined by underscores, no spaces.
  * Every asset name starts with a contract prefix. Prefixes the brief does not list but the
    project needs are marked ASSUMED below (see Reports/2026-11-07_GameBuilder_M0.md).
  * Textures (T_) end in _BC, _N, _ORM or _E.
  * Buildable tiers are T1, T2 or T3; damage states are _Intact, _Damaged, _Broken.
  * Manifest: exact header, known status values, unique asset_id.
"""

import argparse
import csv
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PROJECT_ROOT = os.path.join(REPO_ROOT, "Unreal", "ROOTFALL")

# Prefixes from the brief's naming table.
CONTRACT_PREFIXES = [
    "CA_", "SM_", "SK_", "SKEL_", "A_", "T_", "M_", "MI_", "BP_", "ABP_",
    "DA_", "DT_", "WBP_", "SFX_", "MS_", "UCX_", "SOCKET_",
]
# ASSUMED: maps (L_) and Enhanced Input assets (IA_, IMC_) have no prefix in the brief.
ASSUMED_PREFIXES = ["L_", "IA_", "IMC_"]

UNREAL_PREFIXES = [p for p in CONTRACT_PREFIXES if p not in ("CA_", "UCX_", "SOCKET_")] + ASSUMED_PREFIXES
TEXTURE_SUFFIXES = ("_BC", "_N", "_ORM", "_E")
DAMAGE_STATES = ("Intact", "Damaged", "Broken")
NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]*(_[A-Za-z0-9]+)*$")
TIER_PATTERN = re.compile(r"^T\d+$")

# Engine-managed folders inside Content/ whose file names are not ours.
IGNORED_CONTENT_DIRS = {"__ExternalActors__", "__ExternalObjects__", "Developers", "Collections"}

MANIFEST_HEADER = [
    "asset_id", "type", "concept_file", "blend_file", "export_file",
    "triangles", "normal_map_format", "status", "owner", "notes",
]
MANIFEST_STATUSES = {
    "Planned", "Concept Done", "Greybox", "Modeled", "Textured",
    "Rigged", "Exported", "Imported", "In Game", "Blocked",
}
NORMAL_MAP_FORMATS = {"", "DirectX", "OpenGL", "N/A"}


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checked = 0

    def error(self, path, message):
        self.errors.append("{}: {}".format(os.path.relpath(path, REPO_ROOT), message))

    def warn(self, path, message):
        self.warnings.append("{}: {}".format(os.path.relpath(path, REPO_ROOT), message))


def check_name(report, path, name, allowed_prefixes):
    """Checks one asset base name (no extension)."""
    report.checked += 1
    if " " in name:
        report.error(path, "name contains a space")
        return
    if not NAME_PATTERN.match(name):
        report.error(path, "not PascalCase words joined by underscores")
    prefix = next((p for p in sorted(allowed_prefixes, key=len, reverse=True) if name.startswith(p)), None)
    if prefix is None:
        report.error(path, "no allowed prefix (expected one of {})".format(" ".join(allowed_prefixes)))
        return
    if prefix in ASSUMED_PREFIXES:
        report.warn(path, "uses assumed prefix {} (not in the brief's table)".format(prefix))
    if prefix == "T_" and not name.endswith(TEXTURE_SUFFIXES):
        report.error(path, "texture must end in one of {}".format(" ".join(TEXTURE_SUFFIXES)))

    tokens = name.split("_")[1:]
    for token in tokens:
        if TIER_PATTERN.match(token) and token not in ("T1", "T2", "T3"):
            report.error(path, "tier {} is not T1, T2 or T3".format(token))
    states = [t for t in tokens if t in DAMAGE_STATES]
    if len(states) > 1:
        report.error(path, "more than one damage state ({})".format(", ".join(states)))
    elif states and prefix not in ("T_",) and tokens[-1] not in DAMAGE_STATES:
        # Damage state goes last, e.g. SM_Build_LogWall_T1_Intact (textures may carry a suffix after it).
        report.warn(path, "damage state {} is not the last part of the name".format(states[0]))


def walk_files(root, ignored_dirs=()):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in ignored_dirs and not d.startswith("."))
        for filename in sorted(filenames):
            yield os.path.join(dirpath, filename), filename


def check_unreal_content(report):
    content = os.path.join(PROJECT_ROOT, "Content")
    if not os.path.isdir(content):
        report.error(content, "missing Content folder")
        return
    for path, filename in walk_files(content, IGNORED_CONTENT_DIRS):
        base, ext = os.path.splitext(filename)
        if filename == ".gitkeep":
            continue
        if ext not in (".uasset", ".umap"):
            report.warn(path, "not an Unreal asset; keep source files out of Content/")
            continue
        rel = os.path.relpath(path, content).replace(os.sep, "/")
        if not rel.startswith("RF/"):
            report.error(path, "project assets go under Content/RF/")
        if ext == ".umap":
            report.checked += 1
            if not base.startswith("L_"):
                report.error(path, "maps are named L_<Name> (assumed prefix)")
            elif not NAME_PATTERN.match(base):
                report.error(path, "not PascalCase words joined by underscores")
            continue
        check_name(report, path, base, UNREAL_PREFIXES)


def check_exports(report):
    fbx_dir = os.path.join(REPO_ROOT, "Export", "FBX")
    for path, filename in walk_files(fbx_dir):
        base, ext = os.path.splitext(filename)
        if filename == ".gitkeep" or ext.lower() not in (".fbx",):
            continue
        check_name(report, path, base, ["SM_", "SK_", "SKEL_", "A_"])
    tex_dir = os.path.join(REPO_ROOT, "Export", "Textures")
    for path, filename in walk_files(tex_dir):
        base, ext = os.path.splitext(filename)
        if filename == ".gitkeep" or ext.lower() not in (".png", ".tga", ".exr", ".jpg", ".jpeg"):
            continue
        check_name(report, path, base, ["T_"])


def check_concepts(report):
    concept_dir = os.path.join(REPO_ROOT, "Concept")
    for path, filename in walk_files(concept_dir, {"_raw"}):
        base, ext = os.path.splitext(filename)
        if ext.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        check_name(report, path, base, ["CA_"])


def check_manifest(report):
    path = os.path.join(REPO_ROOT, "Manifest", "asset_manifest.csv")
    if not os.path.isfile(path):
        report.error(path, "manifest is missing")
        return
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        report.error(path, "manifest is empty (no header)")
        return
    header = [cell.strip() for cell in rows[0]]
    if header != MANIFEST_HEADER:
        report.error(path, "header is {} but must be {}".format(",".join(header), ",".join(MANIFEST_HEADER)))
        return
    seen = {}
    for line_number, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue
        where = "{} line {}".format(path, line_number)
        if len(row) != len(MANIFEST_HEADER):
            report.error(where, "has {} columns, expected {}".format(len(row), len(MANIFEST_HEADER)))
            continue
        record = dict(zip(MANIFEST_HEADER, (cell.strip() for cell in row)))
        report.checked += 1
        asset_id = record["asset_id"]
        if not asset_id:
            report.error(where, "empty asset_id")
        elif asset_id in seen:
            report.error(where, "asset_id {} already used on line {}".format(asset_id, seen[asset_id]))
        else:
            seen[asset_id] = line_number
        if asset_id and not NAME_PATTERN.match(asset_id):
            report.error(where, "asset_id {} is not PascalCase words joined by underscores".format(asset_id))
        if record["status"] not in MANIFEST_STATUSES:
            report.error(where, "status '{}' is not one of {}".format(record["status"], ", ".join(sorted(MANIFEST_STATUSES))))
        if record["normal_map_format"] not in NORMAL_MAP_FORMATS:
            report.warn(where, "normal_map_format '{}' is not DirectX or OpenGL".format(record["normal_map_format"]))
        if record["triangles"] and not record["triangles"].isdigit():
            report.error(where, "triangles '{}' is not a whole number".format(record["triangles"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--all", action="store_true", help="also check Concept/ and Export/ file names")
    args = parser.parse_args()

    report = Report()
    check_unreal_content(report)
    check_manifest(report)
    if args.all:
        check_exports(report)
        check_concepts(report)

    for line in report.warnings:
        print("WARNING " + line)
    for line in report.errors:
        print("ERROR   " + line)
    print("check_naming: {} item(s) checked, {} error(s), {} warning(s)".format(
        report.checked, len(report.errors), len(report.warnings)))
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
