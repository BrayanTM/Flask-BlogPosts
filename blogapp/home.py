from flask import Blueprint, render_template, request
from blogapp.models import User, Post


home_bp = Blueprint('home', __name__)


# Funciones Auxiliares
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user


def search_posts(query):
    results = Post.query.filter(
        (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
    ).all()
    return results


# Rutas
@home_bp.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()

    if request.method == 'POST':
        search_query = request.form.get('search')
        if search_query:
            posts = search_posts(search_query)
            value = 'hidden'
            return render_template('index.html', posts=posts, get_user=get_user, value=value)

    return render_template('index.html', posts=posts, get_user=get_user)


@home_bp.route('/blog/<url>')
def blog_post(url):
    post = Post.query.filter_by(url=url).first_or_404()
    return render_template('blog.html', post=post, get_user=get_user)