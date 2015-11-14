from .. import db
from sqlalchemy.orm.collections import attribute_mapped_collection
import wtforms
from wtforms.validators import Required

class Schema(db.Model):
    """
    Metadata describing a field type
    """
    __tablename__ = 'field_schema'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.Text())
    permit_comment = db.Column(db.Boolean())
    weight = db.Column(db.Integer)
    data_type = db.Column(db.Enum("textfield", "integerfield", "boolean"))

    def __repr__(self):
        return "<Field: (%s) %s>" % (self.data_type, self.name)

class Field(db.Model):
    """
    A field containing data
    """
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    widget = None
    validators = []
    type_id = db.Column(db.Integer, db.ForeignKey('field_schema.id'))
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    container = db.relationship('Container',
            lazy='joined',
            join_depth=2,
            back_populates='fields')
    _comment = db.Column('comment', db.String())
    field_type = db.relationship('Schema', backref='fields')
    data_type = db.column_property(
            db.select([Schema.__table__.c.data_type]).where(Schema.__table__.c.id == type_id))
    __mapper_args__ = {
            'polymorphic_identity': 'field',
            'polymorphic_on': data_type,
            'with_polymorphic': '*'
            }

    def __init__(self, schema, container):
        self.field_type = schema
        self.container = container

    @property
    def name(self):
        return self.field_type.name

    @property
    def description(self):
        return self.field_type.description

    @property
    def permit_comment(self):
        return self.field_type.permit_comment

    @property
    def comment(self):
        return self._comment if self.permit_comment else None

    @comment.setter
    def comment(self, value):
        if self.permit_comment:
            self._comment = value
        else:
            raise AttributeError("Cannot set comment")


class TextField(Field):
    __tablename__ = 'textfield'
    __mapper_args__ = {
            'polymorphic_identity': 'textfield'
            }
    id = db.Column(db.Integer, db.ForeignKey('field.id'), primary_key=True)
    value = db.Column(db.String)
    widget = wtforms.StringField

    def __repr__(self):
        return "TextField(%s: %s)" % (self.name, self.value)


class IntegerField(Field):
    __tablename__ = 'integerfield'
    __mapper_args__ = {
            'polymorphic_identity': 'integerfield'
            }
    id = db.Column(db.Integer, db.ForeignKey('field.id'), primary_key=True)
    value = db.Column(db.Integer)
    # FIXME: add an integer validator here
    widget = wtforms.StringField

    def __repr__(self):
        return "IntField(%s: %d)" % (self.name, self.value)

class BooleanField(Field):
    __tablename__ = 'booleanfield'
    __mapper_args__ = {
            'polymorphic_identity': 'boolean'
            }
    id = db.Column(db.Integer, db.ForeignKey('field.id'), primary_key=True)
    value = db.Column(db.Boolean())
    widget = wtforms.BooleanField

    def __repr__(self):
        return "BooleanField(%s: %d)" % (self.name, self.value)

field_models = {
    'textfield':  TextField,
    'boolean': BooleanField,
    'integerfield': IntegerField,
}


class Container(db.Model):
    """
    Metaclass for a fieldable entity.
    """
    __tablename__ = 'container'
    container_type = db.Column(db.Enum("text", "numeric", "boolean"))
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    parent = db.relationship('Container', backref='children', remote_side=[id])
    fields = db.relationship('Field',
            collection_class=attribute_mapped_collection('name'),
            back_populates='container')
    container_type = db.Column(db.Enum("uni", "subject", "city"))
    __mapper_args__ = {
            'polymorphic_on': container_type
            }


class Uni(Container):
    __tablename__ = 'uni'
    __mapper_args__ = {
            'polymorphic_identity': 'uni'
            }
    id = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)

    def __init__(self, city):
        self.parent = city

    def __repr__(self):
        if 'name' in self.fields:
            return "<Uni: %s>" % self.fields['name'].value
        else:
            return "<Uni>" % self


class City(Container):
    __tablename__ = 'city'
    __mapper_args__ = {
            'polymorphic_identity': 'city'
            }
    id = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)

    def __repr__(self):
        if 'name' in self.fields:
            return "<City: %s>" % self.fields['name'].value
        else:
            return "<City>" % self


class Subject(Container):
    __tablename__ = 'subject'
    __mapper_args__ = {
            'polymorphic_identity': 'subject'
            }
    id = db.Column(db.Integer, db.ForeignKey('container.id'), primary_key=True)

    def __init__(self, uni):
        self.parent = uni

    def __repr__(self):
        if 'name' in self.fields:
            return "<Subject: %s>" % self.fields['name'].value
        else:
            return "<Subject>" % self

