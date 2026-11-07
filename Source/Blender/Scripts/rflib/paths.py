"""Repo folders used by the Blender scripts (handoff contract layout)."""
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]          # Source/Blender/Scripts
BLENDER_DIR = SCRIPTS_DIR.parent                            # Source/Blender
REPO_ROOT = BLENDER_DIR.parents[1]                          # repo root

GREYBOX_BLEND_DIR = BLENDER_DIR / "Greybox"                 # greybox .blend sources
PREVIEWS_DIR = BLENDER_DIR / "Previews"
EXPORT_FBX_DIR = REPO_ROOT / "Export" / "FBX"
EXPORT_TEXTURES_DIR = REPO_ROOT / "Export" / "Textures"


def ensure_dirs():
    for d in (GREYBOX_BLEND_DIR, PREVIEWS_DIR, EXPORT_FBX_DIR):
        d.mkdir(parents=True, exist_ok=True)
