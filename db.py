import pg8000, bpy, os

DEFAULT_DB_CONFIG = {
    "user": "urPostgresqlUsername",
    "password": "urPassword",
    "host": "localhost",
    "port": 5432,
    "database": "urDatabase"
}

shot_list_cache = []
artist_list_cache = []

def get_db_config(context):
    prefs = context.preferences.addons[__package__].preferences
    return {
        "user": prefs.user_host or DEFAULT_DB_CONFIG["user"],
        "password": prefs.password_host or DEFAULT_DB_CONFIG["password"],
        "host": prefs.db_host or DEFAULT_DB_CONFIG["host"],
        "port": int(prefs.db_port_host or DEFAULT_DB_CONFIG["port"]),
        "database": prefs.db_name_host or DEFAULT_DB_CONFIG["database"],
    }

def get_artists(context=None):
    global artist_list_cache
    try:
        cfg = get_db_config(bpy.context if context is None else context)
        conn = pg8000.connect(**cfg)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT artist FROM shot_assignments ORDER BY artist;")
        rows = [r[0] for r in cur.fetchall()]
        cur.close(); conn.close()
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
        cur.close(); conn.close()
        shot_list_cache = rows
        return rows
    except Exception as e:
        print("DB Error:", e)
        return []
