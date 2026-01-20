/**
 * Civ VII Mod Editor - Main JavaScript Logic
 * Handles YAML loading/saving, form management, validation, and UI interactions
 */

// Global state
let currentData = {};
let currentFilePath = "";
let isDirty = false;
let dataCache = {}; // Cache for reference data

// Autocomplete field mappings to reference data
const AUTOCOMPLETE_MAPPINGS = {
    yield_type: "yield-types",
    collection: "collection-types",
    effect: "effects",
    requirement_type: "requirement-types",
    core_class: "core-classes",
    domain: "domains",
    formation_class: "formation-classes",
    unit_movement_class: "unit-movement-classes",
    tag: "tags",
    district: "district-types",
    advisory: "advisory-class-types",
    age_type: "ages",
    progression_tree_type: "progression-trees",
    // trait_type removed - not in data files, use text input instead
    terrain_type: "terrain-types",
    biome_type: "biome-types",
    feature_type: "feature-types",
    constructible_type: "constructible-classes",
    // unit_type removed - not in data files, use text input instead
};

// Contextual help text for fields
const FIELD_HELP_TEXT = {
    collection: "Scope of effect: ALL_CITIES (everyone), OWNER (your cities), OWNER_UNIT (your units), ALL_PLAYERS (all civilizations)",
    effect: "Game action: ADJUST_YIELD modifies output, COMBAT_STRENGTH affects unit power, LOYALTY controls city control",
    core_class: "Unit role: MILITARY (combat), CIVILIAN (workers/settlers), SUPPORT (buffs/heals other units)",
    domain: "Movement domain: LAND (ground units), SEA (naval units), AIR (aircraft), SPACE (future tech)",
    formation_class: "Combat formation type: LAND_COMBAT (melee), LAND_RANGED (archers), NAVAL_COMBAT (ships), SIEGE (siege weapons)",
    unit_movement_class: "Terrain movement: FOOT (infantry), MOUNTED (cavalry), NAVAL (ships), FLYING (aircraft)",
    yield_type: "Resource output: PRODUCTION (building), SCIENCE (research), GOLD (economy), CULTURE (civics), FAITH (religion), TOURISM (great works)",
    constructible_valid_districts: "Districts where this building can be placed: URBAN (cities), CITY_CENTER (any city), specialized districts",
    trait_type: "Civilization trait that gives access: TRAIT_SCIENTIFIC, TRAIT_MILITARY, TRAIT_ECONOMIC, TRAIT_CULTURAL, TRAIT_RELIGIOUS",
    terrain_type: "Terrain classification: PLAINS, FOREST, MOUNTAIN, COAST, DESERT - affects yields and movement",
    age_type: "Game age for unlocks: AGE_ANTIQUITY, AGE_EXPLORATION, AGE_MODERN, AGE_ATOMIC, AGE_INFORMATION",
    constructible_type: "Building/improvement ID: BUILDING_* for buildings, QUARTER_* for city quarters, IMPROVEMENT_* for map improvements",
    unit_type: "Unit ID: UNIT_* for military/civilian units, format like UNIT_BABYLON_SABUM_KIBITTUM",
};

// Required fields per section for validation
const REQUIRED_FIELDS = {
    units: ["id", "unit_type"],
    constructibles: ["id", "constructible_type"],
    modifiers: ["id", "modifier"],
    traditions: ["id", "tradition_type"],
    progression_tree_nodes: ["id", "progression_tree_node_type"],
    progression_trees: ["id", "progression_tree_type"],
};

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
    loadReferenceData();
    setupScrollSpy();
});

// ============================================================================
// Navigation
// ============================================================================

function setupScrollSpy() {
    // Highlight active section in sidebar based on scroll position
    const mainContent = document.querySelector('main');
    if (!mainContent) return;
    
    let scrollTimeout;
    
    mainContent.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const sections = document.querySelectorAll('[id^="section-"]');
            let currentSection = '';
            
            sections.forEach(section => {
                const rect = section.getBoundingClientRect();
                // Check if section is in viewport (top of section is visible)
                if (rect.top >= 0 && rect.top < window.innerHeight / 2) {
                    currentSection = section.id;
                }
            });
            
            // If no section found in top half, use the one closest to top
            if (!currentSection && sections.length > 0) {
                sections.forEach(section => {
                    const rect = section.getBoundingClientRect();
                    if (rect.top < window.innerHeight) {
                        currentSection = section.id;
                    }
                });
            }
            
            if (currentSection) {
                // Remove active state from all links
                document.querySelectorAll('.section-nav').forEach(nav => {
                    nav.classList.remove('bg-slate-700', 'text-slate-100');
                    nav.classList.add('text-slate-300');
                });
                
                // Add active state to current section
                const activeLink = document.querySelector(`a[href="#${currentSection}"]`);
                if (activeLink) {
                    activeLink.classList.remove('text-slate-300');
                    activeLink.classList.add('bg-slate-700', 'text-slate-100');
                }
            }
        }, 100); // Debounce 100ms
    });
}

