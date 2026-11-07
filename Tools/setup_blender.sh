#!/usr/bin/env bash
# Installs Blender 5.2 LTS as a Python module (bpy) for headless modelling, baking and FBX export.
# Usage: bash Tools/setup_blender.sh   then   ~/.venv-blender/bin/python <script.py>
set -euo pipefail
VENV="${HOME}/.venv-blender"
if [ ! -x "${VENV}/bin/python" ]; then
  python3 -m venv "${VENV}"
fi
"${VENV}/bin/pip" install -q bpy==5.2.3 numpy pillow
"${VENV}/bin/python" -c "import bpy; print('Blender', bpy.app.version_string)"
