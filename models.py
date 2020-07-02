from app import app
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config['SECRET_KEY'] = 'mysecretkeyyes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gunawan:Belajar2020@192.168.100.99/hadi_produk_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db = SQLAlchemy(app)
Migrate(app,db)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))

    def __init__(self,username,passw):
        self.username = username
        self.password = generate_password_hash(passw)

    def check_password(self,passw):
        return check_password_hash(self.password,passw)

    def __repr__(self):
        return f"username:{self.username}"


class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    groupname = db.Column(db.String(64))

    products = db.relationship('Product',backref='grup',lazy=True)

    def __repr__(self):
        return f"groupname:{self.groupname}"


class Brand(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    brandname = db.Column(db.String(64))

    products = db.relationship('Product',backref='merek',lazy=True)

    def __repr__(self):
        return f"brandname:{self.brandname}"

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    photo = db.Column(db.String(128))

    group_id = db.Column(db.Integer,db.ForeignKey('group.id'))
    brand_id = db.Column(db.Integer,db.ForeignKey('brand.id'))

    def __repr__(self):
        return f"Nama Produk:{self.name} -- Harga:{self.price} --group_id:{self.group_id} --brand_id:{self.brand_id}"