function renderAllSections() {
    const container = document.getElementById("editor-container");
    if (!container) return;
    
    container.innerHTML = "";
    
    // Create all sections with IDs for scrolling
    // IDs use underscores to match keys and avoid potential issues
    const sections = [
        { id: "metadata", title: "Metadata", fn: renderMetadataSection, key: "metadata" },
        { id: "module_localization", title: "Module Localization", fn: renderModuleLocalizationSection, key: "module_localization" },
        { id: "action_group", title: "Action Group", fn: renderActionGroupSection, key: "action_group" },
        { id: "constants", title: "Constants", fn: renderConstantsSection, key: "constants" },
        { id: "imports", title: "Imports", fn: renderImportsSection, key: "imports" },
        { id: "civilization", title: "Civilization", fn: renderCivilizationSection, key: "civilization" },
        { id: "modifiers", title: "Modifiers", fn: renderModifiersSection, key: "modifiers" },
        { id: "traditions", title: "Traditions", fn: renderTraditionsSection, key: "traditions" },
        { id: "units", title: "Units", fn: renderUnitsSection, key: "units" },
        { id: "constructibles", title: "Constructibles", fn: renderConstructiblesSection, key: "constructibles" },
        { id: "progression_tree_nodes", title: "Progression Tree Nodes", fn: renderProgressionTreeNodesSection, key: "progression_tree_nodes" },
        { id: "progression_trees", title: "Progression Trees", fn: renderProgressionTreesSection, key: "progression_trees" },
        { id: "build", title: "Build Configuration", fn: renderBuildSection, key: "build" },
    ];
    
    sections.forEach(({ id, title, fn, key }) => {
        try {
            const sectionDiv = document.createElement('div');
            sectionDiv.id = `section-${id}`;
            sectionDiv.className = 'mb-8 scroll-mt-24';
            
            const heading = document.createElement('h2');
            heading.className = 'text-2xl font-bold mb-4 text-slate-100';
            heading.textContent = title;
            sectionDiv.appendChild(heading);
            
            const content = document.createElement('div');
            content.className = 'bg-slate-900/50 p-6 rounded-lg border border-slate-700';
            
            const data = currentData[key] || {};
            fn(content, data);
            
            sectionDiv.appendChild(content);
            container.appendChild(sectionDiv);
        } catch (error) {
            console.error(`[RENDER_ERROR] Failed to render ${title} (${id}):`, error);
            const errorDiv = document.createElement('div');
            errorDiv.id = `section-${id}`;
            errorDiv.className = 'mb-8 scroll-mt-24 p-4 bg-red-900/30 border border-red-700 rounded';
            errorDiv.innerHTML = `<h2 class="text-2xl font-bold text-red-400 mb-2">${title}</h2><p class="text-red-300 text-sm">Error rendering section: ${error.message}</p>`;
            container.appendChild(errorDiv);
        }
    });
    console.log('[RENDER_COMPLETE] All sections rendered');
    console.log('[RENDER_COMPLETE] All sections rendered');
    
    // Re-attach nav event listeners since sections were just created
    setupNavEventListeners();
}

