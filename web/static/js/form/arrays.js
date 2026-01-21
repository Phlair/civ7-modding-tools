/**
 * Form Module - Array Helpers
 * Handles array field operations and rendering
 */

import { currentData, markDirty } from '../state.js';

/**
 * Add item to string array
 * @param {string} fieldName - Field name
 */
export function addArrayItem(fieldName) {
    const container = document.getElementById(`array-container-${fieldName}`);
    if (!container) return;

    const newIdx = container.children.length;
    const itemHtml = `
        <div class="flex gap-2 items-center mb-2">
            <input 
                type="text"
                value=""
                data-array-item="${newIdx}"
                class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                placeholder="New item"
            />
            <button 
                onclick="window.arrayRemoveItem('${fieldName}', ${newIdx})"
                class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
            >
                ×
            </button>
        </div>
    `;

    const itemDiv = document.createElement('div');
    itemDiv.innerHTML = itemHtml;
    container.appendChild(itemDiv.firstElementChild);
    markDirty();
}

/**
 * Remove item from array
 * @param {string} fieldName - Field name
 * @param {number} idx - Item index
 */
export function removeArrayItem(fieldName, idx) {
    const container = document.getElementById(`array-container-${fieldName}`);
    if (!container) return;

    const items = Array.from(container.querySelectorAll('[data-array-item]'));
    if (items[idx]) {
        items[idx].parentElement.remove();
    }
    markDirty();
}

/**
 * Get array field values
 * @param {string} fieldName - Field name
 * @returns {Array} Array of values
 */
export function getArrayFieldValues(fieldName) {
    const container = document.getElementById(`array-container-${fieldName}`);
    if (!container) return [];

    return Array.from(container.querySelectorAll('[data-array-item]'))
        .map(input => input.value)
        .filter(val => val.trim() !== '');
}

/**
 * Re-render array with updated data
 * @param {string} fieldName - Field name
 * @param {Array} items - Array items
 */
export function rerenderArrayField(fieldName, items = []) {
    const container = document.getElementById(`array-container-${fieldName}`);
    if (!container) return;

    container.innerHTML = items.map((item, idx) => `
        <div class="flex gap-2 items-center mb-2">
            <input 
                type="text"
                value="${item}"
                data-array-item="${idx}"
                class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm"
                onchange="window.arrayUpdateItem('${fieldName}', ${idx}, this.value)"
            />
            <button 
                onclick="window.arrayRemoveItem('${fieldName}', ${idx})"
                class="px-3 py-2 bg-red-600/20 hover:bg-red-600/30 border border-red-600 rounded-lg text-red-400 text-sm"
            >
                ×
            </button>
        </div>
    `).join('');
}

/**
 * Update array item at index
 * @param {string} fieldName - Field name
 * @param {number} idx - Item index
 * @param {string} value - New value
 */
export function updateArrayItem(fieldName, idx, value) {
    const values = getArrayFieldValues(fieldName);
    values[idx] = value;
    import('../expert/sections.js').then(module => {
        if (module.updateFieldValue) {
            module.updateFieldValue(fieldName, values);
        }
    });
    markDirty();
}
// Expose functions to window for inline handlers
if (typeof window !== 'undefined') {
    window.arrayRemoveItem = removeArrayItem;
    window.arrayUpdateItem = updateArrayItem;
    window.arrayAddItem = addArrayItem;
}