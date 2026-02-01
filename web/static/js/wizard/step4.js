/**
 * Wizard Step 4 - Modifiers & Traditions
 */

import { wizardData, markDirty } from '../state.js';
import { showToast } from '../ui.js';
import { createWizardDropdown } from './wizard.js';
import { fetchReferenceData } from '../data/loader.js';
import { renderProgressionTreeSection } from './progression_trees.js';

// Cache for traditions reference data
let cachedTraditions = null;

/**
 * Render Step 4: Modifiers & Traditions
 * @param {HTMLElement} container - Container element to render into
 */
export function renderWizardStep4(container) {
    const hasModifiers = wizardData.modifiers && wizardData.modifiers.length > 0;
    const hasTraditions = wizardData.traditions && wizardData.traditions.length > 0;

    // Ensure functions are available globally for onclick handlers
    if (typeof window !== 'undefined') {
        window.wizardShowModifierForm = wizardShowModifierForm;
        window.wizardEditModifier = wizardEditModifier;
        window.removeWizardModifier = removeWizardModifier;
        window.wizardShowTraditionForm = wizardShowTraditionForm;
        window.wizardEditTradition = wizardEditTradition;
        window.removeWizardTradition = removeWizardTradition;
        window.wizardSaveModifier = wizardSaveModifier;
        window.wizardCancelModifierForm = wizardCancelModifierForm;
        window.wizardSaveTradition = wizardSaveTradition;
        window.wizardCancelTraditionForm = wizardCancelTraditionForm;
        window.wizardAddRequirement = wizardAddRequirement;
        window.wizardRemoveRequirement = wizardRemoveRequirement;
        window.wizardAddRequirementArg = wizardAddRequirementArg;
        window.wizardRemoveRequirementArg = wizardRemoveRequirementArg;
        window.wizardSetTraditionMode = wizardSetTraditionMode;
        window.wizardOnExistingTraditionSelect = wizardOnExistingTraditionSelect;
    }

    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-green-400">✨ Step 4: Advanced Features (Optional)</h3>
                <p class="text-slate-400 text-sm mb-6">Add game modifiers and cultural traditions. Modifiers are automatically bound to your civilization. Progression trees are best configured in Expert Mode.</p>
            </div>
            
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-green-500"></span>
                        Game Modifiers (${wizardData.modifiers?.length || 0})
                    </h4>
                    <button 
                        onclick="window.wizardShowModifierForm()"
                        class="px-3 py-1 bg-green-600 hover:bg-green-700 rounded text-sm font-medium"
                    >
                        + Add Modifier
                    </button>
                </div>
                
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
                                        onclick="window.wizardEditModifier(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="window.removeWizardModifier(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No modifiers added yet</p>'}
                
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
                        
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Modifier Configuration</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Effect *</label>
                                    <select 
                                        id="wizard-modifier-effect" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Loading...</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Collection *</label>
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

                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Battle Tooltip (Optional)</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Preview Description</label>
                                    <textarea 
                                        id="wizard-modifier-preview" 
                                        placeholder="Shows in combat preview (e.g. +4 Combat Strength in Forest)"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Tooltip Text</label>
                                    <textarea 
                                        id="wizard-modifier-tooltip" 
                                        placeholder="Shows in unit tooltip (optional)"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                        
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <label class="flex items-center space-x-2 text-xs text-slate-300">
                                <input
                                    type="checkbox"
                                    id="wizard-modifier-bind-to-civ"
                                    class="rounded bg-slate-700 border-slate-600 text-blue-600 focus:ring-blue-500"
                                />
                                <span>Bind to civilization (always active)</span>
                            </label>
                            <p class="text-xs text-slate-400 mt-1 ml-6">
                                If checked, this modifier will be always active for the civilization.
                                If unchecked, you can link it to specific abilities via the Civ Ability section in Step 2.
                            </p>
                        </div>
                        
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Requirements (Optional)</summary>
                            <div class="p-3 pt-2">
                                <p class="text-xs text-slate-400 mb-2">Control when this modifier applies. Add requirements with type and arguments.</p>
                                <div id="wizard-modifier-requirements-container" class="space-y-2 mb-2">
                                    <!-- Requirements will be added here -->
                                </div>
                                <button 
                                    onclick="window.wizardAddRequirement()"
                                    type="button"
                                    class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs font-medium text-slate-300 border border-slate-600"
                                >
                                    + Add Requirement
                                </button>
                            </div>
                        </details>
                        
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
                                onclick="window.wizardSaveModifier()"
                                id="wizard-modifier-form-save"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="window.wizardCancelModifierForm()"
                                id="wizard-modifier-form-cancel"
                                class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-pink-500"></span>
                        Cultural Traditions (${wizardData.traditions?.length || 0})
                    </h4>
                    <button 
                        onclick="window.wizardShowTraditionForm()"
                        class="px-3 py-1 bg-pink-600 hover:bg-pink-700 rounded text-sm font-medium"
                    >
                        + Add Tradition
                    </button>
                </div>
                
                <p class="text-xs text-slate-400 mb-4">
                    Add traditions (policies) for your civilization. You can use existing base game traditions or create custom ones. Attach modifiers from the Game Modifiers section above.
                </p>
                
                ${hasTraditions ? `
                    <div class="space-y-2 mb-4">
                        ${wizardData.traditions.map((trad, idx) => {
                            const modifierCount = trad.modifier_ids?.length || 0;
                            const isExisting = trad.is_existing_tradition;
                            return `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600">
                                <div class="flex items-center justify-between">
                                    <div class="flex-1">
                                        <div class="flex items-center gap-2">
                                            <p class="font-medium text-sm">${trad.localizations?.[0]?.name || trad.id || 'Unnamed Tradition'}</p>
                                            ${isExisting ? '<span class="px-1.5 py-0.5 text-xs bg-blue-600/30 text-blue-300 rounded">Base Game</span>' : '<span class="px-1.5 py-0.5 text-xs bg-pink-600/30 text-pink-300 rounded">Custom</span>'}
                                        </div>
                                        <p class="text-xs text-slate-400 mt-1">${isExisting ? (trad.base_tradition_id || trad.id) : (trad.tradition_type || trad.id)}</p>
                                        ${trad.localizations?.[0]?.description ? `<p class="text-xs text-slate-500 mt-1 line-clamp-2">${trad.localizations[0].description}</p>` : ''}
                                        ${modifierCount > 0 ? `<p class="text-xs text-green-400 mt-1">📎 ${modifierCount} modifier${modifierCount > 1 ? 's' : ''} attached</p>` : ''}
                                    </div>
                                    <div class="flex gap-2 ml-4">
                                        <button 
                                            onclick="window.wizardEditTradition(${idx})"
                                            class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                        >
                                            Edit
                                        </button>
                                        <button 
                                            onclick="window.removeWizardTradition(${idx})"
                                            class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                            </div>
                        `}).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No traditions added yet. Click "+ Add Tradition" to get started.</p>'}
                
                <div id="wizard-tradition-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                    <div class="space-y-3">
                        <input type="hidden" id="wizard-tradition-edit-idx" value="-1" />
                        
                        <h5 class="text-sm font-semibold text-pink-400 border-b border-slate-600 pb-2 mb-3">Tradition Configuration</h5>
                        
                        <!-- Toggle: Use Existing vs Create Custom -->
                        <div class="flex gap-2 mb-4">
                            <button 
                                type="button"
                                id="wizard-tradition-mode-existing"
                                onclick="window.wizardSetTraditionMode('existing')"
                                class="flex-1 px-3 py-2 rounded text-sm font-medium border transition-colors"
                            >
                                📚 Use Existing Tradition
                            </button>
                            <button 
                                type="button"
                                id="wizard-tradition-mode-custom"
                                onclick="window.wizardSetTraditionMode('custom')"
                                class="flex-1 px-3 py-2 rounded text-sm font-medium border transition-colors"
                            >
                                ✨ Create Custom Tradition
                            </button>
                        </div>
                        
                        <!-- Existing Tradition Selection -->
                        <div id="wizard-tradition-existing-section" class="space-y-3">
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Select Base Game Tradition</label>
                                <select 
                                    id="wizard-tradition-existing-select"
                                    onchange="window.wizardOnExistingTraditionSelect()"
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                >
                                    <option value="">Loading traditions...</option>
                                </select>
                            </div>
                            <div id="wizard-tradition-existing-preview" class="hidden bg-slate-900/50 p-3 rounded border border-slate-700">
                                <p class="text-xs text-slate-400 mb-1">Description:</p>
                                <p id="wizard-tradition-existing-desc" class="text-sm text-slate-200"></p>
                                <p class="text-xs text-slate-400 mt-2">Base Modifiers: <span id="wizard-tradition-existing-mods" class="text-slate-300"></span></p>
                            </div>
                        </div>
                        
                        <!-- Custom Tradition Creation -->
                        <div id="wizard-tradition-custom-section" class="hidden space-y-3">
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Tradition ID *</label>
                                <input 
                                    type="text" 
                                    id="wizard-tradition-id" 
                                    placeholder="TRADITION_MY_CIVILIZATION_ABILITY"
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                />
                                <p class="text-xs text-slate-500 mt-1">Unique identifier for your tradition</p>
                            </div>
                            
                            <div class="grid grid-cols-2 gap-3">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Display Name *</label>
                                    <input 
                                        type="text" 
                                        id="wizard-tradition-name" 
                                        placeholder="My Tradition"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Age</label>
                                    <select 
                                        id="wizard-tradition-age"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">Any Age</option>
                                        <option value="AGE_ANTIQUITY">Antiquity</option>
                                        <option value="AGE_EXPLORATION">Exploration</option>
                                        <option value="AGE_MODERN">Modern</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                <textarea 
                                    id="wizard-tradition-desc" 
                                    placeholder="Describe what this tradition does..."
                                    rows="2"
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                ></textarea>
                            </div>
                        </div>
                        
                        <!-- Modifier Attachment Section (shared between modes) -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700 mt-4">
                            <h6 class="text-xs font-semibold text-green-400 mb-2">📎 Attach Modifiers</h6>
                            <p class="text-xs text-slate-400 mb-2">Select modifiers from the Game Modifiers section above to attach to this tradition.</p>
                            
                            <div id="wizard-tradition-modifiers-list" class="space-y-1 max-h-40 overflow-y-auto">
                                ${(wizardData.modifiers && wizardData.modifiers.length > 0) ? 
                                    wizardData.modifiers.map((mod, idx) => `
                                        <label class="flex items-center gap-2 p-2 rounded hover:bg-slate-800/50 cursor-pointer">
                                            <input 
                                                type="checkbox" 
                                                class="wizard-tradition-modifier-checkbox rounded"
                                                value="${mod.id}"
                                                data-modifier-idx="${idx}"
                                            />
                                            <span class="text-sm text-slate-200">${mod.id}</span>
                                            <span class="text-xs text-slate-400">${mod.modifier?.effect || ''}</span>
                                        </label>
                                    `).join('') :
                                    '<p class="text-xs text-slate-500 italic">No modifiers created yet. Add modifiers in the Game Modifiers section first.</p>'
                                }
                            </div>
                        </div>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="window.wizardSaveTradition()"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save Tradition
                            </button>
                            <button 
                                onclick="window.wizardCancelTraditionForm()"
                                class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            ${renderProgressionTreeSection()}
            
            <div class="bg-blue-900/20 border border-blue-700 rounded-lg p-4">
                <p class="text-sm text-blue-300">
                    <strong>💡 Tip:</strong> Create modifiers first, then attach them to traditions. Traditions define which policy slot they appear in; modifiers define the actual gameplay effects.
                </p>
            </div>
        </div>
    `;
}


/* attachStep4Listeners removed as we use inline onclick handlers */


export function wizardShowModifierForm() {
    const form = document.getElementById('wizard-modifier-form');
    const idxInput = document.getElementById('wizard-modifier-edit-idx');

    document.getElementById('wizard-modifier-id').value = '';
    document.getElementById('wizard-modifier-type').value = '';
    document.getElementById('wizard-modifier-permanent').checked = false;
    document.getElementById('wizard-modifier-runonce').checked = false;
    document.getElementById('wizard-modifier-desc').value = '';
    document.getElementById('wizard-modifier-preview').value = '';
    document.getElementById('wizard-modifier-tooltip').value = '';
    document.getElementById('wizard-modifier-args').value = '';
    idxInput.value = '-1';

    createWizardDropdown('wizard-modifier-effect', 'effects', '', 'Select effect...');
    createWizardDropdown('wizard-modifier-collection', 'collection-types', '', 'Select collection...');

    // Clear requirements
    const requirementsContainer = document.getElementById('wizard-modifier-requirements-container');
    if (requirementsContainer) {
        requirementsContainer.innerHTML = '';
    }

    form.classList.remove('hidden');
    document.getElementById('wizard-modifier-id').focus();
}

export function wizardCancelModifierForm() {
    const form = document.getElementById('wizard-modifier-form');
    form.classList.add('hidden');
    document.getElementById('wizard-modifier-id').value = '';
    document.getElementById('wizard-modifier-type').value = '';
    document.getElementById('wizard-modifier-effect').value = '';
    document.getElementById('wizard-modifier-collection').value = '';
    document.getElementById('wizard-modifier-permanent').checked = false;
    document.getElementById('wizard-modifier-runonce').checked = false;
    document.getElementById('wizard-modifier-desc').value = '';
    document.getElementById('wizard-modifier-preview').value = '';
    document.getElementById('wizard-modifier-tooltip').value = '';
    document.getElementById('wizard-modifier-bind-to-civ').checked = false;
    document.getElementById('wizard-modifier-args').value = '';
    document.getElementById('wizard-modifier-edit-idx').value = '-1';
    
    // Clear requirements
    const requirementsContainer = document.getElementById('wizard-modifier-requirements-container');
    if (requirementsContainer) {
        requirementsContainer.innerHTML = '';
    }
}

export function wizardSaveModifier() {
    const id = document.getElementById('wizard-modifier-id').value.trim();
    const modifierType = document.getElementById('wizard-modifier-type').value.trim();
    const effect = document.getElementById('wizard-modifier-effect').value.trim();
    const collection = document.getElementById('wizard-modifier-collection').value.trim();
    const permanent = document.getElementById('wizard-modifier-permanent').checked;
    const runOnce = document.getElementById('wizard-modifier-runonce').checked;
    const description = document.getElementById('wizard-modifier-desc').value.trim();
    const previewText = document.getElementById('wizard-modifier-preview').value.trim();
    const tooltipText = document.getElementById('wizard-modifier-tooltip').value.trim();
    const bindToCiv = document.getElementById('wizard-modifier-bind-to-civ').checked;
    const argsText = document.getElementById('wizard-modifier-args').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-modifier-edit-idx').value, 10);

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

    if (!wizardData.modifiers) {
        wizardData.modifiers = [];
    }

    const modifier = {
        id: id,
        modifier: {
            effect: effect,
            collection: collection,
        },
    };

    if (modifierType) modifier.modifier_type = modifierType;
    if (permanent) modifier.modifier.permanent = true;
    if (runOnce) modifier.modifier.run_once = true;

    // Parse requirements
    const requirementsContainer = document.getElementById('wizard-modifier-requirements-container');
    if (requirementsContainer && requirementsContainer.children.length > 0) {
        const requirements = [];
        const reqDivs = requirementsContainer.querySelectorAll('[data-req-idx]');
        
        reqDivs.forEach(reqDiv => {
            const typeSelect = reqDiv.querySelector('.wizard-req-type');
            const type = typeSelect ? typeSelect.value.trim() : '';
            
            if (type) {
                const req = { type: type };
                
                // Parse requirement arguments
                const argsContainer = reqDiv.querySelector('.wizard-req-args-container');
                if (argsContainer) {
                    const argDivs = argsContainer.querySelectorAll('[data-arg-idx]');
                    if (argDivs.length > 0) {
                        const args = [];
                        argDivs.forEach(argDiv => {
                            const nameInput = argDiv.querySelector('.wizard-req-arg-name');
                            const valueInput = argDiv.querySelector('.wizard-req-arg-value');
                            const name = nameInput ? nameInput.value.trim() : '';
                            const value = valueInput ? valueInput.value.trim() : '';
                            
                            if (name && value) {
                                args.push({ name: name, value: value });
                            }
                        });
                        if (args.length > 0) {
                            req.arguments = args;
                        }
                    }
                }
                
                requirements.push(req);
            }
        });
        
        if (requirements.length > 0) {
            modifier.modifier.requirements = requirements;
        }
    }

    // Parse arguments
    if (argsText) {
        const args = [];
        const lines = argsText.split('\n');
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed && trimmed.includes(':')) {
                const [name, value] = trimmed.split(':', 2);
                args.push({
                    name: name.trim(),
                    value: value.trim(),
                });
            }
        }
        if (args.length > 0) {
            modifier.modifier.arguments = args;
        }
    }

    if (description) {
        modifier.localizations = [{ description: description }];
    }

    const existingStrings = editIdx >= 0
        ? (wizardData.modifiers?.[editIdx]?.modifier_strings || []).filter(
            s => s.string_type !== 'PREVIEW_DESCRIPTION' && s.string_type !== 'TOOLTIP'
        )
        : [];

    const modifierStrings = [...existingStrings];
    if (previewText) {
        modifierStrings.push({ string_type: 'PREVIEW_DESCRIPTION', text: previewText });
    }
    if (tooltipText) {
        modifierStrings.push({ string_type: 'TOOLTIP', text: tooltipText });
    }
    if (modifierStrings.length > 0) {
        modifier.modifier_strings = modifierStrings;
    }
    
    if (bindToCiv) {
        modifier.bind_to_civilization = true;
    }

    if (editIdx >= 0) {
        wizardData.modifiers[editIdx] = modifier;
        showToast('Modifier updated', 'success');
    } else {
        wizardData.modifiers.push(modifier);
        showToast('Modifier added', 'success');
    }

    wizardCancelModifierForm();
    renderWizardStep4(document.getElementById('wizard-step-content'));
    markDirty();
}

