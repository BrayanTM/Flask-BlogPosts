from flask import Flask
from blogapp import home, auth, post
from blogapp.db_con import db
from .models import User, Post


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(post.post_bp)

    with app.app_context():
        db.create_all()

    return app