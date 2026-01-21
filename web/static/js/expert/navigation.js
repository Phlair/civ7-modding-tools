/**
 * Expert Mode Navigation - Scroll spy and section switching
 * Handles navigation between editor sections
 */

/**
 * Setup scroll spy to highlight active section
 * Updates sidebar navigation as user scrolls
 */
export function setupScrollSpy() {
    const mainContent = document.querySelector('main');
    if (!mainContent) return;

    let scrollTimeout;

    mainContent.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const sections = document.querySelectorAll('[data-section-id]');

            sections.forEach(section => {
                const sectionId = section.getAttribute('data-section-id');
                const navLink = document.querySelector(`[data-nav="${sectionId}"]`);

                if (!navLink) return;

                const rect = section.getBoundingClientRect();
                const isVisible = rect.top < 100 && rect.bottom > 100;

                if (isVisible) {
                    document.querySelectorAll('[data-nav]').forEach(link => {
                        link.classList.remove('bg-blue-600/20', 'border-blue-400', 'text-blue-300');
                        link.classList.add('text-slate-300');
                    });
                    navLink.classList.add('bg-blue-600/20', 'border-blue-400', 'text-blue-300');
                    navLink.classList.remove('text-slate-300');
                }
            });
        }, 100);
    });
}

/**
 * Switch to a section and scroll it into view
 * @param {string} sectionId - Section ID to navigate to
 */
export function switchToSection(sectionId) {
    const section = document.querySelector(`[data-section-id="${sectionId}"]`);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Get all available sections
 * @returns {Array} List of section metadata
 */
export function getAvailableSections() {
    return [
        { id: 'metadata', title: 'Metadata', color: 'blue' },
        { id: 'module_localization', title: 'Module Localization', color: 'purple' },
        { id: 'action_group', title: 'Action Group', color: 'green' },
        { id: 'constants', title: 'Constants', color: 'indigo' },
        { id: 'imports', title: 'Imports', color: 'cyan' },
        { id: 'civilization', title: 'Civilization', color: 'red' },
        { id: 'modifiers', title: 'Modifiers', color: 'orange' },
        { id: 'traditions', title: 'Traditions', color: 'amber' },
        { id: 'units', title: 'Units', color: 'yellow' },
        { id: 'constructibles', title: 'Constructibles', color: 'lime' },
        { id: 'progression_tree_nodes', title: 'Progression Tree Nodes', color: 'emerald' },
        { id: 'progression_trees', title: 'Progression Trees', color: 'teal' },
        { id: 'build', title: 'Build Configuration', color: 'sky' },
    ];
}