export async function wizardEditModifier(idx) {
    const modifier = wizardData.modifiers[idx];
    document.getElementById('wizard-modifier-id').value = modifier.id || '';
    document.getElementById('wizard-modifier-type').value = modifier.modifier_type || '';
    document.getElementById('wizard-modifier-permanent').checked = modifier.modifier?.permanent || false;
    document.getElementById('wizard-modifier-runonce').checked = modifier.modifier?.run_once || false;
    document.getElementById('wizard-modifier-desc').value = modifier.localizations?.[0]?.description || '';
    const previewString = modifier.modifier_strings?.find(s => s.string_type === 'PREVIEW_DESCRIPTION');
    const tooltipString = modifier.modifier_strings?.find(s => s.string_type === 'TOOLTIP');
    document.getElementById('wizard-modifier-preview').value = previewString?.text || '';
    document.getElementById('wizard-modifier-tooltip').value = tooltipString?.text || '';
    document.getElementById('wizard-modifier-bind-to-civ').checked = modifier.bind_to_civilization === true;

    if (modifier.modifier?.arguments) {
        const argsText = modifier.modifier.arguments
            .map(arg => `${arg.name}:${arg.value}`)
            .join('\n');
        document.getElementById('wizard-modifier-args').value = argsText;
    } else {
        document.getElementById('wizard-modifier-args').value = '';
    }

    createWizardDropdown('wizard-modifier-effect', 'effects', modifier.modifier?.effect || '', 'Select effect...');
    createWizardDropdown('wizard-modifier-collection', 'collection-types', modifier.modifier?.collection || '', 'Select collection...');

    // Clear requirements container completely
    const requirementsContainer = document.getElementById('wizard-modifier-requirements-container');
    requirementsContainer.innerHTML = '';
    
    // Load requirement types data once
    const { fetchReferenceData } = await import('../data/loader.js');
    const requirementTypesData = await fetchReferenceData('requirement-types');
    
    if (modifier.modifier?.requirements && Array.isArray(modifier.modifier.requirements)) {
        // Add and populate each requirement synchronously
        for (const req of modifier.modifier.requirements) {
            // Add the requirement div
            const actualReqIdx = requirementsContainer.children.length;
            const reqDiv = document.createElement('div');
            reqDiv.className = 'p-2 bg-slate-800/50 rounded border border-slate-600';
            reqDiv.dataset.reqIdx = actualReqIdx;
            reqDiv.innerHTML = `
                <div class="flex items-start gap-2 mb-2">
                    <div class="flex-1">
                        <label class="block text-xs font-medium text-slate-300 mb-1">Requirement Type *</label>
                        <select 
                            class="wizard-req-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100 focus:outline-none focus:border-blue-400"
                            data-req-idx="${actualReqIdx}"
                        >
                            <option value="">Select requirement type...</option>
                        </select>
                    </div>
                    <button 
                        onclick="window.wizardRemoveRequirement(${actualReqIdx})"
                        type="button"
                        class="mt-5 px-2 py-1 bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300 text-xs"
                    >
                        Remove
                    </button>
                </div>
                <div class="wizard-req-args-container" data-req-idx="${actualReqIdx}">
                    <!-- Arguments will be added here -->
                </div>
                <button 
                    onclick="window.wizardAddRequirementArg(${actualReqIdx})"
                    type="button"
                    class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs font-medium text-slate-300 border border-slate-600 mt-2"
                >
                    + Add Argument
                </button>
            `;
            requirementsContainer.appendChild(reqDiv);
            
            // Populate the requirement type dropdown
            const typeSelect = reqDiv.querySelector('.wizard-req-type');
            if (requirementTypesData && requirementTypesData.values) {
                requirementTypesData.values.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    option.textContent = item.id;
                    if (item.id === req.type) {
                        option.selected = true;
                    }
                    typeSelect.appendChild(option);
                });
            }
            
            // Add requirement arguments
            if (req.arguments && Array.isArray(req.arguments)) {
                const argsContainer = reqDiv.querySelector('.wizard-req-args-container');
                req.arguments.forEach(arg => {
                    const argIdx = argsContainer.children.length;
                    const argDiv = document.createElement('div');
                    argDiv.className = 'flex gap-2 items-center mt-2';
                    argDiv.dataset.argIdx = argIdx;
                    argDiv.innerHTML = `
                        <input 
                            type="text" 
                            placeholder="Name" 
                            class="wizard-req-arg-name flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100 focus:outline-none focus:border-blue-400"
                            value="${arg.name || ''}"
                        />
                        <input 
                            type="text" 
                            placeholder="Value" 
                            class="wizard-req-arg-value flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100 focus:outline-none focus:border-blue-400"
                            value="${arg.value || ''}"
                        />
                        <button 
                            onclick="window.wizardRemoveRequirementArg(${actualReqIdx}, ${argIdx})"
                            type="button"
                            class="px-2 py-1 bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300 text-xs"
                        >
                            ×
                        </button>
                    `;
                    argsContainer.appendChild(argDiv);
                });
            }
        }
    }

    document.getElementById('wizard-modifier-edit-idx').value = idx;
    document.getElementById('wizard-modifier-form').classList.remove('hidden');
}

