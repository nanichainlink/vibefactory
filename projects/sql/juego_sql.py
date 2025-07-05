import sqlite3
import random

# Función para crear una conexión a la base de datos
def crear_conexion(db_name):
    """Crea una conexión a una base de datos SQLite."""
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para crear una tabla de ejemplo
def crear_tabla(conn):
    """Crea una tabla de ejemplo en la base de datos."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    """)
    conn.commit()

# Función para insertar datos de ejemplo
def insertar_datos(conn):
    """Inserta algunos datos de ejemplo en la tabla."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO empleados (nombre, edad) VALUES ('Juan', 30)")
    cursor.execute("INSERT INTO empleados (nombre, edad) VALUES ('Ana', 25)")
    cursor.execute("INSERT INTO empleados (nombre, edad) VALUES ('Pedro', 40)")
    conn.commit()

# Función para generar preguntas SQL
def generar_pregunta(conn):
    """Genera una pregunta SQL aleatoria."""
    preguntas = [
        ("SELECT * FROM empleados WHERE edad > 30", "¿Cuáles empleados tienen más de 30 años?"),
        ("SELECT nombre FROM empleados WHERE edad = 25", "¿Cuál es el nombre del empleado de 25 años?"),
        ("SELECT COUNT(*) FROM empleados", "¿Cuántos empleados hay en total?")
    ]
    pregunta, texto_pregunta = random.choice(preguntas)
    return pregunta, texto_pregunta

# Función para evaluar la respuesta del usuario
def evaluar_respuesta(conn, pregunta, respuesta_usuario):
    """Evalúa si la respuesta del usuario es correcta."""
    cursor = conn.cursor()
    cursor.execute(pregunta)
    respuesta_correcta = cursor.fetchall()
    # Simula la respuesta del usuario como si fuera una consulta SQL
    try:
        cursor.execute(respuesta_usuario)
        respuesta_usuario = cursor.fetchall()
    except sqlite3.Error:
        return False
    
    return respuesta_correcta == respuesta_usuario

# Función principal del juego
def jugar_juego():
    db_name = "juego_sql.db"
    conn = crear_conexion(db_name)
    
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return
    
    crear_tabla(conn)
    insertar_datos(conn)
    
    while True:
        pregunta, texto_pregunta = generar_pregunta(conn)
        print(f"\nPregunta: {texto_pregunta}")
        respuesta_usuario = input("Ingrese su respuesta (SQL): ")
        
        if evaluar_respuesta(conn, pregunta, respuesta_usuario):
            print("¡Correcto!")
        else:
            print("Incorrecto. La respuesta correcta es:")
            cursor = conn.cursor()
            cursor.execute(pregunta)
            print(cursor.fetchall())
        
        jugar_de_nuevo = input("¿Desea jugar de nuevo? (S/N): ")
        if jugar_de_nuevo.upper() != "S":
            break
    
    conn.close()

if __name__ == "__main__":
    jugar_juego()