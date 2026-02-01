/**
 * Progression Tree Node Editor for Wizard Step 4
 * 
 * Provides a visual drag-and-drop tree builder for unique civilization progression trees.
 */

import { wizardData, markDirty } from '../state.js';
import { showToast } from '../ui.js';
import { fetchReferenceData } from '../data/loader.js';

// Cache for reference data
let cachedQuotes = null;
let cachedAdvisoryTypes = null;
let cachedAgeProgressionModifiers = null; // {AGE_ANTIQUITY: {...}, AGE_EXPLORATION: {...}, AGE_MODERN: {...}}

/**
 * Render progression tree section for Step 4
 * @param {HTMLElement} container - Container element to render into
 * @returns {string} HTML for the progression tree section
 */
export function renderProgressionTreeSection() {
    const hasNodes = wizardData.progression_tree_nodes && wizardData.progression_tree_nodes.length > 0;
    
    // Ensure functions are available globally for onclick handlers
    if (typeof window !== 'undefined') {
        window.wizardShowTreeNodeForm = wizardShowTreeNodeForm;
        window.wizardEditTreeNode = wizardEditTreeNode;
        window.removeWizardTreeNode = removeWizardTreeNode;
        window.wizardSaveTreeNode = wizardSaveTreeNode;
        window.wizardCancelTreeNodeForm = wizardCancelTreeNodeForm;
        window.wizardOnQuoteSelect = wizardOnQuoteSelect;
        window.wizardAddUnlock = wizardAddUnlock;
        window.wizardRemoveUnlock = wizardRemoveUnlock;
        window.wizardMoveNodeUp = wizardMoveNodeUp;
        window.wizardMoveNodeDown = wizardMoveNodeDown;
        window.wizardToggleModifierInput = wizardToggleModifierInput;
        window.wizardToggleModifierPreset = wizardToggleModifierPreset;
    }
    
    return `
        <div class="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
            <div class="flex items-center justify-between mb-4">
                <h4 class="font-semibold text-slate-200 flex items-center gap-2">
                    <span class="inline-block w-2 h-2 rounded-full bg-purple-500"></span>
                    Unique Progression Tree (${wizardData.progression_tree_nodes?.length || 0} nodes)
                </h4>
                <button 
                    onclick="window.wizardShowTreeNodeForm()"
                    class="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium"
                >
                    + Add Node
                </button>
            </div>
            
            <p class="text-xs text-slate-400 mb-4">
                Create a unique civic/tech tree for your civilization. Nodes unlock units, buildings, traditions, and modifiers. 
                Nodes are arranged vertically with prerequisites showing connections.
            </p>
            
            ${hasNodes ? renderTreeNodeList() : '<p class="text-slate-400 text-sm py-4">No tree nodes added yet</p>'}
            
            <div id="wizard-tree-node-form" class="hidden bg-slate-800 p-4 rounded border border-slate-600 mt-4">
                ${renderTreeNodeForm()}
            </div>
        </div>
    `;
}

/**
 * Render the list of tree nodes with visual connections
 */
