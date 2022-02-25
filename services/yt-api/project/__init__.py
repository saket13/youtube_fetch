from celery import Celery
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
cache = Cache(app)

def make_celery(app):
    celery = Celery(app.import_name, include=['project.tasks'])
    celery.conf.update(app.config)
    celery.config_from_object("project.config.Config")
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery_app = make_celery(app)

es = Elasticsearch(hosts=[{"host": "elasticsearch"}], retry_on_timeout=True)

from project.views import *