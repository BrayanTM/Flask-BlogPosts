from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from werkzeug.security import generate_password_hash, check_password_hash
from blogapp.db_con import db
from blogapp.models import User
from functools import wraps
from datetime import datetime
import cloudinary
import cloudinary.uploader
import os
import time


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Funciones auxiliares
@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def get_picture_url(public_id):
    return cloudinary.CloudinaryImage(public_id).build_url()


# Rutas
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(
            password, method=os.getenv("CRYPT_METHOD")
        )

        new_user = User(username=username, email=email, password=hashed_password)

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash(
                "Este nombre de usuario o correo electrónico ya existe. Por favor, elige uno diferente.",
                "danger",
            )
            time.sleep(3)
            return redirect(url_for("auth.register"))

        db.session.add(new_user)
        db.session.commit()

        flash("¡Registro exitoso! Por favor, inicia sesión.", "success")
        time.sleep(3)
        return redirect(url_for("auth.login"))
    if g.user:
        return redirect(url_for("post.posts"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            flash("¡Inicio de sesión exitoso!", "success")
            time.sleep(3)
            return redirect(url_for("post.posts"))
        else:
            flash(
                "Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.",
                "danger",
            )
            time.sleep(3)
            return redirect(url_for("auth.login"))
    if g.user:
        return redirect(url_for("post.posts"))
    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.index"))


@auth_bp.route("/profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile(user_id):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        photo = request.files["photo"]

        if password != confirm_password:
            flash(
                "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", "danger"
            )
            time.sleep(3)
            return redirect(url_for("auth.profile", user_id=user_id))

        hashed_password = generate_password_hash(
            password, method=os.getenv("CRYPT_METHOD")
        )

        user = User.query.get_or_404(user_id)
        user.username = username

        if password:
            if len(password) < 8:
                flash("La contraseña debe tener al menos 8 caracteres.", "danger")
                time.sleep(3)
                return redirect(url_for("auth.profile", user_id=user_id))
            user.password = hashed_password

        if photo:
            if user.avatar:
                cloudinary.uploader.destroy(user.avatar, resource_type="image")
            # Generar nombre único para el archivo
            timestamp = datetime.now().timestamp()
            public_id = f"blogapp/{int(timestamp)}"

            upload_result = cloudinary.uploader.upload(
                photo, public_id=public_id, folder="blogapp", resource_type="image"
            )
            user.avatar = upload_result["public_id"]
            user.avatar_url = get_picture_url(upload_result["public_id"])

        db.session.commit()
        flash("¡Perfil actualizado exitosamente!", "success")
        time.sleep(3)
        return redirect(url_for("auth.profile", user_id=user.id))
    user = User.query.get_or_404(user_id)
    return render_template("auth/profile.html", user=user)
