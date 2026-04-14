from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
from database import User, DietPlan, get_db as get_sqlalchemy_db # Reuse DB
from ai_logic import generate_diet_plan
from chatbot import process_chat_message

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meals_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

# Reuse models if possible, but simple here

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already registered'}), 400
    
    new_user = User(username=username, email=email, hashed_password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201

@app.route('/token', methods=['POST'])
def login():
    data = request.form if request.form else request.json
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    if not user:
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=f"{username}@test.com", hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
    
    if check_password_hash(user.hashed_password, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token, 'token_type': 'bearer'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@jwt_required()
@app.route('/users/me')
def me():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@jwt_required()
@app.route('/calculate-diet', methods=['POST'])
def calculate_diet():
    data = request.json
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    
    plan_data = generate_diet_plan(data)
    
    return jsonify(plan_data)

@jwt_required()
@app.route('/my-plans')
def my_plans():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    plans = DietPlan.query.filter_by(user_id=user.id).order_by(DietPlan.created_at.desc()).all()
    return jsonify([{
        'id': p.id,
        'bmi': p.bmi,
        'daily_calories': p.daily_calories,
        'created_at': p.created_at.isoformat()
    } for p in plans])

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = process_chat_message(data['message'])
    return jsonify({'response': response})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting AI Diet Planner on http://127.0.0.1:8000")
    app.run(host='127.0.0.1', port=8000, debug=True)
