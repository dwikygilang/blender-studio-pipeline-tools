bl_info = {
    "name": "Roleplay Studio",
    "author": "Dwiky Gilang I",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Studio",
    "description": "Addon for load shot assigned artist from local database",
    # "wiki_url": "https://github.com/dwiky/roleplay_studio/wiki",
    "category": "Pipeline",
}

import sys, os, bpy, getpass

# ===============================
# PATH LIBS
# ===============================
sys.path.append(os.path.dirname(__file__))
libs_path = os.path.join(os.path.dirname(__file__), "libs")
if libs_path not in sys.path:
    sys.path.append(libs_path)
import pg8000
import bpy

# ===============================
# CONFIG DEFAULT
# ===============================
DEFAULT_DB_CONFIG = {
    "user": "urPostgresqlUsername",
    "password": "urPassword",
    "host": "localhost",  # default host
    "port": 5432,
    "database": "urDatabase"
}


def get_db_config(context):
    """Get config from Addon Preferences"""
    prefs = context.preferences.addons[__name__].preferences
    return {
        "user": prefs.user_host or DEFAULT_DB_CONFIG["user"],
        "password": prefs.password_host or DEFAULT_DB_CONFIG["password"],
        "host": prefs.db_host or DEFAULT_DB_CONFIG["host"],
        "port": int(prefs.db_port_host or DEFAULT_DB_CONFIG["port"]),
        "database": prefs.db_name_host or DEFAULT_DB_CONFIG["database"],
    }

# ===============================
# CACHE
# ===============================
shot_list_cache = []
artist_list_cache = []

# ===============================
# DB FUNCTIONS
# ===============================
def get_artists(context=None):
    global artist_list_cache
    try:
        cfg = get_db_config(bpy.context if context is None else context)
        conn = pg8000.connect(**cfg)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT artist FROM shot_assignments ORDER BY artist;")
        rows = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        artist_list_cache = rows
        return rows
    except Exception as e:
        print("DB Error:", e)
        return []


def get_assigned_shots(artist_name, context=None):
    global shot_list_cache
    try:
        cfg = get_db_config(bpy.context if context is None else context)
        conn = pg8000.connect(**cfg)
        cur = conn.cursor()
        cur.execute("""
            SELECT shot_name, file_path
            FROM shot_assignments
            WHERE artist = %s
            ORDER BY shot_name;
        """, (artist_name,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        shot_list_cache = rows
        return rows
    except Exception as e:
        print("DB Error:", e)
        return []


# ===============================
# ADDON PREFERENCES
# ===============================
class StudioAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    db_host: bpy.props.StringProperty(
        name="Host",
        description="Address host PostgreSQL",
        default="localhost"
    )
    
    user_host: bpy.props.StringProperty(
        name="Username",
        description="Username PostgreSQL",
        default="urPostgresqlUsername"
    )
    
    password_host: bpy.props.StringProperty(
        name="Password",
        description="Password PostgreSQL",
        default="urPassword"
    )
    
    db_name_host: bpy.props.StringProperty(
        name="Database",
        description="Database PostgreSQL",
        default="urDatabase"
    )
    
    db_port_host: bpy.props.StringProperty(
        name="Port",
        description="Port PostgreSQL",
        default="5432"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Database Settings")
        layout.prop(self, "db_host")
        layout.prop(self, "user_host")
        layout.prop(self, "password_host")
        layout.prop(self, "db_name_host")
        layout.prop(self, "db_port_host")

# ===============================
# OPERATORS
# ===============================
class STUDIO_OT_reload_artists(bpy.types.Operator):
    bl_idname = "studio.reload_artists"
    bl_label = "Reload Artists"

    def execute(self, context):
        get_artists(context)
        self.report({'INFO'}, "Artist list updated")
        return {'FINISHED'}


class STUDIO_OT_reload_shots(bpy.types.Operator):
    bl_idname = "studio.reload_shots"
    bl_label = "Reload Shots"

    def execute(self, context):
        artist = context.scene.studio_selected_artist
        if artist:
            get_assigned_shots(artist, context)
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


# ===============================
# PANEL
# ===============================
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

        if not shot_list_cache:
            layout.label(text="No shots assigned")
            return

        for shot_name, filepath in shot_list_cache:
            row = layout.row()
            row.label(text=shot_name)
            op = row.operator("studio.open_shot", text="Open")
            op.filepath = filepath


# ===============================
# REGISTER
# ===============================
classes = [
    StudioAddonPreferences,
    STUDIO_OT_reload_artists,
    STUDIO_OT_reload_shots,
    STUDIO_OT_open_shot,
    STUDIO_PT_shot_loader,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.studio_selected_artist = bpy.props.EnumProperty(
        name="Artist",
        description="Pilih artist",
        items=lambda self, context: [(a, a, "") for a in artist_list_cache] or [("", "No Artist", "")]
    )

    get_artists()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.studio_selected_artist


if __name__ == "__main__":
    register()
