import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify
from flasgger import Swagger
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from .models import db

DEFAULT_DATABASE_URL = 'sqlite:///futebol.db'
migrate = Migrate()


def _as_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {'1', 'true', 't', 'yes', 'y', 'on'}


def _init_database(app):
    retries = int(os.getenv('DB_INIT_RETRIES', '10'))
    delay = float(os.getenv('DB_INIT_DELAY', '2'))

    with app.app_context():
        for attempt in range(1, retries + 1):
            try:
                db.create_all()
                app.logger.info('Banco inicializado com sucesso.')
                return
            except Exception as exc:
                db.session.remove()
                app.logger.warning(
                    'Tentativa %s/%s de inicializar o banco falhou: %s',
                    attempt,
                    retries,
                    exc,
                )
                if attempt == retries:
                    app.logger.warning(
                        'A aplicacao iniciou, mas o banco nao estava disponivel.'
                    )
                    return
                time.sleep(delay)


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        DEFAULT_DATABASE_URL,
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
    app.config['SWAGGER'] = {
        'title': 'API Futebol Flask',
        'uiversion': 3,
    }
    app.url_map.strict_slashes = False

    if test_config:
        app.config.update(test_config)

    Swagger(
        app,
        template={
            'info': {
                'title': 'API Futebol Flask',
                'version': '1.1.0',
                'description': (
                    'API em Flask com Flasgger para gerenciamento de times, '
                    'jogadores, estadios e partidas.'
                ),
            }
        },
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.times import times_bp
    from .blueprints.jogadores import jogadores_bp
    from .blueprints.estadios import estadios_bp
    from .blueprints.partidas import partidas_bp

    app.register_blueprint(times_bp, url_prefix='/times')
    app.register_blueprint(jogadores_bp, url_prefix='/jogadores')
    app.register_blueprint(estadios_bp, url_prefix='/estadios')
    app.register_blueprint(partidas_bp, url_prefix='/partidas')

    @app.get('/')
    def home():
        """
        Informacoes basicas da API
        ---
        responses:
          200:
            description: Status da API
        """
        return jsonify(
            {
                'message': 'API Futebol Flask no ar.',
                'docs': '/apidocs/',
                'health': '/health',
                'endpoints': ['/times', '/jogadores', '/estadios', '/partidas'],
            }
        )

    @app.get('/health')
    def health():
        """
        Healthcheck da aplicacao
        ---
        responses:
          200:
            description: API online
        """
        return jsonify({'status': 'ok'}), 200

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc):
        return jsonify({'error': exc.description}), exc.code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(exc):
        db.session.rollback()
        app.logger.warning('Erro de integridade: %s', exc)
        return jsonify({'error': 'Violacao de integridade no banco de dados.'}), 409

    @app.errorhandler(Exception)
    def handle_generic_exception(exc):
        db.session.rollback()
        app.logger.exception('Erro interno nao tratado: %s', exc)
        return jsonify({'error': 'Erro interno do servidor.'}), 500

    if _as_bool(os.getenv('AUTO_CREATE_TABLES'), default=True):
        _init_database(app)

    return app
