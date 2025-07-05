"""
target_audience.py

Este módulo identifica el público objetivo para un juego educativo cuyo fin es enseñar SQL.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class TargetAudience:
    description: str
    needs: List[str]
    motivations: List[str]
    prior_knowledge: str

def get_target_audience() -> TargetAudience:
    """
    Devuelve la definición del público objetivo para un juego de aprendizaje de SQL.
    """
    return TargetAudience(
        description=(
            "Estudiantes principiantes en bases de datos, especialmente de informática, ingeniería, "
            "o áreas afines, que desean aprender SQL de forma interactiva y lúdica."
        ),
        needs=[
            "Introducción amigable a los conceptos fundamentales de SQL",
            "Superar la frustración inicial y las barreras de aprendizaje de la sintaxis y lógica de SQL",
            "Ejercitar la resolución de retos prácticos con retroalimentación inmediata",
            "Aprender de manera autónoma y a su propio ritmo"
        ],
        motivations=[
            "Interés en adquirir habilidades prácticas en bases de datos relacionales",
            "Mejorar el desempeño académico o profesional",
            "Prepararse para proyectos, prácticas o el mercado laboral",
            "Aprender mediante el juego y la experimentación"
        ],
        prior_knowledge=(
            "No se requiere experiencia previa en SQL, pero es recomendable tener conocimientos básicos "
            "de informática y lógica de programación."
        )
    )

if __name__ == "__main__":
    audience = get_target_audience()
    print("Descripción del público objetivo:")
    print(audience.description)
    print("\nNecesidades:")
    for need in audience.needs:
        print(f"- {need}")
    print("\nMotivaciones:")
    for motivation in audience.motivations:
        print(f"- {motivation}")
    print("\nConocimientos previos recomendados:")
    print(audience.prior_knowledge)