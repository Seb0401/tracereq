from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    from app.routes.proyectos import bp_proyectos
    app.register_blueprint(bp_proyectos, url_prefix='/proyectos')

    return app
