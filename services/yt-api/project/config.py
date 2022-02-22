import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BACKEND = 'redis://redis:6379/0'
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    YOUTUBE_DATA_API_KEY = ''
    DEFAULT_PUBLISH_TIME = '2020-01-22T12:32:39Z'
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Europe/Dublin'
    enable_utc = True
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'redis://redis:6379'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://redis:6379'
    CACHE_DEFAULT_TIMEOUT = 500