/**
 * Civ VII Mod Editor - Main JavaScript Logic
 * Handles YAML loading/saving, form management, validation, and UI interactions
 */

// Global state
let currentData = {};
let currentFilePath = "";
let isDirty = false;
let dataCache = {}; // Cache for reference data

// Wizard state
let currentMode = 'guided'; // 'guided' or 'expert'
let wizardStep = 1; // Current wizard step (1-5)
let wizardData = {}; // Temporary storage for wizard inputs

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
    // Age and Action Groups
    collection: "Scope of effect: ALL_CITIES (everyone), OWNER (your cities), OWNER_UNIT (your units), ALL_PLAYERS (all civilizations)",
    effect: "Game action: ADJUST_YIELD modifies output, COMBAT_STRENGTH affects unit power, LOYALTY controls city control",
    age_type: "Game age for unlocks: AGE_ANTIQUITY, AGE_EXPLORATION, AGE_MODERN, AGE_ATOMIC, AGE_INFORMATION",
    
    // Unit Related
    core_class: "Unit role: MILITARY (combat), CIVILIAN (workers/settlers), SUPPORT (buffs/heals other units)",
    domain: "Movement domain: LAND (ground units), SEA (naval units), AIR (aircraft), SPACE (future tech)",
    formation_class: "Combat formation type: LAND_COMBAT (melee), LAND_RANGED (archers), NAVAL_COMBAT (ships), SIEGE (siege weapons)",
    unit_movement_class: "Terrain movement: FOOT (infantry), MOUNTED (cavalry), NAVAL (ships), FLYING (aircraft)",
    unit_type: "Unit ID: UNIT_* for military/civilian units, format like UNIT_BABYLON_SABUM_KIBITTUM",
    
    // Building Related
    yield_type: "Resource output: PRODUCTION (building), SCIENCE (research), GOLD (economy), CULTURE (civics), FAITH (religion), TOURISM (great works)",
    constructible_valid_districts: "Districts where this building can be placed: URBAN (cities), CITY_CENTER (any city), specialized districts",
    constructible_type: "Building/improvement ID: BUILDING_* for buildings, QUARTER_* for city quarters, IMPROVEMENT_* for map improvements",
    
    // Civilization Related
    trait_type: "Civilization trait that gives access: TRAIT_SCIENTIFIC, TRAIT_MILITARY, TRAIT_ECONOMIC, TRAIT_CULTURAL, TRAIT_RELIGIOUS",
    civilization_type: "Unique civilization identifier, format: CIVILIZATION_NAME (e.g., CIVILIZATION_BABYLON). This is used internally by the game.",
    
    // Terrain
    terrain_type: "Terrain classification: PLAINS, FOREST, MOUNTAIN, COAST, DESERT - affects yields and movement",
    biome_type: "Climate zones: BIOME_TEMPERATE, BIOME_TROPICAL, BIOME_ARID - determines visual style and terrain generation",
    feature_type: "Map features: FEATURE_FOREST, FEATURE_MARSH, FEATURE_REEF - special terrain modifications",
    
    // Mod Metadata
    mod_id: "Unique identifier for your mod. Use lowercase letters, numbers, and hyphens only. Once set, this should not change as it affects save compatibility. Example: 'babylon-scientific-civ'",
    
    // Tags
    tag: "Tags categorize and identify entities. Examples: AGELESS (no age requirement), CULTURE (cultural focus), UNIT_CLASS_MELEE (melee unit type). Over 2,900 tags available.",
    
    // Requirements
    requirement_type: "Conditions that must be met for effects to apply. Examples: REQUIREMENT_CITY_IS_CITY (applies to cities), REQUIREMENT_PLAYER_HAS_CIVILIZATION_OR_LEADER_TRAIT (checks for specific trait)",
    
    // Modifiers  
    modifier_permanent: "If true, the modifier effect persists permanently. If false, it may be temporary or conditional based on requirements.",
    modifier_collection: "Defines what entities this modifier affects. COLLECTION_OWNER targets your own entities, COLLECTION_ALL affects everyone.",
    modifier_effect: "The game mechanic that this modifier changes. There are 205+ different effects available, from combat bonuses to yield modifications.",
    modifier_arguments: "Key-value pairs that configure the effect. Required arguments depend on the effect type chosen. Example: For ADJUST_YIELD, need YieldType and Amount.",
    
    // Localizations
    localization_name: "The display name shown to players in the game UI. Should be concise and recognizable.",
    localization_description: "Detailed description shown in Civilopedia and tooltips. Can be longer and explain mechanics or history.",
    localization_city_names: "List of city names for this civilization. The first name is used for the capital. Include at least 3-5 names, but 10+ is recommended.",
    
    // Bindings
    civilization_bindings: "IDs of other builders to link to this civilization (units, buildings, modifiers, etc.). These must match the 'id' field of items in other sections.",
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
    initializeMode();
});

// ============================================================================
// Mode Switching (Guided vs Expert)
// ============================================================================

function initializeMode() {
    // Start in guided mode by default for new users
    const savedMode = localStorage.getItem('editorMode') || 'guided';
    switchMode(savedMode, false);
}

function switchMode(mode, savePreference = true) {
    currentMode = mode;
    
    if (savePreference) {
        localStorage.setItem('editorMode', mode);
    }
    
    const wizardContainer = document.getElementById('wizard-container');
    const editorContainer = document.getElementById('editor-container');
    const sidebar = document.querySelector('aside');
    const guidedBtn = document.getElementById('mode-guided');
    const expertBtn = document.getElementById('mode-expert');
    
    if (mode === 'guided') {
        // Show wizard, hide expert editor
        wizardContainer?.classList.remove('hidden');
        editorContainer?.classList.add('hidden');
        sidebar?.classList.add('hidden');
        
        // Update button styles
        guidedBtn?.classList.add('bg-blue-600', 'text-white');
        guidedBtn?.classList.remove('text-slate-400', 'hover:text-slate-200');
        expertBtn?.classList.remove('bg-blue-600', 'text-white');
        expertBtn?.classList.add('text-slate-400', 'hover:text-slate-200');
        
        // Initialize wizard if starting fresh
        if (!currentFilePath && wizardStep === 1) {
            initializeWizard();
        } else {
            renderWizardStep();
        }
    } else {
        // Show expert editor, hide wizard
        wizardContainer?.classList.add('hidden');
        editorContainer?.classList.remove('hidden');
        sidebar?.classList.remove('hidden');
        
        // Update button styles
        expertBtn?.classList.add('bg-blue-600', 'text-white');
        expertBtn?.classList.remove('text-slate-400', 'hover:text-slate-200');
        guidedBtn?.classList.remove('bg-blue-600', 'text-white');
        guidedBtn?.classList.add('text-slate-400', 'hover:text-slate-200');
        
        // Sync wizard data to currentData before switching
        if (Object.keys(wizardData).length > 0) {
            syncWizardToCurrentData();
        }
        
        // Render all sections if we have data
        if (Object.keys(currentData).length > 0) {
            renderAllSections();
        }
    }
}

function skipWizard() {
    if (confirm('Switch to Expert Mode? You can always switch back using the toggle at the top.')) {
        switchMode('expert');
    }
}

// ============================================================================
// Wizard Flow
// ============================================================================

function initializeWizard() {
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
        build: { builders: [] }
    };
    renderWizardStep();
}

function renderWizardStep() {
    const content = document.getElementById('wizard-step-content');
    const indicator = document.getElementById('wizard-step-indicator');
    const prevBtn = document.getElementById('wizard-prev-btn');
    const nextBtn = document.getElementById('wizard-next-btn');
    
    if (!content) return;
    
    // Update indicator
    if (indicator) {
        indicator.textContent = `Step ${wizardStep} of 5`;
    }
    
    // Update progress bar
    for (let i = 1; i <= 5; i++) {
        const progressBar = document.getElementById(`progress-step-${i}`);
        if (progressBar) {
            if (i < wizardStep) {
                progressBar.className = 'wizard-progress-step flex-1 h-2 bg-green-600 rounded-full transition-all';
            } else if (i === wizardStep) {
                progressBar.className = 'wizard-progress-step flex-1 h-2 bg-blue-600 rounded-full transition-all';
            } else {
                progressBar.className = 'wizard-progress-step flex-1 h-2 bg-slate-700 rounded-full transition-all';
            }
        }
    }
    
    // Update button states
    if (prevBtn) {
        prevBtn.disabled = wizardStep === 1;
    }
    if (nextBtn) {
        if (wizardStep === 5) {
            nextBtn.textContent = 'Finish & Save';
            nextBtn.className = 'px-6 py-2 bg-green-600 hover:bg-green-700 rounded-lg font-medium transition-colors';
        } else {
            nextBtn.textContent = 'Next →';
            nextBtn.className = 'px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors';
        }
    }
    
    // Render step content
    switch (wizardStep) {
        case 1:
            renderWizardStep1(content);
            break;
        case 2:
            renderWizardStep2(content);
            break;
        case 3:
            renderWizardStep3(content);
            break;
        case 4:
            renderWizardStep4(content);
            break;
        case 5:
            renderWizardStep5(content);
            break;
    }
}

function wizardNextStep() {
    if (wizardStep === 5) {
        // Finish wizard - sync data, auto-generate content, and save
        syncWizardToCurrentData();
        
        // Auto-generate default progression tree if not already created
        generateDefaultProgressionTree();
        
        switchMode('expert');
        showToast('Wizard completed! Default progression tree created. Review in Expert Mode.', 'success');
        return;
    }
    
    // Save current step data
    saveWizardStepData();
    
    // Move to next step
    wizardStep++;
    renderWizardStep();
}

function wizardPrevStep() {
    if (wizardStep > 1) {
        saveWizardStepData();
        wizardStep--;
        renderWizardStep();
    }
}

function saveWizardStepData() {
    // This will be called when moving between steps to save form data
    // Specific implementation in each step renderer
    markDirty();
}

function syncWizardToCurrentData() {
    // Merge wizardData into currentData
    currentData = { ...currentData, ...wizardData };
}

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

// ============================================================================
// Wizard Step Renderers
// ============================================================================

