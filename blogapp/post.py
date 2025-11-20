from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from blogapp.db_con import db
from blogapp.models import Post
from .auth import login_required


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/posts')
@login_required
def posts():
    return render_template('admin/posts.html')


@post_bp.route('/create')
@login_required
def create():
    return render_template('admin/create.html')


@post_bp.route('/update/<int:post_id>')
@login_required
def update(post_id):
    return render_template('admin/update.html')