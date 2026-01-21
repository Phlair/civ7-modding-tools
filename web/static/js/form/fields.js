/**
 * Form Module - Field Creators
 * Handles creation of all form field types with advanced autocomplete
 */

import { 
    AUTOCOMPLETE_MAPPINGS, 
    FIELD_HELP_TEXT, 
    currentMode, 
    getCurrentData, 
    getWizardData,
    getCachedReferenceData,
    setCachedReferenceData 
} from '../state.js';
import './arrays.js';

// Track most-used autocomplete values
let autocompleteUsageStats = JSON.parse(localStorage.getItem('autocompleteUsage') || '{}');

/**
 * Record autocomplete usage for sorting
 * @param {string} fieldName - Field name
 * @param {string} value - Value used
 */
export function recordAutocompleteUsage(fieldName, value) {
    if (!autocompleteUsageStats[fieldName]) {
        autocompleteUsageStats[fieldName] = {};
    }
    if (!autocompleteUsageStats[fieldName][value]) {
        autocompleteUsageStats[fieldName][value] = 0;
    }
    autocompleteUsageStats[fieldName][value]++;
    localStorage.setItem('autocompleteUsage', JSON.stringify(autocompleteUsageStats));
}

/**
 * Get most commonly used values for a field
 * @param {string} fieldName - Field name
 * @param {Array} allOptions - All available options
 * @param {number} limit - Maximum results
 * @returns {Array} Sorted options by usage
 */
export function getMostCommonValues(fieldName, allOptions, limit = 10) {
    const usage = autocompleteUsageStats[fieldName] || {};
    const sorted = allOptions.sort((a, b) => {
        const aCount = usage[a] || 0;
        const bCount = usage[b] || 0;
        return bCount - aCount;
    });
    return sorted.slice(0, limit);
}

/**
 * Get autocomplete options for a field
 * @param {string} fieldName - Field name
 * @param {boolean} includeBindings - Include builder bindings
 * @returns {Promise<Array>} Options array
 */
export async function getAutocompleteOptions(fieldName, includeBindings = false) {
    // Extract the last part of the field name (e.g., "collection" from "modifiers.0.modifier.collection")
    const fieldType = fieldName.split('.').pop();
    
    // Special handling for bindings - pull from current file's builder IDs
    if (includeBindings && fieldType === 'binding') {
        return getAvailableBindings();
    }
    
    const dataType = AUTOCOMPLETE_MAPPINGS[fieldType];
    if (!dataType) {
        return [];
    }
    
    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (response.ok) {
            const data = await response.json();
            // JSON files have structure: { values: [{ id: "...", ... }, ...] }
            let options = data.values ? data.values.map(v => v.id) : [];
            
            // Apply categorization for tags - group by category if available
            if (dataType === 'tags' && data.values && data.values[0]?.category) {
                options = options; // Keep flat for now, categorization in dropdown rendering
            }
            
            return options;
        }
    } catch (error) {
        console.error(`Failed to fetch autocomplete data for ${fieldType}:`, error);
    }
    return [];
}

/**
 * Get available bindings from current data
 * @returns {Array} Builder IDs
 */
export function getAvailableBindings() {
    // Collect all builder IDs from current data or wizard data
    const data = currentMode === 'guided' ? getWizardData() : getCurrentData();
    const bindings = [];
    
    // From units
    if (data.units) {
        data.units.forEach(u => u.id && bindings.push(u.id));
    }
    
    // From constructibles
    if (data.constructibles) {
        data.constructibles.forEach(c => c.id && bindings.push(c.id));
    }
    
    // From modifiers
    if (data.modifiers) {
        data.modifiers.forEach(m => m.id && bindings.push(m.id));
    }
    
    // From traditions
    if (data.traditions) {
        data.traditions.forEach(t => t.id && bindings.push(t.id));
    }
    
    // From progression trees
    if (data.progression_trees) {
        data.progression_trees.forEach(pt => pt.id && bindings.push(pt.id));
    }
    
    // From progression tree nodes
    if (data.progression_tree_nodes) {
        data.progression_tree_nodes.forEach(ptn => ptn.id && bindings.push(ptn.id));
    }
    
    return bindings;
}

/**
 * Create autocomplete field with fuzzy search and dropdown
 * @param {string} fieldName - Field name
 * @param {string} label - Field label
 * @param {string} value - Current value
 * @param {boolean} isRequired - Whether field is required
 * @param {string} helpText - Help text
 * @returns {HTMLElement} Field DOM element
 */
