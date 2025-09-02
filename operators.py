import bpy, os
from . import db

class STUDIO_OT_reload_artists(bpy.types.Operator):
    bl_idname = "studio.reload_artists"
    bl_label = "Reload Artists"

    def execute(self, context):
        db.get_artists(context)
        self.report({'INFO'}, "Artist list updated")
        return {'FINISHED'}

class STUDIO_OT_reload_shots(bpy.types.Operator):
    bl_idname = "studio.reload_shots"
    bl_label = "Reload Shots"

    def execute(self, context):
        artist = context.scene.studio_selected_artist
        if artist:
            db.get_assigned_shots(artist, context)
            self.report({'INFO'}, f"Shot list updated for {artist}")
        else:
            self.report({'WARNING'}, "No artist selected")
        return {'FINISHED'}

class STUDIO_OT_open_shot(bpy.types.Operator):
    bl_idname = "studio.open_shot"
    bl_label = "Open Shot"

    filepath: bpy.props.StringProperty()

    def execute(self, context):
        if os.path.exists(self.filepath):
            bpy.ops.wm.open_mainfile(filepath=self.filepath)
        else:
            self.report({'ERROR'}, f"File not found: {self.filepath}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(STUDIO_OT_reload_artists)
    bpy.utils.register_class(STUDIO_OT_reload_shots)
    bpy.utils.register_class(STUDIO_OT_open_shot)

def unregister():
    bpy.utils.unregister_class(STUDIO_OT_reload_artists)
    bpy.utils.unregister_class(STUDIO_OT_reload_shots)
    bpy.utils.unregister_class(STUDIO_OT_open_shot)
