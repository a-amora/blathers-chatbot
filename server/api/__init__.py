from flask import Blueprint

blathers_routes = Blueprint('api', __name__)

from . import routes