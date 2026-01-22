/**
 * Main Entry Point - Editor Application
 * Initializes all modules and sets up event listeners
 */

import { 
    initializeMode, 
    switchMode, 
    skipWizard,
    wizardPrevStep,
    wizardNextStep,
    createNewMod
} from './wizard/wizard.js';
import { healthCheck, loadFile, saveFile, exportYAML } from './api.js';
import { showToast } from './ui.js';
import { showTemplateModal, hideTemplateModal, loadTemplate } from './templates.js';
import { loadReferenceData } from './data/loader.js';
import * as state from './state.js';

// Expose to global scope IMMEDIATELY for inline handlers (HTML onclick compatibility)
// These must be exposed synchronously before DOMContentLoaded
Object.defineProperty(window, 'switchMode', {
    value: switchMode,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'skipWizard', {
    value: skipWizard,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'wizardPrevStep', {
    value: wizardPrevStep,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'wizardNextStep', {
    value: wizardNextStep,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'createNew', {
    value: createNewMod,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'loadFile', {
    value: async () => {
        const filePathInput = document.getElementById('file-path-input');
        if (filePathInput && filePathInput.value) {
            try {
                const result = await loadFile(filePathInput.value);
                if (result && result.data) {
                    state.setCurrentData(result.data);
                    state.setCurrentFilePath(result.path || filePathInput.value);
                    // Populate wizard with loaded data
                    state.populateWizardFromData(result.data);
                    // Switch to guided mode to use the wizard for editing
                    const { switchMode } = await import('./wizard/wizard.js');
                    switchMode('guided', true);
                    showToast('File loaded! Use the wizard to edit it.', 'success');
                }
            } catch (error) {
                showToast('Error loading file', 'error');
            }
        } else {
            showToast('Please enter a file path', 'error');
        }
    },
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'saveFile', {
    value: async () => {
        if (!state.currentFilePath) {
            showToast('Please load or specify a file path first', 'error');
            return;
        }
        try {
            await saveFile(state.currentFilePath, state.currentData);
            state.isDirty = false;
            showToast('File saved successfully', 'success');
        } catch (error) {
            showToast('Error saving file', 'error');
        }
    },
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'exportYAML', {
    value: async () => {
        try {
            const blob = await exportYAML(state.currentData);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'mod.yml';
            a.click();
            URL.revokeObjectURL(url);
            showToast('Export successful', 'success');
        } catch (error) {
            showToast('Error exporting file', 'error');
        }
    },
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'showTemplateModal', {
    value: showTemplateModal,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'hideTemplateModal', {
    value: hideTemplateModal,
    writable: false,
    configurable: false
});

Object.defineProperty(window, 'loadTemplate', {
    value: async (templateName) => {
        try {
            const data = await loadTemplate(templateName);
            if (data) {
                state.setCurrentData(data);
                // Populate wizard with template data
                state.populateWizardFromData(data);
                // Switch to guided mode to use the wizard with template
                const { switchMode } = await import('./wizard/wizard.js');
                switchMode('guided', true);
                showToast(`Template "${templateName}" loaded! Use the wizard to customize it.`, 'success');
            }
        } catch (error) {
            showToast('Error loading template', 'error');
        }
    },
    writable: false,
    configurable: false
});

/**
 * Initialize application on DOM ready
 */
document.addEventListener('DOMContentLoaded', async () => {
    // Check backend health
    try {
        await healthCheck();
    } catch (error) {
        console.error('Backend health check failed:', error);
        showToast('Warning: Backend may be unavailable', 'error');
    }

    // Load reference data for autocomplete fields
    try {
        await loadReferenceData();
        console.log('[REFERENCE_DATA] Reference data loaded');
    } catch (error) {
        console.error('Failed to load reference data:', error);
    }

    // Initialize mode (guided or expert)
    initializeMode();

    // Setup event listeners
    setupEventListeners();

    console.log('[APP_INITIALIZED] Editor application ready');
});

/**
 * Setup global event listeners
 */
function setupEventListeners() {
    // File path input - load on Enter
    const filePathInput = document.getElementById('file-path-input');
    if (filePathInput) {
        filePathInput.addEventListener('keypress', async (e) => {
            if (e.key === 'Enter') {
                const { loadFile } = await import('./api.js');
                await loadFile(filePathInput.value);
            }
        });
    }

    // Save button
    const saveBtn = document.getElementById('save-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            const { saveFile } = await import('./api.js');
            if (!state.currentFilePath) {
                showToast('Please load or specify a file path first', 'error');
                return;
            }
            try {
                await saveFile(state.currentFilePath, state.currentData);
                state.isDirty = false;
                showToast('File saved successfully', 'success');
            } catch (error) {
                showToast('Error saving file', 'error');
            }
        });
    }

    // Mode toggle buttons
    const guidedBtn = document.getElementById('mode-guided');
    const expertBtn = document.getElementById('mode-expert');

    if (guidedBtn) {
        guidedBtn.addEventListener('click', async () => {
            const { switchMode } = await import('./wizard/wizard.js');
            switchMode('guided');
        });
    }

    if (expertBtn) {
        expertBtn.addEventListener('click', async () => {
            const { switchMode } = await import('./wizard/wizard.js');
            switchMode('expert');
        });
    }
}

// Export for testing and external use
export { setupEventListeners };
