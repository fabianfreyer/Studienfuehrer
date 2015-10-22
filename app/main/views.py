from flask import render_template, redirect, url_for, abort, flash, request, current_app
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..auth.models import Permission, Role

@main.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

