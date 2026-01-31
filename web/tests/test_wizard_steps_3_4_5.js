/**
 * Tests for wizard steps 3, 4, and 5
 * Step 3: Units & Buildings
 * Step 4: Modifiers & Traditions
 * Step 5: Review & Finish
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as step3 from '../static/js/wizard/step3.js';
import * as step4 from '../static/js/wizard/step4.js';
import * as step5 from '../static/js/wizard/step5.js';
import * as state from '../static/js/state.js';
import * as ui from '../static/js/ui.js';
import * as wizard from '../static/js/wizard/wizard.js';

// Mock toast functionality
vi.mock('../static/js/ui.js', () => ({
    showToast: vi.fn(),
    updateDirtyIndicator: vi.fn(),
}));

// Mock wizard dropdown and validation
vi.mock('../static/js/wizard/wizard.js', () => ({
    createWizardDropdown: vi.fn((id, type, value, placeholder) => {
        const elem = document.getElementById(id);
        if (elem) {
            elem.innerHTML = `<option value="${value || ''}">${value || placeholder}</option>`;
        }
    }),
    validateWizardData: vi.fn(() => []),
    showFieldHelp: vi.fn(),
}));

describe('Wizard Step 3 - Units & Buildings', () => {
    let container;

    beforeEach(() => {
        state.clearAllState();
        container = document.createElement('div');
        document.body.appendChild(container);
        state.wizardData.units = [];
        state.wizardData.constructibles = [];
        state.wizardBuildingYields.length = 0;
    });

    afterEach(() => {
        container.remove();
        vi.clearAllMocks();
    });

    describe('renderWizardStep3', () => {
        it('should render step 3 header', () => {
            step3.renderWizardStep3(container);
            expect(container.textContent).toContain('Step 3: Units & Buildings');
            expect(container.textContent).toContain('⚔️');
        });

        it('should show add unit button', () => {
            step3.renderWizardStep3(container);
            const addUnitBtn = container.querySelector('button');
            expect(addUnitBtn).toBeDefined();
            expect(addUnitBtn.textContent).toContain('+ Add Unit');
        });

        it('should show units count', () => {
            state.wizardData.units = [{ id: 'UNIT_TEST' }];
            step3.renderWizardStep3(container);
            expect(container.textContent).toContain('Unique Units (1)');
        });

        it('should show constructibles count', () => {
            state.wizardData.constructibles = [{ id: 'BUILDING_TEST' }];
            step3.renderWizardStep3(container);
            expect(container.textContent).toContain('Unique Buildings (1)');
        });

        it('should render no units message when empty', () => {
            step3.renderWizardStep3(container);
            expect(container.textContent).toContain('No units added yet');
        });
    });

    describe('Unit form management', () => {
        beforeEach(() => {
            step3.renderWizardStep3(container);
        });

        it('should show unit form when add button clicked', () => {
            step3.wizardShowUnitForm();
            const form = document.getElementById('wizard-unit-form');
            expect(form).toBeDefined();
            expect(form.classList.contains('hidden')).toBe(false);
        });

        it('should populate form fields when editing unit', () => {
            state.wizardData.units = [{
                id: 'UNIT_TEST',
                unit_type: 'UNIT_WARRIOR',
                unit: { base_moves: 2, base_sight_range: 3 },
            }];
            step3.wizardEditUnit(0);
            expect(document.getElementById('wizard-unit-id').value).toBe('UNIT_TEST');
            expect(document.getElementById('wizard-unit-type').value).toBe('UNIT_WARRIOR');
            expect(document.getElementById('wizard-unit-moves').value).toBe('2');
        });

        it('should clear form on cancel', () => {
            document.body.innerHTML += `
                <div id="wizard-unit-form">
                    <input id="wizard-unit-id" value="TEST" />
                    <input id="wizard-unit-type" />
                </div>
                <input id="wizard-unit-edit-idx" />
            `;
            step3.wizardCancelUnitForm();
            expect(document.getElementById('wizard-unit-id').value).toBe('');
            expect(document.getElementById('wizard-unit-type').value).toBe('');
            expect(document.getElementById('wizard-unit-edit-idx').value).toBe('-1');
        });
    });

    describe('Unit CRUD operations', () => {
        beforeEach(() => {
            document.body.innerHTML = `
                <div id="wizard-unit-form" class="hidden">
                    <input id="wizard-unit-id" placeholder="Unit ID" />
                    <input id="wizard-unit-type" placeholder="Unit Type" />
                    <input id="wizard-unit-moves" />
                    <input id="wizard-unit-sight" />
                    <input id="wizard-unit-name" />
                    <textarea id="wizard-unit-desc"></textarea>
                    <input id="wizard-unit-icon" />
                    <select id="wizard-unit-cost-yield"></select>
                    <input id="wizard-unit-cost" />
                    <select id="wizard-unit-core-class"></select>
                    <select id="wizard-unit-domain"></select>
                    <select id="wizard-unit-formation"></select>
                    <select id="wizard-unit-movement"></select>
                    <input id="wizard-unit-combat" />
                    <input id="wizard-unit-ranged-combat" />
                    <input id="wizard-unit-range" />
                    <input id="wizard-unit-replaces" />
                    <input id="wizard-unit-edit-idx" value="-1" />
                </div>
                <div id="wizard-step-content"></div>
            `;
        });

        it('should save new unit', () => {
            document.getElementById('wizard-unit-id').value = 'UNIT_NEW';
            document.getElementById('wizard-unit-type').value = 'WARRIOR_TYPE';
            step3.wizardSaveUnit();
            expect(state.wizardData.units.length).toBe(1);
            expect(state.wizardData.units[0].id).toBe('UNIT_NEW');
            expect(ui.showToast).toHaveBeenCalledWith('Unit added', 'success');
        });

        it('should require unit ID', () => {
            document.getElementById('wizard-unit-type').value = 'WARRIOR_TYPE';
            step3.wizardSaveUnit();
            expect(ui.showToast).toHaveBeenCalledWith('Unit ID is required', 'error');
        });

        it('should require unit type', () => {
            document.getElementById('wizard-unit-id').value = 'UNIT_NEW';
            step3.wizardSaveUnit();
            expect(ui.showToast).toHaveBeenCalledWith('Unit Type is required', 'error');
        });

        it('should save unit with optional fields', () => {
            document.getElementById('wizard-unit-id').value = 'UNIT_FULL';
            document.getElementById('wizard-unit-type').value = 'WARRIOR_TYPE';
            document.getElementById('wizard-unit-moves').value = '3';
            document.getElementById('wizard-unit-sight').value = '4';
            document.getElementById('wizard-unit-name').value = 'My Unit';
            document.getElementById('wizard-unit-desc').value = 'Unit description';
            step3.wizardSaveUnit();
            const unit = state.wizardData.units[0];
            expect(unit.unit.base_moves).toBe(3);
            expect(unit.unit.base_sight_range).toBe(4);
            expect(unit.localizations[0].name).toBe('My Unit');
        });

        it('should update existing unit', () => {
            state.wizardData.units = [{ id: 'UNIT_OLD', unit_type: 'OLD_TYPE' }];
            document.getElementById('wizard-unit-edit-idx').value = '0';
            document.getElementById('wizard-unit-id').value = 'UNIT_UPDATED';
            document.getElementById('wizard-unit-type').value = 'NEW_TYPE';
            step3.wizardSaveUnit();
            expect(state.wizardData.units[0].id).toBe('UNIT_UPDATED');
            expect(ui.showToast).toHaveBeenCalledWith('Unit updated', 'success');
        });

        it('should remove unit', () => {
            state.wizardData.units = [
                { id: 'UNIT_1' },
                { id: 'UNIT_2' },
            ];
            step3.removeWizardUnit(0);
            expect(state.wizardData.units.length).toBe(1);
            expect(state.wizardData.units[0].id).toBe('UNIT_2');
            expect(ui.showToast).toHaveBeenCalledWith('Unit removed', 'info');
        });

        it('should save combat stats', () => {
            document.getElementById('wizard-unit-id').value = 'UNIT_COMBAT';
            document.getElementById('wizard-unit-type').value = 'WARRIOR';
            document.getElementById('wizard-unit-combat').value = '15';
            document.getElementById('wizard-unit-ranged-combat').value = '0';
            document.getElementById('wizard-unit-range').value = '0';
            step3.wizardSaveUnit();
            const unit = state.wizardData.units[0];
            expect(unit.unit_stat.combat).toBe(15);
        });
    });

    describe('Building CRUD operations', () => {
        beforeEach(() => {
            document.body.innerHTML = `
                <div id="wizard-constructible-form" class="hidden">
                    <input id="wizard-constructible-id" />
                    <input id="wizard-constructible-type" />
                    <input id="wizard-constructible-name" />
                    <textarea id="wizard-constructible-desc"></textarea>
                    <input id="wizard-constructible-icon" />
                    <input id="wizard-constructible-districts" />
                    <input id="wizard-constructible-edit-idx" value="-1" />
                </div>
                <div id="wizard-building-yields"></div>
                <div id="wizard-step-content"></div>
            `;
        });

        it('should save new building', () => {
            document.getElementById('wizard-constructible-id').value = 'BUILDING_NEW';
            document.getElementById('wizard-constructible-type').value = 'BUILDING_TYPE';
            step3.wizardSaveConstructible();
            expect(state.wizardData.constructibles.length).toBe(1);
            expect(state.wizardData.constructibles[0].id).toBe('BUILDING_NEW');
            expect(ui.showToast).toHaveBeenCalledWith('Building added', 'success');
        });

        it('should require building ID', () => {
            document.getElementById('wizard-constructible-type').value = 'BUILDING_TYPE';
            step3.wizardSaveConstructible();
            expect(ui.showToast).toHaveBeenCalledWith('Building ID is required', 'error');
        });

        it('should save building with districts', () => {
            document.getElementById('wizard-constructible-id').value = 'BUILDING_WITH_DISTRICTS';
            document.getElementById('wizard-constructible-type').value = 'BUILDING_TYPE';
            document.getElementById('wizard-constructible-districts').value = 'DISTRICT_CAMPUS, DISTRICT_HOLY_SITE';
            step3.wizardSaveConstructible();
            const building = state.wizardData.constructibles[0];
            expect(building.constructible_valid_districts.length).toBe(2);
            expect(building.constructible_valid_districts[0]).toBe('DISTRICT_CAMPUS');
        });

        it('should remove building', () => {
            state.wizardData.constructibles = [
                { id: 'BUILDING_1' },
                { id: 'BUILDING_2' },
            ];
            step3.removeWizardConstructible(0);
            expect(state.wizardData.constructibles.length).toBe(1);
        });
    });

describe('Building yields management', () => {
        beforeEach(() => {
            document.body.innerHTML = '<div id="wizard-building-yields"></div>';
        });

        it('should add building yield', () => {
            step3.addWizardBuildingYield();
            expect(state.wizardBuildingYields.length).toBe(1);
            expect(state.wizardBuildingYields[0]).toEqual({ yield_type: '', yield_change: 0 });
        });

        it('should update building yield', () => {
            step3.addWizardBuildingYield();
            step3.updateWizardBuildingYield(0, 'yield_type', 'YIELD_SCIENCE');
            expect(state.wizardBuildingYields[0].yield_type).toBe('YIELD_SCIENCE');
        });

        it('should remove building yield', () => {
            step3.addWizardBuildingYield();
            step3.addWizardBuildingYield();
            expect(state.wizardBuildingYields.length).toBe(2);
            step3.removeWizardBuildingYield(0);
            expect(state.wizardBuildingYields.length).toBe(1);
        });
    });
});

describe('Wizard Step 4 - Modifiers & Traditions', () => {
    let container;

    beforeEach(() => {
        state.clearAllState();
        container = document.createElement('div');
        document.body.appendChild(container);
        state.wizardData.modifiers = [];
        state.wizardData.traditions = [];
    });

    afterEach(() => {
        container.remove();
        vi.clearAllMocks();
    });

    describe('renderWizardStep4', () => {
        it('should render step 4 header', () => {
            step4.renderWizardStep4(container);
            expect(container.textContent).toContain('Step 4: Advanced Features');
            expect(container.textContent).toContain('✨');
        });

        it('should show modifiers count', () => {
            state.wizardData.modifiers = [{ id: 'MOD_TEST' }];
            step4.renderWizardStep4(container);
            expect(container.textContent).toContain('Game Modifiers (1)');
        });

        it('should show traditions count', () => {
            state.wizardData.traditions = [{ id: 'TRAD_TEST' }];
            step4.renderWizardStep4(container);
            expect(container.textContent).toContain('Cultural Traditions (1)');
        });

        it('should show add modifier button', () => {
            step4.renderWizardStep4(container);
            const buttons = container.querySelectorAll('button');
            const addModBtn = Array.from(buttons).find(b => b.textContent.includes('+ Add Modifier'));
            expect(addModBtn).toBeDefined();
        });
    });

    describe('Modifier CRUD operations', () => {
        beforeEach(() => {
            document.body.innerHTML = `
                <div id="wizard-step-content"></div>
                <div id="wizard-modifier-form" class="hidden">
                    <input id="wizard-modifier-id" />
                    <input id="wizard-modifier-type" />
                    <select id="wizard-modifier-effect">
                        <option value="ADJUST_YIELD">ADJUST_YIELD</option>
                        <option value="NEW_EFFECT">NEW_EFFECT</option>
                    </select>
                    <select id="wizard-modifier-collection">
                        <option value="ALL_CITIES">ALL_CITIES</option>
                    </select>
                    <input id="wizard-modifier-permanent" type="checkbox" />
                    <input id="wizard-modifier-runonce" type="checkbox" />
                    <textarea id="wizard-modifier-desc"></textarea>
                    <textarea id="wizard-modifier-args"></textarea>
                    <input id="wizard-modifier-edit-idx" value="-1" />
                </div>
            `;
        });

        it('should save new modifier', () => {
            state.wizardData.modifiers = [];
            document.getElementById('wizard-modifier-id').value = 'MOD_NEW';
            document.getElementById('wizard-modifier-effect').value = 'ADJUST_YIELD';
            document.getElementById('wizard-modifier-collection').value = 'ALL_CITIES';
            step4.wizardSaveModifier();
            expect(state.wizardData.modifiers.length).toBe(1);
            expect(state.wizardData.modifiers[0].id).toBe('MOD_NEW');
            expect(ui.showToast).toHaveBeenCalledWith('Modifier added', 'success');
        });

        it('should require modifier ID', () => {
            state.wizardData.modifiers = [];
            document.getElementById('wizard-modifier-effect').value = 'ADJUST_YIELD';
            document.getElementById('wizard-modifier-collection').value = 'ALL_CITIES';
            step4.wizardSaveModifier();
            expect(ui.showToast).toHaveBeenCalledWith('Modifier ID is required', 'error');
        });

        it('should require effect', () => {
            state.wizardData.modifiers = [];
            document.getElementById('wizard-modifier-id').value = 'MOD_NEW';
            document.getElementById('wizard-modifier-collection').value = 'ALL_CITIES';
            // Don't set effect, leave it empty
            document.getElementById('wizard-modifier-effect').value = '';
            step4.wizardSaveModifier();
            expect(ui.showToast).toHaveBeenCalledWith('Effect is required', 'error');
        });

        it('should require collection', () => {
            state.wizardData.modifiers = [];
            document.getElementById('wizard-modifier-id').value = 'MOD_NEW';
            document.getElementById('wizard-modifier-effect').value = 'ADJUST_YIELD';
            // Don't set collection, leave it empty
            document.getElementById('wizard-modifier-collection').value = '';
            step4.wizardSaveModifier();
            expect(ui.showToast).toHaveBeenCalledWith('Collection is required', 'error');
        });

        it('should save modifier with boolean flags', () => {
            state.wizardData.modifiers = [];
            document.getElementById('wizard-modifier-id').value = 'MOD_FLAGS';
            document.getElementById('wizard-modifier-effect').value = 'ADJUST_YIELD';
            document.getElementById('wizard-modifier-collection').value = 'ALL_CITIES';
            document.getElementById('wizard-modifier-permanent').checked = true;
            document.getElementById('wizard-modifier-runonce').checked = true;
            step4.wizardSaveModifier();
            // Verify the modifier was added
            expect(state.wizardData.modifiers.length).toBeGreaterThan(0);
            const mod = state.wizardData.modifiers[state.wizardData.modifiers.length - 1];
            expect(mod.modifier.permanent).toBe(true);
            expect(mod.modifier.run_once).toBe(true);
        });

        it('should parse modifier arguments', () => {
            state.wizardData.modifiers = [];
            document.getElementById('wizard-modifier-id').value = 'MOD_ARGS';
            document.getElementById('wizard-modifier-effect').value = 'ADJUST_YIELD';
            document.getElementById('wizard-modifier-collection').value = 'ALL_CITIES';
            document.getElementById('wizard-modifier-args').value = 'YieldType:YIELD_SCIENCE\nAmount:100';
            step4.wizardSaveModifier();
            expect(state.wizardData.modifiers.length).toBeGreaterThan(0);
            const mod = state.wizardData.modifiers[state.wizardData.modifiers.length - 1];
            expect(mod.modifier.arguments.length).toBe(2);
            expect(mod.modifier.arguments[0].name).toBe('YieldType');
            expect(mod.modifier.arguments[0].value).toBe('YIELD_SCIENCE');
        });

        it('should update modifier', () => {
            state.wizardData.modifiers = [{
                id: 'MOD_OLD',
                modifier: { effect: 'OLD_EFFECT', collection: 'ALL_CITIES' },
            }];
            document.getElementById('wizard-modifier-edit-idx').value = '0';
            document.getElementById('wizard-modifier-id').value = 'MOD_UPDATED';
            document.getElementById('wizard-modifier-effect').value = 'NEW_EFFECT';
            document.getElementById('wizard-modifier-collection').value = 'ALL_CITIES';
            step4.wizardSaveModifier();
            expect(state.wizardData.modifiers[0].id).toBe('MOD_UPDATED');
            expect(ui.showToast).toHaveBeenCalledWith('Modifier updated', 'success');
        });

        it('should remove modifier', () => {
            state.wizardData.modifiers = [
                { id: 'MOD_1' },
                { id: 'MOD_2' },
            ];
            step4.removeWizardModifier(0);
            expect(state.wizardData.modifiers.length).toBe(1);
            expect(state.wizardData.modifiers[0].id).toBe('MOD_2');
        });

        it('should populate form when editing', () => {
            // Add requirements container
            document.body.innerHTML += '<div id="wizard-modifier-requirements-container"></div>';
            
            state.wizardData.modifiers = [{
                id: 'MOD_EDIT',
                modifier_type: 'CUSTOM_TYPE',
                modifier: {
                    effect: 'ADJUST_YIELD',
                    collection: 'ALL_CITIES',
                    permanent: true,
                    arguments: [
                        { name: 'YieldType', value: 'YIELD_SCIENCE' },
                    ],
                },
                localizations: [{ description: 'Test description' }],
            }];
            step4.wizardEditModifier(0);
            expect(document.getElementById('wizard-modifier-id').value).toBe('MOD_EDIT');
            expect(document.getElementById('wizard-modifier-type').value).toBe('CUSTOM_TYPE');
            expect(document.getElementById('wizard-modifier-permanent').checked).toBe(true);
            expect(document.getElementById('wizard-modifier-desc').value).toBe('Test description');
        });
    });

    describe('Modifier Requirements', () => {
        beforeEach(() => {
            document.body.innerHTML = `
                <div id="wizard-step-content"></div>
                <div id="wizard-modifier-form" class="hidden">
                    <input id="wizard-modifier-id" />
                    <input id="wizard-modifier-type" />
                    <select id="wizard-modifier-effect">
                        <option value="EFFECT_ADJUST_UNIT_STRENGTH_MODIFIER">EFFECT_ADJUST_UNIT_STRENGTH_MODIFIER</option>
                    </select>
                    <select id="wizard-modifier-collection">
                        <option value="COLLECTION_UNIT_COMBAT">COLLECTION_UNIT_COMBAT</option>
                    </select>
                    <input id="wizard-modifier-permanent" type="checkbox" />
                    <input id="wizard-modifier-runonce" type="checkbox" />
                    <textarea id="wizard-modifier-desc"></textarea>
                    <textarea id="wizard-modifier-args"></textarea>
                    <input id="wizard-modifier-edit-idx" value="-1" />
                    <div id="wizard-modifier-requirements-container"></div>
                </div>
            `;
            
            // Mock the data loader
            vi.mock('../static/js/data/loader.js', () => ({
                loadReferenceData: vi.fn(() => Promise.resolve({
                    values: [
                        { id: 'REQUIREMENT_PLOT_BIOME_TYPE_MATCHES' },
                        { id: 'REQUIREMENT_PLOT_IS_OWNER' },
                        { id: 'REQUIREMENT_UNIT_TAG_MATCHES' },
                    ]
                }))
            }));
        });

        it('should add a requirement', () => {
            const container = document.getElementById('wizard-modifier-requirements-container');
            step4.wizardAddRequirement();
            expect(container.children.length).toBe(1);
            expect(container.querySelector('.wizard-req-type')).toBeTruthy();
        });

        it('should remove a requirement', () => {
            const container = document.getElementById('wizard-modifier-requirements-container');
            step4.wizardAddRequirement();
            step4.wizardAddRequirement();
            expect(container.children.length).toBe(2);
            step4.wizardRemoveRequirement(0);
            expect(container.children.length).toBe(1);
        });

        it('should add requirement argument', () => {
            step4.wizardAddRequirement();
            step4.wizardAddRequirementArg(0);
            const argsContainer = document.querySelector('.wizard-req-args-container[data-req-idx="0"]');
            expect(argsContainer.children.length).toBe(1);
            expect(argsContainer.querySelector('.wizard-req-arg-name')).toBeTruthy();
            expect(argsContainer.querySelector('.wizard-req-arg-value')).toBeTruthy();
        });

        it('should remove requirement argument', () => {
            step4.wizardAddRequirement();
            step4.wizardAddRequirementArg(0);
            step4.wizardAddRequirementArg(0);
            const argsContainer = document.querySelector('.wizard-req-args-container[data-req-idx="0"]');
            expect(argsContainer.children.length).toBe(2);
            step4.wizardRemoveRequirementArg(0, 0);
            expect(argsContainer.children.length).toBe(1);
        });

        it('should save modifier with requirements', () => {
            state.wizardData.modifiers = [];
            
            // Setup form
            document.getElementById('wizard-modifier-id').value = 'MOD_WITH_REQ';
            document.getElementById('wizard-modifier-effect').value = 'EFFECT_ADJUST_UNIT_STRENGTH_MODIFIER';
            document.getElementById('wizard-modifier-collection').value = 'COLLECTION_UNIT_COMBAT';
            document.getElementById('wizard-modifier-args').value = 'Amount:3';
            
            // Manually add requirement to container (simulating what wizardAddRequirement would do)
            const requirementsContainer = document.getElementById('wizard-modifier-requirements-container');
            const reqDiv = document.createElement('div');
            reqDiv.dataset.reqIdx = '0';
            reqDiv.innerHTML = `
                <select class="wizard-req-type">
                    <option value="REQUIREMENT_PLOT_BIOME_TYPE_MATCHES" selected>REQUIREMENT_PLOT_BIOME_TYPE_MATCHES</option>
                </select>
                <div class="wizard-req-args-container" data-req-idx="0">
                    <div data-arg-idx="0">
                        <input class="wizard-req-arg-name" value="BiomeType" />
                        <input class="wizard-req-arg-value" value="BIOME_TUNDRA" />
                    </div>
                </div>
            `;
            requirementsContainer.appendChild(reqDiv);
            
            // Save
            step4.wizardSaveModifier();
            
            // Verify
            expect(state.wizardData.modifiers.length).toBe(1);
            const mod = state.wizardData.modifiers[0];
            expect(mod.id).toBe('MOD_WITH_REQ');
            expect(mod.modifier.requirements).toBeTruthy();
            expect(mod.modifier.requirements.length).toBe(1);
            expect(mod.modifier.requirements[0].type).toBe('REQUIREMENT_PLOT_BIOME_TYPE_MATCHES');
            expect(mod.modifier.requirements[0].arguments).toBeTruthy();
            expect(mod.modifier.requirements[0].arguments.length).toBe(1);
            expect(mod.modifier.requirements[0].arguments[0].name).toBe('BiomeType');
            expect(mod.modifier.requirements[0].arguments[0].value).toBe('BIOME_TUNDRA');
        });

        it('should skip requirements without type', () => {
            state.wizardData.modifiers = [];
            
            document.getElementById('wizard-modifier-id').value = 'MOD_EMPTY_REQ';
            document.getElementById('wizard-modifier-effect').value = 'EFFECT_ADJUST_UNIT_STRENGTH_MODIFIER';
            document.getElementById('wizard-modifier-collection').value = 'COLLECTION_UNIT_COMBAT';
            
            // Add requirement but don't set type
            step4.wizardAddRequirement();
            
            step4.wizardSaveModifier();
            
            const mod = state.wizardData.modifiers[0];
            expect(mod.modifier.requirements).toBeUndefined();
        });

        it('should clear requirements when canceling', () => {
            step4.wizardAddRequirement();
            step4.wizardAddRequirement();
            const container = document.getElementById('wizard-modifier-requirements-container');
            expect(container.children.length).toBe(2);
            
            step4.wizardCancelModifierForm();
            expect(container.innerHTML).toBe('');
        });
    });;

    describe('Tradition CRUD operations', () => {
        beforeEach(() => {
            document.body.innerHTML = `
                <div id="wizard-tradition-form" class="hidden" data-mode="custom">
                    <input id="wizard-tradition-id" />
                    <input id="wizard-tradition-name" />
                    <textarea id="wizard-tradition-desc"></textarea>
                    <select id="wizard-tradition-age"></select>
                    <select id="wizard-tradition-trait"></select>
                    <select id="wizard-tradition-existing-select"></select>
                    <div id="wizard-tradition-existing-preview" class="hidden">
                        <p id="wizard-tradition-existing-desc"></p>
                        <span id="wizard-tradition-existing-mods"></span>
                    </div>
                    <input id="wizard-tradition-edit-idx" value="-1" />
                </div>
                <div id="wizard-step-content"></div>
            `;
        });

        it('should save new custom tradition', async () => {
            // Set form to custom mode
            const form = document.getElementById('wizard-tradition-form');
            form.dataset.mode = 'custom';
            
            document.getElementById('wizard-tradition-id').value = 'TRAD_NEW';
            document.getElementById('wizard-tradition-name').value = 'My Tradition';
            await step4.wizardSaveTradition();
            expect(state.wizardData.traditions.length).toBe(1);
            expect(state.wizardData.traditions[0].id).toBe('TRAD_NEW');
            expect(state.wizardData.traditions[0].is_existing_tradition).toBe(false);
            expect(ui.showToast).toHaveBeenCalledWith('Tradition added', 'success');
        });

        it('should require tradition ID for custom tradition', async () => {
            const form = document.getElementById('wizard-tradition-form');
            form.dataset.mode = 'custom';
            document.getElementById('wizard-tradition-id').value = '';
            document.getElementById('wizard-tradition-name').value = 'Name';
            await step4.wizardSaveTradition();
            expect(ui.showToast).toHaveBeenCalledWith('Tradition ID is required', 'error');
        });

        it('should require tradition name for custom tradition', async () => {
            const form = document.getElementById('wizard-tradition-form');
            form.dataset.mode = 'custom';
            document.getElementById('wizard-tradition-id').value = 'TRAD_NEW';
            document.getElementById('wizard-tradition-name').value = '';
            await step4.wizardSaveTradition();
            expect(ui.showToast).toHaveBeenCalledWith('Tradition name is required', 'error');
        });

        it('should save custom tradition with localization', async () => {
            const form = document.getElementById('wizard-tradition-form');
            form.dataset.mode = 'custom';
            document.getElementById('wizard-tradition-id').value = 'TRAD_WITH_LOC';
            document.getElementById('wizard-tradition-name').value = 'My Tradition';
            document.getElementById('wizard-tradition-desc').value = 'Tradition description';
            await step4.wizardSaveTradition();
            const trad = state.wizardData.traditions[0];
            expect(trad.localizations[0].name).toBe('My Tradition');
            expect(trad.localizations[0].description).toBe('Tradition description');
        });

        it('should remove tradition', () => {
            state.wizardData.traditions = [
                { id: 'TRAD_1' },
                { id: 'TRAD_2' },
            ];
            step4.removeWizardTradition(0);
            expect(state.wizardData.traditions.length).toBe(1);
            expect(state.wizardData.traditions[0].id).toBe('TRAD_2');
        });
    });
});

describe('Wizard Step 5 - Review & Finish', () => {
    let container;

    beforeEach(() => {
        state.clearAllState();
        container = document.createElement('div');
        document.body.appendChild(container);
        
        // Initialize wizard data by directly manipulating the object
        state.wizardData.metadata = { id: 'test-mod', name: 'Test Mod', version: '1.0.0' };
        state.wizardData.action_group = { action_group_id: 'AGE_ANTIQUITY' };
        state.wizardData.civilization = {
            civilization_type: 'CIVILIZATION_TEST',
            localizations: [{ name: 'Test Civ', city_names: ['City1', 'City2'] }],
            civilization_traits: ['TRAIT_MILITARY'],
        };
        state.wizardData.units = [];
        state.wizardData.constructibles = [];
        state.wizardData.modifiers = [];
        state.wizardData.traditions = [];
    });

    afterEach(() => {
        container.remove();
        vi.clearAllMocks();
    });

    describe('renderWizardStep5', () => {
        it('should render step 5 header', () => {
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('Step 5: Review & Finish');
            expect(container.textContent).toContain('🎉');
        });

        it('should display mod information', () => {
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('test-mod');
            expect(container.textContent).toContain('Test Mod');
            expect(container.textContent).toContain('1.0.0');
        });

        it('should display civilization info', () => {
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('CIVILIZATION_TEST');
            expect(container.textContent).toContain('Test Civ');
        });

        it('should show success message when no errors', () => {
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('All required fields completed');
        });

        it('should show validation errors', () => {
            // Mock validateWizardData to return errors
            wizard.validateWizardData.mockReturnValueOnce(['Civilization type is required']);
            
            state.wizardData.civilization.civilization_type = '';
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('Required Fields Missing');
        });

        it('should display content counts', () => {
            state.wizardData.units.push({ id: 'UNIT_1' });
            state.wizardData.units.push({ id: 'UNIT_2' });
            state.wizardData.constructibles.push({ id: 'BUILDING_1' });
            state.wizardData.modifiers.push({ id: 'MOD_1' });
            state.wizardData.traditions.push({ id: 'TRAD_1' });
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('Units:');
            expect(container.textContent).toContain('Buildings:');
            expect(container.textContent).toContain('Modifiers:');
            expect(container.textContent).toContain('Traditions:');
        });

        it('should show next steps guidance', () => {
            step5.renderWizardStep5(container);
            expect(container.textContent).toContain('Next Steps');
            expect(container.textContent).toContain('Expert Mode');
        });
    });
});
