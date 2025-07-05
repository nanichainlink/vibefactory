import unittest
from unittest.mock import patch
from app import app  # Suponiendo que la app principal es un Flask app en app.py

class TestMainGameFlow(unittest.TestCase):
    def setUp(self):
        # Configura el cliente de pruebas de Flask
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.authenticate_user')
    def test_login_success(self, mock_auth):
        # Simula autenticación exitosa
        mock_auth.return_value = True
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bienvenido', response.get_data(as_text=True))

    @patch('app.authenticate_user')
    def test_login_failure(self, mock_auth):
        # Simula autenticación fallida
        mock_auth.return_value = False
        response = self.client.post('/login', json={
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Datos de acceso incorrectos', response.get_data(as_text=True))

    @patch('app.get_next_challenge')
    def test_get_challenge(self, mock_challenge):
        # Simula obtención de reto
        mock_challenge.return_value = {
            'id': 1,
            'description': 'SELECT * FROM users WHERE id=1;',
            'expected_result': [{'id': 1, 'name': 'Alice'}]
        }
        response = self.client.get('/challenge/next')
        self.assertEqual(response.status_code, 200)
        self.assertIn('description', response.get_json())

    @patch('app.evaluate_solution')
    def test_submit_solution_correct(self, mock_eval):
        # Simula envío de solución correcta
        mock_eval.return_value = {'correct': True, 'feedback': '¡Correcto!'}
        response = self.client.post('/challenge/1/submit', json={
            'sql': 'SELECT * FROM users WHERE id=1;'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('¡Correcto!', response.get_data(as_text=True))

    @patch('app.evaluate_solution')
    def test_submit_solution_incorrect(self, mock_eval):
        # Simula envío de solución incorrecta
        mock_eval.return_value = {'correct': False, 'feedback': 'Revisa tu consulta SQL.'}
        response = self.client.post('/challenge/1/submit', json={
            'sql': 'SELECT * FROM users;'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Revisa tu consulta SQL.', response.get_data(as_text=True))

    def test_logout(self):
        # Simula cierre de sesión
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sesión finalizada', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()