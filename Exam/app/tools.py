import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Book, Image
from app import db, app

class BooksFilter:
    def __init__(self, name, category_ids):
        self.name = name
        self.category_ids = category_ids
        self.query = Book.query

    def perform(self):
        self.__filter_by_name()
        self.___filter_by_category_ids()
        return self.query.order_by(Book.created_at.desc())

    def __filter_by_name(self):
        if self.name:
            self.query = self.query.filter(Book.name.ilike('%' + self.name + '%'))

    def ___filter_by_category_ids(self):
        if self.category_ids:
            self.query = self.query.filter(Book.category_id.in_(self.category_ids))

class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Image(
            file_name=file_name,
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash)
        db.session.add(self.img)
        db.session.commit()
        self.file.save(
            os.path.join(app.config['UPLOAD_FOLDER'],
                         self.img.storage_filename))
        
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Image.query.filter(Image.md5_hash == self.md5_hash).first()

    def delete_img(self, id):
        self.img = Image.query.get(id)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], self.img.storage_filename))