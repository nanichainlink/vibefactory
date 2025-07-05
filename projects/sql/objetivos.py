# objetivos.py

"""
Definición de los objetivos principales para el juego educativo de SQL.
Este módulo puede ser utilizado por otros componentes del proyecto para mostrar,
evaluar o modificar los objetivos del juego.
"""

from typing import List, Dict

def obtener_objetivos_principales() -> List[Dict[str, str]]:
    """
    Devuelve una lista de los objetivos principales del juego SQL.

    Returns:
        List[Dict[str, str]]: Lista de objetivos, cada uno con 'titulo' y 'descripcion'.
    """
    objetivos = [
        {
            "titulo": "Enseñar SQL de forma interactiva",
            "descripcion": (
                "Facilitar el aprendizaje del lenguaje SQL mediante retos prácticos y situaciones de juego, "
                "permitiendo que los jugadores resuelvan problemas reales y reciban retroalimentación inmediata."
            )
        },
        {
            "titulo": "Gamificación del aprendizaje",
            "descripcion": (
                "Motivar a los estudiantes a través de mecánicas de juego como niveles, recompensas y desafíos, "
                "aumentando el compromiso y la retención del conocimiento."
            )
        },
        {
            "titulo": "Desarrollar habilidades de resolución de problemas",
            "descripcion": (
                "Fomentar el pensamiento lógico y la capacidad de análisis al enfrentar a los jugadores a retos "
                "que requieren diseñar y optimizar consultas SQL para avanzar en el juego."
            )
        },
        {
            "titulo": "Evaluación personalizada y seguimiento del progreso",
            "descripcion": (
                "Ofrecer diagnósticos personalizados sobre el desempeño del estudiante, identificando fortalezas "
                "y áreas de mejora para adaptar el contenido y reforzar el aprendizaje donde sea necesario."
            )
        },
        {
            "titulo": "Promover el aprendizaje autónomo y colaborativo",
            "descripcion": (
                "Permitir que los jugadores avancen a su propio ritmo y, opcionalmente, colaboren o compitan con otros, "
                "favoreciendo tanto el autoaprendizaje como el trabajo en equipo."
            )
        }
    ]
    return objetivos

if __name__ == "__main__":
    # Ejemplo de uso: mostrar los objetivos principales
    objetivos = obtener_objetivos_principales()
    for idx, obj in enumerate(objetivos, 1):
        print(f"{idx}. {obj['titulo']}\n   {obj['descripcion']}\n")