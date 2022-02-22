from project import celery_app
import json

@celery_app.task
def check():
    print("10 seconds stuff")