from blogapp.db_con import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, username, email, password, avatar=None):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar


    def __repr__(self):
        return f"User: '{self.username}'"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=True)
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, author, title, content, url=None, info=None):
        self.author = author
        self.title = title
        self.content = content
        self.url = url
        self.info = info

    def __repr__(self):
        return f"Post: '{self.title}' by User ID: '{self.author}'"
