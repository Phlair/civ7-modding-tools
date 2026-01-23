/**
 * Icon Generation Module - AI-powered icon generation using OpenAI
 * Handles UI for icon generation with reference image selection
 */

import { showToast, showLoading } from './ui.js';
import { getSettings, markDirty, updateFieldValue } from './state.js';

// Reference icons available for styling
const REFERENCE_ICONS = [
    'america', 'assyria', 'chola', 'greece', 'maya', 'norman', 'russia'
];

/**
 * Generate civilization icon
 */
export function generateCivIcon() {
    const settings = getSettings();
    
    if (!settings.openai?.apiKey) {
        showToast('❌ Please configure OpenAI API key in Settings', 'error');
        return;
    }
    
    showIconGenerationModal('civilization', 'Civilization');
}

/**
 * Generate unit icon
 */
export function generateUnitIcon() {
    const settings = getSettings();
    
    if (!settings.openai?.apiKey) {
        showToast('❌ Please configure OpenAI API key in Settings', 'error');
        return;
    }
    
    showIconGenerationModal('unit', 'Unit');
}

/**
 * Generate building icon
 */
export function generateBuildingIcon() {
    const settings = getSettings();
    
    if (!settings.openai?.apiKey) {
        showToast('❌ Please configure OpenAI API key in Settings', 'error');
        return;
    }
    
    showIconGenerationModal('building', 'Building');
}

/**
 * Create and show icon generation modal
 */
