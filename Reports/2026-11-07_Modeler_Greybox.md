# Modeler — Greybox kit

Agent 2, deliverable 1. Every mesh is a plain block built from the brief's dimensions; no concept sheets were used.
All 29 meshes pass the in-Blender validation and the FBX re-import check. **None are verified in Unreal yet:
the user's PC with UE 5.8 was not attached during this task.**

## Done

**Tooling**
- Blender 5.2.3 LTS installed with `bash Tools/setup_blender.sh`, as the `bpy` module in `~/.venv-blender`, outside the repo.
- Shared helpers in `Source/Blender/Scripts/rflib/`:
  - `scene.py`: empty scene, Metric, Unit Scale 1.0.
  - `geo.py`: box, cylinder, stake, prism, torus and hull primitives.
  - `meshbuild.py`: builds objects, applies Exact booleans, adds box-projected UVs at 1 UV = 1 m.
  - `materials.py`: grey `M_Greybox_*` PBR materials.
  - `collision.py`: `UCX_<Mesh>_NN` convex hulls.
  - `sockets.py`: `SOCKET_` empties parented to the mesh.
  - `export.py`: the FBX preset below.
  - `validate.py`: the checks listed under Verified.
  - `pipeline.py`: build, validate, save `.blend`, export FBX, re-import check.
- Build scripts, one per family:
  - `Greybox_RuinKit.py`
  - `Greybox_Buildables.py`
  - `Greybox_RefHuman.py`
  - `Greybox_Overview.py` (preview)
  - `Greybox_BuildAll.py` (runs everything)
- Rebuild everything with `~/.venv-blender/bin/python Source/Blender/Scripts/Greybox_BuildAll.py`. It exits non-zero if any asset fails.

**Meshes**: each one has `Export/FBX/<Name>.fbx` and `Source/Blender/Greybox/<asset_id>.blend`.

| Mesh | Tris | UCX | Size cm (X×Y×Z) | Sockets |
|---|---:|---:|---|---|
| SM_Ruin_Wall_400 | 12 | 1 | 400×20×300 | |
| SM_Ruin_Wall_200 | 12 | 1 | 200×20×300 | |
| SM_Ruin_Wall_100 | 12 | 1 | 100×20×300 | |
| SM_Ruin_Wall_Corner | 12 | 1 | 30×30×300 | |
| SM_Ruin_Wall_Window_400 | 32 | 4 | 400×20×300, opening 100×120 at sill 90 | BarricadeFront, BarricadeBack |
| SM_Ruin_Wall_Door_400 | 28 | 3 | 400×20×300, opening 100×220 | BarricadeFront, BarricadeBack |
| SM_Ruin_Wall_Collapsed_400 | 36 | 7 | 400×20×300 (top falls to 40) | |
| SM_Ruin_Floor_400 | 12 | 1 | 400×400×20 | |
| SM_Ruin_Roof_400 | 12 | 1 | 400×400×220 (rise 200) | |
| SM_Ruin_Stairs_300 | 124 | 1 | 100×400×300 (15 × 20 cm steps) | StairBottom, StairTop |
| SM_Ruin_RubblePile_01 | 84 | 4 | 200×160×80 | |
| SM_Build_Log_T1_Intact | 44 | 1 | 400×30×30 | SnapEnd, Carry |
| SM_Build_LogWall_T1_Intact | 440 | 1 | 400×30×300 (10 logs) | SnapEnd, PlateMount, PlateMountBack |
| SM_Build_SpikedWall_T1_Intact | 536 | 2 | 400×109.6×300 | SnapEnd, PlateMountBack |
| SM_Build_MetalPlate_T3_Intact | 12 | 1 | 400×1×300 | |
| SM_Build_BarbedWire_T1_Intact | 72 | 1 | 400×11.7×130 | SnapEnd |
| SM_Build_WeldedGate_T1_Intact (frame) | 36 | 3 | 400×20×300 | SnapEnd, HingeLeft, HingeRight |
| SM_Build_WeldedGate_Leaf_T1_Intact | 12 | 1 | 179×5×270 | |
| SM_Build_BarricadeDoor_T1_Intact | 48 | 1 | 140×3×170 (4 planks) | |
| SM_Build_BarricadeWindow_T1_Intact | 36 | 1 | 140×3×100 (3 planks) | |
| SM_Build_Watchtower_T1_Intact | 684 | 11 | 230×237×500, deck top 400 | LadderBottom, LadderTop, Lookout |
| SM_Build_SpikePit_T1_Intact | 96 | 5 | 220×220×160 (below ground) | Cover |
| SM_Build_SpikePit_Cover_T1_Intact | 12 | 1 | 198×198×5 | |
| SM_Build_FireRing_T1_Intact | 92 | 3 | 400×120×55 (40 below ground) | SnapEnd |
| SM_Build_NoiseTrap_T1_Intact | 156 | 2 | 305×7×50 | TripLineStart, TripLineEnd |
| SM_Build_Deadfall_T1_Intact (frame) | 60 | 3 | 240×20×250 | WeightArmed |
| SM_Build_Deadfall_Weight_T1_Intact | 44 | 1 | 190×30×30 | |
| SM_Build_Snare_T1_Intact | 88 | 1 | 45.5×5×60 | |
| SM_Ref_Human_180 | 156 | 1 | 58×29.5×180 | |

