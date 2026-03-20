const STORAGE_KEY = "robco-vault:collapsed-folders";
const BOOT_KEY = "robco-vault:boot-shown";

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

function setModalOpen(modalName, isOpen) {
  const modal = document.querySelector(`[data-modal="${modalName}"]`);

  if (!modal) {
    return;
  }

  if (isOpen) {
    modal.removeAttribute("hidden");
  } else {
    modal.setAttribute("hidden", "");
  }
}

document.addEventListener("click", (event) => {
  const openTrigger = event.target.closest("[data-open-modal]");

  if (openTrigger) {
    setModalOpen(openTrigger.getAttribute("data-open-modal"), true);
    return;
  }

  if (event.target.closest("[data-modal-close]")) {
    const modal = event.target.closest(".modal");

    if (modal) {
      modal.setAttribute("hidden", "");
    }
  }
});

function showBootOverlayIfNeeded() {
  const overlay = document.querySelector("[data-boot-overlay]");

  if (!overlay) {
    return;
  }

  const alreadyShown = window.sessionStorage.getItem(BOOT_KEY) === "1";

  if (!alreadyShown) {
    overlay.removeAttribute("hidden");
  }
}

function dismissBootOverlay() {
  const overlay = document.querySelector("[data-boot-overlay]");

  if (!overlay) {
    return;
  }

  overlay.setAttribute("hidden", "");
  window.sessionStorage.setItem(BOOT_KEY, "1");
}

document.addEventListener("click", (event) => {
  if (event.target.closest("[data-boot-dismiss]")) {
    dismissBootOverlay();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  restoreFolderStates();
  showBootOverlayIfNeeded();
});
