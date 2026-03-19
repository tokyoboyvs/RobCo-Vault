import click
import sqlite3
from pathlib import Path
from flask import current_app, g


def get_db():
    if 'db' not in g:
        db_path = current_app.config['DATABASE_PATH']
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    
    return g.db


def close_db(_error=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema_path = Path(current_app.root_path) / 'schema.sql'

    with schema_path.open('r', encoding='utf-8') as schema_file:
        db.executescript(schema_file.read())


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
