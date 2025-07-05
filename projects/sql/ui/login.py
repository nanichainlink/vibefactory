from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from ui.challenge_selection import ChallengeSelectionWindow

# Simulación de usuarios para el ejemplo
USERS = {
    "admin": "admin123",
    "user": "pass"
}

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQL Game - Login")
        self.setFixedSize(300, 180)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.user_label = QLabel("Usuario:")
        self.user_input = QLineEdit()
        self.pass_label = QLabel("Contraseña:")
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton("Ingresar")
        self.login_btn.clicked.connect(self.try_login)

        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def try_login(self):
        user = self.user_input.text()
        pwd = self.pass_input.text()
        if user in USERS and USERS[user] == pwd:
            self.accept_login()
        else:
            QMessageBox.warning(self, "Error", "Datos de acceso incorrectos")

    def accept_login(self):
        self.hide()
        self.challenge_window = ChallengeSelectionWindow()
        self.challenge_window.show()