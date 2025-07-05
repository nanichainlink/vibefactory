# Definición de los tipos de ejercicios y retos SQL para el proyecto "sql game"

EXERCISE_TYPES = [
    {
        "nombre": "Consultas SELECT básicas",
        "descripcion": "Ejercicios para seleccionar columnas y filas específicas de una tabla usando SELECT y WHERE.",
        "ejemplo": "SELECT nombre_cliente, ciudad FROM cliente WHERE categoria = 100;"
    },
    {
        "nombre": "Consultas con operadores lógicos",
        "descripcion": "Ejercicios que requieren el uso de operadores AND, OR, NOT y paréntesis para combinar condiciones.",
        "ejemplo": "SELECT * FROM mascota WHERE especie = 'perro' OR especie = 'gato';"
    },
    {
        "nombre": "Eliminación de duplicados",
        "descripcion": "Ejercicios donde se solicita mostrar resultados únicos usando DISTINCT.",
        "ejemplo": "SELECT DISTINCT propietario FROM mascota;"
    },
    {
        "nombre": "Ordenamiento de resultados",
        "descripcion": "Ejercicios que requieren ordenar los resultados usando ORDER BY.",
        "ejemplo": "SELECT nombre_cliente FROM cliente ORDER BY cliente_id;"
    },
    {
        "nombre": "Funciones de agregación",
        "descripcion": "Ejercicios que involucran SUM, COUNT, AVG, MIN, MAX y GROUP BY.",
        "ejemplo": "SELECT categoria, COUNT(*) FROM cliente GROUP BY categoria;"
    },
    {
        "nombre": "Consultas con JOIN",
        "descripcion": "Ejercicios que requieren combinar datos de dos o más tablas usando INNER JOIN, LEFT JOIN, etc.",
        "ejemplo": "SELECT cliente.nombre_cliente, vendedor.nombre_vendedor FROM cliente JOIN vendedor ON cliente.vendedor_id = vendedor.vendedor_id;"
    },
    {
        "nombre": "Subconsultas",
        "descripcion": "Ejercicios donde se debe usar una consulta anidada dentro de SELECT, WHERE o FROM.",
        "ejemplo": "SELECT nombre FROM producto WHERE precio = (SELECT MAX(precio) FROM producto);"
    },
    {
        "nombre": "Consultas con IN y NOT IN",
        "descripcion": "Ejercicios que usan IN o NOT IN para filtrar valores dentro de una lista o subconsulta.",
        "ejemplo": "SELECT nombre FROM mascota WHERE especie IN ('perro', 'gato');"
    },
    {
        "nombre": "Consultas con LIMIT/OFFSET",
        "descripcion": "Ejercicios para limitar la cantidad de resultados devueltos.",
        "ejemplo": "SELECT * FROM mascota ORDER BY fecha_nacimiento DESC LIMIT 1;"
    },
    {
        "nombre": "Detección de duplicados",
        "descripcion": "Ejercicios que requieren identificar valores duplicados en una columna.",
        "ejemplo": "SELECT email_id FROM empleados GROUP BY email_id HAVING COUNT(*) > 1;"
    }
]