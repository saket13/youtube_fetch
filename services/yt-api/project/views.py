from project import app, db, celery_app
from project.models import Video


@app.route("/hi")
def hello():
    
    return 'Done'