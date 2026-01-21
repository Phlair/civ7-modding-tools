/**
 * Form Module - Validation
 * Handles field validation and error display
 */

import { AUTOCOMPLETE_MAPPINGS, getCurrentData } from '../state.js';
import { getAvailableBindings } from './fields.js';

/**
 * Validate mod data structure
 * @returns {Object} Validation result with isValid and errors
 */
export function validateModData() {
    const currentData = getCurrentData();
    const errors = [];
    
    // Check metadata
    if (!currentData.metadata?.id) errors.push("Metadata: missing 'id'");
    if (!currentData.metadata?.version) errors.push("Metadata: missing 'version'");
    
    // Check required fields per section
    if (currentData.units?.length > 0) {
        currentData.units.forEach((unit, i) => {
            if (!unit.id) errors.push(`Units[${i}]: missing 'id'`);
            if (!unit.unit_type) errors.push(`Units[${i}]: missing 'unit_type'`);
        });
    }
    
    if (currentData.constructibles?.length > 0) {
        currentData.constructibles.forEach((constructible, i) => {
            if (!constructible.id) errors.push(`Constructibles[${i}]: missing 'id'`);
            if (!constructible.constructible_type) errors.push(`Constructibles[${i}]: missing 'constructible_type'`);
        });
    }
    
    if (currentData.modifiers?.length > 0) {
        currentData.modifiers.forEach((modifier, i) => {
            if (!modifier.id) errors.push(`Modifiers[${i}]: missing 'id'`);
            if (!modifier.modifier) errors.push(`Modifiers[${i}]: missing 'modifier'`);
        });
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors,
    };
}

/**
 * Validate field on blur event
 * @param {string} fieldName - Field name
 * @param {string} value - Field value
 * @returns {Promise<void>}
 */
export async function validateFieldBlur(fieldName, value) {
    if (!value || value.length === 0) return; // Skip empty fields
    
    // Extract field type from dot notation
    const fieldType = fieldName.split('.').pop();
    
    // Skip validation for non-autocomplete fields
    if (!AUTOCOMPLETE_MAPPINGS[fieldType] && !fieldName.includes('binding')) return;
    
    // Get the input element
    const inputs = document.querySelectorAll(`input[data-field-name="${fieldName}"]`);
    if (inputs.length === 0) return;
    
    const input = inputs[inputs.length - 1];
    const wrapper = input.closest('div[class*="relative"]') || input.parentElement;
    
    // Validate against reference data
    try {
        const dataType = AUTOCOMPLETE_MAPPINGS[fieldType];
        
        if (!dataType && !fieldName.includes('binding')) return;
        
        let isValid = false;
        
        if (fieldName.includes('binding')) {
            // Validate against available bindings
            const availableBindings = getAvailableBindings();
            isValid = availableBindings.includes(value);
            
            if (!isValid && value.length > 0) {
                showFieldError(wrapper, `Binding "${value}" not found. Available: ${availableBindings.slice(0, 3).join(', ')}...`);
                return;
            }
        } else {
            // Validate against reference data
            const response = await fetch(`/api/data/${dataType}`);
            if (response.ok) {
                const data = await response.json();
                const validIds = data.values ? data.values.map(v => v.id) : [];
                isValid = validIds.includes(value);
                
                if (!isValid && value.length > 0) {
                    const suggestions = validIds.filter(id => id.toLowerCase().includes(value.toLowerCase())).slice(0, 3);
                    showFieldError(wrapper, 
                        `"${value}" is not a valid ${fieldType}. ${suggestions.length > 0 ? `Did you mean: ${suggestions.join(', ')}?` : 'Check reference data for valid options.'}`
                    );
                    return;
                }
            }
        }
        
        // Clear error if valid
        clearFieldError(wrapper);
    } catch (error) {
        console.error('Validation error:', error);
    }
}

/**
 * Validate field dependencies
 * @param {string} fieldName - Field name
 * @param {string} value - Field value
 */
export function validateFieldDependency(fieldName, value) {
    // Validate dependencies between fields
    // Example: if effect field changes, warn if arguments array might be invalid
    
    if (fieldName.includes('effect') && value.startsWith('EFFECT_')) {
        // Future: could check if required arguments exist
    }
    
    if (fieldName.includes('requirement_type') && value.startsWith('REQUIREMENT_')) {
        // Future: could validate requirement configuration
    }
}

/**
 * Show error message for a field
 * @param {HTMLElement} wrapper - Field wrapper element
 * @param {string} message - Error message
 */
export function showFieldError(wrapper, message) {
    // Remove existing error
    const existingError = wrapper.querySelector('.field-error');
    if (existingError) existingError.remove();
    
    // Add red border to input
    const input = wrapper.querySelector('input');
    if (input) {
        input.classList.add('border-red-500', 'bg-red-900/10');
        input.classList.remove('border-slate-600');
    }
    
    // Show error message below
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error text-xs text-red-400 mt-1 bg-red-900/20 p-2 rounded border border-red-700/50';
    errorDiv.textContent = '✗ ' + message;
    wrapper.appendChild(errorDiv);
}

/**
 * Clear error message for a field
 * @param {HTMLElement} wrapper - Field wrapper element
 */
export function clearFieldError(wrapper) {
    // Remove error styling
    const input = wrapper.querySelector('input');
    if (input) {
        input.classList.remove('border-red-500', 'bg-red-900/10');
        input.classList.add('border-slate-600');
    }
    
    // Remove error message
    const errorDiv = wrapper.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}