function renderWizardStep1(container) {
    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-blue-400">📋 Step 1: Basic Information</h3>
                <p class="text-slate-400 text-sm mb-6">Let's start with the essential details about your mod and civilization.</p>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Metadata Section -->
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-blue-500"></span>
                        Mod Information
                    </h4>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Mod ID <span class="text-red-400">*</span>
                                <button onclick="showFieldHelp('mod_id')" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-metadata-id" 
                                value="${wizardData.metadata?.id || ''}"
                                onchange="updateWizardField('metadata', 'id', this.value)"
                                placeholder="e.g., my-civilization-mod"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                            <p class="text-xs text-slate-500 mt-1">Unique identifier (lowercase, hyphens allowed)</p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Version</label>
                            <input 
                                type="text" 
                                id="wizard-metadata-version" 
                                value="${wizardData.metadata?.version || '1.0.0'}"
                                onchange="updateWizardField('metadata', 'version', this.value)"
                                placeholder="1.0.0"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Mod Name <span class="text-red-400">*</span>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-metadata-name" 
                                value="${wizardData.metadata?.name || ''}"
                                onchange="updateWizardField('metadata', 'name', this.value)"
                                placeholder="My Civilization Mod"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Description</label>
                            <textarea 
                                id="wizard-metadata-description" 
                                onchange="updateWizardField('metadata', 'description', this.value)"
                                placeholder="Brief description of your mod..."
                                rows="3"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >${wizardData.metadata?.description || ''}</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Authors</label>
                            <input 
                                type="text" 
                                id="wizard-metadata-authors" 
                                value="${wizardData.metadata?.authors || ''}"
                                onchange="updateWizardField('metadata', 'authors', this.value)"
                                placeholder="Your Name"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                    </div>
                </div>
                
                <!-- Module Localization & Age -->
                <div class="space-y-4">
                    <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                        <h4 class="font-semibold text-slate-200 mb-4 flex items-center gap-2">
                            <span class="inline-block w-2 h-2 rounded-full bg-blue-500"></span>
                            In-Game Display
                        </h4>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-slate-300 mb-1">Module Name</label>
                                <input 
                                    type="text" 
                                    id="wizard-module-name" 
                                    value="${wizardData.module_localization?.name || ''}"
                                    onchange="updateWizardField('module_localization', 'name', this.value)"
                                    placeholder="Display name in-game"
                                    class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-slate-300 mb-1">Module Description</label>
                                <textarea 
                                    id="wizard-module-description" 
                                    onchange="updateWizardField('module_localization', 'description', this.value)"
                                    placeholder="In-game description..."
                                    rows="3"
                                    class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                                >${wizardData.module_localization?.description || ''}</textarea>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                        <h4 class="font-semibold text-slate-200 mb-4 flex items-center gap-2">
                            <span class="inline-block w-2 h-2 rounded-full bg-purple-500"></span>
                            Game Age
                        </h4>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Starting Age <span class="text-red-400">*</span>
                                <button onclick="showFieldHelp('age_type')" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <select 
                                id="wizard-age-type" 
                                onchange="updateWizardField('action_group', 'action_group_id', this.value)"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select Age...</option>
                                <option value="AGE_ANTIQUITY" ${wizardData.action_group?.action_group_id === 'AGE_ANTIQUITY' ? 'selected' : ''}>Antiquity</option>
                                <option value="AGE_EXPLORATION" ${wizardData.action_group?.action_group_id === 'AGE_EXPLORATION' ? 'selected' : ''}>Exploration</option>
                                <option value="AGE_MODERN" ${wizardData.action_group?.action_group_id === 'AGE_MODERN' ? 'selected' : ''}>Modern</option>
                                <option value="ALWAYS" ${wizardData.action_group?.action_group_id === 'ALWAYS' ? 'selected' : ''}>Always Available</option>
                            </select>
                            <p class="text-xs text-slate-500 mt-1">When this civilization becomes available</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bg-blue-900/20 border border-blue-700 rounded-lg p-4 mt-6">
                <p class="text-sm text-blue-300">
                    <strong>💡 Tip:</strong> The Mod ID should be unique and use lowercase letters with hyphens (e.g., "babylon-scientific-civ"). 
                    This will be used internally and cannot be changed later.
                </p>
            </div>
        </div>
    `;
}

function renderWizardStep2(container) {
    const selectedTraits = wizardData.civilization?.civilization_traits || [];
    
    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-red-400">🏛️ Step 2: Core Civilization</h3>
                <p class="text-slate-400 text-sm mb-6">Define the essential characteristics of your civilization.</p>
            </div>
            
            <div class="grid grid-cols-1 gap-6">
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">Basic Identity</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Civilization Type <span class="text-red-400">*</span>
                                <button onclick="showFieldHelp('civilization_type')" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-civ-type" 
                                value="${wizardData.civilization?.civilization_type || ''}"
                                onchange="updateWizardField('civilization', 'civilization_type', this.value)"
                                placeholder="CIVILIZATION_BABYLON"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                            <p class="text-xs text-slate-500 mt-1">Unique ID in format: CIVILIZATION_NAME</p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Display Name <span class="text-red-400">*</span>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-civ-name" 
                                value="${wizardData.civilization?.localizations?.[0]?.name || ''}"
                                onchange="updateWizardCivLocalization('name', this.value)"
                                placeholder="Babylon"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div class="md:col-span-2">
                            <label class="block text-sm font-medium text-slate-300 mb-1">Adjective</label>
                            <input 
                                type="text" 
                                id="wizard-civ-adjective" 
                                value="${wizardData.civilization?.localizations?.[0]?.adjective || ''}"
                                onchange="updateWizardCivLocalization('adjective', this.value)"
                                placeholder="Babylonian"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div class="md:col-span-2">
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Description
                            </label>
                            <textarea 
                                id="wizard-civ-description" 
                                onchange="updateWizardCivLocalization('description', this.value)"
                                placeholder="A civilization known for..."
                                rows="3"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >${wizardData.civilization?.localizations?.[0]?.description || ''}</textarea>
                        </div>
                    </div>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">
                        Civilization Traits <span class="text-red-400">*</span>
                        <button onclick="showFieldHelp('trait_type')" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                    </h4>
                    <div id="wizard-traits-container" class="space-y-2">
                        ${selectedTraits.map((trait, idx) => `
                            <div class="flex items-center gap-2" data-trait-idx="${idx}">
                                <select 
                                    id="wizard-trait-${idx}"
                                    onchange="updateWizardTraitAt(${idx}, this.value)"
                                    class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                >
                                    <option value="">Loading...</option>
                                </select>
                                <button 
                                    onclick="removeWizardTrait(${idx})"
                                    class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button 
                        onclick="addWizardTrait()"
                        class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                    >
                        + Add Trait
                    </button>
                    <p class="text-xs text-slate-500 mt-2">Defines your civilization's strengths and bonuses</p>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">City Names</h4>
                    <div id="wizard-cities-container" class="space-y-2 max-h-48 overflow-y-auto">
                        ${(wizardData.civilization?.localizations?.[0]?.city_names || []).map((city, idx) => `
                            <div class="flex items-center gap-2">
                                <span class="text-slate-400 text-sm w-8">${idx + 1}.</span>
                                <input 
                                    type="text" 
                                    value="${city}"
                                    onchange="updateWizardCityAt(${idx}, this.value)"
                                    class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                    placeholder="City name"
                                />
                                <button 
                                    onclick="removeWizardCity(${idx})"
                                    class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                >
                                    ×
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button 
                        onclick="addWizardCity()"
                        class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                    >
                        + Add City
                    </button>
                    <p class="text-xs text-slate-500 mt-2">Names for your civilization's cities</p>
                </div>
                
                <!-- Visual Art Cultures -->
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">Visual Styles</h4>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Building Culture Set</label>
                            <select 
                                id="wizard-building-culture" 
                                onchange="updateWizardBuildingCulture(this.value)"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select building style...</option>
                            </select>
                            <p class="text-xs text-slate-500 mt-1">Visual style for your civilization's buildings</p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Unit Culture Set</label>
                            <select 
                                id="wizard-unit-culture" 
                                onchange="updateWizardUnitCulture(this.value)"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select unit style...</option>
                            </select>
                            <p class="text-xs text-slate-500 mt-1">Visual style for your civilization's units</p>
                        </div>
                    </div>
                </div>
                
                <!-- Starting Location (Collapsible) -->
                <details class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <summary class="font-semibold text-slate-200 cursor-pointer hover:text-slate-100">
                        ⚙️ Starting Location (Optional)
                    </summary>
                    <div class="mt-4 space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">River Bias</label>
                            <input 
                                type="number" 
                                id="wizard-river-bias" 
                                value="${wizardData.civilization?.start_bias_rivers || ''}"
                                onchange="updateWizardField('civilization', 'start_bias_rivers', parseInt(this.value) || 0)"
                                placeholder="5"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                            <p class="text-xs text-slate-500 mt-1">Preference for starting near rivers (0-10)</p>
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="block text-sm font-medium text-slate-300">Terrain Preferences</label>
                                <button 
                                    onclick="addWizardTerrainBias()"
                                    class="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs font-medium"
                                >
                                    + Add Terrain
                                </button>
                            </div>
                            <div id="wizard-terrain-biases" class="space-y-2">
                                ${(wizardData.civilization?.start_bias_terrains || []).map((bias, idx) => `
                                    <div class="flex gap-2 items-center">
                                        <select 
                                            id="wizard-terrain-type-${idx}"
                                            onchange="updateWizardTerrainBiasAt(${idx}, 'terrain_type', this.value)"
                                            class="flex-1 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        >
                                            <option value="">Loading...</option>
                                        </select>
                                        <input 
                                            type="number" 
                                            value="${bias.score || ''}"
                                            onchange="updateWizardTerrainBiasAt(${idx}, 'score', parseInt(this.value) || 0)"
                                            placeholder="Score"
                                            class="w-20 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        />
                                        <button 
                                            onclick="removeWizardTerrainBias(${idx})"
                                            class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                                        >
                                            ×
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                            <p class="text-xs text-slate-500 mt-2">Preferred terrain types and their scores</p>
                        </div>
                    </div>
                </details>
                
                <!-- Age Transitions (Collapsible) -->
                <details class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <summary class="font-semibold text-slate-200 cursor-pointer hover:text-slate-100">
                        🔄 Age Transitions (Optional)
                    </summary>
                    <div class="mt-4">
                        <div class="flex items-center justify-between mb-2">
                            <label class="block text-sm font-medium text-slate-300">Future Civilization Unlocks</label>
                            <button 
                                onclick="addWizardCivUnlock()"
                                class="px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium"
                            >
                                + Add Unlock
                            </button>
                        </div>
                        <div id="wizard-civ-unlocks" class="space-y-3">
                            ${(wizardData.civilization?.civilization_unlocks || []).map((unlock, idx) => `
                                <div class="p-3 bg-slate-800/50 rounded border border-slate-600 space-y-2">
                                    <div class="grid grid-cols-2 gap-2">
                                        <div>
                                            <label class="block text-xs font-medium text-slate-300 mb-1">Age</label>
                                            <select 
                                                id="wizard-unlock-age-${idx}"
                                                onchange="updateWizardCivUnlockAt(${idx}, 'age_type', this.value)"
                                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                            >
                                                <option value="">Loading...</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label class="block text-xs font-medium text-slate-300 mb-1">Target Civilization</label>
                                            <input 
                                                type="text" 
                                                value="${unlock.type || ''}"
                                                onchange="updateWizardCivUnlockAt(${idx}, 'type', this.value)"
                                                placeholder="CIVILIZATION_PERSIA"
                                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                            />
                                        </div>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Display Name</label>
                                        <input 
                                            type="text" 
                                            value="${unlock.name || ''}"
                                            onchange="updateWizardCivUnlockAt(${idx}, 'name', this.value)"
                                            placeholder="LOC_CIVILIZATION_PERSIA_NAME"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                        />
                                    </div>
                                    <button 
                                        onclick="removeWizardCivUnlock(${idx})"
                                        class="w-full px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                                    >
                                        Remove
                                    </button>
                                </div>
                            `).join('')}
                        </div>
                        <p class="text-xs text-slate-500 mt-2">Define what civilizations this evolves into in future ages</p>
                    </div>
                </details>
            </div>
            
            <div class="bg-blue-900/20 border border-blue-700 rounded-lg p-4 mt-6">
                <p class="text-sm text-blue-300">
                    <strong>💡 Tip:</strong> Traits define your civilization's bonuses and unique abilities. 
                    Choose 1-3 traits that reflect your civilization's strengths.
                </p>
            </div>
        </div>
    `;
    
    // Populate trait dropdowns after rendering
    selectedTraits.forEach((trait, idx) => {
        createWizardDropdown(`wizard-trait-${idx}`, 'traits', trait, 'Select trait...');
    });
    
    // Populate visual art culture dropdowns
    createWizardDropdown('wizard-building-culture', 'building-cultures', wizardData.civilization?.vis_art_building_cultures?.[0] || '', 'Select building style...');
    createWizardDropdown('wizard-unit-culture', 'unit-cultures', wizardData.civilization?.vis_art_unit_cultures?.[0] || '', 'Select unit style...');
    
    // Populate terrain bias dropdowns
    (wizardData.civilization?.start_bias_terrains || []).forEach((bias, idx) => {
        createWizardDropdown(`wizard-terrain-type-${idx}`, 'terrain-types', bias.terrain_type || '', 'Select terrain...');
    });
    
    // Populate civ unlock age dropdowns
    (wizardData.civilization?.civilization_unlocks || []).forEach((unlock, idx) => {
        createWizardDropdown(`wizard-unlock-age-${idx}`, 'ages', unlock.age_type || '', 'Select age...');
    });
}

function renderWizardStep3(container) {
    const hasUnits = wizardData.units && wizardData.units.length > 0;
    const hasConstructibles = wizardData.constructibles && wizardData.constructibles.length > 0;
    
    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-orange-400">⚔️ Step 3: Units & Buildings (Optional)</h3>
                <p class="text-slate-400 text-sm mb-6">Add unique units and buildings for your civilization. You can skip this step and add them later in Expert Mode.</p>
            </div>
            
            <!-- Units Section -->
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-orange-500"></span>
                        Unique Units (${wizardData.units?.length || 0})
                    </h4>
                    <button 
                        onclick="wizardShowUnitForm()"
                        class="px-3 py-1 bg-orange-600 hover:bg-orange-700 rounded text-sm font-medium"
                    >
                        + Add Unit
                    </button>
                </div>
                
                <!-- Units List -->
                ${hasUnits ? `
                    <div class="space-y-2 mb-4">
                        ${wizardData.units.map((unit, idx) => `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600 flex items-center justify-between">
                                <div>
                                    <p class="font-medium text-sm">${unit.id || 'Unnamed Unit'}</p>
                                    <p class="text-xs text-slate-400">${unit.unit_type || '—'}</p>
                                </div>
                                <div class="flex gap-2">
                                    <button 
                                        onclick="wizardEditUnit(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="removeWizardUnit(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No units added yet</p>'}
                
                <!-- Unit Form (hidden by default) -->
                <div id="wizard-unit-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                    <div class="space-y-3">
                        <input type="hidden" id="wizard-unit-edit-idx" value="-1" />
                        
                        <h5 class="text-sm font-semibold text-orange-400 border-b border-slate-600 pb-2 mb-3">Basic Information</h5>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Unit ID *</label>
                            <input 
                                type="text" 
                                id="wizard-unit-id" 
                                placeholder="UNIT_CIVILIZATION_NAME"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Unit Type *</label>
                            <input 
                                type="text" 
                                id="wizard-unit-type" 
                                placeholder="UNIT_TYPE_ID"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        
                        <!-- Unit Config -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Unit Configuration</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Core Class</label>
                                    <select 
                                        id="wizard-unit-core-class" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Domain</label>
                                    <select 
                                        id="wizard-unit-domain" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Formation Class</label>
                                    <select 
                                        id="wizard-unit-formation" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Movement Class</label>
                                    <select 
                                        id="wizard-unit-movement" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div class="grid grid-cols-2 gap-2">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Base Moves</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-moves" 
                                            placeholder="2"
                                            min="1"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Sight Range</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-sight" 
                                            placeholder="2"
                                            min="1"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Localization -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Localization</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Display Name</label>
                                    <input 
                                        type="text" 
                                        id="wizard-unit-name" 
                                        placeholder="Unique Unit Name"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                    <textarea 
                                        id="wizard-unit-desc" 
                                        placeholder="Brief description of the unit"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Optional: Icon & Cost (collapsible) -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Icon & Cost (Optional)</summary>
                            <div class="p-3 pt-0 space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Icon Path</label>
                                    <input 
                                        type="text" 
                                        id="wizard-unit-icon" 
                                        placeholder="fs://game/mod_id/unit_icon.png"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost Yield Type</label>
                                    <select 
                                        id="wizard-unit-cost-yield" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost Amount</label>
                                    <input 
                                        type="number" 
                                        id="wizard-unit-cost" 
                                        placeholder="30"
                                        min="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                            </div>
                        </details>
                        
                        <!-- Optional: Combat Stats (collapsible) -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Combat Stats (Optional)</summary>
                            <div class="p-3 pt-2 space-y-2">
                                <div class="grid grid-cols-3 gap-2">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Combat</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-combat" 
                                            placeholder="15"
                                            min="0"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Ranged</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-ranged-combat" 
                                            placeholder="0"
                                            min="0"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Range</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-range" 
                                            placeholder="0"
                                            min="0"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Replaces Unit</label>
                                    <input 
                                        type="text" 
                                        id="wizard-unit-replaces" 
                                        placeholder="UNIT_WARRIOR"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                    <p class="text-xs text-slate-500 mt-1">Base game unit this replaces</p>
                                </div>
                            </div>
                        </details>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="wizardSaveUnit()"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="wizardCancelUnitForm()"
                                class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Buildings Section -->
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-emerald-500"></span>
                        Unique Buildings (${wizardData.constructibles?.length || 0})
                    </h4>
                    <button 
                        onclick="wizardShowConstructibleForm()"
                        class="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 rounded text-sm font-medium"
                    >
                        + Add Building
                    </button>
                </div>
                
                <!-- Buildings List -->
                ${hasConstructibles ? `
                    <div class="space-y-2 mb-4">
                        ${wizardData.constructibles.map((building, idx) => `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600 flex items-center justify-between">
                                <div>
                                    <p class="font-medium text-sm">${building.id || 'Unnamed Building'}</p>
                                    <p class="text-xs text-slate-400">${building.constructible_type || '—'}</p>
                                </div>
                                <div class="flex gap-2">
                                    <button 
                                        onclick="wizardEditConstructible(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="removeWizardConstructible(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No buildings added yet</p>'}
                
                <!-- Building Form (hidden by default) -->
                <div id="wizard-constructible-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                    <div class="space-y-3">
                        <input type="hidden" id="wizard-constructible-edit-idx" value="-1" />
                        
                        <h5 class="text-sm font-semibold text-emerald-400 border-b border-slate-600 pb-2 mb-3">Basic Information</h5>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Building ID *</label>
                            <input 
                                type="text" 
                                id="wizard-constructible-id" 
                                placeholder="BUILDING_CIVILIZATION_NAME"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Constructible Type *</label>
                            <input 
                                type="text" 
                                id="wizard-constructible-type" 
                                placeholder="BUILDING_TYPE_ID"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        
                        <!-- Localization -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Localization</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Display Name</label>
                                    <input 
                                        type="text" 
                                        id="wizard-constructible-name" 
                                        placeholder="Unique Building Name"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                    <textarea 
                                        id="wizard-constructible-desc" 
                                        placeholder="Brief description of the building"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Optional: Icon & Districts (collapsible) -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Icon & Valid Districts (Optional)</summary>
                            <div class="p-3 pt-0 space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Icon Path</label>
                                    <input 
                                        type="text" 
                                        id="wizard-constructible-icon" 
                                        placeholder="fs://game/mod_id/building_icon.png"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Valid Districts (comma-separated)</label>
                                    <input 
                                        type="text" 
                                        id="wizard-constructible-districts" 
                                        placeholder="DISTRICT_CAMPUS, DISTRICT_HOLY_SITE"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                            </div>
                        </details>
                        
                        <!-- Optional: Yield Changes (collapsible) -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Yields & Bonuses (Optional)</summary>
                            <div class="p-3 pt-2 space-y-2">
                                <div class="flex items-center justify-between mb-2">
                                    <label class="block text-xs font-medium text-slate-300">Yield Bonuses</label>
                                    <button 
                                        onclick="addWizardBuildingYield()"
                                        type="button"
                                        class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                    >
                                        + Add Yield
                                    </button>
                                </div>
                                <div id="wizard-building-yields" class="space-y-2">
                                    <!-- Yields will be dynamically added here -->
                                </div>
                                <p class="text-xs text-slate-500 mt-2">Science, culture, production, etc.</p>
                            </div>
                        </details>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="wizardSaveConstructible()"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="wizardCancelConstructibleForm()"
                                class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bg-amber-900/20 border border-amber-700 rounded-lg p-4">
                <p class="text-sm text-amber-300">
                    <strong>⚠️ Tip:</strong> You can add the basic unit/building info here, or skip and configure full details in Expert Mode.
                </p>
            </div>
        </div>
    `;
}


function renderWizardStep4(container) {
    const hasModifiers = wizardData.modifiers && wizardData.modifiers.length > 0;
    const hasTraditions = wizardData.traditions && wizardData.traditions.length > 0;
    
    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-green-400">✨ Step 4: Advanced Features (Optional)</h3>
                <p class="text-slate-400 text-sm mb-6">Add game modifiers and cultural traditions. Progression trees are best configured in Expert Mode.</p>
            </div>
            
            <!-- Modifiers Section -->
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-green-500"></span>
                        Game Modifiers (${wizardData.modifiers?.length || 0})
                    </h4>
                    <button 
                        onclick="wizardShowModifierForm()"
                        class="px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm font-medium"
                    >
                        + Add Modifier
                    </button>
                </div>
                
                <!-- Modifiers List -->
                ${hasModifiers ? `
                    <div class="space-y-2 mb-4">
                        ${wizardData.modifiers.map((mod, idx) => `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600 flex items-center justify-between">
                                <div>
                                    <p class="font-medium text-sm">${mod.id || 'Unnamed Modifier'}</p>
                                    <p class="text-xs text-slate-400">${mod.modifier?.effect || '—'}</p>
                                </div>
                                <div class="flex gap-2">
                                    <button 
                                        onclick="wizardEditModifier(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="removeWizardModifier(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No modifiers added yet</p>'}
                
                <!-- Modifier Form (hidden by default) -->
                <div id="wizard-modifier-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                    <div class="space-y-3">
                        <input type="hidden" id="wizard-modifier-edit-idx" value="-1" />
                        
                        <h5 class="text-sm font-semibold text-green-400 border-b border-slate-600 pb-2 mb-3">Basic Information</h5>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Modifier ID *</label>
                            <input 
                                type="text" 
                                id="wizard-modifier-id" 
                                placeholder="civilization_modifier"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Modifier Type (optional)</label>
                            <input 
                                type="text" 
                                id="wizard-modifier-type" 
                                placeholder="MODIFIER_CUSTOM_TYPE"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        
                        <!-- Modifier Config -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Modifier Configuration</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">
                                        Effect <button onclick="showFieldHelpModal('Effect', FIELD_HELP_TEXT.effect)" class="ml-1 text-blue-400 hover:text-blue-300" type="button">ⓘ</button> *
                                    </label>
                                    <select 
                                        id="wizard-modifier-effect" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">
                                        Collection <button onclick="showFieldHelpModal('Collection', FIELD_HELP_TEXT.collection)" class="ml-1 text-blue-400 hover:text-blue-300" type="button">ⓘ</button> *
                                    </label>
                                    <select 
                                        id="wizard-modifier-collection" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div class="flex gap-4">
                                    <label class="flex items-center gap-2 text-xs text-slate-300">
                                        <input type="checkbox" id="wizard-modifier-permanent" class="rounded" />
                                        Permanent
                                    </label>
                                    <label class="flex items-center gap-2 text-xs text-slate-300">
                                        <input type="checkbox" id="wizard-modifier-runonce" class="rounded" />
                                        Run Once
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Localization -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Localization</h6>
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                <textarea 
                                    id="wizard-modifier-desc" 
                                    placeholder="Describes what this modifier does"
                                    rows="2"
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                ></textarea>
                            </div>
                        </div>
                        
                        <!-- Optional: Arguments (collapsible) -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Arguments (Optional)</summary>
                            <div class="p-3 pt-2">
                                <p class="text-xs text-slate-400 mb-2">Add modifier arguments as name:value pairs (one per line)</p>
                                <textarea 
                                    id="wizard-modifier-args" 
                                    placeholder="YieldType:YIELD_SCIENCE&#10;Amount:100&#10;Tooltip:LOC_BONUS_TOOLTIP"
                                    rows="3"
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400 font-mono"
                                ></textarea>
                            </div>
                        </details>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="wizardSaveModifier()"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="wizardCancelModifierForm()"
                                class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Traditions Section -->
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-pink-500"></span>
                        Cultural Traditions (${wizardData.traditions?.length || 0})
                    </h4>
                    <button 
                        onclick="wizardShowTraditionForm()"
                        class="px-3 py-1 bg-pink-600 hover:bg-pink-700 rounded text-sm font-medium"
                    >
                        + Add Tradition
                    </button>
                </div>
                
                <!-- Traditions List -->
                ${hasTraditions ? `
                    <div class="space-y-2 mb-4">
                        ${wizardData.traditions.map((trad, idx) => `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600 flex items-center justify-between">
                                <div>
                                    <p class="font-medium text-sm">${trad.id || 'Unnamed Tradition'}</p>
                                    <p class="text-xs text-slate-400">${trad.tradition_type || '—'}</p>
                                </div>
                                <div class="flex gap-2">
                                    <button 
                                        onclick="wizardEditTradition(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="removeWizardTradition(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No traditions added yet</p>'}
                
                <!-- Tradition Form (hidden by default) -->
                <div id="wizard-tradition-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                    <div class="space-y-3">
                        <input type="hidden" id="wizard-tradition-edit-idx" value="-1" />
                        
                        <h5 class="text-sm font-semibold text-pink-400 border-b border-slate-600 pb-2 mb-3">Basic Information</h5>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Tradition ID *</label>
                            <input 
                                type="text" 
                                id="wizard-tradition-id" 
                                placeholder="TRADITION_CIVILIZATION_NAME"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Tradition Type *</label>
                            <input 
                                type="text" 
                                id="wizard-tradition-type" 
                                placeholder="TRADITION_TYPE_ID"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        
                        <!-- Localization -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Localization</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Display Name</label>
                                    <input 
                                        type="text" 
                                        id="wizard-tradition-name" 
                                        placeholder="Tradition Name"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                    <textarea 
                                        id="wizard-tradition-desc" 
                                        placeholder="Brief description of the tradition"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="wizardSaveTradition()"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="wizardCancelTraditionForm()"
                                class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
                <p class="text-sm text-blue-300">
                    <strong>💡 Tip:</strong> You can add basic modifiers and traditions here. For advanced configuration and progression trees, use Expert Mode.
                </p>
            </div>
        </div>
    `;
}

function renderWizardStep5(container) {
    const errors = validateWizardData();
    const hasErrors = errors.length > 0;
    
    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-purple-400">🎉 Step 5: Review & Finish</h3>
                <p class="text-slate-400 text-sm mb-6">Review your civilization configuration before saving.</p>
            </div>
            
            ${hasErrors ? `
                <div class="bg-red-900/20 border border-red-700 rounded-lg p-4">
                    <h4 class="font-semibold text-red-400 mb-2">⚠️ Required Fields Missing</h4>
                    <ul class="list-disc list-inside text-sm text-red-300 space-y-1">
                        ${errors.map(err => `<li>${err}</li>`).join('')}
                    </ul>
                    <p class="text-xs text-red-400 mt-3">Please go back and fill in the required fields.</p>
                </div>
            ` : `
                <div class="bg-green-900/20 border border-green-700 rounded-lg p-4">
                    <p class="text-green-300 text-sm">✓ All required fields completed!</p>
                </div>
            `}
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-3 text-sm">📋 Mod Information</h4>
                    <dl class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <dt class="text-slate-400">ID:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.metadata?.id || '—'}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Name:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.metadata?.name || '—'}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Version:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.metadata?.version || '—'}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Age:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.action_group?.action_group_id || '—'}</dd>
                        </div>
                    </dl>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-3 text-sm">🏛️ Civilization</h4>
                    <dl class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Type:</dt>
                            <dd class="text-slate-200 font-medium text-xs">${wizardData.civilization?.civilization_type || '—'}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Name:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.civilization?.localizations?.[0]?.name || '—'}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Traits:</dt>
                            <dd class="text-slate-200 font-medium text-xs">${wizardData.civilization?.civilization_traits?.length || 0}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Cities:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.civilization?.localizations?.[0]?.city_names?.length || 0}</dd>
                        </div>
                    </dl>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-3 text-sm">⚔️ Content</h4>
                    <dl class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Units:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.units?.length || 0}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Buildings:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.constructibles?.length || 0}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Modifiers:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.modifiers?.length || 0}</dd>
                        </div>
                        <div class="flex justify-between">
                            <dt class="text-slate-400">Traditions:</dt>
                            <dd class="text-slate-200 font-medium">${wizardData.traditions?.length || 0}</dd>
                        </div>
                    </dl>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-3 text-sm">📂 Next Steps</h4>
                    <p class="text-xs text-slate-400 mb-3">
                        Click "Finish & Save" to switch to Expert Mode where you can:
                    </p>
                    <ul class="text-xs text-slate-300 space-y-1 list-disc list-inside">
                        <li>Add advanced modifiers</li>
                        <li>Configure unique units and buildings</li>
                        <li>Set up progression trees</li>
                        <li>Fine-tune all properties</li>
                        <li>Save your YAML file</li>
                    </ul>
                </div>
            </div>
            
            ${!hasErrors ? `
                <div class="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
                    <p class="text-sm text-blue-300">
                        <strong>🎯 Ready to go!</strong> Click "Finish & Save" to complete the wizard and switch to Expert Mode.
                    </p>
                </div>
            ` : ''}
        </div>
    `;
}

// Helper functions for wizard step 2 and 3
function updateWizardField(section, field, value) {
    if (!wizardData[section]) wizardData[section] = {};
    wizardData[section][field] = value;
    markDirty();
}

function updateWizardCivLocalization(field, value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.localizations) wizardData.civilization.localizations = [{}];
    wizardData.civilization.localizations[0][field] = value;
    markDirty();
}

function addWizardTrait() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.civilization_traits) wizardData.civilization.civilization_traits = [];
    wizardData.civilization.civilization_traits.push('');
    renderWizardStep2(document.getElementById('wizard-step-content'));
    markDirty();
}

function updateWizardTraitAt(idx, value) {
    if (wizardData.civilization?.civilization_traits) {
        wizardData.civilization.civilization_traits[idx] = value;
        markDirty();
    }
}

function removeWizardTrait(idx) {
    if (wizardData.civilization?.civilization_traits) {
        wizardData.civilization.civilization_traits.splice(idx, 1);
        renderWizardStep2(document.getElementById('wizard-step-content'));
        markDirty();
    }
}

function addWizardCity() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.localizations) wizardData.civilization.localizations = [{}];
    if (!wizardData.civilization.localizations[0].city_names) wizardData.civilization.localizations[0].city_names = [];
    wizardData.civilization.localizations[0].city_names.push('');
    renderWizardStep2(document.getElementById('wizard-step-content'));
    markDirty();
}

function updateWizardCityAt(idx, value) {
    if (wizardData.civilization?.localizations?.[0]?.city_names) {
        wizardData.civilization.localizations[0].city_names[idx] = value;
        markDirty();
    }
}

function removeWizardCity(idx) {
    if (wizardData.civilization?.localizations?.[0]?.city_names) {
        wizardData.civilization.localizations[0].city_names.splice(idx, 1);
        renderWizardStep2(document.getElementById('wizard-step-content'));
        markDirty();
    }
}

// Visual Art Cultures
function updateWizardBuildingCulture(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    wizardData.civilization.vis_art_building_cultures = value ? [value] : [];
    markDirty();
}

function updateWizardUnitCulture(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    wizardData.civilization.vis_art_unit_cultures = value ? [value] : [];
    markDirty();
}

// Auto-generate default progression tree
function generateDefaultProgressionTree() {
    // Only generate if no progression trees exist
    if (currentData.progression_trees && currentData.progression_trees.length > 0) {
        return; // User already has trees, don't override
    }
    
    const civType = currentData.civilization?.civilization_type || 'CIVILIZATION_CUSTOM';
    const civName = currentData.civilization?.localizations?.[0]?.name || 'Custom';
    const ageType = currentData.action_group || 'AGE_ANTIQUITY';
    const modId = currentData.metadata?.id || 'custom';
    
    // Create base tree ID
    const treeId = `progression_tree_${modId}`;
    const treeType = `TREE_CIVICS_${civType.replace('CIVILIZATION_', '')}`;
    const node1Type = `NODE_CIVICS_${civType.replace('CIVILIZATION_', '')}_1`;
    const node2Type = `NODE_CIVICS_${civType.replace('CIVILIZATION_', '')}_2`;
    
    // Create 2 progression tree nodes
    if (!currentData.progression_tree_nodes) {
        currentData.progression_tree_nodes = [];
    }
    
    currentData.progression_tree_nodes.push({
        id: `${modId}_node1`,
        progression_tree_node_type: node1Type,
        progression_tree_node: {
            progression_tree_node_type: node1Type
        },
        localizations: [{
            name: `${civName} Foundations`
        }],
        bindings: []
    });
    
    currentData.progression_tree_nodes.push({
        id: `${modId}_node2`,
        progression_tree_node_type: node2Type,
        progression_tree_node: {
            progression_tree_node_type: node2Type
        },
        localizations: [{
            name: `${civName} Advancement`
        }],
        bindings: []
    });
    
    // Create the progression tree
    if (!currentData.progression_trees) {
        currentData.progression_trees = [];
    }
    
    currentData.progression_trees.push({
        id: treeId,
        progression_tree_type: treeType,
        progression_tree: {
            progression_tree_type: treeType,
            age_type: ageType
        },
        progression_tree_prereqs: [{
            node: node2Type,
            prereq_node: node1Type
        }],
        localizations: [{
            name: `${civName} Civic Tree`
        }],
        bindings: [
            `${modId}_node1`,
            `${modId}_node2`
        ]
    });
    
    // Update civilization to reference the unique tree
    if (currentData.civilization) {
        if (!currentData.civilization.civilization) {
            currentData.civilization.civilization = {};
        }
        currentData.civilization.civilization.unique_culture_progression_tree = treeType;
        
        // Add tree to bindings
        if (!currentData.civilization.bindings) {
            currentData.civilization.bindings = [];
        }
        if (!currentData.civilization.bindings.includes(treeId)) {
            currentData.civilization.bindings.push(treeId);
        }
    }
    
    markDirty();
}

// Terrain Biases
function addWizardTerrainBias() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.start_bias_terrains) wizardData.civilization.start_bias_terrains = [];
    wizardData.civilization.start_bias_terrains.push({ terrain_type: '', score: 0 });
    renderWizardStep2(document.getElementById('wizard-step-content'));
    markDirty();
}

function updateWizardTerrainBiasAt(idx, field, value) {
    if (wizardData.civilization?.start_bias_terrains?.[idx]) {
        wizardData.civilization.start_bias_terrains[idx][field] = value;
        markDirty();
    }
}

function removeWizardTerrainBias(idx) {
    if (wizardData.civilization?.start_bias_terrains) {
        wizardData.civilization.start_bias_terrains.splice(idx, 1);
        renderWizardStep2(document.getElementById('wizard-step-content'));
        markDirty();
    }
}

// Civilization Unlocks
function addWizardCivUnlock() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.civilization_unlocks) wizardData.civilization.civilization_unlocks = [];
    wizardData.civilization.civilization_unlocks.push({
        age_type: '',
        type: '',
        kind: 'KIND_CIVILIZATION',
        name: '',
        description: '',
        icon: ''
    });
    renderWizardStep2(document.getElementById('wizard-step-content'));
    markDirty();
}

function updateWizardCivUnlockAt(idx, field, value) {
    if (wizardData.civilization?.civilization_unlocks?.[idx]) {
        wizardData.civilization.civilization_unlocks[idx][field] = value;
        markDirty();
    }
}

function removeWizardCivUnlock(idx) {
    if (wizardData.civilization?.civilization_unlocks) {
        wizardData.civilization.civilization_unlocks.splice(idx, 1);
        renderWizardStep2(document.getElementById('wizard-step-content'));
        markDirty();
    }
}

// ============================================================================
// Wizard Helper: Reference Data Dropdown
// ============================================================================

// Convert ID to human-friendly label
function idToLabel(id) {
    if (!id) return '';
    
    // Remove common prefixes
    let label = id
        .replace(/^YIELD_/, '')
        .replace(/^EFFECT_/, '')
        .replace(/^COLLECTION_/, '')
        .replace(/^CORE_CLASS_/, '')
        .replace(/^DOMAIN_/, '')
        .replace(/^FORMATION_CLASS_/, '')
        .replace(/^UNIT_MOVEMENT_CLASS_/, '')
        .replace(/^DISTRICT_/, '')
        .replace(/^TRAIT_/, '')
        .replace(/^AGE_/, '');
    
    // Convert snake_case to Title Case
    return label
        .split('_')
        .map(word => word.charAt(0) + word.slice(1).toLowerCase())
        .join(' ');
}

// Create a wizard dropdown with reference data
async function createWizardDropdown(elementId, dataType, currentValue = '', placeholder = 'Select...') {
    const selectElement = document.getElementById(elementId);
    if (!selectElement) return;
    
    // Hardcoded fallback for traits (not in JSON yet)
    if (dataType === 'traits') {
        const traitValues = [
            { id: 'TRAIT_ECONOMIC', label: 'Economic' },
            { id: 'TRAIT_CULTURAL', label: 'Cultural' },
            { id: 'TRAIT_MILITARY', label: 'Military' },
            { id: 'TRAIT_DIPLOMATIC', label: 'Diplomatic' },
            { id: 'TRAIT_SCIENTIFIC', label: 'Scientific' },
            { id: 'TRAIT_RELIGIOUS', label: 'Religious' },
            { id: 'TRAIT_ANTIQUITY_CIV', label: 'Antiquity Civilization' },
            { id: 'TRAIT_EXPLORATION_CIV', label: 'Exploration Civilization' },
            { id: 'TRAIT_MODERN_CIV', label: 'Modern Civilization' }
        ];
        
        selectElement.innerHTML = '';
        const placeholderOption = document.createElement('option');
        placeholderOption.value = '';
        placeholderOption.textContent = placeholder;
        selectElement.appendChild(placeholderOption);
        
        traitValues.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = `${item.label} (${item.id})`;
            if (item.id === currentValue) {
                option.selected = true;
            }
            selectElement.appendChild(option);
        });
        
        return;
    }
    
    // Fetch data from API
    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (!response.ok) {
            console.error(`Failed to fetch ${dataType}`);
            return;
        }
        
        const data = await response.json();
        const values = data.values || [];
        
        // Clear existing options
        selectElement.innerHTML = '';
        
        // Add placeholder option
        const placeholderOption = document.createElement('option');
        placeholderOption.value = '';
        placeholderOption.textContent = placeholder;
        selectElement.appendChild(placeholderOption);
        
        // Add data options with friendly labels
        values.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            
            // Use name field directly for building-cultures and unit-cultures
            if (dataType === 'building-cultures' || dataType === 'unit-cultures') {
                const displayName = item.name || item.id;
                option.textContent = `${displayName} (${item.id})`;
            } else {
                const label = idToLabel(item.id);
                option.textContent = `${label} (${item.id})`;
            }
            
            if (item.id === currentValue) {
                option.selected = true;
            }
            selectElement.appendChild(option);
        });
        
    } catch (error) {
        console.error(`Error loading ${dataType}:`, error);
    }
}

