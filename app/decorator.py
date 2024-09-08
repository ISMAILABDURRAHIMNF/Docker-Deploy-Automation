from functools import wraps
from flask import jsonify, request
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Unauthorized'}), 401
        try:
            token = token.split()[1]
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401   
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function