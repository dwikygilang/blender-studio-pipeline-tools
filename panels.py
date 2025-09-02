import bpy
from . import db

class STUDIO_PT_shot_loader(bpy.types.Panel):
    bl_label = "Shot Loader"
    bl_idname = "STUDIO_PT_shot_loader"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Studio'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "studio_selected_artist", text="Artist")

        row = layout.row()
        row.operator("studio.reload_artists", text="Refresh Artists")
        row.operator("studio.reload_shots", text="Load Shots")

        layout.separator()

        if not db.shot_list_cache:
            layout.label(text="No shots assigned")
            return

        for shot_name, filepath in db.shot_list_cache:
            row = layout.row()
            row.label(text=shot_name)
            op = row.operator("studio.open_shot", text="Open")
            op.filepath = filepath

def register():
    bpy.utils.register_class(STUDIO_PT_shot_loader)

def unregister():
    bpy.utils.unregister_class(STUDIO_PT_shot_loader)
