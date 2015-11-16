from . import unis
from . import models
from . import forms
from .. import db
from .. import field_storage
from flask import render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_required

@unis.route('/uni/by_city')
def by_city():
    cities = models.City.query.options(db.joinedload('children')).all()
    return render_template("cities.html", cities=cities)

@unis.route('/add/city', methods=('GET', 'POST'))
@login_required
def city_add():
    form = forms.CityAddForm()
    if form.validate_on_submit():
        # Create a city instance
        city = models.City()
        # Fetch the name field schema instance
        name_schema = field_storage.models.Schema.query.filter_by(name='name').first()
        # Create a name field for the city
        name = field_storage.models.TextField(name_schema, city)
        name.value = form.name.data
        db.session.add(city)
        db.session.add(name)
        return form.redirect('unis.by_city')
    return render_template("city_add.html", form=form)

@unis.route('/uni/<int:uni_id>')
def detail(uni_id):
    uni = models.Uni.query.get(uni_id)
    if uni is None:
        abort(404)
    return render_template("uni.html", uni=uni)

@unis.route('/uni/<int:uni_id>/add/subject', methods=('GET', 'POST'))
def uni_add_subject(uni_id):
    """
    Add a subject to a uni
    """
    form = forms.SubjectAddForm()
    # Since we already know what the uni will be, don't show a dropdown for it
    del form.uni
    if form.validate_on_submit():
        # Get the uni to add the subject to
        uni = models.Uni.query.get(uni_id)
        subject = models.Subject(uni)
        # Fetch the name field schema instance
        name_schema = field_storage.models.Schema.query.filter_by(name='name').first()
        # Create a name field for the subject
        name = field_storage.models.TextField(name_schema, subject)
        name.value = form.name.data
        db.session.add(subject)
        db.session.add(name)
        # Flush the db session, so we can see what the ID of the newly added uni is
        db.session.flush()
        return form.redirect('unis.detail', uni_id=uni.id)
    return render_template("basic_form.html", form=form)

@unis.route('/add/uni', methods=('GET', 'POST'))
@login_required
def uni_add():
    """
    Add a uni to a city
    """
    form = forms.UniAddForm()
    # Update the choices to add all the cities
    form.city.choices = [(city.id, city.fields['name'].value) for city in models.City.query.all()]
    if form.validate_on_submit():
        # Get the city to add the uni to
        city = models.City.query.get(form.city.data)
        uni = models.Uni(city)
        # Fetch the name field schema instance
        name_schema = field_storage.models.Schema.query.filter_by(name='name').first()
        # Create a name field for the uni
        name = field_storage.models.TextField(name_schema, uni)
        name.value = form.name.data
        db.session.add(uni)
        db.session.add(name)
        # Flush the db session, so we can see what the ID of the newly added uni is
        db.session.flush()
        return form.redirect('unis.detail', uni_id=uni.id)
    return render_template("uni_add.html", form=form)
