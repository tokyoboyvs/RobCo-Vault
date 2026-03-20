const STORAGE_KEY = "robco-vault:collapsed-folders";

function readCollapsedFolders() {
  try {
    const rawValue = window.localStorage.getItem(STORAGE_KEY);
    const parsedValue = rawValue ? JSON.parse(rawValue) : [];
    return Array.isArray(parsedValue) ? parsedValue : [];
  } catch {
    return [];
  }
}

function writeCollapsedFolders(folderIds) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(folderIds));
}

function applyFolderState(folderId, isCollapsed) {
  const children = document.querySelector(`[data-folder-children="${folderId}"]`);
  const notes = document.querySelector(`[data-folder-notes="${folderId}"]`);
  const toggle = document.querySelector(`[data-folder-toggle][data-folder-id="${folderId}"]`);

  if (children) {
    children.classList.toggle("is-collapsed", isCollapsed);
  }

  if (notes) {
    notes.classList.toggle("is-collapsed", isCollapsed);
  }

  if (toggle) {
    toggle.textContent = isCollapsed ? "[+]" : "[-]";
    toggle.setAttribute("aria-expanded", String(!isCollapsed));
  }
}

function restoreFolderStates() {
  const collapsedFolders = readCollapsedFolders();

  collapsedFolders.forEach((folderId) => {
    applyFolderState(String(folderId), true);
  });
}

document.addEventListener("click", (event) => {
  const toggle = event.target.closest("[data-folder-toggle]");

  if (!toggle) {
    return;
  }

  const folderId = toggle.getAttribute("data-folder-id");
  const collapsedFolders = readCollapsedFolders();
  const isCollapsed = collapsedFolders.includes(folderId);

  const nextCollapsedFolders = isCollapsed ? collapsedFolders.filter((id) => id !== folderId) : [...collapsedFolders, folderId];

  writeCollapsedFolders(nextCollapsedFolders);
  applyFolderState(folderId, !isCollapsed);
});

document.addEventListener("DOMContentLoaded", () => {
  restoreFolderStates();
});
