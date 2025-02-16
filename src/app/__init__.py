"""Main file"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .handler import handler
from .register import register
from .login import login
from .upload import upload

load_dotenv()

def create_app():
    """Main app and blueprint function"""

    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    app.register_blueprint(handler)
    app.register_blueprint(register)
    app.register_blueprint(login)
    app.register_blueprint(upload)

    return app
