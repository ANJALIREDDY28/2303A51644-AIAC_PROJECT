from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from database import SessionLocal, User, DietPlan, engine
from ai_logic import generate_diet_plan
from chatbot import process_chat_message

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

jwt = JWTManager(app)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

@app.route('/register', methods=['POST'])
def register():
    db_session = SessionLocal()
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password = generate_password_hash(data['password'])

        existing_user = db_session.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'error': 'Username or email already registered'}), 400

        new_user = User(username=username, email=email, hashed_password=password)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        return jsonify({'message': 'User created', 'user_id': new_user.id}), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@app.route('/token', methods=['POST'])
def login():
    db_session = SessionLocal()
    try:
        data = request.form
        username = data['username']
        password = data['password']

        # Test user if not existw
        user = db_session.query(User).filter_by(username=username).first()
        if not user:
            hashed_password = generate_password_hash(password)
            user = User(username=username, email=f"{username}@test.com", hashed_password=hashed_password)
            db_session.add(user)
            db_session.commit()
        
        if check_password_hash(user.hashed_password, password):
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token, 'token_type': 'bearer'})
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db_session.close()

@jwt_required()
@app.route('/users/me')
def me():
    try:
        username = get_jwt_identity()
        db_session = SessionLocal()
        user = db_session.query(User).filter(User.username == username).first()
        db_session.close()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calculate-diet', methods=['POST'])
def calculate_diet():
    try:
        data = request.json or {}
        # Defaults for missing fields
        data.setdefault('age', 30)
        data.setdefault('gender', 'male')
        data.setdefault('height', 170.0)
        data.setdefault('weight', 70.0)
        data.setdefault('activity_level', 'medium')
        data.setdefault('goal', 'maintenance')
        data.setdefault('food_preference', 'veg')
        
        plan_data = generate_diet_plan(data)
        return jsonify(plan_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jwt_required()
@app.route('/my-plans')
def my_plans():
    try:
        username = get_jwt_identity()
        db_session = SessionLocal()
        user = db_session.query(User).filter(User.username == username).first()
        plans = db_session.query(DietPlan).filter(DietPlan.user_id == user.id).order_by(DietPlan.created_at.desc()).limit(10).all()
        db_session.close()
        return jsonify([{
            'id': p.id,
            'bmi': getattr(p, 'bmi', 0),
            'daily_calories': getattr(p, 'daily_calories', 0),
            'created_at': p.created_at.isoformat() if p.created_at else ''
        } for p in plans or []])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        response = process_chat_message(data['message'])
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting AI Diet Planner on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
