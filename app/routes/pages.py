from flask import Blueprint, render_template
from app.services.tree_builder import build_root_tree

pages_bp = Blueprint('pages', __name__)


@pages_bp.get('/')
def index():
    tree = build_root_tree()
    current_folder = tree
    return render_template('index.html', tree=tree, current_folder=current_folder)
