from . import unis
from . import models
from . import forms
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

@unis.route('/admin/schema/')
@login_required
def schema_admin():
    schemata = models.Schema.query.all()
    return render_template("admin/schema.html", schemata=schemata)

@unis.route('/admin/schema/add', methods=('GET', 'POST'))
@login_required
def schema_add():
    form = forms.SchemaForm()
    if form.validate_on_submit():
        schema = models.Schema()
        schema.name = form.name.data
        schema.description = form.description.data
        schema.permit_comment = form.permit_comment.data
        schema.data_type = form.data_type.data
        db.session.add(schema)
        return redirect(url_for('unis.schema_admin'))
    return render_template('admin/schema_form.html', form=form)

@unis.route('/admin/schema/edit/<int:schema_id>')
@login_required
def schema_edit(schema_id):
    """
    Edit a schema
    """
    schema = models.Schema.query.get(schema_id)
    form = forms.SchemaForm(obj=schema)
    if form.validate_on_submit():
        schema.name = form.name.data
        schema.description = form.description.data
        schema.permit_comment = form.permit_comment.data
        schema.data_type = form.data_type.data
        db.session.add(schema)
        return redirect(url_for('unis.schema_admin'))
    return render_template('admin/schema_form.html', form=form)

@unis.route('/admin/schema/delete/<int:schema_id>')
@login_required
def schema_delete(schema_id):
    """
    Delete a schema
    """
    schema = models.Schema.query.get(schema_id)
    # Check if there are still fields with this schema left
    if models.Field.query.filter_by(field_type=schema).count() != 0:
        flash('Cannot delete: there are still values for this field in the database')
    else:
        db.session.delete(schema)
        flash('Deleted field: %s' % schema.name)
    return redirect(url_for('unis.schema_admin'))

