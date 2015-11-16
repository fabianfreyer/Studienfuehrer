from .. import db
from sqlalchemy.orm.collections import attribute_mapped_collection
import wtforms
from wtforms.validators import Required
import datetime
from flask import current_app
from collections import defaultdict

class Schema(db.Model):
    """
    Metadata describing a field type
    """
    __tablename__ = 'field_schema'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.Text())
    permit_comment = db.Column(db.Boolean())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
            lazy='joined',
            join_depth=2,
            back_populates='schemata')
    weight = db.Column(db.Integer, default=0)
    data_type = db.Column(db.Enum("textfield", "integerfield", "boolean"))

    def __repr__(self):
        return "<Field: (%s) %s>" % (self.data_type, self.name)

class Field(db.Model):
    class UpdateTimestampExtension(db.MapperExtension):
        def before_update(self, mapper, connection, target):
            """
            Update the timestamp
            """
            target.timestamp = datetime.datetime.now()

        def before_insert(self, mapper, connection, target):
            """
            Update the timestamp
            """
            target.timestamp = datetime.datetime.now()
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
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    data_type = db.column_property(
            db.select([Schema.__table__.c.data_type]).where(Schema.__table__.c.id == type_id))
    __mapper_args__ = {
            'extension': UpdateTimestampExtension(),
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

    @property
    def category(self):
        return self.field_type.category

    @property
    def age(self):
        return datetime.datetime.now()-self.timestamp

    @property
    def outdated(self):
        return (self.age >= current_app.config['FIELD_WARN_OUTDATED'])

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
    class _CategoryPair(object):
        def __init__(self):
            self._category = None
            self._fields = {}

        def __repr__(self):
            return "<CategoryInstance(%s): %r>" % (self.category.name, self._fields)

        def __getitem__(self, key):
            id_ = self._fields[key]
            return Field.query.get(id_)

        def __iter__(self):
            return (self[key] for key in self._fields)

        @property
        def category(self):
            return Category.query.get(self._category)

        @category.setter
        def category(self, value):
            self._category = value.id

        def __call__(self):
            return self.category

        def append(self, field):
            self.category = field.category
            self._fields[field.name] = field.id

        def remove(self, field):
            del self._fields[field.field_type.name]

    __tablename__ = 'container'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    parent = db.relationship('Container', backref='children', remote_side=[id])
    fields = db.relationship('Field',
            cascade='all, delete-orphan',
            collection_class=attribute_mapped_collection('name'),
            back_populates='container')
    container_type = db.Column(db.Enum("uni", "subject", "city"))
    __mapper_args__ = {
            'polymorphic_on': container_type
            }

    @property
    def categories(self):
        res = defaultdict(self._CategoryPair)
        for field in self.fields.values():
            res[field.category.name].append(field)
        return res


class Category(db.Model):
    """
    Metaclass for categories to group fields by.
    """
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    schemata = db.relationship('Schema',
            lazy='subquery',
            cascade='all, delete-orphan',
            collection_class=attribute_mapped_collection('name'),
            back_populates='category')

    def __repr__(self):
        return "<Category: %s>" % self.name
