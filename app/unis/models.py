from .. import db
from .. import field_storage

class Uni(field_storage.models.Container):
    __tablename__ = 'uni'
    __mapper_args__ = {
            'polymorphic_identity': 'uni'
            }
    id = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)

    def __init__(self, city):
        self.parent = city

class City(field_storage.models.Container):
    __tablename__ = 'city'
    __mapper_args__ = {
            'polymorphic_identity': 'city'
            }
    id = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)

class Subject(field_storage.models.Container):
    __tablename__ = 'subject'
    __mapper_args__ = {
            'polymorphic_identity': 'subject'
            }
    id = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)

    def __init__(self, uni):
        self.parent = uni
