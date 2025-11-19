from flask import Blueprint, render_template


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register')
def register():
    return render_template('auth/register.html')


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    return 'pagina de blogposts'


@auth_bp.route('/profile')
def profile():
    return render_template('auth/profile.html')