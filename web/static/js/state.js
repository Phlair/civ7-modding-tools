/**
 * State Module - Global state management
 * Centralized state for wizard and expert mode
 */

// ============================================================================
// Global State Variables
// ============================================================================

export let currentData = {};
export let currentFilePath = '';
export let isDirty = false;
export let dataCache = {}; // Cache for reference data fetches

// Wizard state
export let currentMode = 'guided'; // 'guided' or 'expert'
export let wizardStep = 1; // Current wizard step (1-5)
export let wizardData = {}; // Temporary storage for wizard inputs
export let wizardBuildingYields = []; // Temporary storage for yields in form

// Autocomplete usage tracking
export let autocompleteUsageStats = (() => {
    try {
        return JSON.parse(localStorage.getItem('autocompleteUsage') || '{}');
    } catch {
        return {};
    }
})();

// ============================================================================
// Configuration Objects
// ============================================================================

/**
 * Maps field names to reference data types for autocomplete dropdowns
 */
export const AUTOCOMPLETE_MAPPINGS = {
    yield_type: 'yield-types',
    collection: 'collection-types',
    effect: 'effects',
    requirement_type: 'requirement-types',
    core_class: 'core-classes',
    domain: 'domains',
    formation_class: 'formation-classes',
    unit_movement_class: 'unit-movement-classes',
    tag: 'tags',
    district: 'district-types',
    advisory: 'advisory-class-types',
    age_type: 'ages',
    progression_tree_type: 'progression-trees',
    terrain_type: 'terrain-types',
    biome_type: 'biome-types',
    feature_type: 'feature-types',
    constructible_type: 'constructible-classes',
};

/**
 * Contextual help text for fields
 */
export const FIELD_HELP_TEXT = {
    // Age and Action Groups
    collection: 'Scope of effect: ALL_CITIES (everyone), OWNER (your cities), OWNER_UNIT (your units), ALL_PLAYERS (all civilizations)',
    effect: 'Game action: ADJUST_YIELD modifies output, COMBAT_STRENGTH affects unit power, LOYALTY controls city control',
    age_type: 'Game age for unlocks: AGE_ANTIQUITY, AGE_EXPLORATION, AGE_MODERN, AGE_ATOMIC, AGE_INFORMATION',

    // Unit Related
    core_class: 'Unit role: MILITARY (combat), CIVILIAN (workers/settlers), SUPPORT (buffs/heals other units)',
    domain: 'Movement domain: LAND (ground units), SEA (naval units), AIR (aircraft), SPACE (future tech)',
    formation_class: 'Combat formation type: LAND_COMBAT (melee), LAND_RANGED (archers), NAVAL_COMBAT (ships), SIEGE (siege weapons)',
    unit_movement_class: 'Terrain movement: FOOT (infantry), MOUNTED (cavalry), NAVAL (ships), FLYING (aircraft)',
    unit_type: 'Unit ID: UNIT_* for military/civilian units, format like UNIT_BABYLON_SABUM_KIBITTUM',

    // Building Related
    yield_type: 'Resource output: PRODUCTION (building), SCIENCE (research), GOLD (economy), CULTURE (civics), FAITH (religion), TOURISM (great works)',
    constructible_valid_districts: 'Districts where this building can be placed: URBAN (cities), CITY_CENTER (any city), specialized districts',
    constructible_type: 'Building/improvement ID: BUILDING_* for buildings, QUARTER_* for city quarters, IMPROVEMENT_* for map improvements',

    // Civilization Related
    trait_type: 'Civilization trait that gives access: TRAIT_SCIENTIFIC, TRAIT_MILITARY, TRAIT_ECONOMIC, TRAIT_CULTURAL, TRAIT_RELIGIOUS',
    civilization_type: 'Unique civilization identifier, format: CIVILIZATION_NAME (e.g., CIVILIZATION_BABYLON). This is used internally by the game.',

    // Terrain
    terrain_type: 'Terrain classification: PLAINS, FOREST, MOUNTAIN, COAST, DESERT - affects yields and movement',
    biome_type: 'Climate zones: BIOME_TEMPERATE, BIOME_TROPICAL, BIOME_ARID - determines visual style and terrain generation',
    feature_type: 'Map features: FEATURE_FOREST, FEATURE_MARSH, FEATURE_REEF - special terrain modifications',

    // Mod Metadata
    mod_id: 'Unique identifier for your mod. Use lowercase letters, numbers, and hyphens only. Once set, this should not change as it affects save compatibility. Example: \'babylon-scientific-civ\'',

    // Tags
    tag: 'Tags categorize and identify entities. Examples: AGELESS (no age requirement), CULTURE (cultural focus), UNIT_CLASS_MELEE (melee unit type). Over 2,900 tags available.',

    // Requirements
    requirement_type: 'Conditions that must be met for effects to apply. Examples: REQUIREMENT_CITY_IS_CITY (applies to cities), REQUIREMENT_PLAYER_HAS_CIVILIZATION_OR_LEADER_TRAIT (checks for specific trait)',

    // Modifiers
    modifier_permanent: 'If true, the modifier effect persists permanently. If false, it may be temporary or conditional based on requirements.',
    modifier_collection: 'Defines what entities this modifier affects. COLLECTION_OWNER targets your own entities, COLLECTION_ALL affects everyone.',
    modifier_effect: 'The game mechanic that this modifier changes. There are 205+ different effects available, from combat bonuses to yield modifications.',
    modifier_arguments: 'Key-value pairs that configure the effect. Required arguments depend on the effect type chosen. Example: For ADJUST_YIELD, need YieldType and Amount.',

    // Localizations
    localization_name: 'The display name shown to players in the game UI. Should be concise and recognizable.',
    localization_description: 'Detailed description shown in Civilopedia and tooltips. Can be longer and explain mechanics or history.',
    localization_city_names: 'List of city names for this civilization. The first name is used for the capital. Include at least 3-5 names, but 10+ is recommended.',

    // Bindings
    civilization_bindings: 'IDs of other builders to link to this civilization (units, buildings, modifiers, etc.). These must match the \'id\' field of items in other sections.',
};

