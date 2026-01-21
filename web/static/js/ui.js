/**
 * UI Module - Toast notifications, modals, loading states
 * Pure UI functions with no data dependencies
 */

/**
 * Display a toast notification for 3 seconds
 * @param {string} message - Message to display
 * @param {'info' | 'success' | 'error'} type - Toast type (default: 'info')
 */
export function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const bgClass = type === 'error' ? 'bg-red-600' : type === 'success' ? 'bg-green-600' : 'bg-blue-600';
    
    toast.innerHTML = `
        <div class="fixed bottom-4 right-4 ${bgClass} text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in z-50">
            ${message}
        </div>
    `;
    
    container.appendChild(toast.firstElementChild);
    
    setTimeout(() => {
        toast.firstElementChild?.remove();
    }, 3000);
}

/**
 * Create toast container if it doesn't exist
 * @returns {HTMLElement} Toast container element
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
    return container;
}

/**
 * Show loading spinner overlay
 * Replaces editor content with spinner
 */
export function showLoading() {
    const editorContainer = document.getElementById('editor-container');
    if (!editorContainer) return;
    
    editorContainer.innerHTML = `
        <div class="flex items-center justify-center h-screen">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                <p class="text-slate-400">Loading...</p>
            </div>
        </div>
    `;
}

/**
 * Show field help modal
 * @param {string} fieldLabel - Field label/title
 * @param {string} helpText - Help content
 */
export function showFieldHelpModal(fieldLabel, helpText) {
    const modal = document.getElementById('help-modal') || createHelpModal();
    
    modal.querySelector('.modal-title').textContent = fieldLabel;
    modal.querySelector('.modal-content').textContent = helpText;
    modal.classList.remove('hidden');
}

/**
 * Hide field help modal
 */
export function hideFieldHelpModal() {
    const modal = document.getElementById('help-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

/**
 * Create help modal if it doesn't exist
 * @returns {HTMLElement} Help modal element
 */
function createHelpModal() {
    const modal = document.createElement('div');
    modal.id = 'help-modal';
    modal.className = 'hidden fixed inset-0 bg-black/50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-slate-900 border border-slate-700 rounded-lg p-6 max-w-md">
            <h3 class="modal-title text-lg font-semibold text-slate-200 mb-2"></h3>
            <p class="modal-content text-slate-400 text-sm mb-4"></p>
            <button 
                onclick="import('./ui.js').then(m => m.hideFieldHelpModal())"
                class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
            >
                Close
            </button>
        </div>
    `;
    document.body.appendChild(modal);
    return modal;
}

/**
 * Update dirty indicator in UI
 * Shows/hides unsaved changes indicator and enables/disables save button
 * @param {boolean} isDirty - Whether data has unsaved changes
 */
export function updateDirtyIndicator(isDirty) {
    const dirtyIndicator = document.getElementById('dirty-indicator');
    const saveBtn = document.getElementById('save-btn');
    
    if (dirtyIndicator) {
        if (isDirty) {
            dirtyIndicator.classList.remove('hidden');
        } else {
            dirtyIndicator.classList.add('hidden');
        }
    }
    
    if (saveBtn) {
        saveBtn.disabled = !isDirty;
        saveBtn.classList.toggle('opacity-50', !isDirty);
    }
}

/**
 * Add error styling to form field
 * @param {HTMLElement} wrapper - Field wrapper element
 * @param {string} message - Error message to display
 */
export function showFieldError(wrapper, message) {
    if (!wrapper) return;
    
    // Remove existing error if present
    const existingError = wrapper.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    wrapper.classList.add('border-red-600', 'bg-red-900/20');
    
    const errorEl = document.createElement('p');
    errorEl.className = 'field-error text-red-400 text-xs mt-1';
    errorEl.textContent = message;
    wrapper.appendChild(errorEl);
}

/**
 * Remove error styling from form field
 * @param {HTMLElement} wrapper - Field wrapper element
 */
export function clearFieldError(wrapper) {
    if (!wrapper) return;
    
    wrapper.classList.remove('border-red-600', 'bg-red-900/20');
    
    const errorEl = wrapper.querySelector('.field-error');
    if (errorEl) {
        errorEl.remove();
    }
}