export function removeWizardModifier(idx) {
    if (wizardData.modifiers) {
        wizardData.modifiers.splice(idx, 1);
        renderWizardStep4(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Modifier removed', 'info');
    }
}

/**
 * Set the tradition creation mode (existing vs custom)
 * @param {string} mode - 'existing' or 'custom'
 */
export function wizardSetTraditionMode(mode) {
    const existingBtn = document.getElementById('wizard-tradition-mode-existing');
    const customBtn = document.getElementById('wizard-tradition-mode-custom');
    const existingSection = document.getElementById('wizard-tradition-existing-section');
    const customSection = document.getElementById('wizard-tradition-custom-section');
    
    if (mode === 'existing') {
        existingBtn.classList.add('bg-blue-600', 'border-blue-600', 'text-white');
        existingBtn.classList.remove('bg-slate-700', 'border-slate-600', 'text-slate-300');
        customBtn.classList.remove('bg-pink-600', 'border-pink-600', 'text-white');
        customBtn.classList.add('bg-slate-700', 'border-slate-600', 'text-slate-300');
        existingSection.classList.remove('hidden');
        customSection.classList.add('hidden');
    } else {
        customBtn.classList.add('bg-pink-600', 'border-pink-600', 'text-white');
        customBtn.classList.remove('bg-slate-700', 'border-slate-600', 'text-slate-300');
        existingBtn.classList.remove('bg-blue-600', 'border-blue-600', 'text-white');
        existingBtn.classList.add('bg-slate-700', 'border-slate-600', 'text-slate-300');
        customSection.classList.remove('hidden');
        existingSection.classList.add('hidden');
    }
    
    // Store current mode
    document.getElementById('wizard-tradition-form').dataset.mode = mode;
}

/**
 * Handle selection of existing tradition from dropdown
 */
export async function wizardOnExistingTraditionSelect() {
    const select = document.getElementById('wizard-tradition-existing-select');
    const preview = document.getElementById('wizard-tradition-existing-preview');
    const descEl = document.getElementById('wizard-tradition-existing-desc');
    const modsEl = document.getElementById('wizard-tradition-existing-mods');
    
    const selectedId = select.value;
    if (!selectedId) {
        preview.classList.add('hidden');
        return;
    }
    
    // Find the selected tradition in cache
    const traditions = await loadTraditionsData();
    const tradition = traditions.find(t => t.id === selectedId);
    
    if (tradition) {
        descEl.textContent = tradition.description || 'No description available';
        modsEl.textContent = tradition.modifiers?.length > 0 
            ? tradition.modifiers.join(', ') 
            : 'None';
        preview.classList.remove('hidden');
    }
}

/**
 * Load traditions reference data with caching
 */
async function loadTraditionsData() {
    if (cachedTraditions) {
        return cachedTraditions;
    }
    
    try {
        const data = await fetchReferenceData('traditions');
        cachedTraditions = data.values || [];
        return cachedTraditions;
    } catch (e) {
        console.error('Failed to load traditions:', e);
        return [];
    }
}

/**
 * Populate the existing traditions dropdown
 */
async function populateTraditionsDropdown() {
    const select = document.getElementById('wizard-tradition-existing-select');
    if (!select) return;
    
    const traditions = await loadTraditionsData();
    
    // Group by age
    const byAge = {
        'AGE_ANTIQUITY': [],
        'AGE_EXPLORATION': [],
        'AGE_MODERN': [],
        '': []  // No age restriction
    };
    
    traditions.forEach(t => {
        const age = t.age || '';
        if (byAge[age]) {
            byAge[age].push(t);
        } else {
            byAge[''].push(t);
        }
    });
    
    select.innerHTML = '<option value="">-- Select a Tradition --</option>';
    
    // Add Antiquity traditions
    if (byAge['AGE_ANTIQUITY'].length > 0) {
        const group = document.createElement('optgroup');
        group.label = '🏛️ Antiquity';
        byAge['AGE_ANTIQUITY'].forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = `${t.name || t.id}`;
            group.appendChild(opt);
        });
        select.appendChild(group);
    }
    
    // Add Exploration traditions
    if (byAge['AGE_EXPLORATION'].length > 0) {
        const group = document.createElement('optgroup');
        group.label = '🧭 Exploration';
        byAge['AGE_EXPLORATION'].forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = `${t.name || t.id}`;
            group.appendChild(opt);
        });
        select.appendChild(group);
    }
    
    // Add Modern traditions
    if (byAge['AGE_MODERN'].length > 0) {
        const group = document.createElement('optgroup');
        group.label = '🏭 Modern';
        byAge['AGE_MODERN'].forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = `${t.name || t.id}`;
            group.appendChild(opt);
        });
        select.appendChild(group);
    }
    
    // Add traditions without age
    if (byAge[''].length > 0) {
        const group = document.createElement('optgroup');
        group.label = '🌐 All Ages';
        byAge[''].forEach(t => {
            const opt = document.createElement('option');
            opt.value = t.id;
            opt.textContent = `${t.name || t.id}`;
            group.appendChild(opt);
        });
        select.appendChild(group);
    }
}

