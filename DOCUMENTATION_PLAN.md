# Documentation Review Plan

## Goal
Ensure the Python library is as easy to use as the TypeScript version, with clear instructions for migration and new usage.

## Strategy
Compare existing docs and validate the "Getting Started" experience.

## Test Steps

### 1. README Comparison
*   Review root `README.md` (currently TS focused).
*   Review `docs/INDEX.md` and Python specific docs.
*   **Gap Analysis**: identify what TS has that Python misses.

### 2. API Documentation
*   Check if docstrings exist for main classes (`Mod`, `CivilizationBuilder`, `UnitBuilder`).
*   Check if Python type hints provide sufficient IDE autocomplete (IntelliSense) support, which is a major feature of the TS version.

### 3. Example Code
*   Review `examples/` directory.
*   Are there Python equivalents for all TS examples?
    *   `civilization.ts` -> `civilization.py`
    *   `unit.ts` -> `unit.py`
    *   `progression-tree.ts` -> `progression_tree.py`
*   Are the examples runnable and commented?

### 4. Migration Guide
*   Review `docs/MIGRATION.md` (if it exists) or assess need for one.
*   How hard is it for a TS modder to switch to Python?

## Deliverables
*   `DOCUMENTATION_REPORT.md`: List of missing docs.
*   Updates to `README.md` to dual-support Python and TS or separate them clearly.
