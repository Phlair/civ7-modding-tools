/**
 * Tests for state.js module
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import * as state from '../static/js/state.js';

describe('State Module', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Reset state for each test
        state.clearAllState();
    });

    describe('Initial State', () => {
        it('should initialize with empty current data', () => {
            expect(state.currentData).toEqual({});
        });

        it('should initialize with empty file path', () => {
            expect(state.currentFilePath).toEqual('');
        });

        it('should initialize with clean state', () => {
            expect(state.isDirty).toBe(false);
        });

        it('should initialize with guided mode', () => {
            expect(state.currentMode).toBe('guided');
        });

        it('should initialize with wizard step 1', () => {
            expect(state.wizardStep).toBe(1);
        });
    });

    describe('Configuration Objects', () => {
        it('should have autocomplete mappings', () => {
            expect(state.AUTOCOMPLETE_MAPPINGS).toBeDefined();
            expect(typeof state.AUTOCOMPLETE_MAPPINGS).toBe('object');
        });

        it('should have field help text', () => {
            expect(state.FIELD_HELP_TEXT).toBeDefined();
            expect(typeof state.FIELD_HELP_TEXT).toBe('object');
        });

        it('should have required fields config', () => {
            expect(state.REQUIRED_FIELDS).toBeDefined();
            expect(state.REQUIRED_FIELDS.units).toEqual(['id', 'unit_type']);
        });

        it('should map yield_type to yield-types', () => {
            expect(state.AUTOCOMPLETE_MAPPINGS.yield_type).toBe('yield-types');
        });

        it('should have help text for yield_type', () => {
            expect(state.FIELD_HELP_TEXT.yield_type).toBeDefined();
        });
    });

    describe('markDirty', () => {
        it('should set isDirty to true', () => {
            state.markDirty();
            expect(state.isDirty).toBe(true);
        });

        it('should persist dirty state across calls', () => {
            state.markDirty();
            state.markDirty();
            expect(state.isDirty).toBe(true);
        });
    });

    describe('setCurrentData', () => {
        it('should update current data', () => {
            const data = { id: 'test', name: 'Test Mod' };
            state.setCurrentData(data);
            expect(state.currentData).toEqual(data);
        });

        it('should replace previous data', () => {
            state.setCurrentData({ id: 'old' });
            state.setCurrentData({ id: 'new' });
            expect(state.currentData.id).toBe('new');
        });
    });

    describe('setCurrentFilePath', () => {
        it('should update current file path', () => {
            state.setCurrentFilePath('/path/to/file.yml');
            expect(state.currentFilePath).toBe('/path/to/file.yml');
        });

        it('should replace previous path', () => {
            state.setCurrentFilePath('/old/path.yml');
            state.setCurrentFilePath('/new/path.yml');
            expect(state.currentFilePath).toBe('/new/path.yml');
        });
    });

    describe('setCurrentMode', () => {
        it('should update mode to expert', () => {
            state.setCurrentMode('expert');
            expect(state.currentMode).toBe('expert');
        });

        it('should update mode back to guided', () => {
            state.setCurrentMode('expert');
            state.setCurrentMode('guided');
            expect(state.currentMode).toBe('guided');
        });
    });

    describe('resetWizardData', () => {
        it('should reset wizard step to 1', () => {
            state.setWizardStep(5);
            state.resetWizardData();
            expect(state.getWizardStep()).toBe(1);
        });

        it('should initialize wizard data structure', () => {
            state.resetWizardData();
            expect(state.wizardData).toHaveProperty('metadata');
            expect(state.wizardData).toHaveProperty('units');
            expect(state.wizardData).toHaveProperty('constructibles');
        });

        it('should create empty arrays for complex sections', () => {
            state.resetWizardData();
            expect(Array.isArray(state.wizardData.units)).toBe(true);
            expect(state.wizardData.units).toHaveLength(0);
        });

        it('should initialize build configuration', () => {
            state.resetWizardData();
            expect(state.wizardData.build).toHaveProperty('builders');
        });

        it('should clear building yields', () => {
            const data = state.getWizardData();
            data.buildingYields = [{ type: 'PRODUCTION', amount: 5 }];
            state.resetWizardData();
            expect(state.getWizardData().buildingYields || []).toHaveLength(0);
        });
    });

    describe('setWizardStep', () => {
        it('should update wizard step', () => {
            state.setWizardStep(3);
            expect(state.wizardStep).toBe(3);
        });

        it('should handle step 5', () => {
            state.setWizardStep(5);
            expect(state.wizardStep).toBe(5);
        });
    });

    // autocompleteUsageStats is managed in form/fields.js module, not state

    describe('clearAllState', () => {
        it('should reset all state to initial values', () => {
            state.setCurrentData({ id: 'test' });
            state.setCurrentFilePath('/path.yml');
            state.markDirty();
            state.setCurrentMode('expert');

            state.clearAllState();

            expect(state.currentData).toEqual({});
            expect(state.currentFilePath).toBe('');
            expect(state.isDirty).toBe(false);
        });

        it('should reset wizard state', () => {
            state.setWizardStep(5);
            state.clearAllState();
            expect(state.getWizardStep()).toBe(1);
        });
    });

    describe('syncWizardToCurrentData', () => {
        it('should merge wizard data into current data', () => {
            state.setCurrentData({ id: 'existing' });
            const wizData = state.getWizardData();
            wizData.metadata = { name: 'Test' };

            state.syncWizardToCurrentData();

            expect(state.getCurrentData()).toHaveProperty('id', 'existing');
            expect(state.getCurrentData()).toHaveProperty('metadata');
        });

        it('should preserve existing data when merging', () => {
            state.setCurrentData({ id: 'mod-1', version: '1.0.0' });
            const wizData = state.getWizardData();
            wizData.metadata = { name: 'Test' };

            state.syncWizardToCurrentData();

            expect(state.getCurrentData().id).toBe('mod-1');
            expect(state.getCurrentData().version).toBe('1.0.0');
        });
    });

    describe('Reference Data Cache', () => {
        it('should cache reference data', () => {
            const data = ['YIELD_PRODUCTION', 'YIELD_SCIENCE'];
            state.setCachedReferenceData('yield-types', data);

            expect(state.getCachedReferenceData('yield-types')).toEqual(data);
        });

        it('should return null for uncached data', () => {
            expect(state.getCachedReferenceData('nonexistent')).toBeNull();
        });

        it('should cache multiple data types', () => {
            state.setCachedReferenceData('yield-types', ['PRODUCTION']);
            state.setCachedReferenceData('effects', ['ADJUST_YIELD']);

            expect(state.getCachedReferenceData('yield-types')).toEqual(['PRODUCTION']);
            expect(state.getCachedReferenceData('effects')).toEqual(['ADJUST_YIELD']);
        });

        it('should clear cache', () => {
            state.setCachedReferenceData('yield-types', ['PRODUCTION']);
            state.clearReferenceDataCache();

            expect(state.getCachedReferenceData('yield-types')).toBeNull();
        });
    });
});