export async function wizardShowTraditionForm() {
    const form = document.getElementById('wizard-tradition-form');
    const idxInput = document.getElementById('wizard-tradition-edit-idx');

    // Reset form
    const idField = document.getElementById('wizard-tradition-id');
    const nameField = document.getElementById('wizard-tradition-name');
    const descField = document.getElementById('wizard-tradition-desc');
    const ageField = document.getElementById('wizard-tradition-age');
    const existingSelect = document.getElementById('wizard-tradition-existing-select');
    
    if (idField) idField.value = '';
    if (nameField) nameField.value = '';
    if (descField) descField.value = '';
    if (ageField) ageField.value = '';
    if (existingSelect) existingSelect.value = '';
    idxInput.value = '-1';
    
    // Reset modifier checkboxes
    document.querySelectorAll('.wizard-tradition-modifier-checkbox').forEach(cb => {
        cb.checked = false;
    });
    
    // Hide existing tradition preview
    const preview = document.getElementById('wizard-tradition-existing-preview');
    if (preview) preview.classList.add('hidden');

    // Populate dropdowns
    await populateTraditionsDropdown();
    
    // Default to existing mode
    wizardSetTraditionMode('existing');
    
    form.classList.remove('hidden');
}

export function wizardCancelTraditionForm() {
    const form = document.getElementById('wizard-tradition-form');
    form.classList.add('hidden');
    
    // Reset all form fields
    const idField = document.getElementById('wizard-tradition-id');
    const nameField = document.getElementById('wizard-tradition-name');
    const descField = document.getElementById('wizard-tradition-desc');
    const ageField = document.getElementById('wizard-tradition-age');
    const existingSelect = document.getElementById('wizard-tradition-existing-select');
    
    if (idField) idField.value = '';
    if (nameField) nameField.value = '';
    if (descField) descField.value = '';
    if (ageField) ageField.value = '';
    if (existingSelect) existingSelect.value = '';
    document.getElementById('wizard-tradition-edit-idx').value = '-1';
    
    // Reset modifier checkboxes
    document.querySelectorAll('.wizard-tradition-modifier-checkbox').forEach(cb => {
        cb.checked = false;
    });
}

