import bpy
from . import db

def register():
    bpy.types.Scene.studio_selected_artist = bpy.props.EnumProperty(
        name="Artist",
        description="Pilih artist",
        items=lambda self, context: [(a, a, "") for a in db.artist_list_cache] or [("", "No Artist", "")]
    )
    db.get_artists()

def unregister():
    del bpy.types.Scene.studio_selected_artist
