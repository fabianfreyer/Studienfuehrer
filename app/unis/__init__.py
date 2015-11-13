from flask import Blueprint

unis = Blueprint('unis', __name__)

from . import views, schema_views