export async function wizardSaveTradition() {
    const form = document.getElementById('wizard-tradition-form');
    const mode = form.dataset.mode || 'existing';
    const editIdx = parseInt(document.getElementById('wizard-tradition-edit-idx').value, 10);
    
    // Collect selected modifier IDs
    const selectedModifierIds = [];
    document.querySelectorAll('.wizard-tradition-modifier-checkbox:checked').forEach(cb => {
        selectedModifierIds.push(cb.value);
    });
    
    let tradition;
    
    if (mode === 'existing') {
        // Using an existing base game tradition
        const existingSelect = document.getElementById('wizard-tradition-existing-select');
        const selectedId = existingSelect.value;
        
        if (!selectedId) {
            showToast('Please select an existing tradition', 'error');
            return;
        }
        
        // Find the tradition in cache to get its details
        const traditions = await loadTraditionsData();
        const existingTradition = traditions.find(t => t.id === selectedId);
        
        tradition = {
            id: selectedId,
            is_existing_tradition: true,
            // Store original base game tradition ID for round-trip persistence
            base_tradition_id: selectedId,
            age: existingTradition?.age || '',
            trait_type: existingTradition?.trait_type || '',
            localizations: [{
                name: existingTradition?.name || selectedId,
                description: existingTradition?.description || ''
            }],
            modifier_ids: selectedModifierIds,
            // Preserve original modifiers from base game
            base_modifiers: existingTradition?.modifiers || []
        };
        
    } else {
        // Creating a custom tradition
        const id = document.getElementById('wizard-tradition-id').value.trim();
        const displayName = document.getElementById('wizard-tradition-name').value.trim();
        const description = document.getElementById('wizard-tradition-desc').value.trim();
        const age = document.getElementById('wizard-tradition-age').value;
        
        if (!id) {
            showToast('Tradition ID is required', 'error');
            return;
        }
        
        if (!displayName) {
            showToast('Tradition name is required', 'error');
            return;
        }
        
        // Auto-derive trait from civilization data
        let traitType = '';
        if (wizardData.civilization_type) {
            // Extract civ name from CIVILIZATION_XXX and create TRAIT_XXX_ABILITY
            const civName = wizardData.civilization_type.replace('CIVILIZATION_', '');
            traitType = `TRAIT_${civName}_ABILITY`;
        }
        
        tradition = {
            id: id,
            is_existing_tradition: false,
            age: age,
            trait_type: traitType,
            localizations: [{
                name: displayName,
                description: description
            }],
            modifier_ids: selectedModifierIds
        };
    }

    if (!wizardData.traditions) {
        wizardData.traditions = [];
    }

    if (editIdx >= 0) {
        wizardData.traditions[editIdx] = tradition;
        showToast('Tradition updated', 'success');
    } else {
        wizardData.traditions.push(tradition);
        showToast('Tradition added', 'success');
    }

    wizardCancelTraditionForm();
    renderWizardStep4(document.getElementById('wizard-step-content'));
    markDirty();
}

