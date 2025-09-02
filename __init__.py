bl_info = {
    "name": "Roleplay Studio",
    "author": "Dwiky Gilang I",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Studio",
    "description": "Addon for load shot assigned artist from local database",
    "category": "Pipeline",
}

import bpy

# Import modul internal
from . import preferences, db, operators, panels, props

modules = (preferences, db, operators, panels, props)

def register():
    for m in modules:
        if hasattr(m, "register"):
            m.register()

def unregister():
    for m in reversed(modules):
        if hasattr(m, "unregister"):
            m.unregister()

if __name__ == "__main__":
    register()
