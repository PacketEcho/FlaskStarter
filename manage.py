from flask.cli import FlaskGroup

from autoapp import app
from flaskstarter.extensions import db

cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    db.create_all()


@cli.command('drop_db')
def drop_db():
    db.drop_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
