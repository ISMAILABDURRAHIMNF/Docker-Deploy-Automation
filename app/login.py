from flask import Blueprint, request, jsonify
from .query import query_db
import bcrypt

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET','POST'])
def login_user():
    username = request.form['username'] 
    password = request.form['password']

    user = query_db('SELECT * FROM users WHERE username = %s', (username,), one=True)

    if user and bcrypt.checkpw(password.encode(), user['password'].encode('utf-8')):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401