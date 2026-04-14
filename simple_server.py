from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# Proxy API routes to app_flask logic or stub
@app.route('/token', methods=['POST'])
def token_stub():
    return jsonify({'access_token': 'demo-token', 'token_type': 'bearer'}), 200

@app.route('/register', methods=['POST'])
def register_stub():
    return jsonify({'message': 'Registered'}), 201

@app.route('/users/me')
def me_stub():
    return jsonify({'id':1, 'username': 'demo', 'email': 'demo@example.com'}), 200

@app.route('/calculate-diet', methods=['POST'])
def calculate_diet():
    from ai_logic import generate_diet_plan
    data = request.json
    plan = generate_diet_plan(data)
    return jsonify(plan)

@app.route('/my-plans')
def plans_stub():
    return jsonify([])

@app.route('/chat', methods=['POST'])
def chat():
    from ai_logic import get_chat_response
    data = request.json
    response = get_chat_response(data['message'])
    return jsonify({'response': response})

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)

print("Simple AI Diet Planner Server on http://127.0.0.1:5000 - API Stubs Added")
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