function renderTreeNodeList() {
    const nodes = wizardData.progression_tree_nodes || [];
    
    return `
        <div class="space-y-1">
            ${nodes.map((node, idx) => {
                const prereqIdxs = node.prereq_node_indices || [];
                const hasPrereqs = prereqIdxs.length > 0;
                const unlockCount = node.unlocks?.length || 0;
                
                return `
                    <!-- Connection lines if there are prerequisites -->
                    ${hasPrereqs ? `
                        <div class="flex items-center pl-8 h-4">
                            ${prereqIdxs.map(prereqIdx => {
                                const isDirectAbove = prereqIdx === idx - 1;
                                return `
                                    <div class="relative flex-1">
                                        ${isDirectAbove ? `
                                            <div class="absolute left-0 right-0 top-0 border-l-2 border-purple-500/50 h-full ml-4"></div>
                                        ` : `
                                            <svg class="w-full h-full" style="position: absolute;">
                                                <path 
                                                    d="M ${(prereqIdx + 1) * 20} 0 L ${(prereqIdx + 1) * 20} 8 L ${(idx + 1) * 20} 16" 
                                                    stroke="rgb(168 85 247 / 0.5)" 
                                                    stroke-width="2" 
                                                    fill="none"
                                                />
                                            </svg>
                                        `}
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    ` : ''}
                    
                    <!-- Node card -->
                    <div class="p-3 bg-slate-800/70 rounded border-l-4 ${hasPrereqs ? 'border-purple-500' : 'border-slate-600'} flex items-start gap-3">
                        <div class="flex flex-col gap-1">
                            <button 
                                onclick="window.wizardMoveNodeUp(${idx})"
                                ${idx === 0 ? 'disabled' : ''}
                                class="px-1.5 py-0.5 text-xs bg-slate-700 hover:bg-slate-600 disabled:opacity-30 disabled:cursor-not-allowed rounded text-slate-300"
                                title="Move up"
                            >
                                ↑
                            </button>
                            <button 
                                onclick="window.wizardMoveNodeDown(${idx})"
                                ${idx === nodes.length - 1 ? 'disabled' : ''}
                                class="px-1.5 py-0.5 text-xs bg-slate-700 hover:bg-slate-600 disabled:opacity-30 disabled:cursor-not-allowed rounded text-slate-300"
                                title="Move down"
                            >
                                ↓
                            </button>
                        </div>
                        
                        <div class="flex-1">
                            <div class="flex items-center justify-between mb-1">
                                <p class="font-medium text-sm">${node.localizations?.[0]?.name || 'Unnamed Node'}</p>
                                <div class="flex gap-1">
                                    <button 
                                        onclick="window.wizardEditTreeNode(${idx})"
                                        class="px-2 py-1 text-xs bg-blue-600/30 hover:bg-blue-600/50 border border-blue-600 rounded text-blue-300"
                                    >
                                        Edit
                                    </button>
                                    <button 
                                        onclick="window.removeWizardTreeNode(${idx})"
                                        class="px-2 py-1 text-xs bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                            
                            <div class="text-xs text-slate-400 space-y-0.5">
                                <p>Cost: ${node.progression_tree_node?.cost || 150} | Icon: ${node.progression_tree_node?.icon_string || 'Default'}</p>
                                ${node.quote ? `<p class="italic text-purple-300">"${node.quote.quote_text?.substring(0, 80)}..."</p>` : ''}
                                ${unlockCount > 0 ? `<p class="text-green-400">Unlocks: ${unlockCount} item(s)</p>` : ''}
                                ${hasPrereqs ? `<p class="text-purple-400">Prerequisites: ${prereqIdxs.map(i => i + 1).join(', ')}</p>` : ''}
                            </div>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

/**
 * Render the tree node edit form
 */
function renderTreeNodeForm() {
    return `
        <div class="space-y-3">
            <input type="hidden" id="wizard-tree-node-edit-idx" value="-1" />
            
            <h5 class="text-sm font-semibold text-purple-400 border-b border-slate-600 pb-2 mb-3">Node Information</h5>
            
            <div>
                <label class="block text-xs font-medium text-slate-300 mb-1">Node ID *</label>
                <input 
                    type="text" 
                    id="wizard-tree-node-id" 
                    placeholder="NODE_CIVIC_MY_CIV_FIRST_NODE"
                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                />
            </div>
            
            <div>
                <label class="block text-xs font-medium text-slate-300 mb-1">Name *</label>
                <input 
                    type="text" 
                    id="wizard-tree-node-name" 
                    placeholder="Foundation of Empire"
                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                />
            </div>
            
            <div>
                <label class="block text-xs font-medium text-slate-300 mb-1">Description</label>
                <textarea 
                    id="wizard-tree-node-desc" 
                    placeholder="Describe what this node represents"
                    rows="2"
                    class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                ></textarea>
            </div>
            
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Cost</label>
                    <input 
                        type="number" 
                        id="wizard-tree-node-cost" 
                        value="150"
                        min="0"
                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                    />
                </div>
                
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Icon String</label>
                    <input 
                        type="text" 
                        id="wizard-tree-node-icon" 
                        placeholder="Use civ icon"
                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                    />
                    <p class="text-xs text-slate-400 mt-1">Leave blank to use civilization icon</p>
                </div>
            </div>
            
            <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                <h6 class="text-xs font-semibold text-slate-400 mb-2">Quote (Optional)</h6>
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Select Quote from Library</label>
                    <select 
                        id="wizard-tree-node-quote-select" 
                        onchange="window.wizardOnQuoteSelect()"
                        class="w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-sm text-slate-100 focus:outline-none focus:border-blue-400"
                    >
                        <option value="">Loading quotes...</option>
                    </select>
                </div>
                
                <div id="wizard-tree-node-quote-preview" class="mt-2 p-2 bg-slate-800 rounded border border-slate-600 hidden">
                    <p id="wizard-tree-node-quote-text" class="text-xs italic text-purple-300 mb-1"></p>
                    <p id="wizard-tree-node-quote-author" class="text-xs text-slate-400"></p>
                </div>
            </div>
            
            <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                <h6 class="text-xs font-semibold text-slate-400 mb-2">Prerequisites</h6>
                <p class="text-xs text-slate-400 mb-2">Select which nodes must be completed before this one</p>
                <div id="wizard-tree-node-prereqs-container">
                    <!-- Checkboxes for existing nodes will appear here -->
                </div>
            </div>
            
            <div class="bg-slate-900/50 p-3 rounded border border-slate-700">
                <h6 class="text-xs font-semibold text-slate-400 mb-2">Unlocks</h6>
                <p class="text-xs text-slate-400 mb-2">What does this node unlock? (units, buildings, traditions, modifiers)</p>
                <div id="wizard-tree-node-unlocks-container" class="space-y-2 mb-2">
                    <!-- Unlocks will be added here -->
                </div>
                <button 
                    onclick="window.wizardAddUnlock()"
                    type="button"
                    class="px-2 py-1 bg-slate-700 hover:bg-slate-600 rounded text-xs font-medium text-slate-300 border border-slate-600"
                >
                    + Add Unlock
                </button>
            </div>
            
            <details class="bg-slate-900/50 rounded border border-slate-700">
                <summary class="px-3 py-2 cursor-pointer text-xs font-semibold text-slate-400 hover:text-slate-300">+ Advisory Tags (Optional)</summary>
                <div class="p-3 pt-2">
                    <div id="wizard-tree-node-advisories-container">
                        <!-- Checkboxes for advisory types will appear here -->
                    </div>
                </div>
            </details>
            
            <div class="flex gap-2 mt-4">
                <button 
                    onclick="window.wizardSaveTreeNode()"
                    class="flex-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
                >
                    Save Node
                </button>
                <button 
                    onclick="window.wizardCancelTreeNodeForm()"
                    class="flex-1 px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded text-sm font-medium"
                >
                    Cancel
                </button>
            </div>
        </div>
    `;
}

/**
 * Show the tree node form (for adding or editing)
 */
export async function wizardShowTreeNodeForm() {
    const form = document.getElementById('wizard-tree-node-form');
    form.classList.remove('hidden');
    
    // Load reference data
    await loadQuotesData();
    await loadAdvisoryTypesData();
    
    // Populate prerequisites checkboxes (existing nodes)
    populatePrereqsCheckboxes();
    
    // Focus on the first input
    document.getElementById('wizard-tree-node-id').focus();
}

/**
 * Edit an existing tree node
 */
export async function wizardEditTreeNode(idx) {
    await wizardShowTreeNodeForm();
    
    const node = wizardData.progression_tree_nodes[idx];
    document.getElementById('wizard-tree-node-edit-idx').value = idx;
    document.getElementById('wizard-tree-node-id').value = node.progression_tree_node_type || '';
    document.getElementById('wizard-tree-node-name').value = node.localizations?.[0]?.name || '';
    document.getElementById('wizard-tree-node-desc').value = node.localizations?.[0]?.description || '';
    document.getElementById('wizard-tree-node-cost').value = node.progression_tree_node?.cost || 150;
    document.getElementById('wizard-tree-node-icon').value = node.progression_tree_node?.icon_string || '';
    
    // Set quote if exists
    if (node.quote && node.quote.quote_loc) {
        const quoteSelect = document.getElementById('wizard-tree-node-quote-select');
        quoteSelect.value = node.quote.quote_loc;
        wizardOnQuoteSelect();
    }
    
    // Set prerequisites
    if (node.prereq_node_indices) {
        node.prereq_node_indices.forEach(prereqIdx => {
            const checkbox = document.getElementById(`wizard-prereq-${prereqIdx}`);
            if (checkbox) checkbox.checked = true;
        });
    }
    
    // Set advisories
    if (node.progression_tree_advisories) {
        node.progression_tree_advisories.forEach(adv => {
            const checkbox = document.getElementById(`wizard-advisory-${adv}`);
            if (checkbox) checkbox.checked = true;
        });
    }
    
    // Load unlocks
    if (node.unlocks && node.unlocks.length > 0) {
        const container = document.getElementById('wizard-tree-node-unlocks-container');
        container.innerHTML = '';
        node.unlocks.forEach((unlock, unlockIdx) => {
            addUnlockRow(unlockIdx, unlock);
        });
    }
}

/**
 * Remove a tree node
 */
export function removeWizardTreeNode(idx) {
    if (!confirm('Remove this tree node?')) return;
    
    wizardData.progression_tree_nodes.splice(idx, 1);
    markDirty();
    
    // Re-render step 4
    const container = document.getElementById('wizard-step-content');
    if (container) {
        import('./step4.js').then(module => {
            module.renderWizardStep4(container);
        });
    }
}

/**
 * Save the tree node
 */
export function wizardSaveTreeNode() {
    const nodeId = document.getElementById('wizard-tree-node-id').value.trim();
    const name = document.getElementById('wizard-tree-node-name').value.trim();
    const description = document.getElementById('wizard-tree-node-desc').value.trim();
    const cost = parseInt(document.getElementById('wizard-tree-node-cost').value, 10) || 150;
    const iconString = document.getElementById('wizard-tree-node-icon').value.trim();
    const editIdx = parseInt(document.getElementById('wizard-tree-node-edit-idx').value, 10);
    
    if (!nodeId) {
        showToast('Node ID is required', 'error');
        return;
    }
    if (!name) {
        showToast('Node name is required', 'error');
        return;
    }
    
    if (!wizardData.progression_tree_nodes) {
        wizardData.progression_tree_nodes = [];
    }
    
    const node = {
        progression_tree_node_type: nodeId,
        progression_tree_node: {
            cost: cost,
        },
        localizations: [
            {
                name: name,
            }
        ],
        progression_tree_advisories: [],
        unlocks: [],
        prereq_node_indices: [],
    };
    
    if (description) {
        node.localizations[0].description = description;
    }
    
    if (iconString) {
        node.progression_tree_node.icon_string = iconString;
    }
    
    // Get selected quote
    const quoteSelect = document.getElementById('wizard-tree-node-quote-select');
    if (quoteSelect && quoteSelect.value && cachedQuotes) {
        const selectedQuote = cachedQuotes.find(q => q.quote_loc === quoteSelect.value);
        if (selectedQuote) {
            node.quote = {
                quote_loc: selectedQuote.quote_loc,
                quote_author_loc: selectedQuote.quote_author_loc,
                quote_audio: selectedQuote.quote_audio,
                quote_text: selectedQuote.quote_text,
                quote_author: selectedQuote.quote_author,
            };
        }
    }
    
    // Get prerequisites
    const prereqCheckboxes = document.querySelectorAll('[id^="wizard-prereq-"]:checked');
    prereqCheckboxes.forEach(checkbox => {
        const prereqIdx = parseInt(checkbox.id.replace('wizard-prereq-', ''), 10);
        if (!isNaN(prereqIdx)) {
            node.prereq_node_indices.push(prereqIdx);
        }
    });
    
    // Get advisory tags
    const advisoryCheckboxes = document.querySelectorAll('[id^="wizard-advisory-"]:checked');
    advisoryCheckboxes.forEach(checkbox => {
        const advisory = checkbox.id.replace('wizard-advisory-', '');
        node.progression_tree_advisories.push(advisory);
    });
    
    // Get unlocks
    const unlockDivs = document.querySelectorAll('[data-unlock-idx]');
    unlockDivs.forEach(unlockDiv => {
        const targetKind = unlockDiv.querySelector('.wizard-unlock-kind').value.trim();
        
        // Get target type - check for both select (modifier presets) and input
        let targetType = '';
        const selectElem = unlockDiv.querySelector('.wizard-unlock-type-select');
        const inputElem = unlockDiv.querySelector('.wizard-unlock-type');
        
        if (selectElem) {
            // Using preset dropdown
            const selectedValue = selectElem.value.trim();
            if (selectedValue && selectedValue !== '_custom_') {
                targetType = selectedValue;
            }
        } else if (inputElem) {
            // Using text input
            targetType = inputElem.value.trim();
        }
        
        const unlockDepth = parseInt(unlockDiv.querySelector('.wizard-unlock-depth').value, 10) || 1;
        const hidden = unlockDiv.querySelector('.wizard-unlock-hidden').checked;
        const aiIgnore = unlockDiv.querySelector('.wizard-unlock-ai-ignore').checked;
        
        if (targetKind && targetType) {
            const unlock = {
                target_kind: targetKind,
                target_type: targetType,
                unlock_depth: unlockDepth,
            };
            if (hidden) unlock.hidden = true;
            if (aiIgnore) unlock.ai_ignore_unlock_value = true;
            node.unlocks.push(unlock);
        }
    });
    
    if (editIdx >= 0) {
        wizardData.progression_tree_nodes[editIdx] = node;
        showToast('Tree node updated', 'success');
    } else {
        wizardData.progression_tree_nodes.push(node);
        showToast('Tree node added', 'success');
    }
    
    markDirty();
    wizardCancelTreeNodeForm();
    
    // Re-render step 4
    const container = document.getElementById('wizard-step-content');
    if (container) {
        import('./step4.js').then(module => {
            module.renderWizardStep4(container);
        });
    }
}

/**
 * Cancel tree node editing
 */
export function wizardCancelTreeNodeForm() {
    const form = document.getElementById('wizard-tree-node-form');
    form.classList.add('hidden');
    
    document.getElementById('wizard-tree-node-id').value = '';
    document.getElementById('wizard-tree-node-name').value = '';
    document.getElementById('wizard-tree-node-desc').value = '';
    document.getElementById('wizard-tree-node-cost').value = '150';
    document.getElementById('wizard-tree-node-icon').value = '';
    document.getElementById('wizard-tree-node-quote-select').value = '';
    document.getElementById('wizard-tree-node-edit-idx').value = '-1';
    
    // Hide quote preview
    const preview = document.getElementById('wizard-tree-node-quote-preview');
    if (preview) preview.classList.add('hidden');
    
    // Clear unlocks
    const unlocksContainer = document.getElementById('wizard-tree-node-unlocks-container');
    if (unlocksContainer) unlocksContainer.innerHTML = '';
}

/**
 * Handle quote selection
 */
export function wizardOnQuoteSelect() {
    const quoteSelect = document.getElementById('wizard-tree-node-quote-select');
    const preview = document.getElementById('wizard-tree-node-quote-preview');
    const quoteText = document.getElementById('wizard-tree-node-quote-text');
    const quoteAuthor = document.getElementById('wizard-tree-node-quote-author');
    
    if (!quoteSelect || !preview || !quoteText || !quoteAuthor) return;
    
    const quoteLoc = quoteSelect.value;
    if (!quoteLoc || !cachedQuotes) {
        preview.classList.add('hidden');
        return;
    }
    
    const selectedQuote = cachedQuotes.find(q => q.quote_loc === quoteLoc);
    if (selectedQuote) {
        quoteText.textContent = `"${selectedQuote.quote_text}"`;
        quoteAuthor.textContent = `— ${selectedQuote.quote_author}`;
        preview.classList.remove('hidden');
    } else {
        preview.classList.add('hidden');
    }
}

/**
 * Add an unlock row
 */
export function wizardAddUnlock() {
    const container = document.getElementById('wizard-tree-node-unlocks-container');
    if (!container) return;
    
    const unlockIdx = container.children.length;
    addUnlockRow(unlockIdx);
}

/**
 * Load and cache age-progression modifiers from modifiers.json
 * Filters for MOD_AQ_*, MOD_EX_*, and MOD_MO_* prefixes and groups by age
 */
async function loadAgeProgressionModifiers() {
    if (cachedAgeProgressionModifiers) {
        return cachedAgeProgressionModifiers;
    }
    
    try {
        const modifiersData = await fetchReferenceData('modifiers');
        const ageModifiers = {
            'AGE_ANTIQUITY': {},
            'AGE_EXPLORATION': {},
            'AGE_MODERN': {}
        };
        
        // Filter modifiers by age-specific prefix
        // modifiersData is {name, description, values: []}
        const allModifiers = modifiersData.values || modifiersData;
        if (Array.isArray(allModifiers)) {
            allModifiers.forEach(mod => {
                if (mod.id) {
                    if (mod.id.startsWith('MOD_AQ_')) {
                        ageModifiers['AGE_ANTIQUITY'][mod.id] = mod.description || mod.id;
                    } else if (mod.id.startsWith('MOD_EX_')) {
                        ageModifiers['AGE_EXPLORATION'][mod.id] = mod.description || mod.id;
                    } else if (mod.id.startsWith('MOD_MO_')) {
                        ageModifiers['AGE_MODERN'][mod.id] = mod.description || mod.id;
                    }
                }
            });
        }
        
        cachedAgeProgressionModifiers = ageModifiers;
        return ageModifiers;
    } catch (error) {
        console.error('Error loading age progression modifiers:', error);
        return {
            'AGE_ANTIQUITY': {},
            'AGE_EXPLORATION': {},
            'AGE_MODERN': {}
        };
    }
}

/**
 * Add an unlock row with optional data
 */
async function addUnlockRow(unlockIdx, unlock = null) {
    const container = document.getElementById('wizard-tree-node-unlocks-container');
    if (!container) return;
    
    const unlockDiv = document.createElement('div');
    unlockDiv.className = 'flex gap-2 items-end';
    unlockDiv.dataset.unlockIdx = unlockIdx;
    
    // Determine the age from the node type field
    let nodeAge = 'AGE_ANTIQUITY';
    const nodeTypeField = document.getElementById('wizard-tree-node-id');
    const nodeType = nodeTypeField?.value || '';
    if (nodeType.includes('_EX_') || nodeType.includes('_EXPLORATION')) {
        nodeAge = 'AGE_EXPLORATION';
    } else if (nodeType.includes('_MO_') || nodeType.includes('_MODERN')) {
        nodeAge = 'AGE_MODERN';
    }
    console.log(`addUnlockRow: nodeType="${nodeType}", detected nodeAge="${nodeAge}"`);
    
    // Load modifiers for this age
    const ageModifiers = await loadAgeProgressionModifiers();
    const ageMods = ageModifiers[nodeAge] || {};
    console.log(`addUnlockRow: ${nodeAge} has ${Object.keys(ageMods).length} modifiers`);
    
    const modOptions = Object.entries(ageMods)
        .map(([modId, desc]) => `<option value="${modId}" ${unlock?.target_type === modId ? 'selected' : ''}>${modId}: ${desc.substring(0, 50)}</option>`)
        .join('');
    
    // Normalize target_kind: if old KIND_MODIFIER, determine if it's common or custom
    let targetKind = unlock?.target_kind;
    if (targetKind === 'KIND_MODIFIER') {
        // Legacy support: check if target_type is in common modifiers
        targetKind = (ageMods[unlock?.target_type]) ? 'KIND_MODIFIER_COMMON' : 'KIND_MODIFIER_CUSTOM';
    }
    
    unlockDiv.innerHTML = `
        <div class="flex-1">
            <label class="block text-xs font-medium text-slate-300 mb-1">Kind</label>
            <select class="wizard-unlock-kind w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100" onchange="window.wizardToggleModifierPreset(${unlockIdx}).catch(e => console.error('Error toggling modifier:', e))">
                <option value="KIND_MODIFIER_COMMON" ${targetKind === 'KIND_MODIFIER_COMMON' ? 'selected' : ''}>Modifier (Common)</option>
                <option value="KIND_MODIFIER_CUSTOM" ${targetKind === 'KIND_MODIFIER_CUSTOM' ? 'selected' : ''}>Modifier (Custom)</option>
                <option value="KIND_CONSTRUCTIBLE" ${targetKind === 'KIND_CONSTRUCTIBLE' ? 'selected' : ''}>Building/Improvement</option>
                <option value="KIND_UNIT" ${targetKind === 'KIND_UNIT' ? 'selected' : ''}>Unit</option>
                <option value="KIND_TRADITION" ${targetKind === 'KIND_TRADITION' ? 'selected' : ''}>Tradition</option>
            </select>
        </div>
        <div class="flex-1" id="wizard-unlock-type-${unlockIdx}">
            ${targetKind === 'KIND_MODIFIER_COMMON' ? `
                <label class="block text-xs font-medium text-slate-300 mb-1">Modifier</label>
                <select class="wizard-unlock-type-select w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100">
                    <option value="">-- Select ${nodeAge} Modifier --</option>
                    ${modOptions}
                </select>
            ` : targetKind === 'KIND_MODIFIER_CUSTOM' ? `
                <label class="block text-xs font-medium text-slate-300 mb-1">Custom Modifier ID</label>
                <input 
                    type="text" 
                    placeholder="MOD_YOUR_CUSTOM_MODIFIER"
                    value="${unlock?.target_type || ''}"
                    class="wizard-unlock-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100"
                />
            ` : `
                <label class="block text-xs font-medium text-slate-300 mb-1">Type/ID</label>
                <input 
                    type="text" 
                    placeholder="${targetKind === 'KIND_UNIT' ? 'UNIT_TYPE' : targetKind === 'KIND_CONSTRUCTIBLE' ? 'BUILDING_TYPE' : 'TYPE_ID'}"
                    value="${unlock?.target_type || ''}"
                    class="wizard-unlock-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100"
                />
            `}
        </div>
        <div class="w-20">
            <label class="block text-xs font-medium text-slate-300 mb-1">Depth</label>
            <input 
                type="number" 
                value="${unlock?.unlock_depth || 1}"
                min="1"
                class="wizard-unlock-depth w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100"
            />
        </div>
        <label class="flex items-center gap-1 text-xs text-slate-300 pb-1">
            <input type="checkbox" class="wizard-unlock-hidden rounded" ${unlock?.hidden ? 'checked' : ''} />
            Hidden
        </label>
        <label class="flex items-center gap-1 text-xs text-slate-300 pb-1">
            <input type="checkbox" class="wizard-unlock-ai-ignore rounded" ${unlock?.ai_ignore_unlock_value ? 'checked' : ''} />
            AI Ignore
        </label>
        <button 
            onclick="window.wizardRemoveUnlock(${unlockIdx})"
            type="button"
            class="px-2 py-1 bg-red-600/30 hover:bg-red-600/50 border border-red-600 rounded text-red-300 text-xs"
        >
            ×
        </button>
    `;
    
    container.appendChild(unlockDiv);
    
    // If custom modifier selected initially, show input
    if (unlock?.target_kind === 'KIND_MODIFIER' && unlock?.target_type && !ageMods[unlock.target_type]) {
        wizardToggleModifierInput(unlockIdx, unlock.target_type);
    }
}

/**
 * Remove an unlock and re-index
 */
export function wizardRemoveUnlock(unlockIdx) {
    const container = document.getElementById('wizard-tree-node-unlocks-container');
    if (!container) return;
    
    const unlockDiv = container.querySelector(`[data-unlock-idx="${unlockIdx}"]`);
    if (unlockDiv) {
        unlockDiv.remove();
        
        // Re-index remaining unlocks
        const remainingUnlocks = container.querySelectorAll('[data-unlock-idx]');
        remainingUnlocks.forEach((div, newUnlockIdx) => {
            div.dataset.unlockIdx = newUnlockIdx;
            
            // Update the remove button onclick
            const removeBtn = div.querySelector('button[onclick*="wizardRemoveUnlock"]');
            if (removeBtn) {
                removeBtn.setAttribute('onclick', `window.wizardRemoveUnlock(${newUnlockIdx})`);
            }
        });
    }
}

/**
 * Move a node up in the list
 */
export function wizardMoveNodeUp(idx) {
    if (idx === 0) return;
    
    const nodes = wizardData.progression_tree_nodes;
    [nodes[idx - 1], nodes[idx]] = [nodes[idx], nodes[idx - 1]];
    
    // Update prerequisite indices
    nodes.forEach(node => {
        if (node.prereq_node_indices) {
            node.prereq_node_indices = node.prereq_node_indices.map(prereqIdx => {
                if (prereqIdx === idx) return idx - 1;
                if (prereqIdx === idx - 1) return idx;
                return prereqIdx;
            });
        }
    });
    
    markDirty();
    
    // Re-render
    const container = document.getElementById('wizard-step-content');
    if (container) {
        import('./step4.js').then(module => {
            module.renderWizardStep4(container);
        });
    }
}

/**
 * Move a node down in the list
 */
export function wizardMoveNodeDown(idx) {
    const nodes = wizardData.progression_tree_nodes;
    if (idx === nodes.length - 1) return;
    
    [nodes[idx], nodes[idx + 1]] = [nodes[idx + 1], nodes[idx]];
    
    // Update prerequisite indices
    nodes.forEach(node => {
        if (node.prereq_node_indices) {
            node.prereq_node_indices = node.prereq_node_indices.map(prereqIdx => {
                if (prereqIdx === idx) return idx + 1;
                if (prereqIdx === idx + 1) return idx;
                return prereqIdx;
            });
        }
    });
    
    markDirty();
    
    // Re-render
    const container = document.getElementById('wizard-step-content');
    if (container) {
        import('./step4.js').then(module => {
            module.renderWizardStep4(container);
        });
    }
}

/**
 * Load quotes reference data
 */
async function loadQuotesData() {
    if (cachedQuotes) {
        populateQuotesDropdown();
        return;
    }
    
    try {
        const data = await fetchReferenceData('quotes');
        cachedQuotes = data.values || [];
        populateQuotesDropdown();
    } catch (error) {
        console.error('Failed to load quotes:', error);
        showToast('Failed to load quotes', 'error');
    }
}

/**
 * Populate quotes dropdown
 */
function populateQuotesDropdown() {
    const select = document.getElementById('wizard-tree-node-quote-select');
    if (!select || !cachedQuotes) return;
    
    select.innerHTML = '<option value="">-- Select a quote --</option>';
    
    // Group by age
    const byAge = {};
    cachedQuotes.forEach(quote => {
        const age = quote.age || 'Unknown';
        if (!byAge[age]) byAge[age] = [];
        byAge[age].push(quote);
    });
    
    Object.keys(byAge).sort().forEach(age => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = age.replace('AGE_', '');
        
        byAge[age].forEach(quote => {
            const option = document.createElement('option');
            option.value = quote.quote_loc;
            // Show first 80 chars of quote text
            const preview = quote.quote_text.substring(0, 80);
            option.textContent = `${preview}... — ${quote.quote_author}`;
            optgroup.appendChild(option);
        });
        
        select.appendChild(optgroup);
    });
}

/**
 * Load advisory types reference data
 */
async function loadAdvisoryTypesData() {
    if (cachedAdvisoryTypes) {
        populateAdvisoryCheckboxes();
        return;
    }
    
    try {
        const data = await fetchReferenceData('advisory-class-types');
        cachedAdvisoryTypes = data.values || [];
        populateAdvisoryCheckboxes();
    } catch (error) {
        console.error('Failed to load advisory types:', error);
    }
}

/**
 * Populate advisory checkboxes
 */
function populateAdvisoryCheckboxes() {
    const container = document.getElementById('wizard-tree-node-advisories-container');
    if (!container || !cachedAdvisoryTypes) return;
    
    container.innerHTML = '';
    
    cachedAdvisoryTypes.forEach(advisory => {
        const div = document.createElement('div');
        div.className = 'flex items-center gap-2 mb-1';
        div.innerHTML = `
            <input 
                type="checkbox" 
                id="wizard-advisory-${advisory.id}" 
                class="rounded bg-slate-700 border-slate-600"
            />
            <label for="wizard-advisory-${advisory.id}" class="text-xs text-slate-300">
                ${advisory.id.replace('ADVISORY_', '')}
            </label>
        `;
        container.appendChild(div);
    });
}

/**
 * Toggle between common modifier preset and custom input
 */
export function wizardToggleModifierInput(unlockIdx, customValue = '') {
    const typeContainer = document.getElementById(`wizard-unlock-type-${unlockIdx}`);
    if (!typeContainer) return;
    
    const currentSelect = typeContainer.querySelector('.wizard-unlock-type-select');
    
    if (currentSelect) {
        // Switch to custom input
        typeContainer.innerHTML = `
            <label class="block text-xs font-medium text-slate-300 mb-1">
                Custom Modifier ID 
                <button type="button" onclick="window.wizardToggleModifierInput(${unlockIdx})" class="text-blue-400 hover:text-blue-300 ml-1" title="Switch to common modifiers">⇄</button>
            </label>
            <input 
                type="text" 
                placeholder="MOD_YOUR_CUSTOM_MODIFIER"
                value="${customValue}"
                class="wizard-unlock-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100"
            />
        `;
    } else {
        // Switch to preset dropdown
        const currentInput = typeContainer.querySelector('.wizard-unlock-type');
        const currentValue = currentInput?.value || '';
        const isCommon = COMMON_MODIFIERS[currentValue];
        
        const commonModOptions = Object.entries(COMMON_MODIFIERS)
            .map(([modId, label]) => `<option value="${modId}" ${currentValue === modId ? 'selected' : ''}>${label}</option>`)
            .join('');
        
        typeContainer.innerHTML = `
            <label class="block text-xs font-medium text-slate-300 mb-1">
                Modifier 
                <button type="button" onclick="window.wizardToggleModifierInput(${unlockIdx}, '${currentValue}')" class="text-blue-400 hover:text-blue-300 ml-1" title="Switch to custom input">⇄</button>
            </label>
            <select class="wizard-unlock-type-select w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100">
                <option value="">-- Select Common Modifier --</option>
                ${commonModOptions}
                <option value="_custom_" ${!isCommon && currentValue ? 'selected' : ''}>Custom Modifier ID...</option>
            </select>
        `;
    }
}

/**
 * Toggle unlock type input when kind changes
 */
export async function wizardToggleModifierPreset(unlockIdx) {
    const unlockDiv = document.querySelector(`[data-unlock-idx="${unlockIdx}"]`);
    if (!unlockDiv) return;
    
    const kindSelect = unlockDiv.querySelector('.wizard-unlock-kind');
    const kind = kindSelect.value;
    const typeContainer = document.getElementById(`wizard-unlock-type-${unlockIdx}`);
    
    if (!typeContainer) return;
    
    // Determine the age from the node type field
    let nodeAge = 'AGE_ANTIQUITY';
    const nodeTypeField = document.getElementById('wizard-tree-node-id');
    const nodeType = nodeTypeField?.value || '';
    if (nodeType.includes('_EX_') || nodeType.includes('_EXPLORATION')) {
        nodeAge = 'AGE_EXPLORATION';
    } else if (nodeType.includes('_MO_') || nodeType.includes('_MODERN')) {
        nodeAge = 'AGE_MODERN';
    }
    
    if (kind === 'KIND_MODIFIER_COMMON') {
        // Load modifiers for this age
        const ageModifiers = await loadAgeProgressionModifiers();
        const ageMods = ageModifiers[nodeAge] || {};
        const modOptions = Object.entries(ageMods)
            .map(([modId, desc]) => `<option value="${modId}">${modId}: ${desc.substring(0, 50)}</option>`)
            .join('');
        
        typeContainer.innerHTML = `
            <label class="block text-xs font-medium text-slate-300 mb-1">Modifier</label>
            <select class="wizard-unlock-type-select w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100">
                <option value="">-- Select ${nodeAge} Modifier --</option>
                ${modOptions}
            </select>
        `;
    } else if (kind === 'KIND_MODIFIER_CUSTOM') {
        typeContainer.innerHTML = `
            <label class="block text-xs font-medium text-slate-300 mb-1">Custom Modifier ID</label>
            <input 
                type="text" 
                placeholder="MOD_YOUR_CUSTOM_MODIFIER"
                value=""
                class="wizard-unlock-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100"
            />
        `;
    } else {
        // Show regular text input for other kinds
        const placeholder = kind === 'KIND_UNIT' ? 'UNIT_TYPE' : 
                          kind === 'KIND_CONSTRUCTIBLE' ? 'BUILDING_TYPE' : 
                          kind === 'KIND_TRADITION' ? 'TRADITION_TYPE' : 'TYPE_ID';
        
        typeContainer.innerHTML = `
            <label class="block text-xs font-medium text-slate-300 mb-1">Type/ID</label>
            <input 
                type="text" 
                placeholder="${placeholder}"
                value=""
                class="wizard-unlock-type w-full px-2 py-1 bg-slate-700 border border-slate-600 rounded text-xs text-slate-100"
            />
        `;
    }
}

/**
 * Populate prerequisite checkboxes based on existing nodes
 */
function populatePrereqsCheckboxes() {
    const container = document.getElementById('wizard-tree-node-prereqs-container');
    if (!container) return;
    
    const editIdx = parseInt(document.getElementById('wizard-tree-node-edit-idx').value, 10);
    const nodes = wizardData.progression_tree_nodes || [];
    
    container.innerHTML = '';
    
    if (nodes.length === 0 || (editIdx === 0 && nodes.length === 1)) {
        container.innerHTML = '<p class="text-xs text-slate-400">No existing nodes available as prerequisites</p>';
        return;
    }
    
    nodes.forEach((node, idx) => {
        // Don't allow a node to depend on itself
        if (idx === editIdx) return;
        
        const div = document.createElement('div');
        div.className = 'flex items-center gap-2 mb-1';
        div.innerHTML = `
            <input 
                type="checkbox" 
                id="wizard-prereq-${idx}" 
                class="rounded bg-slate-700 border-slate-600"
            />
            <label for="wizard-prereq-${idx}" class="text-xs text-slate-300">
                Node ${idx + 1}: ${node.localizations?.[0]?.name || 'Unnamed'}
            </label>
        `;
        container.appendChild(div);
    });
}
