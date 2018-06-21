import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('postgres://wpwjvzuigjsecx:9d26ea380126dda79a04a3855ef04b83837ce482d9cd84b86dc4cd0daab52517@ec2-54-204-2-26.compute-1.amazonaws.com:5432/d784h8nod9aubj') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False