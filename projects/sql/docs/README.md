import sqlite3

conn = sqlite3.connect("sqlgame.db")
cursor = conn.cursor()
# Ejemplo: Crear una tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS jugadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    puntaje INTEGER DEFAULT 0
)
""")
conn.commit()