export function createAutocompleteField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            import('../ui.js').then(m => m.showFieldHelpModal(label, helpText));
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const inputWrapper = document.createElement("div");
    inputWrapper.className = "relative";
    
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    input.autocomplete = "off";
    
    const dropdown = document.createElement("div");
    dropdown.className = "absolute top-full left-0 right-0 mt-1 bg-slate-800 border border-slate-600 rounded shadow-lg max-h-64 overflow-y-auto z-1000";
    dropdown.style.display = "none";
    
    let allOptions = [];
    let filteredOptions = [];
    let categoryData = null;
    
    // Load options asynchronously
    (async () => {
        const isBindingField = fieldName.includes('binding');
        allOptions = await getAutocompleteOptions(fieldName, isBindingField);
        
        // Load category data for tags
        if (fieldName.includes('tag')) {
            try {
                const response = await fetch('/api/data/tags');
                if (response.ok) {
                    const data = await response.json();
                    categoryData = data.values;
                }
            } catch (e) {
                console.error('Failed to load tag categories:', e);
            }
        }
        
        updateDropdown();
    })();
    
    function getCategoryLabel(tagId) {
        if (!categoryData) return null;
        const tag = categoryData.find(t => t.id === tagId);
        return tag?.category || 'UNCATEGORIZED';
    }
    
    function updateDropdown() {
        const query = input.value.toLowerCase();
        
        // Filter options based on query
        if (query.length === 0) {
            // Show most-common values first when empty
            const mostCommon = getMostCommonValues(fieldName, allOptions, 15);
            filteredOptions = mostCommon.length > 0 ? mostCommon : allOptions.slice(0, 50);
        } else {
            filteredOptions = allOptions.filter(opt => {
                const optStr = String(opt).toLowerCase();
                return optStr.includes(query);
            });
        }
        
        filteredOptions = filteredOptions.slice(0, 50); // Cap at 50 options
        
        dropdown.innerHTML = "";
        
        if (filteredOptions.length === 0) {
            const noResults = document.createElement("div");
            noResults.className = "px-3 py-2 text-slate-400 text-sm";
            noResults.textContent = query.length > 0 ? "No results" : "No options available";
            dropdown.appendChild(noResults);
            dropdown.style.display = "block";
        } else {
            // Group by category for tags
            if (fieldName.includes('tag') && categoryData) {
                const grouped = {};
                filteredOptions.forEach(opt => {
                    const cat = getCategoryLabel(opt) || 'UNCATEGORIZED';
                    if (!grouped[cat]) grouped[cat] = [];
                    grouped[cat].push(opt);
                });
                
                // Render categorized options
                Object.entries(grouped).forEach(([category, values]) => {
                    const catHeader = document.createElement("div");
                    catHeader.className = "px-3 py-1 text-xs font-semibold text-slate-400 bg-slate-900 sticky top-0";
                    catHeader.textContent = category;
                    dropdown.appendChild(catHeader);
                    
                    values.forEach(opt => {
                        const optDiv = document.createElement("div");
                        optDiv.className = "px-4 py-2 cursor-pointer hover:bg-slate-700 text-slate-100 text-sm border-l-2 border-slate-700";
                        optDiv.textContent = opt;
                        optDiv.onclick = () => {
                            input.value = opt;
                            recordAutocompleteUsage(fieldName, opt);
                            import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, opt));
                            dropdown.style.display = "none";
                            
                            // Validate and show feedback
                            import('../form/validation.js').then(m => m.validateFieldDependency && m.validateFieldDependency(fieldName, opt));
                        };
                        dropdown.appendChild(optDiv);
                    });
                });
            } else {
                // Regular flat list for non-tag fields
                filteredOptions.forEach((opt, idx) => {
                    const optDiv = document.createElement("div");
                    optDiv.className = "px-3 py-2 cursor-pointer hover:bg-slate-700 text-slate-100 text-sm" + 
                        (idx < 5 ? " bg-slate-700/30" : ""); // Highlight most-common at top
                    optDiv.textContent = opt;
                    optDiv.onclick = () => {
                        input.value = opt;
                        recordAutocompleteUsage(fieldName, opt);
                        import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, opt));
                        dropdown.style.display = "none";
                        
                        // Validate and show feedback
                        import('../form/validation.js').then(m => m.validateFieldDependency && m.validateFieldDependency(fieldName, opt));
                    };
                    dropdown.appendChild(optDiv);
                });
            }
            dropdown.style.display = "block";
        }
    }
    
    input.addEventListener("input", updateDropdown);
    input.addEventListener("focus", () => {
        // Show all options when focused
        if (allOptions.length > 0) {
            updateDropdown();
        }
    });
    input.addEventListener("blur", () => {
        // Validate on blur
        setTimeout(() => {
            import('../form/validation.js').then(m => m.validateFieldBlur && m.validateFieldBlur(fieldName, input.value));
        }, 200);
    });
    input.addEventListener("change", (e) => {
        recordAutocompleteUsage(fieldName, e.target.value);
        import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, e.target.value));
    });
    
    document.addEventListener("click", (e) => {
        if (!inputWrapper.contains(e.target)) {
            dropdown.style.display = "none";
        }
    });
    
    inputWrapper.appendChild(input);
    inputWrapper.appendChild(dropdown);
    div.appendChild(inputWrapper);
    
    // Store reference for validation
    if (!div.dataset.fieldName) {
        div.dataset.fieldName = fieldName;
        div.dataset.fieldType = 'autocomplete';
    }
    
    return div;
}

