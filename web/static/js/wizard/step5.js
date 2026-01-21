/**
 * Wizard Step 5 - Review & Finish
 */

import { wizardData } from '../state.js';
import { validateWizardData } from './wizard.js';

/**
 * Render Step 5: Review & Finish
 * @param {HTMLElement} container - Container element to render into
 */
export function renderWizardStep5(container) {
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
