from project import celery_app
from celery.schedules import crontab

# Scheduler schedules this task to run every minute
celery_app.conf.beat_schedule = {
    "async-fetch-videos-every-minute": {
        "task": "project.tasks.fetch",
        "schedule": 60.0
    }
}

