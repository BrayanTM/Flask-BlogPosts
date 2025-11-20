from flask import Flask
from blogapp import home, auth, post
from blogapp.db_con import db
from flask_migrate import Migrate
import cloudinary
import os


migrate = Migrate()


def create_app():
    app = Flask(__name__)

    cloudinary.config(cloudinary_url=os.getenv("CLOUDINARY_URL"))

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home.home_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(post.post_bp)

    with app.app_context():
        db.create_all()

    return app
