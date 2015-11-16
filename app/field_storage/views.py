from . import field_storage
from . import models
from . import forms
from .. import db
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required
from flask.ext.babel import lazy_gettext as _

@field_storage.route('/admin/schema/')
@login_required
def schema_admin():
    categories = models.Category.query.all()
    return render_template("admin/schema.html", categories=categories)

@field_storage.route('/add/category', methods=('GET', 'POST'))
@login_required
def category_add():
    """
    Add a category
    """
    form = forms.CategoryForm()
    if form.validate_on_submit():
        category = models.Category()
        category.name = form.name.data
        db.session.add(category)
        return redirect(url_for('field_storage.schema_admin'))
    return render_template('basic_form.html', form=form, action="add")

@field_storage.route('/edit/category/<int:category_id>', methods=('GET', 'POST'))
@login_required
def category_edit(category_id):
    """
    Edit a category
    """
    category = models.Category.query.get(category_id)
    form = forms.CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        return redirect(url_for('field_storage.schema_admin'))
    return render_template('basic_form.html', form=form, action="edit")

@field_storage.route('/delete/category/<int:category_id>')
@login_required
def category_delete(category_id):
    """
    Delete a category
    """
    category = models.Category.query.get(category_id)
    # Check if there are still fields with this category left
    schema = db.aliased(models.Schema)
    if category.schemata:
        flash(_('Cannot delete category: there are still schemata for this field in the database'))
    else:
        db.session.delete(category)
        flash(_('Deleted Category: %s' % category.name))
    return redirect(url_for('field_storage.schema_admin'))

@field_storage.route('/add/schema', methods=('GET', 'POST'))
@field_storage.route('/add/schema/<int:category_id>', methods=('GET', 'POST'))
@login_required
def schema_add(category_id=None):
    form = forms.SchemaForm()

    if category_id is None:
        form.category.choices = [
                (category.id, category.name)
                for category in models.Category.query.all()]
    else:
        del form.category

    if form.validate_on_submit():
        schema = models.Schema()
        schema.name = form.name.data
        schema.description = form.description.data
        schema.permit_comment = form.permit_comment.data
        schema.data_type = form.data_type.data
        schema.category = models.Category.query.get(category_id if category_id else form.category.data)
        db.session.add(schema)
        return redirect(url_for('field_storage.schema_admin'))
    return render_template('admin/schema_form.html', form=form)

@field_storage.route('/edit/schema/<int:schema_id>', methods=('GET', 'POST'))
@login_required
def schema_edit(schema_id):
    """
    Edit a schema
    """
    schema = models.Schema.query.get(schema_id)
    form = forms.SchemaForm(obj=schema)

    form.category.choices = [
            (category.id, category.name)
            for category in models.Category.query.all()]

    if form.validate_on_submit():
        schema.name = form.name.data
        schema.description = form.description.data
        schema.permit_comment = form.permit_comment.data
        schema.data_type = form.data_type.data
        schema.category = models.Category.query.get(form.category.data)
        db.session.add(schema)
        return redirect(url_for('field_storage.schema_admin'))
    return render_template('admin/schema_form.html', form=form)

@field_storage.route('/delete/schema/<int:schema_id>')
@login_required
def schema_delete(schema_id):
    """
    Delete a schema
    """
    schema = models.Schema.query.get(schema_id)
    # Check if there are still fields with this schema left
    if models.Field.query.filter_by(field_type=schema).count() != 0:
        flash(_('Cannot delete field: there are still values for this field in the database'))
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
    container = models.Container.query.get(container_id)
    form.field_type.choices = [
            (schema.id, schema.name)
            for schema in models.Schema.query.all()
            if schema.name not in container.fields]
    if form.validate_on_submit():
        return redirect(url_for('field_storage.add_field_values', container_id=container_id, schema_id=form.field_type.data))
    return render_template('field_type_select.html', form=form, container=container)

def container_view(container):
    """
    Helper function to redirect to the adequate view for a container
    """
    if container.container_type == 'uni':
        return redirect(url_for('unis.detail', uni_id=container.id))
    elif container.container_type == 'city':
        return redirect(url_for('unis.by_city')),
    elif container.container_type == 'subject':
        return redirect(url_for('unis.detail', uni_id=container.parent.id)),

def build_field_form(schema, field=None):
    from wtforms.validators import Required
    # Add a value field depending on the type of the field
    model = models.field_models[schema.data_type]
    form = forms.FieldForm.add_field('value',
        model.widget(schema.name,
            model.validators.append(Required())
        ))(obj=field)
    # Remove the comment field if it isn't allowed
    if not schema.permit_comment:
        del form.comment

    return form

@field_storage.route('/add/field/<int:container_id>/<int:schema_id>', methods=('GET', 'POST'))
@login_required
def add_field_values(container_id, schema_id):
    """
    Add a Field to a container: Show the Form to actually add the form
    """
    schema = models.Schema.query.get(schema_id)
    container = models.Container.query.get(container_id)
    form = build_field_form(schema)

    if form.validate_on_submit():
        model = models.field_models[schema.data_type]
        field = model(schema, container)
        field.value = form.value.data
        if schema.permit_comment:
            field.comment = form.comment.data
        db.session.add(field)
        return container_view(container)

    return render_template('field_form.html', action="add", form=form, schema=schema, container=container)

@field_storage.route('/edit/field/<int:field_id>/', methods=('GET', 'POST'))
@login_required
def edit_field(field_id):
    field = models.Field.query.get(field_id)
    form = build_field_form(field.field_type, field)

    if form.validate_on_submit():
        field.value = form.value.data
        if field.field_type.permit_comment:
            field.comment = form.comment.data
        db.session.add(field)
        return container_view(field.container)

    return render_template('field_form.html', action="edit", form=form, schema=field.field_type, container=field.container)

@field_storage.route('/delete/field/<int:field_id>')
@login_required
def delete_field(field_id):
    """
    Delete a field
    """
    field = models.Field.query.get(field_id)
    # delete the field
    if not field:
        flash(_("Cannot delete field: No such field"))
    else:
        db.session.delete(field)

    # redirect to field owner
    return container_view(field.container)
