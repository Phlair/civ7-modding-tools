/**
 * Wizard Step 1 - Basic Information
 * Metadata, module localization, and starting age
 */

import { wizardData, markDirty } from '../state.js';

/**
 * Render Step 1: Basic Information
 * @param {HTMLElement} container - Container element to render into
 */
export function renderWizardStep1(container) {
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
                                <button onclick="import('./wizard.js').then(m => m.showFieldHelp('mod_id'))" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <input 
                                type="text" 
                                id="wizard-metadata-id" 
                                value="${wizardData.metadata?.id || ''}"
                                onchange="import('./step1.js').then(m => m.updateMetadata('id', this.value))"
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
                                onchange="import('./step1.js').then(m => m.updateMetadata('version', this.value))"
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
                                onchange="import('./step1.js').then(m => m.updateMetadata('name', this.value))"
                                placeholder="My Civilization Mod"
                                class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                            />
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-300 mb-1">Description</label>
                            <textarea 
                                id="wizard-metadata-description" 
                                onchange="import('./step1.js').then(m => m.updateMetadata('description', this.value))"
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
                                onchange="import('./step1.js').then(m => m.updateMetadata('authors', this.value))"
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
                                    onchange="import('./step1.js').then(m => m.updateModuleLocalization('name', this.value))"
                                    placeholder="Display name in-game"
                                    class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-slate-300 mb-1">Module Description</label>
                                <textarea 
                                    id="wizard-module-description" 
                                    onchange="import('./step1.js').then(m => m.updateModuleLocalization('description', this.value))"
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
                                <button onclick="import('./wizard.js').then(m => m.showFieldHelp('age_type'))" class="ml-1 text-blue-400 hover:text-blue-300">ⓘ</button>
                            </label>
                            <select 
                                id="wizard-age-type" 
                                onchange="import('./step1.js').then(m => m.updateActionGroup('action_group_id', this.value))"
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

/**
 * Update metadata field
 * @param {string} field - Field name
 * @param {string} value - Field value
 */
export function updateMetadata(field, value) {
    if (!wizardData.metadata) {
        wizardData.metadata = {};
    }
    wizardData.metadata[field] = value;
    if (field === 'id' && value) {
        const pascal_case = String(value)
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join('');
        wizardData.metadata.package = pascal_case || value;
    }
    markDirty();
}

/**
 * Update module localization field
 * @param {string} field - Field name
 * @param {string} value - Field value
 */
export function updateModuleLocalization(field, value) {
    if (!wizardData.module_localization) {
        wizardData.module_localization = {};
    }
    wizardData.module_localization[field] = value;
    markDirty();
}

/**
 * Update action group field
 * @param {string} field - Field name
 * @param {string} value - Field value
 */
export function updateActionGroup(field, value) {
    if (!wizardData.action_group) {
        wizardData.action_group = {};
    }
    wizardData.action_group[field] = value;
    markDirty();
}
