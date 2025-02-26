"""Register route file"""

from flask import Blueprint, request, jsonify
import bcrypt
from .query import query_db

register = Blueprint('register', __name__)

@register.route('/register', methods=['POST'])
def register_user():
    """Register function"""
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    check_account = query_db('SELECT username FROM akun WHERE username = %s '\
                             'OR email = %s', (username, email), one=False)

    if check_account:
        return jsonify({'message' : 'Username atau email sudah terpakai!'}), 401

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query_db('INSERT INTO akun (username, email, password) '\
             'VALUES (%s, %s, %s)', (username, email, hashed_password))

    return jsonify({'message': 'Akun berhasil dibuat!'}), 200
