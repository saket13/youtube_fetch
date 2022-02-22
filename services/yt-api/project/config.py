import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BACKEND = os.getenv("CELERY_BACKEND")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE")
    broker_url = 'redis://redis:6379/0'
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Europe/Dublin'
    enable_utc = True