from tkinter import Image
from flask import Blueprint, flash, redirect, render_template, request, flash, url_for
from app import db
from models import Category, Book, User, Image
from tools import BooksFilter, ImageSaver
from auth import check_rights
import bleach

bp = Blueprint('books', __name__, url_prefix='/books')

BOOK_PARAMS = [
    'name', 'short_desc', 'author_id', 'category_id'
]

PER_PAGE = 5

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }

def search_params():
    return{
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids')
    }

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = BooksFilter(**search_params()).perform()
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    categories = Category.query.all()
    return render_template('books/index.html', 
                            books=books,
                            categories=categories,
                            search_params=search_params(),
                            pagination=pagination,
                            )

@bp.route('/new')
@check_rights('create')
def new():
    categories = Category.query.all()
    users = User.query.all()
    return render_template('books/new.html', categories=categories, users=users)

@bp.route('/create', methods=['POST'])
def create():

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()

    book = Book(**params(), background_image_id=img.id)
    db.session.add(book)
    db.session.commit()

    flash(f'Книга {book.name} была успешно добавлена!', 'success')

    return redirect(url_for('books.index'))

@bp.route('/<int:book_id>', methods=['POST', 'GET'])
def show(book_id):
    book = Book.query.get(book_id)
    return render_template('books/show.html', book=book)

@bp.route('/<int:book_id>/edit')
@check_rights('update')
def edit(book_id):
    book = Book.query.get(book_id)
    users = User.query.all()
    categories  = Category.query.all()
    return render_template('books/edit.html', book=book, categories=categories, users=users)

@bp.route('/<int:book_id>/update', methods=['POST'])
@check_rights('update')
def update(book_id):
    book = Book.query.get(book_id)

    try:
        name = request.form.get('name')
        if len(name) > 0 : 
            book.name = name
        else: 
            1/0
        
        short_desc = bleach.clean(request.form.get('short_desc')) 
        if len(request.form.get('short_desc')) > 0 : 
            book.short_desc = short_desc
        else: 
            1/0
        
        category = request.form.get('category')
        if len(category) != 0:
            book.category_id = category
        
        author = request.form.get('author')
        if len(author) != 0:
            book.author_id = author

        db.session.add(book)
        db.session.commit()
    except:
        flash('Заполните все поля. Ошибка сохранения', 'danger')
        return redirect(url_for('books.edit', book_id=book_id))

    flash(f'Книга "{book.name}" была успешно обновлена.', 'success')
    return redirect(url_for('index'))

@bp.route('/<int:book_id>/delete', methods=['POST'])
@check_rights('delete')
def delete(book_id):
    # img = Image.query.filter(Book.background_image_id == book_id).first()
    # img_del = ImageSaver(img)
    # img_del.delete_img(img.id)

    Book.query.filter(Book.id == book_id).delete()
    db.session.commit()

    flash(f'Книга была удалена', 'success')
    return redirect(url_for('books.index'))