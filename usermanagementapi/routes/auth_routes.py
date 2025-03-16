from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from usermanagementapi.models.db import get_db_connection
from usermanagementapi.utils.security import hash_password, check_password

auth_routes = Blueprint("auth_routes", __name__)

# Register a user
@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = hash_password(password)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 400
        
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Login a user
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, email, password, role FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password(password, user["password"]):
            access_token = create_access_token(identity={"id": user["id"], "role": user["role"]})
            return jsonify({"access_token": access_token}), 200

        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Get all users
@auth_routes.route('/users', methods=['GET'])
def get_users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, name, email, role, created_at FROM users")
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Get user by ID
@auth_routes.route('/users/<int:user_id>', methods=['GET'])
def fetch_user(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, name, email, role, created_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Update user
@auth_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    role = data.get("role")

    if not name and not role:
        return jsonify({"error": "At least one field (name or role) is required"}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        update_fields = []
        params = []

        if name:
            update_fields.append("name = %s")
            params.append(name)
        if role:
            update_fields.append("role = %s")
            params.append(role)

        params.append(user_id)
        update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"

        cursor.execute(update_query, params)
        db.commit()

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Delete user
@auth_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()



