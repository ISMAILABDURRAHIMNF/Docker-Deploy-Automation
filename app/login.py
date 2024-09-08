from flask import Blueprint, request, jsonify, session
from .query import query_db
import bcrypt
import jwt
from .decorator import login_required
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET','POST'])
def login_user():
    username = request.form['username'] 
    password = request.form['password']

    user = query_db('SELECT * FROM akun WHERE nama = %s', (username,), one=True)

    if user and bcrypt.checkpw(password.encode(), user['password'].encode('utf-8')):
        # session['user'] = username
        token = jwt.encode({
            'user': username,
            'exp': datetime.now() + timedelta(minutes=30)
        }, os.getenv('SECRET_KEY') , algorithm="HS256")
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@login.route('/logout')
@login_required
def logout_user():
    session.pop('user', None)
    return jsonify({'message': 'Logged out'}), 200