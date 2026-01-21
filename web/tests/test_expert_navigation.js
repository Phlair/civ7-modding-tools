/**
 * Tests for expert mode navigation
 */

import { describe, it, expect, beforeEach } from 'vitest';
import * as nav from '../static/js/expert/navigation.js';

describe('Expert Navigation Module', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
    });

    describe('getAvailableSections', () => {
        it('should return all 13 sections', () => {
            const sections = nav.getAvailableSections();
            expect(sections).toHaveLength(13);
        });

        it('should include metadata section', () => {
            const sections = nav.getAvailableSections();
            const metadata = sections.find(s => s.id === 'metadata');
            expect(metadata).toBeDefined();
            expect(metadata.title).toBe('Metadata');
        });

        it('should include civilization section', () => {
            const sections = nav.getAvailableSections();
            const civ = sections.find(s => s.id === 'civilization');
            expect(civ).toBeDefined();
        });

        it('should have color for each section', () => {
            const sections = nav.getAvailableSections();
            sections.forEach(section => {
                expect(section).toHaveProperty('color');
                expect(typeof section.color).toBe('string');
            });
        });
    });

    describe('switchToSection', () => {
        it('should find and scroll to section', () => {
            const section = document.createElement('section');
            section.setAttribute('data-section-id', 'metadata');
            section.scrollIntoView = vi.fn();
            document.body.appendChild(section);

            nav.switchToSection('metadata');

            expect(section.scrollIntoView).toHaveBeenCalledWith({
                behavior: 'smooth',
                block: 'start',
            });
        });

        it('should handle missing section gracefully', () => {
            expect(() => nav.switchToSection('nonexistent')).not.toThrow();
        });
    });
});
