/**
 * Wizard Module - Wizard flow engine and mode switching
 * Handles wizard state, step navigation, and mode transitions
 */

import {
    setCurrentMode,
    setWizardStep,
    resetWizardData,
    syncWizardToCurrentData,
    wizardData,
    clearAllState,
    currentData,
    wizardStep,
    markDirty,
} from '../state.js';
import { showToast } from '../ui.js';

/**
 * Initialize wizard mode
 * Always defaults to 'guided' (wizard is primary)
 */
export function initializeMode() {
    // Always start in guided mode - wizard is the primary interface
    switchMode('guided', false);
}

/**
 * Switch between guided and expert modes
 * @param {string} mode - 'guided' or 'expert'
 * @param {boolean} savePreference - Whether to save preference to localStorage
 */
export function switchMode(mode, savePreference = true) {
    setCurrentMode(mode);

    if (savePreference) {
        try {
            localStorage.setItem('editorMode', mode);
        } catch {
            // Silently fail if localStorage is unavailable
        }
    }

    const wizardContainer = document.getElementById('wizard-container');
    const editorContainer = document.getElementById('editor-container');
    const sidebar = document.querySelector('aside');
    const expertToggle = document.getElementById('expert-mode-toggle');
    const wizardToggle = document.getElementById('wizard-mode-toggle');

    if (mode === 'guided') {
        if (wizardContainer) wizardContainer.classList.remove('hidden');
        if (editorContainer) editorContainer.classList.add('hidden');
        if (sidebar) sidebar.classList.add('hidden');
        if (expertToggle) expertToggle.classList.remove('hidden');
        if (wizardToggle) wizardToggle.classList.add('hidden');
        renderWizardStep();
    } else {
        if (wizardContainer) wizardContainer.classList.add('hidden');
        if (editorContainer) editorContainer.classList.remove('hidden');
        if (sidebar) sidebar.classList.remove('hidden');
        if (expertToggle) expertToggle.classList.add('hidden');
        if (wizardToggle) wizardToggle.classList.remove('hidden');
        if (Object.keys(wizardData || {}).length > 0) {
            syncWizardToCurrentData();
        }
        // Call async function without blocking
        renderExpertMode().catch(err => console.error('[EXPERT_MODE_ERROR]', err));
    }
}

/**
 * Move to previous wizard step
 */
export function wizardPrevStep() {
    const currentStep = getCurrentWizardStep();
    if (currentStep > 1) {
        saveWizardStepData();
        setWizardStep(currentStep - 1);
        renderWizardStep();
    }
}

/**
 * Move to next wizard step
 */
export function wizardNextStep() {
    const currentStep = getCurrentWizardStep();
    if (currentStep === 5) {
        const errors = validateWizardData();
        if (errors.length > 0) {
            showToast(`Please fix: ${errors.join(', ')}`, 'error');
            return;
        }

        syncWizardToCurrentData();
        generateDefaultProgressionTree();
        switchMode('expert');
        showToast('Wizard completed! Default progression tree created.', 'success');
        return;
    }

    saveWizardStepData();
    setWizardStep(currentStep + 1);
    renderWizardStep();
}

/**
 * Render expert mode with all sections
 */
export async function renderExpertMode() {
    const editorContainer = document.getElementById('editor-container');
    if (!editorContainer) return;

    const { renderAllSections } = await import('../expert/sections.js');
    renderAllSections(editorContainer, currentData);
}

/**
 * Skip wizard and go directly to expert mode
 */
export function skipWizard() {
    if (confirm('Switch to Expert Mode? You can always switch back using the toggle at the top.')) {
        switchMode('expert');
    }
}

/**
 * Initialize wizard with empty data structure
 */
export function initializeWizard() {
    resetWizardData();
    renderWizardStep();
}

/**
 * Render current wizard step
 * Dispatches to appropriate step renderer
 */
export function renderWizardStep() {
    const content = document.getElementById('wizard-step-content');
    const indicator = document.getElementById('wizard-step-indicator');
    const prevBtn = document.getElementById('wizard-prev-btn');
    const nextBtn = document.getElementById('wizard-next-btn');

    if (!content) return;

    import('./step1.js').then(m => {
        import('./step2.js').then(m2 => {
            import('./step3.js').then(m3 => {
                import('./step4.js').then(m4 => {
                    import('./step5.js').then(m5 => {
                        const stepRenderers = [
                            null,
                            m.renderWizardStep1,
                            m2.renderWizardStep2,
                            m3.renderWizardStep3,
                            m4.renderWizardStep4,
                            m5.renderWizardStep5,
                        ];

                        const currentStep = wizardStep;
                        if (stepRenderers[currentStep]) {
                            stepRenderers[currentStep](content);
                        }

                        updateWizardIndicators(indicator);

                        if (prevBtn) {
                            prevBtn.disabled = currentStep === 1;
                        }
                        if (nextBtn) {
                            if (currentStep === 5) {
                                nextBtn.textContent = 'Finish & Save';
                                nextBtn.className = 'px-6 py-2 bg-green-600 hover:bg-green-700 rounded-lg font-medium transition-colors';
                            } else {
                                nextBtn.textContent = 'Next →';
                                nextBtn.className = 'px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors';
                            }
                        }
                    });
                });
            });
        });
    });
}

