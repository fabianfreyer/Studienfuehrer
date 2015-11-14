from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required

class SchemaForm(Form):
   name = StringField('Name', validators=[Required()])
   description = TextAreaField('Description', validators=[Required()])
   data_type = SelectField('Type',
           choices=[('textfield', 'Text'),
                    ('integerfield', 'Numeric'),
                    ('boolean', 'Boolean')])
   permit_comment = BooleanField('Permit Comment')
   submit = SubmitField()

class FieldAddSelectTypeForm(Form):
    field_type = SelectField('Field Type', coerce=int)
    submit = SubmitField('Next')

class FieldAddForm(Form):
    @classmethod
    def add_field(cls, name, field):
        """
        Helper function to add a field to this form
        """
        setattr(cls, name, field)
        return cls

    comment = TextAreaField('Comment')
    submit = SubmitField()
