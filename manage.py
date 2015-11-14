#!/usr/bin/env python
import os
import config
from app import create_app, db
from app.auth.models import User, Role, Permission
from app.unis.models import Uni, City, Subject
from app.field_storage.models import Schema, Field
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return {
        'app': app,
        'db': db,
        'User': User,
        'Role': Role,
        'Permission': Permission,
        'Schema': Schema,
        'Field': Field,
        'Uni': Uni,
        'City': City,
        'Subject': Subject
    }

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def createsuperuser(username="root", email="root@localhost"):
    """
    Create a superuser
    """
    import getpass
    password = getpass.getpass()
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role is None:
        raise ValueError('Admin role not found. Did you initialize the database with manage.py initdb')
    # FIXME: check if the account exists first
    u = User(username=username, email=email, role=admin_role, password=password)
    db.session.add(u)
    db.session.commit()


@manager.command
def initdb():
    """
    Initialize the database on the first run
    """
    db.create_all()
    Role.insert_roles()
    if Schema.query.filter_by(name='name') is None:
        # Create name field
        name = Schema()
        name.name = 'name'
        name.description = 'A basic name field.'
        name.permit_comment = False
        name.weight = -1000
        name.data_type = "textfield"
        db.session.add(name)
    db.session.commit()

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittestTextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

