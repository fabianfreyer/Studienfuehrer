from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required
from wtforms import ValidationError

class SchemaForm(Form):
   name = StringField('Name', validators=[Required()])
   description = TextAreaField('Description', validators=[Required()])
   data_type = SelectField('Type',
           choices=[('textfield', 'Text'),
                    ('numericfield', 'Numeric'),
                    ('boolean', 'Boolean')])
   permit_comment = BooleanField('Permit Comment')
   submit = SubmitField()

class UniAddForm(Form):
    name = StringField('Name', validators=[Required()])
    city = SelectField('City', coerce=int)
    submit = SubmitField()

class CityAddForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField()
