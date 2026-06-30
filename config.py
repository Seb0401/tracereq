import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

def build_db_uri():
    if os.environ.get('DATABASE_URL'):
        return os.environ['DATABASE_URL']
    return URL.create(
        drivername='mysql+pymysql',
        username=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        database=os.environ.get('DB_NAME', 'tracereq'),
    )

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = build_db_uri()

config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}