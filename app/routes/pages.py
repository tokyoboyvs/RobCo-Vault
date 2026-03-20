from app.repositories.notes import create_note
from app.services.tree_builder import build_root_tree, build_folder_node
from flask import Blueprint, redirect, render_template, request, url_for
from app.repositories.folders import create_folder, delete_folder, get_folder_by_id, rename_folder

pages_bp = Blueprint('pages', __name__)


@pages_bp.get('/')
def index():
    tree = build_root_tree()
    folder_id = request.args.get('folder_id', type=int)

    if tree is None:
        current_folder = None
    elif folder_id is None:
        current_folder = tree
    else:
        folder_row = get_folder_by_id(folder_id)
        current_folder = build_folder_node(folder_row) if folder_row else tree
    
    return render_template(
        'index.html',
        tree=tree,
        current_folder=current_folder,
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
