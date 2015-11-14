from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required

class SubjectAddForm(Form):
    name = StringField('Name', validators=[Required()])
    uni = SelectField('University', coerce=int)
    submit = SubmitField()

class UniAddForm(Form):
    name = StringField('Name', validators=[Required()])
    city = SelectField('City', coerce=int)
    submit = SubmitField()

class CityAddForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField()
