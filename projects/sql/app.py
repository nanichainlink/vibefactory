from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Mock de autenticación
def authenticate_user(username, password):
    return username == 'testuser' and password == 'testpass'

# Mock de obtención de retos
def get_next_challenge():
    return {
        'id': 1,
        'description': 'SELECT * FROM users WHERE id=1;',
        'expected_result': [{'id': 1, 'name': 'Alice'}]
    }

# Mock de evaluación de soluciones
def evaluate_solution(challenge_id, sql):
    if sql.strip().lower() == 'select * from users where id=1;':
        return {'correct': True, 'feedback': '¡Correcto!'}
    else:
        return {'correct': False, 'feedback': 'Revisa tu consulta SQL.'}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if authenticate_user(data['username'], data['password']):
        session['user'] = data['username']
        return jsonify({'message': f'Bienvenido, {data["username"]}'}), 200
    else:
        return jsonify({'message': 'Datos de acceso incorrectos'}), 401

@app.route('/challenge/next', methods=['GET'])
def next_challenge():
    if 'user' not in session:
        return jsonify({'message': 'No autenticado'}), 401
    challenge = get_next_challenge()
    return jsonify(challenge), 200

@app.route('/challenge/<int:challenge_id>/submit', methods=['POST'])
def submit_solution(challenge_id):
    if 'user' not in session:
        return jsonify({'message': 'No autenticado'}), 401
    data = request.get_json()
    result = evaluate_solution(challenge_id, data['sql'])
    return jsonify({'feedback': result['feedback']}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Sesión finalizada'}), 200

if __name__ == '__main__':
    app.run(debug=True)