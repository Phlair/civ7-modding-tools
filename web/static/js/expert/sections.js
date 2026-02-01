/**
 * Expert Mode Sections - Main section renderers
 * Handles rendering of all 13 editor sections
 */

import { getAvailableSections } from './navigation.js';
import { getCurrentData, markDirty } from '../state.js';
import { 
    createTextField, 
    createNumberField, 
    createBooleanField, 
    createStringArrayField,
    createAutocompleteField 
} from '../form/fields.js';

const COLOR_MAP = {
    'blue': 'text-blue-400',
    'purple': 'text-purple-400',
    'amber': 'text-amber-400',
    'cyan': 'text-cyan-400',
    'red': 'text-red-400',
    'green': 'text-green-400',
    'orange': 'text-orange-400',
    'indigo': 'text-indigo-400',
    'yellow': 'text-yellow-400',
    'lime': 'text-lime-400',
    'emerald': 'text-emerald-400',
    'teal': 'text-teal-400',
    'sky': 'text-sky-400',
    'pink': 'text-pink-400',
    'violet': 'text-violet-400',
    'fuchsia': 'text-fuchsia-400',
};

/**
 * Render all sections into editor container
 * @param {HTMLElement} container - Editor container element
 * @param {Object} data - Current data object
 */
export function renderAllSections(container, data) {
    if (!container) return;

    container.innerHTML = '';

    const sections = getAvailableSections();

    sections.forEach(({ id, title, color }) => {
        const section = document.createElement('section');
        section.setAttribute('data-section-id', id);
        section.className = `mb-8 bg-slate-900/50 p-6 rounded-lg border border-slate-700 transition-colors hover:border-slate-600`;

        // Header with collapsible toggle
        const header = document.createElement('div');
        header.className = 'flex items-center justify-between cursor-pointer hover:opacity-80';
        header.onclick = () => toggleSection(section);

        const title_elem = document.createElement('h2');
        title_elem.className = `text-xl font-bold ${COLOR_MAP[color] || 'text-blue-400'}`;
        title_elem.textContent = title;

        const toggle = document.createElement('span');
        toggle.className = 'transition-transform duration-200 text-slate-400';
        toggle.textContent = '▼';

        header.appendChild(title_elem);
        header.appendChild(toggle);
        section.appendChild(header);

        // Content area (initially visible)
        const content = document.createElement('div');
        content.className = 'section-content mt-4';
        content.setAttribute('data-section', id);
        section.appendChild(content);

        container.appendChild(section);

        // Render section content
        renderSectionContent(content, id, data[id]);
    });

    console.log('[SECTIONS_RENDERED] All 13 sections rendered');
}

/**
 * Toggle section visibility
 * @param {HTMLElement} section - Section element
 */
function toggleSection(section) {
    const content = section.querySelector('.section-content');
    if (content) {
        content.classList.toggle('hidden');
        const toggle = section.querySelector('span:last-child');
        if (toggle) {
            toggle.classList.toggle('rotate-180');
        }
    }
}

/**
 * Render content for a specific section
 * @param {HTMLElement} container - Container element
 * @param {string} sectionId - Section ID
 * @param {Object} data - Section data
 */
function renderSectionContent(container, sectionId, data) {
    switch (sectionId) {
        case 'metadata':
            renderMetadataSection(container, data);
            break;
        case 'module_localization':
            renderModuleLocalizationSection(container, data);
            break;
        case 'action_group':
            renderActionGroupSection(container, data);
            break;
        case 'civilization':
            renderCivilizationSection(container, data);
            break;
        case 'units':
            renderUnitsSection(container, data);
            break;
        case 'constructibles':
            renderConstructiblesSection(container, data);
            break;
        case 'modifiers':
            renderModifiersSection(container, data);
            break;
        case 'traditions':
            renderTraditionsSection(container, data);
            break;
        case 'constants':
            renderConstantsSection(container, data);
            break;
        case 'imports':
            renderImportsSection(container, data);
            break;
        case 'progression_tree_nodes':
            renderProgressionTreeNodesSection(container, data);
            break;
        case 'progression_trees':
            renderProgressionTreesSection(container, data);
            break;
        case 'build':
            renderBuildSection(container, data);
            break;
    }
}

