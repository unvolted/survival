"""Build, validate and export the whole greybox kit, then render the overview preview.

Run:  ~/.venv-blender/bin/python Source/Blender/Scripts/Greybox_BuildAll.py [--results out.json] [--no-render]

Writes Source/Blender/Greybox/<AssetId>.blend, Export/FBX/<SM_Name>.fbx and
Source/Blender/Previews/Greybox_Overview.png. Exits non-zero if any asset fails validation.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import Greybox_Buildables   # noqa: E402
import Greybox_RefHuman     # noqa: E402
import Greybox_RuinKit      # noqa: E402
from rflib.pipeline import main  # noqa: E402

ALL_SPECS = Greybox_RuinKit.SPECS + Greybox_Buildables.SPECS + Greybox_RefHuman.SPECS

if __name__ == "__main__":
    argv = [a for a in sys.argv[1:] if a != "--no-render"]
    _, failed = main(ALL_SPECS, argv)
    if not failed and "--no-render" not in sys.argv and "--no-export" not in argv:
        import Greybox_Overview  # noqa: E402
        Greybox_Overview.render()
    sys.exit(1 if failed else 0)