- The largest mesh is 684 triangles. Budgets used: 8k for modular walls and large pieces, 3k for small props.
- Preview: `Source/Blender/Previews/Greybox_Overview.png`. It is rendered from the **exported FBX files**, with each attachment mounted on its host socket.
- Manifest: 29 rows added to `Manifest/asset_manifest.csv`, each with status `Greybox`, owner `Agent 2`, normal map `None` (no textures), and pivot notes.

### FBX export preset (`rflib/export.py`, `FBX_STATIC_MESH_PRESET`)
Scene: Metric, Unit Scale 1.0, 1 Blender unit = 1 m. Every mesh is built in place with identity transforms (location 0, rotation 0, scale 1).
One FBX per asset, with only that asset's objects selected (render mesh + `UCX_` + `SOCKET_`).
```
bpy.ops.export_scene.fbx(
  use_selection=True, use_visible=False, use_active_collection=False,
  global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_UNITS',
  use_space_transform=True, bake_space_transform=False, axis_forward='-Z', axis_up='Y',
  object_types={'EMPTY','MESH'}, use_mesh_modifiers=True, mesh_smooth_type='FACE',
  use_subsurf=False, use_mesh_edges=False, use_tspace=False, use_triangles=True,
  use_custom_props=False, colors_type='NONE', add_leaf_bones=False,
  primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=True,
  armature_nodetype='NULL', bake_anim=False, path_mode='AUTO', embed_textures=False, batch_mode='OFF')
```
Header of the written FBX: `UnitScaleFactor = 100` (metres), Y up, X as the coordinate axis, front axis Z with sign +1.
The preset is for static meshes only. Skeletal and animation exports need `ARMATURE` in `object_types` and `bake_anim=True`. That preset is not written yet.

## Verified
In Blender, `rflib/validate.py` checked every mesh and all passed:
- **Units:** Metric, scale 1.0.
- **Names:** `SM_` name pattern; render object named exactly as the asset.
- **Transforms:** applied on the mesh and on every UCX (location, rotation and scale identity, no parent, no modifiers).
- **Dimensions and pivot:** mesh bounds equal the design bounds relative to the origin, within 0.1 mm.
- **Topology:** manifold (no non-manifold edges, no loose verts, no zero-area faces); normals consistent; every closed shell has positive signed volume (outward normals).
- **Triangles:** count within budget.
- **Materials and UVs:** every face has a material; a UV layer exists.
- **Collision:** every UCX is named `UCX_<Mesh>_NN`, is manifold and convex, and stays within 1 cm of the mesh bounds.
- **Sockets:** expected set present, parented to the mesh, scale 1.

