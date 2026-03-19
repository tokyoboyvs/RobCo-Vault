from app.repositories.folders import get_root_folder, list_child_folders
from app.repositories.notes import list_notes_by_folder


def build_folder_node(folder_row):
    folder = dict(folder_row)

    child_folders = [
        build_folder_node(child_folder)
        for child_folder in list_child_folders(folder['id'])
    ]

    child_notes = [
        dict(note_row)
        for note_row in list_notes_by_folder(folder['id'])
    ]

    folder['folders'] = child_folders
    folder['notes'] = child_notes
    return folder


def build_root_tree():
    root_folder = get_root_folder()

    if root_folder is None:
        return None
    
    return build_folder_node(root_folder)
