def listar_tipos_ejercicios():
    """
    Devuelve una lista de los tipos de ejercicios SQL definidos para el juego.
    """
    from exercise_types import EXERCISE_TYPES
    return [
        {
            "nombre": tipo["nombre"],
            "descripcion": tipo["descripcion"]
        }
        for tipo in EXERCISE_TYPES
    ]

def mostrar_ejemplo(tipo_nombre):
    """
    Dado el nombre de un tipo de ejercicio, muestra un ejemplo SQL asociado.
    """
    from exercise_types import EXERCISE_TYPES
    for tipo in EXERCISE_TYPES:
        if tipo["nombre"] == tipo_nombre:
            return tipo["ejemplo"]
    return None