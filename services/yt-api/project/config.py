import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path('.env')
load_dotenv(dotenv_path=ENV_PATH)

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BACKEND = os.getenv('CELERY_BACKEND')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    YOUTUBE_DATA_API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Europe/Dublin'
    enable_utc = True
    CACHE_TYPE = os.getenv('CACHE_TYPE')
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT')
    CACHE_REDIS_DB = os.getenv('CACHE_REDIS_DB')
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = os.getenv('CACHE_DEFAULT_TIMEOUT')
    ES_HOST = os.getenv('ES_HOST')
    ES_PORT = os.getenv('ES_PORT')