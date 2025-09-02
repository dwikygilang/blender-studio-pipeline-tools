import bpy

class StudioAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    db_host: bpy.props.StringProperty(name="Host", default="localhost")
    user_host: bpy.props.StringProperty(name="Username", default="urPostgresqlUsername")
    password_host: bpy.props.StringProperty(name="Password", default="urPassword")
    db_name_host: bpy.props.StringProperty(name="Database", default="urDatabase")
    db_port_host: bpy.props.StringProperty(name="Port", default="5432")

    def draw(self, context):
        layout = self.layout
        layout.label(text="Database Settings")
        layout.prop(self, "db_host")
        layout.prop(self, "user_host")
        layout.prop(self, "password_host")
        layout.prop(self, "db_name_host")
        layout.prop(self, "db_port_host")

def register():
    bpy.utils.register_class(StudioAddonPreferences)

def unregister():
    bpy.utils.unregister_class(StudioAddonPreferences)
