import random

class DifficultyAdjuster:
    """
    Ajusta la dificultad de los retos SQL según los resultados de las pruebas iniciales de los jugadores.
    """

    def __init__(self, retos):
        """
        retos: lista de diccionarios, cada uno con información del reto, incluyendo 'id', 'dificultad', 'aciertos', 'intentos'
        """
        self.retos = retos

    def ajustar_dificultad(self):
        """
        Ajusta la dificultad de cada reto en función de la tasa de éxito de los jugadores.
        """
        for reto in self.retos:
            tasa_exito = reto['aciertos'] / reto['intentos'] if reto['intentos'] > 0 else 0

            # Lógica de ajuste:
            # Si la tasa de éxito es muy alta, subir dificultad; si es muy baja, bajarla.
            if tasa_exito > 0.85 and reto['dificultad'] < 5:
                reto['dificultad'] += 1
            elif tasa_exito < 0.4 and reto['dificultad'] > 1:
                reto['dificultad'] -= 1
            # Si está en el rango medio, no cambiar dificultad

    def obtener_retos(self):
        return self.retos

    def seleccionar_reto_para_jugador(self, nivel_jugador):
        """
        Selecciona un reto adecuado al nivel del jugador.
        """
        retos_filtrados = [r for r in self.retos if r['dificultad'] == nivel_jugador]
        if retos_filtrados:
            return random.choice(retos_filtrados)
        # Si no hay retos exactos, buscar el más cercano
        return min(self.retos, key=lambda r: abs(r['dificultad'] - nivel_jugador))