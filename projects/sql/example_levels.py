"""
Módulo: example_levels.py

Define ejemplos de niveles y retos para el juego de aprendizaje de SQL.
"""

from mechanics import SQLChallenge, Level

# Ejemplo de retos básicos
challenge1 = SQLChallenge(
    description="Selecciona todos los nombres de la tabla 'usuarios'.",
    solution_query="SELECT nombre FROM usuarios;",
    test_cases=[{'input': None, 'expected_output': [('Ana',), ('Luis',), ('Carlos',)]}],
    hint="Usa SELECT y FROM."
)

challenge2 = SQLChallenge(
    description="Selecciona los usuarios mayores de 18 años.",
    solution_query="SELECT nombre FROM usuarios WHERE edad > 18;",
    test_cases=[{'input': None, 'expected_output': [('Luis',), ('Carlos',)]}],
    hint="Recuerda la cláusula WHERE."
)

level1 = Level(
    name="Consultas Básicas",
    challenges=[challenge1, challenge2]
)

# Puedes definir más niveles y retos avanzados aquí

LEVELS = [level1]