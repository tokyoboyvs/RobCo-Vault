import sqlite3

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
