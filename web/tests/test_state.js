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

        it('should use wizard imports when populated', () => {
            // Load file with imports into currentData
            state.setCurrentData({
                id: 'mod-1',
                imports: [
                    { id: 'civilization_icon_uploaded_123', target: 'civilization' },
                    { id: 'unit_icon_uploaded_456', target: 'unit' }
                ]
            });
            
            // Populate wizard from this data
            state.populateWizardFromData(state.getCurrentData());
            
            // Verify wizard has the imports
            expect(state.getWizardData().imports).toHaveLength(2);
            
            // Now simulate filtering out one and adding a new one (like icon handler does)
            const wizData = state.getWizardData();
            wizData.imports = wizData.imports.filter(
                imp => !imp.id?.includes('unit_icon')
            );
            wizData.imports.push({ id: 'unit_icon_new_789', target: 'unit' });
            
            // Sync should preserve the civilization import and the new unit import
            state.syncWizardToCurrentData();
            
            const currentImports = state.getCurrentData().imports;
            expect(currentImports).toHaveLength(2);
            expect(currentImports.some(imp => imp.id === 'civilization_icon_uploaded_123')).toBe(true);
            expect(currentImports.some(imp => imp.id === 'unit_icon_new_789')).toBe(true);
            expect(currentImports.some(imp => imp.id === 'unit_icon_uploaded_456')).toBe(false);
        });

        it('should handle empty imports array correctly', () => {
            state.setCurrentData({
                id: 'mod-1',
                imports: [{ id: 'icon_123' }]
            });
            
            state.populateWizardFromData(state.getCurrentData());
            
            // Manually clear wizard imports
            const wizData = state.getWizardData();
            wizData.imports = [];
            
            // Sync should use the empty array from wizard, not keep existing
            state.syncWizardToCurrentData();
            
            expect(state.getCurrentData().imports).toEqual([]);
        });

        it('should auto-bind modifiers to civilization', () => {
            // Set up wizard data with modifiers
            const wizData = state.getWizardData();
            wizData.modifiers = [
                { id: 'MODIFIER_CIV_BONUS_SCIENCE' },
                { id: 'MODIFIER_CIV_BONUS_CULTURE' }
            ];

            state.syncWizardToCurrentData();

            expect(state.getCurrentData().civilization).toBeDefined();
            expect(state.getCurrentData().civilization.bindings).toBeDefined();
            expect(state.getCurrentData().civilization.bindings).toContain('MODIFIER_CIV_BONUS_SCIENCE');
            expect(state.getCurrentData().civilization.bindings).toContain('MODIFIER_CIV_BONUS_CULTURE');
        });

        it('should not duplicate modifier bindings', () => {
            // Set up existing civilization with one modifier
            state.setCurrentData({
                civilization: {
                    bindings: ['MODIFIER_EXISTING']
                }
            });

            // Add modifiers including the existing one
            const wizData = state.getWizardData();
            wizData.modifiers = [
                { id: 'MODIFIER_EXISTING' },
                { id: 'MODIFIER_NEW' }
            ];

            state.syncWizardToCurrentData();

            expect(state.getCurrentData().civilization.bindings).toHaveLength(2);
            expect(state.getCurrentData().civilization.bindings).toContain('MODIFIER_EXISTING');
            expect(state.getCurrentData().civilization.bindings).toContain('MODIFIER_NEW');
        });

        it('should preserve non-modifier bindings when adding modifiers', () => {
            // Set up civilization with existing bindings (units, buildings, etc.)
            state.setCurrentData({
                civilization: {
                    bindings: ['unit', 'building', 'progression_tree']
                }
            });

            // Add modifiers
            const wizData = state.getWizardData();
            wizData.modifiers = [
                { id: 'MODIFIER_CIV_BONUS' }
            ];

            state.syncWizardToCurrentData();

            expect(state.getCurrentData().civilization.bindings).toHaveLength(4);
            expect(state.getCurrentData().civilization.bindings).toContain('unit');
            expect(state.getCurrentData().civilization.bindings).toContain('building');
            expect(state.getCurrentData().civilization.bindings).toContain('progression_tree');
            expect(state.getCurrentData().civilization.bindings).toContain('MODIFIER_CIV_BONUS');
        });

        it('should handle modifiers without ID gracefully', () => {
            const wizData = state.getWizardData();
            wizData.modifiers = [
                { id: 'MODIFIER_VALID' },
                { modifier: {} }, // No ID field
                { id: null }, // Null ID
                { id: '' } // Empty ID
            ];

            state.syncWizardToCurrentData();

            // Should only add the valid modifier
            expect(state.getCurrentData().civilization.bindings).toHaveLength(1);
            expect(state.getCurrentData().civilization.bindings).toContain('MODIFIER_VALID');
        });

        it('should not add bindings if no modifiers exist', () => {
            const wizData = state.getWizardData();
            wizData.modifiers = [];
            wizData.civilization = {
                civilization_type: 'CIVILIZATION_TEST'
            };

            state.syncWizardToCurrentData();

            // civilization should exist but bindings should not be created
            expect(state.getCurrentData().civilization).toBeDefined();
            expect(state.getCurrentData().civilization.bindings).toBeUndefined();
        });
    });

    describe('populateWizardFromData', () => {
        it('should populate module_localization from loaded YAML', () => {
            const loadedData = {
                module_localization: {
                    name: 'Babylon Module',
                    description: 'Babylon civilization module',
                    authors: 'Phlair',
                },
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.module_localization.name).toBe('Babylon Module');
            expect(state.wizardData.module_localization.description).toBe(
                'Babylon civilization module'
            );
            expect(state.wizardData.module_localization.authors).toBe('Phlair');
        });

        it('should handle action_group as string or object', () => {
            const loadedData1 = {
                action_group: 'AGE_ANTIQUITY',
            };

            state.populateWizardFromData(loadedData1);
            expect(state.wizardData.action_group.action_group_id).toBe('AGE_ANTIQUITY');

            const loadedData2 = {
                action_group: { action_group_id: 'AGE_EXPLORATION' },
            };

            state.populateWizardFromData(loadedData2);
            expect(state.wizardData.action_group.action_group_id).toBe('AGE_EXPLORATION');
        });

        it('should populate metadata from loaded data', () => {
            const loadedData = {
                metadata: {
                    id: 'babylon',
                    version: '1.0.0',
                    name: 'Babylon',
                    description: 'Babylon Civilization',
                    authors: 'Phlair',
                    package: 'Babylon',
                },
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.metadata.id).toBe('babylon');
            expect(state.wizardData.metadata.name).toBe('Babylon');
            expect(state.wizardData.metadata.package).toBe('Babylon');
        });

        it('should populate civilization data from loaded YAML', () => {
            const loadedData = {
                civilization: {
                    civilization_type: 'CIVILIZATION_BABYLON',
                    civilization_traits: ['TRAIT_SCIENTIFIC'],
                    leaders: ['LEADER_HAMMURABI'],
                    vis_art_building_cultures: ['BUILDING_CULTURE_MID'],
                    building_culture_base: 'MUD',
                    vis_art_unit_cultures: ['MidE'],
                    civilization_unlocks: [
                        { age_type: 'AGE_EXPLORATION', type: 'CIVILIZATION_PERSIA' },
                    ],
                },
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.civilization.civilization_type).toBe(
                'CIVILIZATION_BABYLON'
            );
            expect(state.wizardData.civilization.civilization_traits).toEqual([
                'TRAIT_SCIENTIFIC',
            ]);
            expect(state.wizardData.civilization.vis_art_building_cultures).toEqual([
                'BUILDING_CULTURE_MID',
            ]);
            expect(state.wizardData.civilization.building_culture_base).toBe('MUD');
            expect(state.wizardData.civilization.vis_art_unit_cultures).toEqual(['MidE']);
            expect(state.wizardData.civilization.civilization_unlocks).toHaveLength(1);
            expect(state.wizardData.civilization.civilization_unlocks[0].type).toBe(
                'CIVILIZATION_PERSIA'
            );
        });

        it('should populate units array from loaded data', () => {
            const loadedData = {
                units: [
                    { id: 'unit1', unit_type: 'UNIT_BABYLON_SCOUT' },
                    { id: 'unit2', unit_type: 'UNIT_BABYLON_PRIEST' },
                ],
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.units).toHaveLength(2);
            expect(state.wizardData.units[0].id).toBe('unit1');
            expect(state.wizardData.units[1].unit_type).toBe('UNIT_BABYLON_PRIEST');
        });

        it('should populate constructibles array from loaded data', () => {
            const loadedData = {
                constructibles: [
                    { id: 'building1', constructible_type: 'BUILDING_LIBRARY' },
                ],
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.constructibles).toHaveLength(1);
            expect(state.wizardData.constructibles[0].constructible_type).toBe(
                'BUILDING_LIBRARY'
            );
        });

        it('should populate modifiers array from loaded data', () => {
            const loadedData = {
                modifiers: [
                    { id: 'mod1', modifier: { effect: 'ADJUST_YIELD' } },
                ],
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.modifiers).toHaveLength(1);
            expect(state.wizardData.modifiers[0].modifier.effect).toBe('ADJUST_YIELD');
        });

        it('should populate traditions array from loaded data', () => {
            const loadedData = {
                traditions: [{ id: 'trad1', tradition_type: 'TRADITION_SCIENCE' }],
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.traditions).toHaveLength(1);
            expect(state.wizardData.traditions[0].tradition_type).toBe('TRADITION_SCIENCE');
        });

        it('should populate progression tree nodes from loaded data', () => {
            const loadedData = {
                progression_tree_nodes: [
                    { id: 'node1', progression_tree_node_type: 'NODE_TECH' },
                ],
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.progression_tree_nodes).toHaveLength(1);
            expect(state.wizardData.progression_tree_nodes[0].id).toBe('node1');
        });

        it('should populate progression trees from loaded data', () => {
            const loadedData = {
                progression_trees: [
                    { id: 'tree1', progression_tree_type: 'TECH_TREE' },
                ],
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.progression_trees).toHaveLength(1);
            expect(state.wizardData.progression_trees[0].progression_tree_type).toBe(
                'TECH_TREE'
            );
        });

        it('should populate all sections together from complete loaded data', () => {
            const loadedData = {
                metadata: { id: 'babylon', name: 'Babylon' },
                module_localization: { name: 'Babylon Module' },
                action_group: { action_group_id: 'AGE_ANTIQUITY' },
                civilization: { civilization_type: 'CIVILIZATION_BABYLON' },
                units: [{ id: 'unit1', unit_type: 'UNIT_SCOUT' }],
                constructibles: [{ id: 'building1' }],
                modifiers: [{ id: 'mod1' }],
                traditions: [{ id: 'trad1' }],
                progression_tree_nodes: [{ id: 'node1' }],
                progression_trees: [{ id: 'tree1' }],
                constants: { city_names: ['Babylon', 'Nippur'] },
                imports: [{ id: 'icon1' }],
                build: { builders: [] },
            };

            state.populateWizardFromData(loadedData);

            expect(state.wizardData.metadata.id).toBe('babylon');
            expect(state.wizardData.module_localization.name).toBe('Babylon Module');
            expect(state.wizardData.action_group.action_group_id).toBe('AGE_ANTIQUITY');
            expect(state.wizardData.civilization.civilization_type).toBe(
                'CIVILIZATION_BABYLON'
            );
            expect(state.wizardData.units).toHaveLength(1);
            expect(state.wizardData.constructibles).toHaveLength(1);
            expect(state.wizardData.modifiers).toHaveLength(1);
            expect(state.wizardData.traditions).toHaveLength(1);
            expect(state.wizardData.progression_tree_nodes).toHaveLength(1);
            expect(state.wizardData.progression_trees).toHaveLength(1);
            expect(state.wizardData.constants.city_names).toEqual(['Babylon', 'Nippur']);
            expect(state.wizardData.imports).toHaveLength(1);
        });

        it('should handle null/undefined data gracefully', () => {
            state.populateWizardFromData(null);

            expect(state.wizardData.metadata).toEqual({});
            expect(state.wizardData.units).toEqual([]);
            expect(state.wizardData.civilization).toEqual({});
        });

        it('should reset wizard step to 1 when populating', () => {
            state.setWizardStep(5);
            state.populateWizardFromData({
                metadata: { id: 'test' },
            });

            expect(state.wizardStep).toBe(1);
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