function setupNavEventListeners() {
    document.querySelectorAll('.section-nav').forEach(link => {
        // Remove old listeners by cloning
        const newLink = link.cloneNode(true);
        link.parentNode.replaceChild(newLink, link);
        
        newLink.addEventListener('click', (e) => {
            e.preventDefault();
            const href = newLink.getAttribute('href');
            if (href && href.startsWith('#')) {
                const sectionId = href.substring(1);
                const element = document.getElementById(sectionId);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });
}

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
    
    // Setup nav event listeners
    setupNavEventListeners();
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

        // Render all sections
        renderAllSections();
        
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

    // Client-side validation
    const validation = validateModData();
    if (!validation.isValid) {
        showToast(`Validation failed: ${validation.errors.join(", ")}`, "error");
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
        // Send to backend to convert to proper YAML format
        fetch("/api/civilization/export", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentData),
        }).then(response => response.blob()).then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${currentData.metadata?.id || "mod"}.yml`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast("Exported successfully", "success");
        }).catch(err => {
            showToast(`Export error: ${err.message}`, "error");
        });
    } catch (error) {
        showToast(`Export error: ${error.message}`, "error");
    }
}

function createNew() {
    // Create a skeleton YAML with all sections
    currentData = {
        metadata: {
            id: "my-mod",
            version: "1.0.0",
            name: "My Mod",
            description: "Mod description",
            authors: "Author Name",
        },
        module_localization: {},
        action_group: {
            action_group_id: "ALWAYS",
        },
        constants: {},
        imports: [],
        civilization: {},
        modifiers: [],
        traditions: [],
        units: [],
        constructibles: [],
        progression_tree_nodes: [],
        progression_trees: [],
        build: {
            mod_folder: "./",
            output_folder: "./dist",
        },
    };
    
    currentFilePath = "my-mod.yml";
    isDirty = true;
    
    document.getElementById("file-path-input").value = currentFilePath;
    renderEditor(currentData);
    updateDirtyIndicator();
    showToast("Created new skeleton YAML. Enter file path and save.", "success");
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
        case "imports":
            renderImportsSection(container, data);
            break;
        case "civilization":
            renderCivilizationSection(container, data);
            break;
        case "modifiers":
            renderModifiersSection(container, data);
            break;
        case "traditions":
            renderTraditionsSection(container, data);
            break;
        case "units":
            renderUnitsSection(container, data);
            break;
        case "constructibles":
            renderConstructiblesSection(container, data);
            break;
        case "progression_tree_nodes":
            renderProgressionTreeNodesSection(container, data);
            break;
        case "progression_trees":
            renderProgressionTreesSection(container, data);
            break;
        case "build":
            renderBuildSection(container, data);
            break;
        default:
            container.innerHTML = `<p class="text-slate-400 text-sm">Section: ${sectionId}</p>`;
    }
}

// ============================================================================
// Section Renderers
// ============================================================================

function renderMetadataSection(container, data) {
    if (!currentData.metadata) currentData.metadata = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Mod Metadata";
    container.appendChild(h3);
    
    const meta = currentData.metadata;
    container.appendChild(createTextField("metadata.id", "ID", meta.id, true));
    container.appendChild(createTextField("metadata.version", "Version", meta.version, true));
    container.appendChild(createTextField("metadata.name", "Name", meta.name, true));
    container.appendChild(createTextField("metadata.description", "Description", meta.description));
    container.appendChild(createTextField("metadata.authors", "Authors", meta.authors));
    container.appendChild(createBooleanField("metadata.affects_saved_games", "Affects Saved Games", meta.affects_saved_games));
    container.appendChild(createBooleanField("metadata.enabled_by_default", "Enabled by Default", meta.enabled_by_default));
    container.appendChild(createTextField("metadata.package", "Package", meta.package));
}

function renderModuleLocalizationSection(container, data) {
    if (!currentData.module_localization) currentData.module_localization = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Module Localization";
    container.appendChild(h3);
    
    const loc = currentData.module_localization;
    container.appendChild(createTextField("module_localization.name", "Name", loc.name));
    container.appendChild(createTextField("module_localization.description", "Description", loc.description));
    container.appendChild(createTextField("module_localization.authors", "Authors", loc.authors));
}

function renderActionGroupSection(container, data) {
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Action Group";
    container.appendChild(h3);
    
    const actionGroup = currentData.action_group || "";
    container.appendChild(createTextField("action_group", "Action Group", actionGroup));
}

function renderCivilizationSection(container, data) {
    if (!currentData.civilization) currentData.civilization = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Civilization";
    container.appendChild(h3);
    
    const civ = currentData.civilization;
    container.appendChild(createTextField("civilization.id", "ID", civ.id, true));
    container.appendChild(createTextField("civilization.civilization_type", "Civilization Type", civ.civilization_type, true));
    container.appendChild(createTextField("civilization.trait_type", "Trait Type", civ.trait_type, false));
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

function updateFieldValue(fieldPath, value) {
    // Handle both nested paths (e.g., "units.0.unit.base_moves") and event objects
    if (typeof fieldPath === 'object' && fieldPath.target) {
        // Legacy event-based call
        const event = fieldPath;
        const input = event.target;
        const section = input.closest("[data-section]")?.dataset.section;
        const field = input.dataset.field;

        if (section && field) {
            if (!currentData[section]) {
                currentData[section] = {};
            }

            if (input.type === "checkbox") {
                currentData[section][field] = input.checked;
            } else {
                currentData[section][field] = input.value;
            }

            markDirty();
        }
        return;
    }

    // New path-based update for nested fields
    const parts = fieldPath.split(".");
    let obj = currentData;

    // Navigate/create nested structure
    for (let i = 0; i < parts.length - 1; i++) {
        const part = parts[i];
        // Check if this part is an array index
        if (!isNaN(part)) {
            // Previous part should be an array
            const prevObj = obj;
            const prevKey = parts[i - 1];
            if (!Array.isArray(prevObj[prevKey])) {
                prevObj[prevKey] = [];
            }
            obj = prevObj[prevKey][parseInt(part)];
        } else {
            if (!obj[part]) {
                obj[part] = {};
            }
            obj = obj[part];
        }
    }

    const lastPart = parts[parts.length - 1];
    obj[lastPart] = value;
    markDirty();
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
// ============================================================================
// Validation
// ============================================================================

function validateModData() {
    const errors = [];
    
    // Check metadata
    if (!currentData.metadata?.id) errors.push("Metadata: missing 'id'");
    if (!currentData.metadata?.version) errors.push("Metadata: missing 'version'");
    
    // Check required fields per section
    if (currentData.units?.length > 0) {
        currentData.units.forEach((unit, i) => {
            if (!unit.id) errors.push(`Units[${i}]: missing 'id'`);
            if (!unit.unit_type) errors.push(`Units[${i}]: missing 'unit_type'`);
        });
    }
    
    if (currentData.constructibles?.length > 0) {
        currentData.constructibles.forEach((constructible, i) => {
            if (!constructible.id) errors.push(`Constructibles[${i}]: missing 'id'`);
            if (!constructible.constructible_type) errors.push(`Constructibles[${i}]: missing 'constructible_type'`);
        });
    }
    
    if (currentData.modifiers?.length > 0) {
        currentData.modifiers.forEach((modifier, i) => {
            if (!modifier.id) errors.push(`Modifiers[${i}]: missing 'id'`);
            if (!modifier.modifier) errors.push(`Modifiers[${i}]: missing 'modifier'`);
        });
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors,
    };
}

// ============================================================================
// Autocomplete Helpers
// ============================================================================

async function getAutocompleteOptions(fieldName) {
    // Extract the last part of the field name (e.g., "collection" from "modifiers.0.modifier.collection")
    const fieldType = fieldName.split('.').pop();
    const dataType = AUTOCOMPLETE_MAPPINGS[fieldType];
    if (!dataType) {
        return [];
    }
    
    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (response.ok) {
            const data = await response.json();
            // JSON files have structure: { values: [{ id: "...", ... }, ...] }
            const options = data.values ? data.values.map(v => v.id) : [];
            return options;
        }
    } catch (error) {
        console.error(`Failed to fetch autocomplete data for ${fieldType}:`, error);
    }
    return [];
}

function createAutocompleteField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    if (helpText) {
        const helpSpan = document.createElement("div");
        helpSpan.className = "text-xs text-blue-300 mb-2 bg-blue-900/30 p-2 rounded border border-blue-700/50";
        helpSpan.textContent = "💡 " + helpText;
        div.appendChild(helpSpan);
    }
    
    const inputWrapper = document.createElement("div");
    inputWrapper.className = "relative";
    
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    input.autocomplete = "off";
    
    const dropdown = document.createElement("div");
    dropdown.className = "absolute top-full left-0 right-0 mt-1 bg-slate-800 border border-slate-600 rounded shadow-lg max-h-48 overflow-y-auto";
    dropdown.style.display = "none";
    dropdown.style.zIndex = "1000";
    
    let options = [];
    let filteredOptions = [];
    
    // Load options asynchronously
    (async () => {
        options = await getAutocompleteOptions(fieldName);
        updateDropdown();
    })();
    
    function updateDropdown() {
        const query = input.value.toLowerCase();
        filteredOptions = query.length === 0 ? options : options.filter(opt => {
            const optStr = String(opt).toLowerCase();
            return optStr.includes(query);
        });
        filteredOptions = filteredOptions.slice(0, 50); // Show up to 50 options
        
        dropdown.innerHTML = "";
        
        if (filteredOptions.length === 0) {
            const noResults = document.createElement("div");
            noResults.className = "px-3 py-2 text-slate-400 text-sm";
            noResults.textContent = query.length > 0 ? "No results" : "No options available";
            dropdown.appendChild(noResults);
            dropdown.style.display = "block";
        } else {
            filteredOptions.forEach(opt => {
                const optDiv = document.createElement("div");
                optDiv.className = "px-3 py-2 cursor-pointer hover:bg-slate-700 text-slate-100 text-sm";
                optDiv.textContent = opt;
                optDiv.onclick = () => {
                    input.value = opt;
                    updateFieldValue(fieldName, opt);
                    dropdown.style.display = "none";
                };
                dropdown.appendChild(optDiv);
            });
            dropdown.style.display = "block";
        }
    }
    
    input.addEventListener("input", updateDropdown);
    input.addEventListener("focus", () => {
        // Show all options when focused
        if (options.length > 0) {
            updateDropdown();
        }
    });
    input.addEventListener("change", (e) => {
        updateFieldValue(fieldName, e.target.value);
    });
    
    document.addEventListener("click", (e) => {
        if (!inputWrapper.contains(e.target)) {
            dropdown.style.display = "none";
        }
    });
    
    inputWrapper.appendChild(input);
    inputWrapper.appendChild(dropdown);
    div.appendChild(inputWrapper);
    
    return div;
}

function createTextField(fieldName, label, value = "", isRequired = false) {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label + (isRequired ? " *" : "");
    div.appendChild(labelElem);
    
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400";
    input.addEventListener("change", (e) => {
        updateFieldValue(fieldName, e.target.value);
    });
    
    div.appendChild(input);
    return div;
}

function createNumberField(fieldName, label, value = "", isRequired = false) {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label + (isRequired ? " *" : "");
    div.appendChild(labelElem);
    
    const input = document.createElement("input");
    input.type = "number";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400";
    input.addEventListener("change", (e) => {
        updateFieldValue(fieldName, parseInt(e.target.value) || "");
    });
    
    div.appendChild(input);
    return div;
}

function createBooleanField(fieldName, label, value = false) {
    const div = document.createElement("div");
    div.className = "mb-4 flex items-center gap-3";
    
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = value === true || value === "true";
    input.className = "w-4 h-4 rounded bg-slate-700 border-slate-600";
    input.addEventListener("change", (e) => {
        updateFieldValue(fieldName, e.target.checked);
    });
    
    const labelElem = document.createElement("label");
    labelElem.className = "text-sm font-medium text-slate-300";
    labelElem.textContent = label;
    
    div.appendChild(input);
    div.appendChild(labelElem);
    return div;
}

function createStringArrayField(fieldName, label, items = [], sectionId = null) {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label;
    div.appendChild(labelElem);
    
    const itemsContainer = document.createElement("div");
    itemsContainer.className = "space-y-2";
    itemsContainer.id = `array-${fieldName}`;
    
    items.forEach((item, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "flex gap-2";
        
        const input = document.createElement("input");
        input.type = "text";
        input.value = item;
        input.className = "flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm";
        input.addEventListener("change", (e) => {
            updateFieldValue(fieldName + "." + i, e.target.value);
        });
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.className = "px-3 py-2 bg-red-700 hover:bg-red-800 text-white text-sm rounded transition";
        removeBtn.onclick = () => {
            const parts = fieldName.split(".");
            let obj = currentData;
            for (let j = 0; j < parts.length - 1; j++) {
                obj = obj[parts[j]];
            }
            const arr = obj[parts[parts.length - 1]];
            if (Array.isArray(arr)) {
                arr.splice(i, 1);
                markDirty();
                // Refresh only the array container
                const container = itemDiv.closest(".section-content") || div.parentElement;
                if (sectionId) {
                    renderSectionContent(container, sectionId, currentData);
                }
            }
        };
        
        itemDiv.appendChild(input);
        itemDiv.appendChild(removeBtn);
        itemsContainer.appendChild(itemDiv);
    });
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition";
    addBtn.onclick = () => {
        const parts = fieldName.split(".");
        let obj = currentData;
        for (let j = 0; j < parts.length - 1; j++) {
            if (!obj[parts[j]]) obj[parts[j]] = {};
            obj = obj[parts[j]];
        }
        if (!Array.isArray(obj[parts[parts.length - 1]])) {
            obj[parts[parts.length - 1]] = [];
        }
        obj[parts[parts.length - 1]].push("");
        markDirty();
        // Refresh the array container
        const container = div.closest(".section-content");
        if (sectionId && container) {
            renderSectionContent(container, sectionId, currentData);
        }
    };
    
    div.appendChild(itemsContainer);
    div.appendChild(addBtn);
    return div;
}

// ============================================================================
// Section Renderers
// ============================================================================

function renderConstantsSection(container, data) {
    if (!currentData.constants) currentData.constants = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "City Names";
    container.appendChild(h3);
    
    const cityNames = currentData.constants.city_names || [];
    container.appendChild(createStringArrayField("constants.city_names", "City Names", cityNames, "constants"));
}

function renderImportsSection(container, data) {
    if (!currentData.imports) currentData.imports = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Import Assets";
    container.appendChild(h3);
    
    const itemsContainer = document.createElement("div");
    itemsContainer.id = "imports-items";
    
    currentData.imports.forEach((importItem, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
        itemDiv.dataset.index = i;
        
        const titleDiv = document.createElement("div");
        titleDiv.className = "flex justify-between items-center mb-3";
        const title = document.createElement("h4");
        title.textContent = `Import ${i + 1}`;
        title.className = "font-semibold text-slate-300";
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
        removeBtn.onclick = () => {
            currentData.imports.splice(i, 1);
            markDirty();
            renderImportsSection(container, data);
        };
        
        titleDiv.appendChild(title);
        titleDiv.appendChild(removeBtn);
        itemDiv.appendChild(titleDiv);
        
        itemDiv.appendChild(createTextField(`imports.${i}.id`, "ID", importItem.id));
        itemDiv.appendChild(createTextField(`imports.${i}.source_path`, "Source Path", importItem.source_path));
        itemDiv.appendChild(createTextField(`imports.${i}.target_name`, "Target Name", importItem.target_name));
        
        itemsContainer.appendChild(itemDiv);
    });
    
    container.appendChild(itemsContainer);
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Import";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.imports.push({ id: "", source_path: "", target_name: "" });
        markDirty();
        renderImportsSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderTraditionsSection(container, data) {
    if (!currentData.traditions) currentData.traditions = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Traditions";
    container.appendChild(h3);
    
    currentData.traditions.forEach((tradition, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
        
        const titleDiv = document.createElement("div");
        titleDiv.className = "flex justify-between items-center mb-3";
        const title = document.createElement("h4");
        title.textContent = `Tradition: ${tradition.id || "(New)"}`;
        title.className = "font-semibold text-slate-300";
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
        removeBtn.onclick = () => {
            currentData.traditions.splice(i, 1);
            markDirty();
            renderTraditionsSection(container, data);
        };
        
        titleDiv.appendChild(title);
        titleDiv.appendChild(removeBtn);
        itemDiv.appendChild(titleDiv);
        
        itemDiv.appendChild(createTextField(`traditions.${i}.id`, "ID", tradition.id, true));
        itemDiv.appendChild(createAutocompleteField(`traditions.${i}.tradition_type`, "Tradition Type", tradition.tradition_type));
        
        if (tradition.localizations?.length > 0) {
            const locDiv = document.createElement("div");
            locDiv.className = "mt-3 p-3 bg-slate-900 rounded";
            tradition.localizations.forEach((loc, li) => {
                locDiv.appendChild(createTextField(`traditions.${i}.localizations.${li}.name`, "Name", loc.name));
                locDiv.appendChild(createTextField(`traditions.${i}.localizations.${li}.description`, "Description", loc.description));
            });
            itemDiv.appendChild(locDiv);
        }
        
        container.appendChild(itemDiv);
    });
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Tradition";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.traditions.push({
            id: "",
            tradition_type: "",
            tradition: {},
            localizations: [{ name: "", description: "" }],
            bindings: [],
        });
        markDirty();
        renderTraditionsSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderProgressionTreeNodesSection(container, data) {
    if (!currentData.progression_tree_nodes) currentData.progression_tree_nodes = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Progression Tree Nodes";
    container.appendChild(h3);
    
    if (currentData.progression_tree_nodes.length === 0) {
        const emptyMsg = document.createElement("p");
        emptyMsg.className = "text-slate-400 text-sm mb-4";
        emptyMsg.textContent = "No progression tree nodes added yet.";
        container.appendChild(emptyMsg);
    } else {
        currentData.progression_tree_nodes.forEach((node, i) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
            
            const titleDiv = document.createElement("div");
            titleDiv.className = "flex justify-between items-center mb-3";
            const title = document.createElement("h4");
            title.textContent = `Node: ${node.id || "(New)"}`;
            title.className = "font-semibold text-slate-300";
            
            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
            removeBtn.onclick = () => {
                currentData.progression_tree_nodes.splice(i, 1);
                markDirty();
                renderProgressionTreeNodesSection(container, data);
            };
            
            titleDiv.appendChild(title);
            titleDiv.appendChild(removeBtn);
            itemDiv.appendChild(titleDiv);
            
            itemDiv.appendChild(createTextField(`progression_tree_nodes.${i}.id`, "ID", node.id, true));
            itemDiv.appendChild(createTextField(`progression_tree_nodes.${i}.progression_tree_node_type`, "Node Type", node.progression_tree_node_type, true));
            
            if (node.localizations?.length > 0) {
                const locDiv = document.createElement("div");
                locDiv.className = "mt-3 p-3 bg-slate-900 rounded";
                node.localizations.forEach((loc, li) => {
                    locDiv.appendChild(createTextField(`progression_tree_nodes.${i}.localizations.${li}.name`, "Name", loc.name));
                });
                itemDiv.appendChild(locDiv);
            }
            
            container.appendChild(itemDiv);
        });
    }
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Node";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.progression_tree_nodes.push({
            id: "",
            progression_tree_node_type: "",
            progression_tree_node: {},
            progression_tree_advisories: [],
            localizations: [{ name: "" }],
            bindings: [],
        });
        markDirty();
        renderProgressionTreeNodesSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderProgressionTreesSection(container, data) {
    if (!currentData.progression_trees) currentData.progression_trees = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Progression Trees";
    container.appendChild(h3);
    
    if (currentData.progression_trees.length === 0) {
        const emptyMsg = document.createElement("p");
        emptyMsg.className = "text-slate-400 text-sm mb-4";
        emptyMsg.textContent = "No progression trees added yet.";
        container.appendChild(emptyMsg);
    } else {
        currentData.progression_trees.forEach((tree, i) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
            
            const titleDiv = document.createElement("div");
            titleDiv.className = "flex justify-between items-center mb-3";
            const title = document.createElement("h4");
            title.textContent = `Tree: ${tree.id || "(New)"}`;
            title.className = "font-semibold text-slate-300";
            
            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
            removeBtn.onclick = () => {
                currentData.progression_trees.splice(i, 1);
                markDirty();
                renderProgressionTreesSection(container, data);
            };
            
            titleDiv.appendChild(title);
            titleDiv.appendChild(removeBtn);
            itemDiv.appendChild(titleDiv);
            
            itemDiv.appendChild(createTextField(`progression_trees.${i}.id`, "ID", tree.id, true));
            itemDiv.appendChild(createTextField(`progression_trees.${i}.progression_tree_type`, "Tree Type", tree.progression_tree_type, true));
            itemDiv.appendChild(createAutocompleteField(`progression_trees.${i}.progression_tree.age_type`, "Age Type", tree.progression_tree?.age_type));
            
            if (tree.localizations?.length > 0) {
                const locDiv = document.createElement("div");
                locDiv.className = "mt-3 p-3 bg-slate-900 rounded";
                tree.localizations.forEach((loc, li) => {
                    locDiv.appendChild(createTextField(`progression_trees.${i}.localizations.${li}.name`, "Name", loc.name));
                });
                itemDiv.appendChild(locDiv);
            }
            
            container.appendChild(itemDiv);
        });
    }
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Tree";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.progression_trees.push({
            id: "",
            progression_tree_type: "",
            progression_tree: { age_type: "" },
            progression_tree_prereqs: [],
            localizations: [{ name: "" }],
            bindings: [],
        });
        markDirty();
        renderProgressionTreesSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderUnitsSection(container, data) {
    if (!currentData.units) currentData.units = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Units";
    container.appendChild(h3);
    
    currentData.units.forEach((unit, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
        
        const titleDiv = document.createElement("div");
        titleDiv.className = "flex justify-between items-center mb-3";
        const title = document.createElement("h4");
        title.textContent = `Unit: ${unit.id || "(New)"}`;
        title.className = "font-semibold text-slate-300";
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
        removeBtn.onclick = () => {
            currentData.units.splice(i, 1);
            markDirty();
            renderUnitsSection(container, data);
        };
        
        titleDiv.appendChild(title);
        titleDiv.appendChild(removeBtn);
        itemDiv.appendChild(titleDiv);
        
        // Basic fields
        itemDiv.appendChild(createTextField(`units.${i}.id`, "ID", unit.id, true));
        itemDiv.appendChild(createTextField(`units.${i}.unit_type`, "Unit Type", unit.unit_type, true));
        
        // Unit object
        if (!unit.unit) unit.unit = {};
        const unitDiv = document.createElement("div");
        unitDiv.className = "mt-3 p-3 bg-slate-900 rounded";
        unitDiv.appendChild(document.createElement("h5")).textContent = "Unit Config";
        unitDiv.lastChild.className = "font-semibold text-slate-400 mb-2 text-sm";
        
        unitDiv.appendChild(createAutocompleteField(`units.${i}.unit.core_class`, "Core Class", unit.unit.core_class, false, FIELD_HELP_TEXT.core_class));
        unitDiv.appendChild(createAutocompleteField(`units.${i}.unit.domain`, "Domain", unit.unit.domain, false, FIELD_HELP_TEXT.domain));
        unitDiv.appendChild(createAutocompleteField(`units.${i}.unit.formation_class`, "Formation Class", unit.unit.formation_class, false, FIELD_HELP_TEXT.formation_class));
        unitDiv.appendChild(createAutocompleteField(`units.${i}.unit.unit_movement_class`, "Movement Class", unit.unit.unit_movement_class, false, FIELD_HELP_TEXT.unit_movement_class));
        unitDiv.appendChild(createNumberField(`units.${i}.unit.base_moves`, "Base Moves", unit.unit.base_moves));
        unitDiv.appendChild(createNumberField(`units.${i}.unit.base_sight_range`, "Sight Range", unit.unit.base_sight_range));
        
        itemDiv.appendChild(unitDiv);
        
        // Icon
        if (unit.icon) {
            itemDiv.appendChild(createTextField(`units.${i}.icon.path`, "Icon Path", unit.icon.path));
        }
        
        // Unit cost
        if (unit.unit_cost) {
            itemDiv.appendChild(createAutocompleteField(`units.${i}.unit_cost.yield_type`, "Cost Yield", unit.unit_cost.yield_type, false, FIELD_HELP_TEXT.yield_type));
            itemDiv.appendChild(createNumberField(`units.${i}.unit_cost.cost`, "Cost Amount", unit.unit_cost.cost));
        }
        
        // Localizations
        if (unit.localizations?.length > 0) {
            const locDiv = document.createElement("div");
            locDiv.className = "mt-3 p-3 bg-slate-900 rounded";
            locDiv.appendChild(document.createElement("h5")).textContent = "Localizations";
            locDiv.lastChild.className = "font-semibold text-slate-400 mb-2 text-sm";
            
            unit.localizations.forEach((loc, li) => {
                locDiv.appendChild(createTextField(`units.${i}.localizations.${li}.name`, "Name", loc.name));
                locDiv.appendChild(createTextField(`units.${i}.localizations.${li}.description`, "Description", loc.description));
            });
            itemDiv.appendChild(locDiv);
        }
        
        container.appendChild(itemDiv);
    });
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Unit";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.units.push({
            id: "",
            unit_type: "",
            type_tags: [],
            unit: { base_moves: 2, base_sight_range: 2 },
            icon: { path: "" },
            unit_cost: { yield_type: "", cost: 0 },
            localizations: [{ name: "", description: "" }],
        });
        markDirty();
        renderUnitsSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderConstructiblesSection(container, data) {
    if (!currentData.constructibles) currentData.constructibles = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Constructibles (Buildings/Improvements)";
    container.appendChild(h3);
    
    currentData.constructibles.forEach((constructible, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
        
        const titleDiv = document.createElement("div");
        titleDiv.className = "flex justify-between items-center mb-3";
        const title = document.createElement("h4");
        title.textContent = `Constructible: ${constructible.id || "(New)"}`;
        title.className = "font-semibold text-slate-300";
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
        removeBtn.onclick = () => {
            currentData.constructibles.splice(i, 1);
            markDirty();
            renderConstructiblesSection(container, data);
        };
        
        titleDiv.appendChild(title);
        titleDiv.appendChild(removeBtn);
        itemDiv.appendChild(titleDiv);
        
        // Basic fields
        itemDiv.appendChild(createTextField(`constructibles.${i}.id`, "ID", constructible.id, true));
        itemDiv.appendChild(createTextField(`constructibles.${i}.constructible_type`, "Type", constructible.constructible_type, true));
        
        // Valid districts
        const districts = constructible.constructible_valid_districts || [];
        itemDiv.appendChild(createStringArrayField(`constructibles.${i}.constructible_valid_districts`, "Valid Districts", districts, "constructibles"));
        
        // Icon
        if (constructible.icon) {
            itemDiv.appendChild(createTextField(`constructibles.${i}.icon.path`, "Icon Path", constructible.icon.path));
        }
        
        // Localizations
        if (constructible.localizations?.length > 0) {
            const locDiv = document.createElement("div");
            locDiv.className = "mt-3 p-3 bg-slate-900 rounded";
            locDiv.appendChild(document.createElement("h5")).textContent = "Localizations";
            locDiv.lastChild.className = "font-semibold text-slate-400 mb-2 text-sm";
            
            constructible.localizations.forEach((loc, li) => {
                locDiv.appendChild(createTextField(`constructibles.${i}.localizations.${li}.name`, "Name", loc.name));
                locDiv.appendChild(createTextField(`constructibles.${i}.localizations.${li}.description`, "Description", loc.description));
            });
            itemDiv.appendChild(locDiv);
        }
        
        container.appendChild(itemDiv);
    });
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Constructible";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.constructibles.push({
            id: "",
            constructible_type: "",
            constructible: { cost: 1 },
            building: {},
            type_tags: [],
            constructible_valid_districts: [],
            constructible_maintenances: [],
            yield_changes: [],
            icon: { path: "" },
            advisories: [],
            localizations: [{ name: "", description: "" }],
        });
        markDirty();
        renderConstructiblesSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderModifiersSection(container, data) {
    if (!currentData.modifiers) currentData.modifiers = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Modifiers";
    container.appendChild(h3);
    
    const itemsContainer = document.createElement("div");
    itemsContainer.id = "modifiers-items";
    
    currentData.modifiers.forEach((modifier, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
        itemDiv.dataset.index = i;
        
        const titleDiv = document.createElement("div");
        titleDiv.className = "flex justify-between items-center mb-3";
        const title = document.createElement("h4");
        title.textContent = `Modifier: ${modifier.id || "(New)"}`;
        title.className = "font-semibold text-slate-300";
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.textContent = "Remove";
        removeBtn.className = "px-3 py-1 bg-red-700 hover:bg-red-800 text-white text-sm rounded";
        removeBtn.onclick = () => {
            currentData.modifiers.splice(i, 1);
            markDirty();
            renderModifiersSection(container, data);
        };
        
        titleDiv.appendChild(title);
        titleDiv.appendChild(removeBtn);
        itemDiv.appendChild(titleDiv);
        
        // Basic fields
        itemDiv.appendChild(createTextField(`modifiers.${i}.id`, "ID", modifier.id, true));
        itemDiv.appendChild(createTextField(`modifiers.${i}.modifier_type`, "Modifier Type", modifier.modifier_type));
        
        // Modifier object
        if (!modifier.modifier) modifier.modifier = {};
        const modDiv = document.createElement("div");
        modDiv.className = "mt-3 p-3 bg-slate-900 rounded";
        modDiv.appendChild(document.createElement("h5")).textContent = "Modifier Config";
        modDiv.lastChild.className = "font-semibold text-slate-400 mb-2 text-sm";
        
        modDiv.appendChild(createAutocompleteField(`modifiers.${i}.modifier.collection`, "Collection", modifier.modifier.collection, true, FIELD_HELP_TEXT.collection));
        modDiv.appendChild(createAutocompleteField(`modifiers.${i}.modifier.effect`, "Effect", modifier.modifier.effect, true, FIELD_HELP_TEXT.effect));
        modDiv.appendChild(createBooleanField(`modifiers.${i}.modifier.permanent`, "Permanent", modifier.modifier.permanent));
        modDiv.appendChild(createBooleanField(`modifiers.${i}.modifier.run_once`, "Run Once", modifier.modifier.run_once));
        
        itemDiv.appendChild(modDiv);
        
        // Localizations
        if (modifier.localizations?.length > 0) {
            const locDiv = document.createElement("div");
            locDiv.className = "mt-3 p-3 bg-slate-900 rounded";
            locDiv.appendChild(document.createElement("h5")).textContent = "Localizations";
            locDiv.lastChild.className = "font-semibold text-slate-400 mb-2 text-sm";
            
            modifier.localizations.forEach((loc, li) => {
                locDiv.appendChild(createTextField(`modifiers.${i}.localizations.${li}.description`, "Description", loc.description));
            });
            itemDiv.appendChild(locDiv);
        }
        
        itemsContainer.appendChild(itemDiv);
    });
    
    container.appendChild(itemsContainer);
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Modifier";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.modifiers.push({
            id: "",
            modifier_type: "",
            modifier: {
                collection: "",
                effect: "",
                permanent: false,
                requirements: [],
                arguments: [],
            },
            localizations: [{ description: "" }],
        });
        markDirty();
        renderModifiersSection(container, data);
    };
    container.appendChild(addBtn);
}

function renderBuildSection(container, data) {
    if (!currentData.build) currentData.build = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Build Configuration";
    container.appendChild(h3);
    
    container.appendChild(createTextField("build.output_dir", "Output Directory", currentData.build.output_dir));
    
    const builders = currentData.build.builders || [];
    container.appendChild(createStringArrayField("build.builders", "Builders to Export", builders, "build"));
}