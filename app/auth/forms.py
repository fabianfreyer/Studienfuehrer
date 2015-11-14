from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length
from wtforms import ValidationError
from flask.ext.babel import lazy_gettext as _

class LoginForm(Form):
    username = StringField(_('Username'), validators=[Required(), Length(1, 64)])
    password = PasswordField(_('Password'), validators=[Required()])
    submit = SubmitField(_('Login'))
