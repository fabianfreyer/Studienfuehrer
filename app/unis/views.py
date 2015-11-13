from . import unis
from . import models
from . import forms
from .. import db
from flask import render_template, redirect, request, url_for, flash

@unis.route('/cities/')
def cities():
    cities = models.City.query.options(db.joinedload('children')).all()
    return render_template("cities.html", cities=cities)
