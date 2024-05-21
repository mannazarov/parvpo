import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    RABBITMQ_URL = os.environ.get('RABBITMQ_URL') or 'amqp://guest:guest@rabbitmq:5672/%2F'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
