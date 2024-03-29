from flask import Blueprint, flash, redirect, render_template, request, flash, url_for
from app import db
from models import Category, Course, User, Review
from tools import CoursesFilter, ImageSaver, ReviewsFilter
from flask_login import current_user

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'name', 'short_desc', 'full_desc', 'author_id',
    'category_id'
]

PER_PAGE = 5
PER_PAGE_REVIEWS = 5

def params():
    return { p: request.form.get(p) for p in COURSE_PARAMS }

def search_params():
    return{
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids')
    }

def search_params_reviews(course_id, sort):
    return {
        'course_id': course_id,
        'sort': sort
    }

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    courses = CoursesFilter(**search_params()).perform()
    pagination = courses.paginate(page, PER_PAGE)
    courses = pagination.items
    categories = Category.query.all()
    rating = Course.rating
    return render_template('courses/index.html', 
                            courses=courses,
                            categories=categories,
                            search_params=search_params(),
                            pagination=pagination,
                            rating=rating
                            )

@bp.route('/new')
def new():
    categories = Category.query.all()
    users = User.query.all()
    return render_template('courses/new.html', categories=categories, users=users)

@bp.route('/create', methods=['POST'])
def create():

    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()

    course = Course(**params(), background_image_id=img.id)
    db.session.add(course)
    db.session.commit()

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>', methods=['POST', 'GET'])
def show(course_id):
    course = Course.query.get(course_id)
    if request.method == 'POST':
        text = request.form.get('review')
        mark = int(request.form.get('mark'))
        review = Review(rating=mark, text=text, course_id=course_id, user_id=current_user.get_id())
        course.rating_num += 1
        course.rating_sum += int(review.rating)
        db.session.add(review)
        db.session.commit()
        flash(f'Отзыв был успешно добавлен!', 'success')
    if request.args.get('show_all_reviews'):
        return redirect(url_for('courses.show_all_rewiews', course_id=course_id))  
    reviews = Review.query.filter_by(course_id=course_id).limit(5)
    flag = True
    if Review.query.filter_by(course_id=course_id, user_id=current_user.get_id()).first():
        flag = False
    return render_template('courses/show.html', course=course, reviews=reviews, flag=flag)


@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    sort = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    reviews = ReviewsFilter(course_id).perform_date_desc()
    course = Course.query.filter_by(id=course_id).first()
    pagination = reviews.paginate(page, PER_PAGE_REVIEWS)
    reviews = pagination.items 
    if sort == 'new':
        reviews = ReviewsFilter(course_id).perform_date_desc()
    if sort == 'old':
        reviews = ReviewsFilter(course_id).perform_date_asc()
    if sort == 'good':
        reviews = ReviewsFilter(course_id).perform_rating_desc()
    if sort == 'bad':
        reviews = ReviewsFilter(course_id).perform_rating_asc()
    return render_template('courses/reviews.html', reviews=reviews,
                            course=course, type_of_sort=sort, pagination=pagination, 
                            search_params=search_params_reviews(course_id, sort))