export async function wizardEditTradition(idx) {
    const tradition = wizardData.traditions[idx];
    const form = document.getElementById('wizard-tradition-form');
    
    // Populate dropdowns first
    await populateTraditionsDropdown();
    
    // Determine mode based on tradition type
    if (tradition.is_existing_tradition) {
        // Existing tradition mode
        wizardSetTraditionMode('existing');
        
        const existingSelect = document.getElementById('wizard-tradition-existing-select');
        // Use base_tradition_id if available, otherwise fall back to id
        if (existingSelect) existingSelect.value = tradition.base_tradition_id || tradition.id;
        
        // Trigger preview update
        await wizardOnExistingTraditionSelect();
    } else {
        // Custom tradition mode
        wizardSetTraditionMode('custom');
        
        const idField = document.getElementById('wizard-tradition-id');
        const nameField = document.getElementById('wizard-tradition-name');
        const descField = document.getElementById('wizard-tradition-desc');
        const ageField = document.getElementById('wizard-tradition-age');
        
        if (idField) idField.value = tradition.tradition_type || tradition.id || '';
        if (nameField) nameField.value = tradition.localizations?.[0]?.name || '';
        if (descField) descField.value = tradition.localizations?.[0]?.description || '';
        if (ageField) ageField.value = tradition.age || tradition.tradition?.age_type || '';
    }
    
    // Check the modifier checkboxes that are attached to this tradition
    const attachedModifierIds = tradition.modifier_ids || [];
    document.querySelectorAll('.wizard-tradition-modifier-checkbox').forEach(cb => {
        cb.checked = attachedModifierIds.includes(cb.value);
    });
    
    document.getElementById('wizard-tradition-edit-idx').value = idx;
    form.classList.remove('hidden');
}

