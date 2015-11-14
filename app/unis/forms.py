from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required
from flask.ext.babel import lazy_gettext as _

class SubjectAddForm(Form):
    name = StringField(_('Name'), validators=[Required()])
    uni = SelectField(_('University'), coerce=int)
    submit = SubmitField()

class UniAddForm(Form):
    name = StringField(_('Name'), validators=[Required()])
    city = SelectField(_('City'), coerce=int)
    submit = SubmitField()

class CityAddForm(Form):
    name = StringField(_('Name'), validators=[Required()])
    submit = SubmitField()
