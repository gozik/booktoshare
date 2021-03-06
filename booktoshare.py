import click

from flask import current_app

from app import db, create_app
from app.models.auth import User, Role
from app.models.books import Book


def register(app):
    @app.cli.command("create_admin")
    @click.argument("password")
    def create_admin(password):
        pass # TODO


app = create_app()
register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,
            'Book': Book}




