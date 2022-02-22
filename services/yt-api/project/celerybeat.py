from project import celery_app
from celery.schedules import crontab


celery_app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "project.tasks.check",
        "schedule": 10.0
    }
}