/**
 * Convert ID to human-friendly label
 * @param {string} id - ID string
 * @returns {string} Friendly label
 */
function idToLabel(id) {
    if (!id) return '';
    
    // Remove common prefixes
    let label = id
        .replace(/^(CIVILIZATION|UNIT|BUILDING|QUARTER|IMPROVEMENT|MODIFIER|TRADITION|TRAIT|AGE|BIOME|TERRAIN|FEATURE|DISTRICT|GOVERNMENT|YIELD|EFFECT|REQUIREMENT|COLLECTION)_/, '');
    
    // Convert underscores to spaces
    label = label.replace(/_/g, ' ');
    
    // Title case each word
    label = label.split(' ').map(word => {
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
    }).join(' ');
    
    return label;
}

/**
 * Create dropdown select field with reference data
 * @param {string} fieldName - Field name
 * @param {string} label - Field label
 * @param {string} value - Current value
 * @param {string} dataType - Reference data type
 * @param {string} helpText - Help text
 * @returns {HTMLElement} Field DOM element
 */
export function createDataSelectField(fieldName, label, value = "", dataType = null, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300";
    labelElem.textContent = label;
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            import('../ui.js').then(m => m.showFieldHelpModal(label, helpText));
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const select = document.createElement("select");
    select.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors mt-1";
    select.dataset.fieldName = fieldName;
    select.dataset.dataType = dataType;
    
    // Generate unique ID for select element
    const selectId = `expert-select-${fieldName.replace(/\./g, '-').replace(/\[/g, '-').replace(/\]/g, '')}`;
    select.id = selectId;
    
    // Add placeholder
    const placeholderOption = document.createElement("option");
    placeholderOption.value = "";
    placeholderOption.textContent = "Select...";
    select.appendChild(placeholderOption);
    
    // Populate using wizard dropdown function
    if (dataType) {
        (async () => {
            try {
                const response = await fetch(`/api/data/${dataType}`);
                if (!response.ok) {
                    console.error(`Failed to fetch ${dataType}`);
                    return;
                }
                
                const data = await response.json();
                const values = data.values || [];
                
                // Clear existing options
                select.innerHTML = '';
                
                // Re-add placeholder
                const placeholder = document.createElement('option');
                placeholder.value = '';
                placeholder.textContent = 'Select...';
                select.appendChild(placeholder);
                
                // Add data options with friendly labels (wizard style)
                values.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    const friendlyLabel = idToLabel(item.id);
                    option.textContent = `${friendlyLabel} (${item.id})`;
                    if (item.id === value) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
                
            } catch (error) {
                console.error(`Error loading ${dataType}:`, error);
            }
        })();
    }
    
    select.addEventListener("change", (e) => {
        import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, e.target.value));
        import('../state.js').then(m => m.markDirty && m.markDirty());
    });
    
    div.appendChild(select);
    
    return div;
}

/**
 * Create text input field
 * @param {string} fieldName - Field name
 * @param {string} label - Field label
 * @param {string} value - Current value
 * @param {boolean} isRequired - Whether field is required
 * @param {string} helpText - Help text
 * @returns {HTMLElement} Field DOM element
 */
export function createTextField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            import('../ui.js').then(m => m.showFieldHelpModal(label, helpText));
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const input = document.createElement("input");
    input.type = "text";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors mt-1";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    
    input.addEventListener("change", (e) => {
        import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, e.target.value));
        import('../state.js').then(m => m.markDirty && m.markDirty());
    });
    
    input.addEventListener("blur", () => {
        import('../form/validation.js').then(m => m.validateFieldBlur && m.validateFieldBlur(fieldName, input.value));
    });
    
    div.appendChild(input);
    
    return div;
}

/**
 * Create number input field
 * @param {string} fieldName - Field name
 * @param {string} label - Field label
 * @param {number} value - Current value
 * @param {boolean} isRequired - Whether field is required
 * @param {string} helpText - Help text
 * @returns {HTMLElement} Field DOM element
 */
