/**
 * API Module - Backend communication
 * File operations, reference data fetching, and API integration
 */

import { getCachedReferenceData, setCachedReferenceData } from './state.js';

/**
 * Upload and load a YAML file
 * @param {File} file - File object from input element
 * @returns {Promise<Object>} Parsed YAML data
 */
export async function uploadFile(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/civilization/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[UPLOAD_ERROR]', error);
        throw error;
    }
}

/**
 * Load a YAML file from disk
 * @param {string} filePath - Absolute path to YAML file
 * @returns {Promise<Object>} Parsed YAML data
 */
export async function loadFile(filePath) {
    try {
        const response = await fetch('/api/civilization/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: filePath }),
        });

        if (!response.ok) {
            throw new Error(`Load failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[LOAD_ERROR]', error);
        throw error;
    }
}

/**
 * Save data to YAML file on disk
 * @param {string} filePath - Absolute path to YAML file
 * @param {Object} data - Data to save
 * @returns {Promise<Object>} Save confirmation
 */
export async function saveFile(filePath, data) {
    try {
        const response = await fetch('/api/civilization/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: filePath, data }),
        });

        if (!response.ok) {
            throw new Error(`Save failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[SAVE_ERROR]', error);
        throw error;
    }
}

/**
 * Export data as YAML blob for download
 * @param {Object} data - Data to export
 * @returns {Promise<Blob>} YAML blob
 */
export async function exportYAML(data) {
    try {
        const response = await fetch('/api/civilization/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`Export failed: ${response.statusText}`);
        }

        return await response.blob();
    } catch (error) {
        console.error('[EXPORT_ERROR]', error);
        throw error;
    }
}

/**
 * Save YAML to disk via backend
 * @param {Object} data - Data to export
 * @param {string} downloadPath - Directory path to save to
 * @returns {Promise<Object>} Save confirmation
 */
export async function exportYAMLToDisk(data, downloadPath) {
    try {
        const response = await fetch('/api/civilization/export-disk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data, download_path: downloadPath }),
        });

        if (!response.ok) {
            throw new Error(`Export failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[EXPORT_DISK_ERROR]', error);
        throw error;
    }
}

/**
 * Save built mod to disk via backend
 * @param {Object} data - Data to export and build
 * @param {string} downloadPath - Directory path to save to
 * @returns {Promise<Object>} Save confirmation
 */
export async function exportBuiltModToDisk(data, downloadPath) {
    try {
        const response = await fetch('/api/civilization/export-built-disk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data, download_path: downloadPath }),
        });

        if (!response.ok) {
            throw new Error(`Export failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[EXPORT_BUILT_DISK_ERROR]', error);
        throw error;
    }
}

/**
 * Export data as a fully built mod (zipped)
 * @param {Object} data - Data to export and build
 * @returns {Promise<Blob>} Built mod zip blob
 */
export async function exportBuiltMod(data) {
    try {
        const response = await fetch('/api/civilization/export-built', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`Build export failed: ${response.statusText}`);
        }

        return await response.blob();
    } catch (error) {
        console.error('[BUILD_EXPORT_ERROR]', error);
        throw error;
    }
}

/**
 * Validate mod data on server
 * @param {Object} data - Data to validate
 * @returns {Promise<Object>} Validation result
 */
export async function validateModData(data) {
    try {
        const response = await fetch('/api/civilization/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`Validation failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[VALIDATION_ERROR]', error);
        throw error;
    }
}

/**
 * Validate a single field value against reference data
 * @param {string} fieldName - Field name
 * @param {string} value - Value to validate
 * @param {string} dataType - Reference data type
 * @returns {Promise<Object>} Validation result
 */
export async function validateField(fieldName, value, dataType) {
    try {
        const response = await fetch('/api/field/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ field_name: fieldName, value, data_type: dataType }),
        });

        if (!response.ok) {
            throw new Error(`Field validation failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[FIELD_VALIDATION_ERROR]', error);
        throw error;
    }
}

/**
 * Fetch reference data from API
 * Uses caching to avoid redundant requests
 * @param {string} dataType - Type of reference data (yield-types, effects, etc.)
 * @returns {Promise<Array>} Reference data
 */
export async function fetchReferenceData(dataType) {
    // Check cache first
    const cached = getCachedReferenceData(dataType);
    if (cached) {
        return cached;
    }

    try {
        const response = await fetch(`/api/data/${dataType}`);

        if (!response.ok) {
            throw new Error(`Failed to fetch ${dataType}: ${response.statusText}`);
        }

        const data = await response.json();
        setCachedReferenceData(dataType, data);
        return data;
    } catch (error) {
        console.error(`[REFERENCE_DATA_ERROR] ${dataType}`, error);
        throw error;
    }
}

/**
 * Get list of available reference data types
 * @returns {Promise<Array>} List of data type names
 */
export async function getReferenceDataTypes() {
    try {
        const response = await fetch('/api/data/list');

        if (!response.ok) {
            throw new Error(`Failed to fetch data types: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[DATA_TYPES_ERROR]', error);
        throw error;
    }
}

/**
 * Health check for backend
 * @returns {Promise<Object>} Health status
 */
export async function healthCheck() {
    try {
        const response = await fetch('/api/health');

        if (!response.ok) {
            throw new Error(`Health check failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('[HEALTH_CHECK_ERROR]', error);
        throw error;
    }
}
