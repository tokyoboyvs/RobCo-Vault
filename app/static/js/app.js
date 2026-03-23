const STORAGE_KEY = "robco-vault:collapsed-folders";
const BOOT_KEY = "robco-vault:boot-shown";
const THEME_KEY = "robco-vault:theme";

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

function closeTreeMenus() {
  document.querySelectorAll("[data-tree-menu]").forEach((menu) => {
    menu.classList.add("hidden");
  });

  document.querySelectorAll("[data-tree-menu-toggle]").forEach((button) => {
    button.setAttribute("aria-expanded", "false");
  });
}

document.addEventListener("click", (event) => {
  const menuToggle = event.target.closest("[data-tree-menu-toggle]");

  if (menuToggle) {
    const menuName = menuToggle.getAttribute("data-tree-menu-toggle");
    const menu = document.querySelector(`[data-tree-menu="${menuName}"]`);
    const isHidden = menu ? menu.classList.contains("hidden") : true;

    closeTreeMenus();

    if (menu && isHidden) {
      menu.classList.remove("hidden");
      menuToggle.setAttribute("aria-expanded", "true");
    }

    return;
  }

  const openTrigger = event.target.closest("[data-open-modal]");

  if (openTrigger) {
    closeTreeMenus();
    setModalOpen(openTrigger.getAttribute("data-open-modal"), true);
    return;
  }

  if (event.target.closest("[data-modal-close]")) {
    const modal = event.target.closest(".modal");

    if (modal) {
      modal.setAttribute("hidden", "");
    }

    return;
  }

  if (!event.target.closest("[data-tree-menu]")) {
    closeTreeMenus();
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

function applyTheme(themeName) {
  const theme = themeName === "classic" ? "classic" : "modern";
  document.body.setAttribute("data-theme", theme);
}

function restoreTheme() {
  const savedTheme = window.localStorage.getItem(THEME_KEY) || "modern";
  applyTheme(savedTheme);
}

document.addEventListener("click", (event) => {
  const themeButton = event.target.closest("[data-theme-select]");

  if (!themeButton) {
    return;
  }

  const themeName = themeButton.getAttribute("data-theme-select");
  window.localStorage.setItem(THEME_KEY, themeName);
  applyTheme(themeName);
});

document.addEventListener("DOMContentLoaded", () => {
  restoreTheme();
  restoreFolderStates();
  showBootOverlayIfNeeded();
});
