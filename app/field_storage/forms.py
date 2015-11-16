from ..utils.redirect_back import RedirectForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms_components import SelectField
from wtforms.validators import Required
from flask.ext.babel import lazy_gettext as _

class SchemaForm(RedirectForm):
   name = StringField('Name', validators=[Required()])
   category = SelectField(_('Category'), coerce=int)
   description = TextAreaField('Description', validators=[Required()])
   data_type = SelectField('Type',
           choices=[('textfield', _('Text')),
                    ('integerfield', _('Numeric')),
                    ('boolean', _('Boolean'))])
   permit_comment = BooleanField(_('Permit Comment'))
   submit = SubmitField()

class FieldAddSelectTypeForm(RedirectForm):
    field_type = SelectField(_('Field Type'), coerce=int)
    submit = SubmitField(_('Next'))

class CategoryForm(RedirectForm):
   name = StringField('Name', validators=[Required()])
   submit = SubmitField()

class FieldForm(RedirectForm):
    @classmethod
    def add_field(cls, name, field):
        """
        Helper function to add a field to this form
        """
        setattr(cls, name, field)
        return cls

    comment = TextAreaField(_('Comment'))
    submit = SubmitField()
