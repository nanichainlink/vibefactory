from difficulty_adjuster import DifficultyAdjuster

# Simulación de retos con resultados de pruebas iniciales
retos = [
    {'id': 1, 'dificultad': 2, 'aciertos': 18, 'intentos': 20},
    {'id': 2, 'dificultad': 3, 'aciertos': 5, 'intentos': 20},
    {'id': 3, 'dificultad': 4, 'aciertos': 10, 'intentos': 20},
    {'id': 4, 'dificultad': 1, 'aciertos': 1, 'intentos': 20},
    {'id': 5, 'dificultad': 5, 'aciertos': 19, 'intentos': 20},
]

ajustador = DifficultyAdjuster(retos)
ajustador.ajustar_dificultad()

print("Retos ajustados:")
for reto in ajustador.obtener_retos():
    print(f"Reto {reto['id']}: dificultad {reto['dificultad']} (aciertos: {reto['aciertos']}, intentos: {reto['intentos']})")

# Ejemplo de selección de reto para un jugador de nivel 3
reto_para_jugador = ajustador.seleccionar_reto_para_jugador(3)
print(f"\nReto sugerido para jugador de nivel 3: {reto_para_jugador}")