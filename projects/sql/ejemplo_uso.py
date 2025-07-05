from sql_validation import validate_sql_answer

# Configuración de conexión (ajustar según tu entorno)
db_config = {
    "user": "usuario",
    "password": "contraseña",
    "host": "localhost",
    "port": 1433,
    "database": "mi_base",
    "driver": "ODBC+Driver+17+for+SQL+Server"
}

user_query = "SELECT nombre, edad FROM empleados WHERE edad > 30"
solution_query = "SELECT nombre, edad FROM empleados WHERE edad > 30"

es_valido, mensaje = validate_sql_answer(db_config, user_query, solution_query)

if es_valido:
    print("✅ Respuesta correcta")
else:
    print("❌ Respuesta incorrecta:")
    print(mensaje)