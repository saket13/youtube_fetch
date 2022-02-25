from flask.cli import FlaskGroup
from project import app, db, es
from project.models import Video

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

@cli.command("create_es_index")
def create_index():
    print(es.ping())
    created = False
    index_name='videos'
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

if __name__ == "__main__":
    cli()
