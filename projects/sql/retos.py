# retos.py

from typing import List, Dict

class SQLChallenge:
    def __init__(self, nivel: int, instrucciones: str, datos_iniciales: List[str], solucion_esperada: List[Dict]):
        self.nivel = nivel
        self.instrucciones = instrucciones
        self.datos_iniciales = datos_iniciales
        self.solucion_esperada = solucion_esperada

def obtener_retos_iniciales() -> List[SQLChallenge]:
    """
    Devuelve una lista con los primeros retos del juego SQL.
    Cada reto contiene instrucciones, datos iniciales y la solución esperada.
    """
    retos = []

    # Nivel 1: Selección básica
    instrucciones_1 = (
        "Nivel 1: Selecciona todos los registros de la tabla 'Canciones'.\n"
        "Utiliza la instrucción SELECT adecuada para mostrar todas las columnas y filas."
    )
    datos_iniciales_1 = [
        "CREATE TABLE Canciones (titulo TEXT, reproducciones INTEGER);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Imagine', 150);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Yesterday', 200);"
    ]
    solucion_esperada_1 = [
        {"titulo": "Imagine", "reproducciones": 150},
        {"titulo": "Yesterday", "reproducciones": 200}
    ]
    retos.append(SQLChallenge(1, instrucciones_1, datos_iniciales_1, solucion_esperada_1))

    # Nivel 2: Filtro con WHERE
    instrucciones_2 = (
        "Nivel 2: Selecciona las canciones con más de 160 reproducciones.\n"
        "Utiliza la cláusula WHERE para filtrar los resultados."
    )
    datos_iniciales_2 = [
        "CREATE TABLE Canciones (titulo TEXT, reproducciones INTEGER);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Imagine', 150);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Yesterday', 200);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Hey Jude', 180);"
    ]
    solucion_esperada_2 = [
        {"titulo": "Yesterday", "reproducciones": 200},
        {"titulo": "Hey Jude", "reproducciones": 180}
    ]
    retos.append(SQLChallenge(2, instrucciones_2, datos_iniciales_2, solucion_esperada_2))

    # Nivel 3: Selección de columnas específicas
    instrucciones_3 = (
        "Nivel 3: Muestra únicamente los títulos de todas las canciones.\n"
        "Debes seleccionar solo la columna 'titulo'."
    )
    datos_iniciales_3 = [
        "CREATE TABLE Canciones (titulo TEXT, reproducciones INTEGER);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Imagine', 150);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Yesterday', 200);",
        "INSERT INTO Canciones (titulo, reproducciones) VALUES ('Hey Jude', 180);"
    ]
    solucion_esperada_3 = [
        {"titulo": "Imagine"},
        {"titulo": "Yesterday"},
        {"titulo": "Hey Jude"}
    ]
    retos.append(SQLChallenge(3, instrucciones_3, datos_iniciales_3, solucion_esperada_3))

    return retos