// ============================================================================
// Wizard Step 3: Units & Buildings - Form Handlers
// ============================================================================

function wizardShowUnitForm() {
    const form = document.getElementById('wizard-unit-form');
    const idxInput = document.getElementById('wizard-unit-edit-idx');
    
    // Clear form fields
    document.getElementById('wizard-unit-id').value = '';
    document.getElementById('wizard-unit-type').value = '';
    document.getElementById('wizard-unit-moves').value = '';
    document.getElementById('wizard-unit-sight').value = '';
    document.getElementById('wizard-unit-name').value = '';
    document.getElementById('wizard-unit-desc').value = '';
    document.getElementById('wizard-unit-icon').value = '';
    document.getElementById('wizard-unit-cost').value = '';
    idxInput.value = '-1';
    
    // Populate dropdowns with reference data
    createWizardDropdown('wizard-unit-core-class', 'core-classes', '', 'Select core class...');
    createWizardDropdown('wizard-unit-domain', 'domains', '', 'Select domain...');
    createWizardDropdown('wizard-unit-formation', 'formation-classes', '', 'Select formation...');
    createWizardDropdown('wizard-unit-movement', 'unit-movement-classes', '', 'Select movement type...');
    createWizardDropdown('wizard-unit-cost-yield', 'yield-types', '', 'Select yield type...');
    
    // Toggle visibility
    form.classList.remove('hidden');
    document.getElementById('wizard-unit-id').focus();
}

