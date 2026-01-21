/**
 * Tests for api.js module
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import * as api from '../static/js/api.js';

describe('API Module', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('loadFile', () => {
        it('should fetch file from API', async () => {
            const mockData = { id: 'test', name: 'Test Mod' };
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockData,
            });
            global.fetch = mockFetch;

            const result = await api.loadFile('/path/to/file.yml');

            expect(mockFetch).toHaveBeenCalledWith('/api/civilization/load', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: '/path/to/file.yml' }),
            });
            expect(result).toEqual(mockData);
        });

        it('should throw error on failed response', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Not Found',
            });
            global.fetch = mockFetch;

            await expect(api.loadFile('/invalid.yml')).rejects.toThrow('Load failed');
        });

        it('should throw error on network failure', async () => {
            const mockFetch = vi.fn().mockRejectedValue(new Error('Network error'));
            global.fetch = mockFetch;

            await expect(api.loadFile('/path.yml')).rejects.toThrow();
        });

        it('should log error on failure', async () => {
            const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
            const mockFetch = vi.fn().mockRejectedValue(new Error('Test error'));
            global.fetch = mockFetch;

            try {
                await api.loadFile('/path.yml');
            } catch (e) {
                // Expected
            }

            expect(consoleSpy).toHaveBeenCalledWith('[LOAD_ERROR]', expect.any(Error));
            consoleSpy.mockRestore();
        });
    });

    describe('saveFile', () => {
        it('should save file via API', async () => {
            const mockData = { id: 'test', name: 'Test' };
            const mockResponse = { success: true };
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });
            global.fetch = mockFetch;

            const result = await api.saveFile('/path/to/file.yml', mockData);

            expect(mockFetch).toHaveBeenCalledWith('/api/civilization/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: '/path/to/file.yml', data: mockData }),
            });
            expect(result).toEqual(mockResponse);
        });

        it('should throw error on save failure', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Internal Server Error',
            });
            global.fetch = mockFetch;

            await expect(api.saveFile('/path.yml', {})).rejects.toThrow('Save failed');
        });
    });

    describe('exportYAML', () => {
        it('should export data as blob', async () => {
            const mockBlob = new Blob(['test yaml']);
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                blob: async () => mockBlob,
            });
            global.fetch = mockFetch;

            const result = await api.exportYAML({ id: 'test' });

            expect(mockFetch).toHaveBeenCalledWith('/api/civilization/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: 'test' }),
            });
            expect(result).toEqual(mockBlob);
        });

        it('should throw error on export failure', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Bad Request',
            });
            global.fetch = mockFetch;

            await expect(api.exportYAML({})).rejects.toThrow('Export failed');
        });
    });

    describe('validateModData', () => {
        it('should validate mod data', async () => {
            const mockResponse = { isValid: true, errors: [] };
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });
            global.fetch = mockFetch;

            const result = await api.validateModData({ id: 'test' });

            expect(mockFetch).toHaveBeenCalledWith('/api/civilization/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: 'test' }),
            });
            expect(result).toEqual(mockResponse);
        });

        it('should throw error on validation failure', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Bad Request',
            });
            global.fetch = mockFetch;

            await expect(api.validateModData({})).rejects.toThrow('Validation failed');
        });
    });

    describe('validateField', () => {
        it('should validate single field', async () => {
            const mockResponse = { isValid: true };
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });
            global.fetch = mockFetch;

            const result = await api.validateField('yield_type', 'PRODUCTION', 'yield-types');

            expect(mockFetch).toHaveBeenCalledWith('/api/field/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ field_name: 'yield_type', value: 'PRODUCTION', data_type: 'yield-types' }),
            });
            expect(result).toEqual(mockResponse);
        });
    });

    describe('fetchReferenceData', () => {
        it('should fetch reference data from API', async () => {
            const mockData = ['YIELD_PRODUCTION', 'YIELD_SCIENCE'];
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockData,
            });
            global.fetch = mockFetch;

            const result = await api.fetchReferenceData('yield-types');

            expect(mockFetch).toHaveBeenCalledWith('/api/data/yield-types');
            expect(result).toEqual(mockData);
        });

        it('should use cached data on subsequent calls', async () => {
            const mockData = { values: ['YIELD_PRODUCTION'] };
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockData,
            });
            global.fetch = mockFetch;

            // Clear cache before test
            await import('../static/js/state.js').then(m => m.clearReferenceDataCache());

            // First call
            await api.fetchReferenceData('yield-types');
            // Second call should use cache
            await api.fetchReferenceData('yield-types');

            // Should only fetch once due to caching
            expect(mockFetch).toHaveBeenCalledTimes(1);
        });

        it('should throw error on fetch failure', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Not Found',
            });
            global.fetch = mockFetch;

            await expect(api.fetchReferenceData('invalid-type')).rejects.toThrow();
        });
    });

    describe('getReferenceDataTypes', () => {
        it('should get list of data types', async () => {
            const mockTypes = ['yield-types', 'effects', 'tags'];
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockTypes,
            });
            global.fetch = mockFetch;

            const result = await api.getReferenceDataTypes();

            expect(mockFetch).toHaveBeenCalledWith('/api/data/list');
            expect(result).toEqual(mockTypes);
        });
    });

    describe('healthCheck', () => {
        it('should check API health', async () => {
            const mockResponse = { status: 'ok' };
            const mockFetch = vi.fn().mockResolvedValue({
                ok: true,
                json: async () => mockResponse,
            });
            global.fetch = mockFetch;

            const result = await api.healthCheck();

            expect(mockFetch).toHaveBeenCalledWith('/api/health');
            expect(result).toEqual(mockResponse);
        });

        it('should throw error on health check failure', async () => {
            const mockFetch = vi.fn().mockResolvedValue({
                ok: false,
                statusText: 'Service Unavailable',
            });
            global.fetch = mockFetch;

            await expect(api.healthCheck()).rejects.toThrow('Health check failed');
        });
    });
});
