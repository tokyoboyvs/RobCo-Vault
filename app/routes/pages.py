from app.services.tree_builder import build_root_tree, build_folder_node
from flask import Blueprint, redirect, render_template, request, url_for
from app.repositories.folders import create_folder, delete_folder, get_folder_by_id, rename_folder
from app.repositories.notes import create_note, delete_note, get_note_by_id, rename_note, update_note_content

pages_bp = Blueprint('pages', __name__)


@pages_bp.get('/')
def index():
    tree = build_root_tree()
    folder_id = request.args.get('folder_id', type=int)
    note_id = request.args.get('note_id', type=int)

    if tree is None:
        current_folder = None
        current_note = None
    else:
        current_note = None

        if note_id is not None:
            note_row = get_note_by_id(note_id)

            if note_row is not None:
                current_note = dict(note_row)
                folder_row = get_folder_by_id(note_row['folder_id'])
                current_folder = build_folder_node(folder_row) if folder_row else tree
            else:
                current_folder = tree
        elif folder_id is None:
            current_folder = tree
        else:
            folder_row = get_folder_by_id(folder_id)
            current_folder = build_folder_node(folder_row) if folder_row else tree
    
    return render_template(
        'index.html',
        tree=tree,
        current_folder=current_folder,
        current_note=current_note,
    )


@pages_bp.post('/folders/create')
def create_folder_action():
    parent_id = request.form.get('parent_id', type=int)
    name = request.form.get('name', '', type=str).strip()

    if not parent_id:
        return redirect(url_for('pages.index'))
    
    if not name:
        return redirect(url_for('pages.index', folder_id=parent_id))
    
    create_folder(name=name, parent_id=parent_id)
    return redirect(url_for('pages.index', folder_id=parent_id))


@pages_bp.post('/folders/rename')
def rename_folder_action():
    folder_id = request.form.get('folder_id', type=int)
    name = request.form.get('name', '', type=str).strip()

    if not folder_id:
        return redirect(url_for('pages.index'))
    
    folder_row = get_folder_by_id(folder_id)

    if folder_row is None:
        return redirect(url_for('pages.index'))
    
    if folder_row['is_root']:
        return redirect(url_for('pages.index', folder_id=folder_id))
    
    if not name:
        return redirect(url_for('pages.index', folder_id=folder_id))
    
    rename_folder(folder_id=folder_id, name=name)
    return redirect(url_for('pages.index', folder_id=folder_id))


@pages_bp.post('/folders/delete')
def delete_folder_action():
    folder_id = request.form.get('folder_id', type=int)

    if not folder_id:
        return redirect(url_for('pages.index'))
    
    folder_row = get_folder_by_id(folder_id)

    if folder_row is None:
        return redirect(url_for('pages.index'))
    
    if folder_row['is_root']:
        return redirect(url_for('pages.index', folder_id=folder_id))
    
    parent_id = folder_row['parent_id']
    delete_folder(folder_id)

    if parent_id is None:
        return redirect(url_for('pages.index'))
    
    return redirect(url_for('pages.index', folder_id=parent_id))


@pages_bp.post('/notes/create')
def create_note_action():
    folder_id = request.form.get('folder_id', type=int)
    name = request.form.get('name', '', type=str).strip()

    if not folder_id:
        return redirect(url_for('pages.index'))
    
    folder_row = get_folder_by_id(folder_id)

    if folder_row is None:
        return redirect(url_for('pages.index'))
    
    if not name:
        return redirect(url_for('pages.index', folder_id=folder_id))
    
    create_note(name=name, folder_id=folder_id)
    return redirect(url_for('pages.index', folder_id=folder_id))


@pages_bp.post('/notes/save')
def save_note_action():
    note_id = request.form.get('note_id', type=int)
    content = request.form.get('content', '', type=str)

    if not note_id:
        return redirect(url_for('pages.index'))

    note_row = get_note_by_id(note_id)

    if note_row is None:
        return redirect(url_for('pages.index'))

    update_note_content(note_id=note_id, content=content)
    return redirect(url_for('pages.index', note_id=note_id))


@pages_bp.post('/notes/rename')
def rename_note_action():
    note_id = request.form.get('note_id', type=int)
    name = request.form.get('name', '', type=str).strip()

    if not note_id:
        return redirect(url_for('pages.index'))

    note_row = get_note_by_id(note_id)

    if note_row is None:
        return redirect(url_for('pages.index'))

    if not name:
        return redirect(url_for('pages.index', note_id=note_id))

    rename_note(note_id=note_id, name=name)
    return redirect(url_for('pages.index', note_id=note_id))


@pages_bp.post('/notes/delete')
def delete_note_action():
    note_id = request.form.get('note_id', type=int)

    if not note_id:
        return redirect(url_for('pages.index'))

    note_row = get_note_by_id(note_id)

    if note_row is None:
        return redirect(url_for('pages.index'))

    folder_id = note_row['folder_id']
    delete_note(note_id)
    return redirect(url_for('pages.index', folder_id=folder_id))
