from flask import Blueprint, render_template


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/posts')
def posts():
    return 'pagina de blogposts'


@post_bp.route('/create')
def create():
    return 'pagina de blogposts'


@post_bp.route('/update/<int:post_id>')
def update(post_id):
    return f'pagina para actualizar el blogpost {post_id}'