from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap

def create_app():

    app = Flask(__name__)

    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    return app