"""Scene setup: an empty scene in metric units with unit scale 1.0 (1 Blender unit = 1 m = 100 UU)."""
import bpy


def setup_units(scene=None):
    scene = scene or bpy.context.scene
    us = scene.unit_settings
    us.system = 'METRIC'
    us.scale_length = 1.0
    us.length_unit = 'CENTIMETERS'   # display only; geometry is authored in metres
    us.mass_unit = 'KILOGRAMS'
    return scene


def reset_scene():
    """Start from an empty factory scene (no default cube, camera or light)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Never write .blend1 backups next to the sources.
    bpy.context.preferences.filepaths.save_version = 0
    return setup_units(bpy.context.scene)


def new_collection(name, scene=None):
    scene = scene or bpy.context.scene
    col = bpy.data.collections.new(name)
    scene.collection.children.link(col)
    return col


def check_units(scene=None):
    """Return a list of problems with the scene unit setup (empty when correct)."""
    scene = scene or bpy.context.scene
    us = scene.unit_settings
    errors = []
    if us.system != 'METRIC':
        errors.append(f"unit system is {us.system}, expected METRIC")
    if abs(us.scale_length - 1.0) > 1e-9:
        errors.append(f"unit scale is {us.scale_length}, expected 1.0")
    return errors
