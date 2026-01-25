/**
 * Wizard Step 4 - Modifiers & Traditions
 */

import { wizardData, markDirty } from '../state.js';
import { showToast } from '../ui.js';
import { createWizardDropdown } from './wizard.js';

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
                        + Tradition
                    </button>
                </div>
                
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
                        `).join('')}
                    </div>
                ` : '<p class="text-slate-400 text-sm py-4">No traditions added yet</p>'}
                
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
                                onclick="window.wizardSaveTradition()"
                                id="wizard-tradition-form-save"
                                class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                            >
                                Save
                            </button>
                            <button 
                                onclick="window.wizardCancelTraditionForm()"
                                id="wizard-tradition-form-cancel"
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


/* attachStep4Listeners removed as we use inline onclick handlers */


export function wizardShowModifierForm() {
    const form = document.getElementById('wizard-modifier-form');
    const idxInput = document.getElementById('wizard-modifier-edit-idx');

    document.getElementById('wizard-modifier-id').value = '';
    document.getElementById('wizard-modifier-type').value = '';
    document.getElementById('wizard-modifier-permanent').checked = false;
    document.getElementById('wizard-modifier-runonce').checked = false;
    document.getElementById('wizard-modifier-desc').value = '';
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

export function wizardEditModifier(idx) {
    const modifier = wizardData.modifiers[idx];
    document.getElementById('wizard-modifier-id').value = modifier.id || '';
    document.getElementById('wizard-modifier-type').value = modifier.modifier_type || '';
    document.getElementById('wizard-modifier-permanent').checked = modifier.modifier?.permanent || false;
    document.getElementById('wizard-modifier-runonce').checked = modifier.modifier?.run_once || false;
    document.getElementById('wizard-modifier-desc').value = modifier.localizations?.[0]?.description || '';

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

    // Clear and populate requirements
    const requirementsContainer = document.getElementById('wizard-modifier-requirements-container');
    requirementsContainer.innerHTML = '';
    
    if (modifier.modifier?.requirements && Array.isArray(modifier.modifier.requirements)) {
        modifier.modifier.requirements.forEach((req, reqIdx) => {
            wizardAddRequirement();
            
            // Wait for the requirement to be added, then populate it
            setTimeout(() => {
                const reqDiv = requirementsContainer.querySelector(`[data-req-idx="${reqIdx}"]`);
                if (reqDiv) {
                    const typeSelect = reqDiv.querySelector('.wizard-req-type');
                    
                    // Load and set the requirement type
                    import('../data/loader.js').then(loader => {
                        loader.loadReferenceData('requirement-types').then(data => {
                            typeSelect.innerHTML = '<option value="">Select requirement type...</option>';
                            if (data && data.values) {
                                data.values.forEach(item => {
                                    const option = document.createElement('option');
                                    option.value = item.id;
                                    option.textContent = item.id;
                                    if (item.id === req.type) {
                                        option.selected = true;
                                    }
                                    typeSelect.appendChild(option);
                                });
                            }
                        });
                    });
                    
                    // Populate requirement arguments
                    if (req.arguments && Array.isArray(req.arguments)) {
                        req.arguments.forEach(arg => {
                            wizardAddRequirementArg(reqIdx);
                            
                            setTimeout(() => {
                                const argsContainer = reqDiv.querySelector('.wizard-req-args-container');
                                const argDivs = argsContainer.querySelectorAll('[data-arg-idx]');
                                const lastArgDiv = argDivs[argDivs.length - 1];
                                
                                if (lastArgDiv) {
                                    const nameInput = lastArgDiv.querySelector('.wizard-req-arg-name');
                                    const valueInput = lastArgDiv.querySelector('.wizard-req-arg-value');
                                    
                                    if (nameInput) nameInput.value = arg.name || '';
                                    if (valueInput) valueInput.value = arg.value || '';
                                }
                            }, 50);
                        });
                    }
                }
            }, 100);
        });
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

export function wizardShowTraditionForm() {
    const form = document.getElementById('wizard-tradition-form');
    const idxInput = document.getElementById('wizard-tradition-edit-idx');

    document.getElementById('wizard-tradition-id').value = '';
    document.getElementById('wizard-tradition-type').value = '';
    document.getElementById('wizard-tradition-name').value = '';
    document.getElementById('wizard-tradition-desc').value = '';
    idxInput.value = '-1';

    form.classList.remove('hidden');
    document.getElementById('wizard-tradition-id').focus();
}

export function wizardCancelTraditionForm() {
    const form = document.getElementById('wizard-tradition-form');
    form.classList.add('hidden');
    document.getElementById('wizard-tradition-id').value = '';
    document.getElementById('wizard-tradition-type').value = '';
    document.getElementById('wizard-tradition-name').value = '';
    document.getElementById('wizard-tradition-desc').value = '';
    document.getElementById('wizard-tradition-edit-idx').value = '-1';
}

export function wizardSaveTradition() {
    const id = document.getElementById('wizard-tradition-id').value.trim();
    const type = document.getElementById('wizard-tradition-type').value.trim();
    const displayName = document.getElementById('wizard-tradition-name').value.trim();
    const description = document.getElementById('wizard-tradition-desc').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-tradition-edit-idx').value, 10);

    if (!id) {
        showToast('Tradition ID is required', 'error');
        return;
    }
    if (!type) {
        showToast('Tradition Type is required', 'error');
        return;
    }

    if (!wizardData.traditions) {
        wizardData.traditions = [];
    }

    const tradition = {
        id: id,
        tradition_type: type,
        tradition: {},
    };

    if (displayName || description) {
        tradition.localizations = [{}];
        if (displayName) tradition.localizations[0].name = displayName;
        if (description) tradition.localizations[0].description = description;
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

export function wizardEditTradition(idx) {
    const tradition = wizardData.traditions[idx];
    document.getElementById('wizard-tradition-id').value = tradition.id || '';
    document.getElementById('wizard-tradition-type').value = tradition.tradition_type || '';
    document.getElementById('wizard-tradition-name').value = tradition.localizations?.[0]?.name || '';
    document.getElementById('wizard-tradition-desc').value = tradition.localizations?.[0]?.description || '';
    document.getElementById('wizard-tradition-edit-idx').value = idx;
    document.getElementById('wizard-tradition-form').classList.remove('hidden');
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
export function wizardAddRequirement() {
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
    import('../data/loader.js').then(loader => {
        loader.fetchReferenceData('requirement-types').then(data => {
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
        });
    });
}

/**
 * Remove a requirement from the modifier form
 */
export function wizardRemoveRequirement(reqIdx) {
    const container = document.getElementById('wizard-modifier-requirements-container');
    const reqDiv = container.querySelector(`[data-req-idx="${reqIdx}"]`);
    if (reqDiv) {
        reqDiv.remove();
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
 * Remove an argument from a requirement
 */
export function wizardRemoveRequirementArg(reqIdx, argIdx) {
    const argsContainer = document.querySelector(`.wizard-req-args-container[data-req-idx="${reqIdx}"]`);
    if (!argsContainer) return;
    
    const argDiv = argsContainer.querySelector(`[data-arg-idx="${argIdx}"]`);
    if (argDiv) {
        argDiv.remove();
    }
}
