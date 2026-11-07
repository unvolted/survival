"""Greybox: SM_Ref_Human_180, a 180 cm reference figure for scale checks in Unreal.

Run:  ~/.venv-blender/bin/python Source/Blender/Scripts/Greybox_RefHuman.py [--no-export]

Faces -Y in Blender (the brief's character convention). Dark markers on the face, chest and toes show
the front, so a wrong import rotation is obvious. Pivot bottom centre between the feet; top of head at
exactly 180 cm. Placed next to the UE5 Mannequin it should read the same height.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rflib import geo                       # noqa: E402
from rflib.pipeline import AssetSpec, main  # noqa: E402

F, K = "Ref", "RefFront"
HEIGHT = 1.80


def figure():
    b = geo.box
    parts = []
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 0.03, sx * 0.17))
        parts.append(b((x0, -0.075, 0.08), (x1, 0.075, 0.88), F))          # leg
        parts.append(b((x0, -0.12, 0.0), (x1, 0.08, 0.08), F))             # foot
        parts.append(b((x0 + 0.01, -0.18, 0.0), (x1 - 0.01, -0.12, 0.06), K))  # toe marker (front)
        a0, a1 = sorted((sx * 0.20, sx * 0.29))
        parts.append(b((a0, -0.05, 0.90), (a1, 0.05, 1.48), F))            # arm
    parts.append(b((-0.20, -0.11, 0.88), (0.20, 0.11, 1.50), F))           # torso
    parts.append(b((-0.10, -0.12, 1.25), (0.10, -0.11, 1.40), K))          # chest marker (front)
    parts.append(b((-0.06, -0.06, 1.50), (0.06, 0.06, 1.56), F))           # neck
    parts.append(b((-0.10, -0.115, 1.56), (0.10, 0.115, HEIGHT), F))       # head
    parts.append(b((-0.02, -0.145, 1.64), (0.02, -0.115, 1.68), K))        # nose (front)
    return {"parts": parts, "ucx": [b((-0.29, -0.18, 0), (0.29, 0.115, HEIGHT))]}


SPECS = [
    AssetSpec("SM_Ref_Human_180", "Ref_Human_180", "Reference", figure,
              ((-0.29, -0.18, 0), (0.29, 0.115, HEIGHT)), 3000,
              "pivot bottom centre between the feet; faces -Y",
              "scale reference only; UCX box for scale tests"),
]

if __name__ == "__main__":
    _, failed = main(SPECS)
    sys.exit(1 if failed else 0)
