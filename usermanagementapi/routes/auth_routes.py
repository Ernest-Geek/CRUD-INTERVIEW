from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.db import get_db_connection
from utils.security import hash_password, check_password

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = hash_password(data.get('password'))

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already exist"}), 400
        
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s %s %s)"
                       (name, email, password))
        db.commit()
        return jsonify({"message": "User registered Succesfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Database error"}), 500
    finally:
        cursor.close()
        db.close()

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user and check_password(password, user[3]):
        access_token = create_access_token(identity={"id": user[0], "role": user[4]})
        return jsonify({"access_token": access_token})
    
    return jsonify({"error": "Invalid credentials"}), 401

