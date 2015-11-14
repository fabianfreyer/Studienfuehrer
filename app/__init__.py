from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.babel import Babel
from config import config
from flask.json import JSONEncoder as BaseEncoder
from speaklater import _LazyString


bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

class JSONEncoder(BaseEncoder):
    """
    JSON encoder to enable serializing lazy strings
    """
    def default(self, o):
        if isinstance(o, _LazyString):
            return str(o)
        return BaseEncoder.default(self, o)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.json_encoder = JSONEncoder
    config[config_name].init_app(app)

    babel = Babel(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .field_storage import field_storage as field_storage_blueprint
    app.register_blueprint(field_storage_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .unis import unis as unis_blueprint
    app.register_blueprint(unis_blueprint)

    return app