FBX round trip: each exported FBX was re-imported into an empty scene, and all assets passed:
- **Bounds:** world-space bounds equal the design bounds.
- **Scale:** object scale is 1.0.
- **Triangles:** fully triangulated, with the same count as the `.blend`.
- **Contents:** materials, UCX count and socket world positions and rotations are present and match. No stray objects.

The validator is proven on purpose-broken meshes. It caught flipped normals, an open shell, unapplied scale, a centred pivot instead of a corner pivot, a non-convex UCX and a missing socket. Its first version missed the non-convex case; that was fixed with per-triangle planes.

Preview: I looked at it and at zoomed crops. It shows the following:
- **Scale:** the 180 cm figure reads at about 60% of a 300 cm wall.
- **Facing:** the spikes face -Y.
- **Sockets:** the plate, both barricades, the gate leaves (one opened -70°), the pit cover and the deadfall weight all land correctly on their sockets.
- **Grid:** a room of floor, 4 walls and 4 corners assembles cleanly on the 100 cm grid.
- **Below-ground pieces:** they show through holes cut in the preview ground.
- **Fix found by the preview:** the deadfall crossbar was coplanar with its posts (black patches); fixed.

**NOT verified in Unreal.** The user's PC with UE 5.8 was not attached, so no import was done, and nothing confirms these yet:
- the 180 cm figure measures 180 cm (180 UU);
- the axis mapping;
- UCX and socket pickup;
- the Nanite build.

Under the agent rules these rows stay `Greybox`; I did not mark any `Exported`/`Imported`. The first export of each asset type still needs a check in Unreal. The 29 FBX files already exist because the task asked for the whole greybox kit; if the check finds a problem, the preset is fixed and everything is re-exported with one command.
1. **Static prop:** `SM_Ref_Human_180`. Should be 180 UU tall, scale 1.0, front markers (nose, chest, toes) facing +Y in Unreal. Blender -Y should map to UE +Y and Blender +X to UE +X.
2. **Modular piece:** `SM_Ruin_Wall_400` plus `SM_Ruin_Wall_Window_400`. Should be 400×20×300 UU, with the pivot at the grid corner, 1 and 4 UCX hulls, and sockets `BarricadeFront`/`BarricadeBack`.
3. **Buildable with sockets:** `SM_Build_LogWall_T1_Intact`. Should be 400×30×300 UU with sockets `SnapEnd`, `PlateMount` and `PlateMountBack`.

Also check that `UCX_` hulls are picked up as simple collision and `SOCKET_` empties become sockets when the FBX has `UnitScaleFactor = 100`.

## Assumptions
1. **Pipeline version:** I followed the repo's current `CLAUDE.md` and `.claude/agents/modeler.md` (Blender, FBX, `Export/FBX/`). The instructions I was launched with described an older glTF/`assets/models/` layout; that layout is not used.
2. **Ruin wall pivot:** the pivot is at the bottom of the wall's start end, **on the grid line**, and the 20 cm thickness straddles the line (±10 cm). Perpendicular walls then meet on grid points.
   - `SM_Ruin_Wall_Corner` is a 30×30 cm pillar centred on the grid point. It hides the wall overlap at L, T and X joins.
   - Inside its footprint, the pillar top is coplanar with the wall tops. This is invisible with the shared greybox material but shows as dark patches in Cycles at the preview room's corners.
   - The final kit needs a wall-top cap or trim. I did not raise the pillar, because it would then clash with an upper-storey pillar.
3. **Floor tile:** the pivot is at the cell corner **at walking level**, and the 20 cm slab hangs below (z -20 to 0).
   - Floor tops then sit at 0/300/600, an upper slab fills the top of the walls below, and the 300 cm stairs reach the next floor exactly.
   - This departs from "bottom corner", on purpose.
4. **Openings, roof and stairs:**
   - Door opening 100×220 cm and window opening 100×120 cm with a 90 cm sill, both centred at x 150–250.
   - Roof: rise 200 cm over a 400 cm run, no overhang; two pieces make an 800 cm gable. There is no gable-end wall yet.
   - Stairs: 100 cm wide, 400 cm run.