/**
 * Required fields per section for validation
 */
export const REQUIRED_FIELDS = {
    units: ['id', 'unit_type'],
    constructibles: ['id', 'constructible_type'],
    modifiers: ['id', 'modifier'],
    traditions: ['id', 'tradition_type'],
    progression_tree_nodes: ['id', 'progression_tree_node_type'],
    progression_trees: ['id', 'progression_tree_type'],
};

// ============================================================================
// State Management Functions
// ============================================================================

/**
 * Mark the current state as dirty (unsaved changes)
 * Saves dirty flag to internal state
 */
export function markDirty() {
    isDirty = true;
    import('./ui.js').then(m => m.updateDirtyIndicator(true));
}

/**
 * Set the current data object
 * @param {Object} data - New data object
 */
export function setCurrentData(data) {
    currentData = data;
}

/**
 * Get the current data object
 * @returns {Object} Current data object
 */
export function getCurrentData() {
    return currentData;
}

/**
 * Set the current file path
 * @param {string} path - New file path
 */
export function setCurrentFilePath(path) {
    currentFilePath = path;
}

/**
 * Get the current file path
 * @returns {string} Current file path
 */
export function getCurrentFilePath() {
    return currentFilePath;
}

/**
 * Set the current mode (guided or expert)
 * @param {string} mode - 'guided' or 'expert'
 */
export function setCurrentMode(mode) {
    currentMode = mode;
}

/**
 * Get the current mode
 * @returns {string} Current mode ('guided' or 'expert')
 */
export function getCurrentMode() {
    return currentMode;
}

/**
 * Get wizard data
 * @returns {Object} Wizard data object
 */
export function getWizardData() {
    return wizardData;
}

/**
 * Get wizard step
 * @returns {number} Current wizard step
 */
export function getWizardStep() {
    return wizardStep;
}

/**
 * Reset wizard state to initial values
 */
export function resetWizardData() {
    wizardStep = 1;
    wizardData = {
        metadata: {},
        module_localization: {},
        action_group: {},
        civilization: {},
        units: [],
        constructibles: [],
        modifiers: [],
        traditions: [],
        progression_tree_nodes: [],
        progression_trees: [],
        constants: {},
        imports: [],
        build: { builders: [] },
    };
    wizardBuildingYields = [];
}

/**
 * Set wizard step
 * @param {number} step - Step number (1-5)
 */
export function setWizardStep(step) {
    wizardStep = step;
}

/**
 * Update a field in wizard data
 * @param {string} fieldPath - Dot-separated path to field (e.g., 'metadata.id')
 * @param {any} value - New value
 */