/**
 * Update field value in data structure
 * @param {string} fieldPath - Dot-notation path (e.g., "metadata.id" or "units.0.unit_type")
 * @param {*} value - New value
 */
export function updateFieldValue(fieldPath, value) {
    const currentData = getCurrentData();
    const parts = fieldPath.split(".");
    let obj = currentData;

    // Navigate/create nested structure
    for (let i = 0; i < parts.length - 1; i++) {
        const part = parts[i];
        // Check if this part is an array index
        if (!isNaN(part)) {
            // Get the array from previous object
            const arrayIndex = parseInt(part);
            obj = obj[arrayIndex];
            if (!obj) {
                console.error(`Invalid array index ${part} in path ${fieldPath}`);
                return;
            }
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
// Section Renderers
// ============================================================================

/**
 * Render metadata section
 */
function renderMetadataSection(container, data) {
    const currentData = getCurrentData();
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
    container.appendChild(createTextField("metadata.package", "Package", meta.package, true));
}

/**
 * Render module localization section
 */
function renderModuleLocalizationSection(container, data) {
    const currentData = getCurrentData();
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

/**
 * Render action group section
 */
function renderActionGroupSection(container, data) {
    const currentData = getCurrentData();
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Action Group";
    container.appendChild(h3);
    
    const actionGroup = currentData.action_group?.action_group_id || "";
    container.appendChild(createTextField("action_group.action_group_id", "Action Group ID", actionGroup));
}

/**
 * Render civilization section (uses sub-renderers from civilization.js)
 */
function renderCivilizationSection(container, data) {
    const currentData = getCurrentData();
    if (!currentData.civilization) currentData.civilization = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Civilization";
    container.appendChild(h3);
    
    const civ = currentData.civilization;
    
    // Basic fields
    container.appendChild(createTextField("civilization.civilization_type", "Type", civ.civilization_type, true));
    container.appendChild(createTextField("civilization.inherit_from", "Inherit From", civ.inherit_from));
    container.appendChild(createTextField("civilization.domain", "Domain", civ.domain));
    container.appendChild(createTextField("civilization.unique_culture_progression_tree", "Unique Culture Progression Tree", civ.unique_culture_progression_tree));
    container.appendChild(createNumberField("civilization.random_city_name_depth", "Random City Name Depth", civ.random_city_name_depth));
    
    // Traits array
    const traitsSection = document.createElement("div");
    traitsSection.className = "mt-4";
    const traitsLabel = document.createElement("label");
    traitsLabel.className = "block text-sm font-medium text-slate-300 mb-2";
    traitsLabel.textContent = "Civilization Traits";
    traitsSection.appendChild(traitsLabel);
    traitsSection.appendChild(createStringArrayField("civilization.civilization_traits", "Traits", civ.civilization_traits || [], "civilization"));
    container.appendChild(traitsSection);
    
    // Tags array
    const tagsSection = document.createElement("div");
    tagsSection.className = "mt-4";
    const tagsLabel = document.createElement("label");
    tagsLabel.className = "block text-sm font-medium text-slate-300 mb-2";
    tagsLabel.textContent = "Tags";
    tagsSection.appendChild(tagsLabel);
    tagsSection.appendChild(createStringArrayField("civilization.tags", "Tags", civ.tags || [], "civilization"));
    container.appendChild(tagsSection);
    
    // Icon configuration
    if (civ.icon || true) {
        const iconSection = document.createElement("div");
        iconSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const iconHeader = document.createElement("h4");
        iconHeader.className = "font-semibold text-slate-300 mb-3";
        iconHeader.textContent = "Icon Configuration";
        iconSection.appendChild(iconHeader);
        if (!civ.icon) civ.icon = {};
        iconSection.appendChild(createTextField("civilization.icon.path", "Icon Path", civ.icon.path));
        container.appendChild(iconSection);
    }
    
    // Import comprehensive sub-renderers from civilization.js
    // These handle complex nested structures
    import('../expert/civilization.js').then((civilizationModule) => {
        // Start Bias Terrains
        const terrainSection = document.createElement("div");
        terrainSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const terrainHeader = document.createElement("h4");
        terrainHeader.className = "font-semibold text-slate-300 mb-3";
        terrainHeader.textContent = "Start Bias Terrains";
        terrainSection.appendChild(terrainHeader);
        const terrainContainer = document.createElement("div");
        terrainSection.appendChild(terrainContainer);
        civilizationModule.renderStartBiasTerrains(terrainContainer);
        container.appendChild(terrainSection);
        
        // Start Bias Rivers
        const riverSection = document.createElement("div");
        riverSection.className = "mt-4";
        riverSection.appendChild(createNumberField("civilization.start_bias_rivers", "Start Bias Rivers", civ.start_bias_rivers));
        container.appendChild(riverSection);
        
        // Civilization Unlocks
        const unlocksSection = document.createElement("div");
        unlocksSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const unlocksHeader = document.createElement("h4");
        unlocksHeader.className = "font-semibold text-slate-300 mb-3";
        unlocksHeader.textContent = "Civilization Unlocks (Age Transitions)";
        unlocksSection.appendChild(unlocksHeader);
        const unlocksContainer = document.createElement("div");
        unlocksSection.appendChild(unlocksContainer);
        civilizationModule.renderCivilizationUnlocks(unlocksContainer);
        container.appendChild(unlocksSection);
        
        // Leader Civilization Biases
        const biasesSection = document.createElement("div");
        biasesSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const biasesHeader = document.createElement("h4");
        biasesHeader.className = "font-semibold text-slate-300 mb-3";
        biasesHeader.textContent = "Leader Civilization Biases";
        biasesSection.appendChild(biasesHeader);
        const biasesContainer = document.createElement("div");
        biasesSection.appendChild(biasesContainer);
        civilizationModule.renderLeaderCivilizationBiases(biasesContainer);
        container.appendChild(biasesSection);
        
        // Localizations
        const locSection = document.createElement("div");
        locSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const locHeader = document.createElement("h4");
        locHeader.className = "font-semibold text-slate-300 mb-3";
        locHeader.textContent = "Localizations";
        locSection.appendChild(locHeader);
        const locContainer = document.createElement("div");
        locSection.appendChild(locContainer);
        civilizationModule.renderLocalizations(locContainer);
        container.appendChild(locSection);
        
        // Loading Info
        const loadingSection = document.createElement("div");
        loadingSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const loadingHeader = document.createElement("h4");
        loadingHeader.className = "font-semibold text-slate-300 mb-3";
        loadingHeader.textContent = "Loading Screen Information";
        loadingSection.appendChild(loadingHeader);
        const loadingContainer = document.createElement("div");
        loadingSection.appendChild(loadingContainer);
        civilizationModule.renderLoadingInfoCivilizations(loadingContainer);
        container.appendChild(loadingSection);
        
        // Leader Civ Priorities
        const prioritiesSection = document.createElement("div");
        prioritiesSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const prioritiesHeader = document.createElement("h4");
        prioritiesHeader.className = "font-semibold text-slate-300 mb-3";
        prioritiesHeader.textContent = "Leader Civilization Priorities (AI)";
        prioritiesSection.appendChild(prioritiesHeader);
        const prioritiesContainer = document.createElement("div");
        prioritiesSection.appendChild(prioritiesContainer);
        civilizationModule.renderLeaderCivPriorities(prioritiesContainer);
        container.appendChild(prioritiesSection);
        
        // AI List Types
        const aiListTypesSection = document.createElement("div");
        aiListTypesSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const aiListTypesHeader = document.createElement("h4");
        aiListTypesHeader.className = "font-semibold text-slate-300 mb-3";
        aiListTypesHeader.textContent = "AI List Types";
        aiListTypesSection.appendChild(aiListTypesHeader);
        const aiListTypesContainer = document.createElement("div");
        aiListTypesSection.appendChild(aiListTypesContainer);
        civilizationModule.renderAIListTypes(aiListTypesContainer);
        container.appendChild(aiListTypesSection);
        
        // AI Lists
        const aiListsSection = document.createElement("div");
        aiListsSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const aiListsHeader = document.createElement("h4");
        aiListsHeader.className = "font-semibold text-slate-300 mb-3";
        aiListsHeader.textContent = "AI Lists";
        aiListsSection.appendChild(aiListsHeader);
        const aiListsContainer = document.createElement("div");
        aiListsSection.appendChild(aiListsContainer);
        civilizationModule.renderAILists(aiListsContainer);
        container.appendChild(aiListsSection);
        
        // AI Favored Items
        const aiFavoredSection = document.createElement("div");
        aiFavoredSection.className = "mt-4 p-4 bg-slate-800/50 rounded border border-slate-600";
        const aiFavoredHeader = document.createElement("h4");
        aiFavoredHeader.className = "font-semibold text-slate-300 mb-3";
        aiFavoredHeader.textContent = "AI Favored Items";
        aiFavoredSection.appendChild(aiFavoredHeader);
        const aiFavoredContainer = document.createElement("div");
        aiFavoredSection.appendChild(aiFavoredContainer);
        civilizationModule.renderAIFavoredItems(aiFavoredContainer);
        container.appendChild(aiFavoredSection);
        
        // Visual Art Cultures
        const buildingCultureSection = document.createElement("div");
        buildingCultureSection.className = "mt-4";
        const buildingCultureLabel = document.createElement("label");
        buildingCultureLabel.className = "block text-sm font-medium text-slate-300 mb-2";
        buildingCultureLabel.textContent = "Building Art Cultures";
        buildingCultureSection.appendChild(buildingCultureLabel);
        buildingCultureSection.appendChild(createStringArrayField("civilization.art_eras_building", "Building Cultures", civ.art_eras_building || [], "civilization"));
        container.appendChild(buildingCultureSection);
        
        const unitCultureSection = document.createElement("div");
        unitCultureSection.className = "mt-4";
        const unitCultureLabel = document.createElement("label");
        unitCultureLabel.className = "block text-sm font-medium text-slate-300 mb-2";
        unitCultureLabel.textContent = "Unit Art Cultures";
        unitCultureSection.appendChild(unitCultureLabel);
        unitCultureSection.appendChild(createStringArrayField("civilization.art_eras_unit", "Unit Cultures", civ.art_eras_unit || [], "civilization"));
        container.appendChild(unitCultureSection);
        
        // Bindings
        const bindingsSection = document.createElement("div");
        bindingsSection.className = "mt-4";
        const bindingsLabel = document.createElement("label");
        bindingsLabel.className = "block text-sm font-medium text-slate-300 mb-2";
        bindingsLabel.textContent = "Bindings";
        bindingsSection.appendChild(bindingsLabel);
        bindingsSection.appendChild(createStringArrayField("civilization.bindings", "Bindings", civ.bindings || [], "civilization"));
        container.appendChild(bindingsSection);
    }).catch((err) => {
        console.error('[CIVILIZATION_SECTION] Failed to load civilization module:', err);
    });
}

/**
 * Render constants section
 */
function renderConstantsSection(container, data) {
    const currentData = getCurrentData();
    if (!currentData.constants) currentData.constants = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Constants";
    container.appendChild(h3);
    
    const cityNames = currentData.constants.city_names || [];
    container.appendChild(createStringArrayField("constants.city_names", "City Names", cityNames, "constants"));
}

/**
 * Render imports section
 */
function renderImportsSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
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

/**
 * Render traditions section
 */
function renderTraditionsSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
    if (!currentData.traditions) currentData.traditions = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Traditions";
    container.appendChild(h3);
    
    const itemsContainer = document.createElement("div");
    
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
        itemDiv.appendChild(createTextField(`traditions.${i}.tradition_type`, "Type", tradition.tradition_type, true));
        
        itemsContainer.appendChild(itemDiv);
    });
    
    container.appendChild(itemsContainer);
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Tradition";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.traditions.push({ id: "", tradition_type: "" });
        markDirty();
        renderTraditionsSection(container, data);
    };
    container.appendChild(addBtn);
}

