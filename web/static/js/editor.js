/**
 * Civ VII Mod Editor - Main JavaScript Logic
 * Handles YAML loading/saving, form management, validation, and UI interactions
 */

// Global state
let currentData = {};
let currentFilePath = "";
let isDirty = false;
let dataCache = {}; // Cache for reference data

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
    loadReferenceData();
});

// ============================================================================
// Event Listeners
// ============================================================================

function setupEventListeners() {
    const filePathInput = document.getElementById("file-path-input");
    if (filePathInput) {
        filePathInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                loadFile();
            }
        });
    }

    const saveBtn = document.getElementById("save-btn");
    if (saveBtn) {
        saveBtn.disabled = true;
    }
}

// ============================================================================
// File Operations
// ============================================================================

async function loadFile() {
    const filePathInput = document.getElementById("file-path-input");
    const filePath = filePathInput?.value?.trim();

    if (!filePath) {
        showToast("Please enter a file path", "error");
        return;
    }

    try {
        showLoading();
        const response = await fetch("/api/civilization/load", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ file_path: filePath }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to load file");
        }

        const result = await response.json();
        currentData = result.data || {};
        currentFilePath = result.path;
        isDirty = false;

        renderEditor(currentData);
        updateDirtyIndicator();
        showToast(`Loaded: ${currentFilePath}`, "success");
    } catch (error) {
        showToast(`Error: ${error.message}`, "error");
    }
}

async function saveFile() {
    if (!currentFilePath) {
        showToast("No file loaded", "error");
        return;
    }

    try {
        const response = await fetch("/api/civilization/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                path: currentFilePath,
                data: currentData,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to save file");
        }

        isDirty = false;
        updateDirtyIndicator();
        showToast("File saved successfully", "success");
    } catch (error) {
        showToast(`Error: ${error.message}`, "error");
    }
}

