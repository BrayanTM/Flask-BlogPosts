from flask import Flask
from blogapp import home, auth, post


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(post.post_bp)

    return app