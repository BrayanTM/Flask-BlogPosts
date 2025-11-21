import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    
    # SQLAlchemy requiere 'postgresql://' en lugar de 'postgresql+psycopg2://'
    database_url = os.getenv('DATABASE_URL', '')
    if database_url.startswith('postgresql+psycopg2://'):
        database_url = database_url.replace('postgresql+psycopg2://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url

    CKEDITOR_PKG_TYPE = 'full'