from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.String)
    updated_at = db.Column(db.DateTime)
    baked_goods = db.relationship('BakedGood', backref='bakery', lazy=True)

    serialize_only = ('id', 'name', 'created_at', 'updated_at', 'baked_goods')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'baked_goods': [baked_good.to_dict() for baked_good in self.baked_goods]
        }

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.String)
    updated_at = db.Column(db.DateTime)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'), nullable=False)

    serialize_only = ('id', 'name', 'price', 'created_at', 'updated_at', 'bakery')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'bakery': self.bakery.to_dict() if self.bakery else None
        }