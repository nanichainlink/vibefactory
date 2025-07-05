"""
Módulo: game_mechanics.py

Este módulo define y documenta las mecánicas de juego básicas para un 'SQL Game'.
Incluye la estructura de niveles, puntos, recompensas y retroalimentación inmediata.
"""

from enum import Enum, auto
from typing import List, Dict, Optional

class FeedbackType(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    HINT = auto()
    LEVEL_UP = auto()

class RewardType(Enum):
    BADGE = auto()
    EXTRA_POINTS = auto()
    UNLOCK_LEVEL = auto()

class GameLevel:
    """
    Representa un nivel del juego.
    """
    def __init__(self, level_number: int, description: str, points_to_pass: int):
        self.level_number = level_number
        self.description = description
        self.points_to_pass = points_to_pass

class Player:
    """
    Representa a un jugador y su progreso.
    """
    def __init__(self, username: str):
        self.username = username
        self.current_level = 1
        self.points = 0
        self.rewards: List[RewardType] = []

    def add_points(self, amount: int):
        self.points += amount

    def add_reward(self, reward: RewardType):
        self.rewards.append(reward)

    def level_up(self):
        self.current_level += 1

class GameMechanics:
    """
    Clase principal que gestiona las mecánicas de juego.
    """
    def __init__(self, levels: List[GameLevel]):
        self.levels = {level.level_number: level for level in levels}

    def give_feedback(self, feedback_type: FeedbackType, extra: Optional[str] = None) -> str:
        """
        Proporciona retroalimentación inmediata al jugador.
        """
        feedback_messages = {
            FeedbackType.CORRECT: "¡Respuesta correcta! +10 puntos.",
            FeedbackType.INCORRECT: "Respuesta incorrecta. Intenta de nuevo.",
            FeedbackType.HINT: f"Pista: {extra}" if extra else "Aquí tienes una pista.",
            FeedbackType.LEVEL_UP: "¡Felicidades! Has subido de nivel."
        }
        return feedback_messages[feedback_type]

    def check_level_up(self, player: Player) -> bool:
        """
        Verifica si el jugador puede subir de nivel.
        """
        current_level = self.levels.get(player.current_level)
        if current_level and player.points >= current_level.points_to_pass:
            player.level_up()
            return True
        return False

    def assign_reward(self, player: Player, reward: RewardType):
        """
        Asigna una recompensa al jugador.
        """
        player.add_reward(reward)

# Ejemplo de definición de niveles
LEVELS = [
    GameLevel(1, "Introducción a SELECT y consultas básicas.", 20),
    GameLevel(2, "Consultas con condiciones WHERE.", 40),
    GameLevel(3, "Consultas con JOIN y funciones agregadas.", 60),
]

# Documentación de mecánicas de juego
GAME_MECHANICS_DOC = {
    "niveles": [
        {
            "numero": level.level_number,
            "descripcion": level.description,
            "puntos_para_avanzar": level.points_to_pass
        } for level in LEVELS
    ],
    "puntos": "Los jugadores obtienen puntos por cada respuesta correcta. Los puntos acumulados permiten avanzar de nivel.",
    "recompensas": [
        "Insignias (BADGE) por completar niveles.",
        "Puntos extra (EXTRA_POINTS) por respuestas rápidas o consecutivas.",
        "Desbloqueo de niveles (UNLOCK_LEVEL) al alcanzar ciertos hitos."
    ],
    "retroalimentacion_inmediata": [
        "Mensaje inmediato tras cada respuesta: correcta o incorrecta.",
        "Pistas disponibles tras errores consecutivos.",
        "Notificación de subida de nivel."
    ]
}