function wizardCancelUnitForm() {
    const form = document.getElementById('wizard-unit-form');
    form.classList.add('hidden');
    document.getElementById('wizard-unit-id').value = '';
    document.getElementById('wizard-unit-type').value = '';
    document.getElementById('wizard-unit-core-class').value = '';
    document.getElementById('wizard-unit-domain').value = '';
    document.getElementById('wizard-unit-formation').value = '';
    document.getElementById('wizard-unit-movement').value = '';
    document.getElementById('wizard-unit-moves').value = '';
    document.getElementById('wizard-unit-sight').value = '';
    document.getElementById('wizard-unit-name').value = '';
    document.getElementById('wizard-unit-desc').value = '';
    document.getElementById('wizard-unit-icon').value = '';
    document.getElementById('wizard-unit-cost-yield').value = '';
    document.getElementById('wizard-unit-cost').value = '';
    document.getElementById('wizard-unit-combat').value = '';
    document.getElementById('wizard-unit-ranged-combat').value = '';
    document.getElementById('wizard-unit-range').value = '';
    document.getElementById('wizard-unit-replaces').value = '';
    document.getElementById('wizard-unit-edit-idx').value = '-1';
}

function wizardSaveUnit() {
    const id = document.getElementById('wizard-unit-id').value.trim();
    const type = document.getElementById('wizard-unit-type').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-unit-edit-idx').value);
    
    if (!id) {
        showToast('Unit ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Unit Type is required', 'error');
        return;
    }
    
    // Initialize array if needed
    if (!wizardData.units) {
        wizardData.units = [];
    }
    
    // Gather all fields
    const coreClass = document.getElementById('wizard-unit-core-class').value.trim();
    const domain = document.getElementById('wizard-unit-domain').value.trim();
    const formation = document.getElementById('wizard-unit-formation').value.trim();
    const movement = document.getElementById('wizard-unit-movement').value.trim();
    const moves = document.getElementById('wizard-unit-moves').value;
    const sight = document.getElementById('wizard-unit-sight').value;
    const displayName = document.getElementById('wizard-unit-name').value.trim();
    const description = document.getElementById('wizard-unit-desc').value.trim();
    const icon = document.getElementById('wizard-unit-icon').value.trim();
    const costYield = document.getElementById('wizard-unit-cost-yield').value.trim();
    const costAmount = document.getElementById('wizard-unit-cost').value;
    const combat = document.getElementById('wizard-unit-combat').value;
    const rangedCombat = document.getElementById('wizard-unit-ranged-combat').value;
    const range = document.getElementById('wizard-unit-range').value;
    const replacesUnit = document.getElementById('wizard-unit-replaces').value.trim();
    
    // Create unit object
    const unit = {
        id: id,
        unit_type: type,
        unit: {}
    };
    
    // Add unit config fields if provided
    if (coreClass) unit.unit.core_class = coreClass;
    if (domain) unit.unit.domain = domain;
    if (formation) unit.unit.formation_class = formation;
    if (movement) unit.unit.unit_movement_class = movement;
    if (moves) unit.unit.base_moves = parseInt(moves);
    if (sight) unit.unit.base_sight_range = parseInt(sight);
    
    // Add combat stats if provided
    if (combat || rangedCombat || range) {
        unit.unit_stat = {};
        if (combat) unit.unit_stat.combat = parseInt(combat);
        if (rangedCombat) unit.unit_stat.ranged_combat = parseInt(rangedCombat);
        if (range) unit.unit_stat.range = parseInt(range);
    }
    
    // Add unit replacement if provided
    if (replacesUnit) {
        unit.unit_replace = {
            replaces_unit_type: replacesUnit
        };
    }
    
    // Add localization if provided
    if (displayName || description) {
        unit.localizations = [{}];
        if (displayName) unit.localizations[0].name = displayName;
        if (description) unit.localizations[0].description = description;
    }
    
    // Add icon if provided
    if (icon) {
        unit.icon = { path: icon };
    }
    
    // Add cost if provided
    if (costYield && costAmount) {
        unit.unit_cost = {
            yield_type: costYield,
            cost: parseInt(costAmount)
        };
    }
    
    if (editIdx >= 0) {
        // Update existing
        wizardData.units[editIdx] = unit;
        showToast('Unit updated', 'success');
    } else {
        // Add new
        wizardData.units.push(unit);
        showToast('Unit added', 'success');
    }
    
    wizardCancelUnitForm();
    renderWizardStep3(document.getElementById('wizard-step-content'));
    markDirty();
}

function wizardEditUnit(idx) {
    const unit = wizardData.units[idx];
    document.getElementById('wizard-unit-id').value = unit.id || '';
    document.getElementById('wizard-unit-type').value = unit.unit_type || '';
    document.getElementById('wizard-unit-moves').value = unit.unit?.base_moves || '';
    document.getElementById('wizard-unit-sight').value = unit.unit?.base_sight_range || '';
    document.getElementById('wizard-unit-name').value = unit.localizations?.[0]?.name || '';
    document.getElementById('wizard-unit-desc').value = unit.localizations?.[0]?.description || '';
    document.getElementById('wizard-unit-icon').value = unit.icon?.path || '';
    document.getElementById('wizard-unit-cost').value = unit.unit_cost?.cost || '';
    document.getElementById('wizard-unit-combat').value = unit.unit_stat?.combat || '';
    document.getElementById('wizard-unit-ranged-combat').value = unit.unit_stat?.ranged_combat || '';
    document.getElementById('wizard-unit-range').value = unit.unit_stat?.range || '';
    document.getElementById('wizard-unit-replaces').value = unit.unit_replace?.replaces_unit_type || '';
    document.getElementById('wizard-unit-edit-idx').value = idx;
    
    // Populate dropdowns with current values
    createWizardDropdown('wizard-unit-core-class', 'core-classes', unit.unit?.core_class || '', 'Select core class...');
    createWizardDropdown('wizard-unit-domain', 'domains', unit.unit?.domain || '', 'Select domain...');
    createWizardDropdown('wizard-unit-formation', 'formation-classes', unit.unit?.formation_class || '', 'Select formation...');
    createWizardDropdown('wizard-unit-movement', 'unit-movement-classes', unit.unit?.unit_movement_class || '', 'Select movement type...');
    createWizardDropdown('wizard-unit-cost-yield', 'yield-types', unit.unit_cost?.yield_type || '', 'Select yield type...');
    
    document.getElementById('wizard-unit-form').classList.remove('hidden');
}

