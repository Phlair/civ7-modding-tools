/**
 * Data Module - Reference Data Loader
 * Handles loading and caching of reference data from the API
 */

import { getCachedReferenceData, setCachedReferenceData } from '../state.js';

/**
 * Load available reference data types
 * @returns {Promise<void>}
 */
export async function loadReferenceData() {
    try {
        const response = await fetch("/api/data/list");
        if (response.ok) {
            const result = await response.json();
            // Cache is ready for use in autocomplete fields
            console.log('[REFERENCE_DATA] Loaded data types list:', result);
        }
    } catch (error) {
        console.error("Failed to load reference data:", error);
    }
}

/**
 * Fetch specific reference data type with caching
 * @param {string} dataType - Data type to fetch
 * @returns {Promise<Object|null>} Data object or null
 */
export async function fetchReferenceData(dataType) {
    const cached = getCachedReferenceData(dataType);
    if (cached) {
        return cached;
    }

    try {
        const response = await fetch(`/api/data/${dataType}`);
        if (response.ok) {
            const data = await response.json();
            setCachedReferenceData(dataType, data);
            return data;
        }
    } catch (error) {
        console.error(`Failed to fetch ${dataType}:`, error);
    }

    return null;
}
