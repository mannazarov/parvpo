from logging.handlers import RotatingFileHandler
from redis import Redis
from flask import Flask, request
from app.models import get_tasks
from config import Config
import sqlite3
import logging
from pythonjsonlogger import jsonlogger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация базы данных
    init_db()

    # Настройка логирования в файл
    handler = RotatingFileHandler('app.log', maxBytes=200000, backupCount=10)
    handler.setLevel(logging.DEBUG)

    # Используем JSONFormatter для логирования в формате JSON
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Настройка логирования werkzeug (HTTP-запросы)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)

    # Логирование ошибок
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error("An error occurred", exc_info=e)
        return str(e), 500

    @app.before_request
    def log_request_info():
        app.logger.debug('Request received', extra={
            'headers': dict(request.headers),
            'body': request.get_data().decode('utf-8')
        })

    @app.after_request
    def log_response_info(response):
        app.logger.debug('Response sent', extra={'status': response.status})
        return response

    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    #app.redis = Redis.from_url(app.config['REDIS_URL'])

    # Прогрев кэша при старте
#    @app.before_first_request
 #   def warm_up_cache():
  #      with app.app_context():
   #         get_tasks()


    # Регистрация маршрутов
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    app.logger.info('App started')

    return app


def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
