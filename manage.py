import sys

from flask.cli import FlaskGroup

from sistema import create_app, db
from sistema.api.models.tarefa import Tarefa


app = create_app()
cli = FlaskGroup(create_app=create_app)  # new


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()