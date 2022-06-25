import os
from flask import url_for
import sqlalchemy as sa
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Category %r>' % self.name

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Roles %r>' % self.name

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    
    roles = db.relationship('Role')

    def __repr__(self):
        return '<User %r>' % self.login

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    year = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    publishing_house = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.name

    @property
    def rating(self):
        if self.rating_num > 0:
            return self.rating_sum/self.rating_num
        return 0

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(200), nullable=False, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    book = db.relationship('Books')

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return str(self.id) + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)