/**
 * Get current wizard step
 * @returns {number} Current step (1-5)
 */
export function getCurrentWizardStep() {
    return wizardStep;
}

/**
 * Update wizard step indicators
 * @param {HTMLElement} indicator - Indicator element
 */
function updateWizardIndicators(indicator) {
    if (!indicator) return;

    const step = wizardStep;
    indicator.textContent = `Step ${step} of 5`;

    // Update progress bar
    for (let i = 1; i <= 5; i++) {
        const progressBar = document.getElementById(`progress-step-${i}`);
        if (!progressBar) continue;
        if (i < step) {
            progressBar.className = 'wizard-progress-step flex-1 h-2 bg-green-600 rounded-full transition-all';
        } else if (i === step) {
            progressBar.className = 'wizard-progress-step flex-1 h-2 bg-blue-600 rounded-full transition-all';
        } else {
            progressBar.className = 'wizard-progress-step flex-1 h-2 bg-slate-700 rounded-full transition-all';
        }
    }
}

/**
 * Navigate to next wizard step (DUPLICATE REMOVED - see earlier definition)
 */
// Removed duplicate function - see line ~140

/**
 * Navigate to previous wizard step (DUPLICATE REMOVED - see earlier definition)
 */
// Removed duplicate function - see line ~130

/**
 * Save wizard step data
 * Called when moving between steps to persist form changes
 */
export function saveWizardStepData() {
    markDirty();
}

/**
 * Validate wizard data before finishing
 * @returns {Promise<Object>} Validation result { isValid: boolean, errors: string[] }
 */
export function validateWizardData() {
    const errors = [];

    if (!wizardData.metadata?.id) errors.push('Mod ID is required');
    if (!wizardData.metadata?.name) errors.push('Mod Name is required');
    if (!wizardData.metadata?.package) errors.push('Package is required');
    if (!wizardData.action_group?.action_group_id) errors.push('Starting Age is required');
    if (!wizardData.civilization?.civilization_type) errors.push('Civilization Type is required');
    if (!wizardData.civilization?.localizations?.[0]?.name) errors.push('Civilization Display Name is required');
    if (!wizardData.civilization?.civilization_traits || wizardData.civilization.civilization_traits.length === 0) {
        errors.push('At least one Civilization Trait is required');
    }

    return errors;
}

/**
 * Show field help modal with contextual information
 * @param {string} fieldName - Field name to show help for
 */
export function showFieldHelp(fieldName) {
    import('../state.js').then(m => {
        import('../ui.js').then(ui => {
            const helpText = m.FIELD_HELP_TEXT[fieldName] || 'No help available for this field';
            ui.showFieldHelpModal(fieldName, helpText);
        });
    });
}

/**
 * Create a new mod (clear all data and reset wizard)
 */
export function createNewMod() {
    if (confirm('Create a new mod? Current changes will be lost.')) {
        import('../state.js').then(m => {
            m.clearAllState();
            resetWizardData();
            initializeWizard();
            showToast('New mod created', 'success');
        });
    }
}

// ============================================================================
// Wizard Helper: Reference Data Dropdown
// ============================================================================

export function idToLabel(id) {
    if (!id) return '';

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

    return label
        .split('_')
        .map(word => word.charAt(0) + word.slice(1).toLowerCase())
        .join(' ');
}

