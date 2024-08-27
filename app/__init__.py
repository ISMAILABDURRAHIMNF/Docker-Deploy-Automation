from flask import Flask
from .main import main
from .register import register
from .login import login

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)
    app.register_blueprint(register)
    app.register_blueprint(login)

    return app