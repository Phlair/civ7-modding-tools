/**
 * Wizard Step 3 - Units & Buildings
 */

import { wizardData, wizardBuildingYields, markDirty } from '../state.js';
import { showToast } from '../ui.js';
import { createWizardDropdown, showFieldHelp } from './wizard.js';

/**
 * Render Step 3: Units & Buildings
 * @param {HTMLElement} container - Container element to render into
 */
export function renderWizardStep3(container) {
    const hasUnits = wizardData.units && wizardData.units.length > 0;
    const hasConstructibles = wizardData.constructibles && wizardData.constructibles.length > 0;
    
    // Ensure functions are available globally for onclick handlers
    if (typeof window !== 'undefined') {
        window.wizardShowUnitForm = wizardShowUnitForm;
        window.wizardEditUnit = wizardEditUnit;
        window.removeWizardUnit = removeWizardUnit;
        window.wizardShowConstructibleForm = wizardShowConstructibleForm;
        window.wizardEditConstructible = wizardEditConstructible;
        window.removeWizardConstructible = removeWizardConstructible;
        window.wizardSaveUnit = wizardSaveUnit;
        window.wizardCancelUnitForm = wizardCancelUnitForm;
        window.wizardSaveConstructible = wizardSaveConstructible;
        window.wizardCancelConstructibleForm = wizardCancelConstructibleForm;
        window.addWizardBuildingYield = addWizardBuildingYield;
        window.updateWizardBuildingYield = updateWizardBuildingYield;
        window.removeWizardBuildingYield = removeWizardBuildingYield;
        window.showFieldHelp = showFieldHelp;
    }

    container.innerHTML = `
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold mb-2 text-orange-400">⚔️ Step 3: Units & Buildings (Optional)</h3>
                <p class="text-slate-400 text-sm mb-6">Add unique units and buildings for your civilization. You can skip this step and add them later in Expert Mode.</p>
            </div>
            
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-orange-500"></span>
                        Unique Units (${wizardData.units?.length || 0})
                    </h4>
                    <button 
                        onclick="window.wizardShowUnitForm()"
                        class="px-3 py-1 bg-orange-600 hover:bg-orange-700 rounded text-sm font-medium"
                    >
                        + Add Unit
                    </button>
                </div>
                
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
                                        onclick="window.wizardEditUnit(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="window.removeWizardUnit(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No units added yet</p>'}
                
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
                                onclick="window.wizardSaveUnit()"
                                id="wizard-unit-form-save"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="window.wizardCancelUnitForm()"
                                id="wizard-unit-form-cancel"
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
                        <span class="inline-block w-2 h-2 rounded-full bg-emerald-500"></span>
                        Unique Buildings (${wizardData.constructibles?.length || 0})
                    </h4>
                    <button 
                        onclick="window.wizardShowConstructibleForm()"
                        class="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 rounded text-sm font-medium"
                    >
                        + Add Building
                    </button>
                </div>
                
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
                                        onclick="window.wizardEditConstructible(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="window.removeWizardConstructible(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No buildings added yet</p>'}
                
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
                        
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Yields & Bonuses (Optional)</summary>
                            <div class="p-3 pt-2 space-y-2">
                                <div class="flex items-center justify-between mb-2">
                                    <label class="block text-xs font-medium text-slate-300">Yield Bonuses</label>
                                    <button 
                                        onclick="window.addWizardBuildingYield()"
                                        type="button"
                                        class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                    >
                                        + Add Yield
                                    </button>
                                </div>
                                <div id="wizard-building-yields" class="space-y-2"></div>
                                <p class="text-xs text-slate-500 mt-2">Science, culture, production, etc.</p>
                            </div>
                        </details>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="window.wizardSaveConstructible()"
                                id="wizard-constructible-form-save"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="window.wizardCancelConstructibleForm()"
                                id="wizard-constructible-form-cancel"
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


/* attachStep3Listeners removed as we use inline onclick handlers */


export function wizardShowUnitForm() {
    const form = document.getElementById('wizard-unit-form');
    const idxInput = document.getElementById('wizard-unit-edit-idx');

    document.getElementById('wizard-unit-id').value = '';
    document.getElementById('wizard-unit-type').value = '';
    document.getElementById('wizard-unit-moves').value = '';
    document.getElementById('wizard-unit-sight').value = '';
    document.getElementById('wizard-unit-name').value = '';
    document.getElementById('wizard-unit-desc').value = '';
    document.getElementById('wizard-unit-icon').value = '';
    document.getElementById('wizard-unit-cost').value = '';
    idxInput.value = '-1';

    createWizardDropdown('wizard-unit-core-class', 'core-classes', '', 'Select core class...');
    createWizardDropdown('wizard-unit-domain', 'domains', '', 'Select domain...');
    createWizardDropdown('wizard-unit-formation', 'formation-classes', '', 'Select formation...');
    createWizardDropdown('wizard-unit-movement', 'unit-movement-classes', '', 'Select movement type...');
    createWizardDropdown('wizard-unit-cost-yield', 'yield-types', '', 'Select yield type...');

    form.classList.remove('hidden');
    document.getElementById('wizard-unit-id').focus();
}

export function wizardCancelUnitForm() {
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

export function wizardSaveUnit() {
    const id = document.getElementById('wizard-unit-id').value.trim();
    const type = document.getElementById('wizard-unit-type').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-unit-edit-idx').value, 10);

    if (!id) {
        showToast('Unit ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Unit Type is required', 'error');
        return;
    }

    if (!wizardData.units) {
        wizardData.units = [];
    }

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

    const unit = {
        id: id,
        unit_type: type,
        unit: {},
    };

    if (coreClass) unit.unit.core_class = coreClass;
    if (domain) unit.unit.domain = domain;
    if (formation) unit.unit.formation_class = formation;
    if (movement) unit.unit.unit_movement_class = movement;
    if (moves) unit.unit.base_moves = parseInt(moves, 10);
    if (sight) unit.unit.base_sight_range = parseInt(sight, 10);

    if (combat || rangedCombat || range) {
        unit.unit_stat = {};
        if (combat) unit.unit_stat.combat = parseInt(combat, 10);
        if (rangedCombat) unit.unit_stat.ranged_combat = parseInt(rangedCombat, 10);
        if (range) unit.unit_stat.range = parseInt(range, 10);
    }

    if (replacesUnit) {
        unit.unit_replace = {
            replaces_unit_type: replacesUnit,
        };
    }

    if (displayName || description) {
        unit.localizations = [{}];
        if (displayName) unit.localizations[0].name = displayName;
        if (description) unit.localizations[0].description = description;
    }

    if (icon) {
        unit.icon = { path: icon };
    }

    if (costYield && costAmount) {
        unit.unit_cost = {
            yield_type: costYield,
            cost: parseInt(costAmount, 10),
        };
    }

    if (editIdx >= 0) {
        wizardData.units[editIdx] = unit;
        showToast('Unit updated', 'success');
    } else {
        wizardData.units.push(unit);
        showToast('Unit added', 'success');
    }

    wizardCancelUnitForm();
    renderWizardStep3(document.getElementById('wizard-step-content'));
    markDirty();
}

export function wizardEditUnit(idx) {
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

    createWizardDropdown('wizard-unit-core-class', 'core-classes', unit.unit?.core_class || '', 'Select core class...');
    createWizardDropdown('wizard-unit-domain', 'domains', unit.unit?.domain || '', 'Select domain...');
    createWizardDropdown('wizard-unit-formation', 'formation-classes', unit.unit?.formation_class || '', 'Select formation...');
    createWizardDropdown('wizard-unit-movement', 'unit-movement-classes', unit.unit?.unit_movement_class || '', 'Select movement type...');
    createWizardDropdown('wizard-unit-cost-yield', 'yield-types', unit.unit_cost?.yield_type || '', 'Select yield type...');

    document.getElementById('wizard-unit-form').classList.remove('hidden');
}

export function removeWizardUnit(idx) {
    if (wizardData.units) {
        wizardData.units.splice(idx, 1);
        renderWizardStep3(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Unit removed', 'info');
    }
}

export function wizardShowConstructibleForm() {
    const form = document.getElementById('wizard-constructible-form');
    const idxInput = document.getElementById('wizard-constructible-edit-idx');

    document.getElementById('wizard-constructible-id').value = '';
    document.getElementById('wizard-constructible-type').value = '';
    document.getElementById('wizard-constructible-name').value = '';
    document.getElementById('wizard-constructible-desc').value = '';
    document.getElementById('wizard-constructible-icon').value = '';
    document.getElementById('wizard-constructible-districts').value = '';
    wizardBuildingYields.length = 0;
    renderWizardBuildingYields();
    idxInput.value = '-1';

    form.classList.remove('hidden');
    document.getElementById('wizard-constructible-id').focus();
}

export function wizardCancelConstructibleForm() {
    const form = document.getElementById('wizard-constructible-form');
    form.classList.add('hidden');
    document.getElementById('wizard-constructible-id').value = '';
    document.getElementById('wizard-constructible-type').value = '';
    document.getElementById('wizard-constructible-name').value = '';
    document.getElementById('wizard-constructible-desc').value = '';
    document.getElementById('wizard-constructible-icon').value = '';
    document.getElementById('wizard-constructible-districts').value = '';
    wizardBuildingYields.length = 0;
    document.getElementById('wizard-constructible-edit-idx').value = '-1';
}

export function wizardSaveConstructible() {
    const id = document.getElementById('wizard-constructible-id').value.trim();
    const type = document.getElementById('wizard-constructible-type').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-constructible-edit-idx').value, 10);

    if (!id) {
        showToast('Building ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Building Type is required', 'error');
        return;
    }

    if (!wizardData.constructibles) {
        wizardData.constructibles = [];
    }

    const displayName = document.getElementById('wizard-constructible-name').value.trim();
    const description = document.getElementById('wizard-constructible-desc').value.trim();
    const icon = document.getElementById('wizard-constructible-icon').value.trim();
    const districts = document.getElementById('wizard-constructible-districts').value.trim();

    const constructible = {
        id: id,
        constructible_type: type,
    };

    if (displayName || description) {
        constructible.localizations = [{}];
        if (displayName) constructible.localizations[0].name = displayName;
        if (description) constructible.localizations[0].description = description;
    }

    if (icon) {
        constructible.icon = { path: icon };
    }

    if (districts) {
        constructible.constructible_valid_districts = districts
            .split(',')
            .map(d => d.trim())
            .filter(d => d.length > 0);
    }

    if (wizardBuildingYields.length > 0) {
        constructible.yield_changes = wizardBuildingYields.filter(y => y.yield_type && y.yield_change);
    }

    if (editIdx >= 0) {
        wizardData.constructibles[editIdx] = constructible;
        showToast('Building updated', 'success');
    } else {
        wizardData.constructibles.push(constructible);
        showToast('Building added', 'success');
    }

    wizardCancelConstructibleForm();
    renderWizardStep3(document.getElementById('wizard-step-content'));
    markDirty();
}

export function wizardEditConstructible(idx) {
    const building = wizardData.constructibles[idx];
    document.getElementById('wizard-constructible-id').value = building.id || '';
    document.getElementById('wizard-constructible-type').value = building.constructible_type || '';
    document.getElementById('wizard-constructible-name').value = building.localizations?.[0]?.name || '';
    document.getElementById('wizard-constructible-desc').value = building.localizations?.[0]?.description || '';
    document.getElementById('wizard-constructible-icon').value = building.icon?.path || '';
    document.getElementById('wizard-constructible-districts').value = (building.constructible_valid_districts || []).join(', ');
    wizardBuildingYields.length = 0;
    wizardBuildingYields.push(...(building.yield_changes || []));
    renderWizardBuildingYields();
    document.getElementById('wizard-constructible-edit-idx').value = idx;
    document.getElementById('wizard-constructible-form').classList.remove('hidden');
}

export function removeWizardConstructible(idx) {
    if (wizardData.constructibles) {
        wizardData.constructibles.splice(idx, 1);
        renderWizardStep3(document.getElementById('wizard-step-content'));
        markDirty();
        showToast('Building removed', 'info');
    }
}

export function addWizardBuildingYield() {
    wizardBuildingYields.push({ yield_type: '', yield_change: 0 });
    renderWizardBuildingYields();
}

export function updateWizardBuildingYield(idx, field, value) {
    if (wizardBuildingYields[idx]) {
        wizardBuildingYields[idx][field] = field === 'yield_change' ? parseInt(value, 10) || 0 : value;
    }
}

export function removeWizardBuildingYield(idx) {
    wizardBuildingYields.splice(idx, 1);
    renderWizardBuildingYields();
}

export function renderWizardBuildingYields() {
    const container = document.getElementById('wizard-building-yields');
    if (!container) return;

    container.innerHTML = wizardBuildingYields.map((yieldItem, idx) => `
        <div class="flex gap-2 items-center">
            <select 
                id="wizard-yield-type-${idx}"
                onchange="window.updateWizardBuildingYield(${idx}, 'yield_type', this.value)"
                class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            >
                <option value="">Loading...</option>
            </select>
            <input 
                type="number" 
                value="${yieldItem.yield_change || ''}"
                onchange="window.updateWizardBuildingYield(${idx}, 'yield_change', this.value)"
                placeholder="Amount"
                class="w-24 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            />
            <button 
                onclick="window.removeWizardBuildingYield(${idx})"
                type="button"
                class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
            >
                ×
            </button>
        </div>
    `).join('');

    wizardBuildingYields.forEach((yieldItem, idx) => {
        createWizardDropdown(`wizard-yield-type-${idx}`, 'yield-types', yieldItem.yield_type || '', 'Select yield...');
    });
}
