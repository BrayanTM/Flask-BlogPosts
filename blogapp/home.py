from flask import Blueprint, render_template


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/blog')
def blog():
    return render_template('blog.html')