export function removeWizardTradition(idx) {
    if (wizardData.traditions) {
        wizardData.traditions.splice(idx, 1);
        renderWizardStep4(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Tradition removed', 'info');
    }
}

/**
 * Add a new requirement to the modifier form
 */
export async function wizardAddRequirement() {
    const container = document.getElementById('wizard-modifier-requirements-container');
    const reqIdx = container.children.length;
    
    const reqDiv = document.createElement('div');
    reqDiv.className = 'p-2 bg-slate-800/50 rounded border border-slate-600';
    reqDiv.dataset.reqIdx = reqIdx;
    reqDiv.innerHTML = `
        <div class="flex items-start gap-2 mb-2">
            <div class="flex-1">
                <label class="block text-xs font-medium text-slate-300 mb-1">Requirement Type *</label>
                <select 
                    class="wizard-req-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100 focus:outline-none focus:border-blue-400"
                    data-req-idx="${reqIdx}"
                >
                    <option value="">Loading...</option>
                </select>
            </div>
            <button 
                onclick="window.wizardRemoveRequirement(${reqIdx})"
                type="button"
                class="mt-5 px-2 py-1 bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300 text-xs"
            >
                Remove
            </button>
        </div>
        <div class="wizard-req-args-container" data-req-idx="${reqIdx}">
            <!-- Arguments will be added here -->
        </div>
        <button 
            onclick="window.wizardAddRequirementArg(${reqIdx})"
            type="button"
            class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs font-medium text-slate-300 border border-slate-600 mt-2"
        >
            + Add Argument
        </button>
    `;
    
    container.appendChild(reqDiv);
    
    // Load requirement types dropdown
    const { fetchReferenceData } = await import('../data/loader.js');
    const data = await fetchReferenceData('requirement-types');
    const select = reqDiv.querySelector('.wizard-req-type');
    select.innerHTML = '<option value="">Select requirement type...</option>';
    if (data && data.values) {
        data.values.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = item.id;
            select.appendChild(option);
        });
    }
}

