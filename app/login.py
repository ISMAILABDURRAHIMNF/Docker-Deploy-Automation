from flask import Blueprint, request, jsonify, session
from .query import query_db
import bcrypt
from .decorator import login_required

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET','POST'])
def login_user():
    username = request.form['username'] 
    password = request.form['password']

    user = query_db('SELECT * FROM users WHERE username = %s', (username,), one=True)

    if user and bcrypt.checkpw(password.encode(), user['password'].encode('utf-8')):
        session['user'] = username
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@login.route('/logout')
@login_required
def logout_user():
    session.pop('user', None)
    return jsonify({'message': 'Logged out'}), 200