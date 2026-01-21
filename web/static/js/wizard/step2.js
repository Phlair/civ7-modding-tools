/**
 * Wizard Step 2 - Core Civilization
 * Civilization traits, names, unlocks
 */

import { wizardData, markDirty } from '../state.js';
import { createWizardDropdown } from './wizard.js';

/**
 * Render Step 2: Core Civilization
 * @param {HTMLElement} container - Container element to render into
 */
export function renderWizardStep2(container) {
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
                                <button onclick="import('./wizard.js').then(m => m.showFieldHelp('civilization_type'))" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-civ-type" 
                                value="${wizardData.civilization?.civilization_type || ''}"
                                onchange="window.updateCivilization('civilization_type', this.value)"
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
                                onchange="window.updateWizardCivLocalization('name', this.value)"
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
                                onchange="window.updateWizardCivLocalization('adjective', this.value)"
                                placeholder="Babylonian"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div class="md:col-span-2">
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Civilization Icon Path
                                <button onclick="import('./wizard.js').then(m => m.showFieldHelp('civilization_icon'))" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-civ-icon" 
                                value="${wizardData.civilization?.icon?.path || ''}"
                                onchange="window.updateWizardIconPath(this.value)"
                                placeholder="icons/civ_sym_babylon"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                            <p class="text-xs text-slate-500 mt-1">Path to civilization icon (e.g., icons/civ_sym_iceni)</p>
                        </div>
                        <div class="md:col-span-2">
                            <label class="block text-sm font-medium text-slate-300 mb-1">
                                Description
                            </label>
                            <textarea 
                                id="wizard-civ-description" 
                                onchange="window.updateWizardCivLocalization('description', this.value)"
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
                        <button onclick="import('./wizard.js').then(m => m.showFieldHelp('trait_type'))" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                    </h4>
                    <div id="wizard-traits-container" class="space-y-2">
                        ${selectedTraits.map((trait, idx) => `
                            <div class="flex items-center gap-2" data-trait-idx="${idx}">
                                <select 
                                    id="wizard-trait-${idx}"
                                    onchange="window.updateWizardTraitAt(${idx}, this.value)"
                                    class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                >
                                    <option value="">Loading...</option>
                                </select>
                                <button 
                                    onclick="window.removeWizardTrait(${idx})"
                                    class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button 
                        onclick="window.addWizardTrait()"
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
                                    onchange="window.updateWizardCityAt(${idx}, this.value)"
                                    class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                    placeholder="City name"
                                />
                                <button 
                                    onclick="window.removeWizardCity(${idx})"
                                    class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                >
                                    ×
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button 
                        onclick="window.addWizardCity()"
                        class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                    >
                        + Add City
                    </button>
                    <p class="text-xs text-slate-500 mt-2">Names for your civilization's cities</p>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">Visual Styles</h4>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Building Culture Set</label>
                            <select 
                                id="wizard-building-culture" 
                                onchange="window.updateWizardBuildingCulture(this.value)"
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
                                onchange="window.updateWizardUnitCulture(this.value)"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select unit style...</option>
                            </select>
                            <p class="text-xs text-slate-500 mt-1">Visual style for your civilization's units</p>
                        </div>
                    </div>
                </div>
                
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
                                onchange="window.updateCivilization('start_bias_rivers', parseInt(this.value) || 0)"
                                placeholder="5"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                            <p class="text-xs text-slate-500 mt-1">Preference for starting near rivers (0-10)</p>
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="block text-sm font-medium text-slate-300">Terrain Preferences</label>
                                <button 
                                    onclick="window.addWizardTerrainBias()"
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
                                            onchange="window.updateWizardTerrainBiasAt(${idx}, 'terrain_type', this.value)"
                                            class="flex-1 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        >
                                            <option value="">Loading...</option>
                                        </select>
                                        <input 
                                            type="number" 
                                            value="${bias.score || ''}"
                                            onchange="window.updateWizardTerrainBiasAt(${idx}, 'score', parseInt(this.value) || 0)"
                                            placeholder="Score"
                                            class="w-20 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        />
                                        <button 
                                            onclick="window.removeWizardTerrainBias(${idx})"
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
                
                <details class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <summary class="font-semibold text-slate-200 cursor-pointer hover:text-slate-100">
                        🔄 Age Transitions (Optional)
                    </summary>
                    <div class="mt-4">
                        <div class="flex items-center justify-between mb-2">
                            <label class="block text-sm font-medium text-slate-300">Future Civilization Unlocks</label>
                            <button 
                                onclick="window.addWizardCivUnlock()"
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
                                                onchange="window.updateWizardCivUnlockAt(${idx}, 'age_type', this.value)"
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
                                                onchange="window.updateWizardCivUnlockAt(${idx}, 'type', this.value)"
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
                                            onchange="window.updateWizardCivUnlockAt(${idx}, 'type', this.value)"
                                            placeholder="LOC_CIVILIZATION_PERSIA_NAME"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                        />
                                    </div>
                                    <button 
                                        onclick="window.removeWizardCivUnlock(${idx})"
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

    selectedTraits.forEach((trait, idx) => {
        createWizardDropdown(`wizard-trait-${idx}`, 'civilization-traits', trait, 'Select trait...');
    });

    createWizardDropdown(
        'wizard-building-culture',
        'building-cultures',
        wizardData.civilization?.vis_art_building_cultures?.[0] || '',
        'Select building style...'
    );
    createWizardDropdown(
        'wizard-unit-culture',
        'unit-cultures',
        wizardData.civilization?.vis_art_unit_cultures?.[0] || '',
        'Select unit style...'
    );

    (wizardData.civilization?.start_bias_terrains || []).forEach((bias, idx) => {
        createWizardDropdown(`wizard-terrain-type-${idx}`, 'terrain-types', bias.terrain_type || '', 'Select terrain...');
    });

    (wizardData.civilization?.civilization_unlocks || []).forEach((unlock, idx) => {
        createWizardDropdown(`wizard-unlock-age-${idx}`, 'ages', unlock.age_type || '', 'Select age...');
    });
}

export function updateCivilization(field, value) {
    if (!wizardData.civilization) {
        wizardData.civilization = {};
    }
    wizardData.civilization[field] = value;
    markDirty();
}

export function updateWizardCivLocalization(field, value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.localizations) wizardData.civilization.localizations = [{}];
    wizardData.civilization.localizations[0][field] = value;
    markDirty();
}

export function updateWizardIconPath(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.icon) wizardData.civilization.icon = {};
    wizardData.civilization.icon.path = value;
    markDirty();
}

export function addWizardTrait() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.civilization_traits) wizardData.civilization.civilization_traits = [];
    wizardData.civilization.civilization_traits.push('');
    rerenderStep2();
    markDirty();
}

export function updateWizardTraitAt(idx, value) {
    if (wizardData.civilization?.civilization_traits) {
        wizardData.civilization.civilization_traits[idx] = value;
        markDirty();
    }
}

export function removeWizardTrait(idx) {
    if (wizardData.civilization?.civilization_traits) {
        wizardData.civilization.civilization_traits.splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

export function addWizardCity() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.localizations) wizardData.civilization.localizations = [{}];
    if (!wizardData.civilization.localizations[0].city_names) wizardData.civilization.localizations[0].city_names = [];
    wizardData.civilization.localizations[0].city_names.push('');
    rerenderStep2();
    markDirty();
}

export function updateWizardCityAt(idx, value) {
    if (wizardData.civilization?.localizations?.[0]?.city_names) {
        wizardData.civilization.localizations[0].city_names[idx] = value;
        markDirty();
    }
}

export function removeWizardCity(idx) {
    if (wizardData.civilization?.localizations?.[0]?.city_names) {
        wizardData.civilization.localizations[0].city_names.splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

export function updateWizardBuildingCulture(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    wizardData.civilization.vis_art_building_cultures = value ? [value] : [];
    markDirty();
}

export function updateWizardUnitCulture(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    wizardData.civilization.vis_art_unit_cultures = value ? [value] : [];
    markDirty();
}

export function addWizardTerrainBias() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.start_bias_terrains) wizardData.civilization.start_bias_terrains = [];
    wizardData.civilization.start_bias_terrains.push({ terrain_type: '', score: 0 });
    rerenderStep2();
    markDirty();
}

export function updateWizardTerrainBiasAt(idx, field, value) {
    if (wizardData.civilization?.start_bias_terrains?.[idx]) {
        wizardData.civilization.start_bias_terrains[idx][field] = value;
        markDirty();
    }
}

export function removeWizardTerrainBias(idx) {
    if (wizardData.civilization?.start_bias_terrains) {
        wizardData.civilization.start_bias_terrains.splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

export function addWizardCivUnlock() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.civilization_unlocks) wizardData.civilization.civilization_unlocks = [];
    wizardData.civilization.civilization_unlocks.push({
        age_type: '',
        type: '',
        kind: 'KIND_CIVILIZATION',
        name: '',
        description: '',
        icon: '',
    });
    rerenderStep2();
    markDirty();
}

export function updateWizardCivUnlockAt(idx, field, value) {
    if (wizardData.civilization?.civilization_unlocks?.[idx]) {
        wizardData.civilization.civilization_unlocks[idx][field] = value;
        markDirty();
    }
}

export function removeWizardCivUnlock(idx) {
    if (wizardData.civilization?.civilization_unlocks) {
        wizardData.civilization.civilization_unlocks.splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

function rerenderStep2() {
    const container = document.getElementById('wizard-step-content');
    if (container) {
        renderWizardStep2(container);
    }
}

// Expose all wizard functions to window for onclick handlers
if (typeof window !== 'undefined') {
    window.updateCivilization = updateCivilization;
    window.updateWizardCivLocalization = updateWizardCivLocalization;
    window.updateWizardIconPath = updateWizardIconPath;
    window.updateWizardBuildingCulture = updateWizardBuildingCulture;
    window.updateWizardUnitCulture = updateWizardUnitCulture;
    window.addWizardTrait = addWizardTrait;
    window.updateWizardTraitAt = updateWizardTraitAt;
    window.removeWizardTrait = removeWizardTrait;
    // Note: addWizardTag, removeWizardTag not implemented - tags handled differently in wizard
    window.addWizardCity = addWizardCity;
    window.updateWizardCityAt = updateWizardCityAt;
    window.removeWizardCity = removeWizardCity;
    // Note: addWizardBuilding, removeWizardBuilding, addWizardUnit, removeWizardUnit not in wizard  
    window.addWizardCivUnlock = addWizardCivUnlock;
    window.updateWizardCivUnlockAt = updateWizardCivUnlockAt;
    window.removeWizardCivUnlock = removeWizardCivUnlock;
    window.addWizardTerrainBias = addWizardTerrainBias;
    window.updateWizardTerrainBiasAt = updateWizardTerrainBiasAt;
    window.removeWizardTerrainBias = removeWizardTerrainBias;
    // Note: addWizardStartBiasTerrain, removeWizardStartBiasRiver, addWizardStartBiasRiver not implemented
}
