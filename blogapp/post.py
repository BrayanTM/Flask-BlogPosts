from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from blogapp.db_con import db
from blogapp.models import Post
from .auth import login_required


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/posts')
@login_required
def posts():
    posts = Post.query.filter_by(author=g.user.id).all()
    return render_template('admin/posts.html', posts=posts)


@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        url = request.form['url']
        url = url.lower().replace(' ', '-')
        title = request.form['title']
        description = request.form['description']
        content = request.form['ckeditor']
        post = Post(author=g.user.id, url=url, title=title, info=description, content=content)

        existing_post = Post.query.filter_by(url=url).first()
        if existing_post:
            flash('La URL ya existe. Por favor, elige una diferente.', 'danger')
            return redirect(url_for('post.create'))

        db.session.add(post)
        db.session.commit()
        flash('Blog creado exitosamente', 'success')
        return redirect(url_for('post.posts'))
    return render_template('admin/create.html')


@post_bp.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.info = request.form['description']
        post.content = request.form['ckeditor']
        db.session.commit()
        flash('Blog actualizado exitosamente', 'success')
        return redirect(url_for('post.posts'))
    return render_template('admin/update.html', post=post)


@post_bp.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != g.user.id:
        flash('No tienes permisos para eliminar este blog', 'danger')
        return redirect(url_for('post.posts'))
    db.session.delete(post)
    db.session.commit()
    flash('Blog eliminado exitosamente', 'success')
    return redirect(url_for('post.posts'))