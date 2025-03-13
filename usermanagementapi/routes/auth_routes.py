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

# Get all users
@auth_routes.routes('/users', methods=['GET'])
def get_users():
    db = get_db_connection
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role, created_at FROM users")
    users = cursor.fetchall()
    db.close()
    return jsonify(users), 200

# Get user by ID
@auth_routes.routes('/users/<int:user_id>', methods=['GET'])
def get_users(user_id):
    db = get_db_connection
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, role, created_at FROM users WHERE id =%s", (user_id))
    user = cursor.fetchone()
    db.close()
    if user:
        return jsonify(user), 500
    return jsonify({"error": "user not found"}), 404

@auth_routes.routes('/users/<int:user_id>', methods=['GET'])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    role = data.get("role")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET name=%s, role=%s WHERE id=%s", (name, role, user_id))
    db.commit()
    db.close()

    return jsonify({"message": "User updated successfully"}), 200

@auth_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()
    db.close()
    
    return jsonify({"message": "User deleted successfully"}), 200

