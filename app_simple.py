from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
from datetime import datetime
from ai_logic import generate_diet_plan
from chatbot import process_chat_message

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
jwt = JWTManager(app)
CORS(app)

# DB functions
def get_db_connection():
    conn = sqlite3.connect('meals_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM users WHERE username = ? OR email = ?", (data['username'], data['email']))
    if cur.fetchone():
        conn.close()
        return jsonify({'error': 'Username or email already exists'}), 400
    
    hashed_pw = generate_password_hash(data['password'])
    cur.execute("INSERT INTO users (username, email, hashed_password, created_at) VALUES (?, ?, ?, ?)",
                (data['username'], data['email'], hashed_pw, datetime.utcnow()))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    
    return jsonify({'message': 'User created', 'user_id': user_id}), 201

@app.route('/token', methods=['POST'])
def login():
    data = request.form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (data['username'],))
    user = cur.fetchone()
    conn.close()
    
    if user and check_password_hash(user['hashed_password'], data['password']):
        access_token = create_access_token(identity=user['username'])
        return jsonify({'access_token': access_token, 'token_type': 'bearer'})
    return jsonify({'error': 'Invalid credentials'}), 401

@jwt_required()
@app.route('/users/me')
def me():
    username = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return jsonify({'id': user['id'], 'username': user['username'], 'email': user['email']})

@jwt_required()
@app.route('/calculate-diet', methods=['POST'])
def calculate_diet():
    data = request.json
    username = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    user_id = user['id']
    
    plan_data = generate_diet_plan(data)
    
    cur.execute("""
        INSERT INTO diet_plans (user_id, age, gender, height, weight, activity_level, goal, food_preference, 
        bmi, bmr, daily_calories, breakfast, lunch, dinner, snacks, water_intake, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, data['age'], data['gender'], data['height'], data['weight'], data['activity_level'], data['goal'], data['food_preference'], 
          plan_data['bmi'], plan_data['bmr'], plan_data['daily_calories'], plan_data['breakfast'], plan_data['lunch'], plan_data['dinner'], 
          plan_data['snacks'], plan_data['water_intake'], datetime.utcnow()))
    conn.commit()
    conn.close()
    
    return jsonify(plan_data)

@jwt_required()
@app.route('/my-plans')
def my_plans():
    username = get_jwt_identity()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    user_id = user['id']
    cur.execute("SELECT bmi, daily_calories, created_at FROM diet_plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    plans = cur.fetchall()
    conn.close()
    return jsonify([{'id': p['id'], 'bmi': p['bmi'], 'daily_calories': p['daily_calories'], 'created_at': p['created_at']} for p in plans])

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    return jsonify({'response': process_chat_message(data['message'])})

if __name__ == '__main__':
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, hashed_password TEXT, created_at TIMESTAMP)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS diet_plans
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, age INTEGER, gender TEXT, height REAL, weight REAL, activity_level TEXT, goal TEXT, food_preference TEXT, 
                    bmi REAL, bmr REAL, daily_calories REAL, breakfast TEXT, lunch TEXT, dinner TEXT, snacks TEXT, water_intake TEXT, created_at TIMESTAMP)''')
    conn.commit()
    conn.close()
    app.run(debug=True, port=8000)

