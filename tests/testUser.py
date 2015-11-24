from tests import TestCase
from app import db

class TestUser(TestCase):
    def test_superuser(self):
        from app.auth.models import Role, User
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role is None:
            raise ValueError('Admin role not found. Did you initialize the database with manage.py initdb')
        user = User(username="testuser", email="testemail@testserver", role=admin_role, password="testpassword")
        db.session.add(user)
        db.session.commit()
        assert user in db.session
