from . import unis
from . import models
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

@unis.route('/admin/schema/')
@login_required
def schema_admin():
    schemata = models.Schema.query.all()
    return render_template("admin/schema.html", schemata=schemata)

@unis.route('/cities/')
def city_index():
    cities = models.City.query.options(db.joinedload('children')).all()
    return render_template("cities.html", cities=cities)
