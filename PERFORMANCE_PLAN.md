# Performance Review Plan

## Goal
Quantify the performance difference between the compiled TypeScript/Node.js implementation and the Python implementation. Ensure the Python port is performant enough for large mod generation.

## Strategy
Run identical build tasks in both environments using the existing `benchmark.py` script and additional stress tests if needed.

## Test Steps

### 1. Baseline Benchmark (Gondor Example)
*   **Tool**: `benchmark.py` (already exists in repo).
*   **Method**:
    *   Run TS: `tsx build.ts` (via `npm run build`) x 10 iterations.
    *   Run Python: `python examples/gondor_civilization.py` x 10 iterations.
*   **Metrics**:
    *   Mean execution time.
    *   Cold start overhead (process startup).

### 2. Large Scale Stress Test (Proposed)
*   **Concept**: Generate a mod with 100 civilizations and 500 units to test serialization scaling.
*   **TS**: Create `benchmark-stress.ts` loop.
*   **Python**: Create `benchmark_stress.py` loop.
*   **Metrics**:
    *   Time to generate 1000+ files.
    *   Memory usage (optional).

### 3. Dependency Overhead
*   Analyze `uv` vs `npm` install times (cold environment setup).
*   Analyze import time overhead (`node_modules` resolution vs `python` imports).

## Deliverables
*   `PERFORMANCE_REPORT.md`: Comparison table and graphs (if possible).
*   Optimization recommendations for Python if > 2x slower than TS (unlikely, but possible due to IO).