5. **Buildable pivots:**
   - **Line pieces** (log, log wall, spiked wall, barbed wire, fire ring, gate frame): run +X from a pivot at the bottom of the start end, centred on the thickness. `SOCKET_SnapEnd` marks the far end for chaining free-form lines.
   - **Placed pieces:** bottom centre.
   - **Attachments:** pivot at the mount point. Snap it to the host's `SOCKET_` and copy the socket rotation.
   - Front faces -Y in Blender, which should be +Y in Unreal (not verified).
6. **Free-form log:** a horizontal 400 × 30 cm log with flat cut ends; the same log is stacked 10 times in the wall at 30 cm spacing.
   - The ghost can place log *i* at (0, 0, 30·i cm) in the wall's space, then swap in the wall mesh.
   - A last, shorter log on a free-form line can be scaled along X, since the pivot is at its start.
7. **Metal plate:** named `SM_Build_MetalPlate_T3_Intact`, because metal plating *is* tier T3.
   - It is one 400×300×1 cm sheet covering a whole wall face.
   - "2 cm proud" is read as the plate's back face sitting 2 cm in front of the outermost wood. `SOCKET_PlateMount`/`PlateMountBack` already include that 2 cm.
   - The spiked wall only has a back mount.
8. **Welded gate:** named `_T1` as the base tier of that buildable even though it is metal. It is a frame that replaces a 400 cm wall segment (360×280 cm clear), plus one leaf mesh used twice. The right leaf goes on `SOCKET_HingeRight`, which is pre-rotated 180°.
9. **Separate meshes for moving or removable parts:** gate leaf, pit cover, deadfall weight.
10. **Dimensions the brief does not give:**
    - Spike pit: 200×200×150 cm hole.
    - Fire ring: built as a straight 400 cm burn-trench segment that chains around a perimeter; 60×30 cm channel.
    - Barbed wire: 130 cm tall.
    - Watchtower: deck top at 400 cm, 230 cm square deck.
    - Noise trap: 300 cm string at 25 cm.
    - Deadfall: zombie-scale frame, weight armed at 180 cm.
    - Snare: small-animal size.
    - The tripwire alarm is not a separate mesh.
11. **Ruin naming:** ruin pieces take no `_Intact` suffix, following the example `SM_Ruin_Wall_400` in the task. Later damaged and overgrown variants can add a suffix.
12. **Materials:** greybox materials are grey `M_Greybox_*` slots (Concrete, Wood, Metal, Soil, Rope, Ref, RefFront). No textures were made, so the normal map format is `None`.

## Blocked
- **Unreal verification:** needs the user's PC with UE 5.8 attached. Until then, no row moves past `Greybox`.

## Next
- **Game developer:**
  - Import from `Export/FBX/` at 1.0 scale, with combine meshes on, so UCX and sockets are kept.
  - Pivots and sockets are in each manifest row's notes and in the table above.
  - Spike pit and fire ring dig below z=0: the landscape needs a hole there (landscape hole material), or place them on raised ground.
  - Spike pit cover: hide or remove it when triggered, and restore it when the pit is re-armed.
  - Deadfall weight: drop it from `SOCKET_WeightArmed` to z=0.
  - Gate leaf: rotate about its local Z.
  - Watchtower ladder: use `SOCKET_LadderBottom`/`LadderTop` for climbing.
  - Noise trap: use `SOCKET_TripLineStart`/`End` to build the trigger box.
  - The `_Damaged`/`_Broken` swaps can reuse the `_Intact` greybox until final art exists.
- **Main session:** when the PC is attached, run the three Unreal checks listed under Verified, then fix the preset if needed and re-export.
- **Modeler (next task):** final buildables and ruin kit once their manifest rows are `Concept Done`. `CA_Buildables_*` and `CA_RuinKit_*` sheets are appearing in `Concept/`, but they have no manifest rows yet.
