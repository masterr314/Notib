from click import command, echo
from flask.cli import with_appcontext
from extensions import db


@command('create_db')
@with_appcontext
def create_db():
    """CLI command for creating db"""
    db.create_all()
    echo('DB created!')


@command('drop_db')
@with_appcontext
def drop_db():
    """CLI command for dropping db"""
    db.drop_all()
    echo('DB dropped!')