/**
 * Render progression tree nodes section
 */
function renderProgressionTreeNodesSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
    if (!currentData.progression_tree_nodes) currentData.progression_tree_nodes = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Progression Tree Nodes";
    container.appendChild(h3);
    
    const itemsContainer = document.createElement("div");
    itemsContainer.id = "progression-tree-nodes-items";
    
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
        itemDiv.appendChild(createTextField(`progression_tree_nodes.${i}.progression_tree_node_type`, "Type", node.progression_tree_node_type, true));
        
        itemsContainer.appendChild(itemDiv);
    });
    
    container.appendChild(itemsContainer);
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Node";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.progression_tree_nodes.push({ id: "", progression_tree_node_type: "" });
        markDirty();
        renderProgressionTreeNodesSection(container, data);
    };
    container.appendChild(addBtn);
}

/**
 * Render progression trees section
 */
function renderProgressionTreesSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
    if (!currentData.progression_trees) currentData.progression_trees = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Progression Trees";
    container.appendChild(h3);
    
    const itemsContainer = document.createElement("div");
    itemsContainer.id = "progression-trees-items";
    
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
        itemDiv.appendChild(createTextField(`progression_trees.${i}.progression_tree_type`, "Type", tree.progression_tree_type, true));
        
        itemsContainer.appendChild(itemDiv);
    });
    
    container.appendChild(itemsContainer);
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Tree";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.progression_trees.push({ id: "", progression_tree_type: "" });
        markDirty();
        renderProgressionTreesSection(container, data);
    };
    container.appendChild(addBtn);
}

