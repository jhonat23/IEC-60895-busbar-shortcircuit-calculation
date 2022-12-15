from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap
from .calcs import calcs
from .report import report

def create_app():

    app = Flask(__name__)

    #Blueprints
    app.register_blueprint(calcs)
    app.register_blueprint(report)

    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    return app