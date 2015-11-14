from . import field_storage
from . import models
from . import forms
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

@field_storage.route('/admin/schema/')
@login_required
def schema_admin():
    schemata = models.Schema.query.all()
    return render_template("admin/schema.html", schemata=schemata)

@field_storage.route('/admin/schema/add', methods=('GET', 'POST'))
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
        return redirect(url_for('field_storage.schema_admin'))
    return render_template('admin/schema_form.html', form=form)

@field_storage.route('/admin/schema/edit/<int:schema_id>')
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
        return redirect(url_for('field_storage.schema_admin'))
    return render_template('admin/schema_form.html', form=form)

@field_storage.route('/admin/schema/delete/<int:schema_id>')
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
    return redirect(url_for('field_storage.schema_admin'))

@field_storage.route('/add/field/<int:container_id>/', methods=('GET', 'POST'))
@login_required
def add_field_select_type(container_id):
    """
    Add a Field to a container: Show a field type selector
    """
    form = forms.FieldAddSelectTypeForm()
    form.field_type.choices = [(schema.id, schema.name) for schema in models.Schema.query.all()]
    if form.validate_on_submit():
        return redirect(url_for('field_storage.add_field_values', container_id=container_id, schema_id=form.field_type.data))
    return render_template('basic_form.html', form=form)

def container_view(container):
    """
    Helper function to redirect to the adequate view for a container
    """
    if container.container_type == 'uni':
        return redirect(url_for('unis.uni', uni_id=container_id))
    elif container.container_type == 'city':
        return redirect(url_for('unis.cities')),
    elif container.container_type == 'subject':
        return redirect(url_for('unis.uni', uni_id=container.parent.id)),


@field_storage.route('/add/field/<int:container_id>/<int:schema_id>', methods=('GET', 'POST'))
@login_required
def add_field_values(container_id, schema_id):
    """
    Add a Field to a container: Show the Form to actually add the form
    """
    from wtforms.validators import Required
    schema = models.Schema.query.get(schema_id)

    # Add a value field depending on the type of the field
    model = models.field_models[schema.data_type]
    form = forms.FieldAddForm.add_field('value',
        model.widget(schema.name,
            model.validators.append(Required())
        ))()

    # Remove the comment field if it isn't allowed
    if not schema.permit_comment:
        del form.comment

    container = models.Container.query.get(container_id)

    if form.validate_on_submit():
        field = model(schema, container)
        field.value = form.value.data
        db.session.add(field)
        return container_view(container)

    return render_template('field_add.html', form=form, schema=schema, container=container)

@field_storage.route('/delete/field/<int:field_id>')
@login_required
def delete_field(field_id):
    """
    Delete a field
    """
    field = models.Field.query.get(field_id)
    # delete the field
    if not field:
        flash("No such field!")
    else:
        db.session.delete(field)

    # redirect to field owner
    return container_view(field.container)
