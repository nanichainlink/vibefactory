import sqlite3

def create_connection(db_file):
    """Crea una conexión a la base de datos SQLite especificada por db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conectado a la base de datos: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Crea las tablas necesarias para el entorno de práctica SQL Game."""
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabla de niveles o retos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        difficulty TEXT CHECK(difficulty IN ('Fácil', 'Medio', 'Difícil')) NOT NULL
    );
    """)

    # Tabla de intentos de usuario por reto
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id INTEGER NOT NULL,
        submitted_query TEXT NOT NULL,
        is_correct BOOLEAN,
        attempt_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (challenge_id) REFERENCES challenges(id)
    );
    """)

    # Tabla de datos de ejemplo: empleados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        department_id INTEGER,
        hire_date DATE NOT NULL,
        salary REAL NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    );
    """)

    # Tabla de departamentos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    # Tabla de proyectos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_date DATE,
        end_date DATE
    );
    """)

    # Tabla de asignaciones de empleados a proyectos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        assigned_date DATE,
        FOREIGN KEY (employee_id) REFERENCES employees(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );
    """)

    conn.commit()
    print("Tablas creadas correctamente.")

def insert_sample_data(conn):
    """Inserta datos de ejemplo en las tablas employees, departments y projects."""
    cursor = conn.cursor()

    # Departamentos
    departments = [
        ("Recursos Humanos",),
        ("Tecnología",),
        ("Ventas",),
        ("Marketing",)
    ]
    cursor.executemany("INSERT INTO departments (name) VALUES (?)", departments)

    # Empleados
    employees = [
        ("Ana", "García", 1, "2022-01-15", 25000),
        ("Luis", "Pérez", 2, "2021-09-01", 32000),
        ("María", "López", 2, "2020-06-20", 35000),
        ("Carlos", "Sánchez", 3, "2019-03-10", 28000),
        ("Elena", "Martínez", 4, "2023-02-01", 22000)
    ]
    cursor.executemany(
        "INSERT INTO employees (first_name, last_name, department_id, hire_date, salary) VALUES (?, ?, ?, ?, ?)",
        employees
    )

    # Proyectos
    projects = [
        ("Migración de Servidores", "2023-01-01", "2023-06-30"),
        ("Campaña de Marketing 2024", "2024-02-01", None),
        ("Implementación CRM", "2022-09-15", "2023-03-15")
    ]
    cursor.executemany(
        "INSERT INTO projects (name, start_date, end_date) VALUES (?, ?, ?)",
        projects
    )

    # Asignaciones de empleados a proyectos
    employee_projects = [
        (1, 1, "2023-01-10"),
        (2, 1, "2023-01-15"),
        (3, 3, "2022-09-20"),
        (4, 2, "2024-02-10"),
        (5, 2, "2024-02-15")
    ]
    cursor.executemany(
        "INSERT INTO employee_projects (employee_id, project_id, assigned_date) VALUES (?, ?, ?)",
        employee_projects
    )

    conn.commit()
    print("Datos de ejemplo insertados correctamente.")

if __name__ == "__main__":
    conn = create_connection("sqlgame.db")
    if conn:
        create_tables(conn)
        insert_sample_data(conn)
        conn.close()