from flask import Flask
from .main import main
from .register import register
from .login import login
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')
    
    app.register_blueprint(main)
    app.register_blueprint(register)
    app.register_blueprint(login)

    return app