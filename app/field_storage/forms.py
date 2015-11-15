from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required
from flask.ext.babel import lazy_gettext as _

class SchemaForm(Form):
   name = StringField('Name', validators=[Required()])
   description = TextAreaField('Description', validators=[Required()])
   data_type = SelectField('Type',
           choices=[('textfield', _('Text')),
                    ('integerfield', _('Numeric')),
                    ('boolean', _('Boolean'))])
   permit_comment = BooleanField(_('Permit Comment'))
   submit = SubmitField()

class FieldAddSelectTypeForm(Form):
    field_type = SelectField(_('Field Type'), coerce=int)
    submit = SubmitField(_('Next'))

class FieldForm(Form):
    @classmethod
    def add_field(cls, name, field):
        """
        Helper function to add a field to this form
        """
        setattr(cls, name, field)
        return cls

    comment = TextAreaField(_('Comment'))
    submit = SubmitField()
