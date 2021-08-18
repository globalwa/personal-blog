import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    CKEDITOR_PKG_TYPE = 'standart'
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = 'upload'
    UPLOADED_PATH = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = ['jpg', 'gif', 'png', 'jpeg']
    POSTS_PER_PAGE = 5