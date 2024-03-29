import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Course, Image, Review
from app import db, app

class CoursesFilter:
    def __init__(self, name, category_ids):
        self.name = name
        self.category_ids = category_ids
        self.query = Course.query

    def perform(self):
        self.__filter_by_name()
        self.___filter_by_category_ids()
        return self.query.order_by(Course.created_at.desc())

    def __filter_by_name(self):
        if self.name:
            self.query = self.query.filter(Course.name.ilike('%' + self.name + '%'))

    def ___filter_by_category_ids(self):
        if self.category_ids:
            self.query = self.query.filter(Course.category_id.in_(self.category_ids))

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

class ReviewsFilter:
    def __init__(self, course_id):
        self.query = Review.query.filter_by(course_id=course_id)

    def perform_date_desc(self):
        return self.query.order_by(Review.created_at.desc())

    def perform_date_asc(self):
        return self.query.order_by(Review.created_at.asc())

    def perform_rating_desc(self):
        return self.query.order_by(Review.rating.desc())

    def perform_rating_asc(self):
        return self.query.order_by(Review.rating.asc())