function showIconGenerationModal(iconType, displayName) {
    // Remove existing modal if present
    document.querySelectorAll('.icon-generation-modal').forEach(m => m.remove());
    
    const modal = document.createElement('div');
    modal.className = 'icon-generation-modal fixed inset-0 bg-black/50 flex items-center justify-center z-50';
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    };
    
    const referenceCheckboxes = REFERENCE_ICONS.map(name => `
        <label class="flex items-center gap-2 p-2 rounded hover:bg-slate-800 cursor-pointer">
            <input 
                type="checkbox" 
                class="reference-checkbox w-4 h-4" 
                data-icon="${name}"
                checked
            />
            <img src="/static/icons/${name}.png" alt="${name}" class="w-12 h-12 rounded border border-slate-600" />
            <span class="text-xs text-slate-300">${name}</span>
        </label>
    `).join('');
    
    modal.innerHTML = `
        <div class="bg-slate-900 border border-slate-700 rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h3 class="text-xl font-semibold text-slate-200 mb-1">✨ Generate ${displayName} Icon</h3>
            <p class="text-xs text-slate-500 mb-6">Describe what you want, AI will create a perfectly styled icon</p>
            
            <div class="space-y-4">
                <!-- Prompt Input -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">
                        Icon Description <span class="text-red-400">*</span>
                    </label>
                    <textarea 
                        id="icon-prompt"
                        placeholder="E.g., 'Ancient Babylon with ziggurat and astronomy symbols, blue and gold colors' or 'Roman legionary soldier with sword and shield'"
                        rows="4"
                        maxlength="500"
                        class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400 resize-none"
                    ></textarea>
                    <p class="text-xs text-slate-500 mt-1">
                        Be descriptive about style, colors, and main elements (max 500 characters)
                    </p>
                </div>
                
                <!-- Reference Icons -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">
                        Reference Style (Auto-selected for consistency)
                    </label>
                    <div class="grid grid-cols-4 gap-2 bg-slate-800/50 p-3 rounded-lg border border-slate-700">
                        ${referenceCheckboxes}
                    </div>
                    <p class="text-xs text-slate-500 mt-2">
                        💡 All 7 example icons are used to match the game's visual style. Uncheck to exclude specific icons.
                    </p>
                </div>
                
                <!-- Preview Area -->
                <div id="icon-preview-container" class="hidden">
                    <label class="block text-sm font-medium text-slate-300 mb-2">Generated Icon Preview</label>
                    <div class="flex justify-center">
                        <img id="icon-preview-image" class="w-64 h-64 border-2 border-blue-500 rounded" />
                    </div>
                    <p class="text-xs text-slate-500 mt-2 text-center">256x256 PNG with transparent background</p>
                </div>
                
                <!-- Progress -->
                <div id="generation-progress" class="hidden">
                    <div class="flex items-center gap-2 text-sm text-slate-300">
                        <div class="animate-spin">⏳</div>
                        <span>Generating icon using GPT Image...</span>
                    </div>
                    <p class="text-xs text-slate-500 mt-2">This takes about 10-20 seconds</p>
                </div>
                
                <!-- Action Buttons -->
                <div class="flex gap-2 pt-4">
                    <button 
                        id="generate-btn"
                        onclick="window.handleIconGenerate('${iconType}')"
                        class="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium transition-colors"
                    >
                        Generate Icon
                    </button>
                    <button 
                        id="save-icon-btn"
                        onclick="window.handleIconSave('${iconType}')"
                        class="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg font-medium transition-colors hidden"
                    >
                        Save & Use
                    </button>
                    <button 
                        onclick="document.querySelector('.icon-generation-modal').remove()"
                        class="flex-1 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg font-medium transition-colors"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

/**
 * Handle icon generation API call
 */
export async function handleIconGenerate(iconType) {
    const prompt = document.querySelector('#icon-prompt')?.value || '';
    
    if (!prompt.trim()) {
        showToast('❌ Please describe the icon you want', 'error');
        return;
    }
    
    if (prompt.trim().length < 10) {
        showToast('❌ Please provide a more detailed description (at least 10 characters)', 'error');
        return;
    }
    
    // Get selected reference images
    const selectedReferences = Array.from(
        document.querySelectorAll('.reference-checkbox:checked')
    ).map(cb => cb.dataset.icon);
    
    const settings = getSettings();
    const generateBtn = document.querySelector('#generate-btn');
    const progressDiv = document.querySelector('#generation-progress');
    
    // Update UI
    generateBtn.disabled = true;
    progressDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/icons/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: prompt,
                icon_type: iconType,
                model: settings.openai?.defaultModel || 'gpt-image-1-mini',
                quality: settings.openai?.defaultQuality || 'medium',
                reference_images: selectedReferences,
                api_key: settings.openai?.apiKey,
            }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Generation failed');
        }
        
        const result = await response.json();
        
        if (result.success) {
            // Store the image data for saving later
            window._generatedIconData = result.image;
            
            // Show preview
            const previewContainer = document.querySelector('#icon-preview-container');
            const previewImg = document.querySelector('#icon-preview-image');
            previewImg.src = `data:image/png;base64,${result.image}`;
            previewContainer.classList.remove('hidden');
            
            // Show save button
            document.querySelector('#save-icon-btn').classList.remove('hidden');
            
            showToast('✅ Icon generated successfully! Click "Save & Use" to add it to your mod.', 'success');
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('[ICON_GEN_ERROR]', error);
        showToast(`❌ Generation failed: ${error.message}`, 'error');
    } finally {
        generateBtn.disabled = false;
        progressDiv.classList.add('hidden');
    }
}

/**
 * Handle saving generated icon
 */
export async function handleIconSave(iconType) {
    const prompt = document.querySelector('#icon-prompt')?.value || '';
    const modal = document.querySelector('.icon-generation-modal');
    
    if (!window._generatedIconData) {
        showToast('❌ No generated icon found. Please generate first.', 'error');
        return;
    }
    
    try {
        // Generate a target name based on type
        const timestamp = Date.now();
        const targetName = `icon_${iconType}_${timestamp}`;
        
        // Call API to save icon
        const response = await fetch('/api/icons/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image_b64: window._generatedIconData,
                icon_type: iconType,
                target_name: targetName,
                prompt: prompt,
            }),
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to save');
        }
        
        const result = await response.json();
        
        if (result.success) {
            // Update the appropriate field based on icon type
            const iconPath = result.icon_path;
            
            if (iconType === 'civilization') {
                const iconInput = document.querySelector('#wizard-civ-icon');
                if (iconInput) {
                    iconInput.value = iconPath;
                    iconInput.dispatchEvent(new Event('change'));
                }
            } else if (iconType === 'unit') {
                const iconInput = document.querySelector('#wizard-unit-icon');
                if (iconInput) {
                    iconInput.value = iconPath;
                    iconInput.dispatchEvent(new Event('change'));
                }
            } else if (iconType === 'building') {
                const iconInput = document.querySelector('#wizard-constructible-icon');
                if (iconInput) {
                    iconInput.value = iconPath;
                    iconInput.dispatchEvent(new Event('change'));
                }
            }
            
            // Add import entry to data - update wizardData and sync
            const { wizardData, syncWizardToCurrentData } = await import('./state.js');
            
            if (!wizardData.imports) {
                wizardData.imports = [];
            }
            
            // Remove old icon imports for this type (civilization/unit/building)
            const iconTypePattern = `${iconType}_icon`;
            wizardData.imports = wizardData.imports.filter(
                imp => !imp.id?.includes(iconTypePattern) && !imp.target_name?.startsWith('icon_uploaded')
            );
            
            // Add new import entry
            wizardData.imports.push(result.import_entry);
            
            // SYNC to currentData so export gets the updated imports
            syncWizardToCurrentData();
            
            markDirty();
            showToast(`✅ Icon saved to generated_icons/${result.target_name}.png and added to your mod!`, 'success');
            modal?.remove();
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('[ICON_SAVE_ERROR]', error);
        showToast(`❌ Failed to save icon: ${error.message}`, 'error');
    }
}