/**
 * Remove a requirement from the modifier form and re-index remaining requirements
 */
export function wizardRemoveRequirement(reqIdx) {
    const container = document.getElementById('wizard-modifier-requirements-container');
    const reqDiv = container.querySelector(`[data-req-idx="${reqIdx}"]`);
    if (reqDiv) {
        reqDiv.remove();
        
        // Re-index all remaining requirements to avoid gaps
        const remainingReqs = container.querySelectorAll('[data-req-idx]');
        remainingReqs.forEach((div, newIdx) => {
            // Update the requirement div index
            div.dataset.reqIdx = newIdx;
            
            // Update the select data attribute
            const select = div.querySelector('.wizard-req-type');
            if (select) {
                select.dataset.reqIdx = newIdx;
            }
            
            // Update the args container data attribute
            const argsContainer = div.querySelector('.wizard-req-args-container');
            if (argsContainer) {
                argsContainer.dataset.reqIdx = newIdx;
            }
            
            // Update onclick handlers
            const removeBtn = div.querySelector('button[onclick^="window.wizardRemoveRequirement"]');
            if (removeBtn) {
                removeBtn.setAttribute('onclick', `window.wizardRemoveRequirement(${newIdx})`);
            }
            
            const addArgBtn = div.querySelector('button[onclick^="window.wizardAddRequirementArg"]');
            if (addArgBtn) {
                addArgBtn.setAttribute('onclick', `window.wizardAddRequirementArg(${newIdx})`);
            }
            
            // Update argument remove buttons
            const argRemoveBtns = div.querySelectorAll('button[onclick*="wizardRemoveRequirementArg"]');
            argRemoveBtns.forEach((btn, argIdx) => {
                btn.setAttribute('onclick', `window.wizardRemoveRequirementArg(${newIdx}, ${argIdx})`);
            });
        });
    }
}

/**
 * Add an argument to a requirement
 */
export function wizardAddRequirementArg(reqIdx) {
    const argsContainer = document.querySelector(`.wizard-req-args-container[data-req-idx="${reqIdx}"]`);
    if (!argsContainer) return;
    
    const argIdx = argsContainer.children.length;
    const argDiv = document.createElement('div');
    argDiv.className = 'flex gap-2 items-center mt-2';
    argDiv.dataset.argIdx = argIdx;
    argDiv.innerHTML = `
        <input 
            type="text" 
            placeholder="Name" 
            class="wizard-req-arg-name flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100 focus:outline-none focus:border-blue-400"
        />
        <input 
            type="text" 
            placeholder="Value" 
            class="wizard-req-arg-value flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100 focus:outline-none focus:border-blue-400"
        />
        <button 
            onclick="window.wizardRemoveRequirementArg(${reqIdx}, ${argIdx})"
            type="button"
            class="px-2 py-1 bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300 text-xs"
        >
            ×
        </button>
    `;
    
    argsContainer.appendChild(argDiv);
}

/**
 * Remove an argument from a requirement and re-index remaining arguments
 */
export function wizardRemoveRequirementArg(reqIdx, argIdx) {
    const argsContainer = document.querySelector(`.wizard-req-args-container[data-req-idx="${reqIdx}"]`);
    if (!argsContainer) return;
    
    const argDiv = argsContainer.querySelector(`[data-arg-idx="${argIdx}"]`);
    if (argDiv) {
        argDiv.remove();
        
        // Re-index remaining arguments
        const remainingArgs = argsContainer.querySelectorAll('[data-arg-idx]');
        remainingArgs.forEach((div, newArgIdx) => {
            div.dataset.argIdx = newArgIdx;
            
            // Update the remove button onclick
            const removeBtn = div.querySelector('button[onclick*="wizardRemoveRequirementArg"]');
            if (removeBtn) {
                removeBtn.setAttribute('onclick', `window.wizardRemoveRequirementArg(${reqIdx}, ${newArgIdx})`);
            }
        });
    }
}
