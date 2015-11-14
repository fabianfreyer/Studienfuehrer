from . import unis
from . import models
from . import forms
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

@unis.route('/cities/')
def cities():
    cities = models.City.query.options(db.joinedload('children')).all()
    return render_template("cities.html", cities=cities)

@unis.route('/city/add', methods=('GET', 'POST'))
@login_required
def city_add():
    form = forms.CityAddForm()
    if form.validate_on_submit():
        # Create a city instance
        city = models.City()
        # Fetch the name field schema instance
        name_schema = models.Schema.query.filter_by(name='name').first()
        # Create a name field for the city
        name = models.TextField(name_schema, city)
        name.value = form.name.data
        db.session.add(city)
        db.session.add(name)
        return redirect(url_for('unis.cities'))
    return render_template("city_add.html", form=form)
