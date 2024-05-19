from flask import Flask, request
from config import Config
import sqlite3
import logging
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация базы данных
    init_db()

    # Настройка логирования
    handler = RotatingFileHandler('/var/log/flask/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)  # Изменено на DEBUG
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Логирование ошибок
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"An error occurred: {e}")
        return str(e), 500

    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())

    @app.after_request
    def log_response_info(response):
        app.logger.debug('Response: %s', response.status)
        return response

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