/**
 * Render units section
 */
function renderUnitsSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
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
        itemDiv.appendChild(createTextField(`units.${i}.unit_type`, "Type", unit.unit_type, true));
        
        // Unit stats
        if (unit.unit) {
            itemDiv.appendChild(createNumberField(`units.${i}.unit.base_moves`, "Base Moves", unit.unit.base_moves));
            itemDiv.appendChild(createNumberField(`units.${i}.unit.base_sight_range`, "Base Sight Range", unit.unit.base_sight_range));
        }
        
        // Icon
        if (unit.icon) {
            itemDiv.appendChild(createTextField(`units.${i}.icon.path`, "Icon Path", unit.icon.path));
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
            unit: { base_moves: 2, base_sight_range: 2 },
            icon: { path: "" }
        });
        markDirty();
        renderUnitsSection(container, data);
    };
    container.appendChild(addBtn);
}

/**
 * Render constructibles section
 */
function renderConstructiblesSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
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
            constructible_valid_districts: [],
            icon: { path: "" }
        });
        markDirty();
        renderConstructiblesSection(container, data);
    };
    container.appendChild(addBtn);
}

/**
 * Render modifiers section
 */
function renderModifiersSection(container, data) {
    const currentData = getCurrentData();
    container.innerHTML = "";
    if (!currentData.modifiers) currentData.modifiers = [];
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Modifiers";
    container.appendChild(h3);
    
    currentData.modifiers.forEach((modifier, i) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "p-4 mb-4 bg-slate-800 border border-slate-700 rounded";
        
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
        
        // Modifier details
        if (modifier.modifier) {
            itemDiv.appendChild(createAutocompleteField(`modifiers.${i}.modifier.collection`, "Collection", modifier.modifier.collection, false, "Scope of effect"));
            itemDiv.appendChild(createAutocompleteField(`modifiers.${i}.modifier.effect`, "Effect", modifier.modifier.effect, false, "Game action"));
        }

        const previewValue = (modifier.modifier_strings || []).find(
            s => s.string_type === 'PREVIEW_DESCRIPTION'
        )?.text || '';
        const tooltipValue = (modifier.modifier_strings || []).find(
            s => s.string_type === 'TOOLTIP'
        )?.text || '';

        const stringsWrapper = document.createElement('div');
        stringsWrapper.className = 'mt-4 p-3 bg-slate-900/50 border border-slate-700 rounded';

        const stringsTitle = document.createElement('h5');
        stringsTitle.className = 'text-sm font-semibold text-slate-300 mb-2';
        stringsTitle.textContent = 'Battle Tooltip (Optional)';
        stringsWrapper.appendChild(stringsTitle);

        const previewField = document.createElement('div');
        previewField.className = 'mb-3';
        previewField.innerHTML = `
            <label class="block text-sm font-medium text-slate-300 mb-2">Preview Description</label>
            <input
                type="text"
                value="${previewValue.replace(/"/g, '&quot;')}"
                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors"
                placeholder="Shows in combat preview"
            />
        `;
        const previewInput = previewField.querySelector('input');
        previewInput.addEventListener('input', (e) => {
            const text = e.target.value.trim();
            if (!modifier.modifier_strings) modifier.modifier_strings = [];
            modifier.modifier_strings = modifier.modifier_strings.filter(
                s => s.string_type !== 'PREVIEW_DESCRIPTION'
            );
            if (text) {
                modifier.modifier_strings.push({ string_type: 'PREVIEW_DESCRIPTION', text: text });
            }
            markDirty();
        });
        stringsWrapper.appendChild(previewField);

        const tooltipField = document.createElement('div');
        tooltipField.innerHTML = `
            <label class="block text-sm font-medium text-slate-300 mb-2">Tooltip Text</label>
            <input
                type="text"
                value="${tooltipValue.replace(/"/g, '&quot;')}"
                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors"
                placeholder="Shows in unit tooltip"
            />
        `;
        const tooltipInput = tooltipField.querySelector('input');
        tooltipInput.addEventListener('input', (e) => {
            const text = e.target.value.trim();
            if (!modifier.modifier_strings) modifier.modifier_strings = [];
            modifier.modifier_strings = modifier.modifier_strings.filter(
                s => s.string_type !== 'TOOLTIP'
            );
            if (text) {
                modifier.modifier_strings.push({ string_type: 'TOOLTIP', text: text });
            }
            markDirty();
        });
        stringsWrapper.appendChild(tooltipField);

        itemDiv.appendChild(stringsWrapper);
        
        container.appendChild(itemDiv);
    });
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "+ Add Modifier";
    addBtn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition";
    addBtn.onclick = () => {
        currentData.modifiers.push({
            id: "",
            modifier: { collection: "", effect: "" }
        });
        markDirty();
        renderModifiersSection(container, data);
    };
    container.appendChild(addBtn);
}

/**
 * Render build section
 */
function renderBuildSection(container, data) {
    const currentData = getCurrentData();
    if (!currentData.build) currentData.build = {};
    
    const h3 = document.createElement("h3");
    h3.className = "text-lg font-semibold text-slate-200 mb-4";
    h3.textContent = "Build Configuration";
    container.appendChild(h3);
    
    const buildPath = currentData.build.output_path || "";
    container.appendChild(createTextField("build.output_path", "Output Path", buildPath));
    container.appendChild(createBooleanField("build.clear_output", "Clear Output Directory", currentData.build.clear_output !== false));
}
