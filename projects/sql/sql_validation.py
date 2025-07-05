import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from typing import Any, Dict, Tuple

def get_db_engine(db_config: Dict[str, Any]) -> sqlalchemy.engine.Engine:
    """
    Crea un engine de SQLAlchemy para conectarse a la base de datos.
    db_config debe contener: user, password, host, port, database, driver.
    """
    # Ejemplo para SQL Server con pyodbc
    conn_str = (
        f"mssql+pyodbc://{db_config['user']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config['port']}/{db_config['database']}?"
        f"driver={db_config['driver']}"
    )
    return create_engine(conn_str)

def execute_query(engine: sqlalchemy.engine.Engine, query: str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL y devuelve el resultado como DataFrame.
    """
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza el DataFrame para comparación:
    - Ordena columnas alfabéticamente
    - Ordena filas por todas las columnas
    - Resetea índices
    - Convierte todos los valores a string para evitar problemas de tipos
    """
    df = df.copy()
    df = df[sorted(df.columns)]
    df = df.sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.astype(str)

def compare_results(user_df: pd.DataFrame, solution_df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Compara dos DataFrames normalizados.
    Devuelve (True, "") si son iguales, (False, mensaje de error) si no.
    """
    user_norm = normalize_df(user_df)
    sol_norm = normalize_df(solution_df)
    if user_norm.equals(sol_norm):
        return True, ""
    else:
        diff_user = user_norm[~user_norm.apply(tuple, 1).isin(sol_norm.apply(tuple, 1))]
        diff_sol = sol_norm[~sol_norm.apply(tuple, 1).isin(user_norm.apply(tuple, 1))]
        msg = (
            f"Diferencias encontradas:\n"
            f"En respuesta del usuario y no en la solución:\n{diff_user}\n\n"
            f"En la solución y no en la respuesta del usuario:\n{diff_sol}"
        )
        return False, msg

def validate_sql_answer(
    db_config: Dict[str, Any],
    user_query: str,
    solution_query: str
) -> Tuple[bool, str]:
    """
    Valida la respuesta SQL del usuario comparando el resultado con la solución esperada.
    """
    engine = get_db_engine(db_config)
    user_df = execute_query(engine, user_query)
    solution_df = execute_query(engine, solution_query)
    return compare_results(user_df, solution_df)