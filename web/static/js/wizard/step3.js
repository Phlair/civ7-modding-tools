/**
 * Wizard Step 3 - Units & Buildings
 */

import { wizardData, wizardBuildingYields, markDirty } from '../state.js';
import { showToast } from '../ui.js';
import { createWizardDropdown, showFieldHelp } from './wizard.js';

// Additional arrays for building configuration
let wizardBuildingAdjacencies = [];
let wizardBuildingPlunders = [];
let wizardBuildingCostProgressions = [];
let wizardBuildingValidDistricts = [];
let wizardBuildingValidTerrains = [];
let wizardBuildingValidBiomes = [];
let wizardBuildingValidFeatures = [];

// Cache for reference data to avoid re-fetching
let cachedDistrictTypes = null;
let cachedTerrainTypes = null;
let cachedBiomeTypes = null;
let cachedFeatureTypes = null;

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
        window.wizardDuplicateUnit = wizardDuplicateUnit;
        window.removeWizardUnit = removeWizardUnit;
        window.updateUnitIconPath = updateUnitIconPath;
        window.wizardShowConstructibleForm = wizardShowConstructibleForm;
        window.wizardEditConstructible = wizardEditConstructible;
        window.removeWizardConstructible = removeWizardConstructible;
        window.updateBuildingIconPath = updateBuildingIconPath;
        window.wizardSaveUnit = wizardSaveUnit;
        window.wizardCancelUnitForm = wizardCancelUnitForm;
        window.wizardSaveConstructible = wizardSaveConstructible;
        window.wizardCancelConstructibleForm = wizardCancelConstructibleForm;
        window.addWizardBuildingYield = addWizardBuildingYield;
        window.updateWizardBuildingYield = updateWizardBuildingYield;
        window.removeWizardBuildingYield = removeWizardBuildingYield;
        window.addWizardBuildingAdjacency = addWizardBuildingAdjacency;
        window.updateWizardBuildingAdjacency = updateWizardBuildingAdjacency;
        window.removeWizardBuildingAdjacency = removeWizardBuildingAdjacency;
        window.addWizardBuildingPlunder = addWizardBuildingPlunder;
        window.updateWizardBuildingPlunder = updateWizardBuildingPlunder;
        window.removeWizardBuildingPlunder = removeWizardBuildingPlunder;
        window.setConstructibleIsBuilding = setConstructibleIsBuilding;
        window.showFieldHelp = showFieldHelp;
        window.populateVisualRemapDropdown = populateVisualRemapDropdown;
        window.populateConstructibleVisualRemapDropdown = populateConstructibleVisualRemapDropdown;
        window.toggleUnitReplacesCustom = toggleUnitReplacesCustom;
        window.toggleUnitUpgradeCustom = toggleUnitUpgradeCustom;
        window.addWizardBuildingDistrict = addWizardBuildingDistrict;
        window.updateWizardBuildingDistrict = updateWizardBuildingDistrict;
        window.removeWizardBuildingDistrict = removeWizardBuildingDistrict;
        window.addWizardBuildingTerrain = addWizardBuildingTerrain;
        window.updateWizardBuildingTerrain = updateWizardBuildingTerrain;
        window.removeWizardBuildingTerrain = removeWizardBuildingTerrain;
        window.addWizardBuildingBiome = addWizardBuildingBiome;
        window.updateWizardBuildingBiome = updateWizardBuildingBiome;
        window.removeWizardBuildingBiome = removeWizardBuildingBiome;
        window.addWizardBuildingFeature = addWizardBuildingFeature;
        window.updateWizardBuildingFeature = updateWizardBuildingFeature;
        window.removeWizardBuildingFeature = removeWizardBuildingFeature;
        window.wizardShowUniqueQuarterForm = wizardShowUniqueQuarterForm;
        window.wizardCancelUniqueQuarterForm = wizardCancelUniqueQuarterForm;
        window.wizardSaveUniqueQuarter = wizardSaveUniqueQuarter;
        window.wizardEditUniqueQuarter = wizardEditUniqueQuarter;
        window.removeWizardUniqueQuarter = removeWizardUniqueQuarter;
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
                                        onclick="window.wizardDuplicateUnit(${idx})"
                                        class="px-2 py-1 text-xs bg-green-600/30 hover:bg-green-600/50 border border-green-600 rounded text-green-300"
                                    >
                                        Duplicate
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
                        
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Icon *</label>
                            <div class="flex gap-2">
                                <input 
                                    type="text" 
                                    id="wizard-unit-icon" 
                                    placeholder="icons/units/unit_icon.png"
                                    onchange="window.updateUnitIconPath(this.value)"
                                    class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                />
                                <button 
                                    onclick="window.generateUnitIcon()"
                                    class="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium whitespace-nowrap transition-colors"
                                    title="Generate icon using AI"
                                >
                                    ✨
                                </button>
                            </div>
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
                                <div class="grid grid-cols-2 gap-2">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Tier</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-tier" 
                                            placeholder="1"
                                            min="1"
                                            max="3"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1">Unit tier (1-3)</p>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Maintenance</label>
                                        <input 
                                            type="number" 
                                            id="wizard-unit-maintenance" 
                                            placeholder="0"
                                            min="0"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1">Gold per turn</p>
                                    </div>
                                </div>
                                <div>
                                    <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-unit-zone-control"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span>Zone of Control</span>
                                    </label>
                                    <p class="text-xs text-slate-500 mt-1 ml-6">Restricts enemy movement adjacent to this unit</p>
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
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Summary Description</label>
                                    <textarea 
                                        id="wizard-unit-summary" 
                                        placeholder="Brief summary of unit's role and purpose"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                    <p class="text-xs text-slate-500 mt-1">Appears at top of unit card. Ability descriptions from base game abilities will be auto-appended.</p>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Historical Context (Optional)</label>
                                    <textarea 
                                        id="wizard-unit-historical" 
                                        placeholder="Historical background or lore about this unit"
                                        rows="3"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                    <p class="text-xs text-slate-500 mt-1">Separate historical/lore section shown below the summary.</p>
                                </div>
                            </div>
                        </div>
                        
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Cost (Optional)</summary>
                            <div class="p-3 pt-0 space-y-2">
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
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Cost Progression (Optional)</summary>
                            <div class="p-3 pt-0 space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost Progression Model</label>
                                    <select 
                                        id="wizard-unit-cost-progression-model" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">None</option>
                                        <option value="">Loading...</option>
                                    </select>
                                    <p class="text-xs text-slate-500 mt-1">Controls how costs increase per unit built</p>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost Increase Amount</label>
                                    <input 
                                        type="number" 
                                        id="wizard-unit-cost-progression-param" 
                                        placeholder="0"
                                        min="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                    <p class="text-xs text-slate-500 mt-1">Amount to increase cost by</p>
                                </div>
                            </div>
                        </details>
                        
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Advanced Properties (Optional)</summary>
                            <div class="p-3 pt-0 space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Promotion Class</label>
                                    <select 
                                        id="wizard-unit-promotion-class" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">None</option>
                                        <option value="">Loading...</option>
                                    </select>
                                    <p class="text-xs text-slate-500 mt-1">Determines available promotions</p>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Prerequisite Population</label>
                                    <input 
                                        type="number" 
                                        id="wizard-unit-prereq-population" 
                                        placeholder="0"
                                        min="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                    <p class="text-xs text-slate-500 mt-1">City population required to build this unit</p>
                                </div>
                                <div class="grid grid-cols-2 gap-2">
                                    <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-unit-can-train"
                                            checked
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span>Can Train</span>
                                    </label>
                                    <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-unit-can-purchase"
                                            checked
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span>Can Purchase</span>
                                    </label>
                                </div>
                                <div class="grid grid-cols-2 gap-2">
                                    <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-unit-can-earn-xp"
                                            checked
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span>Can Earn XP</span>
                                    </label>
                                    <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-unit-found-city"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span>Found City</span>
                                    </label>
                                </div>
                                <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                    <input 
                                        type="checkbox" 
                                        id="wizard-unit-make-trade-route"
                                        class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    />
                                    <span>Make Trade Route</span>
                                </label>
                            </div>
                            <div class="pt-2 border-t border-slate-700">
                                <label class="flex items-center space-x-2 text-xs font-medium text-slate-300">
                                    <input 
                                        type="checkbox" 
                                        id="wizard-unit-show-in-civ-picker"
                                        checked
                                        class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    />
                                    <span>Show in Civ Selection Screen</span>
                                </label>
                                <p class="text-xs text-slate-500 mt-1 ml-6">Uncheck to hide this unit from the civilization picker (useful for upgrade tiers)</p>
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
                                    <div class="flex items-center justify-between mb-1">
                                        <label class="block text-xs font-medium text-slate-300">Replaces Unit</label>
                                        <label class="flex items-center space-x-2 text-xs text-slate-400">
                                            <input 
                                                type="checkbox" 
                                                id="wizard-unit-replaces-custom-toggle"
                                                onchange="window.toggleUnitReplacesCustom(this.checked)"
                                                class="w-3 h-3 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                            />
                                            <span>Custom</span>
                                        </label>
                                    </div>
                                    <select 
                                        id="wizard-unit-replaces" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">None</option>
                                        <option value="">Loading...</option>
                                    </select>
                                    <input 
                                        type="text" 
                                        id="wizard-unit-replaces-custom" 
                                        placeholder="UNIT_CUSTOM_NAME"
                                        class="hidden w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                    <p class="text-xs text-slate-500 mt-1">Base game unit this replaces</p>
                                </div>
                                <div>
                                    <div class="flex items-center justify-between mb-1">
                                        <label class="block text-xs font-medium text-slate-300">Upgrades To</label>
                                        <label class="flex items-center space-x-2 text-xs text-slate-400">
                                            <input 
                                                type="checkbox" 
                                                id="wizard-unit-upgrade-custom-toggle"
                                                onchange="window.toggleUnitUpgradeCustom(this.checked)"
                                                class="w-3 h-3 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                            />
                                            <span>Custom</span>
                                        </label>
                                    </div>
                                    <select 
                                        id="wizard-unit-upgrade-to" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">None</option>
                                        <option value="">Loading...</option>
                                    </select>
                                    <input 
                                        type="text" 
                                        id="wizard-unit-upgrade-custom" 
                                        placeholder="UNIT_CUSTOM_NAME"
                                        class="hidden w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                    <p class="text-xs text-slate-500 mt-1">Next unit in upgrade chain</p>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Advisory Class</label>
                                    <select 
                                        id="wizard-unit-advisory" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">None</option>
                                        <option value="">Loading...</option>
                                    </select>
                                    <p class="text-xs text-slate-500 mt-1">Advisory category for AI and UI</p>
                                </div>
                            </div>
                        </details>
                        
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Tech/Civic Unlocks (Optional)</summary>
                            <div class="p-3 pt-2 space-y-3">
                                <div class="flex items-center space-x-2 mb-2">
                                    <input 
                                        type="checkbox" 
                                        id="wizard-unit-auto-infer-unlock"
                                        checked
                                        onchange="window.toggleUnitAutoInferUnlock(!this.checked)"
                                        class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                    />
                                    <label class="text-xs font-medium text-slate-300">Auto-infer unlock from replaced unit</label>
                                </div>
                                <p class="text-xs text-slate-500 -mt-2">When enabled, this unit will unlock at the same tech/civic as the unit it replaces. Disable to set custom unlock requirements.</p>
                                <div id="wizard-unit-custom-unlock-fields" class="space-y-2 hidden">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Unlock Tech</label>
                                        <select 
                                            id="wizard-unit-unlock-tech" 
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        >
                                            <option value="">None</option>
                                            <option value="">Loading...</option>
                                        </select>
                                        <p class="text-xs text-slate-500 mt-1">Technology that unlocks this unit</p>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Unlock Civic</label>
                                        <select 
                                            id="wizard-unit-unlock-civic" 
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        >
                                            <option value="">None</option>
                                            <option value="">Loading...</option>
                                        </select>
                                        <p class="text-xs text-slate-500 mt-1">Civic that unlocks this unit (overrides tech if both set)</p>
                                    </div>
                                </div>
                            </div>
                        </details>
                        
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Unit Abilities (Optional)</summary>
                            <div class="p-3 pt-2 space-y-3">
                                <p class="text-xs text-slate-500 mb-2">Add special abilities to this unit with passive bonuses, combat modifiers, or charged effects.</p>
                                
                                <!-- Abilities List -->
                                <div id="wizard-unit-abilities-list" class="space-y-2 mb-3"></div>
                                
                                <!-- Add Ability Button -->
                                <button 
                                    onclick="window.wizardShowAbilityForm()"
                                    class="w-full px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium"
                                >
                                    + Add Ability
                                </button>
                                
                                <!-- Ability Form (Hidden by default) -->
                                <div id="wizard-ability-form" class="hidden mt-3 p-3 bg-slate-800/50 rounded border border-slate-600 space-y-2">
                                    <input type="hidden" id="wizard-ability-edit-idx" value="-1" />
                                    
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Unique Ability ID *</label>
                                        <input 
                                            type="text" 
                                            id="wizard-ability-id" 
                                            placeholder="ABILITY_MY_UNIQUE_DRUID"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1">Unique identifier for this specific ability instance</p>
                                    </div>
                                    
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Ability Type *</label>
                                        <select 
                                            id="wizard-ability-type-select" 
                                            onchange="window.toggleAbilityCustomType(this.value === '__CUSTOM__')"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        >
                                            <option value="">Select existing ability...</option>
                                            <option value="__CUSTOM__">✨ Create Custom Ability</option>
                                        </select>
                                        <input 
                                            type="text" 
                                            id="wizard-ability-type-custom" 
                                            placeholder="ABILITY_MY_CUSTOM_UNIT"
                                            class="hidden w-full px-2 py-1 mt-2 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1" id="wizard-ability-type-help">Select an existing game ability or create a custom one</p>
                                    </div>
                                    
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Display Name *</label>
                                        <input 
                                            type="text" 
                                            id="wizard-ability-name" 
                                            placeholder="Phalanx Formation"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                    
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Description *</label>
                                        <textarea 
                                            id="wizard-ability-description" 
                                            placeholder="Gains +2 combat strength from each adjacent Hoplite"
                                            rows="2"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        ></textarea>
                                    </div>
                                    
                                    <div class="flex items-center space-x-2">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-ability-inactive"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <label class="text-xs font-medium text-slate-300">Inactive (auto-activate on unit creation)</label>
                                    </div>
                                    
                                    <div class="flex items-center space-x-2">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-ability-charged"
                                            onchange="document.getElementById('wizard-ability-recharge-div').classList.toggle('hidden', !this.checked)"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
                                        />
                                        <label class="text-xs font-medium text-slate-300">Charged Ability (limited uses)</label>
                                    </div>
                                    
                                    <div id="wizard-ability-recharge-div" class="hidden">
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Recharge Turns</label>
                                        <input 
                                            type="number" 
                                            id="wizard-ability-recharge-turns" 
                                            placeholder="5"
                                            min="1"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1">Number of turns between ability uses</p>
                                    </div>
                                    
                                    <div id="wizard-ability-modifiers-div">
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Modifier IDs (comma-separated)</label>
                                        <input 
                                            type="text" 
                                            id="wizard-ability-modifiers" 
                                            placeholder="HOPLITE_MOD_COMBAT_FROM_ADJACENT"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1" id="wizard-ability-modifiers-help">Optional: Only needed for custom abilities. Existing abilities already have their effects defined.</p>
                                    </div>
                                    
                                    <div class="flex gap-2 mt-3">
                                        <button 
                                            onclick="window.wizardSaveAbility()"
                                            class="flex-1 px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium"
                                        >
                                            Save Ability
                                        </button>
                                        <button 
                                            onclick="window.wizardCancelAbilityForm()"
                                            class="flex-1 px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs font-medium"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </details>
                        
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Visual Remap (Optional)</h6>
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Base Unit 3D Model</label>
                                <select 
                                    id="wizard-unit-visual-remap" 
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                >
                                    <option value="">Loading...</option>
                                </select>
                                <p class="text-xs text-slate-500 mt-1">Select an existing unit to reuse its 3D model. Available units are filtered by your civilization's starting age.</p>
                            </div>
                        </div>
                        
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
                        
                        <!-- Type Selector -->
                        <div class="bg-slate-900 p-3 rounded border border-slate-700">
                            <label class="block text-xs font-medium text-slate-300 mb-2">Constructible Type *</label>
                            <div class="flex gap-2">
                                <button 
                                    type="button"
                                    id="wizard-constructible-is-building-btn"
                                    onclick="window.setConstructibleIsBuilding(true)"
                                    class="flex-1 px-3 py-2 bg-blue-600 border border-blue-500 rounded text-sm font-medium transition-colors"
                                >
                                    Building
                                </button>
                                <button 
                                    type="button"
                                    id="wizard-constructible-is-improvement-btn"
                                    onclick="window.setConstructibleIsBuilding(false)"
                                    class="flex-1 px-3 py-2 bg-slate-700 border border-slate-600 rounded text-sm font-medium transition-colors"
                                >
                                    Improvement
                                </button>
                            </div>
                            <input type="hidden" id="wizard-constructible-is-building" value="true" />
                        </div>
                        
                        <h5 class="text-sm font-semibold text-emerald-400 border-b border-slate-600 pb-2 mb-3">Basic Information</h5>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">ID *</label>
                            <input 
                                type="text" 
                                id="wizard-constructible-id" 
                                placeholder="BUILDING_CIVILIZATION_NAME or IMPROVEMENT_CIVILIZATION_NAME"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Base Type *</label>
                            <input 
                                type="text" 
                                id="wizard-constructible-type" 
                                placeholder="BUILDING_LIBRARY or IMPROVEMENT_FARM"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                            <p class="text-xs text-slate-500 mt-1">The base game building/improvement this replaces or extends</p>
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
                                        placeholder="Royal Library"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                    <textarea 
                                        id="wizard-constructible-desc" 
                                        placeholder="Provides +2 Science and +1 Culture per adjacent Campus district."
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Tooltip (Optional)</label>
                                    <textarea 
                                        id="wizard-constructible-tooltip" 
                                        placeholder="Additional gameplay information"
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Icon -->
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Icon Path</label>
                            <div class="flex gap-2">
                                <input 
                                    type="text" 
                                    id="wizard-constructible-icon" 
                                    placeholder="fs://game/mod_id/icon_building_name.png"
                                    onchange="window.updateBuildingIconPath(this.value)"
                                    class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                />
                                <button 
                                    onclick="window.generateBuildingIcon()"
                                    class="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium whitespace-nowrap transition-colors"
                                    title="Generate icon using AI"
                                >
                                    ✨ AI
                                </button>
                            </div>
                        </div>
                        
                        <!-- Visual Remap -->
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Visual Remap (Optional)</h6>
                            <div>
                                <label class="block text-xs font-medium text-slate-300 mb-1">Use Visuals From</label>
                                <select 
                                    id="wizard-constructible-visual-remap" 
                                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                >
                                    <option value="">None (custom or default visuals)</option>
                                </select>
                                <p class="text-xs text-slate-500 mt-1">Use visuals from an existing base game building/improvement</p>
                            </div>
                        </div>
                        
                        <!-- Placement Constraints -->
                        <details class="bg-slate-900/50 rounded border border-slate-700" open>
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">📍 Placement Constraints</summary>
                            <div class="p-3 pt-2 space-y-3">
                                <div id="wizard-constructible-district-section">
                                    <div class="flex items-center justify-between mb-2">
                                        <label class="block text-xs font-medium text-slate-300">Valid Districts (Building Only)</label>
                                        <button 
                                            onclick="window.addWizardBuildingDistrict()"
                                            type="button"
                                            class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                        >
                                            + Add District
                                        </button>
                                    </div>
                                    <div id="wizard-building-districts" class="space-y-2"></div>
                                    <p class="text-xs text-slate-500 mt-1">Districts where this building can be constructed</p>
                                </div>
                                <div>
                                    <div class="flex items-center justify-between mb-2">
                                        <label class="block text-xs font-medium text-slate-300">Valid Terrains</label>
                                        <button 
                                            onclick="window.addWizardBuildingTerrain()"
                                            type="button"
                                            class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                        >
                                            + Add Terrain
                                        </button>
                                    </div>
                                    <div id="wizard-building-terrains" class="space-y-2"></div>
                                </div>
                                <div>
                                    <div class="flex items-center justify-between mb-2">
                                        <label class="block text-xs font-medium text-slate-300">Valid Biomes</label>
                                        <button 
                                            onclick="window.addWizardBuildingBiome()"
                                            type="button"
                                            class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                        >
                                            + Add Biome
                                        </button>
                                    </div>
                                    <div id="wizard-building-biomes" class="space-y-2"></div>
                                </div>
                                <div>
                                    <div class="flex items-center justify-between mb-2">
                                        <label class="block text-xs font-medium text-slate-300">Valid Features</label>
                                        <button 
                                            onclick="window.addWizardBuildingFeature()"
                                            type="button"
                                            class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                        >
                                            + Add Feature
                                        </button>
                                    </div>
                                    <div id="wizard-building-features" class="space-y-2"></div>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">River Placement</label>
                                    <select 
                                        id="wizard-constructible-river" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">No requirement</option>
                                    </select>
                                </div>
                            </div>
                        </details>
                        
                        <!-- Yields & Maintenance -->
                        <details class="bg-slate-900/50 rounded border border-slate-700" open>
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">📊 Yields & Maintenance</summary>
                            <div class="p-3 pt-2 space-y-3">
                                <div>
                                    <div class="flex items-center justify-between mb-2">
                                        <label class="block text-xs font-medium text-slate-300">Base Yields</label>
                                        <button 
                                            onclick="window.addWizardBuildingYield()"
                                            type="button"
                                            class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                        >
                                            + Add Yield
                                        </button>
                                    </div>
                                    <div id="wizard-building-yields" class="space-y-2"></div>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Gold Maintenance</label>
                                    <input 
                                        type="number" 
                                        id="wizard-constructible-maintenance-gold" 
                                        placeholder="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Happiness Maintenance</label>
                                    <input 
                                        type="number" 
                                        id="wizard-constructible-maintenance-happiness" 
                                        placeholder="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                            </div>
                        </details>
                        
                        <!-- Adjacency Bonuses -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">🔗 Adjacency Bonuses</summary>
                            <div class="p-3 pt-2 space-y-2">
                                <div class="flex items-center justify-between mb-2">
                                    <label class="block text-xs font-medium text-slate-300">Adjacency Patterns</label>
                                    <button 
                                        onclick="window.addWizardBuildingAdjacency()"
                                        type="button"
                                        class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                    >
                                        + Add Adjacency
                                    </button>
                                </div>
                                <div id="wizard-building-adjacencies" class="space-y-2"></div>
                                <p class="text-xs text-slate-500 mt-2">Bonuses from adjacent tiles (wonders, rivers, districts, etc.)</p>
                            </div>
                        </details>
                        
                        <!-- Plunder & Costs -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">💰 Plunder & Costs</summary>
                            <div class="p-3 pt-2 space-y-3">
                                <div>
                                    <div class="flex items-center justify-between mb-2">
                                        <label class="block text-xs font-medium text-slate-300">Plunder Rewards</label>
                                        <button 
                                            onclick="window.addWizardBuildingPlunder()"
                                            type="button"
                                            class="px-2 py-1 bg-green-600 hover:bg-green-700 rounded text-xs font-medium"
                                        >
                                            + Add Plunder
                                        </button>
                                    </div>
                                    <div id="wizard-building-plunders" class="space-y-2"></div>
                                    <p class="text-xs text-slate-500 mt-1">Rewards when pillaged by enemies</p>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost Progression (%)</label>
                                    <input 
                                        type="number" 
                                        id="wizard-constructible-cost-progression" 
                                        placeholder="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                    <p class="text-xs text-slate-500 mt-1">Percentage increase per copy (e.g., 15 = 15% more expensive each time)</p>
                                </div>
                            </div>
                        </details>
                        
                        <!-- Advanced Properties -->
                        <details class="bg-slate-900/50 rounded border border-slate-700">
                            <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">⚙️ Advanced Properties</summary>
                            <div class="p-3 pt-2 space-y-3">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Age <span class="text-slate-500 text-xs">(auto-set from civ)</span></label>
                                    <select 
                                        id="wizard-constructible-age" 
                                        disabled
                                        class="w-full px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm text-slate-400 cursor-not-allowed"
                                    >
                                        <option value="">Auto</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost Progression Model</label>
                                    <select 
                                        id="wizard-constructible-cost-model" 
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    >
                                        <option value="">No progression model</option>
                                    </select>
                                    <input 
                                        type="text" 
                                        id="wizard-constructible-cost-model-text" 
                                        placeholder="COST_PROGRESSION_BUILDING_LINEAR" 
                                        style="display:none;"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">District Defense Bonus</label>
                                    <input 
                                        type="number" 
                                        id="wizard-constructible-district-defense" 
                                        placeholder="0"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div class="space-y-2">
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-requires-unlock"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Requires Unlock</span>
                                    </label>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-immune-damage"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Immune to Damage</span>
                                    </label>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-repairable"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Repairable</span>
                                    </label>
                                </div>
                                
                                <!-- Building-specific -->
                                <div id="wizard-constructible-building-section" class="space-y-2 pt-2 border-t border-slate-700">
                                    <h6 class="text-xs font-semibold text-slate-400">Building-Specific</h6>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-purchasable"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Purchasable with Gold</span>
                                    </label>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-multiple-per-city"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Multiple Per City</span>
                                    </label>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Town</label>
                                        <input 
                                            type="text" 
                                            id="wizard-constructible-town" 
                                            placeholder="TOWN_PLACEHOLDER"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                    </div>
                                </div>
                                
                                <!-- Improvement-specific -->
                                <div id="wizard-constructible-improvement-section" class="hidden space-y-2 pt-2 border-t border-slate-700">
                                    <h6 class="text-xs font-semibold text-slate-400">Improvement-Specific</h6>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Trait Type <span class="text-slate-500 text-xs">(auto-set from civ)</span></label>
                                        <input 
                                            type="text"
                                            id="wizard-constructible-trait-type"
                                            disabled
                                            placeholder="Auto"
                                            class="w-full px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm text-slate-400 cursor-not-allowed"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Unit Healing Bonus</label>
                                        <input 
                                            type="number" 
                                            id="wizard-constructible-unit-healing"
                                            placeholder="5"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                        />
                                        <p class="text-xs text-slate-500 mt-1">Healing per turn for military units on this tile (e.g., 5 for Pairidaeza)</p>
                                    </div>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-city-buildable"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">City Buildable</span>
                                    </label>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-one-per-settlement"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">One Per Settlement</span>
                                    </label>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-same-adjacent-valid"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Can Be Built Next to Same Type</span>
                                    </label>
                                    <label class="flex items-center gap-2 cursor-pointer">
                                        <input 
                                            type="checkbox" 
                                            id="wizard-constructible-ageless"
                                            class="w-4 h-4 bg-slate-700 border border-slate-600 rounded focus:ring-2 focus:ring-blue-400"
                                        />
                                        <span class="text-xs text-slate-300">Ageless <span class="text-slate-500">(available in all ages + adds AGELESS tag)</span></span>
                                    </label>
                                </div>
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
            
            <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                        <span class="inline-block w-2 h-2 rounded-full bg-purple-500"></span>
                        Unique Quarters (${wizardData.unique_quarters?.length || 0})
                    </h4>
                    ${(wizardData.constructibles?.filter(c => c.constructible?.constructible_class === 'BUILDING' || c.is_building !== false).length >= 2) ? `
                        <button 
                            onclick="window.wizardShowUniqueQuarterForm()"
                            class="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium"
                        >
                            + Create Quarter
                        </button>
                    ` : `
                        <p class="text-xs text-slate-400">Add 2+ buildings first</p>
                    `}
                </div>
                
                ${wizardData.unique_quarters && wizardData.unique_quarters.length > 0 ? `
                    <div class="space-y-2 mb-4">
                        ${wizardData.unique_quarters.map((quarter, idx) => `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600">
                                <div class="flex items-center justify-between mb-2">
                                    <div>
                                        <p class="font-medium text-sm">${quarter.id || 'Unnamed Quarter'}</p>
                                        <p class="text-xs text-slate-400">${quarter.unique_quarter_type || '—'}</p>
                                    </div>
                                    <div class="flex gap-2">
                                        <button 
                                            onclick="window.wizardEditUniqueQuarter(${idx})"
                                            class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                        >
                                            Edit
                                        </button>
                                        <button 
                                            onclick="window.removeWizardUniqueQuarter(${idx})"
                                            class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                                <div class="flex gap-2 text-xs text-slate-400">
                                    <span>🏛️ ${quarter.building_type_1 || 'Building 1'}</span>
                                    <span>+</span>
                                    <span>🏛️ ${quarter.building_type_2 || 'Building 2'}</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No unique quarters created yet. Combine 2 buildings to create one!</p>'}
                
                <div id="wizard-unique-quarter-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                    <div class="space-y-3">
                        <input type="hidden" id="wizard-unique-quarter-edit-idx" value="-1" />
                        
                        <h5 class="text-sm font-semibold text-purple-400 border-b border-slate-600 pb-2 mb-3">Create Unique Quarter</h5>
                        
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <p class="text-xs text-slate-400 mb-3">
                                Unique Quarters combine 2 buildings into a special district that provides bonus effects when both are built in the same city.
                            </p>
                        </div>
                        
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Quarter ID *</label>
                            <input 
                                type="text" 
                                id="wizard-unique-quarter-id" 
                                placeholder="QUARTER_CIVILIZATION_NAME"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Quarter Type *</label>
                            <input 
                                type="text" 
                                id="wizard-unique-quarter-type" 
                                placeholder="QUARTER_TYPE_ID"
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">First Building *</label>
                            <select 
                                id="wizard-unique-quarter-building1" 
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select building...</option>
                            </select>
                        </div>
                        
                        <div>
                            <label class="block text-xs font-medium text-slate-300 mb-1">Second Building *</label>
                            <select 
                                id="wizard-unique-quarter-building2" 
                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select building...</option>
                            </select>
                        </div>
                        
                        <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                            <h6 class="text-xs font-semibold text-slate-400 mb-2">Localization</h6>
                            <div class="space-y-2">
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Display Name</label>
                                    <input 
                                        type="text" 
                                        id="wizard-unique-quarter-name" 
                                        placeholder="Royal Academy"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    />
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                                    <textarea 
                                        id="wizard-unique-quarter-desc" 
                                        placeholder="A prestigious district combining academic and cultural institutions."
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                                <div>
                                    <label class="block text-xs font-medium text-slate-300 mb-1">Tooltip (Optional)</label>
                                    <textarea 
                                        id="wizard-unique-quarter-tooltip" 
                                        placeholder="Additional effects and bonuses..."
                                        rows="2"
                                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                                    ></textarea>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex gap-2 mt-4">
                            <button 
                                onclick="window.wizardSaveUniqueQuarter()"
                                id="wizard-unique-quarter-form-save"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="window.wizardCancelUniqueQuarterForm()"
                                id="wizard-unique-quarter-form-cancel"
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
    document.getElementById('wizard-unit-summary').value = '';
    document.getElementById('wizard-unit-historical').value = '';
    document.getElementById('wizard-unit-icon').value = '';
    document.getElementById('wizard-unit-cost').value = '';
    idxInput.value = '-1';

    createWizardDropdown('wizard-unit-core-class', 'core-classes', '', 'Select core class...');
    createWizardDropdown('wizard-unit-domain', 'domains', '', 'Select domain...');
    createWizardDropdown('wizard-unit-formation', 'formation-classes', '', 'Select formation...');
    createWizardDropdown('wizard-unit-movement', 'unit-movement-classes', '', 'Select movement type...');
    createWizardDropdown('wizard-unit-cost-yield', 'yield-types', '', 'Select yield type...');
    createWizardDropdown('wizard-unit-cost-progression-model', 'cost-progression-models', '', 'None');
    createWizardDropdown('wizard-unit-promotion-class', 'promotion-classes', '', 'None');
    createWizardDropdown('wizard-unit-replaces', 'units', '', 'None');
    // Reset replaces custom fields
    document.getElementById('wizard-unit-replaces-custom').value = '';
    document.getElementById('wizard-unit-replaces-custom-toggle').checked = false;
    toggleUnitReplacesCustom(false);
    createWizardDropdown('wizard-unit-upgrade-to', 'units', '', 'None');
    // Reset upgrade custom fields
    document.getElementById('wizard-unit-upgrade-custom').value = '';
    document.getElementById('wizard-unit-upgrade-custom-toggle').checked = false;
    toggleUnitUpgradeCustom(false);
    createWizardDropdown('wizard-unit-advisory', 'advisory-class-types', '', 'None');
    populateVisualRemapDropdown('');
    // Reset unlock fields
    document.getElementById('wizard-unit-auto-infer-unlock').checked = true;
    createWizardDropdown('wizard-unit-unlock-tech', 'progression-trees', '', 'None');
    createWizardDropdown('wizard-unit-unlock-civic', 'progression-trees', '', 'None');
    toggleUnitAutoInferUnlock(false);
    // Reset civ picker visibility
    document.getElementById('wizard-unit-show-in-civ-picker').checked = true;
    // Reset abilities
    wizardUnitCurrentAbilities = [];
    renderWizardUnitAbilitiesList();

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
    document.getElementById('wizard-unit-tier').value = '';
    document.getElementById('wizard-unit-maintenance').value = '';
    document.getElementById('wizard-unit-zone-control').checked = false;
    document.getElementById('wizard-unit-promotion-class').value = '';
    document.getElementById('wizard-unit-cost-progression-model').value = '';
    document.getElementById('wizard-unit-cost-progression-param').value = '';
    document.getElementById('wizard-unit-prereq-population').value = '';
    document.getElementById('wizard-unit-can-train').checked = true;
    document.getElementById('wizard-unit-can-purchase').checked = true;
    document.getElementById('wizard-unit-can-earn-xp').checked = true;
    document.getElementById('wizard-unit-found-city').checked = false;
    document.getElementById('wizard-unit-make-trade-route').checked = false;
    document.getElementById('wizard-unit-name').value = '';
    document.getElementById('wizard-unit-summary').value = '';
    document.getElementById('wizard-unit-historical').value = '';
    document.getElementById('wizard-unit-icon').value = '';
    document.getElementById('wizard-unit-cost-yield').value = '';
    document.getElementById('wizard-unit-cost').value = '';
    document.getElementById('wizard-unit-combat').value = '';
    document.getElementById('wizard-unit-ranged-combat').value = '';
    document.getElementById('wizard-unit-range').value = '';
    document.getElementById('wizard-unit-replaces').value = '';
    document.getElementById('wizard-unit-replaces-custom').value = '';
    document.getElementById('wizard-unit-replaces-custom-toggle').checked = false;
    toggleUnitReplacesCustom(false);
    document.getElementById('wizard-unit-upgrade-to').value = '';
    document.getElementById('wizard-unit-upgrade-custom').value = '';
    document.getElementById('wizard-unit-upgrade-custom-toggle').checked = false;
    toggleUnitUpgradeCustom(false);
    document.getElementById('wizard-unit-advisory').value = '';
    document.getElementById('wizard-unit-auto-infer-unlock').checked = true;
    document.getElementById('wizard-unit-unlock-tech').value = '';
    document.getElementById('wizard-unit-unlock-civic').value = '';
    toggleUnitAutoInferUnlock(false);
    document.getElementById('wizard-unit-show-in-civ-picker').checked = true;
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
    const tier = document.getElementById('wizard-unit-tier').value;
    const maintenance = document.getElementById('wizard-unit-maintenance').value;
    const zoneOfControl = document.getElementById('wizard-unit-zone-control').checked;
    const promotionClass = document.getElementById('wizard-unit-promotion-class').value.trim();
    const costProgressionModel = document.getElementById('wizard-unit-cost-progression-model').value.trim();
    const costProgressionParam = document.getElementById('wizard-unit-cost-progression-param').value;
    const prereqPopulation = document.getElementById('wizard-unit-prereq-population').value;
    const canTrain = document.getElementById('wizard-unit-can-train').checked;
    const canPurchase = document.getElementById('wizard-unit-can-purchase').checked;
    const canEarnXp = document.getElementById('wizard-unit-can-earn-xp').checked;
    const foundCity = document.getElementById('wizard-unit-found-city').checked;
    const makeTradeRoute = document.getElementById('wizard-unit-make-trade-route').checked;
    const displayName = document.getElementById('wizard-unit-name').value.trim();
    const summaryDesc = document.getElementById('wizard-unit-summary').value.trim();
    const historicalDesc = document.getElementById('wizard-unit-historical').value.trim();
    const icon = document.getElementById('wizard-unit-icon').value.trim();
    const costYield = document.getElementById('wizard-unit-cost-yield').value.trim();
    const costAmount = document.getElementById('wizard-unit-cost').value;
    const combat = document.getElementById('wizard-unit-combat').value;
    const rangedCombat = document.getElementById('wizard-unit-ranged-combat').value;
    const range = document.getElementById('wizard-unit-range').value;
    // Get replaces value from either custom input or dropdown
    const replacesCustomToggle = document.getElementById('wizard-unit-replaces-custom-toggle').checked;
    const replacesUnit = replacesCustomToggle 
        ? document.getElementById('wizard-unit-replaces-custom').value.trim()
        : document.getElementById('wizard-unit-replaces').value.trim();
    // Get upgrade value from either custom input or dropdown
    const upgradeCustomToggle = document.getElementById('wizard-unit-upgrade-custom-toggle').checked;
    const upgradeToUnit = upgradeCustomToggle
        ? document.getElementById('wizard-unit-upgrade-custom').value.trim()
        : document.getElementById('wizard-unit-upgrade-to').value.trim();
    const advisory = document.getElementById('wizard-unit-advisory').value.trim();
    const visualRemapBase = document.getElementById('wizard-unit-visual-remap').value.trim();
    const autoInferUnlock = document.getElementById('wizard-unit-auto-infer-unlock').checked;
    const unlockTech = document.getElementById('wizard-unit-unlock-tech').value.trim();
    const unlockCivic = document.getElementById('wizard-unit-unlock-civic').value.trim();
    const showInCivPicker = document.getElementById('wizard-unit-show-in-civ-picker').checked;

    const unit = {
        id: id,
        unit_type: type,
        unit: {},
    };

    if (coreClass) unit.unit.core_class = coreClass;
    if (domain) unit.unit.domain = domain;
    if (formation) unit.unit.formation_class = formation;
    if (movement) unit.unit.unit_movement_class = movement;
    // Always set moves and sight with defaults if not provided
    unit.unit.base_moves = moves ? parseInt(moves, 10) : 2;
    unit.unit.base_sight_range = sight ? parseInt(sight, 10) : 2;
    
    // New properties
    if (tier) unit.unit.tier = parseInt(tier, 10);
    if (maintenance) unit.unit.maintenance = parseInt(maintenance, 10);
    if (zoneOfControl) unit.unit.zone_of_control = true;
    if (promotionClass) unit.unit.promotion_class = promotionClass;
    if (costProgressionModel) unit.unit.cost_progression_model = costProgressionModel;
    if (costProgressionParam) unit.unit.cost_progression_param1 = parseInt(costProgressionParam, 10);
    if (prereqPopulation) unit.unit.prereq_population = parseInt(prereqPopulation, 10);
    if (!canTrain) unit.unit.can_train = false;
    if (!canPurchase) unit.unit.can_purchase = false;
    if (!canEarnXp) unit.unit.can_earn_experience = false;
    if (foundCity) unit.unit.found_city = true;
    if (makeTradeRoute) unit.unit.make_trade_route = true;
    
    // Set trait_type from civilization (required for unique units)
    if (wizardData.civilization?.civilization_traits && wizardData.civilization.civilization_traits.length > 0) {
        // Use the first civilization trait (typically the main civ trait like TRAIT_BABYLON)
        const civTrait = wizardData.civilization.civilization_traits.find(t => !t.startsWith('TRAIT_ANTIQUITY') && !t.startsWith('TRAIT_ATTRIBUTE'));
        if (civTrait) {
            unit.unit.trait_type = civTrait;
        }
    }

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

    if (upgradeToUnit) {
        unit.unit_upgrade = {
            upgrade_unit: upgradeToUnit,
        };
    }

    if (advisory) {
        unit.unit_advisories = [{
            advisory_class_type: advisory,
        }];
    }

    // Tech/Civic unlock configuration
    if (autoInferUnlock !== undefined) {
        unit.auto_infer_unlock = autoInferUnlock;
    }
    if (unlockTech) {
        unit.unlock_tech = unlockTech;
    }
    if (unlockCivic) {
        unit.unlock_civic = unlockCivic;
    }
    
    // Civ picker visibility
    if (showInCivPicker !== undefined) {
        unit.show_in_civ_picker = showInCivPicker;
    }
    
    // Unit abilities
    if (wizardUnitCurrentAbilities && wizardUnitCurrentAbilities.length > 0) {
        unit.unit_abilities = wizardUnitCurrentAbilities;
    }

    if (visualRemapBase) {
        unit.visual_remap = {
            to: visualRemapBase,
        };
    }

    if (displayName || summaryDesc || historicalDesc) {
        unit.localizations = [{}];
        if (displayName) unit.localizations[0].name = displayName;
        if (summaryDesc) unit.localizations[0].summary_description = summaryDesc;
        if (historicalDesc) unit.localizations[0].historical_description = historicalDesc;
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

export async function wizardEditUnit(idx) {
    const unit = wizardData.units[idx];
    document.getElementById('wizard-unit-id').value = unit.id || '';
    document.getElementById('wizard-unit-type').value = unit.unit_type || '';
    document.getElementById('wizard-unit-moves').value = unit.unit?.base_moves || '';
    document.getElementById('wizard-unit-sight').value = unit.unit?.base_sight_range || '';
    document.getElementById('wizard-unit-tier').value = unit.unit?.tier || '';
    document.getElementById('wizard-unit-maintenance').value = unit.unit?.maintenance || '';
    document.getElementById('wizard-unit-zone-control').checked = unit.unit?.zone_of_control || false;
    document.getElementById('wizard-unit-promotion-class').value = unit.unit?.promotion_class || '';
    document.getElementById('wizard-unit-cost-progression-param').value = unit.unit?.cost_progression_param1 || '';
    document.getElementById('wizard-unit-prereq-population').value = unit.unit?.prereq_population || '';
    document.getElementById('wizard-unit-can-train').checked = unit.unit?.can_train !== false;
    document.getElementById('wizard-unit-can-purchase').checked = unit.unit?.can_purchase !== false;
    document.getElementById('wizard-unit-can-earn-xp').checked = unit.unit?.can_earn_experience !== false;
    document.getElementById('wizard-unit-found-city').checked = unit.unit?.found_city || false;
    document.getElementById('wizard-unit-make-trade-route').checked = unit.unit?.make_trade_route || false;
    document.getElementById('wizard-unit-show-in-civ-picker').checked = unit.show_in_civ_picker !== false;
    document.getElementById('wizard-unit-name').value = unit.localizations?.[0]?.name || '';
    document.getElementById('wizard-unit-summary').value = unit.localizations?.[0]?.summary_description || unit.localizations?.[0]?.description || '';
    document.getElementById('wizard-unit-historical').value = unit.localizations?.[0]?.historical_description || '';
    document.getElementById('wizard-unit-icon').value = unit.icon?.path || '';
    document.getElementById('wizard-unit-cost').value = unit.unit_cost?.cost || '';
    document.getElementById('wizard-unit-combat').value = unit.unit_stat?.combat || '';
    document.getElementById('wizard-unit-ranged-combat').value = unit.unit_stat?.ranged_combat || '';
    document.getElementById('wizard-unit-range').value = unit.unit_stat?.range || '';
    document.getElementById('wizard-unit-replaces').value = unit.unit_replace?.replaces_unit_type || '';
    document.getElementById('wizard-unit-upgrade-to').value = unit.unit_upgrade?.upgrade_unit || '';
    document.getElementById('wizard-unit-advisory').value = unit.unit_advisories?.[0]?.advisory_class_type || '';
    document.getElementById('wizard-unit-edit-idx').value = idx;

    createWizardDropdown('wizard-unit-core-class', 'core-classes', unit.unit?.core_class || '', 'Select core class...');
    createWizardDropdown('wizard-unit-domain', 'domains', unit.unit?.domain || '', 'Select domain...');
    createWizardDropdown('wizard-unit-formation', 'formation-classes', unit.unit?.formation_class || '', 'Select formation...');
    createWizardDropdown('wizard-unit-movement', 'unit-movement-classes', unit.unit?.unit_movement_class || '', 'Select movement type...');
    createWizardDropdown('wizard-unit-cost-yield', 'yield-types', unit.unit_cost?.yield_type || '', 'Select yield type...');
    createWizardDropdown('wizard-unit-cost-progression-model', 'cost-progression-models', unit.unit?.cost_progression_model || '', 'None');
    createWizardDropdown('wizard-unit-promotion-class', 'promotion-classes', unit.unit?.promotion_class || '', 'None');
    
    // Handle replaces - check if it's a known unit or custom
    const replacesValue = unit.unit_replace?.replaces_unit_type || '';
    await createWizardDropdown('wizard-unit-replaces', 'units', replacesValue, 'None');
    // If value wasn't found in dropdown, it's custom
    const replacesDropdown = document.getElementById('wizard-unit-replaces');
    const isReplacesCustom = replacesValue && replacesDropdown.value !== replacesValue;
    if (isReplacesCustom) {
        document.getElementById('wizard-unit-replaces-custom').value = replacesValue;
        document.getElementById('wizard-unit-replaces-custom-toggle').checked = true;
        toggleUnitReplacesCustom(true);
    }
    
    // Handle upgrade - check if it's a known unit or custom
    const upgradeValue = unit.unit_upgrade?.upgrade_unit || '';
    await createWizardDropdown('wizard-unit-upgrade-to', 'units', upgradeValue, 'None');
    // If value wasn't found in dropdown, it's custom
    const upgradeDropdown = document.getElementById('wizard-unit-upgrade-to');
    const isUpgradeCustom = upgradeValue && upgradeDropdown.value !== upgradeValue;
    if (isUpgradeCustom) {
        document.getElementById('wizard-unit-upgrade-custom').value = upgradeValue;
        document.getElementById('wizard-unit-upgrade-custom-toggle').checked = true;
        toggleUnitUpgradeCustom(true);
    }
    
    createWizardDropdown('wizard-unit-advisory', 'advisory-class-types', unit.unit_advisories?.[0]?.advisory_class_type || '', 'None');
    await populateVisualRemapDropdown(unit.visual_remap?.to || '');

    // Load unlock configuration
    const autoInferUnlock = unit.auto_infer_unlock !== false; // Default to true
    document.getElementById('wizard-unit-auto-infer-unlock').checked = autoInferUnlock;
    createWizardDropdown('wizard-unit-unlock-tech', 'progression-trees', unit.unlock_tech || '', 'None');
    createWizardDropdown('wizard-unit-unlock-civic', 'progression-trees', unit.unlock_civic || '', 'None');
    // Show/hide custom unlock fields based on auto-infer setting
    toggleUnitAutoInferUnlock(!autoInferUnlock);
    
    // Load abilities
    wizardUnitCurrentAbilities = unit.unit_abilities || [];
    renderWizardUnitAbilitiesList();

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

/**
 * Duplicate an existing unit
 */
export function wizardDuplicateUnit(idx) {
    if (!wizardData.units || !wizardData.units[idx]) return;
    
    // Deep clone the unit
    const originalUnit = wizardData.units[idx];
    const duplicatedUnit = JSON.parse(JSON.stringify(originalUnit));
    
    // Modify IDs to indicate it's a duplicate
    const originalId = duplicatedUnit.id || 'UNIT';
    const originalType = duplicatedUnit.unit_type || 'UNIT_TYPE';
    
    // Add _2, _3, etc. suffix if not already present
    const idMatch = originalId.match(/^(.+?)(_(\d+))?$/);
    const typeMatch = originalType.match(/^(.+?)(_(\d+))?$/);
    
    const baseId = idMatch[1];
    const currentIdNum = idMatch[3] ? parseInt(idMatch[3]) : 1;
    const newIdNum = currentIdNum + 1;
    
    const baseType = typeMatch[1];
    const currentTypeNum = typeMatch[3] ? parseInt(typeMatch[3]) : 1;
    const newTypeNum = currentTypeNum + 1;
    
    duplicatedUnit.id = `${baseId}_${newIdNum}`;
    duplicatedUnit.unit_type = `${baseType}_${newTypeNum}`;
    
    // Add the duplicated unit after the original
    wizardData.units.splice(idx + 1, 0, duplicatedUnit);
    
    renderWizardStep3(document.getElementById('wizard-step-content'));
    markDirty();
    showToast('Unit duplicated successfully', 'success');
}

/**
 * Update the icon path for the unit currently being edited
 */
export function updateUnitIconPath(value) {
    const iconInput = document.getElementById('wizard-unit-icon');
    if (iconInput) {
        iconInput.value = value;
    }
    markDirty();
}

export function wizardShowConstructibleForm() {
    wizardCancelConstructibleForm(); // Reset all fields
    const form = document.getElementById('wizard-constructible-form');
    form.classList.remove('hidden');
    
    // Initialize type toggle to building
    setConstructibleIsBuilding(true);
    
    // Initialize empty arrays
    renderWizardBuildingYields();
    renderWizardBuildingAdjacencies();
    renderWizardBuildingPlunders();
    renderWizardBuildingDistricts();
    renderWizardBuildingTerrains();
    renderWizardBuildingBiomes();
    renderWizardBuildingFeatures();
    
    // Populate dropdown fields
    populateConstructibleDropdowns();
    
    // Populate visual remap dropdown
    populateConstructibleVisualRemapDropdown();
    
    document.getElementById('wizard-constructible-id').focus();
}

// Helper function to populate all dropdown fields in constructible form
async function populateConstructibleDropdowns() {
    // Populate river placement dropdown
    try {
        const response = await fetch('/api/data/river-placements');
        if (response.ok) {
            const data = await response.json();
            const select = document.getElementById('wizard-constructible-river');
            if (select) {
                const currentValue = select.value;
                select.innerHTML = '<option value="">No requirement</option>' +
                    data.values.map(item => `<option value="${item.id}">${item.id}</option>`).join('');
                select.value = currentValue;
            }
        }
    } catch (error) {
        console.error('Error loading river placements:', error);
    }
    
    // Populate cost progression model dropdown
    try {
        const response = await fetch('/api/data/cost-progression-models');
        if (response.ok) {
            const data = await response.json();
            const select = document.getElementById('wizard-constructible-cost-model');
            if (select) {
                const currentValue = select.value;
                select.innerHTML = '<option value="">No progression model</option>' +
                    data.values.map(item => `<option value="${item.id}">${item.id}</option>`).join('');
                select.value = currentValue;
            }
        }
    } catch (error) {
        console.error('Error loading cost progression models:', error);
    }
}

export function wizardCancelConstructibleForm() {
    const form = document.getElementById('wizard-constructible-form');
    form.classList.add('hidden');
    
    // Clear basic fields
    document.getElementById('wizard-constructible-id').value = '';
    document.getElementById('wizard-constructible-type').value = '';
    document.getElementById('wizard-constructible-name').value = '';
    document.getElementById('wizard-constructible-desc').value = '';
    document.getElementById('wizard-constructible-tooltip').value = '';
    document.getElementById('wizard-constructible-icon').value = '';
    
    // Clear placement constraints
    wizardBuildingValidDistricts.length = 0;
    wizardBuildingValidTerrains.length = 0;
    wizardBuildingValidBiomes.length = 0;
    wizardBuildingValidFeatures.length = 0;
    renderWizardBuildingDistricts();
    renderWizardBuildingTerrains();
    renderWizardBuildingBiomes();
    renderWizardBuildingFeatures();
    document.getElementById('wizard-constructible-river').value = '';
    
    // Clear yields and arrays
    wizardBuildingYields.length = 0;
    wizardBuildingAdjacencies.length = 0;
    wizardBuildingPlunders.length = 0;
    renderWizardBuildingYields();
    renderWizardBuildingAdjacencies();
    renderWizardBuildingPlunders();
    
    // Clear maintenance
    document.getElementById('wizard-constructible-maintenance-gold').value = '';
    document.getElementById('wizard-constructible-maintenance-happiness').value = '';
    
    // Clear cost progression
    document.getElementById('wizard-constructible-cost-progression').value = '';
    
    // Clear advanced properties
    const autoAge = wizardData.action_group?.action_group_id || 'AGE_ANTIQUITY';
    const ageSelect = document.getElementById('wizard-constructible-age');
    ageSelect.innerHTML = `<option value="${autoAge}">${autoAge.replace('AGE_', '')}</option>`;
    
    document.getElementById('wizard-constructible-cost-model').value = '';
    document.getElementById('wizard-constructible-district-defense').value = '';
    document.getElementById('wizard-constructible-requires-unlock').checked = false;
    document.getElementById('wizard-constructible-immune-damage').checked = false;
    document.getElementById('wizard-constructible-repairable').checked = false;
    
    // Clear building-specific
    document.getElementById('wizard-constructible-purchasable').checked = false;
    document.getElementById('wizard-constructible-multiple-per-city').checked = false;
    document.getElementById('wizard-constructible-town').value = '';
    
    // Clear improvement-specific
    const civType = wizardData.civilization?.civilization_type || '';
    const autoTrait = civType ? civType.replace('CIVILIZATION_', 'TRAIT_') : '';
    document.getElementById('wizard-constructible-trait-type').value = autoTrait;
    
    document.getElementById('wizard-constructible-unit-healing').value = '';
    document.getElementById('wizard-constructible-city-buildable').checked = false;
    document.getElementById('wizard-constructible-one-per-settlement').checked = false;
    document.getElementById('wizard-constructible-same-adjacent-valid').checked = false;
    document.getElementById('wizard-constructible-ageless').checked = false;
    
    // Reset type to building
    document.getElementById('wizard-constructible-is-building').value = 'true';
    setConstructibleIsBuilding(true);
    
    document.getElementById('wizard-constructible-edit-idx').value = '-1';
}

export function wizardSaveConstructible() {
    const id = document.getElementById('wizard-constructible-id').value.trim();
    const type = document.getElementById('wizard-constructible-type').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-constructible-edit-idx').value, 10);
    const isBuilding = document.getElementById('wizard-constructible-is-building').value === 'true';

    if (!id) {
        showToast('ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Base Type is required', 'error');
        return;
    }

    if (!wizardData.constructibles) {
        wizardData.constructibles = [];
    }

    // Basic fields
    const displayName = document.getElementById('wizard-constructible-name').value.trim();
    const description = document.getElementById('wizard-constructible-desc').value.trim();
    const tooltip = document.getElementById('wizard-constructible-tooltip').value.trim();
    const icon = document.getElementById('wizard-constructible-icon').value.trim();
    
    // Placement constraints - now from arrays
    const riverPlacement = document.getElementById('wizard-constructible-river').value.trim();
    
    // Maintenance
    const maintenanceGold = document.getElementById('wizard-constructible-maintenance-gold').value.trim();
    const maintenanceHappiness = document.getElementById('wizard-constructible-maintenance-happiness').value.trim();
    
    // Costs
    const costProgression = document.getElementById('wizard-constructible-cost-progression').value.trim();
    
    // Advanced properties
    // Auto-populate age from civilization's action_group
    const age = wizardData.action_group?.action_group_id || 'AGE_ANTIQUITY';
    const costModel = document.getElementById('wizard-constructible-cost-model').value.trim();
    const districtDefense = document.getElementById('wizard-constructible-district-defense').value.trim();
    const requiresUnlock = document.getElementById('wizard-constructible-requires-unlock').checked;
    const immuneDamage = document.getElementById('wizard-constructible-immune-damage').checked;
    const repairable = document.getElementById('wizard-constructible-repairable').checked;

    const constructible = {
        id: id,
        constructible_type: type,
        is_building: isBuilding,
    };

    // Localization
    if (displayName || description || tooltip) {
        constructible.localizations = [{}];
        if (displayName) constructible.localizations[0].name = displayName;
        if (description) constructible.localizations[0].description = description;
        if (tooltip) constructible.localizations[0].tooltip = tooltip;
    }

    // Icon
    if (icon) {
        constructible.icon = { path: icon };
    }

    // Visual remap - use same format as units
    const visualRemap = document.getElementById('wizard-constructible-visual-remap').value.trim();
    if (visualRemap) {
        constructible.visual_remap = { to: visualRemap };
    }

    // Placement constraints - from arrays
    if (wizardBuildingValidDistricts.length > 0) {
        constructible.constructible_valid_districts = wizardBuildingValidDistricts.filter(d => d.length > 0);
    }
    if (wizardBuildingValidTerrains.length > 0) {
        constructible.constructible_valid_terrains = wizardBuildingValidTerrains.filter(t => t.length > 0);
        console.log('[DEBUG] Saving terrains:', wizardBuildingValidTerrains, 'Filtered:', constructible.constructible_valid_terrains);
    }
    if (wizardBuildingValidBiomes.length > 0) {
        constructible.constructible_valid_biomes = wizardBuildingValidBiomes.filter(b => b.length > 0);
    }
    if (wizardBuildingValidFeatures.length > 0) {
        constructible.constructible_valid_features = wizardBuildingValidFeatures.filter(f => f.length > 0);
    }
    if (riverPlacement) {
        constructible.river_placement = riverPlacement;
    }

    // Yields
    if (wizardBuildingYields.length > 0) {
        constructible.yield_changes = wizardBuildingYields.filter(y => y.yield_type && y.yield_change);
    }

    // Maintenance
    if (maintenanceGold) {
        constructible.maintenance_gold = parseInt(maintenanceGold, 10);
    }
    if (maintenanceHappiness) {
        constructible.maintenance_happiness = parseInt(maintenanceHappiness, 10);
    }

    // Adjacencies
    if (wizardBuildingAdjacencies.length > 0) {
        constructible.adjacencies = wizardBuildingAdjacencies.filter(a => a.pattern_id || a.yield_type);
    }

    // Plunders
    if (wizardBuildingPlunders.length > 0) {
        constructible.plunders = wizardBuildingPlunders.filter(p => p.plunder_type && p.amount);
    }

    // Cost progression
    if (costProgression) {
        constructible.cost_progressions = [{
            percent: parseInt(costProgression, 10)
        }];
    }

    // Advanced properties
    if (age) constructible.age = age;
    if (costModel) constructible.cost_progression_model = costModel;
    if (districtDefense) constructible.district_defense = parseInt(districtDefense, 10);
    if (requiresUnlock) constructible.requires_unlock = true;
    if (immuneDamage) constructible.immune_damage = true;
    if (repairable) constructible.repairable = true;

    // Building-specific properties
    if (isBuilding) {
        const purchasable = document.getElementById('wizard-constructible-purchasable').checked;
        const multiplePerCity = document.getElementById('wizard-constructible-multiple-per-city').checked;
        const town = document.getElementById('wizard-constructible-town').value.trim();

        if (purchasable) constructible.building = { ...constructible.building, purchasable: true };
        if (multiplePerCity) constructible.building = { ...constructible.building, multiple_per_city: true };
        if (town) constructible.building = { ...constructible.building, town: town };
    } else {
        // Improvement-specific properties
        // Auto-generate trait from civilization type (e.g., CIVILIZATION_ICENI -> TRAIT_ICENI)
        const civType = wizardData.civilization?.civilization_type || '';
        const traitType = civType ? civType.replace('CIVILIZATION_', 'TRAIT_') : '';
        
        const unitHealing = document.getElementById('wizard-constructible-unit-healing').value.trim();
        const cityBuildable = document.getElementById('wizard-constructible-city-buildable').checked;
        const onePerSettlement = document.getElementById('wizard-constructible-one-per-settlement').checked;
        const sameAdjacentValid = document.getElementById('wizard-constructible-same-adjacent-valid').checked;
        const ageless = document.getElementById('wizard-constructible-ageless').checked;

        if (traitType) constructible.improvement = { ...constructible.improvement, trait_type: traitType };
        if (unitHealing) constructible.improvement = { ...constructible.improvement, unit_healing: parseInt(unitHealing, 10) };
        
        // Always set boolean fields explicitly (not just when true)
        constructible.improvement = { 
            ...constructible.improvement, 
            city_buildable: cityBuildable,
            one_per_settlement: onePerSettlement,
            same_adjacent_valid: sameAdjacentValid
        };
        
        // Handle AGELESS as a type_tag, not an age
        if (ageless) {
            constructible.type_tags = constructible.type_tags || [];
            if (!constructible.type_tags.includes('AGELESS')) {
                constructible.type_tags.push('AGELESS');
            }
        }
    }

    if (editIdx >= 0) {
        wizardData.constructibles[editIdx] = constructible;
        showToast('Constructible updated', 'success');
    } else {
        wizardData.constructibles.push(constructible);
        showToast('Constructible added', 'success');
    }

    wizardCancelConstructibleForm();
    renderWizardStep3(document.getElementById('wizard-step-content'));
    markDirty();
}

export async function wizardEditConstructible(idx) {
    const building = wizardData.constructibles[idx];
    const isBuilding = building.is_building !== false; // Default to true
    
    console.log('[DEBUG] Opening constructible for edit:', building);
    console.log('[DEBUG] Terrain data from saved object:', building.constructible_valid_terrains);
    
    // Set type toggle
    document.getElementById('wizard-constructible-is-building').value = isBuilding ? 'true' : 'false';
    setConstructibleIsBuilding(isBuilding, false); // Don't clear fields yet
    
    // Basic fields
    document.getElementById('wizard-constructible-id').value = building.id || '';
    document.getElementById('wizard-constructible-type').value = building.constructible_type || '';
    document.getElementById('wizard-constructible-name').value = building.localizations?.[0]?.name || '';
    document.getElementById('wizard-constructible-desc').value = building.localizations?.[0]?.description || '';
    document.getElementById('wizard-constructible-tooltip').value = building.localizations?.[0]?.tooltip || '';
    document.getElementById('wizard-constructible-icon').value = building.icon?.path || '';
    
    // Placement constraints - populate arrays
    wizardBuildingValidDistricts.length = 0;
    wizardBuildingValidDistricts.push(...(building.constructible_valid_districts || []));
    
    wizardBuildingValidTerrains.length = 0;
    wizardBuildingValidTerrains.push(...(building.constructible_valid_terrains || []));
    console.log('[DEBUG] After loading into array, wizardBuildingValidTerrains:', wizardBuildingValidTerrains);
    
    wizardBuildingValidBiomes.length = 0;
    wizardBuildingValidBiomes.push(...(building.constructible_valid_biomes || []));
    
    wizardBuildingValidFeatures.length = 0;
    wizardBuildingValidFeatures.push(...(building.constructible_valid_features || []));
    
    document.getElementById('wizard-constructible-river').value = building.river_placement || '';
    
    // Render arrays AFTER populating - these will load data if needed
    await renderWizardBuildingDistricts();
    await renderWizardBuildingTerrains();
    await renderWizardBuildingBiomes();
    await renderWizardBuildingFeatures();
    
    // Populate dropdown fields BEFORE setting values
    await populateConstructibleDropdowns();
    
    // Populate visual remap dropdown and set value
    await populateConstructibleVisualRemapDropdown(building.visual_remap?.to || '');
    
    // Yields
    wizardBuildingYields.length = 0;
    wizardBuildingYields.push(...(building.yield_changes || []));
    renderWizardBuildingYields();
    
    // Maintenance
    document.getElementById('wizard-constructible-maintenance-gold').value = building.maintenance_gold || '';
    document.getElementById('wizard-constructible-maintenance-happiness').value = building.maintenance_happiness || '';
    
    // Adjacencies
    wizardBuildingAdjacencies.length = 0;
    wizardBuildingAdjacencies.push(...(building.adjacencies || []));
    renderWizardBuildingAdjacencies();
    
    // Plunders
    wizardBuildingPlunders.length = 0;
    wizardBuildingPlunders.push(...(building.plunders || []));
    renderWizardBuildingPlunders();
    
    // Cost progression
    document.getElementById('wizard-constructible-cost-progression').value = building.cost_progressions?.[0]?.percent || '';
    
    // Advanced properties - set AFTER dropdowns are populated
    // Display auto-generated age
    const autoAge = wizardData.action_group?.action_group_id || 'AGE_ANTIQUITY';
    const ageSelect = document.getElementById('wizard-constructible-age');
    ageSelect.innerHTML = `<option value="${autoAge}">${autoAge.replace('AGE_', '')}</option>`;
    
    document.getElementById('wizard-constructible-cost-model').value = building.cost_progression_model || '';
    document.getElementById('wizard-constructible-district-defense').value = building.district_defense || '';
    document.getElementById('wizard-constructible-requires-unlock').checked = building.requires_unlock || false;
    document.getElementById('wizard-constructible-immune-damage').checked = building.immune_damage || false;
    document.getElementById('wizard-constructible-repairable').checked = building.repairable || false;
    
    // Building-specific
    if (isBuilding) {
        document.getElementById('wizard-constructible-purchasable').checked = building.building?.purchasable || false;
        document.getElementById('wizard-constructible-multiple-per-city').checked = building.building?.multiple_per_city || false;
        document.getElementById('wizard-constructible-town').value = building.building?.town || '';
    } else {
        // Improvement-specific - display auto-generated trait
        const civType = wizardData.civilization?.civilization_type || '';
        const autoTrait = civType ? civType.replace('CIVILIZATION_', 'TRAIT_') : '';
        document.getElementById('wizard-constructible-trait-type').value = autoTrait;
        
        document.getElementById('wizard-constructible-unit-healing').value = building.improvement?.unit_healing || '';
        document.getElementById('wizard-constructible-city-buildable').checked = building.improvement?.city_buildable || false;
        document.getElementById('wizard-constructible-one-per-settlement').checked = building.improvement?.one_per_settlement || false;
        document.getElementById('wizard-constructible-same-adjacent-valid').checked = building.improvement?.same_adjacent_valid || false;
        
        // Check AGELESS from type_tags instead of age
        const hasAgeless = building.type_tags && building.type_tags.includes('AGELESS');
        document.getElementById('wizard-constructible-ageless').checked = hasAgeless;
    }
    
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

/**
 * Update the icon path for the building currently being edited
 */
export function updateBuildingIconPath(value) {
    const iconInput = document.getElementById('wizard-constructible-icon');
    if (iconInput) {
        iconInput.value = value;
    }
    markDirty();
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

/**
 * Set constructible type (building vs improvement) and toggle visibility of sections
 */
export function setConstructibleIsBuilding(isBuilding, clearFields = true) {
    document.getElementById('wizard-constructible-is-building').value = isBuilding ? 'true' : 'false';
    
    // Update button styles
    const buildingBtn = document.getElementById('wizard-constructible-is-building-btn');
    const improvementBtn = document.getElementById('wizard-constructible-is-improvement-btn');
    
    if (isBuilding) {
        buildingBtn.classList.add('bg-blue-600', 'border-blue-500');
        buildingBtn.classList.remove('bg-slate-700', 'border-slate-600');
        improvementBtn.classList.remove('bg-blue-600', 'border-blue-500');
        improvementBtn.classList.add('bg-slate-700', 'border-slate-600');
    } else {
        improvementBtn.classList.add('bg-blue-600', 'border-blue-500');
        improvementBtn.classList.remove('bg-slate-700', 'border-slate-600');
        buildingBtn.classList.remove('bg-blue-600', 'border-blue-500');
        buildingBtn.classList.add('bg-slate-700', 'border-slate-600');
    }
    
    // Toggle section visibility
    const districtSection = document.getElementById('wizard-constructible-district-section');
    const buildingSection = document.getElementById('wizard-constructible-building-section');
    const improvementSection = document.getElementById('wizard-constructible-improvement-section');
    
    if (districtSection) {
        districtSection.style.display = isBuilding ? 'block' : 'none';
    }
    if (buildingSection) {
        buildingSection.style.display = isBuilding ? 'block' : 'none';
    }
    if (improvementSection) {
        improvementSection.style.display = isBuilding ? 'none' : 'block';
    }
    
    if (clearFields) {
        // Clear type-specific fields when switching
        if (isBuilding) {
            document.getElementById('wizard-constructible-trait-type').value = '';
            document.getElementById('wizard-constructible-city-buildable').checked = false;
            document.getElementById('wizard-constructible-one-per-settlement').checked = false;
        } else {
            document.getElementById('wizard-constructible-districts').value = '';
            document.getElementById('wizard-constructible-purchasable').checked = false;
            document.getElementById('wizard-constructible-multiple-per-city').checked = false;
            document.getElementById('wizard-constructible-town').value = '';
        }
    }
}

// Adjacency management
export function addWizardBuildingAdjacency() {
    wizardBuildingAdjacencies.push({ pattern_id: '' });
    renderWizardBuildingAdjacencies();
}

export function updateWizardBuildingAdjacency(idx, field, value) {
    if (wizardBuildingAdjacencies[idx]) {
        wizardBuildingAdjacencies[idx][field] = value;
    }
}

export function removeWizardBuildingAdjacency(idx) {
    wizardBuildingAdjacencies.splice(idx, 1);
    renderWizardBuildingAdjacencies();
}

export function renderWizardBuildingAdjacencies() {
    const container = document.getElementById('wizard-building-adjacencies');
    if (!container) return;

    container.innerHTML = wizardBuildingAdjacencies.map((adj, idx) => `
        <div class="flex gap-2 items-center">
            <select 
                id="wizard-adjacency-pattern-${idx}"
                onchange="window.updateWizardBuildingAdjacency(${idx}, 'pattern_id', this.value)"
                class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            >
                <option value="">Loading...</option>
            </select>
            <button 
                onclick="window.removeWizardBuildingAdjacency(${idx})"
                type="button"
                class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
            >
                ×
            </button>
        </div>
    `).join('');

    wizardBuildingAdjacencies.forEach(async (adj, idx) => {
        const dropdown = document.getElementById(`wizard-adjacency-pattern-${idx}`);
        if (!dropdown) return;

        try {
            const response = await fetch('/api/data/adjacency-patterns');
            if (!response.ok) throw new Error('Failed to fetch adjacency patterns');
            
            const data = await response.json();
            const patterns = data.values || [];
            
            dropdown.innerHTML = '<option value="">Select pattern...</option>' +
                patterns.map(pattern => {
                    const selected = adj.pattern_id === pattern.id ? 'selected' : '';
                    return `<option value="${pattern.id}" ${selected}>${pattern.name}</option>`;
                }).join('');
        } catch (error) {
            console.error('Error loading adjacency patterns:', error);
            dropdown.innerHTML = '<option value="">Error loading patterns</option>';
        }
    });
}

// Plunder management
export function addWizardBuildingPlunder() {
    wizardBuildingPlunders.push({ plunder_type: '', amount: 0 });
    renderWizardBuildingPlunders();
}

export function updateWizardBuildingPlunder(idx, field, value) {
    if (wizardBuildingPlunders[idx]) {
        wizardBuildingPlunders[idx][field] = field === 'amount' ? parseInt(value, 10) || 0 : value;
    }
}

export function removeWizardBuildingPlunder(idx) {
    wizardBuildingPlunders.splice(idx, 1);
    renderWizardBuildingPlunders();
}

export function renderWizardBuildingPlunders() {
    const container = document.getElementById('wizard-building-plunders');
    if (!container) return;

    container.innerHTML = wizardBuildingPlunders.map((plunder, idx) => `
        <div class="flex gap-2 items-center">
            <select 
                id="wizard-plunder-type-${idx}"
                onchange="window.updateWizardBuildingPlunder(${idx}, 'plunder_type', this.value)"
                class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            >
                <option value="">Loading...</option>
            </select>
            <input 
                type="number" 
                value="${plunder.amount || ''}"
                onchange="window.updateWizardBuildingPlunder(${idx}, 'amount', this.value)"
                placeholder="Amount"
                class="w-24 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
            />
            <button 
                onclick="window.removeWizardBuildingPlunder(${idx})"
                type="button"
                class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
            >
                ×
            </button>
        </div>
    `).join('');

    wizardBuildingPlunders.forEach((plunder, idx) => {
        createWizardDropdown(`wizard-plunder-type-${idx}`, 'plunder-types', plunder.plunder_type || '', 'Select plunder type...');
    });
}

// Placement Constraints - Valid Districts
export function addWizardBuildingDistrict() {
    wizardBuildingValidDistricts.push('');
    renderWizardBuildingDistricts();
}

export function updateWizardBuildingDistrict(idx, value) {
    if (idx >= 0 && idx < wizardBuildingValidDistricts.length) {
        wizardBuildingValidDistricts[idx] = value;
    }
}

export function removeWizardBuildingDistrict(idx) {
    wizardBuildingValidDistricts.splice(idx, 1);
    renderWizardBuildingDistricts();
}

export async function renderWizardBuildingDistricts() {
    const container = document.getElementById('wizard-building-districts');
    if (!container) return;

    // Load district types if not cached
    if (!cachedDistrictTypes) {
        try {
            const response = await fetch('/api/data/district-types');
            if (response.ok) {
                const data = await response.json();
                cachedDistrictTypes = data.values || [];
            }
        } catch (error) {
            console.error('Error loading district types:', error);
            return;
        }
    }

    container.innerHTML = wizardBuildingValidDistricts.map((district, idx) => {
        const options = cachedDistrictTypes.map(d => 
            `<option value="${d.id}" ${d.id === district ? 'selected' : ''}>${d.id}</option>`
        ).join('');
        
        return `
            <div class="flex gap-2 items-center">
                <select 
                    id="wizard-district-${idx}"
                    onchange="window.updateWizardBuildingDistrict(${idx}, this.value)"
                    class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                >
                    <option value="">Select district...</option>
                    ${options}
                </select>
                <button 
                    onclick="window.removeWizardBuildingDistrict(${idx})"
                    type="button"
                    class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                >
                    ×
                </button>
            </div>
        `;
    }).join('');
}

// Placement Constraints - Valid Terrains
export function addWizardBuildingTerrain() {
    wizardBuildingValidTerrains.push('');
    renderWizardBuildingTerrains();
}

export function updateWizardBuildingTerrain(idx, value) {
    if (idx >= 0 && idx < wizardBuildingValidTerrains.length) {
        wizardBuildingValidTerrains[idx] = value;
    }
}

export function removeWizardBuildingTerrain(idx) {
    wizardBuildingValidTerrains.splice(idx, 1);
    renderWizardBuildingTerrains();
}

export async function renderWizardBuildingTerrains() {
    const container = document.getElementById('wizard-building-terrains');
    if (!container) return;

    // Load terrain types if not cached
    if (!cachedTerrainTypes) {
        try {
            const response = await fetch('/api/data/terrain-types');
            if (response.ok) {
                const data = await response.json();
                cachedTerrainTypes = data.values || [];
            }
        } catch (error) {
            console.error('Error loading terrain types:', error);
            return;
        }
    }

    container.innerHTML = wizardBuildingValidTerrains.map((terrain, idx) => {
        const options = cachedTerrainTypes.map(t => 
            `<option value="${t.id}" ${t.id === terrain ? 'selected' : ''}>${t.id}</option>`
        ).join('');
        
        return `
            <div class="flex gap-2 items-center">
                <select 
                    id="wizard-terrain-${idx}"
                    onchange="window.updateWizardBuildingTerrain(${idx}, this.value)"
                    class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                >
                    <option value="">Select terrain...</option>
                    ${options}
                </select>
                <button 
                    onclick="window.removeWizardBuildingTerrain(${idx})"
                    type="button"
                    class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                >
                    ×
                </button>
            </div>
        `;
    }).join('');
}

// Placement Constraints - Valid Biomes
export function addWizardBuildingBiome() {
    wizardBuildingValidBiomes.push('');
    renderWizardBuildingBiomes();
}

export function updateWizardBuildingBiome(idx, value) {
    if (idx >= 0 && idx < wizardBuildingValidBiomes.length) {
        wizardBuildingValidBiomes[idx] = value;
    }
}

export function removeWizardBuildingBiome(idx) {
    wizardBuildingValidBiomes.splice(idx, 1);
    renderWizardBuildingBiomes();
}

export async function renderWizardBuildingBiomes() {
    const container = document.getElementById('wizard-building-biomes');
    if (!container) return;

    // Load biome types if not cached
    if (!cachedBiomeTypes) {
        try {
            const response = await fetch('/api/data/biome-types');
            if (response.ok) {
                const data = await response.json();
                cachedBiomeTypes = data.values || [];
            }
        } catch (error) {
            console.error('Error loading biome types:', error);
            return;
        }
    }

    container.innerHTML = wizardBuildingValidBiomes.map((biome, idx) => {
        const options = cachedBiomeTypes.map(b => 
            `<option value="${b.id}" ${b.id === biome ? 'selected' : ''}>${b.id}</option>`
        ).join('');
        
        return `
            <div class="flex gap-2 items-center">
                <select 
                    id="wizard-biome-${idx}"
                    onchange="window.updateWizardBuildingBiome(${idx}, this.value)"
                    class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                >
                    <option value="">Select biome...</option>
                    ${options}
                </select>
                <button 
                    onclick="window.removeWizardBuildingBiome(${idx})"
                    type="button"
                    class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                >
                    ×
                </button>
            </div>
        `;
    }).join('');
}

// Placement Constraints - Valid Features
export function addWizardBuildingFeature() {
    wizardBuildingValidFeatures.push('');
    renderWizardBuildingFeatures();
}

export function updateWizardBuildingFeature(idx, value) {
    if (idx >= 0 && idx < wizardBuildingValidFeatures.length) {
        wizardBuildingValidFeatures[idx] = value;
    }
}

export function removeWizardBuildingFeature(idx) {
    wizardBuildingValidFeatures.splice(idx, 1);
    renderWizardBuildingFeatures();
}

export async function renderWizardBuildingFeatures() {
    const container = document.getElementById('wizard-building-features');
    if (!container) return;

    // Load feature types if not cached
    if (!cachedFeatureTypes) {
        try {
            const response = await fetch('/api/data/feature-types');
            if (response.ok) {
                const data = await response.json();
                cachedFeatureTypes = data.values || [];
            }
        } catch (error) {
            console.error('Error loading feature types:', error);
            return;
        }
    }

    container.innerHTML = wizardBuildingValidFeatures.map((feature, idx) => {
        const options = cachedFeatureTypes.map(f => 
            `<option value="${f.id}" ${f.id === feature ? 'selected' : ''}>${f.id}</option>`
        ).join('');
        
        return `
            <div class="flex gap-2 items-center">
                <select 
                    id="wizard-feature-${idx}"
                    onchange="window.updateWizardBuildingFeature(${idx}, this.value)"
                    class="flex-1 px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                >
                    <option value="">Select feature...</option>
                    ${options}
                </select>
                <button 
                    onclick="window.removeWizardBuildingFeature(${idx})"
                    type="button"
                    class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                >
                    ×
                </button>
            </div>
        `;
    }).join('');
}


/**
 * Populate visual remap dropdown with all available units
 * @param {string} selectedValue - Currently selected unit ID
 */
export async function populateVisualRemapDropdown(selectedValue = '') {
    const dropdown = document.getElementById('wizard-unit-visual-remap');
    if (!dropdown) return;

    try {
        const response = await fetch('/api/data/units');
        if (!response.ok) throw new Error('Failed to fetch units');
        
        const data = await response.json();
        const units = data.values || [];
        
        // Build options with all units, sorted alphabetically by ID
        dropdown.innerHTML = '<option value="">None (no visual remap)</option>' +
            units.sort((a, b) => a.id.localeCompare(b.id)).map(unit => {
                return `<option value="${unit.id}">${unit.id}</option>`;
            }).join('');
        
        // Restore selection
        if (selectedValue) {
            dropdown.value = selectedValue;
        }
    } catch (error) {
        console.error('Error populating visual remap dropdown:', error);
        dropdown.innerHTML = '<option value="">Error loading units</option>';
    }
}

/**
 * Populate constructible visual remap dropdown with all available constructibles
 * @param {string} selectedValue - Currently selected constructible ID
 */
export async function populateConstructibleVisualRemapDropdown(selectedValue = '') {
    const dropdown = document.getElementById('wizard-constructible-visual-remap');
    if (!dropdown) return;

    try {
        const response = await fetch('/api/data/constructibles');
        if (!response.ok) throw new Error('Failed to fetch constructibles');
        
        const data = await response.json();
        const constructibles = data.values || [];
        
        // Build options with all constructibles, sorted alphabetically by ID
        dropdown.innerHTML = '<option value="">None (custom or default visuals)</option>' +
            constructibles.sort((a, b) => a.id.localeCompare(b.id)).map(item => {
                return `<option value="${item.id}">${item.id}</option>`;
            }).join('');
        
        // Restore selection
        if (selectedValue) {
            dropdown.value = selectedValue;
        }
    } catch (error) {
        console.error('Error populating constructible visual remap dropdown:', error);
        dropdown.innerHTML = '<option value="">Error loading constructibles</option>';
    }
}

/**
 * Toggle between dropdown and custom text input for Replaces Unit field
 */
export function toggleUnitReplacesCustom(isCustom) {
    const dropdown = document.getElementById('wizard-unit-replaces');
    const customInput = document.getElementById('wizard-unit-replaces-custom');
    
    if (isCustom) {
        dropdown.classList.add('hidden');
        customInput.classList.remove('hidden');
        // Transfer value if switching
        if (dropdown.value) {
            customInput.value = dropdown.value;
        }
    } else {
        dropdown.classList.remove('hidden');
        customInput.classList.add('hidden');
        // Transfer value if switching
        if (customInput.value) {
            dropdown.value = customInput.value;
        }
    }
}

/**
 * Toggle between dropdown and custom text input for Upgrades To field
 */
export function toggleUnitUpgradeCustom(isCustom) {
    const dropdown = document.getElementById('wizard-unit-upgrade-to');
    const customInput = document.getElementById('wizard-unit-upgrade-custom');
    
    if (isCustom) {
        dropdown.classList.add('hidden');
        customInput.classList.remove('hidden');
        // Transfer value if switching
        if (dropdown.value) {
            customInput.value = dropdown.value;
        }
    } else {
        dropdown.classList.remove('hidden');
        customInput.classList.add('hidden');
        // Transfer value if switching
        if (customInput.value) {
            dropdown.value = customInput.value;
        }
    }
}

/**
 * Toggle between auto-infer unlock and custom unlock fields
 */
export function toggleUnitAutoInferUnlock(showCustom) {
    const customFields = document.getElementById('wizard-unit-custom-unlock-fields');
    
    if (showCustom) {
        customFields.classList.remove('hidden');
    } else {
        customFields.classList.add('hidden');
    }
}

// Expose toggle functions to window for inline event handlers
window.toggleUnitReplacesCustom = toggleUnitReplacesCustom;
window.toggleUnitUpgradeCustom = toggleUnitUpgradeCustom;
window.toggleUnitAutoInferUnlock = toggleUnitAutoInferUnlock;

// ===== UNIT ABILITIES CRUD =====

export function renderWizardUnitAbilitiesList() {
    const container = document.getElementById('wizard-unit-abilities-list');
    if (!container) return;

    const abilities = wizardUnitCurrentAbilities || [];
    
    if (abilities.length === 0) {
        container.innerHTML = '<p class="text-xs text-slate-500 italic">No abilities added yet</p>';
        return;
    }

    container.innerHTML = abilities.map((ability, idx) => `
        <div class="p-2 bg-slate-800/50 rounded border border-slate-600 flex items-center justify-between">
            <div class="flex-1">
                <div class="font-semibold text-slate-200 text-xs">${ability.ability_id || ability.ability_type || 'Unknown Ability'}</div>
                <div class="text-xs text-slate-400 mt-1">${ability.name || 'No name'}</div>
                ${ability.inactive ? '<span class="inline-block px-1.5 py-0.5 mt-1 bg-amber-600/20 text-amber-400 text-xs rounded">Inactive</span>' : ''}
                ${ability.charged_config ? '<span class="inline-block px-1.5 py-0.5 mt-1 bg-purple-600/20 text-purple-400 text-xs rounded">Charged</span>' : ''}
            </div>
            <div class="flex gap-1">
                <button 
                    onclick="window.wizardEditAbility(${idx})"
                    class="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs"
                    title="Edit"
                >
                    Edit
                </button>
                <button 
                    onclick="window.wizardRemoveAbility(${idx})"
                    class="px-2 py-1 bg-red-600 hover:bg-red-700 rounded text-xs"
                    title="Remove"
                >
                    Remove
                </button>
            </div>
        </div>
    `).join('');
}

let wizardUnitCurrentAbilities = [];

export function wizardShowAbilityForm() {
    const form = document.getElementById('wizard-ability-form');
    const editIdx = document.getElementById('wizard-ability-edit-idx');
    
    // Reset form
    document.getElementById('wizard-ability-id').value = '';
    document.getElementById('wizard-ability-type-select').value = '';
    document.getElementById('wizard-ability-type-custom').value = '';
    document.getElementById('wizard-ability-type-custom').classList.add('hidden');
    document.getElementById('wizard-ability-name').value = '';
    document.getElementById('wizard-ability-name').disabled = false;
    document.getElementById('wizard-ability-description').value = '';
    document.getElementById('wizard-ability-description').disabled = false;
    document.getElementById('wizard-ability-inactive').checked = false;
    document.getElementById('wizard-ability-charged').checked = false;
    document.getElementById('wizard-ability-recharge-turns').value = '';
    document.getElementById('wizard-ability-modifiers').value = '';
    document.getElementById('wizard-ability-recharge-div').classList.add('hidden');
    document.getElementById('wizard-ability-type-help').textContent = 'Select an existing game ability or create a custom one';
    document.getElementById('wizard-ability-modifiers-help').textContent = 'Optional: Only needed for custom abilities. Existing abilities already have their effects defined.';
    editIdx.value = '-1';
    
    // Load ability options if not already loaded
    loadAbilityOptions();
    
    form.classList.remove('hidden');
}

export function wizardCancelAbilityForm() {
    const form = document.getElementById('wizard-ability-form');
    form.classList.add('hidden');
}

export function wizardSaveAbility() {
    const editIdx = parseInt(document.getElementById('wizard-ability-edit-idx').value, 10);
    const abilityId = document.getElementById('wizard-ability-id').value.trim();
    const selectedType = document.getElementById('wizard-ability-type-select').value;
    const customType = document.getElementById('wizard-ability-type-custom').value.trim();
    const abilityType = selectedType === '__CUSTOM__' ? customType : selectedType;
    const name = document.getElementById('wizard-ability-name').value.trim();
    const description = document.getElementById('wizard-ability-description').value.trim();
    const inactive = document.getElementById('wizard-ability-inactive').checked;
    const charged = document.getElementById('wizard-ability-charged').checked;
    const rechargeTurns = document.getElementById('wizard-ability-recharge-turns').value;
    const modifiersText = document.getElementById('wizard-ability-modifiers').value.trim();

    if (!abilityId || !abilityType || !name || !description) {
        showToast('Ability ID, type, name, and description are required', 'error');
        return;
    }

    const ability = {
        ability_id: abilityId,
        ability_type: abilityType,
        name: name,
        description: description,
        inactive: inactive || undefined,
        modifiers: modifiersText ? modifiersText.split(',').map(m => m.trim()).filter(m => m) : [],
    };

    if (charged && rechargeTurns) {
        ability.charged_config = { recharge_turns: parseInt(rechargeTurns, 10) };
    }

    if (editIdx >= 0) {
        // Edit existing
        wizardUnitCurrentAbilities[editIdx] = ability;
    } else {
        // Add new
        wizardUnitCurrentAbilities.push(ability);
    }

    wizardCancelAbilityForm();
    renderWizardUnitAbilitiesList();
    markDirty();
}

export function wizardEditAbility(idx) {
    const ability = wizardUnitCurrentAbilities[idx];
    if (!ability) return;

    // Load ability options first
    loadAbilityOptions().then(() => {
        const select = document.getElementById('wizard-ability-type-select');
        const customInput = document.getElementById('wizard-ability-type-custom');
        const nameInput = document.getElementById('wizard-ability-name');
        const descInput = document.getElementById('wizard-ability-description');
        const abilityId = ability.ability_id || '';
        const abilityType = ability.ability_type || '';
        
        // Check if it's an existing ability
        const isExisting = abilityDataCache[abilityType];
        
        document.getElementById('wizard-ability-id').value = abilityId;
        
        if (isExisting) {
            select.value = abilityType;
            customInput.classList.add('hidden');
            // Use stored name/description from ability data, but allow editing
            nameInput.value = ability.name || isExisting.name || abilityType;
            descInput.value = ability.description || isExisting.description || '';
            // Don't disable for editing - user might want to override
            nameInput.disabled = false;
            descInput.disabled = false;
        } else {
            select.value = '__CUSTOM__';
            customInput.value = abilityType;
            customInput.classList.remove('hidden');
            nameInput.value = ability.name || '';
            descInput.value = ability.description || '';
            nameInput.disabled = false;
            descInput.disabled = false;
            document.getElementById('wizard-ability-type-help').textContent = 'Custom ability identifier';
            document.getElementById('wizard-ability-modifiers-help').textContent = 'Required: Define modifiers to specify what this custom ability does';
        }
        
        document.getElementById('wizard-ability-inactive').checked = ability.inactive || false;
        document.getElementById('wizard-ability-charged').checked = !!ability.charged_config;
        document.getElementById('wizard-ability-recharge-turns').value = ability.charged_config?.recharge_turns || '';
        document.getElementById('wizard-ability-modifiers').value = ability.modifiers?.join(', ') || '';
        document.getElementById('wizard-ability-edit-idx').value = idx;
        
        // Show/hide recharge field
        if (ability.charged_config) {
            document.getElementById('wizard-ability-recharge-div').classList.remove('hidden');
        } else {
            document.getElementById('wizard-ability-recharge-div').classList.add('hidden');
        }

        document.getElementById('wizard-ability-form').classList.remove('hidden');
    });
}

export function wizardRemoveAbility(idx) {
    wizardUnitCurrentAbilities.splice(idx, 1);
    renderWizardUnitAbilitiesList();
    markDirty();
}

// Helper: Toggle custom ability type input
export function toggleAbilityCustomType(isCustom) {
    const customInput = document.getElementById('wizard-ability-type-custom');
    const helpText = document.getElementById('wizard-ability-type-help');
    const modifiersHelp = document.getElementById('wizard-ability-modifiers-help');
    const nameInput = document.getElementById('wizard-ability-name');
    const descInput = document.getElementById('wizard-ability-description');
    
    if (isCustom) {
        customInput.classList.remove('hidden');
        customInput.focus();
        helpText.textContent = 'Enter unique ability identifier (e.g., ABILITY_MY_CUSTOM_UNIT)';
        modifiersHelp.textContent = 'Required: Define modifiers to specify what this custom ability does';
        // Clear and enable name/description for custom abilities
        nameInput.value = '';
        descInput.value = '';
        nameInput.disabled = false;
        descInput.disabled = false;
    } else {
        customInput.classList.add('hidden');
        customInput.value = '';
        
        // Get the selected ability
        const selectedAbilityId = document.getElementById('wizard-ability-type-select').value;
        if (selectedAbilityId && abilityDataCache[selectedAbilityId]) {
            const abilityData = abilityDataCache[selectedAbilityId];
            // Auto-populate with localization keys from game data
            nameInput.value = abilityData.name || selectedAbilityId;
            descInput.value = abilityData.description || '';
            // Make read-only since these come from the game
            nameInput.disabled = true;
            descInput.disabled = true;
            helpText.textContent = 'Existing game ability - name and description from game data';
            modifiersHelp.textContent = 'Optional: Only needed for custom abilities. This existing ability already has its effects defined in the game.';
        } else {
            helpText.textContent = 'Select an existing game ability or create a custom one';
            modifiersHelp.textContent = 'Optional: Only needed for custom abilities. Existing abilities already have their effects defined.';
            nameInput.disabled = false;
            descInput.disabled = false;
        }
    }
}

// Helper: Load ability options from reference data
let abilityOptionsLoaded = false;
let abilityDataCache = {}; // Store full ability data for lookup
async function loadAbilityOptions() {
    if (abilityOptionsLoaded) return;
    
    const select = document.getElementById('wizard-ability-type-select');
    if (!select) return;
    
    try {
        const response = await fetch('/api/data/unit-abilities');
        const data = await response.json();
        
        // Clear loading option
        while (select.options.length > 2) {
            select.remove(2);
        }
        
        // Add abilities and cache their data
        if (data.values && Array.isArray(data.values)) {
            data.values.forEach(ability => {
                const option = document.createElement('option');
                option.value = ability.id;
                // Show ID with preview of name if available
                const displayText = ability.name && ability.name !== '' 
                    ? `${ability.id} (${ability.name})`
                    : ability.id;
                option.textContent = displayText;
                select.appendChild(option);
                
                // Cache the full ability data
                abilityDataCache[ability.id] = ability;
            });
        }
        
        abilityOptionsLoaded = true;
    } catch (error) {
        console.error('Failed to load unit abilities:', error);
    }
}

// Expose ability functions to window
window.wizardShowAbilityForm = wizardShowAbilityForm;
window.wizardCancelAbilityForm = wizardCancelAbilityForm;
window.wizardSaveAbility = wizardSaveAbility;
window.wizardEditAbility = wizardEditAbility;
window.wizardRemoveAbility = wizardRemoveAbility;
window.toggleAbilityCustomType = toggleAbilityCustomType;
/**
 * Unique Quarter Functions
 */

function wizardShowUniqueQuarterForm() {
    const form = document.getElementById('wizard-unique-quarter-form');
    const editIdx = document.getElementById('wizard-unique-quarter-edit-idx').value;
    
    // Populate building dropdowns
    populateQuarterBuildingDropdowns();
    
    // If not editing, clear form
    if (editIdx === '-1') {
        document.getElementById('wizard-unique-quarter-id').value = '';
        document.getElementById('wizard-unique-quarter-type').value = '';
        document.getElementById('wizard-unique-quarter-building1').value = '';
        document.getElementById('wizard-unique-quarter-building2').value = '';
        document.getElementById('wizard-unique-quarter-name').value = '';
        document.getElementById('wizard-unique-quarter-desc').value = '';
        document.getElementById('wizard-unique-quarter-tooltip').value = '';
    }
    
    form.classList.remove('hidden');
    document.getElementById('wizard-unique-quarter-id').focus();
}

function populateQuarterBuildingDropdowns() {
    const buildings = wizardData.constructibles?.filter(c => 
        c.constructible?.constructible_class === 'BUILDING' || c.is_building !== false
    ) || [];
    
    const dropdown1 = document.getElementById('wizard-unique-quarter-building1');
    const dropdown2 = document.getElementById('wizard-unique-quarter-building2');
    
    // Clear existing options except first
    dropdown1.innerHTML = '<option value="">Select building...</option>';
    dropdown2.innerHTML = '<option value="">Select building...</option>';
    
    buildings.forEach(building => {
        const id = building.id || building.constructible?.constructible_type;
        const name = building.localizations?.[0]?.name || id || 'Unnamed Building';
        
        const opt1 = document.createElement('option');
        opt1.value = id;
        opt1.textContent = name;
        dropdown1.appendChild(opt1);
        
        const opt2 = document.createElement('option');
        opt2.value = id;
        opt2.textContent = name;
        dropdown2.appendChild(opt2);
    });
}

function wizardCancelUniqueQuarterForm() {
    const form = document.getElementById('wizard-unique-quarter-form');
    form.classList.add('hidden');
    document.getElementById('wizard-unique-quarter-edit-idx').value = '-1';
}

function wizardSaveUniqueQuarter() {
    const id = document.getElementById('wizard-unique-quarter-id').value.trim();
    const type = document.getElementById('wizard-unique-quarter-type').value.trim();
    const building1 = document.getElementById('wizard-unique-quarter-building1').value.trim();
    const building2 = document.getElementById('wizard-unique-quarter-building2').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-unique-quarter-edit-idx').value, 10);
    
    // Validation
    if (!id) {
        showToast('Quarter ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Quarter Type is required', 'error');
        return;
    }
    if (!building1 || !building2) {
        showToast('Both buildings are required', 'error');
        return;
    }
    if (building1 === building2) {
        showToast('Buildings must be different', 'error');
        return;
    }
    
    const quarter = {
        id: id,
        unique_quarter_type: type,
        building_type_1: building1,
        building_type_2: building2,
        localization: {
            name: document.getElementById('wizard-unique-quarter-name').value.trim() || id,
            description: document.getElementById('wizard-unique-quarter-desc').value.trim() || '',
            tooltip: document.getElementById('wizard-unique-quarter-tooltip').value.trim() || ''
        }
    };
    
    if (!wizardData.unique_quarters) {
        wizardData.unique_quarters = [];
    }
    
    if (editIdx >= 0) {
        wizardData.unique_quarters[editIdx] = quarter;
        showToast('Unique quarter updated', 'success');
    } else {
        wizardData.unique_quarters.push(quarter);
        showToast('Unique quarter added', 'success');
    }
    
    markDirty();
    wizardCancelUniqueQuarterForm();
    
    // Re-render step 3 to show updated quarter list
    const container = document.getElementById('wizard-step-3');
    if (container) {
        renderWizardStep3(container);
    }
}

function wizardEditUniqueQuarter(idx) {
    const quarter = wizardData.unique_quarters[idx];
    if (!quarter) return;
    
    document.getElementById('wizard-unique-quarter-id').value = quarter.id || '';
    document.getElementById('wizard-unique-quarter-type').value = quarter.unique_quarter_type || '';
    document.getElementById('wizard-unique-quarter-building1').value = quarter.building_type_1 || '';
    document.getElementById('wizard-unique-quarter-building2').value = quarter.building_type_2 || '';
    document.getElementById('wizard-unique-quarter-name').value = quarter.localization?.name || '';
    document.getElementById('wizard-unique-quarter-desc').value = quarter.localization?.description || '';
    document.getElementById('wizard-unique-quarter-tooltip').value = quarter.localization?.tooltip || '';
    document.getElementById('wizard-unique-quarter-edit-idx').value = idx;
    
    wizardShowUniqueQuarterForm();
}

function removeWizardUniqueQuarter(idx) {
    if (!confirm('Remove this unique quarter?')) return;
    
    wizardData.unique_quarters.splice(idx, 1);
    markDirty();
    showToast('Unique quarter removed', 'success');
    
    // Re-render step 3
    const container = document.getElementById('wizard-step-3');
    if (container) {
        renderWizardStep3(container);
    }
}

// Expose unique quarter functions to window
window.wizardShowUniqueQuarterForm = wizardShowUniqueQuarterForm;
window.wizardCancelUniqueQuarterForm = wizardCancelUniqueQuarterForm;
window.wizardSaveUniqueQuarter = wizardSaveUniqueQuarter;
window.wizardEditUniqueQuarter = wizardEditUniqueQuarter;
window.removeWizardUniqueQuarter = removeWizardUniqueQuarter;