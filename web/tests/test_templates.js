/**
 * Tests for templates.js module
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as templates from '../static/js/templates.js';

describe('Templates Module', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
        vi.clearAllMocks();
    });

    describe('showTemplateModal', () => {
        it('should show template modal by removing hidden class', () => {
            const modal = document.createElement('div');
            modal.id = 'template-modal';
            modal.className = 'hidden';
            document.body.appendChild(modal);
            
            templates.showTemplateModal();
            
            expect(modal.classList.contains('hidden')).toBe(false);
        });

        it('should handle missing modal gracefully', () => {
            expect(() => templates.showTemplateModal()).not.toThrow();
        });
    });

    describe('hideTemplateModal', () => {
        it('should hide template modal by adding hidden class', () => {
            const modal = document.createElement('div');
            modal.id = 'template-modal';
            document.body.appendChild(modal);
            
            templates.hideTemplateModal();
            
            expect(modal.classList.contains('hidden')).toBe(true);
        });

        it('should handle missing modal gracefully', () => {
            expect(() => templates.hideTemplateModal()).not.toThrow();
        });
    });

    describe('loadTemplate', () => {
        it('should fetch template from API', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => ({ id: 'scientific', name: 'Scientific Civ' }),
            });
            global.fetch = mockFetch;
            
            const result = await templates.loadTemplate('scientific');
            
            expect(mockFetch).toHaveBeenCalledWith('/api/template/scientific');
            expect(result).toEqual({ id: 'scientific', name: 'Scientific Civ' });
        });

        it('should hide modal after loading template', async () => {
            const modal = document.createElement('div');
            modal.id = 'template-modal';
            document.body.appendChild(modal);
            
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => ({}),
            });
            global.fetch = mockFetch;
            
            await templates.loadTemplate('scientific');
            
            expect(modal.classList.contains('hidden')).toBe(true);
        });

        it('should throw error when fetch fails', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Not Found',
            });
            global.fetch = mockFetch;
            
            await expect(templates.loadTemplate('invalid')).rejects.toThrow();
        });

        it('should throw error on network failure', async () => {
            const mockFetch = vi.fn().mockRejectedValue(new Error('Network error'));
            global.fetch = mockFetch;
            
            await expect(templates.loadTemplate('scientific')).rejects.toThrow();
        });

        it('should log error on failure', async () => {
            const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
            const mockFetch = vi.fn().mockRejectedValue(new Error('Test error'));
            global.fetch = mockFetch;
            
            try {
                await templates.loadTemplate('scientific');
            } catch (e) {
                // Expected
            }
            
            expect(consoleSpy).toHaveBeenCalled();
            consoleSpy.mockRestore();
        });
    });

    describe('getAvailableTemplates', () => {
        it('should return array of templates', async () => {
            const templates_list = await templates.getAvailableTemplates();
            
            expect(Array.isArray(templates_list)).toBe(true);
            expect(templates_list.length).toBeGreaterThan(0);
        });

        it('should include blank template', async () => {
            const templates_list = await templates.getAvailableTemplates();
            const blank = templates_list.find(t => t.name === 'blank');
            
            expect(blank).toBeTruthy();
            expect(blank.label).toBe('Blank Mod');
        });

        it('should include scientific template', async () => {
            const templates_list = await templates.getAvailableTemplates();
            const scientific = templates_list.find(t => t.name === 'scientific');
            
            expect(scientific).toBeTruthy();
            expect(scientific.label).toBe('Scientific Civilization');
        });

        it('should include military template', async () => {
            const templates_list = await templates.getAvailableTemplates();
            const military = templates_list.find(t => t.name === 'military');
            
            expect(military).toBeTruthy();
        });

        it('should include cultural template', async () => {
            const templates_list = await templates.getAvailableTemplates();
            const cultural = templates_list.find(t => t.name === 'cultural');
            
            expect(cultural).toBeTruthy();
        });

        it('should include economic template', async () => {
            const templates_list = await templates.getAvailableTemplates();
            const economic = templates_list.find(t => t.name === 'economic');
            
            expect(economic).toBeTruthy();
        });

        it('should have required properties for each template', async () => {
            const templates_list = await templates.getAvailableTemplates();
            
            templates_list.forEach(template => {
                expect(template).toHaveProperty('name');
                expect(template).toHaveProperty('label');
                expect(template).toHaveProperty('description');
                expect(typeof template.name).toBe('string');
                expect(typeof template.label).toBe('string');
                expect(typeof template.description).toBe('string');
            });
        });
    });
});
