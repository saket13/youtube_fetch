from flask.cli import FlaskGroup
from project import app, db
from project.models import Video

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()
