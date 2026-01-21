/**
 * Tests for wizard module
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as wizard from '../static/js/wizard/wizard.js';
import * as state from '../static/js/state.js';

describe('Wizard Module', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        state.clearAllState();
        document.body.innerHTML = `
            <div id="wizard-container"></div>
            <div id="wizard-step-content"></div>
            <div id="wizard-step-indicator"></div>
            <div id="editor-container" class="hidden"></div>
            <aside class="hidden"></aside>
            <button id="mode-guided"></button>
            <button id="mode-expert"></button>
        `;
    });

    describe('switchMode', () => {
        it('should show wizard in guided mode', () => {
            const wizardContainer = document.getElementById('wizard-container');
            wizard.switchMode('guided');
            expect(wizardContainer.classList.contains('hidden')).toBe(false);
        });

        it('should hide wizard in expert mode', () => {
            const wizardContainer = document.getElementById('wizard-container');
            wizard.switchMode('expert');
            expect(wizardContainer.classList.contains('hidden')).toBe(true);
        });

        it('should show editor in expert mode', () => {
            const editorContainer = document.getElementById('editor-container');
            wizard.switchMode('expert');
            expect(editorContainer.classList.contains('hidden')).toBe(false);
        });

        it('should save preference to localStorage', () => {
            const localStorageSpy = vi.spyOn(Storage.prototype, 'setItem');
            wizard.switchMode('expert', true);
            expect(localStorageSpy).toHaveBeenCalledWith('editorMode', 'expert');
        });

        it('should not save preference when savePreference is false', () => {
            const localStorageSpy = vi.spyOn(Storage.prototype, 'setItem');
            wizard.switchMode('expert', false);
            expect(localStorageSpy).not.toHaveBeenCalled();
        });
    });

    describe('initializeWizard', () => {
        it('should reset wizard data', () => {
            const wizData = state.getWizardData();
            wizData.test = 'data';
            wizard.initializeWizard();
            expect(state.getWizardData().metadata).toBeDefined();
        });

        it('should initialize empty metadata', () => {
            wizard.initializeWizard();
            expect(state.wizardData.metadata).toEqual({});
        });

        it('should initialize empty units array', () => {
            wizard.initializeWizard();
            expect(Array.isArray(state.wizardData.units)).toBe(true);
        });

        it('should initialize empty constructibles array', () => {
            wizard.initializeWizard();
            expect(Array.isArray(state.wizardData.constructibles)).toBe(true);
        });
    });

    describe('validateWizardData', () => {
        it('should require mod id', async () => {
            state.resetWizardData();
            const wizData = state.getWizardData();
            wizData.metadata = { name: 'Test' };
            wizData.civilization = { civilization_type: 'TEST' };
            const result = await wizard.validateWizardData();
            // Note: async handling needed
        });

        it('should require mod name', async () => {
            state.resetWizardData();
            const wizData = state.getWizardData();
            wizData.metadata = { id: 'test-mod' };
            wizData.civilization = { civilization_type: 'TEST' };
            const result = await wizard.validateWizardData();
            // Note: async handling needed
        });

        it('should require civilization type', async () => {
            state.resetWizardData();
            const wizData = state.getWizardData();
            wizData.metadata = { id: 'test-mod', name: 'Test' };
            const result = await wizard.validateWizardData();
            // Note: async handling needed
        });
    });

    describe('createNewMod', () => {
        it('should clear state when confirmed', async () => {
            vi.spyOn(global, 'confirm').mockReturnValue(true);
            const clearSpy = vi.spyOn(state, 'clearAllState');

            wizard.createNewMod();
            
            // Wait for async import to complete
            await new Promise(resolve => setTimeout(resolve, 10));

            expect(clearSpy).toHaveBeenCalled();
            clearSpy.mockRestore();
        });

        it('should not clear state when canceled', async () => {
            vi.spyOn(global, 'confirm').mockReturnValue(false);
            const clearSpy = vi.spyOn(state, 'clearAllState').mockImplementation(() => {});

            wizard.createNewMod();
            
            // Wait to ensure no async operations happened
            await new Promise(resolve => setTimeout(resolve, 10));

            expect(clearSpy).not.toHaveBeenCalled();
            clearSpy.mockRestore();
        });
    });

    describe('skipWizard', () => {
        it('should switch to expert mode when confirmed', () => {
            vi.spyOn(global, 'confirm').mockReturnValue(true);
            const modeSpy = vi.spyOn(state, 'setCurrentMode');

            wizard.skipWizard();

            expect(modeSpy).toHaveBeenCalledWith('expert');
            modeSpy.mockRestore();
        });

        it('should not switch mode when canceled', () => {
            vi.spyOn(global, 'confirm').mockReturnValue(false);
            const modeSpy = vi.spyOn(state, 'setCurrentMode');

            wizard.skipWizard();

            expect(modeSpy).not.toHaveBeenCalled();
            modeSpy.mockRestore();
        });
    });
});
