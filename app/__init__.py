import logging
from flask import Flask
from config import Config
from .extensions import db
from .models import Movie
from .seed import seed_movies


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    db.init_app(app)

    from .blueprints.main import main_bp
    from .blueprints.auth import auth_bp
    from .blueprints.movies import movies_bp
    from .blueprints.lists import lists_bp
    from .blueprints.payments import payments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(lists_bp)
    app.register_blueprint(payments_bp)

    @app.template_filter('brl')
    def brl(value):
        return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    with app.app_context():
        db.create_all()
        seed_movies()
        app.logger.info('Banco inicializado. Filmes cadastrados: %s', Movie.query.count())

    return app
