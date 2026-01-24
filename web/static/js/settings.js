/**
 * Settings Module - User preferences and configuration
 * Manages OpenAI API key and icon generation settings
 */

import { showToast } from './ui.js';
import { updateSettings, getSettings } from './state.js';

/**
 * Show settings modal
 */
export function showSettingsModal() {
    const settings = getSettings();
    
    // Remove existing modal if present
    document.querySelectorAll('.settings-modal').forEach(m => m.remove());
    
    const modal = document.createElement('div');
    modal.className = 'settings-modal fixed inset-0 bg-black/50 flex items-center justify-center z-50';
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    };
    
    const apiKey = settings.openai?.apiKey || '';
    const defaultModel = settings.openai?.defaultModel || 'gpt-image-1.5';
    const defaultQuality = settings.openai?.defaultQuality || 'medium';
    const downloadPath = settings.export?.downloadPath || '';
    const useDiskPath = settings.export?.useDiskPath || false;
    
    modal.innerHTML = `
        <div class="bg-slate-900 border border-slate-700 rounded-lg p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
            <h3 class="text-xl font-semibold text-slate-200 mb-1">⚙️ Settings</h3>
            <p class="text-xs text-slate-500 mb-6">Configure preferences</p>
            
            <div class="space-y-4">
                <!-- Export Path Section -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-2">
                        Export Options
                    </label>
                    <div class="flex items-center gap-2 mb-3">
                        <input 
                            type="checkbox"
                            id="settings-use-disk-path"
                            ${useDiskPath ? 'checked' : ''}
                            class="w-4 h-4"
                        />
                        <label for="settings-use-disk-path" class="text-sm text-slate-300">
                            Save exports to disk instead of browser download
                        </label>
                    </div>
                    <input 
                        type="text" 
                        id="settings-download-path"
                        value="${downloadPath}"
                        placeholder="e.g., C:\\Users\\Username\\Downloads or /home/user/Downloads"
                        class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400 disabled:opacity-50 disabled:bg-slate-900"
                        ${!useDiskPath ? 'disabled' : ''}
                    />
                    <p class="text-xs text-slate-500 mt-1">
                        Leave empty to use browser download. When set, exports will be saved directly to this folder.
                    </p>
                </div>
                
                <!-- API Key Section -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-1">
                        OpenAI API Key <span class="text-red-400">*</span>
                    </label>
                    <div class="flex gap-2">
                        <input 
                            type="password" 
                            id="settings-api-key"
                            value="${apiKey}"
                            placeholder="sk-proj-..."
                            class="flex-1 px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                        />
                        <button 
                            onclick="window.toggleApiKeyVisibility()"
                            class="px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm font-medium"
                            id="toggle-key-btn"
                            title="Show/hide API key"
                        >
                            👁️
                        </button>
                    </div>
                    <p class="text-xs text-amber-400 mt-2">
                        ⚠️ Key stored locally in your browser. Never share with others.
                    </p>
                    <p class="text-xs text-slate-500 mt-2">
                        Get your free key at <a href="https://platform.openai.com/api-keys" target="_blank" class="text-blue-400 hover:text-blue-300">platform.openai.com/api-keys</a>
                    </p>
                </div>
                
                <!-- Model Selection -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-1">
                        Model
                    </label>
                    <select 
                        id="settings-model"
                        class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                    >
                        <option value="gpt-image-1.5" ${defaultModel === 'gpt-image-1.5' ? 'selected' : ''}>
                            GPT Image 1.5 (Recommended - ~$0.15/image)
                        </option>
                        <option value="gpt-image-1-mini" ${defaultModel === 'gpt-image-1-mini' ? 'selected' : ''}>
                            GPT Image 1 Mini (Cheaper - ~$0.04/image)
                        </option>
                    </select>
                    <p class="text-xs text-slate-500 mt-1">
                        GPT Image 1.5 provides better quality with reference images
                    </p>
                </div>
                
                <!-- Quality Selection -->
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-1">
                        Output Quality
                    </label>
                    <select 
                        id="settings-quality"
                        class="w-full px-3 py-2 bg-slate-800 border border-slate-600 rounded-lg text-sm focus:outline-none focus:border-blue-400"
                    >
                        <option value="low" ${defaultQuality === 'low' ? 'selected' : ''}>Low (Fast)</option>
                        <option value="medium" ${defaultQuality === 'medium' ? 'selected' : ''}>Medium (Balanced)</option>
                        <option value="high" ${defaultQuality === 'high' ? 'selected' : ''}>High (Best quality)</option>
                    </select>
                </div>
                
                <!-- Info Box -->
                <div class="bg-blue-900/20 border border-blue-700 rounded-lg p-3 text-xs text-blue-300">
                    <p class="font-semibold mb-1">💡 How icon generation works:</p>
                    <ol class="list-decimal list-inside space-y-1 text-blue-200">
                        <li>Enter a description of your icon (e.g., "Eagle with blue and gold")</li>
                        <li>System uses reference icons to match art style</li>
                        <li>AI generates a 256x256 PNG with transparent background</li>
                        <li>Review and save to your mod</li>
                    </ol>
                </div>
                
                <!-- Action Buttons -->
                <div class="flex gap-2 pt-4">
                    <button 
                        onclick="window.saveSettings()"
                        class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium"
                    >
                        Save Settings
                    </button>
                    <button 
                        onclick="document.querySelector('.settings-modal').remove()"
                        class="flex-1 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg font-medium"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Setup checkbox toggle after modal is in DOM
    const checkbox = document.getElementById('settings-use-disk-path');
    const input = document.getElementById('settings-download-path');
    if (checkbox && input) {
        checkbox.addEventListener('change', () => {
            input.disabled = !checkbox.checked;
        });
    }
}

/**
 * Toggle API key visibility
 */
export function toggleApiKeyVisibility() {
    const input = document.querySelector('#settings-api-key');
    const btn = document.querySelector('#toggle-key-btn');
    
    if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = '🙈';
    } else {
        input.type = 'password';
        btn.textContent = '👁️';
    }
}

/**
 * Save settings to localStorage
 */
export function saveSettings() {
    const apiKey = document.querySelector('#settings-api-key')?.value || '';
    const model = document.querySelector('#settings-model')?.value || 'gpt-image-1.5';
    const quality = document.querySelector('#settings-quality')?.value || 'medium';
    const useDiskPath = document.querySelector('#settings-use-disk-path')?.checked || false;
    const downloadPath = document.querySelector('#settings-download-path')?.value || '';
    
    if (!apiKey.trim()) {
        showToast('Please enter your OpenAI API key', 'error');
        return;
    }
    
    if (!apiKey.startsWith('sk-')) {
        showToast('API key should start with "sk-"', 'error');
        return;
    }

    if (useDiskPath && !downloadPath.trim()) {
        showToast('Please enter a download path when disk saving is enabled', 'error');
        return;
    }
    
    updateSettings('openai.apiKey', apiKey);
    updateSettings('openai.defaultModel', model);
    updateSettings('openai.defaultQuality', quality);
    updateSettings('export.useDiskPath', useDiskPath);
    updateSettings('export.downloadPath', downloadPath);
    
    showToast('Settings saved successfully', 'success');
    document.querySelector('.settings-modal').remove();
}
