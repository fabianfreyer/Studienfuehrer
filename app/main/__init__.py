from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..auth.models import Permission

@main.app_context_processor
def inject_permisssions():
    return dict(Permission=Permission)
