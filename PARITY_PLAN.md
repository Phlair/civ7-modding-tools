# Parity Review Plan

## Goal
Verify that the Python implementation of `civ7-modding-tools` achieves 100% functional parity with the original TypeScript version, producing identical (or semantically equivalent) mod output structures.

## Strategy
We will use the "Gondor Civilization" example as the baseline for comparison, as it utilizes nearly all available builders (Civilization, Unit, Constructible, ProgressionTree, ImportFile, Modifiers).

## Test Steps

### 1. Build Reference Output (TypeScript)
*   **Command**: `npm run build` (runs `build.ts`)
*   **Output Directory**: `dist-ts-reference/` (We will rename standard `dist/` to this for comparison)
*   **Verification**: Ensure `mod-test.modinfo` and XML subdirectories are created.

### 2. Build Candidate Output (Python)
*   **Command**: `uv run python examples/gondor_civilization.py`
*   **Output Directory**: `dist-py-candidate/` (Script should be configured to output here)
*   **Verification**: Ensure directory structure matches TS output.

### 3. Structural Comparison
*   **Directory Walk**: Compare file tree of `dist-ts-reference/` vs `dist-py-candidate/`.
*   **File Presence**:
    *   Check if `.modinfo` exists in root.
    *   Check `civilizations/`, `units/`, `constructibles/` subfolders match.
    *   Check `imports/` folder contains copied assets.

### 4. Content Comparison (Deep Dive)
*   **ModInfo Analysis**:
    *   Compare `mod-test.modinfo` files.
    *   Check `<Mod id="..." version="...">` attributes.
    *   Check `<ActionCriteria>` block generation (critical for logic).
    *   Check `<ActionGroup>` definitions.
*   **XML Generation Analysis**:
    *   Pick key files: `civilizations/.../always.xml`, `units/.../always.xml`.
    *   Compare XML structure (ignoring attribute order if semantically same, though identical order is preferred).
    *   Check XML formatting (indentation, headers).
    *   Check boolean serialization (`"true"` vs `"True"`).
*   **Asset Import**:
    *   Verify `civ-icon.png` is identical in bytes.

### 5. Automated Diff Report
*   Run a script to diff all generated text files and report discrepancies.
*   Analyze differences:
    *   **Accepted Differences**: UUIDs (if random), timestamp comments.
    *   **Critical Failures**: Missing attributes, wrong casing (`PascalCase` vs `snake_case` in XML), missing tags.

## Deliverables
*   `PARITY_REPORT.md`: Detailed breakdown of differences.
*   Fixes PR for any identified parity gaps.
