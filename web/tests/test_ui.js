/**
 * Tests for ui.js module
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as ui from '../static/js/ui.js';

describe('UI Module', () => {
    beforeEach(() => {
        // Clean up DOM before each test
        document.body.innerHTML = '';
    });

    describe('showToast', () => {
        it('should create and display toast notification', () => {
            ui.showToast('Test message', 'info');
            
            const toast = document.querySelector('[class*="animate-fade-in"]');
            expect(toast).toBeTruthy();
            expect(toast.textContent).toContain('Test message');
        });

        it('should apply correct background class for info type', () => {
            ui.showToast('Info message', 'info');
            
            const toast = document.querySelector('[class*="animate-fade-in"]');
            expect(toast.className).toContain('bg-blue-600');
        });

        it('should apply correct background class for success type', () => {
            ui.showToast('Success message', 'success');
            
            const toast = document.querySelector('[class*="animate-fade-in"]');
            expect(toast.className).toContain('bg-green-600');
        });

        it('should apply correct background class for error type', () => {
            ui.showToast('Error message', 'error');
            
            const toast = document.querySelector('[class*="animate-fade-in"]');
            expect(toast.className).toContain('bg-red-600');
        });

        it('should default to info type when not specified', () => {
            ui.showToast('Default message');
            
            const toast = document.querySelector('[class*="animate-fade-in"]');
            expect(toast.className).toContain('bg-blue-600');
        });

        it('should create toast container if it does not exist', () => {
            ui.showToast('Test');
            
            const container = document.getElementById('toast-container');
            expect(container).toBeTruthy();
        });

        it('should reuse existing toast container', () => {
            ui.showToast('First');
            const container1 = document.getElementById('toast-container');
            
            ui.showToast('Second');
            const container2 = document.getElementById('toast-container');
            
            expect(container1).toBe(container2);
        });
    });

    describe('showLoading', () => {
        it('should show loading spinner in editor container', () => {
            const editor = document.createElement('div');
            editor.id = 'editor-container';
            document.body.appendChild(editor);
            
            ui.showLoading();
            
            const spinner = editor.querySelector('.animate-spin');
            expect(spinner).toBeTruthy();
        });

        it('should handle missing editor container gracefully', () => {
            expect(() => ui.showLoading()).not.toThrow();
        });

        it('should display loading text', () => {
            const editor = document.createElement('div');
            editor.id = 'editor-container';
            document.body.appendChild(editor);
            
            ui.showLoading();
            
            expect(editor.textContent).toContain('Loading...');
        });
    });

    describe('updateDirtyIndicator', () => {
        it('should show dirty indicator when isDirty is true', () => {
            const indicator = document.createElement('div');
            indicator.id = 'dirty-indicator';
            indicator.className = 'hidden';
            document.body.appendChild(indicator);
            
            ui.updateDirtyIndicator(true);
            
            expect(indicator.classList.contains('hidden')).toBe(false);
        });

        it('should hide dirty indicator when isDirty is false', () => {
            const indicator = document.createElement('div');
            indicator.id = 'dirty-indicator';
            document.body.appendChild(indicator);
            
            ui.updateDirtyIndicator(false);
            
            expect(indicator.classList.contains('hidden')).toBe(true);
        });

        it('should enable save button when isDirty is true', () => {
            const saveBtn = document.createElement('button');
            saveBtn.id = 'save-btn';
            saveBtn.disabled = true;
            document.body.appendChild(saveBtn);
            
            ui.updateDirtyIndicator(true);
            
            expect(saveBtn.disabled).toBe(false);
        });

        it('should disable save button when isDirty is false', () => {
            const saveBtn = document.createElement('button');
            saveBtn.id = 'save-btn';
            saveBtn.disabled = false;
            document.body.appendChild(saveBtn);
            
            ui.updateDirtyIndicator(false);
            
            expect(saveBtn.disabled).toBe(true);
        });

        it('should handle missing elements gracefully', () => {
            expect(() => ui.updateDirtyIndicator(true)).not.toThrow();
        });
    });

    describe('showFieldError', () => {
        it('should add error styling to wrapper', () => {
            const wrapper = document.createElement('div');
            wrapper.className = 'border border-slate-600';
            document.body.appendChild(wrapper);
            
            ui.showFieldError(wrapper, 'This field is required');
            
            expect(wrapper.classList.contains('border-red-600')).toBe(true);
            expect(wrapper.classList.contains('bg-red-900/20')).toBe(true);
        });

        it('should add error message to wrapper', () => {
            const wrapper = document.createElement('div');
            document.body.appendChild(wrapper);
            
            ui.showFieldError(wrapper, 'This field is required');
            
            const error = wrapper.querySelector('.field-error');
            expect(error).toBeTruthy();
            expect(error.textContent).toBe('This field is required');
        });

        it('should remove existing error before adding new one', () => {
            const wrapper = document.createElement('div');
            document.body.appendChild(wrapper);
            
            ui.showFieldError(wrapper, 'First error');
            ui.showFieldError(wrapper, 'Second error');
            
            const errors = wrapper.querySelectorAll('.field-error');
            expect(errors).toHaveLength(1);
            expect(errors[0].textContent).toBe('Second error');
        });

        it('should handle null wrapper gracefully', () => {
            expect(() => ui.showFieldError(null, 'Error')).not.toThrow();
        });
    });

    describe('clearFieldError', () => {
        it('should remove error styling from wrapper', () => {
            const wrapper = document.createElement('div');
            wrapper.className = 'border-red-600 bg-red-900/20';
            document.body.appendChild(wrapper);
            
            ui.clearFieldError(wrapper);
            
            expect(wrapper.classList.contains('border-red-600')).toBe(false);
            expect(wrapper.classList.contains('bg-red-900/20')).toBe(false);
        });

        it('should remove error message element', () => {
            const wrapper = document.createElement('div');
            const error = document.createElement('p');
            error.className = 'field-error';
            error.textContent = 'Error message';
            wrapper.appendChild(error);
            document.body.appendChild(wrapper);
            
            ui.clearFieldError(wrapper);
            
            expect(wrapper.querySelector('.field-error')).toBeFalsy();
        });

        it('should handle missing error element gracefully', () => {
            const wrapper = document.createElement('div');
            document.body.appendChild(wrapper);
            
            expect(() => ui.clearFieldError(wrapper)).not.toThrow();
        });

        it('should handle null wrapper gracefully', () => {
            expect(() => ui.clearFieldError(null)).not.toThrow();
        });
    });
});
