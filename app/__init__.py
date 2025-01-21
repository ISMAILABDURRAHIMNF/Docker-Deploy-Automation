from flask import Flask
from .main import main
from .register import register
from .login import login
from .upload import upload
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('SECRET_KEY')
    
    CORS(app, resources={r"/*": {"origins": "https://docker.deeployin.my.id"}})
    app.register_blueprint(main)
    app.register_blueprint(register)
    app.register_blueprint(login)
    app.register_blueprint(upload)

    return app
