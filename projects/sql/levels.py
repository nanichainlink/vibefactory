from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class SQLChallenge:
    id: int
    title: str
    description: str
    objectives: List[str]
    required_sql: List[str]
    example_query: Optional[str] = None
    hints: List[str] = field(default_factory=list)

@dataclass
class SQLLevel:
    level: int
    name: str
    challenges: List[SQLChallenge]

def get_sql_levels() -> List[SQLLevel]:
    """
    Devuelve la estructura progresiva de niveles y retos para el juego de aprendizaje de SQL.
    """
    return [
        SQLLevel(
            level=1,
            name="Consultas Básicas",
            challenges=[
                SQLChallenge(
                    id=1,
                    title="Primer SELECT",
                    description="Realiza una consulta SELECT para mostrar todos los datos de la tabla 'usuarios'.",
                    objectives=["Aprender la sintaxis básica de SELECT", "Obtener todas las columnas"],
                    required_sql=["SELECT"],
                    example_query="SELECT * FROM usuarios;",
                    hints=["Recuerda usar * para seleccionar todas las columnas."]
                ),
                SQLChallenge(
                    id=2,
                    title="Filtrar con WHERE",
                    description="Selecciona los usuarios cuyo país sea 'España'.",
                    objectives=["Filtrar filas con WHERE"],
                    required_sql=["SELECT", "WHERE"],
                    example_query="SELECT * FROM usuarios WHERE pais = 'España';",
                    hints=["WHERE sirve para filtrar filas según una condición."]
                ),
            ]
        ),
        SQLLevel(
            level=2,
            name="Consultas Intermedias",
            challenges=[
                SQLChallenge(
                    id=3,
                    title="Ordenar resultados",
                    description="Muestra todos los productos ordenados por precio de mayor a menor.",
                    objectives=["Ordenar resultados con ORDER BY"],
                    required_sql=["ORDER BY", "DESC"],
                    example_query="SELECT * FROM productos ORDER BY precio DESC;",
                    hints=["ORDER BY permite ordenar los resultados.", "DESC es para descendente."]
                ),
                SQLChallenge(
                    id=4,
                    title="Limitar resultados",
                    description="Muestra los 5 usuarios más recientes.",
                    objectives=["Limitar resultados con LIMIT"],
                    required_sql=["LIMIT", "ORDER BY"],
                    example_query="SELECT * FROM usuarios ORDER BY fecha_registro DESC LIMIT 5;",
                    hints=["LIMIT restringe la cantidad de filas devueltas."]
                ),
            ]
        ),
        SQLLevel(
            level=3,
            name="Agregaciones y Agrupaciones",
            challenges=[
                SQLChallenge(
                    id=5,
                    title="Contar filas",
                    description="Cuenta cuántos usuarios hay en la tabla.",
                    objectives=["Usar funciones de agregación (COUNT)"],
                    required_sql=["COUNT"],
                    example_query="SELECT COUNT(*) FROM usuarios;",
                    hints=["COUNT(*) cuenta todas las filas."]
                ),
                SQLChallenge(
                    id=6,
                    title="Agrupar por columna",
                    description="Muestra cuántos usuarios hay por país.",
                    objectives=["Agrupar resultados con GROUP BY"],
                    required_sql=["GROUP BY", "COUNT"],
                    example_query="SELECT pais, COUNT(*) FROM usuarios GROUP BY pais;",
                    hints=["GROUP BY agrupa los resultados por el valor de una columna."]
                ),
            ]
        ),
        SQLLevel(
            level=4,
            name="Consultas Avanzadas: JOIN",
            challenges=[
                SQLChallenge(
                    id=7,
                    title="JOIN básico",
                    description="Muestra el nombre del usuario y el nombre de su país usando JOIN entre 'usuarios' y 'paises'.",
                    objectives=["Unir tablas con INNER JOIN"],
                    required_sql=["JOIN", "ON"],
                    example_query="SELECT usuarios.nombre, paises.nombre FROM usuarios JOIN paises ON usuarios.pais_id = paises.id;",
                    hints=["JOIN permite combinar filas de dos tablas."]
                ),
                SQLChallenge(
                    id=8,
                    title="LEFT JOIN",
                    description="Muestra todos los usuarios y, si existe, el nombre de su país.",
                    objectives=["Entender LEFT JOIN"],
                    required_sql=["LEFT JOIN"],
                    example_query="SELECT usuarios.nombre, paises.nombre FROM usuarios LEFT JOIN paises ON usuarios.pais_id = paises.id;",
                    hints=["LEFT JOIN devuelve todas las filas de la tabla izquierda."]
                ),
            ]
        ),
        SQLLevel(
            level=5,
            name="Consultas Avanzadas: Subconsultas y Funciones",
            challenges=[
                SQLChallenge(
                    id=9,
                    title="Subconsulta en WHERE",
                    description="Muestra los productos cuyo precio es mayor que el precio medio.",
                    objectives=["Usar subconsultas en WHERE"],
                    required_sql=["SELECT", "WHERE", "AVG"],
                    example_query="SELECT * FROM productos WHERE precio > (SELECT AVG(precio) FROM productos);",
                    hints=["Puedes usar una consulta SELECT dentro de WHERE."]
                ),
                SQLChallenge(
                    id=10,
                    title="Funciones de cadena",
                    description="Muestra los nombres de usuario en mayúsculas.",
                    objectives=["Aplicar funciones de cadena como UPPER"],
                    required_sql=["UPPER"],
                    example_query="SELECT UPPER(nombre) FROM usuarios;",
                    hints=["UPPER convierte texto a mayúsculas."]
                ),
            ]
        ),
    ]