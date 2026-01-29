/**
 * Wizard Step 2 - Core Civilization
 * Civilization traits, names, unlocks
 */

import { wizardData, markDirty, getSettings } from '../state.js';
import { createWizardDropdown } from './wizard.js';
import { showToast, showLoadingToast } from '../ui.js';

/**
 * Render Step 2: Core Civilization
 * @param {HTMLElement} container - Container element to render into
 */
export function renderWizardStep2(container) {
    const selectedTraits = wizardData.civilization?.civilization_traits || [];

    // Ensure all functions are available on window object immediately
    if (typeof window !== 'undefined') {
        window.addWizardTerrainBias = addWizardTerrainBias;
        window.addWizardCivUnlock = addWizardCivUnlock;
    }

    // Check for open details to preserve state during re-renders (before innerHTML wipe)
    const startingLocationElem = container.querySelector('#wizard-details-starting-location');
    const ageTransitionsElem = container.querySelector('#wizard-details-age-transitions');
    const isStartingLocationOpen = startingLocationElem?.hasAttribute('open') ?? false;
    const isAgeTransitionsOpen = ageTransitionsElem?.hasAttribute('open') ?? false;
    
    console.log('[STEP2_RENDER] Found starting location elem:', !!startingLocationElem, 'open attr:', startingLocationElem?.getAttribute('open'), 'isOpen:', isStartingLocationOpen);
    console.log('[STEP2_RENDER] Found age transitions elem:', !!ageTransitionsElem, 'open attr:', ageTransitionsElem?.getAttribute('open'), 'isOpen:', isAgeTransitionsOpen);

    const startLocTemplate = isStartingLocationOpen ? 'open' : '';
    const ageTransTemplate = isAgeTransitionsOpen ? 'open' : '';
    console.log('[STEP2_RENDER] Template will include: starting-loc open attr="' + startLocTemplate + '", age-trans open attr="' + ageTransTemplate + '"');

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
                            <div class="flex gap-2">
                                <input 
                                    type="text" 
                                    id="wizard-civ-icon" 
                                    value="${wizardData.civilization?.icon?.path || ''}"
                                    onchange="window.updateWizardIconPath(this.value)"
                                    placeholder="icons/civs/civ_sym_babylon"
                                    class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                                />
                                <button 
                                    onclick="window.generateCivIcon()"
                                    class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg text-sm font-medium whitespace-nowrap transition-colors"
                                    title="Generate icon using AI"
                                >
                                    ✨ Generate
                                </button>
                                <button 
                                    onclick="document.getElementById('wizard-civ-icon-upload-input').click()"
                                    class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium whitespace-nowrap transition-colors"
                                    title="Upload a local icon file"
                                >
                                    📁 Upload
                                </button>
                                <input 
                                    type="file" 
                                    id="wizard-civ-icon-upload-input" 
                                    accept="image/*"
                                    style="display: none;"
                                    onchange="window.handleCivIconUpload(this)"
                                />
                            </div>
                            <p class="text-xs text-slate-500 mt-1">Path to civilization icon (e.g., icons/civs/civ_sym_iceni) or click Generate to create with AI</p>
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
                    <h4 class="font-semibold text-slate-200 mb-4">
                        Citizen Names
                        <button 
                            onclick="window.generateCitizenNames()"
                            class="ml-2 px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium"
                            title="Generate culturally appropriate citizen names using AI"
                        >
                            ✨ AI Generate
                        </button>
                    </h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="block text-sm font-medium text-slate-300">Male Names</label>
                                <button 
                                    onclick="window.addWizardCitizenName('male')"
                                    class="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs font-medium"
                                >
                                    + Add
                                </button>
                            </div>
                            <div id="wizard-male-citizen-names" class="space-y-2 max-h-48 overflow-y-auto">
                                ${(wizardData.civilization?.localizations?.[0]?.citizen_names?.male || []).map((name, idx) => `
                                    <div class="flex items-center gap-2">
                                        <span class="text-slate-400 text-sm w-8">${idx + 1}.</span>
                                        <input 
                                            type="text" 
                                            value="${name}"
                                            onchange="window.updateWizardCitizenNameAt('male', ${idx}, this.value)"
                                            class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                            placeholder="Male name"
                                        />
                                        <button 
                                            onclick="window.removeWizardCitizenName('male', ${idx})"
                                            class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                        >
                                            ×
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="block text-sm font-medium text-slate-300">Female Names</label>
                                <button 
                                    onclick="window.addWizardCitizenName('female')"
                                    class="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs font-medium"
                                >
                                    + Add
                                </button>
                            </div>
                            <div id="wizard-female-citizen-names" class="space-y-2 max-h-48 overflow-y-auto">
                                ${(wizardData.civilization?.localizations?.[0]?.citizen_names?.female || []).map((name, idx) => `
                                    <div class="flex items-center gap-2">
                                        <span class="text-slate-400 text-sm w-8">${idx + 1}.</span>
                                        <input 
                                            type="text" 
                                            value="${name}"
                                            onchange="window.updateWizardCitizenNameAt('female', ${idx}, this.value)"
                                            class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                            placeholder="Female name"
                                        />
                                        <button 
                                            onclick="window.removeWizardCitizenName('female', ${idx})"
                                            class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                        >
                                            ×
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                    <p class="text-xs text-slate-500 mt-2">Names for your civilization's citizens</p>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">Civilization Favored Wonders</h4>
                    <div id="wizard-favored-wonders-container" class="space-y-2">
                        ${(wizardData.civilization?.civilization_favored_wonders || []).map((wonder, idx) => `
                            <div class="flex items-center gap-2">
                                <select 
                                    id="wizard-wonder-${idx}"
                                    onchange="window.autoFillFavoredWonder(${idx}, this.value)"
                                    class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                                >
                                    <option value="">Loading...</option>
                                </select>
                                <button 
                                    onclick="window.removeWizardFavoredWonder(${idx})"
                                    class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button 
                        onclick="window.addWizardFavoredWonder()"
                        class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                    >
                        + Add Wonder
                    </button>
                    <p class="text-xs text-slate-500 mt-2">Wonders this civilization is historically associated with</p>
                </div>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">Leader Civilization Bias</h4>
                    <div class="mb-3 p-3 bg-blue-900/30 border border-blue-700 rounded text-xs text-slate-300">
                        <p><strong>Leader Bias:</strong> Define which leaders have affinity for this civilization and why.</p>
                        <ul class="list-disc list-inside mt-2 text-slate-400">
                            <li><strong>Bias (1-3):</strong> Higher values = stronger affinity</li>
                            <li><strong>Choice Type:</strong> Geographic (location), Strategic (playstyle), or Historical (actual history)</li>
                        </ul>
                    </div>
                    <div id="wizard-leader-biases-container" class="space-y-3">
                        ${(wizardData.civilization?.leader_civilization_biases || []).map((bias, idx) => `
                            <div class="p-3 bg-slate-800/50 rounded border border-slate-600 space-y-2">
                                <div class="grid grid-cols-3 gap-2">
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Leader</label>
                                        <select 
                                            id="wizard-leader-${idx}"
                                            onchange="window.autoFillLeaderBias(${idx}, this.value)"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                        >
                                            <option value="">Loading...</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Bias (1-3)</label>
                                        <input 
                                            type="number" 
                                            min="1" 
                                            max="3" 
                                            value="${bias.bias || 2}"
                                            onchange="window.updateWizardLeaderBiasAt(${idx}, 'bias', parseInt(this.value) || 2)"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                        />
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Choice Type</label>
                                        <select 
                                            onchange="window.updateWizardLeaderBiasAt(${idx}, 'choice_type', this.value)"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                        >
                                            <option value="LOC_CREATE_GAME_GEOGRAPHIC_CHOICE" ${bias.choice_type === 'LOC_CREATE_GAME_GEOGRAPHIC_CHOICE' ? 'selected' : ''}>Geographic</option>
                                            <option value="LOC_CREATE_GAME_STRATEGIC_CHOICE" ${bias.choice_type === 'LOC_CREATE_GAME_STRATEGIC_CHOICE' ? 'selected' : ''}>Strategic</option>
                                            <option value="LOC_CREATE_GAME_HISTORICAL_CHOICE" ${bias.choice_type === 'LOC_CREATE_GAME_HISTORICAL_CHOICE' ? 'selected' : ''}>Historical</option>
                                        </select>
                                    </div>
                                </div>
                                <button 
                                    onclick="window.removeWizardLeaderBias(${idx})"
                                    class="w-full px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                                >
                                    Remove
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button 
                        onclick="window.addWizardLeaderBias()"
                        class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                    >
                        + Add Leader Bias
                    </button>
                    <p class="text-xs text-slate-500 mt-2">AI leader selection preferences and unlock display</p>
                </div>
                
                <details class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <summary class="font-semibold text-slate-200 cursor-pointer hover:text-slate-100">
                        🗺️ Named Places (Rivers & Volcanoes) - Optional
                    </summary>
                    <div class="mt-4 space-y-4">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="block text-sm font-medium text-slate-300">Named Rivers</label>
                                <div class="flex gap-2">
                                    <button 
                                        onclick="window.generateNamedPlaces('rivers')"
                                        class="px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium"
                                        title="Generate river names using AI"
                                    >
                                        ✨ AI Generate
                                    </button>
                                    <button 
                                        onclick="window.addWizardNamedPlace('river')"
                                        class="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs font-medium"
                                    >
                                        + Add River
                                    </button>
                                </div>
                            </div>
                            <div id="wizard-named-rivers" class="space-y-2">
                                ${(wizardData.civilization?.named_rivers || []).map((river, idx) => `
                                    <div class="flex gap-2 items-center">
                                        <input 
                                            type="text" 
                                            value="${river.named_place_type || ''}"
                                            onchange="window.updateWizardNamedPlaceAt('river', ${idx}, 'named_place_type', this.value)"
                                            placeholder="RIVER_THAMES"
                                            class="w-1/2 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        />
                                        <input 
                                            type="text" 
                                            value="${river.localizations?.[0]?.name || ''}"
                                            onchange="window.updateWizardNamedPlaceNameAt('river', ${idx}, this.value)"
                                            placeholder="Thames"
                                            class="flex-1 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        />
                                        <button 
                                            onclick="window.removeWizardNamedPlace('river', ${idx})"
                                            class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                                        >
                                            ×
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="block text-sm font-medium text-slate-300">Named Volcanoes</label>
                                <div class="flex gap-2">
                                    <button 
                                        onclick="window.generateNamedPlaces('volcanoes')"
                                        class="px-2 py-1 bg-purple-600 hover:bg-purple-700 rounded text-xs font-medium"
                                        title="Generate volcano names using AI"
                                    >
                                        ✨ AI Generate
                                    </button>
                                    <button 
                                        onclick="window.addWizardNamedPlace('volcano')"
                                        class="px-2 py-1 bg-blue-600 hover:bg-blue-700 rounded text-xs font-medium"
                                    >
                                        + Add Volcano
                                    </button>
                                </div>
                            </div>
                            <div id="wizard-named-volcanoes" class="space-y-2">
                                ${(wizardData.civilization?.named_volcanoes || []).map((volcano, idx) => `
                                    <div class="flex gap-2 items-center">
                                        <input 
                                            type="text" 
                                            value="${volcano.named_place_type || ''}"
                                            onchange="window.updateWizardNamedPlaceAt('volcano', ${idx}, 'named_place_type', this.value)"
                                            placeholder="VOLCANO_VESUVIUS"
                                            class="w-1/2 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        />
                                        <input 
                                            type="text" 
                                            value="${volcano.localizations?.[0]?.name || ''}"
                                            onchange="window.updateWizardNamedPlaceNameAt('volcano', ${idx}, this.value)"
                                            placeholder="Mount Vesuvius"
                                            class="flex-1 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
                                        />
                                        <button 
                                            onclick="window.removeWizardNamedPlace('volcano', ${idx})"
                                            class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
                                        >
                                            ×
                                        </button>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <p class="text-xs text-slate-500">Custom names for rivers and volcanoes on your civilization's home continent</p>
                    </div>
                </details>
                
                <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 class="font-semibold text-slate-200 mb-4">Visual Styles</h4>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">🏰 Palace/Capital Building Style</label>
                            <select 
                                id="wizard-building-culture-palace" 
                                onchange="window.updateWizardBuildingCulturePalace(this.value)"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select palace style...</option>
                            </select>
                            <p class="text-xs text-slate-500 mt-1">Distinctive visual theme for your capital and palace buildings. <strong>Must match your civilization's era or it will render as default Greek style.</strong></p>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">🏘️ Building Material</label>
                            <select 
                                id="wizard-building-culture-ages" 
                                onchange="window.updateWizardBuildingCultureAges(this.value)"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            >
                                <option value="">Select building material...</option>
                            </select>
                            <p class="text-xs text-slate-500 mt-1">Base material (Stone, Mud, etc.) scaled across all eras</p>
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
                
                <details id="wizard-details-starting-location" class="bg-slate-900/50 p-4 rounded-lg border border-slate-700" ${startLocTemplate}>
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
                
                <details id="wizard-details-age-transitions" class="bg-slate-900/50 p-4 rounded-lg border border-slate-700" ${ageTransTemplate}>
                    <summary class="font-semibold text-slate-200 cursor-pointer hover:text-slate-100">
                        🔄 Age Transitions (Optional)
                    </summary>
                    <div class="mt-4">
                        <div class="mb-4 p-3 bg-blue-900/30 border border-blue-700 rounded text-xs text-slate-300">
                            <p><strong>Civilization Unlocks:</strong> Define which civilizations can be unlocked in future ages.</p>
                            <ul class="list-disc list-inside mt-2 text-slate-400 space-y-1">
                                <li>Select the age and target civilization - names and icons are auto-generated</li>
                                <li>Optionally add an <strong>unlock reason</strong> tooltip (e.g., "Carthage and Spain were both Mediterranean powers")</li>
                            </ul>
                        </div>
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
                                                onchange="window.updateWizardCivUnlockAt(${idx}, 'age_type', this.value); window.updateCivUnlockTargetOptions(${idx})"
                                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                            >
                                                <option value="">Loading...</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label class="block text-xs font-medium text-slate-300 mb-1">Target Civilization</label>
                                            <select 
                                                id="wizard-unlock-target-${idx}"
                                                onchange="window.autoFillCivUnlock(${idx}, this.value)"
                                                class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                            >
                                                <option value="">Loading civilizations...</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div>
                                        <label class="block text-xs font-medium text-slate-300 mb-1">Unlock Reason (Optional) <span class="text-slate-500">- e.g., "Carthage and Spain were both Mediterranean powers"</span></label>
                                        <textarea 
                                            onchange="window.updateWizardCivUnlockAt(${idx}, 'unlock_reason', this.value)"
                                            placeholder="Explain why this civilization unlocks (optional)"
                                            rows="2"
                                            class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                                        >${unlock.unlock_reason || ''}</textarea>
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

    // Filter palace cultures by the selected era
    const selectedEra = wizardData.action_group?.action_group_id;
    createWizardDropdown(
        'wizard-building-culture-palace',
        'building-cultures-palace',
        wizardData.civilization?.vis_art_building_cultures?.[0] || '',
        'Select palace style...',
        selectedEra  // Pass era filter
    );
    createWizardDropdown(
        'wizard-building-culture-ages',
        'building-culture-bases',
        wizardData.civilization?.building_culture_base || '',
        'Select building material...'
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
        // Populate target civilization dropdown after age is set
        updateCivUnlockTargetOptions(idx);
    });

    // Initialize favored wonders dropdowns
    (wizardData.civilization?.civilization_favored_wonders || []).forEach((wonder, idx) => {
        createWizardDropdown(`wizard-wonder-${idx}`, 'wonders', wonder.favored_wonder_type || '', 'Select wonder...');
    });

    // Initialize leader bias dropdowns
    (wizardData.civilization?.leader_civilization_biases || []).forEach((bias, idx) => {
        createWizardDropdown(`wizard-leader-${idx}`, 'leaders', bias.leader_type || '', 'Select leader...');
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
    
    // If an icon path is set, ensure there's a corresponding import entry
    if (value && value.trim()) {
        if (!wizardData.imports) {
            wizardData.imports = [];
        }
        
        // Remove old civilization icon imports (both new format with type and old format)
        wizardData.imports = wizardData.imports.filter(
            imp => !imp.id?.includes('civilization_icon') && !imp.source_path?.includes('generated_icons/icon_civilization_')
        );
        
        // Only create an import entry if one doesn't already exist for this path
        const importExists = wizardData.imports.some(
            imp => imp.source_path === value
        );
        
        if (!importExists) {
            // Create a manual import entry for this path
            // For relative icon paths like "icons/icon_uploaded_1769131114478",
            // we need to construct the source path (the actual file location)
            let sourcePathForImport = value;
            
            // If it looks like a relative path, try to resolve to generated_icons
            if (!value.includes('generated_icons') && !value.startsWith('/')) {
                // Extract just the filename part
                const fileName = value.split('/').pop();
                // Assume it's in generated_icons folder
                sourcePathForImport = `generated_icons/${fileName}.png`;
            }
            
            const cleanName = value.split('/').pop() || 'civilization_icon';
            
            wizardData.imports.push({
                id: `civilization_icon_manual_${Date.now()}`,
                source_path: sourcePathForImport,
                target_name: cleanName,
            });
        }
    }
    
    markDirty();
}

/**
 * Handle civilization icon file upload
 */
export async function handleCivIconUpload(inputElement) {
    const file = inputElement.files?.[0];
    if (!file) return;

    // Validate file is an image
    if (!file.type.startsWith('image/')) {
        const { showToast } = await import('../ui.js');
        showToast('❌ Please select a valid image file', 'error');
        return;
    }

    try {
        const { showToast } = await import('../ui.js');
        showToast('📤 Uploading icon...', 'info');

        // Create FormData for file upload
        const formData = new FormData();
        formData.append('file', file);
        formData.append('icon_type', 'civilization');  // Specify icon type

        const response = await fetch('/api/icons/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Upload failed');
        }

        const result = await response.json();
        
        if (result.success) {
            // Update the icon path field (same as generate handler)
            const iconInput = document.getElementById('wizard-civ-icon');
            if (iconInput) {
                iconInput.value = result.icon_path;
                iconInput.dispatchEvent(new Event('change'));
            }
            
            // Update wizardData imports
            const { wizardData } = await import('../state.js');
            
            if (!wizardData.imports) {
                wizardData.imports = [];
            }
            
            // Remove old civilization icon imports (both new format with type and old format)
            // Check both ID pattern and source_path pattern to handle legacy uploads
            wizardData.imports = wizardData.imports.filter(
                imp => !imp.id?.includes('civilization_icon') && !imp.source_path?.includes('generated_icons/icon_civilization_')
            );
            
            // Add new import entry
            wizardData.imports.push(result.import_entry);
            
            // SYNC to currentData so export gets the updated imports
            const { syncWizardToCurrentData } = await import('../state.js');
            syncWizardToCurrentData();
            
            markDirty();
            showToast(`✅ Icon uploaded successfully!`, 'success');
        } else {
            throw new Error(result.error || 'Upload failed');
        }
    } catch (error) {
        const { showToast } = await import('../ui.js');
        console.error('[ICON_UPLOAD_ERROR]', error);
        showToast(`❌ Upload failed: ${error.message}`, 'error');
    } finally {
        // Reset file input
        inputElement.value = '';
    }
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

export function updateWizardBuildingCulturePalace(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.vis_art_building_cultures) {
        wizardData.civilization.vis_art_building_cultures = [];
    }
    wizardData.civilization.vis_art_building_cultures[0] = value || '';
    markDirty();
}

export function updateWizardBuildingCultureAges(value) {
    if (!wizardData.civilization) wizardData.civilization = {};
    wizardData.civilization.building_culture_base = value || '';
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
    
    // Instead of full re-render, just add the new item to the DOM
    const container = document.getElementById('wizard-terrain-biases');
    if (container) {
        const newIdx = wizardData.civilization.start_bias_terrains.length - 1;
        const newItem = document.createElement('div');
        newItem.className = 'flex gap-2 items-center';
        newItem.innerHTML = `
            <select 
                id="wizard-terrain-type-${newIdx}"
                onchange="window.updateWizardTerrainBiasAt(${newIdx}, 'terrain_type', this.value)"
                class="flex-1 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
            >
                <option value="">Loading...</option>
            </select>
            <input 
                type="number" 
                value=""
                onchange="window.updateWizardTerrainBiasAt(${newIdx}, 'score', parseInt(this.value) || 0)"
                placeholder="Score"
                class="w-20 px-2 py-1 bg-slate-800 border border-slate-600 rounded text-sm"
            />
            <button 
                onclick="window.removeWizardTerrainBias(${newIdx})"
                class="px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
            >
                ×
            </button>
        `;
        container.appendChild(newItem);
        
        // Load terrain types for the new dropdown
        import('../form/fields.js').then(m => {
            m.getAutocompleteOptions('terrain_type').then(options => {
                const select = newItem.querySelector(`#wizard-terrain-type-${newIdx}`);
                if (select) {
                    select.innerHTML = options.map(opt => `<option value="${opt}">${opt}</option>`).join('');
                }
            });
        });
    }
    
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
        age_type: 'AGE_ANTIQUITY',
        type: '',
        kind: 'KIND_CIVILIZATION',
        name: '',
        description: '',
        icon: '',
    });
    
    // Instead of full re-render, just add the new item to the DOM
    const container = document.getElementById('wizard-civ-unlocks');
    if (container) {
        const newIdx = wizardData.civilization.civilization_unlocks.length - 1;
        const unlock = wizardData.civilization.civilization_unlocks[newIdx];
        
        const newItem = document.createElement('div');
        newItem.className = 'p-3 bg-slate-800/50 rounded border border-slate-600 space-y-2';
        newItem.innerHTML = `
            <div class="grid grid-cols-2 gap-2">
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Age</label>
                    <select 
                        id="wizard-unlock-age-${newIdx}"
                        onchange="window.updateWizardCivUnlockAt(${newIdx}, 'age_type', this.value); window.updateCivUnlockTargetOptions(${newIdx})"
                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                    >
                        <option value="">Loading...</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Target Civilization</label>
                    <select 
                        id="wizard-unlock-target-${newIdx}"
                        onchange="window.autoFillCivUnlock(${newIdx}, this.value)"
                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                    >
                        <option value="">Loading civilizations...</option>
                    </select>
                </div>
            </div>
            <div>
                <label class="block text-xs font-medium text-slate-300 mb-1">Unlock Reason (Optional) <span class="text-slate-500">- e.g., "Carthage and Spain were both Mediterranean powers"</span></label>
                <textarea 
                    onchange="window.updateWizardCivUnlockAt(${newIdx}, 'unlock_reason', this.value)"
                    placeholder="Explain why this civilization unlocks (optional)"
                    rows="2"
                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm"
                ></textarea>
            </div>
            <button 
                onclick="window.removeWizardCivUnlock(${newIdx})"
                class="w-full px-2 py-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-xs"
            >
                Remove
            </button>
        `;
        container.appendChild(newItem);
        
        // Load age types for the new age dropdown
        import('../form/fields.js').then(m => {
            m.getAutocompleteOptions('age_type').then(options => {
                const select = newItem.querySelector(`#wizard-unlock-age-${newIdx}`);
                if (select) {
                    select.innerHTML = options.map(opt => `<option value="${opt}" ${opt === 'AGE_ANTIQUITY' ? 'selected' : ''}>${opt}</option>`).join('');
                    // Now that age is set, load civilizations for that age
                    window.updateCivUnlockTargetOptions(newIdx);
                }
            });
        });
        
        // Expose function to update target civilization options
        window.updateCivUnlockTargetOptions = updateCivUnlockTargetOptions;
    }
    
    markDirty();
}

function updateCivUnlockTargetOptions(idx) {
    const ageSelect = document.getElementById(`wizard-unlock-age-${idx}`);
    const targetSelect = document.getElementById(`wizard-unlock-target-${idx}`);
    
    if (!ageSelect || !targetSelect) return;
    
    const selectedAge = ageSelect.value;
    const currentValue = wizardData.civilization?.civilization_unlocks?.[idx]?.type || '';
    
    // Fetch all civilizations and filter by age
    fetch('/api/data/civilizations')
        .then(res => res.json())
        .then(data => {
            const civs = data.values || [];
            const filteredCivs = selectedAge 
                ? civs.filter(civ => civ.age === selectedAge)
                : civs;
            
            targetSelect.innerHTML = filteredCivs
                .map(civ => `<option value="${civ.id}" ${civ.id === currentValue ? 'selected' : ''}>${civ.id}</option>`)
                .join('');
        })
        .catch(err => {
            console.error('Failed to load civilizations:', err);
            targetSelect.innerHTML = '<option value="">Error loading civilizations</option>';
        });
}

export function autoFillCivUnlock(idx, civType) {
    if (wizardData.civilization?.civilization_unlocks?.[idx]) {
        const unlock = wizardData.civilization.civilization_unlocks[idx];
        unlock.type = civType;
        unlock.name = `LOC_${civType}_NAME`;
        unlock.description = `LOC_${civType}_DESCRIPTION`;
        unlock.icon = civType;
        unlock.kind = 'KIND_CIVILIZATION';
        markDirty();
    }
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

// ============================================================================
// Citizen Names CRUD
// ============================================================================

export function addWizardCitizenName(gender) {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.localizations) wizardData.civilization.localizations = [{}];
    if (!wizardData.civilization.localizations[0].citizen_names) {
        wizardData.civilization.localizations[0].citizen_names = { male: [], female: [] };
    }
    
    wizardData.civilization.localizations[0].citizen_names[gender].push('');
    rerenderStep2();
    markDirty();
}

export function updateWizardCitizenNameAt(gender, idx, value) {
    if (wizardData.civilization?.localizations?.[0]?.citizen_names?.[gender]?.[idx] !== undefined) {
        wizardData.civilization.localizations[0].citizen_names[gender][idx] = value;
        markDirty();
    }
}

export function removeWizardCitizenName(gender, idx) {
    if (wizardData.civilization?.localizations?.[0]?.citizen_names?.[gender]) {
        wizardData.civilization.localizations[0].citizen_names[gender].splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

export async function generateCitizenNames() {
    const civName = wizardData.civilization?.localizations?.[0]?.name || 'Generic';
    const adjective = wizardData.civilization?.localizations?.[0]?.adjective || civName;
    const settings = getSettings();
    
    if (!settings.openai?.apiKey) {
        showToast('Please set your OpenAI API key in Settings first', 'error');
        return;
    }
    
    const dismissLoading = showLoadingToast('Generating citizen names using AI...');
    
    try {
        const response = await fetch('/api/citizens/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                civilization_name: civName,
                adjective: adjective,
                count: 10,
                api_key: settings.openai.apiKey
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate citizen names');
        }
        
        const data = await response.json();
        
        if (!wizardData.civilization) wizardData.civilization = {};
        if (!wizardData.civilization.localizations) wizardData.civilization.localizations = [{}];
        wizardData.civilization.localizations[0].citizen_names = {
            male: data.male_names || [],
            female: data.female_names || []
        };
        
        rerenderStep2();
        markDirty();
        dismissLoading();
        showToast(`✅ Generated ${data.male_names.length} male and ${data.female_names.length} female names`, 'success');
    } catch (error) {
        console.error('Failed to generate citizen names:', error);
        dismissLoading();
        showToast(`❌ ${error.message || 'Failed to generate citizen names. Check your OpenAI API key in settings.'}`, 'error');
    }
}

export async function generateNamedPlaces(placeType) {
    const civName = wizardData.civilization?.localizations?.[0]?.name || 'Generic';
    const adjective = wizardData.civilization?.localizations?.[0]?.adjective || civName;
    const settings = getSettings();
    
    if (!settings.openai?.apiKey) {
        showToast('Please set your OpenAI API key in Settings first', 'error');
        return;
    }
    
    const placeLabel = placeType === 'rivers' ? 'rivers' : 'volcanoes';
    const dismissLoading = showLoadingToast(`Generating ${placeLabel} using AI...`);
    
    try {
        const response = await fetch('/api/named-places/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                civilization_name: civName,
                adjective: adjective,
                place_type: placeType,
                count: 5,
                api_key: settings.openai.apiKey
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Failed to generate ${placeLabel}`);
        }
        
        const data = await response.json();
        
        if (!wizardData.civilization) wizardData.civilization = {};
        
        // Determine which array to update
        const arrayKey = placeType === 'rivers' ? 'named_rivers' : 'named_volcanoes';
        
        // Replace the array with generated places
        wizardData.civilization[arrayKey] = (data.places || []).map(place => ({
            named_place_type: place.type_id,
            localizations: [{
                name: place.name
            }]
        }));
        
        rerenderStep2();
        markDirty();
        dismissLoading();
        showToast(`✅ Generated ${data.places.length} ${placeLabel}`, 'success');
    } catch (error) {
        console.error(`Failed to generate ${placeLabel}:`, error);
        dismissLoading();
        showToast(`❌ ${error.message || `Failed to generate ${placeLabel}. Check your OpenAI API key in settings.`}`, 'error');
    }
}

// ============================================================================
// Favored Wonders CRUD
// ============================================================================

export function addWizardFavoredWonder() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.civilization_favored_wonders) {
        wizardData.civilization.civilization_favored_wonders = [];
    }
    
    wizardData.civilization.civilization_favored_wonders.push({
        favored_wonder_type: '',
        favored_wonder_name: ''
    });
    rerenderStep2();
    markDirty();
}

export function autoFillFavoredWonder(idx, wonderType) {
    if (wizardData.civilization?.civilization_favored_wonders?.[idx]) {
        const wonder = wizardData.civilization.civilization_favored_wonders[idx];
        wonder.favored_wonder_type = wonderType;
        wonder.favored_wonder_name = `LOC_${wonderType}_NAME`;
        markDirty();
    }
}

export function removeWizardFavoredWonder(idx) {
    if (wizardData.civilization?.civilization_favored_wonders) {
        wizardData.civilization.civilization_favored_wonders.splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

// ============================================================================
// Leader Civilization Bias CRUD
// ============================================================================

export function addWizardLeaderBias() {
    if (!wizardData.civilization) wizardData.civilization = {};
    if (!wizardData.civilization.leader_civilization_biases) {
        wizardData.civilization.leader_civilization_biases = [];
    }
    
    wizardData.civilization.leader_civilization_biases.push({
        leader_type: '',
        bias: 2,
        reason_type: '',
        choice_type: 'LOC_CREATE_GAME_GEOGRAPHIC_CHOICE'
    });
    rerenderStep2();
    markDirty();
}

export function autoFillLeaderBias(idx, leaderType) {
    if (wizardData.civilization?.leader_civilization_biases?.[idx]) {
        const bias = wizardData.civilization.leader_civilization_biases[idx];
        const civType = wizardData.civilization.civilization_type || 'CIVILIZATION_CUSTOM';
        const civShortName = civType.replace('CIVILIZATION_', '');
        const leaderShortName = leaderType.replace('LEADER_', '');
        
        bias.leader_type = leaderType;
        bias.reason_type = `LOC_UNLOCK_PLAY_AS_${leaderShortName}_${civShortName}_TOOLTIP`;
        markDirty();
    }
}

export function updateWizardLeaderBiasAt(idx, field, value) {
    if (wizardData.civilization?.leader_civilization_biases?.[idx]) {
        wizardData.civilization.leader_civilization_biases[idx][field] = value;
        markDirty();
    }
}

export function removeWizardLeaderBias(idx) {
    if (wizardData.civilization?.leader_civilization_biases) {
        wizardData.civilization.leader_civilization_biases.splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

// ============================================================================
// Named Places CRUD
// ============================================================================

export function addWizardNamedPlace(type) {
    if (!wizardData.civilization) wizardData.civilization = {};
    const arrayName = type === 'river' ? 'named_rivers' : 'named_volcanoes';
    
    if (!wizardData.civilization[arrayName]) {
        wizardData.civilization[arrayName] = [];
    }
    
    wizardData.civilization[arrayName].push({
        named_place_type: '',
        localizations: [{ name: '' }]
    });
    rerenderStep2();
    markDirty();
}

export function updateWizardNamedPlaceAt(type, idx, field, value) {
    const arrayName = type === 'river' ? 'named_rivers' : 'named_volcanoes';
    if (wizardData.civilization?.[arrayName]?.[idx]) {
        wizardData.civilization[arrayName][idx][field] = value;
        markDirty();
    }
}

export function updateWizardNamedPlaceNameAt(type, idx, value) {
    const arrayName = type === 'river' ? 'named_rivers' : 'named_volcanoes';
    if (wizardData.civilization?.[arrayName]?.[idx]) {
        if (!wizardData.civilization[arrayName][idx].localizations) {
            wizardData.civilization[arrayName][idx].localizations = [{}];
        }
        wizardData.civilization[arrayName][idx].localizations[0].name = value;
        markDirty();
    }
}

export function removeWizardNamedPlace(type, idx) {
    const arrayName = type === 'river' ? 'named_rivers' : 'named_volcanoes';
    if (wizardData.civilization?.[arrayName]) {
        wizardData.civilization[arrayName].splice(idx, 1);
        rerenderStep2();
        markDirty();
    }
}

// Expose all wizard functions to window for onclick handlers
if (typeof window !== 'undefined') {
    window.updateCivilization = updateCivilization;
    window.updateWizardCivLocalization = updateWizardCivLocalization;
    window.updateWizardIconPath = updateWizardIconPath;
    window.handleCivIconUpload = handleCivIconUpload;
    window.updateWizardBuildingCulturePalace = updateWizardBuildingCulturePalace;
    window.updateWizardBuildingCultureAges = updateWizardBuildingCultureAges;
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
    window.autoFillCivUnlock = autoFillCivUnlock;
    window.updateWizardCivUnlockAt = updateWizardCivUnlockAt;
    window.removeWizardCivUnlock = removeWizardCivUnlock;
    window.updateCivUnlockTargetOptions = updateCivUnlockTargetOptions;
    window.addWizardTerrainBias = addWizardTerrainBias;
    window.updateWizardTerrainBiasAt = updateWizardTerrainBiasAt;
    window.removeWizardTerrainBias = removeWizardTerrainBias;
    // Citizen names
    window.addWizardCitizenName = addWizardCitizenName;
    window.updateWizardCitizenNameAt = updateWizardCitizenNameAt;
    window.removeWizardCitizenName = removeWizardCitizenName;
    window.generateCitizenNames = generateCitizenNames;
    // Favored wonders
    window.addWizardFavoredWonder = addWizardFavoredWonder;
    window.autoFillFavoredWonder = autoFillFavoredWonder;
    window.removeWizardFavoredWonder = removeWizardFavoredWonder;
    // Leader biases
    window.addWizardLeaderBias = addWizardLeaderBias;
    window.autoFillLeaderBias = autoFillLeaderBias;
    window.updateWizardLeaderBiasAt = updateWizardLeaderBiasAt;
    window.removeWizardLeaderBias = removeWizardLeaderBias;
    // Named places
    window.addWizardNamedPlace = addWizardNamedPlace;
    window.updateWizardNamedPlaceAt = updateWizardNamedPlaceAt;
    window.updateWizardNamedPlaceNameAt = updateWizardNamedPlaceNameAt;
    window.removeWizardNamedPlace = removeWizardNamedPlace;
    window.generateNamedPlaces = generateNamedPlaces;
    // Note: addWizardStartBiasTerrain, removeWizardStartBiasRiver, addWizardStartBiasRiver not implemented
}
