from flask import Blueprint, request, jsonify
from .query import query_db
import bcrypt

register = Blueprint('register', __name__)

@register.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query_db('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    
    return jsonify({'message': 'User registered successfully'}), 201