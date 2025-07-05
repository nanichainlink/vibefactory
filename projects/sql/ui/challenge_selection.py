from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget
)
from ui.editor import SQLEditorWindow

# Simulación de retos
CHALLENGES = [
    {"id": 1, "title": "Selecciona todos los usuarios", "description": "Escribe una consulta para seleccionar todos los usuarios de la tabla users."},
    {"id": 2, "title": "Cuenta los productos", "description": "Cuenta cuántos productos hay en la tabla products."},
    {"id": 3, "title": "Filtra por edad", "description": "Selecciona los usuarios mayores de 18 años de la tabla users."}
]

class ChallengeSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Game - Selección de Retos")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Selecciona un reto:")
        self.challenge_list = QListWidget()
        for ch in CHALLENGES:
            self.challenge_list.addItem(f"{ch['id']}. {ch['title']}")
        self.select_btn = QPushButton("Seleccionar reto")
        self.select_btn.clicked.connect(self.select_challenge)

        layout.addWidget(self.label)
        layout.addWidget(self.challenge_list)
        layout.addWidget(self.select_btn)
        self.setLayout(layout)

    def select_challenge(self):
        idx = self.challenge_list.currentRow()
        if idx >= 0:
            challenge = CHALLENGES[idx]
            self.hide()
            self.editor_window = SQLEditorWindow(challenge)
            self.editor_window.show()