from app.db import get_db


def list_notes_by_folder(folder_id):
    db = get_db()
    return db.execute(
        '''
        SELECT id, name, folder_id, created_at, last_edit
        FROM notes
        WHERE folder_id = ?
        ORDER BY name COLLATE NOCASE
        ''',
        (folder_id,),
    ).fetchall()
