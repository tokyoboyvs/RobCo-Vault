from flask import Blueprint, redirect, render_template, request, url_for
from app.repositories.folders import create_folder, get_folder_by_id
from app.services.tree_builder import build_root_tree, build_folder_node

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
