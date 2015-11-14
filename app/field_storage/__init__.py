from flask import Blueprint

field_storage = Blueprint('field_storage', __name__)

from . import views