export async function createWizardDropdown(
    elementId,
    dataType,
    currentValue = '',
    placeholder = 'Select...',
    filterByEra = null
) {
    const selectElement = document.getElementById(elementId);
    if (!selectElement) return;

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
            { id: 'TRAIT_MODERN_CIV', label: 'Modern Civilization' },
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

    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (!response.ok) {
            console.error(`Failed to fetch ${dataType}`);
            return;
        }

        const data = await response.json();
        let values = data.values || [];

        // Filter palace cultures by era if specified
        if (dataType === 'building-cultures-palace' && filterByEra) {
            values = values.filter(item => 
                item.eras && item.eras.length > 0 && item.eras.includes(filterByEra)
            );
        }

        selectElement.innerHTML = '';

        const placeholderOption = document.createElement('option');
        placeholderOption.value = '';
        placeholderOption.textContent = placeholder;
        selectElement.appendChild(placeholderOption);

        values.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;

            if (dataType === 'building-cultures' || dataType === 'building-cultures-palace' || dataType === 'building-cultures-ages' || dataType === 'building-culture-bases' || dataType === 'unit-cultures') {
                const displayName = item.name || item.id;
                let optionText = `${displayName} (${item.id})`;
                
                // Add era info for palace cultures
                if (dataType === 'building-cultures-palace' && item.eras && item.eras.length > 0) {
                    const eraLabels = item.eras.map(era => era.replace('AGE_', '').toLowerCase()).join(', ');
                    optionText += ` [${eraLabels}]`;
                }
                
                option.textContent = optionText;
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
// Wizard Helper: Default Progression Tree
// ============================================================================

export function generateDefaultProgressionTree() {
    // Check if we need to generate default nodes for existing trees
    const existingTrees = currentData.progression_trees || [];
    const existingNodes = currentData.progression_tree_nodes || [];
    const existingNodeIds = new Set(existingNodes.map(n => n.id));
    
    // For each tree, ensure it has valid node bindings
    for (const tree of existingTrees) {
        if (!tree.bindings || tree.bindings.length === 0 || 
            !tree.bindings.some(bindingId => existingNodeIds.has(bindingId))) {
            // Tree has no nodes - generate defaults for it
            const civType = currentData.civilization?.civilization_type || 'CIVILIZATION_CUSTOM';
            const civName = currentData.civilization?.localizations?.[0]?.name || 'Custom';
            const treeId = tree.id;
            const treeType = tree.progression_tree_type;
            const node1Type = `${treeType.replace('TREE_', 'NODE_')}_1`;
            const node2Type = `${treeType.replace('TREE_', 'NODE_')}_2`;
            
            if (!currentData.progression_tree_nodes) {
                currentData.progression_tree_nodes = [];
            }
            
            currentData.progression_tree_nodes.push({
                id: `${treeId}_node1`,
                progression_tree_node_type: node1Type,
                progression_tree_node: {
                    progression_tree_node_type: node1Type,
                },
                localizations: [{
                    name: `${civName} Foundations`,
                }],
                bindings: [],
            });
            
            currentData.progression_tree_nodes.push({
                id: `${treeId}_node2`,
                progression_tree_node_type: node2Type,
                progression_tree_node: {
                    progression_tree_node_type: node2Type,
                },
                localizations: [{
                    name: `${civName} Advancement`,
                }],
                bindings: [],
            });
            
            // Update tree bindings
            tree.bindings = [`${treeId}_node1`, `${treeId}_node2`];
            
            // Ensure prereqs exist
            if (!tree.progression_tree_prereqs) {
                tree.progression_tree_prereqs = [];
            }
            tree.progression_tree_prereqs.push({
                node: node2Type,
                prereq_node: node1Type,
            });
            
            markDirty();
        }
    }
    
    // If no trees exist at all, create a default one
    if (existingTrees.length === 0) {
        const civType = currentData.civilization?.civilization_type || 'CIVILIZATION_CUSTOM';
        const civName = currentData.civilization?.localizations?.[0]?.name || 'Custom';
        const ageType = currentData.action_group?.action_group_id || 'AGE_ANTIQUITY';
        const modId = currentData.metadata?.id || 'custom';

    const treeId = `progression_tree_${modId}`;
    const treeType = `TREE_CIVICS_${civType.replace('CIVILIZATION_', '')}`;
    const node1Type = `NODE_CIVICS_${civType.replace('CIVILIZATION_', '')}_1`;
    const node2Type = `NODE_CIVICS_${civType.replace('CIVILIZATION_', '')}_2`;

    if (!currentData.progression_tree_nodes) {
        currentData.progression_tree_nodes = [];
    }

    currentData.progression_tree_nodes.push({
        id: `${modId}_node1`,
        progression_tree_node_type: node1Type,
        progression_tree_node: {
            progression_tree_node_type: node1Type,
        },
        localizations: [{
            name: `${civName} Foundations`,
        }],
        bindings: [],
    });

    currentData.progression_tree_nodes.push({
        id: `${modId}_node2`,
        progression_tree_node_type: node2Type,
        progression_tree_node: {
            progression_tree_node_type: node2Type,
        },
        localizations: [{
            name: `${civName} Advancement`,
        }],
        bindings: [],
    });

    if (!currentData.progression_trees) {
        currentData.progression_trees = [];
    }

        currentData.progression_trees.push({
            id: treeId,
            progression_tree_type: treeType,
            progression_tree: {
                progression_tree_type: treeType,
                age_type: ageType,
            },
            progression_tree_prereqs: [{
                node: node2Type,
                prereq_node: node1Type,
            }],
            localizations: [{
                name: `${civName} Civic Tree`,
            }],
            bindings: [
                `${modId}_node1`,
                `${modId}_node2`,
            ],
        });

        if (currentData.civilization) {
            if (!currentData.civilization.civilization) {
                currentData.civilization.civilization = {};
            }
            currentData.civilization.civilization.unique_culture_progression_tree = treeType;

            if (!currentData.civilization.bindings) {
                currentData.civilization.bindings = [];
            }
            if (!currentData.civilization.bindings.includes(treeId)) {
                currentData.civilization.bindings.push(treeId);
            }
        }

        markDirty();
    }
}