export function updateWizardField(fieldPath, value) {
    if (typeof fieldPath === 'string' && typeof value !== 'undefined') {
        const parts = fieldPath.split('.');
        let target = wizardData;

        for (let i = 0; i < parts.length - 1; i++) {
            const part = parts[i];
            if (!target[part]) target[part] = {};
            target = target[part];
        }

        target[parts[parts.length - 1]] = value;

        if (fieldPath === 'metadata.id' && value) {
            const pascal_case = String(value)
                .split('-')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                .join('');
            if (!wizardData.metadata) wizardData.metadata = {};
            wizardData.metadata.package = pascal_case || value;
        }

        markDirty();
        return;
    }

    if (arguments.length === 3) {
        const [section, field, section_value] = arguments;
        if (!wizardData[section]) wizardData[section] = {};
        wizardData[section][field] = section_value;

        if (section === 'metadata' && field === 'id' && section_value) {
            const pascal_case = String(section_value)
                .split('-')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                .join('');
            wizardData.metadata.package = pascal_case || section_value;
        }

        markDirty();
    }
}

/**
 * Record autocomplete field usage for smart sorting
 * @param {string} fieldName - Field name
 * @param {string} value - Value selected
 */
export function recordAutocompleteUsage(fieldName, value) {
    if (!autocompleteUsageStats[fieldName]) {
        autocompleteUsageStats[fieldName] = {};
    }
    if (!autocompleteUsageStats[fieldName][value]) {
        autocompleteUsageStats[fieldName][value] = 0;
    }
    autocompleteUsageStats[fieldName][value] += 1;

    try {
        localStorage.setItem('autocompleteUsage', JSON.stringify(autocompleteUsageStats));
    } catch {
        // Silently fail if localStorage is full or unavailable
    }
}

/**
 * Clear all state (for new mod creation)
 */
export function clearAllState() {
    currentData = {};
    currentFilePath = '';
    isDirty = false;
    resetWizardData();
    import('./ui.js').then(m => m.updateDirtyIndicator(false));
}

/**
 * Merge wizard data into current data
 * Used when transitioning from wizard to expert mode
 */
export function syncWizardToCurrentData() {
    currentData = { ...currentData, ...wizardData };
}

/**
 * Get cached reference data
 * @param {string} dataType - Type of reference data
 * @returns {Array|null} Cached data or null if not cached
 */
export function getCachedReferenceData(dataType) {
    return dataCache[dataType] || null;
}

/**
 * Set cached reference data
 * @param {string} dataType - Type of reference data
 * @param {Array} data - Reference data to cache
 */
export function setCachedReferenceData(dataType, data) {
    dataCache[dataType] = data;
}

/**
 * Clear reference data cache
 */
export function clearReferenceDataCache() {
    dataCache = {};
}

/**
 * Update a field in current data using a dot-path
 * @param {string|Event} fieldPath - Dot-separated path or event object
 * @param {any} value - Value to set
 */
export function updateFieldValue(fieldPath, value) {
    if (typeof fieldPath === 'object' && fieldPath?.target) {
        const input = fieldPath.target;
        const section = input.closest('[data-section]')?.dataset.section;
        const field = input.dataset.field;

        if (section && field) {
            if (!currentData[section]) {
                currentData[section] = {};
            }

            if (input.type === 'checkbox') {
                currentData[section][field] = input.checked;
            } else {
                currentData[section][field] = input.value;
            }

            markDirty();
        }
        return;
    }

    const parts = String(fieldPath).split('.');
    let obj = currentData;

    for (let i = 0; i < parts.length - 1; i++) {
        const part = parts[i];
        const next_part = parts[i + 1];

        if (!isNaN(part)) {
            const index = parseInt(part, 10);
            const parent = obj;
            const parent_key = parts[i - 1];

            if (!Array.isArray(parent[parent_key])) {
                parent[parent_key] = [];
            }

            if (!parent[parent_key][index]) {
                parent[parent_key][index] = isNaN(next_part) ? {} : [];
            }

            obj = parent[parent_key][index];
            continue;
        }

        if (!obj[part]) {
            obj[part] = isNaN(next_part) ? {} : [];
        }
        obj = obj[part];
    }

    const last_part = parts[parts.length - 1];
    obj[last_part] = value;
    markDirty();
}
