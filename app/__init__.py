from flask import Flask
from .routes import bp
import secrets

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    app.register_blueprint(bp)
    return app 