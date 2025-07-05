from levels import get_sql_levels

def print_levels():
    levels = get_sql_levels()
    for level in levels:
        print(f"Nivel {level.level}: {level.name}")
        for challenge in level.challenges:
            print(f"  - Reto {challenge.id}: {challenge.title}")
            print(f"    Descripción: {challenge.description}")
            print(f"    Objetivos: {', '.join(challenge.objectives)}")
            print(f"    SQL requerido: {', '.join(challenge.required_sql)}")
            print(f"    Ejemplo: {challenge.example_query}")
            print(f"    Pistas: {', '.join(challenge.hints)}")
        print()

if __name__ == "__main__":
    print_levels()