function removeWizardUnit(idx) {
    if (wizardData.units) {
        wizardData.units.splice(idx, 1);
        renderWizardStep3(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Unit removed', 'info');
    }
}

// Constructible (Building) handlers
let wizardBuildingYields = []; // Temporary storage for yields in form

function wizardShowConstructibleForm() {
    const form = document.getElementById('wizard-constructible-form');
    const idxInput = document.getElementById('wizard-constructible-edit-idx');
    
    // Clear form fields
    document.getElementById('wizard-constructible-id').value = '';
    document.getElementById('wizard-constructible-type').value = '';
    document.getElementById('wizard-constructible-name').value = '';
    document.getElementById('wizard-constructible-desc').value = '';
    document.getElementById('wizard-constructible-icon').value = '';
    document.getElementById('wizard-constructible-districts').value = '';
    wizardBuildingYields = [];
    renderWizardBuildingYields();
    idxInput.value = '-1';
    
    // Toggle visibility
    form.classList.remove('hidden');
    document.getElementById('wizard-constructible-id').focus();
}

function wizardCancelConstructibleForm() {
    const form = document.getElementById('wizard-constructible-form');
    form.classList.add('hidden');
    document.getElementById('wizard-constructible-id').value = '';
    document.getElementById('wizard-constructible-type').value = '';
    document.getElementById('wizard-constructible-name').value = '';
    document.getElementById('wizard-constructible-desc').value = '';
    document.getElementById('wizard-constructible-icon').value = '';
    document.getElementById('wizard-constructible-districts').value = '';
    wizardBuildingYields = [];
    document.getElementById('wizard-constructible-edit-idx').value = '-1';
}

function wizardSaveConstructible() {
    const id = document.getElementById('wizard-constructible-id').value.trim();
    const type = document.getElementById('wizard-constructible-type').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-constructible-edit-idx').value);
    
    if (!id) {
        showToast('Building ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Building Type is required', 'error');
        return;
    }
    
    // Initialize array if needed
    if (!wizardData.constructibles) {
        wizardData.constructibles = [];
    }
    
    // Gather all fields
    const displayName = document.getElementById('wizard-constructible-name').value.trim();
    const description = document.getElementById('wizard-constructible-desc').value.trim();
    const icon = document.getElementById('wizard-constructible-icon').value.trim();
    const districts = document.getElementById('wizard-constructible-districts').value.trim();
    
    // Create constructible object
    const constructible = {
        id: id,
        constructible_type: type
    };
    
    // Add localization if provided
    if (displayName || description) {
        constructible.localizations = [{}];
        if (displayName) constructible.localizations[0].name = displayName;
        if (description) constructible.localizations[0].description = description;
    }
    
    // Add icon if provided
    if (icon) {
        constructible.icon = { path: icon };
    }
    
    // Add valid districts if provided
    if (districts) {
        constructible.constructible_valid_districts = districts
            .split(',')
            .map(d => d.trim())
            .filter(d => d.length > 0);
    }
    
    // Add yield changes if provided
    if (wizardBuildingYields.length > 0) {
        constructible.yield_changes = wizardBuildingYields.filter(y => y.yield_type && y.yield_change);
    }
    
    if (editIdx >= 0) {
        // Update existing
        wizardData.constructibles[editIdx] = constructible;
        showToast('Building updated', 'success');
    } else {
        // Add new
        wizardData.constructibles.push(constructible);
        showToast('Building added', 'success');
    }
    
    wizardCancelConstructibleForm();
    renderWizardStep3(document.getElementById('wizard-step-content'));
    markDirty();
}

function wizardEditConstructible(idx) {
    const building = wizardData.constructibles[idx];
    document.getElementById('wizard-constructible-id').value = building.id || '';
    document.getElementById('wizard-constructible-type').value = building.constructible_type || '';
    document.getElementById('wizard-constructible-name').value = building.localizations?.[0]?.name || '';
    document.getElementById('wizard-constructible-desc').value = building.localizations?.[0]?.description || '';
    document.getElementById('wizard-constructible-icon').value = building.icon?.path || '';
    document.getElementById('wizard-constructible-districts').value = (building.constructible_valid_districts || []).join(', ');
    wizardBuildingYields = building.yield_changes || [];
    renderWizardBuildingYields();
    document.getElementById('wizard-constructible-edit-idx').value = idx;
    document.getElementById('wizard-constructible-form').classList.remove('hidden');
}

function removeWizardConstructible(idx) {
    if (wizardData.constructibles) {
        wizardData.constructibles.splice(idx, 1);
        renderWizardStep3(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Building removed', 'info');
    }
}

// Building Yield Helpers
function addWizardBuildingYield() {
    wizardBuildingYields.push({ yield_type: '', yield_change: 0 });
    renderWizardBuildingYields();
}

function updateWizardBuildingYield(idx, field, value) {
    if (wizardBuildingYields[idx]) {
        wizardBuildingYields[idx][field] = field === 'yield_change' ? parseInt(value) || 0 : value;
    }
}

function removeWizardBuildingYield(idx) {
    wizardBuildingYields.splice(idx, 1);
    renderWizardBuildingYields();
}

function renderWizardBuildingYields() {
    const container = document.getElementById('wizard-building-yields');
    if (!container) return;
    
    container.innerHTML = wizardBuildingYields.map((yieldItem, idx) => `
        <div class="flex gap-2 items-center">
            <select 
                id="wizard-yield-type-${idx}"
                onchange="updateWizardBuildingYield(${idx}, 'yield_type', this.value)"
                class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            >
                <option value="">Loading...</option>
            </select>
            <input 
                type="number" 
                value="${yieldItem.yield_change || ''}"
                onchange="updateWizardBuildingYield(${idx}, 'yield_change', this.value)"
                placeholder="Amount"
                class="w-24 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            />
            <button 
                onclick="removeWizardBuildingYield(${idx})"
                type="button"
                class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
            >
                ×
            </button>
        </div>
    `).join('');
    
    // Populate yield type dropdowns
    wizardBuildingYields.forEach((yieldItem, idx) => {
        createWizardDropdown(`wizard-yield-type-${idx}`, 'yield-types', yieldItem.yield_type || '', 'Select yield...');
    });
}

// ============================================================================
// Wizard Step 4: Modifiers & Traditions - Form Handlers
// ============================================================================

function wizardShowModifierForm() {
    const form = document.getElementById('wizard-modifier-form');
    const idxInput = document.getElementById('wizard-modifier-edit-idx');
    
    // Clear form fields
    document.getElementById('wizard-modifier-id').value = '';
    document.getElementById('wizard-modifier-type').value = '';
    document.getElementById('wizard-modifier-permanent').checked = false;
    document.getElementById('wizard-modifier-runonce').checked = false;
    document.getElementById('wizard-modifier-desc').value = '';
    document.getElementById('wizard-modifier-args').value = '';
    idxInput.value = '-1';
    
    // Populate dropdowns with reference data
    createWizardDropdown('wizard-modifier-effect', 'effects', '', 'Select effect...');
    createWizardDropdown('wizard-modifier-collection', 'collection-types', '', 'Select collection...');
    
    // Toggle visibility
    form.classList.remove('hidden');
    document.getElementById('wizard-modifier-id').focus();
}

function wizardCancelModifierForm() {
    const form = document.getElementById('wizard-modifier-form');
    form.classList.add('hidden');
    document.getElementById('wizard-modifier-id').value = '';
    document.getElementById('wizard-modifier-type').value = '';
    document.getElementById('wizard-modifier-effect').value = '';
    document.getElementById('wizard-modifier-collection').value = '';
    document.getElementById('wizard-modifier-permanent').checked = false;
    document.getElementById('wizard-modifier-runonce').checked = false;
    document.getElementById('wizard-modifier-desc').value = '';
    document.getElementById('wizard-modifier-args').value = '';
    document.getElementById('wizard-modifier-edit-idx').value = '-1';
}

function wizardSaveModifier() {
    const id = document.getElementById('wizard-modifier-id').value.trim();
    const modifierType = document.getElementById('wizard-modifier-type').value.trim();
    const effect = document.getElementById('wizard-modifier-effect').value.trim();
    const collection = document.getElementById('wizard-modifier-collection').value.trim();
    const permanent = document.getElementById('wizard-modifier-permanent').checked;
    const runOnce = document.getElementById('wizard-modifier-runonce').checked;
    const description = document.getElementById('wizard-modifier-desc').value.trim();
    const argsText = document.getElementById('wizard-modifier-args').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-modifier-edit-idx').value);
    
    if (!id) {
        showToast('Modifier ID is required', 'error');
        return;
    }
    if (!effect) {
        showToast('Effect is required', 'error');
        return;
    }
    if (!collection) {
        showToast('Collection is required', 'error');
        return;
    }
    
    // Initialize array if needed
    if (!wizardData.modifiers) {
        wizardData.modifiers = [];
    }
    
    // Create modifier object with nested structure
    const modifier = {
        id: id,
        modifier: {
            effect: effect,
            collection: collection
        }
    };
    
    // Add optional fields
    if (modifierType) modifier.modifier_type = modifierType;
    if (permanent) modifier.modifier.permanent = true;
    if (runOnce) modifier.modifier.run_once = true;
    
    // Parse arguments if provided
    if (argsText) {
        const args = [];
        const lines = argsText.split('\n');
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed && trimmed.includes(':')) {
                const [name, value] = trimmed.split(':', 2);
                args.push({
                    name: name.trim(),
                    value: value.trim()
                });
            }
        }
        if (args.length > 0) {
            modifier.modifier.arguments = args;
        }
    }
    
    // Add localization if provided
    if (description) {
        modifier.localizations = [{ description: description }];
    }
    
    if (editIdx >= 0) {
        // Update existing
        wizardData.modifiers[editIdx] = modifier;
        showToast('Modifier updated', 'success');
    } else {
        // Add new
        wizardData.modifiers.push(modifier);
        showToast('Modifier added', 'success');
    }
    
    wizardCancelModifierForm();
    renderWizardStep4(document.getElementById('wizard-step-content'));
    markDirty();
}

function wizardEditModifier(idx) {
    const modifier = wizardData.modifiers[idx];
    document.getElementById('wizard-modifier-id').value = modifier.id || '';
    document.getElementById('wizard-modifier-type').value = modifier.modifier_type || '';
    document.getElementById('wizard-modifier-permanent').checked = modifier.modifier?.permanent || false;
    document.getElementById('wizard-modifier-runonce').checked = modifier.modifier?.run_once || false;
    document.getElementById('wizard-modifier-desc').value = modifier.localizations?.[0]?.description || '';
    
    // Convert arguments to text format
    if (modifier.modifier?.arguments) {
        const argsText = modifier.modifier.arguments
            .map(arg => `${arg.name}:${arg.value}`)
            .join('\n');
        document.getElementById('wizard-modifier-args').value = argsText;
    } else {
        document.getElementById('wizard-modifier-args').value = '';
    }
    
    // Populate dropdowns with current values
    createWizardDropdown('wizard-modifier-effect', 'effects', modifier.modifier?.effect || '', 'Select effect...');
    createWizardDropdown('wizard-modifier-collection', 'collection-types', modifier.modifier?.collection || '', 'Select collection...');
    
    document.getElementById('wizard-modifier-edit-idx').value = idx;
    document.getElementById('wizard-modifier-form').classList.remove('hidden');
}