function exportYAML() {
    try {
        const yaml = JSON.stringify(currentData, null, 2); // Temp: will use proper YAML
        const blob = new Blob([yaml], { type: "application/yaml" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${currentData.metadata?.id || "mod"}.yml`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast("Exported successfully", "success");
    } catch (error) {
        showToast(`Export error: ${error.message}`, "error");
    }
}

// ============================================================================
// Editor Rendering
// ============================================================================

function renderEditor(data) {
    const container = document.getElementById("editor-container");
    if (!container) return;

    container.innerHTML = "";

    const sections = [
        { id: "metadata", title: "Metadata", badge: "Info" },
        { id: "module_localization", title: "Module Localization", badge: "Config" },
        { id: "action_group", title: "Action Group", badge: "Gate" },
        { id: "constants", title: "Constants", badge: "Data" },
        { id: "imports", title: "Imports", badge: "Assets" },
        { id: "civilization", title: "Civilization", badge: "Main" },
        { id: "modifiers", title: "Modifiers", badge: "Effects" },
        { id: "traditions", title: "Traditions", badge: "Cultural" },
        { id: "units", title: "Units", badge: "Military" },
        { id: "constructibles", title: "Constructibles", badge: "Buildings" },
        { id: "progression_tree_nodes", title: "Progression Tree Nodes", badge: "Trees" },
        { id: "progression_trees", title: "Progression Trees", badge: "Tech" },
        { id: "build", title: "Build Configuration", badge: "Output" },
    ];

    sections.forEach((section) => {
        const sectionData = data[section.id.replace(/_/g, "_")] || {};
        const sectionEl = createCollapsibleSection(
            section.id,
            section.title,
            section.badge,
            sectionData
        );
        container.appendChild(sectionEl);
    });
}

function createCollapsibleSection(id, title, badge, sectionData) {
    const section = document.createElement("div");
    section.className = "section mb-6 border border-slate-700 rounded-lg overflow-hidden";
    section.id = `section-${id}`;

    const header = document.createElement("button");
    header.className =
        "w-full px-6 py-4 bg-gradient-to-r from-slate-800 to-slate-700 hover:from-slate-700 hover:to-slate-600 flex items-center justify-between font-semibold text-slate-200 transition-colors";
    header.innerHTML = `
        <div class="flex items-center gap-3">
            <span>${title}</span>
            <span class="text-xs px-2 py-1 rounded-full bg-slate-700 text-slate-300">${badge}</span>
        </div>
        <span class="chevron">▼</span>
    `;
    header.onclick = (e) => toggleSection(e);

    const content = document.createElement("div");
    content.className = "section-content bg-slate-900/50 px-6 py-4";

    // Render section-specific fields
    renderSectionContent(content, id, sectionData);

    section.appendChild(header);
    section.appendChild(content);

    return section;
}

function renderSectionContent(container, sectionId, data) {
    container.innerHTML = "";

    switch (sectionId) {
        case "metadata":
            renderMetadataSection(container, data);
            break;
        case "module_localization":
            renderModuleLocalizationSection(container, data);
            break;
        case "action_group":
            renderActionGroupSection(container, data);
            break;
        case "constants":
            renderConstantsSection(container, data);
            break;
        case "civilization":
            renderCivilizationSection(container, data);
            break;
        default:
            container.innerHTML = `<p class="text-slate-400 text-sm">Section: ${sectionId}</p>`;
    }
}

// ============================================================================
// Section Renderers
// ============================================================================

function renderMetadataSection(container, data) {
    const fields = [
        { name: "id", label: "ID", type: "text", required: true },
        { name: "version", label: "Version", type: "text", required: true },
        { name: "name", label: "Name", type: "text", required: true },
        { name: "description", label: "Description", type: "text" },
        { name: "authors", label: "Authors", type: "text" },
        { name: "affects_saved_games", label: "Affects Saved Games", type: "boolean" },
        { name: "enabled_by_default", label: "Enabled by Default", type: "boolean" },
        { name: "package", label: "Package", type: "text" },
    ];

    renderFormFields(container, "metadata", data, fields);
}

function renderModuleLocalizationSection(container, data) {
    const fields = [
        { name: "name", label: "Name", type: "text" },
        { name: "description", label: "Description", type: "text" },
        { name: "authors", label: "Authors", type: "text" },
    ];

    renderFormFields(container, "module_localization", data, fields);
}

function renderActionGroupSection(container, data) {
    const input = document.createElement("input");
    input.type = "text";
    input.value = data || "";
    input.className =
        "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:border-blue-400";
    input.onchange = () => {
        currentData.action_group = input.value;
        markDirty();
    };

    const label = document.createElement("label");
    label.className = "block text-sm font-medium text-slate-300 mb-2";
    label.textContent = "Action Group";

    container.appendChild(label);
    container.appendChild(input);
}

function renderCivilizationSection(container, data) {
    if (!data || typeof data !== "object") {
        container.innerHTML = "<p class='text-slate-400 text-sm'>No civilization data</p>";
        return;
    }

    const fields = [
        { name: "id", label: "ID", type: "text" },
        { name: "civilization_type", label: "Civilization Type", type: "text" },
    ];

    renderFormFields(container, "civilization", data, fields);
}

function renderConstantsSection(container, data) {
    container.innerHTML = "<p class='text-slate-400 text-sm'>Constants section - WIP</p>";
}

// ============================================================================
// Form Utilities
// ============================================================================

function renderFormFields(container, sectionKey, sectionData, fields) {
    fields.forEach((field) => {
        const value = sectionData[field.name] ?? "";
        const fieldEl = createFormField(field.name, field.label, field.type, value, field.required);
        fieldEl.dataset.section = sectionKey;
        container.appendChild(fieldEl);
    });
}

function createFormField(name, label, type, value, required = false) {
    const div = document.createElement("div");
    div.className = "mb-4";

    const labelEl = document.createElement("label");
    labelEl.className = "block text-sm font-medium text-slate-300 mb-2";
    labelEl.innerHTML = label + (required ? ' <span class="text-red-500">*</span>' : "");

    let input;
    if (type === "boolean") {
        input = document.createElement("input");
        input.type = "checkbox";
        input.checked = value === true;
        input.className =
            "w-4 h-4 rounded bg-slate-800 border-slate-600 text-blue-500 cursor-pointer";
    } else {
        input = document.createElement("input");
        input.type = type;
        input.value = value || "";
        input.className =
            "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400";
    }

    input.dataset.field = name;
    input.onchange = (e) => updateFieldValue(e);

    div.appendChild(labelEl);
    div.appendChild(input);

    return div;
}

function updateFieldValue(event) {
    const input = event.target;
    const section = input.closest("[data-section]")?.dataset.section;
    const fieldName = input.dataset.field;

    if (section && fieldName) {
        if (!currentData[section]) {
            currentData[section] = {};
        }

        if (input.type === "checkbox") {
            currentData[section][fieldName] = input.checked;
        } else {
            currentData[section][fieldName] = input.value;
        }

        markDirty();
    }
}

// ============================================================================
// UI Interactions
// ============================================================================

function switchSection(sectionId, event) {
    event?.preventDefault();
    document.querySelectorAll(".section-nav").forEach((el) => el.classList.remove("active"));
    event?.target?.closest(".section-nav")?.classList.add("active");
}

function toggleSection(event) {
    const section = event.target.closest(".section");
    const content = section.querySelector(".section-content");
    const chevron = section.querySelector(".chevron");

    if (content.classList.contains("hidden")) {
        content.classList.remove("hidden");
        chevron.textContent = "▼";
    } else {
        content.classList.add("hidden");
        chevron.textContent = "▶";
    }
}

function markDirty() {
    isDirty = true;
    updateDirtyIndicator();
}

function updateDirtyIndicator() {
    const indicator = document.getElementById("dirty-indicator");
    const saveBtn = document.getElementById("save-btn");

    if (isDirty) {
        indicator?.classList.remove("hidden");
        indicator?.classList.add("flex");
        if (saveBtn) saveBtn.disabled = false;
    } else {
        indicator?.classList.add("hidden");
        indicator?.classList.remove("flex");
        if (saveBtn) saveBtn.disabled = true;
    }
}

// ============================================================================
// Reference Data Loading
// ============================================================================

async function loadReferenceData() {
    try {
        const response = await fetch("/api/data/list");
        if (response.ok) {
            const result = await response.json();
            // Cache is ready for use in autocomplete fields
        }
    } catch (error) {
        console.error("Failed to load reference data:", error);
    }
}

async function fetchReferenceData(dataType) {
    if (dataCache[dataType]) {
        return dataCache[dataType];
    }

    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (response.ok) {
            const data = await response.json();
            dataCache[dataType] = data;
            return data;
        }
    } catch (error) {
        console.error(`Failed to fetch ${dataType}:`, error);
    }

    return null;
}

// ============================================================================
// Notifications
// ============================================================================

function showToast(message, type = "info") {
    const toast = document.getElementById("toast");
    const toastMessage = document.getElementById("toast-message");

    if (!toast || !toastMessage) return;

    toastMessage.textContent = message;

    const bgClass =
        type === "error"
            ? "bg-red-900/80 border border-red-700 text-red-200"
            : type === "success"
              ? "bg-green-900/80 border border-green-700 text-green-200"
              : "bg-blue-900/80 border border-blue-700 text-blue-200";

    toast.className = `fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg ${bgClass}`;

    clearTimeout(toast.timeoutId);
    toast.timeoutId = setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}

function showLoading() {
    const container = document.getElementById("editor-container");
    if (container) {
        container.innerHTML = '<div class="flex justify-center items-center py-16"><div class="animate-spin text-2xl">⏳</div></div>';
    }
}
