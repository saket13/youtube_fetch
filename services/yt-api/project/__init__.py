from celery import Celery
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BROKER_URL'],
                    broker=app.config['CELERY_BACKEND'], include=['project.tasks'])
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


@app.route("/")
def hello_world():
    return jsonify(hello="world")