function removeWizardModifier(idx) {
    if (wizardData.modifiers) {
        wizardData.modifiers.splice(idx, 1);
        renderWizardStep4(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Modifier removed', 'info');
    }
}

// Tradition handlers
function wizardShowTraditionForm() {
    const form = document.getElementById('wizard-tradition-form');
    const idxInput = document.getElementById('wizard-tradition-edit-idx');
    
    // Clear form fields
    document.getElementById('wizard-tradition-id').value = '';
    document.getElementById('wizard-tradition-type').value = '';
    document.getElementById('wizard-tradition-name').value = '';
    document.getElementById('wizard-tradition-desc').value = '';
    idxInput.value = '-1';
    
    // Toggle visibility
    form.classList.remove('hidden');
    document.getElementById('wizard-tradition-id').focus();
}

function wizardCancelTraditionForm() {
    const form = document.getElementById('wizard-tradition-form');
    form.classList.add('hidden');
    document.getElementById('wizard-tradition-id').value = '';
    document.getElementById('wizard-tradition-type').value = '';
    document.getElementById('wizard-tradition-name').value = '';
    document.getElementById('wizard-tradition-desc').value = '';
    document.getElementById('wizard-tradition-edit-idx').value = '-1';
}

function wizardSaveTradition() {
    const id = document.getElementById('wizard-tradition-id').value.trim();
    const type = document.getElementById('wizard-tradition-type').value.trim();
    const displayName = document.getElementById('wizard-tradition-name').value.trim();
    const description = document.getElementById('wizard-tradition-desc').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-tradition-edit-idx').value);
    
    if (!id) {
        showToast('Tradition ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Tradition Type is required', 'error');
        return;
    }
    
    // Initialize array if needed
    if (!wizardData.traditions) {
        wizardData.traditions = [];
    }
    
    // Create tradition object
    const tradition = {
        id: id,
        tradition_type: type,
        tradition: {}
    };
    
    // Add localization if provided
    if (displayName || description) {
        tradition.localizations = [{}];
        if (displayName) tradition.localizations[0].name = displayName;
        if (description) tradition.localizations[0].description = description;
    }
    
    if (editIdx >= 0) {
        // Update existing
        wizardData.traditions[editIdx] = tradition;
        showToast('Tradition updated', 'success');
    } else {
        // Add new
        wizardData.traditions.push(tradition);
        showToast('Tradition added', 'success');
    }
    
    wizardCancelTraditionForm();
    renderWizardStep4(document.getElementById('wizard-step-content'));
    markDirty();
}

function wizardEditTradition(idx) {
    const tradition = wizardData.traditions[idx];
    document.getElementById('wizard-tradition-id').value = tradition.id || '';
    document.getElementById('wizard-tradition-type').value = tradition.tradition_type || '';
    document.getElementById('wizard-tradition-name').value = tradition.localizations?.[0]?.name || '';
    document.getElementById('wizard-tradition-desc').value = tradition.localizations?.[0]?.description || '';
    document.getElementById('wizard-tradition-edit-idx').value = idx;
    document.getElementById('wizard-tradition-form').classList.remove('hidden');
}

function removeWizardTradition(idx) {
    if (wizardData.traditions) {
        wizardData.traditions.splice(idx, 1);
        renderWizardStep4(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Tradition removed', 'info');
    }
}

function validateWizardData() {
    const errors = [];
    
    if (!wizardData.metadata?.id) errors.push('Mod ID is required');
    if (!wizardData.metadata?.name) errors.push('Mod Name is required');
    if (!wizardData.action_group?.action_group_id) errors.push('Starting Age is required');
    if (!wizardData.civilization?.civilization_type) errors.push('Civilization Type is required');
    if (!wizardData.civilization?.localizations?.[0]?.name) errors.push('Civilization Display Name is required');
    if (!wizardData.civilization?.civilization_traits || wizardData.civilization.civilization_traits.length === 0) {
        errors.push('At least one Civilization Trait is required');
    }
    
    return errors;
}

function showFieldHelp(fieldName) {
    const helpText = FIELD_HELP_TEXT[fieldName] || 'No help available for this field.';
    alert(helpText); // Replace with modal in production
}

// ============================================================================
// Editor Rendering
// ============================================================================

function createNew() {
    // When creating new in guided mode, initialize wizard
    if (currentMode === 'guided') {
        initializeWizard();
        showToast('Starting guided civilization creator...', 'success');
    } else {
        // Original createNew logic for expert mode
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
        renderAllSections();
        updateDirtyIndicator();
        showToast("Created new skeleton YAML. Enter file path and save.", "success");
    }
}

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
    
    // Basic Info
    const basicSection = document.createElement("div");
    basicSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const basicTitle = document.createElement("h4");
    basicTitle.className = "text-sm font-semibold text-blue-400 mb-3";
    basicTitle.textContent = "Basic Information";
    basicSection.appendChild(basicTitle);
    basicSection.appendChild(createTextField("civilization.id", "ID", civ.id, true));
    basicSection.appendChild(createTextField("civilization.civilization_type", "Civilization Type", civ.civilization_type, true));
    container.appendChild(basicSection);
    
    // Civilization Config (nested)
    const civConfigSection = document.createElement("div");
    civConfigSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const civConfigTitle = document.createElement("h4");
    civConfigTitle.className = "text-sm font-semibold text-blue-400 mb-3";
    civConfigTitle.textContent = "Civilization Configuration";
    civConfigSection.appendChild(civConfigTitle);
    const civConfig = civ.civilization || {};
    civConfigSection.appendChild(createTextField("civilization.civilization.domain", "Domain", civConfig.domain));
    civConfigSection.appendChild(createTextField("civilization.civilization.civilization_type", "Civilization Type", civConfig.civilization_type));
    civConfigSection.appendChild(createTextField("civilization.civilization.unique_culture_progression_tree", "Unique Culture Progression Tree", civConfig.unique_culture_progression_tree));
    civConfigSection.appendChild(createNumberField("civilization.civilization.random_city_name_depth", "Random City Name Depth", civConfig.random_city_name_depth));
    container.appendChild(civConfigSection);
    
    // Traits
    const traitsSection = document.createElement("div");
    traitsSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const traitsTitle = document.createElement("h4");
    traitsTitle.className = "text-sm font-semibold text-blue-400 mb-3";
    traitsTitle.textContent = "Civilization Traits";
    traitsSection.appendChild(traitsTitle);
    traitsSection.appendChild(createStringArrayField("civilization.civilization_traits", "Traits", civ.civilization_traits || [], "civilization"));
    container.appendChild(traitsSection);
    
    // Tags
    const tagsSection = document.createElement("div");
    tagsSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const tagsTitle = document.createElement("h4");
    tagsTitle.className = "text-sm font-semibold text-blue-400 mb-3";
    tagsTitle.textContent = "Civilization Tags";
    tagsSection.appendChild(tagsTitle);
    tagsSection.appendChild(createStringArrayField("civilization.civilization_tags", "Tags", civ.civilization_tags || [], "civilization"));
    container.appendChild(tagsSection);
    
    // Icon
    const iconSection = document.createElement("div");
    iconSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const iconTitle = document.createElement("h4");
    iconTitle.className = "text-sm font-semibold text-blue-400 mb-3";
    iconTitle.textContent = "Icon";
    iconSection.appendChild(iconTitle);
    const civIcon = civ.icon || {};
    iconSection.appendChild(createTextField("civilization.icon.path", "Icon Path", civIcon.path));
    container.appendChild(iconSection);
    
    // Start Bias Terrains
    const startBiasTerrainSection = document.createElement("div");
    startBiasTerrainSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const startBiasTerrainTitle = document.createElement("h4");
    startBiasTerrainTitle.className = "text-sm font-semibold text-blue-400 mb-3";
    startBiasTerrainTitle.textContent = "Start Bias - Terrains";
    startBiasTerrainSection.appendChild(startBiasTerrainTitle);
    renderStartBiasTerrains(startBiasTerrainSection, civ.start_bias_terrains || [], container);
    container.appendChild(startBiasTerrainSection);
    
    // Start Bias Rivers
    const startBiasRiversSection = document.createElement("div");
    startBiasRiversSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    startBiasRiversSection.appendChild(createNumberField("civilization.start_bias_rivers", "Start Bias - Rivers", civ.start_bias_rivers));
    container.appendChild(startBiasRiversSection);
    
    // Civilization Unlocks
    const unlocksSection = document.createElement("div");
    unlocksSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const unlocksTitle = document.createElement("h4");
    unlocksTitle.className = "text-sm font-semibold text-purple-400 mb-3";
    unlocksTitle.textContent = "Civilization Unlocks";
    unlocksSection.appendChild(unlocksTitle);
    renderCivilizationUnlocks(unlocksSection, civ.civilization_unlocks || [], container);
    container.appendChild(unlocksSection);
    
    // Leader Civilization Biases
    const leaderBiasesSection = document.createElement("div");
    leaderBiasesSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const leaderBiasesTitle = document.createElement("h4");
    leaderBiasesTitle.className = "text-sm font-semibold text-purple-400 mb-3";
    leaderBiasesTitle.textContent = "Leader Civilization Biases";
    leaderBiasesSection.appendChild(leaderBiasesTitle);
    renderLeaderCivilizationBiases(leaderBiasesSection, civ.leader_civilization_biases || [], container);
    container.appendChild(leaderBiasesSection);
    
    // Localizations
    const localizationsSection = document.createElement("div");
    localizationsSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const localizationsTitle = document.createElement("h4");
    localizationsTitle.className = "text-sm font-semibold text-cyan-400 mb-3";
    localizationsTitle.textContent = "Localizations";
    localizationsSection.appendChild(localizationsTitle);
    renderLocalizations(localizationsSection, civ.localizations || [], container);
    container.appendChild(localizationsSection);
    
    // Loading Info Civilizations
    const loadingInfoSection = document.createElement("div");
    loadingInfoSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const loadingInfoTitle = document.createElement("h4");
    loadingInfoTitle.className = "text-sm font-semibold text-orange-400 mb-3";
    loadingInfoTitle.textContent = "Loading Info";
    loadingInfoSection.appendChild(loadingInfoTitle);
    renderLoadingInfoCivilizations(loadingInfoSection, civ.loading_info_civilizations || [], container);
    container.appendChild(loadingInfoSection);
    
    // Leader Civ Priorities
    const leaderPrioritiesSection = document.createElement("div");
    leaderPrioritiesSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const leaderPrioritiesTitle = document.createElement("h4");
    leaderPrioritiesTitle.className = "text-sm font-semibold text-orange-400 mb-3";
    leaderPrioritiesTitle.textContent = "Leader Civilization Priorities";
    leaderPrioritiesSection.appendChild(leaderPrioritiesTitle);
    renderLeaderCivPriorities(leaderPrioritiesSection, civ.leader_civ_priorities || [], container);
    container.appendChild(leaderPrioritiesSection);
    
    // AI List Types
    const aiListTypesSection = document.createElement("div");
    aiListTypesSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const aiListTypesTitle = document.createElement("h4");
    aiListTypesTitle.className = "text-sm font-semibold text-green-400 mb-3";
    aiListTypesTitle.textContent = "AI List Types";
    aiListTypesSection.appendChild(aiListTypesTitle);
    renderAIListTypes(aiListTypesSection, civ.ai_list_types || [], container);
    container.appendChild(aiListTypesSection);
    
    // AI Lists
    const aiListsSection = document.createElement("div");
    aiListsSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const aiListsTitle = document.createElement("h4");
    aiListsTitle.className = "text-sm font-semibold text-green-400 mb-3";
    aiListsTitle.textContent = "AI Lists";
    aiListsSection.appendChild(aiListsTitle);
    renderAILists(aiListsSection, civ.ai_lists || [], container);
    container.appendChild(aiListsSection);
    
    // AI Favored Items
    const aiFavoredSection = document.createElement("div");
    aiFavoredSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const aiFavoredTitle = document.createElement("h4");
    aiFavoredTitle.className = "text-sm font-semibold text-green-400 mb-3";
    aiFavoredTitle.textContent = "AI Favored Items";
    aiFavoredSection.appendChild(aiFavoredTitle);
    renderAIFavoredItems(aiFavoredSection, civ.ai_favored_items || [], container);
    container.appendChild(aiFavoredSection);
    
    // Visual Art Cultures
    const visArtSection = document.createElement("div");
    visArtSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const visArtTitle = document.createElement("h4");
    visArtTitle.className = "text-sm font-semibold text-pink-400 mb-3";
    visArtTitle.textContent = "Visual Art Cultures";
    visArtSection.appendChild(visArtTitle);
    visArtSection.appendChild(createStringArrayField("civilization.vis_art_building_cultures", "Building Cultures", civ.vis_art_building_cultures || [], "civilization"));
    visArtSection.appendChild(createStringArrayField("civilization.vis_art_unit_cultures", "Unit Cultures", civ.vis_art_unit_cultures || [], "civilization"));
    container.appendChild(visArtSection);
    
    // Bindings
    const bindingsSection = document.createElement("div");
    bindingsSection.className = "mb-6 p-4 bg-slate-800/30 rounded-lg border border-slate-700";
    const bindingsTitle = document.createElement("h4");
    bindingsTitle.className = "text-sm font-semibold text-pink-400 mb-3";
    bindingsTitle.textContent = "Bindings";
    bindingsSection.appendChild(bindingsTitle);
    bindingsSection.appendChild(createStringArrayField("civilization.bindings", "Bindings", civ.bindings || [], "civilization"));
    container.appendChild(bindingsSection);
}

// Helper functions for rendering complex civilization sub-structures
function renderStartBiasTerrains(container, terrains, parentContainer) {
    // Clear and re-render the entire subsection to keep field paths in sync
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentTerrains = currentData.civilization.start_bias_terrains || [];
        currentTerrains.forEach((terrain, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.start_bias_terrains.${idx}.terrain_type`, "Terrain Type", terrain.terrain_type || ""));
            itemDiv.appendChild(createNumberField(`civilization.start_bias_terrains.${idx}.score`, "Score", terrain.score || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.start_bias_terrains.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Terrain Bias";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.start_bias_terrains) {
            currentData.civilization.start_bias_terrains = [];
        }
        currentData.civilization.start_bias_terrains.push({ terrain_type: "", score: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderCivilizationUnlocks(container, unlocks, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentUnlocks = currentData.civilization.civilization_unlocks || [];
        currentUnlocks.forEach((unlock, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.age_type`, "Age Type", unlock.age_type || ""));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.type`, "Type", unlock.type || ""));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.kind`, "Kind", unlock.kind || ""));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.name`, "Name", unlock.name || ""));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.description`, "Description", unlock.description || ""));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.icon`, "Icon", unlock.icon || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.civilization_unlocks.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Civilization Unlock";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.civilization_unlocks) {
            currentData.civilization.civilization_unlocks = [];
        }
        currentData.civilization.civilization_unlocks.push({ age_type: "", type: "", kind: "", name: "", description: "", icon: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderLeaderCivilizationBiases(container, biases, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentBiases = currentData.civilization.leader_civilization_biases || [];
        currentBiases.forEach((bias, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.leader_civilization_biases.${idx}.leader_type`, "Leader Type", bias.leader_type || ""));
            itemDiv.appendChild(createNumberField(`civilization.leader_civilization_biases.${idx}.bias`, "Bias", bias.bias || ""));
            itemDiv.appendChild(createTextField(`civilization.leader_civilization_biases.${idx}.reason_type`, "Reason Type", bias.reason_type || ""));
            itemDiv.appendChild(createTextField(`civilization.leader_civilization_biases.${idx}.choice_type`, "Choice Type", bias.choice_type || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.leader_civilization_biases.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Leader Bias";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.leader_civilization_biases) {
            currentData.civilization.leader_civilization_biases = [];
        }
        currentData.civilization.leader_civilization_biases.push({ leader_type: "", bias: "", reason_type: "", choice_type: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderLocalizations(container, localizations, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentLocs = currentData.civilization.localizations || [];
        currentLocs.forEach((loc, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.entity_id`, "Entity ID (optional)", loc.entity_id || ""));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.name`, "Name", loc.name || ""));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.description`, "Description", loc.description || ""));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.full_name`, "Full Name", loc.full_name || ""));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.adjective`, "Adjective", loc.adjective || ""));
            
            if (loc.city_names) {
                itemDiv.appendChild(createStringArrayField(`civilization.localizations.${idx}.city_names`, "City Names", loc.city_names || [], "civilization"));
            }
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.localizations.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Localization";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.localizations) {
            currentData.civilization.localizations = [];
        }
        currentData.civilization.localizations.push({ name: "", description: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderLoadingInfoCivilizations(container, infos, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentInfos = currentData.civilization.loading_info_civilizations || [];
        currentInfos.forEach((info, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.civilization_text`, "Civilization Text", info.civilization_text || ""));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.subtitle`, "Subtitle", info.subtitle || ""));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.tip`, "Tip", info.tip || ""));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.background_image_high`, "Background Image (High)", info.background_image_high || ""));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.background_image_low`, "Background Image (Low)", info.background_image_low || ""));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.foreground_image`, "Foreground Image", info.foreground_image || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.loading_info_civilizations.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Loading Info";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.loading_info_civilizations) {
            currentData.civilization.loading_info_civilizations = [];
        }
        currentData.civilization.loading_info_civilizations.push({ civilization_text: "", subtitle: "", tip: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderLeaderCivPriorities(container, priorities, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentPriorities = currentData.civilization.leader_civ_priorities || [];
        currentPriorities.forEach((priority, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.leader_civ_priorities.${idx}.leader_type`, "Leader Type", priority.leader_type || ""));
            itemDiv.appendChild(createNumberField(`civilization.leader_civ_priorities.${idx}.priority`, "Priority", priority.priority || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.leader_civ_priorities.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Priority";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.leader_civ_priorities) {
            currentData.civilization.leader_civ_priorities = [];
        }
        currentData.civilization.leader_civ_priorities.push({ leader_type: "", priority: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderAIListTypes(container, listTypes, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentListTypes = currentData.civilization.ai_list_types || [];
        currentListTypes.forEach((listType, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.ai_list_types.${idx}.list_type`, "List Type", listType.list_type || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.ai_list_types.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add AI List Type";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.ai_list_types) {
            currentData.civilization.ai_list_types = [];
        }
        currentData.civilization.ai_list_types.push({ list_type: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderAILists(container, aiLists, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentAILists = currentData.civilization.ai_lists || [];
        currentAILists.forEach((aiList, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.ai_lists.${idx}.list_type`, "List Type", aiList.list_type || ""));
            itemDiv.appendChild(createTextField(`civilization.ai_lists.${idx}.leader_type`, "Leader Type", aiList.leader_type || ""));
            itemDiv.appendChild(createTextField(`civilization.ai_lists.${idx}.system`, "System", aiList.system || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.ai_lists.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add AI List";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.ai_lists) {
            currentData.civilization.ai_lists = [];
        }
        currentData.civilization.ai_lists.push({ list_type: "", leader_type: "", system: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

function renderAIFavoredItems(container, favoredItems, parentContainer) {
    container.innerHTML = "";
    
    const itemsDiv = document.createElement("div");
    itemsDiv.className = "space-y-3";
    
    const rerenderItems = () => {
        itemsDiv.innerHTML = "";
        const currentItems = currentData.civilization.ai_favored_items || [];
        currentItems.forEach((item, idx) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2";
            
            itemDiv.appendChild(createTextField(`civilization.ai_favored_items.${idx}.list_type`, "List Type", item.list_type || ""));
            itemDiv.appendChild(createTextField(`civilization.ai_favored_items.${idx}.item`, "Item", item.item || ""));
            itemDiv.appendChild(createNumberField(`civilization.ai_favored_items.${idx}.value`, "Value", item.value || ""));
            
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
            removeBtn.type = "button";
            removeBtn.onclick = () => {
                currentData.civilization.ai_favored_items.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);
            
            itemsDiv.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
    const addBtn = document.createElement("button");
    addBtn.textContent = "+ Add Favored Item";
    addBtn.className = "px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm";
    addBtn.type = "button";
    addBtn.onclick = () => {
        if (!currentData.civilization.ai_favored_items) {
            currentData.civilization.ai_favored_items = [];
        }
        currentData.civilization.ai_favored_items.push({ list_type: "", item: "", value: "" });
        markDirty();
        rerenderItems();
    };
    
    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
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

// Track most-used autocomplete values
let autocompleteUsageStats = JSON.parse(localStorage.getItem('autocompleteUsage') || '{}');

function recordAutocompleteUsage(fieldName, value) {
    if (!autocompleteUsageStats[fieldName]) {
        autocompleteUsageStats[fieldName] = {};
    }
    if (!autocompleteUsageStats[fieldName][value]) {
        autocompleteUsageStats[fieldName][value] = 0;
    }
    autocompleteUsageStats[fieldName][value]++;
    localStorage.setItem('autocompleteUsage', JSON.stringify(autocompleteUsageStats));
}

function getMostCommonValues(fieldName, allOptions, limit = 10) {
    const usage = autocompleteUsageStats[fieldName] || {};
    const sorted = allOptions.sort((a, b) => {
        const aCount = usage[a] || 0;
        const bCount = usage[b] || 0;
        return bCount - aCount;
    });
    return sorted.slice(0, limit);
}

async function getAutocompleteOptions(fieldName, includeBindings = false) {
    // Extract the last part of the field name (e.g., "collection" from "modifiers.0.modifier.collection")
    const fieldType = fieldName.split('.').pop();
    
    // Special handling for bindings - pull from current file's builder IDs
    if (includeBindings && fieldType === 'binding') {
        return getAvailableBindings();
    }
    
    const dataType = AUTOCOMPLETE_MAPPINGS[fieldType];
    if (!dataType) {
        return [];
    }
    
    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (response.ok) {
            const data = await response.json();
            // JSON files have structure: { values: [{ id: "...", ... }, ...] }
            let options = data.values ? data.values.map(v => v.id) : [];
            
            // Apply categorization for tags - group by category if available
            if (dataType === 'tags' && data.values && data.values[0]?.category) {
                options = options; // Keep flat for now, categorization in dropdown rendering
            }
            
            return options;
        }
    } catch (error) {
        console.error(`Failed to fetch autocomplete data for ${fieldType}:`, error);
    }
    return [];
}

function getAvailableBindings() {
    // Collect all builder IDs from current data or wizard data
    const data = currentMode === 'guided' ? wizardData : currentData;
    const bindings = [];
    
    // From units
    if (data.units) {
        data.units.forEach(u => u.id && bindings.push(u.id));
    }
    
    // From constructibles
    if (data.constructibles) {
        data.constructibles.forEach(c => c.id && bindings.push(c.id));
    }
    
    // From modifiers
    if (data.modifiers) {
        data.modifiers.forEach(m => m.id && bindings.push(m.id));
    }
    
    // From traditions
    if (data.traditions) {
        data.traditions.forEach(t => t.id && bindings.push(t.id));
    }
    
    // From progression trees
    if (data.progression_trees) {
        data.progression_trees.forEach(pt => pt.id && bindings.push(pt.id));
    }
    
    // From progression tree nodes
    if (data.progression_tree_nodes) {
        data.progression_tree_nodes.forEach(ptn => ptn.id && bindings.push(ptn.id));
    }
    
    return bindings;
}

function createAutocompleteField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            showFieldHelpModal(label, helpText);
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const inputWrapper = document.createElement("div");
    inputWrapper.className = "relative";
    
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    input.autocomplete = "off";
    
    const dropdown = document.createElement("div");
    dropdown.className = "absolute top-full left-0 right-0 mt-1 bg-slate-800 border border-slate-600 rounded shadow-lg max-h-64 overflow-y-auto z-1000";
    dropdown.style.display = "none";
    
    let allOptions = [];
    let filteredOptions = [];
    let categoryData = null;
    
    // Load options asynchronously
    (async () => {
        const isBindingField = fieldName.includes('binding');
        allOptions = await getAutocompleteOptions(fieldName, isBindingField);
        
        // Load category data for tags
        if (fieldName.includes('tag')) {
            try {
                const response = await fetch('/api/data/tags');
                if (response.ok) {
                    const data = await response.json();
                    categoryData = data.values;
                }
            } catch (e) {
                console.error('Failed to load tag categories:', e);
            }
        }
        
        updateDropdown();
    })();
    
    function getCategoryLabel(tagId) {
        if (!categoryData) return null;
        const tag = categoryData.find(t => t.id === tagId);
        return tag?.category || 'UNCATEGORIZED';
    }
    
    function updateDropdown() {
        const query = input.value.toLowerCase();
        
        // Filter options based on query
        if (query.length === 0) {
            // Show most-common values first when empty
            const mostCommon = getMostCommonValues(fieldName, allOptions, 15);
            filteredOptions = mostCommon.length > 0 ? mostCommon : allOptions.slice(0, 50);
        } else {
            filteredOptions = allOptions.filter(opt => {
                const optStr = String(opt).toLowerCase();
                return optStr.includes(query);
            });
        }
        
        filteredOptions = filteredOptions.slice(0, 50); // Cap at 50 options
        
        dropdown.innerHTML = "";
        
        if (filteredOptions.length === 0) {
            const noResults = document.createElement("div");
            noResults.className = "px-3 py-2 text-slate-400 text-sm";
            noResults.textContent = query.length > 0 ? "No results" : "No options available";
            dropdown.appendChild(noResults);
            dropdown.style.display = "block";
        } else {
            // Group by category for tags
            if (fieldName.includes('tag') && categoryData) {
                const grouped = {};
                filteredOptions.forEach(opt => {
                    const cat = getCategoryLabel(opt) || 'UNCATEGORIZED';
                    if (!grouped[cat]) grouped[cat] = [];
                    grouped[cat].push(opt);
                });
                
                // Render categorized options
                Object.entries(grouped).forEach(([category, values]) => {
                    const catHeader = document.createElement("div");
                    catHeader.className = "px-3 py-1 text-xs font-semibold text-slate-400 bg-slate-900 sticky top-0";
                    catHeader.textContent = category;
                    dropdown.appendChild(catHeader);
                    
                    values.forEach(opt => {
                        const optDiv = document.createElement("div");
                        optDiv.className = "px-4 py-2 cursor-pointer hover:bg-slate-700 text-slate-100 text-sm border-l-2 border-slate-700";
                        optDiv.textContent = opt;
                        optDiv.onclick = () => {
                            input.value = opt;
                            recordAutocompleteUsage(fieldName, opt);
                            updateFieldValue(fieldName, opt);
                            dropdown.style.display = "none";
                            
                            // Validate and show feedback
                            validateFieldDependency(fieldName, opt);
                        };
                        dropdown.appendChild(optDiv);
                    });
                });
            } else {
                // Regular flat list for non-tag fields
                filteredOptions.forEach((opt, idx) => {
                    const optDiv = document.createElement("div");
                    optDiv.className = "px-3 py-2 cursor-pointer hover:bg-slate-700 text-slate-100 text-sm" + 
                        (idx < 5 ? " bg-slate-700/30" : ""); // Highlight most-common at top
                    optDiv.textContent = opt;
                    optDiv.onclick = () => {
                        input.value = opt;
                        recordAutocompleteUsage(fieldName, opt);
                        updateFieldValue(fieldName, opt);
                        dropdown.style.display = "none";
                        
                        // Validate and show feedback
                        validateFieldDependency(fieldName, opt);
                    };
                    dropdown.appendChild(optDiv);
                });
            }
            dropdown.style.display = "block";
        }
    }
    
    input.addEventListener("input", updateDropdown);
    input.addEventListener("focus", () => {
        // Show all options when focused
        if (allOptions.length > 0) {
            updateDropdown();
        }
    });
    input.addEventListener("blur", () => {
        // Validate on blur
        setTimeout(() => {
            validateFieldBlur(fieldName, input.value);
        }, 200);
    });
    input.addEventListener("change", (e) => {
        recordAutocompleteUsage(fieldName, e.target.value);
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
    
    // Store reference for validation
    if (!div.dataset.fieldName) {
        div.dataset.fieldName = fieldName;
        div.dataset.fieldType = 'autocomplete';
    }
    
    return div;
}

// Create a wizard-style dropdown for reference data fields in expert mode
function createDataSelectField(fieldName, label, value = "", dataType = null, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300";
    labelElem.textContent = label;
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            showFieldHelpModal(label, helpText);
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const select = document.createElement("select");
    select.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors mt-1";
    select.dataset.fieldName = fieldName;
    select.dataset.dataType = dataType;
    
    // Generate unique ID for select element
    const selectId = `expert-select-${fieldName.replace(/\./g, '-').replace(/\[/g, '-').replace(/\]/g, '')}`;
    select.id = selectId;
    
    // Add placeholder
    const placeholderOption = document.createElement("option");
    placeholderOption.value = "";
    placeholderOption.textContent = "Select...";
    select.appendChild(placeholderOption);
    
    // Populate using wizard dropdown function
    if (dataType) {
        (async () => {
            try {
                const response = await fetch(`/api/data/${dataType}`);
                if (!response.ok) {
                    console.error(`Failed to fetch ${dataType}`);
                    return;
                }
                
                const data = await response.json();
                const values = data.values || [];
                
                // Clear existing options
                select.innerHTML = '';
                
                // Re-add placeholder
                const placeholder = document.createElement('option');
                placeholder.value = '';
                placeholder.textContent = 'Select...';
                select.appendChild(placeholder);
                
                // Add data options with friendly labels (wizard style)
                values.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    const friendlyLabel = idToLabel(item.id);
                    option.textContent = `${friendlyLabel} (${item.id})`;
                    if (item.id === value) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
                
            } catch (error) {
                console.error(`Error loading ${dataType}:`, error);
            }
        })();
    }
    
    select.addEventListener("change", (e) => {
        updateFieldValue(fieldName, e.target.value);
        markDirty();
    });
    
    div.appendChild(select);
    
    return div;
}

function createTextField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            showFieldHelpModal(label, helpText);
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors mt-1";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    
    input.addEventListener("change", (e) => {
        updateFieldValue(fieldName, e.target.value);
        markDirty();
    });
    
    // Add blur validation for required fields
    if (isRequired) {
        input.addEventListener("blur", () => {
            if (input.value.trim().length === 0) {
                showFieldError(div, `${label} is required`);
            } else {
                clearFieldError(div);
            }
        });
    }
    
    div.appendChild(input);
    return div;
}

function createNumberField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            showFieldHelpModal(label, helpText);
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const input = document.createElement("input");
    input.type = "number";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors mt-1";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    
    input.addEventListener("change", (e) => {
        const numValue = e.target.value ? parseInt(e.target.value) : "";
        updateFieldValue(fieldName, numValue);
        markDirty();
    });
    
    // Add blur validation
    if (isRequired) {
        input.addEventListener("blur", () => {
            if (input.value.trim().length === 0) {
                showFieldError(div, `${label} is required`);
            } else if (isNaN(parseInt(input.value))) {
                showFieldError(div, `${label} must be a number`);
            } else {
                clearFieldError(div);
            }
        });
    }
    
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
    
    const rerenderItems = () => {
        itemsContainer.innerHTML = "";
        
        // Get current array from currentData
        const parts = fieldName.split(".");
        let obj = currentData;
        for (let j = 0; j < parts.length - 1; j++) {
            if (!obj[parts[j]]) obj[parts[j]] = {};
            obj = obj[parts[j]];
        }
        const currentItems = obj[parts[parts.length - 1]] || [];
        
        currentItems.forEach((item, i) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "flex gap-2";
            
            const input = document.createElement("input");
            input.type = "text";
            input.value = item;
            input.dataset.fieldName = fieldName + "." + i;
            input.className = "flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm";
            input.addEventListener("change", (e) => {
                updateFieldValue(fieldName + "." + i, e.target.value);
            });
            
            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.textContent = "Remove";
            removeBtn.className = "px-3 py-2 bg-red-700 hover:bg-red-800 text-white text-sm rounded transition";
            removeBtn.onclick = () => {
                currentItems.splice(i, 1);
                markDirty();
                rerenderItems();
            };
            
            itemDiv.appendChild(input);
            itemDiv.appendChild(removeBtn);
            itemsContainer.appendChild(itemDiv);
        });
    };
    
    rerenderItems();
    
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
        rerenderItems();
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

function renderTraditionsSection(container, data) {
    container.innerHTML = "";
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
        itemDiv.appendChild(createDataSelectField(`traditions.${i}.tradition_type`, "Tradition Type", tradition.tradition_type, 'traditions'));
        
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
    container.innerHTML = "";
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
    container.innerHTML = "";
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
            itemDiv.appendChild(createDataSelectField(`progression_trees.${i}.progression_tree.age_type`, "Age Type", tree.progression_tree?.age_type, 'ages'));
            
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
        itemDiv.appendChild(createTextField(`units.${i}.unit_type`, "Unit Type", unit.unit_type, true));
        
        // Unit object
        if (!unit.unit) unit.unit = {};
        const unitDiv = document.createElement("div");
        unitDiv.className = "mt-3 p-3 bg-slate-900 rounded";
        unitDiv.appendChild(document.createElement("h5")).textContent = "Unit Config";
        unitDiv.lastChild.className = "font-semibold text-slate-400 mb-2 text-sm";
        
        unitDiv.appendChild(createDataSelectField(`units.${i}.unit.core_class`, "Core Class", unit.unit.core_class, 'core-classes', FIELD_HELP_TEXT.core_class));
        unitDiv.appendChild(createDataSelectField(`units.${i}.unit.domain`, "Domain", unit.unit.domain, 'domains', FIELD_HELP_TEXT.domain));
        unitDiv.appendChild(createDataSelectField(`units.${i}.unit.formation_class`, "Formation Class", unit.unit.formation_class, 'formation-classes', FIELD_HELP_TEXT.formation_class));
        unitDiv.appendChild(createDataSelectField(`units.${i}.unit.unit_movement_class`, "Movement Class", unit.unit.unit_movement_class, 'unit-movement-classes', FIELD_HELP_TEXT.unit_movement_class));
        unitDiv.appendChild(createNumberField(`units.${i}.unit.base_moves`, "Base Moves", unit.unit.base_moves));
        unitDiv.appendChild(createNumberField(`units.${i}.unit.base_sight_range`, "Sight Range", unit.unit.base_sight_range));
        
        itemDiv.appendChild(unitDiv);
        
        // Icon
        if (unit.icon) {
            itemDiv.appendChild(createTextField(`units.${i}.icon.path`, "Icon Path", unit.icon.path));
        }
        
        // Unit cost
        if (unit.unit_cost) {
            itemDiv.appendChild(createDataSelectField(`units.${i}.unit_cost.yield_type`, "Cost Yield", unit.unit_cost.yield_type, 'yield-types', FIELD_HELP_TEXT.yield_type));
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

// ============================================================================
// Real-Time Validation
// ============================================================================

async function validateFieldBlur(fieldName, value) {
    if (!value || value.length === 0) return; // Skip empty fields
    
    // Extract field type from dot notation
    const fieldType = fieldName.split('.').pop();
    
    // Skip validation for non-autocomplete fields
    if (!AUTOCOMPLETE_MAPPINGS[fieldType] && !fieldName.includes('binding')) return;
    
    // Get the input element
    const inputs = document.querySelectorAll(`input[data-field-name="${fieldName}"]`);
    if (inputs.length === 0) return;
    
    const input = inputs[inputs.length - 1];
    const wrapper = input.closest('div[class*="relative"]') || input.parentElement;
    
    // Validate against reference data
    try {
        const dataType = AUTOCOMPLETE_MAPPINGS[fieldType];
        
        if (!dataType && !fieldName.includes('binding')) return;
        
        let isValid = false;
        
        if (fieldName.includes('binding')) {
            // Validate against available bindings
            const availableBindings = getAvailableBindings();
            isValid = availableBindings.includes(value);
            
            if (!isValid && value.length > 0) {
                showFieldError(wrapper, `Binding "${value}" not found. Available: ${availableBindings.slice(0, 3).join(', ')}...`);
                return;
            }
        } else {
            // Validate against reference data
            const response = await fetch(`/api/data/${dataType}`);
            if (response.ok) {
                const data = await response.json();
                const validIds = data.values ? data.values.map(v => v.id) : [];
                isValid = validIds.includes(value);
                
                if (!isValid && value.length > 0) {
                    const suggestions = validIds.filter(id => id.toLowerCase().includes(value.toLowerCase())).slice(0, 3);
                    showFieldError(wrapper, 
                        `"${value}" is not a valid ${fieldType}. ${suggestions.length > 0 ? `Did you mean: ${suggestions.join(', ')}?` : 'Check reference data for valid options.'}`
                    );
                    return;
                }
            }
        }
        
        // Clear error if valid
        clearFieldError(wrapper);
    } catch (error) {
        console.error('Validation error:', error);
    }
}

function validateFieldDependency(fieldName, value) {
    // Validate dependencies between fields
    // Example: if effect field changes, warn if arguments array might be invalid
    
    if (fieldName.includes('effect') && value.startsWith('EFFECT_')) {
        // Future: could check if required arguments exist
    }
    
    if (fieldName.includes('requirement_type') && value.startsWith('REQUIREMENT_')) {
        // Future: could validate requirement configuration
    }
}

function showFieldError(wrapper, message) {
    // Remove existing error
    const existingError = wrapper.querySelector('.field-error');
    if (existingError) existingError.remove();
    
    // Add red border to input
    const input = wrapper.querySelector('input');
    if (input) {
        input.classList.add('border-red-500', 'bg-red-900/10');
        input.classList.remove('border-slate-600');
    }
    
    // Show error message below
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error text-xs text-red-400 mt-1 bg-red-900/20 p-2 rounded border border-red-700/50';
    errorDiv.textContent = '✗ ' + message;
    wrapper.appendChild(errorDiv);
}

function clearFieldError(wrapper) {
    // Remove error styling
    const input = wrapper.querySelector('input');
    if (input) {
        input.classList.remove('border-red-500', 'bg-red-900/10');
        input.classList.add('border-slate-600');
    }
    
    // Remove error message
    const errorDiv = wrapper.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function showFieldHelpModal(fieldLabel, helpText) {
    // Create and show a styled help modal
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4';
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    };
    
    const content = document.createElement('div');
    content.className = 'bg-slate-800 rounded-lg border border-slate-700 p-6 max-w-md';
    
    const title = document.createElement('h3');
    title.className = 'text-lg font-semibold text-blue-400 mb-3';
    title.textContent = fieldLabel;
    content.appendChild(title);
    
    const text = document.createElement('p');
    text.className = 'text-sm text-slate-300 mb-4 leading-relaxed';
    text.textContent = helpText;
    content.appendChild(text);
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors';
    closeBtn.textContent = 'Got it';
    closeBtn.onclick = () => modal.remove();
    content.appendChild(closeBtn);
    
    modal.appendChild(content);
    document.body.appendChild(modal);
}

function markDirty() {
    isDirty = true;
    updateDirtyIndicator();
}

function renderModifiersSection(container, data) {
    container.innerHTML = "";
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
        
        modDiv.appendChild(createDataSelectField(`modifiers.${i}.modifier.collection`, "Collection", modifier.modifier.collection, 'collection-types', FIELD_HELP_TEXT.collection));
        modDiv.appendChild(createDataSelectField(`modifiers.${i}.modifier.effect`, "Effect", modifier.modifier.effect, 'effects', FIELD_HELP_TEXT.effect));
        modDiv.appendChild(createBooleanField(`modifiers.${i}.modifier.permanent`, "Permanent", modifier.modifier.permanent));
        modDiv.appendChild(createBooleanField(`modifiers.${i}.modifier.run_once`, "Run Once", modifier.modifier.run_once));
        
        // Requirements array
        if (modifier.modifier.requirements?.length > 0 || true) {  // Always show section for editability
            const reqDiv = document.createElement("div");
            reqDiv.className = "mt-2 p-2 bg-slate-800/50 rounded border border-slate-700";
            const reqTitle = document.createElement("h6");
            reqTitle.className = "text-xs font-semibold text-slate-400 mb-2";
            reqTitle.textContent = "Requirements";
            reqDiv.appendChild(reqTitle);
            
            const reqsContainer = document.createElement("div");
            
            const rerenderReqs = () => {
                reqsContainer.innerHTML = "";
                const currentReqs = currentData.modifiers[i].modifier.requirements || [];
                currentReqs.forEach((req, ri) => {
                    const reqItemDiv = document.createElement("div");
                    reqItemDiv.className = "p-2 bg-slate-900 rounded mb-2 space-y-1";
                    reqItemDiv.appendChild(createTextField(`modifiers.${i}.modifier.requirements.${ri}.type`, "Type", req.type || ""));
                    
                    const removeReqBtn = document.createElement("button");
                    removeReqBtn.type = "button";
                    removeReqBtn.textContent = "Remove Requirement";
                    removeReqBtn.className = "px-2 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
                    removeReqBtn.onclick = () => {
                        currentData.modifiers[i].modifier.requirements.splice(ri, 1);
                        markDirty();
                        rerenderReqs();
                    };
                    reqItemDiv.appendChild(removeReqBtn);
                    reqsContainer.appendChild(reqItemDiv);
                });
            };
            
            rerenderReqs();
            reqDiv.appendChild(reqsContainer);
            
            const addReqBtn = document.createElement("button");
            addReqBtn.type = "button";
            addReqBtn.textContent = "+ Add Requirement";
            addReqBtn.className = "px-2 py-1 bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300 text-xs";
            addReqBtn.onclick = () => {
                if (!currentData.modifiers[i].modifier.requirements) {
                    currentData.modifiers[i].modifier.requirements = [];
                }
                currentData.modifiers[i].modifier.requirements.push({ type: "" });
                markDirty();
                rerenderReqs();
            };
            reqDiv.appendChild(addReqBtn);
            modDiv.appendChild(reqDiv);
        }
        
        // Arguments array
        if (modifier.modifier.arguments?.length > 0 || true) {  // Always show section for editability
            const argsDiv = document.createElement("div");
            argsDiv.className = "mt-2 p-2 bg-slate-800/50 rounded border border-slate-700";
            const argsTitle = document.createElement("h6");
            argsTitle.className = "text-xs font-semibold text-slate-400 mb-2";
            argsTitle.textContent = "Arguments";
            argsDiv.appendChild(argsTitle);
            
            const argsContainer = document.createElement("div");
            
            const rerenderArgs = () => {
                argsContainer.innerHTML = "";
                const currentArgs = currentData.modifiers[i].modifier.arguments || [];
                currentArgs.forEach((arg, ai) => {
                    const argItemDiv = document.createElement("div");
                    argItemDiv.className = "p-2 bg-slate-900 rounded mb-2 space-y-1";
                    argItemDiv.appendChild(createTextField(`modifiers.${i}.modifier.arguments.${ai}.name`, "Name", arg.name || ""));
                    argItemDiv.appendChild(createTextField(`modifiers.${i}.modifier.arguments.${ai}.value`, "Value", arg.value || ""));
                    
                    const removeArgBtn = document.createElement("button");
                    removeArgBtn.type = "button";
                    removeArgBtn.textContent = "Remove Argument";
                    removeArgBtn.className = "px-2 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs";
                    removeArgBtn.onclick = () => {
                        currentData.modifiers[i].modifier.arguments.splice(ai, 1);
                        markDirty();
                        rerenderArgs();
                    };
                    argItemDiv.appendChild(removeArgBtn);
                    argsContainer.appendChild(argItemDiv);
                });
            };
            
            rerenderArgs();
            argsDiv.appendChild(argsContainer);
            
            const addArgBtn = document.createElement("button");
            addArgBtn.type = "button";
            addArgBtn.textContent = "+ Add Argument";
            addArgBtn.className = "px-2 py-1 bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300 text-xs";
            addArgBtn.onclick = () => {
                if (!currentData.modifiers[i].modifier.arguments) {
                    currentData.modifiers[i].modifier.arguments = [];
                }
                currentData.modifiers[i].modifier.arguments.push({ name: "", value: "" });
                markDirty();
                rerenderArgs();
            };
            argsDiv.appendChild(addArgBtn);
            modDiv.appendChild(argsDiv);
        }
        
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

// ============================================================================
// Template System
// ============================================================================

function showTemplateModal() {
    const modal = document.getElementById('template-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function hideTemplateModal() {
    const modal = document.getElementById('template-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

async function loadTemplate(templateName) {
    try {
        hideTemplateModal();
        showLoading();
        
        const response = await fetch(`/api/templates/${templateName}`);
        
        if (!response.ok) {
            throw new Error(`Template not found: ${templateName}`);
        }
        
        const templateData = await response.json();
        
        // Load into wizard data if in guided mode, otherwise currentData
        if (currentMode === 'guided') {
            wizardData = templateData;
            wizardStep = 1;
            renderWizardStep();
            showToast(`Loaded ${templateName} template in Guided Mode`, 'success');
        } else {
            currentData = templateData;
            currentFilePath = `${templateName}-civilization.yml`;
            document.getElementById("file-path-input").value = currentFilePath;
            renderAllSections();
            showToast(`Loaded ${templateName} template in Expert Mode`, 'success');
        }
        
        isDirty = true;
        updateDirtyIndicator();
    } catch (error) {
        showToast(`Error loading template: ${error.message}`, 'error');
    }
}