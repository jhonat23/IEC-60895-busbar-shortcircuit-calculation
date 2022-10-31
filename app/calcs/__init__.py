from flask import Blueprint

calcs = Blueprint('calcs', __name__)

from . import views