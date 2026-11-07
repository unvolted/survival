"""ROOTFALL shared Blender helpers (Agent 2, modeler).

Modules
    paths      repo-relative output folders
    scene      empty scene with metric units, unit scale 1.0
    geo        primitive builders as plain vertex/face lists (Part)
    meshbuild  Part lists -> Blender objects, exact booleans, box UVs
    materials  simple grey PBR materials (M_Greybox_*)
    collision  UCX_ convex hull helpers
    sockets    SOCKET_ empties
    export     the FBX export preset from the brief
    validate   in-Blender checks and the FBX round-trip check
    pipeline   AssetSpec + build/validate/save/export runner

Run every script with the bpy module from Tools/setup_blender.sh:
    ~/.venv-blender/bin/python Source/Blender/Scripts/<Script>.py
"""
