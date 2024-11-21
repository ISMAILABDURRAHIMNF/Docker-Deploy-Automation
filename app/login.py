from flask import Blueprint, request, jsonify, session
from flask_cors import CORS
from .query import query_db
import bcrypt
import jwt
from .decorator import login_required
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

login = Blueprint('login', __name__)
CORS(login, resources={r"/*": {"origins": "http://localhost:5173"}})

@login.route('/login', methods=['POST'])
def login_user():
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
        query_db('UPDATE akun SET login_token = %s WHERE username = %s', (token, username), one=True)
        print(token)
        return jsonify({'token': token, 'id': user['id']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@login.route('/logout', methods=['POST'])
def logout_user():
    token = request.form.get('token')
    print(token)
    query_db('UPDATE akun SET login_token = NULL WHERE login_token = %s', (token,), one=True)
    return jsonify({'message': 'Logged out'}), 200