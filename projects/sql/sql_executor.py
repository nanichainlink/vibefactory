import sqlite3
import re

class SQLExecutor:
    """
    Clase para ejecutar consultas SQL de usuarios de forma segura y controlada.
    Utiliza SQLite como backend por su integración nativa con Python[4].
    """

    # Lista blanca de comandos permitidos (solo SELECT y consultas de lectura)
    ALLOWED_COMMANDS = {'SELECT', 'PRAGMA', 'EXPLAIN', 'WITH'}

    def __init__(self, db_path):
        self.db_path = db_path

    def is_safe_query(self, query):
        """
        Verifica si la consulta es segura:
        - Solo permite comandos en la lista blanca.
        - No permite múltiples sentencias ni comentarios.
        """
        # Elimina espacios iniciales y finales
        stripped = query.strip().upper()
        # Extrae el primer comando SQL
        first_word = stripped.split()[0]
        # Verifica si el comando está permitido
        if first_word not in self.ALLOWED_COMMANDS:
            return False
        # No permite punto y coma fuera del final (evita múltiples sentencias)
        if ';' in stripped[:-1]:
            return False
        # No permite comentarios SQL
        if '--' in stripped or '/*' in stripped or '*/' in stripped:
            return False
        return True

    def execute_query(self, query):
        """
        Ejecuta la consulta SQL si es segura.
        Devuelve los resultados o un mensaje de error controlado.
        """
        if not self.is_safe_query(query):
            return {
                "success": False,
                "error": "Consulta no permitida. Solo se permiten consultas de lectura (SELECT)."
            }
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                return {
                    "success": True,
                    "columns": columns,
                    "rows": rows
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error al ejecutar la consulta: {str(e)}"
            }