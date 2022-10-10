from flask import Blueprint, flash, redirect, render_template, request, flash, url_for
from app import db
from models import Category, Book, User
from tools import BooksFilter, ImageSaver
from auth import check_rights

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
