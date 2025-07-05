"""
Módulo: mechanics.py

Define las mecánicas básicas del juego para aprender SQL.
Incluye la estructura de retos, niveles y validación de consultas SQL.
"""

from typing import List, Dict, Any, Optional

class SQLChallenge:
    """
    Representa un reto individual que el jugador debe resolver escribiendo una consulta SQL.
    """
    def __init__(self, description: str, solution_query: str, test_cases: List[Dict[str, Any]], hint: Optional[str] = None):
        self.description = description
        self.solution_query = solution_query
        self.test_cases = test_cases  # Cada test_case tiene 'input' y 'expected_output'
        self.hint = hint

    def check_solution(self, user_query: str, db_connection) -> bool:
        """
        Ejecuta la consulta del usuario y compara con los resultados esperados.
        """
        try:
            cursor = db_connection.cursor()
            cursor.execute(user_query)
            user_result = cursor.fetchall()
            # Compara con todos los casos de prueba
            for case in self.test_cases:
                if user_result != case['expected_output']:
                    return False
            return True
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False

class Level:
    """
    Un nivel agrupa varios retos relacionados con un tema o dificultad.
    """
    def __init__(self, name: str, challenges: List[SQLChallenge]):
        self.name = name
        self.challenges = challenges

    def get_next_challenge(self, current_index: int) -> Optional[SQLChallenge]:
        if current_index + 1 < len(self.challenges):
            return self.challenges[current_index + 1]
        return None

class Game:
    """
    Controla la progresión del jugador a través de los niveles y retos.
    """
    def __init__(self, levels: List[Level]):
        self.levels = levels
        self.current_level = 0
        self.current_challenge = 0

    def get_current_challenge(self) -> SQLChallenge:
        return self.levels[self.current_level].challenges[self.current_challenge]

    def advance(self):
        """
        Avanza al siguiente reto o nivel.
        """
        if self.current_challenge + 1 < len(self.levels[self.current_level].challenges):
            self.current_challenge += 1
        elif self.current_level + 1 < len(self.levels):
            self.current_level += 1
            self.current_challenge = 0
        else:
            print("¡Juego completado!")

    def reset(self):
        self.current_level = 0
        self.current_challenge = 0