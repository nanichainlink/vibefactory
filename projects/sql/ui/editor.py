from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from ui.result_area import ResultArea
import sqlite3

# Base de datos de ejemplo
DB_FILE = "game.db"

def setup_demo_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Crear tablas de ejemplo
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT)")
    # Insertar datos si la tabla está vacía
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (name, age) VALUES ('Alice', 22), ('Bob', 17), ('Carol', 30)")
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO products (name) VALUES ('Laptop'), ('Mouse'), ('Keyboard')")
    conn.commit()
    conn.close()

setup_demo_db()

class SQLEditorWindow(QWidget):
    def __init__(self, challenge):
        super().__init__()
        self.challenge = challenge
        self.setWindowTitle(f"SQL Game - {challenge['title']}")
        self.setFixedSize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.desc_label = QLabel(self.challenge["description"])
        self.editor = QTextEdit()
        self.run_btn = QPushButton("Ejecutar Consulta")
        self.run_btn.clicked.connect(self.run_query)
        self.result_area = ResultArea()

        layout.addWidget(self.desc_label)
        layout.addWidget(self.editor)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.result_area)
        self.setLayout(layout)

    def run_query(self):
        query = self.editor.toPlainText()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        try:
            c.execute(query)
            if query.strip().lower().startswith("select"):
                rows = c.fetchall()
                headers = [desc[0] for desc in c.description]
                self.result_area.show_results(headers, rows)
            else:
                conn.commit()
                self.result_area.show_message("Consulta ejecutada correctamente.")
        except Exception as e:
            self.result_area.show_message(f"Error: {e}")
        finally:
            conn.close()