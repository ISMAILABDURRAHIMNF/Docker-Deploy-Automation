"""Login route file"""

import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import bcrypt
import jwt
from .query import query_db

load_dotenv()

login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
def login_user():
    """Login function"""

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(username, password)

    user = query_db('SELECT * FROM akun WHERE username = %s', (username,), one=True)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({
            'user': username,
            'exp': datetime.now() + timedelta(minutes=30)
        }, os.getenv('SECRET_KEY') , algorithm="HS256")
        query_db('UPDATE akun SET login_token = %s '\
                 'WHERE username = %s', (token, username), one=True)
        print(token)
        return jsonify({'message': 'Login berhasil!','token': token, 'id': user['id']}), 200
    return jsonify({'message': 'Username atau password invalid'}), 401

@login.route('/logout', methods=['POST'])
def logout_user():
    """Logout Function"""

    token = request.form.get('token')
    print(token)
    query_db('UPDATE akun SET login_token = NULL WHERE login_token = %s', (token,), one=True)
    return jsonify({'message': 'Log Out berhasil!'}), 200
