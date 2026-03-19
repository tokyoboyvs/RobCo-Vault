from app.db import get_db


def get_root_folder():
    db =get_db()
    return db.execute(
        '''
        SELECT id, name, parent_id, is_root, created_at, last_edit
        FROM folders
        WHERE is_root = 1
        LIMIT 1
        '''
    ).fetchone()


def get_folder_by_id(folder_id):
    db = get_db()
    return db.execute(
        '''
        SELECT id, name, parent_id, is_root, created_at, last_edit
        FROM folders
        WHERE id = ?
        LIMIT 1
        ''',
        (folder_id,),
    ).fetchone()


def list_child_folders(parent_id):
    db = get_db()
    return db.execute(
        '''
        SELECT id, name, parent_id, is_root, created_at, last_edit
        FROM folders
        WHERE parent_id = ?
        ORDER BY name COLLATE NOCASE
        ''',
        (parent_id,),
    ).fetchall()