export function createNumberField(fieldName, label, value = "", isRequired = false, helpText = "") {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelDiv = document.createElement("div");
    labelDiv.className = "flex items-center justify-between";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300";
    labelElem.textContent = label + (isRequired ? " *" : "");
    
    // Add help icon if help text available
    if (helpText) {
        const helpBtn = document.createElement("button");
        helpBtn.className = "text-blue-400 hover:text-blue-300 text-sm font-bold ml-1";
        helpBtn.textContent = "ⓘ";
        helpBtn.type = "button";
        helpBtn.onclick = (e) => {
            e.preventDefault();
            import('../ui.js').then(m => m.showFieldHelpModal(label, helpText));
        };
        labelElem.appendChild(helpBtn);
    }
    
    labelDiv.appendChild(labelElem);
    div.appendChild(labelDiv);
    
    const input = document.createElement("input");
    input.type = "number";
    input.value = value || "";
    input.className = "w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm focus:outline-none focus:border-blue-400 transition-colors mt-1";
    input.dataset.fieldName = fieldName;
    input.dataset.isRequired = isRequired;
    
    input.addEventListener("change", (e) => {
        const numValue = parseFloat(e.target.value) || 0;
        import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, numValue));
        import('../state.js').then(m => m.markDirty && m.markDirty());
    });
    
    input.addEventListener("blur", () => {
        import('../form/validation.js').then(m => m.validateFieldBlur && m.validateFieldBlur(fieldName, input.value));
    });
    
    div.appendChild(input);
    
    return div;
}

/**
 * Create boolean checkbox field
 * @param {string} fieldName - Field name
 * @param {string} label - Field label
 * @param {boolean} value - Current value
 * @returns {HTMLElement} Field DOM element
 */
export function createBooleanField(fieldName, label, value = false) {
    const div = document.createElement("div");
    div.className = "mb-4 flex items-center";
    
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = value || false;
    input.className = "mr-2 rounded bg-slate-800 border-slate-600 text-blue-600 focus:ring-blue-500";
    input.dataset.fieldName = fieldName;
    
    input.addEventListener("change", (e) => {
        import('../expert/sections.js').then(m => m.updateFieldValue && m.updateFieldValue(fieldName, e.target.checked));
        import('../state.js').then(m => m.markDirty && m.markDirty());
    });
    
    const labelElem = document.createElement("label");
    labelElem.className = "text-sm font-medium text-slate-300";
    labelElem.textContent = label;
    
    div.appendChild(input);
    div.appendChild(labelElem);
    
    return div;
}

/**
 * Create string array field
 * @param {string} fieldName - Field name
 * @param {string} label - Field label
 * @param {Array} items - Current items
 * @param {string} sectionId - Section ID for re-rendering
 * @returns {HTMLElement} Field DOM element
 */
export function createStringArrayField(fieldName, label, items = [], sectionId = null) {
    const div = document.createElement("div");
    div.className = "mb-4";
    
    const labelElem = document.createElement("label");
    labelElem.className = "block text-sm font-medium text-slate-300 mb-2";
    labelElem.textContent = label;
    div.appendChild(labelElem);
    
    const itemsContainer = document.createElement("div");
    itemsContainer.className = "space-y-2";
    itemsContainer.id = `array-container-${fieldName}`;
    
    items.forEach((item, idx) => {
        const itemDiv = document.createElement("div");
        itemDiv.className = "flex gap-2";
        
        const itemInput = document.createElement("input");
        itemInput.type = "text";
        itemInput.value = item || "";
        itemInput.className = "flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded text-slate-100 text-sm";
        itemInput.dataset.arrayIdx = idx;
        
        itemInput.onchange = (e) => {
            // Use global event handler pattern if exposed, otherwise dynamic import fallback
            if (window.arrayUpdateItem) {
                // If using global scope pattern
                window.arrayUpdateItem(fieldName, idx, e.target.value);
            } else {
                // Legacy fallback
                import('../form/arrays.js').then(m => {
                    const values = m.getArrayFieldValues(fieldName);
                    values[idx] = e.target.value;
                    import('../expert/sections.js').then(n => n.updateFieldValue && n.updateFieldValue(fieldName, values));
                    import('../state.js').then(n => n.markDirty && n.markDirty());
                });
            }
        };
        
        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded text-red-400 text-sm";
        removeBtn.textContent = "×";
        removeBtn.setAttribute("onclick", `window.arrayRemoveItem('${fieldName}', ${idx})`);
        
        itemDiv.appendChild(itemInput);
        itemDiv.appendChild(removeBtn);
        itemsContainer.appendChild(itemDiv);
    });
    
    div.appendChild(itemsContainer);
    
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.className = "mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium";
    addBtn.textContent = "+ Add Item";
    addBtn.setAttribute("onclick", `window.arrayAddItem('${fieldName}')`);
    
    div.appendChild(addBtn);
    
    return div;
}

// Export alias for HTML compatibility
export const recordFieldUsage = recordAutocompleteUsage;
