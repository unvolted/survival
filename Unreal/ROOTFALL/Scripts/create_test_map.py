"""Create (or refresh) the M0 empty test map /Game/RF/Maps/L_Test_Empty.

Unreal editor Python script (needs the Python Editor Script Plugin and Editor Scripting Utilities,
both enabled in ROOTFALL.uproject). Safe to run again: an existing map is loaded and only the
missing actors are added; nothing else in the map is touched.

The map holds only what is needed to stand in it:
  RF_TestFloor        100 m x 100 m engine plane at Z = 0
  RF_TestPlayerStart  PlayerStart 1 m above the floor
  RF_TestSun          directional light

Run it on the PC (paths relative to Unreal/ROOTFALL; see README.md "Create the test map"):
  UnrealEditor.exe ROOTFALL.uproject -ExecutePythonScript="<abs path>/Scripts/create_test_map.py --quit"
or in an open editor:  Tools > Execute Python Script..., or the Output Log console:  py "<abs path>/Scripts/create_test_map.py"
"""

import sys

import unreal

MAP_PATH = "/Game/RF/Maps/L_Test_Empty"
FLOOR_MESH = "/Engine/BasicShapes/Plane"  # 100 x 100 uu plane, pivot at its centre

FLOOR_LABEL = "RF_TestFloor"
PLAYER_START_LABEL = "RF_TestPlayerStart"
SUN_LABEL = "RF_TestSun"


def log(message):
    unreal.log("[create_test_map] " + message)


def fail(message):
    unreal.log_error("[create_test_map] " + message)
    raise RuntimeError(message)


def open_or_create_map(level_subsystem):
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        log("Map exists, loading " + MAP_PATH)
        if not level_subsystem.load_level(MAP_PATH):
            fail("Could not load " + MAP_PATH)
        return False

    log("Creating " + MAP_PATH)
    if not level_subsystem.new_level(MAP_PATH):
        fail("Could not create " + MAP_PATH)
    return True


def find_actor(actor_subsystem, label):
    for actor in actor_subsystem.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def ensure_floor(actor_subsystem):
    if find_actor(actor_subsystem, FLOOR_LABEL):
        return False
    mesh = unreal.EditorAssetLibrary.load_asset(FLOOR_MESH)
    if mesh is None:
        fail("Engine mesh not found: " + FLOOR_MESH)
    floor = actor_subsystem.spawn_actor_from_object(mesh, unreal.Vector(0.0, 0.0, 0.0), unreal.Rotator(roll=0.0, pitch=0.0, yaw=0.0))
    if floor is None:
        fail("Could not spawn the floor")
    floor.set_actor_label(FLOOR_LABEL)
    floor.set_actor_scale3d(unreal.Vector(100.0, 100.0, 1.0))  # 100 m x 100 m
    return True


def ensure_player_start(actor_subsystem):
    if find_actor(actor_subsystem, PLAYER_START_LABEL):
        return False
    start = actor_subsystem.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0.0, 0.0, 100.0), unreal.Rotator(roll=0.0, pitch=0.0, yaw=0.0))
    if start is None:
        fail("Could not spawn the PlayerStart")
    start.set_actor_label(PLAYER_START_LABEL)
    return True


def ensure_sun(actor_subsystem):
    if find_actor(actor_subsystem, SUN_LABEL):
        return False
    sun = actor_subsystem.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0.0, 0.0, 500.0), unreal.Rotator(roll=0.0, pitch=-50.0, yaw=30.0))
    if sun is None:
        fail("Could not spawn the directional light")
    sun.set_actor_label(SUN_LABEL)
    return True


def main():
    level_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    if level_subsystem is None or actor_subsystem is None:
        fail("Editor subsystems are not available. Run this in the editor, not as a game.")

    created = open_or_create_map(level_subsystem)
    added = [
        name
        for name, was_added in (
            (FLOOR_LABEL, ensure_floor(actor_subsystem)),
            (PLAYER_START_LABEL, ensure_player_start(actor_subsystem)),
            (SUN_LABEL, ensure_sun(actor_subsystem)),
        )
        if was_added
    ]

    if created or added:
        if not level_subsystem.save_current_level():
            fail("Could not save " + MAP_PATH)
        log("Saved {} ({}; added: {})".format(MAP_PATH, "new map" if created else "existing map", ", ".join(added) or "nothing"))
    else:
        log("Nothing to do: {} already has all its actors".format(MAP_PATH))

    log("Done. Commit Content/RF/Maps/L_Test_Empty.umap (Git LFS).")


main()

if "--quit" in sys.argv[1:]:
    unreal.SystemLibrary.quit_editor()
