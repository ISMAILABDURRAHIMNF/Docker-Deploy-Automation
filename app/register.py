from flask import Blueprint, request, jsonify
from .query import query_db
import bcrypt
from flask_cors import CORS

register = Blueprint('register', __name__)
CORS(register, resources={r"/*": {"origins": "http://localhost:5173"}})

@register.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query_db('INSERT INTO akun (username, email, password) VALUES (%s,%s, %s)', (username, email, hashed_password))
    
    return jsonify({'message': 'User registered successfully'}), 201