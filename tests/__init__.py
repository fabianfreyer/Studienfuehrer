from flask import Flask
from flask.ext.testing import TestCase as GeneralTestCase
from app import create_app, db

class TestCase(GeneralTestCase):
    """
    A test case base class
    """
    def create_app(self):
        from manage import initdb
        app = create_app('testing')
        initdb()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
