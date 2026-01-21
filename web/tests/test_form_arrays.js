/**
 * Tests for form arrays module
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import * as arrays from '../static/js/form/arrays.js';

describe('Form Arrays Module', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
        vi.clearAllMocks();
    });

    describe('addArrayItem', () => {
        it('should add new item to array', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            document.body.appendChild(container);

            arrays.addArrayItem('cities');

            expect(container.children).toHaveLength(1);
        });

        it('should create input field for new item', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            document.body.appendChild(container);

            arrays.addArrayItem('cities');

            const input = container.querySelector('input');
            expect(input).toBeTruthy();
            expect(input.placeholder).toBe('New item');
        });

        it('should handle missing container gracefully', () => {
            expect(() => arrays.addArrayItem('nonexistent')).not.toThrow();
        });
    });

    describe('removeArrayItem', () => {
        it('should remove item at index', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            container.innerHTML = `
                <div><input data-array-item="0" value="Rome" /></div>
                <div><input data-array-item="1" value="Athens" /></div>
            `;
            document.body.appendChild(container);

            arrays.removeArrayItem('cities', 0);

            expect(container.children).toHaveLength(1);
        });

        it('should handle missing index gracefully', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            document.body.appendChild(container);

            expect(() => arrays.removeArrayItem('cities', 0)).not.toThrow();
        });
    });

    describe('getArrayFieldValues', () => {
        it('should return array of values', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            container.innerHTML = `
                <div><input data-array-item="0" value="Rome" /></div>
                <div><input data-array-item="1" value="Athens" /></div>
            `;
            document.body.appendChild(container);

            const values = arrays.getArrayFieldValues('cities');

            expect(values).toEqual(['Rome', 'Athens']);
        });

        it('should filter empty values', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            container.innerHTML = `
                <div><input data-array-item="0" value="Rome" /></div>
                <div><input data-array-item="1" value="   " /></div>
                <div><input data-array-item="2" value="Athens" /></div>
            `;
            document.body.appendChild(container);

            const values = arrays.getArrayFieldValues('cities');

            expect(values).toEqual(['Rome', 'Athens']);
        });

        it('should return empty array if container missing', () => {
            const values = arrays.getArrayFieldValues('nonexistent');
            expect(values).toEqual([]);
        });
    });

    describe('rerenderArrayField', () => {
        it('should rerender array items', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            document.body.appendChild(container);

            arrays.rerenderArrayField('cities', ['Rome', 'Athens', 'Sparta']);

            const inputs = container.querySelectorAll('[data-array-item]');
            expect(inputs).toHaveLength(3);
            expect(inputs[0].value).toBe('Rome');
            expect(inputs[2].value).toBe('Sparta');
        });

        it('should clear previous items', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            container.innerHTML = '<div><input data-array-item="0" value="Old" /></div>';
            document.body.appendChild(container);

            arrays.rerenderArrayField('cities', ['New']);

            expect(container.querySelectorAll('[data-array-item]')).toHaveLength(1);
            expect(container.querySelector('input').value).toBe('New');
        });

        it('should handle empty array', () => {
            const container = document.createElement('div');
            container.id = 'array-container-cities';
            document.body.appendChild(container);

            arrays.rerenderArrayField('cities', []);

            expect(container.innerHTML).toBe('');
        });
    });
});
