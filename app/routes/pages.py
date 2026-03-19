from flask import Blueprint, render_template, request
from app.repositories.folders import get_folder_by_id
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
