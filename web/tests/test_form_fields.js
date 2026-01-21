/**
 * Tests for form fields module
 */

import { describe, it, expect, beforeEach } from 'vitest';
import * as fields from '../static/js/form/fields.js';

describe('Form Fields Module', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    describe('createTextField', () => {
        it('should create text input field', () => {
            const element = fields.createTextField('mod_name', 'Mod Name', 'My Mod');
            expect(element.tagName).toBe('DIV');
            const input = element.querySelector('input[type="text"]');
            expect(input).toBeTruthy();
            expect(input.value).toBe('My Mod');
            expect(element.textContent).toContain('Mod Name');
        });

        it('should mark field as required', () => {
            const element = fields.createTextField('mod_id', 'Mod ID', '', true);
            const input = element.querySelector('input');
            expect(input.dataset.isRequired).toBe('true');
            expect(element.textContent).toContain('*');
        });

        it('should not mark optional field as required', () => {
            const element = fields.createTextField('description', 'Description', '', false);
            expect(element.textContent).not.toContain('*');
        });

        it('should include field name in data attribute', () => {
            const element = fields.createTextField('test_field', 'Test', '');
            const input = element.querySelector('input');
            expect(input.dataset.fieldName).toBe('test_field');
        });
    });

    describe('createNumberField', () => {
        it('should create number input field', () => {
            const element = fields.createNumberField('level', 'Level', 5);
            const input = element.querySelector('input[type="number"]');
            expect(input).toBeTruthy();
            expect(input.value).toBe('5');
            expect(element.textContent).toContain('Level');
        });

        it('should mark field as required', () => {
            const element = fields.createNumberField('amount', 'Amount', 0, true);
            expect(element.textContent).toContain('*');
        });
    });

    describe('createBooleanField', () => {
        it('should create checkbox field', () => {
            const element = fields.createBooleanField('permanent', 'Permanent', true);
            const input = element.querySelector('input[type="checkbox"]');
            expect(input).toBeTruthy();
            expect(input.checked).toBe(true);
            expect(element.textContent).toContain('Permanent');
        });

        it('should not check unchecked field', () => {
            const element = fields.createBooleanField('temporary', 'Temporary', false);
            const input = element.querySelector('input[type="checkbox"]');
            expect(input.checked).toBe(false);
        });
    });

    describe('createStringArrayField', () => {
        it('should create array field', () => {
            const element = fields.createStringArrayField('cities', 'City Names', ['Rome', 'Athens']);
            expect(element.textContent).toContain('City Names');
            const inputs = element.querySelectorAll('input[type="text"]');
            expect(inputs[0].value).toBe('Rome');
            expect(inputs[1].value).toBe('Athens');
        });

        it('should include add button', () => {
            const element = fields.createStringArrayField('tags', 'Tags', []);
            const addBtn = element.querySelector('button');
            expect(addBtn.textContent).toContain('Add Item');
        });

        it('should include remove buttons for each item', () => {
            const element = fields.createStringArrayField('cities', 'Cities', ['Rome', 'Athens']);
            const removeButtons = element.querySelectorAll('button');
            // Should have 2 remove buttons + 1 add button = 3 total
            expect(removeButtons.length).toBeGreaterThanOrEqual(2);
        });
    });

    describe('createAutocompleteField', () => {
        it('should create autocomplete field', () => {
            const element = fields.createAutocompleteField('yield_type', 'Yield Type', 'PRODUCTION');
            expect(element.textContent).toContain('Yield Type');
            const input = element.querySelector('input[type="text"]');
            expect(input.value).toBe('PRODUCTION');
        });

        it('should mark as required', () => {
            const element = fields.createAutocompleteField('effect', 'Effect', '', true);
            expect(element.textContent).toContain('*');
        });

        it('should include dropdown div', () => {
            const element = fields.createAutocompleteField('tags', 'Tags', '');
            // Dropdown is absolute positioned div with specific styles
            const divs = element.querySelectorAll('div');
            expect(divs.length).toBeGreaterThan(1); // Has wrapper + dropdown divs
        });
    });

    describe('recordFieldUsage', () => {
        it('should track field usage', () => {
            expect(() => {
                fields.recordFieldUsage('yield_type', 'PRODUCTION');
            }).not.toThrow();
        });
    });
});
