/**
 * Templates Module - Template loading and management
 * Handles predefined mod templates for wizard
 */

/**
 * Show template selection modal
 */
export function showTemplateModal() {
    const modal = document.getElementById('template-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

/**
 * Hide template selection modal
 */
export function hideTemplateModal() {
    const modal = document.getElementById('template-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

/**
 * Load a predefined template and initialize wizard or editor
 * @param {string} templateName - Name of template (blank, scientific, military, cultural, economic)
 * @returns {Promise<Object>} Template data
 */
export async function loadTemplate(templateName) {
    try {
        const response = await fetch(`/api/template/${templateName}`);
        if (!response.ok) {
            throw new Error(`Failed to load template: ${response.statusText}`);
        }
        
        const templateData = await response.json();
        hideTemplateModal();
        return templateData;
    } catch (error) {
        console.error('[TEMPLATE_ERROR]', error);
        throw error;
    }
}

/**
 * Get list of available templates
 * @returns {Promise<Array>} List of template names
 */
export async function getAvailableTemplates() {
    return [
        { name: 'blank', label: 'Blank Mod', description: 'Start from scratch' },
        { name: 'scientific', label: 'Scientific Civilization', description: 'Research-focused civ' },
        { name: 'military', label: 'Military Civilization', description: 'Combat-focused civ' },
        { name: 'cultural', label: 'Cultural Civilization', description: 'Culture-focused civ' },
        { name: 'economic', label: 'Economic Civilization', description: 'Gold/production-focused civ' },
    ];
}
