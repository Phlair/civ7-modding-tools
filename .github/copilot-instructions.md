# Phlair's Civ VII Modding Tools - Copilot Instructions

## Project Overview

Python library for programmatically generating Civilization VII mods using type-safe builders and automatic XML generation.

- **Version**: 1.3.0
- **Python**: 3.12+
- **Package Manager**: uv

## Architecture

```
Mod → Builders → Nodes → Files → .modinfo + XML
```

### Core Components

**1. Mod (Orchestrator)**
- Path: `src/civ7_modding_tools/core/mod.py`
- Manages all builders and files
- Generates `.modinfo` and coordinates XML output
- Auto-extracts action group criteria
- Constructor supports both dict and kwargs patterns

**2. Builders (13 classes)**
- Path: `src/civ7_modding_tools/builders/builders.py`
- Extend `BaseBuilder` (abstract)
- Implement `.fill(payload)` for fluent API
- Implement `.build() -> list[BaseFile]`
- All have `action_group_bundle` property

**Builder Types:**
- `CivilizationBuilder` - Full civilizations
- `UnitBuilder` - Military/civilian units
- `ConstructibleBuilder` - Buildings/improvements
- `ProgressionTreeBuilder` - Civic/tech trees
- `ProgressionTreeNodeBuilder` - Tree nodes
- `ModifierBuilder` - Game modifiers
- `TraditionBuilder` - Traditions
- `UniqueQuarterBuilder` - Unique districts
- `LeaderUnlockBuilder` - Leader age transitions
- `CivilizationUnlockBuilder` - Civ age transitions
- `UnlockBuilder` - Generic unlocks
- `ImportFileBuilder` - Asset imports

**3. Nodes (79 types)**
- Path: `src/civ7_modding_tools/nodes/`
- Extend `BaseNode` with `_name` class variable
- Properties convert snake_case → PascalCase XML attributes
- Method: `to_xml_element() -> dict | None`
- Boolean → "true"/"false" strings
- `None` values omitted from output

**4. Files (3 types)**
- Path: `src/civ7_modding_tools/files/__init__.py`
- `BaseFile` - Abstract base
- `XmlFile` - Uses xmltodict, 4-space indent
- `ImportFile` - Copies external assets

**5. Localizations (11 classes)**
- Path: `src/civ7_modding_tools/localizations/__init__.py`
- Pydantic BaseModel subclasses
- Method: `get_nodes(entity_id) -> list[dict]`
- One per builder type

**6. Constants (21 Enums)**
- Path: `src/civ7_modding_tools/constants/__init__.py`
- `Trait` - Civilization traits (ECONOMIC, CULTURAL, etc.)
- `UnitClass` - Unit classifications (MELEE, RANGED, etc.)
- `Yield` - Resources (PRODUCTION, GOLD, SCIENCE, etc.)
- `Effect` - Game effects
- `Requirement` - Game conditions
- `District` - District types
- `Age` - Game ages (ANTIQUITY, EXPLORATION, MODERN)
- And 14 more...

**7. Utils**
- Path: `src/civ7_modding_tools/utils/__init__.py`
- `locale(prefix, var)` - Generate LOC keys
- `fill(obj, payload)` - Set object properties
- `trim(s)` - Remove prefixes
- `kebab_case(s)` - Convert to kebab-case
- `camel_to_pascal(s)` - Convert case
- `without(lst, *vals)` - Filter list
- `uniq_by(lst, key_fn)` - Deduplicate

## Key Patterns

### Builder Pattern
```python
# Constructor with fill()
builder = CivilizationBuilder().fill({
    'civilization_type': 'CIVILIZATION_ROME',
    'civilization_traits': [Trait.MILITARY.value]
})

# Or constructor with dict
builder = CivilizationBuilder({...})
```

### Action Groups
Controls when content loads (by age):
```python
from civ7_modding_tools import ActionGroupBundle

# Age-specific
AGE_ANTIQUITY = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')

# Always loaded
ALWAYS = ActionGroupBundle(action_group_id='ALWAYS')

builder.action_group_bundle = AGE_ANTIQUITY
```

Creates 4 action group variants:
- `shell` - UI scope
- `always` - Always loaded
- `current` - Current age only
- `persist` - Age + future ages

### Path Generation
Two-step process:
1. `trim("CIVILIZATION_GONDOR")` → `"GONDOR"`
2. `kebab_case("GONDOR")` → `"gondor"`

Result: `/civilizations/gondor/`

Examples:
- `UNIT_GONDOR_SCOUT` → `/units/gondor-scout/`
- `BUILDING_GONDOR2` → `/constructibles/gondor2/`

### File Naming
Standard names:
- `always.xml` - Always-loaded content
- `current.xml` - Current age content
- `persist.xml` - Persisting content
- `shell.xml` - UI/shell content
- `game-effects.xml` - Modifiers
- `icons.xml` - Icon definitions
- `localization.xml` - Localized text
- `legacy.xml` - Legacy compatibility (INSERT OR IGNORE)
- `visual-remap.xml` - Visual remapping
- `unlocks.xml` - Unlocks

ImportFileBuilder uses `target_name` parameter for output filename.

## Reference Data Files

Predefined enumeration values extracted from the game data. These are the valid configuration options available for building mods—use these exact IDs when creating civilizations, units, buildings, modifiers, etc.

**Location:** `src/civ7_modding_tools/data/`  
**Format:** 31 JSON files (kebab-case naming) with 3,400+ valid game values

### Core Data Types
- `yield-types.json` - Valid yield resource types (production, science, gold, culture, etc.)
- `district-types.json` - Valid district categories for constructible placement
- `terrain-types.json` - Valid terrain types for map features and yield modifiers
- `ages.json` - Valid game ages for age-gated content
- `tags.json` - Valid entity tags for categorization and filtering (2,945 tags)

### Unit/Building Systems
- `unit-movement-classes.json` - Valid unit movement types (foot soldiers, mounted, naval, etc.)
- `core-classes.json` - Valid unit role categories (military, civilian, support)
- `formation-classes.json` - Valid unit formation types for grouping and combat
- `constructible-classes.json` - Valid constructible type categories
- `domains.json` - Valid operational domains (land, sea)

### Map & Terrain
- `biome-types.json` - Valid biome types for terrain generation
- `feature-types.json` - Valid map features (forests, marshes, reefs, etc.)
- `river-placements.json` - Valid river placement options relative to buildings
- `building-cultures.json` - Valid visual building style sets (with civilization mappings)
- `unit-cultures.json` - Valid visual unit style sets (with civilization mappings)

### Game Mechanics
- `cost-progression-models.json` - Valid cost scaling formulas for buildings/units
- `government-types.json` - Valid government types
- `project-types.json` - Valid city project types
- `difficulty-types.json` - Valid difficulty levels
- `progression-trees.json` - Valid civics/tech tree IDs

### Effects & Conditions
- `effects.json` - Valid modifier effect types (205 total)
- `requirement-types.json` - Valid conditional test types for effect application (127 total)
- `collection-types.json` - Valid modifier scope types (player, city, plot, unit, etc.)

### Python API

Load and reference valid game values:

```python
from civ7_modding_tools.data import get_yield_types, get_effects

# Each returns the valid values for that configuration option
yields = get_yield_types()           # All valid yield types to reference
effects = get_effects()              # All valid effect types to reference
# Use these in your builder configurations
```

**Regenerate:** Run `python src/civ7_modding_tools/scripts/extract_data_values.py` when game data updates.

## Code Conventions

### Language & Style

- **British English** in all docs/comments
- **PEP 8** with 100-character line limit
- **snake_case** for all Python identifiers
- **PascalCase** for classes only
- **Full type hints** required

### Naming
- Functions/vars: `snake_case`
- Classes: `PascalCase`
- Constants/enums: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### Type Hints
```python
from typing import Any, Optional

def fill(obj: T, payload: dict[str, Any]) -> T:  # Use T, not Generic
def locale(prefix: str | None, variable: str) -> str:  # Use | not Union
```

Use modern syntax:
- `dict[str, Any]` not `Dict[str, Any]`
- `list[str]` not `List[str]`
- `str | None` not `Optional[str]`

### Docstrings (PEP 257)
```python
def my_function(arg: str) -> str:
    """
    Brief one-line summary.
    
    Longer description if needed, explaining behaviour,
    arguments, return values, and examples.
    
    Args:
        arg: Argument description
        
    Returns:
        Return value description
        
    Raises:
        ValueError: When validation fails
    """
```

## Common Operations

### Creating a Mod
```python
mod = Mod(
    id='my-mod',
    version='1.0.0',
    name='My Mod Name',
    description='Mod description',
    authors='Author Name'
)
```

### Adding Builders
```python
# Single
mod.add(civilization_builder)

# Multiple
mod.add([unit1, unit2, building1])
```

### Building Output
```python
mod.build('./dist')  # Generates files in ./dist/
mod.build('./dist', clear=False)  # Don't clear directory first
```

### Using Constants
```python
from civ7_modding_tools.constants import Trait, UnitClass, Yield

# Always use .value to get string
civilization.fill({
    'civilization_traits': [Trait.ECONOMIC.value, Trait.MILITARY.value],
})
```

### Localizations
```python
from civ7_modding_tools.localizations import CivilizationLocalization

loc = CivilizationLocalization(
    name='Rome',
    description='The eternal city',
    adjective='Roman',
    city_names=['Rome', 'Antium', 'Cumae']
)

civ.fill({'localizations': [loc]})
```

## Testing

### Running Tests
```bash
uv run pytest              # All tests
uv run pytest --cov        # With coverage
uv run pytest -v           # Verbose
uv run pytest tests/test_integration_e2e.py  # Specific file
```

### Test Structure
- `tests/test_*.py` - 12 test files
- `tests/fixtures/` - Test data
- Uses pytest with 94% coverage

### Writing Tests
```python
def test_my_feature():
    """Test description."""
    mod = Mod(id='test')
    builder = CivilizationBuilder().fill({...})
    mod.add(builder)
    
    # Generate to temp dir
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        # Assert file exists, XML structure, etc.
```

## Development Workflow

1. **Make changes** to Python files
2. **Add tests** in `tests/`
3. **Run tests**: `uv run pytest`
4. **Check coverage**: `uv run pytest --cov`
5. **Type check** (optional): `uv run mypy src/`
6. **Commit** changes

## Critical Rules

1. **Never use camelCase** in Python code (snake_case only)
2. **Always use type hints** on functions/methods
3. **Use Pydantic** for all data models
4. **Extend BaseBuilder** for new builders
5. **Implement build()** returning `list[BaseFile]`
6. **Use .value** on enum constants
7. **Follow 100-char** line limit
8. **British spelling** in docs
9. **Test new features** with pytest
10. **Document** all public APIs

## File Organization

```
src/civ7_modding_tools/
├── __init__.py           # Package exports
├── core/
│   ├── __init__.py
│   └── mod.py            # Mod + ActionGroupBundle
├── builders/
│   ├── __init__.py
│   └── builders.py       # All 13 builders
├── nodes/
│   ├── __init__.py
│   ├── base.py           # BaseNode
│   ├── nodes.py          # Game entities (60+ nodes)
│   ├── database.py       # Database operations
│   └── action_groups.py  # Action group nodes
├── files/
│   └── __init__.py       # BaseFile, XmlFile, ImportFile
├── localizations/
│   └── __init__.py       # 11 localization classes
├── constants/
│   └── __init__.py       # 21 enum classes
├── utils/
│   └── __init__.py       # Utility functions
└── xml_builder.py        # XML generation utilities
```

## Dependencies

- **pydantic** (≥2.0.0) - Data validation
- **xmltodict** (≥0.13.0) - XML generation

## Web Editor (Optional)

### Overview

Visual web interface for editing YAML civilization mod configurations using FastAPI, HTMX, and Tailwind CSS. Not required for programmatic mod generation, but provides intuitive UI for YAML-based editing.

Notes:
- `web/templates/index.html` loads Tailwind via CDN and includes the HTMX script (HTMX components are optional).
- Core UI rendering is handled by ES6 modules in `web/static/js/`.

### Architecture

```
Browser (Client) ←→ FastAPI REST API ←→ File System + Reference Data
    - ES6 Modules      - 9 endpoints        - YAML load/save + templates
  - Tailwind CSS     - Pydantic validation - 33 JSON data files
  - Vanilla JS       - Caching system     - civ7_modding_tools/data
```

### File Organization (Modular)

**Frontend Structure (ES6 Modules - no build step required):**

```
web/static/js/
├── main.js              # Entry point, exposes functions to window for inline handlers
├── state.js             # Global state (currentData, wizardData, dataCache), config objects
├── api.js               # Backend communication (loadFile, saveFile, exportYAML, etc.)
├── ui.js                # Toast notifications, loading states, dirty indicator updates
├── templates.js         # Template loading and selection via modal
├── data/
│   └── loader.js        # Reference data loader and caching
├── wizard/
│   ├── wizard.js        # Wizard flow engine: switchMode(), wizardNextStep(), wizardPrevStep()
│   ├── step1.js         # Metadata, module localization, age section
│   ├── step2.js         # Civilization core properties, traits, tags, icon
│   ├── step3.js         # Units & buildings: renderWizardStep3() with inline handlers
│   ├── step4.js         # Modifiers & traditions: renderWizardStep4() with inline handlers
│   └── step5.js         # Review & finish: validation summary, content counts
├── expert/
│   ├── sections.js      # renderAllSections() dispatches to 13 section renderers
│   ├── civilization.js  # 9 civilization sub-renderers (terrains, unlocks, biases, localizations, etc.)
│   └── navigation.js    # getAvailableSections() returns 13 sections with metadata
└── form/
    ├── fields.js        # Field creators: createTextField(), createStringArrayField(), etc.
    └── arrays.js        # Array helpers exposed to window: arrayAddItem(), arrayRemoveItem()
```

**Testing Structure (Vitest with browser APIs):**

```
web/tests/
├── test_ui.js                      # UI module tests (toast, loading, dirty indicator)
├── test_templates.js               # Template loading and selection tests
├── test_state.js                   # State management tests (dirty tracking, data updates)
├── test_api.js                     # API layer tests (load, save, export, validate)
├── test_wizard.js                  # Wizard flow engine tests (step navigation, mode switching)
├── test_wizard_steps_3_4_5.js      # Units, Buildings, Modifiers, Traditions, Review tests (47 tests)
├── test_expert_navigation.js       # Navigation tests (scroll spy, section switching)
├── test_form_fields.js             # Field creator tests (all field types)
└── test_form_arrays.js             # Array helper tests (add, remove, rerender)
```

**Backend Files:**

| Path | Purpose |
|------|---------|
| `web/app.py` | FastAPI backend with Pydantic validation, YAML parsing, reference data endpoints |
| `web/run.py` | Development server launcher (auto-reload, uvicorn wrapper) |
| `web/templates/index.html` | HTML entry point, module imports, navbar, containers for wizard/expert |
| `web/templates/components.html` | Reusable HTMX form components (optional) |
| `web/static/css/styles.css` | Tailwind CSS, custom animations, dark theme overrides |
| `web/__init__.py` | FastAPI app initialization |

### REST API Endpoints

**File Operations:**
- `POST /api/civilization/load` - Load YAML, returns parsed data
- `POST /api/civilization/save` - Persist edited YAML to disk
- `POST /api/civilization/export` - Export YAML as downloadable file
- `POST /api/civilization/validate` - Validate configuration structure

**Reference Data:**
- `GET /api/data/{type}` - Get specific data (yield-types, effects, tags, etc.) with caching
- `GET /api/data/list` - List all 33 available data types
- `POST /api/field/validate` - Validate field value against reference data

**Utility:**
- `GET /api/health` - Health check
- `GET /docs` - Swagger UI (auto-generated)

**Templates:**
- `GET /api/templates/{template_name}` - Load a pre-built template (blank, scientific, military, cultural, economic)

### Running the Editor

```bash
# Install dependencies
uv sync --extra web

# Start server
python web/run.py
# Server runs at http://127.0.0.1:8000
# Auto-reloads on file changes
```

### Module Architecture & Patterns

**Event Handling Pattern (Critical):**
Due to frequent DOM re-renders in wizard/expert modes, event handlers cannot use `addEventListener` (listeners are lost when DOM is replaced). Instead:
- All interactive functions are exposed to `window` object synchronously via `Object.defineProperty()` or direct assignment
- Event handlers use inline `onclick="window.functionName()"` attributes
- This ensures handlers persist through DOM mutations
- Example: `<button onclick="window.wizardNextStep()">Next</button>`

**1. Main Entry Point (main.js)**
- Imports and exposes wizard functions to `window`: `switchMode`, `skipWizard`, `wizardPrevStep`, `wizardNextStep`, `createNewMod`
- Uses `Object.defineProperty()` for read-only window assignments (security)
- Initializes reference data loader on `DOMContentLoaded`
- Sets up event delegation for navbar and container clicks

**2. State Management (state.js)**
- Exports: `currentData`, `wizardData`, `isDirty`, `dataCache` (mutable globals)
- Mutation functions: `markDirty()`, `setCurrentData()`, `getCurrentData()`, `resetWizardData()`
- Config objects: `AUTOCOMPLETE_MAPPINGS`, `FIELD_HELP_TEXT`, `REQUIRED_FIELDS`
- All state mutations go through exported functions for traceability

**3. API Layer (api.js)**
- Async functions: `loadFile(path)`, `saveFile(path, data)`, `exportYAML()`, `validateModData(data)`, `healthCheck()`
- Reference data: `fetchReferenceData(type)`, caching via state.js
- Error handling with console prefixes: `[LOAD_ERROR]`, `[SAVE_ERROR]`, `[VALIDATION_ERROR]`
- All communication via fetch to FastAPI backend

**4. UI Module (ui.js)**
- Pure functions: `showToast(message, type)`, `showLoading(element)`, `updateDirtyIndicator(isDirty)`
- No state dependencies, direct DOM manipulation
- Uses Tailwind classes: `bg-green-600`, `text-red-400`, `opacity-50`, etc.
- Synchronous (no async operations)

**5. Templates Module (templates.js)**
- `showTemplateModal()` / `hideTemplateModal()` control the template modal
- `loadTemplate(templateName)` fetches template data (currently calls `/api/template/{name}`; backend route is `/api/templates/{template_name}`)
- `getAvailableTemplates()` returns template metadata used by the UI

**6. Data Loader (data/loader.js)**
- `loadReferenceData()` - Fetches `/api/data/list`, logs available types
- Caches reference data in state for form field use
- Called on app initialization

**7. Wizard Flow (wizard/wizard.js)**
- Functions: `initializeMode()`, `switchMode(mode)`, `wizardNextStep()`, `wizardPrevStep()`, `skipWizard()`, `initializeWizard()`
- `renderWizardStep()` - Main renderer, dynamically imports step modules
- `validateWizardData()` - Validates current step before advancing
- `saveWizardStepData()` - Merges step data into `wizardData`
- Exposes step renderers: `renderWizardStep1()` through `renderWizardStep5()`
- LocalStorage: Saves user's mode preference ("wizard" or "expert")

**8. Wizard Steps (wizard/step1-5.js)**
- Each exports: `renderWizardStepN(container)` - Renders UI for that step
- Internal functions exposed to `window` inside render: handlers for form interactions
- Steps 3 & 4: Use inline `onclick="window.wizardSaveUnit()"`, `onclick="window.wizardSaveModifier()"`, etc.
- Step data synchronized via `state.wizardData` mutations
- Step 5: Displays validation errors, content counts, next steps

**9. Expert Sections (expert/sections.js)**
- `renderAllSections(container, data)` - Main entry point, creates 13 collapsible sections
- `renderSectionContent(container, sectionId, data)` - Switch dispatcher to 13 renderers
- `updateFieldValue(fieldPath, value)` - Dot-notation path updater (e.g., "civilization.traits")
- Each section has collapsible header with arrow toggle
- Sections import sub-renderers asynchronously (civilization.js for civ-specific renderers)

**10. Civilization Sub-renderers (expert/civilization.js)**
- Exports: 9 renderer functions for civ-specific nested structures
  - `renderStartBiasTerrains()`, `renderCivilizationUnlocks()`, `renderLeaderCivilizationBiases()`
  - `renderLocalizations()`, `renderLoadingInfoCivilizations()`, `renderLeaderCivPriorities()`
  - `renderAIListTypes()`, `renderAILists()`, `renderAIFavoredItems()`
- Pattern: Each maintains local `rerenderItems()` function to handle CRUD with inline `onclick` handlers
- Uses `getCurrentData()` to read current state, `markDirty()` on mutations

**11. Expert Navigation (expert/navigation.js)**
- `getAvailableSections()` - Returns array of 13 section metadata: `{id, title, color}`
- `setupScrollSpy()` - Highlights active section on scroll (optional)
- `switchToSection(sectionId)` - Smooth scrolls to section
- Color mapping for visual distinction

**12. Form Fields (form/fields.js)**
- Exports: `createTextField()`, `createNumberField()`, `createBooleanField()`, `createAutocompleteField()`, `createStringArrayField()`
- Each returns DOM element (not string HTML)
- Autocomplete: Fuzzy search against reference data, usage tracking in localStorage
- String arrays: Creates items with inline `onclick` handlers calling `window.arrayAddItem()` / `window.arrayRemoveItem()`
- **Imports `form/arrays.js`** at top for side-effect of exposing functions to window

**13. Form Arrays (form/arrays.js)**
- Exports: `addArrayItem(fieldName)`, `removeArrayItem(fieldName, idx)`, `updateArrayItem(fieldName, idx, value)`
- Getter: `getArrayFieldValues(fieldName)` - Returns current array values
- Re-render: `rerenderArrayField(fieldName, items)` - Clears and rebuilds all items
- Container id pattern: `array-container-${fieldName}` (used by `createStringArrayField`)
- **Exposes to window**: `arrayAddItem`, `arrayRemoveItem`, `arrayUpdateItem` via side-effect
- All operations call `markDirty()` after mutation

### Features

- **Two Modes**: Guided wizard (5 steps) + Expert mode (13 collapsible sections)
- **Color-Coded Navigation**: 13 unique colors for quick section identification
- **Dirty State Tracking**: Automatically set on any field change, saved to UI indicator
- **Real-Time Validation**: Field blur validation against reference data
- **Reference Data Integration**: Autocomplete dropdowns with fuzzy search and usage tracking
- **Form Components**: Text, number, boolean, autocomplete selects, string arrays, nested objects
- **Dark Theme UI**: Optimized for modding workflows with Tailwind CSS
- **No Build Step**: ES6 modules load directly in browser (Chrome 61+, Firefox 60+, Safari 11+)

### Development Workflow

**Adding a new section to expert mode:**
1. Add section metadata to `getAvailableSections()` in `expert/navigation.js` (id, title, color)
2. Create `renderXyzSection(container, data)` in `expert/sections.js`
3. Add `case 'xyz'` in `renderSectionContent()` dispatcher
4. If section is complex, export renderer from `expert/civilization.js` or create new sub-renderer file
5. Use inline `onclick` handlers; expose functions to `window` if needed
6. Add tests in `web/tests/test_*.js` (create new test file if complex)

**Adding new form field type:**
1. Create export in `form/fields.js`: `createCustomField(name, label, value, options)`
2. Add HTML template with appropriate input type
3. Call `updateFieldValue()` on change to sync with `currentData`
4. Add tests in `web/tests/test_form_fields.js`

**Adding a new wizard step:**
1. Create `web/static/js/wizard/stepN.js` with `renderWizardStepN(container)` export
2. Expose step handler functions to `window` inside render function (see step3.js, step4.js as patterns)
3. Use inline `onclick="window.functionName()"` for all interactive elements
4. Call state mutations or form field handlers for updates
5. Add tests in `web/tests/test_wizard_steps_3_4_5.js` (consolidated test file)

**Adding API endpoint:**
1. Create route in `app.py` with Pydantic validation
2. Create async wrapper in `api.js` (error handling with console prefix like `[LOAD_ERROR]`)
3. Call from component: `import('./api.js').then(m => m.newFunction())`
4. Add tests in `web/tests/test_api.js`

### Testing

**Run tests:**
```bash
npx vitest                  # Watch mode
npx vitest run              # Single run with coverage
npx vitest web/tests/test_wizard_steps_3_4_5.js  # Specific file
```

**Test structure:**
- 9 test files in `web/tests/`: one per major module
- Use Vitest + jsdom for DOM testing
- Mock external dependencies: `vi.mock()` for modules, `vi.fn()` for functions
- Mock fetch calls: `global.fetch = vi.fn().mockResolvedValue(...)`
- Test exports (functions, not implementation)
- Use `beforeEach()` to reset DOM, mocks, state

**Test file mapping:**
| Test File | Covers | Test Count |
|-----------|--------|------------|
| `test_state.js` | State management, dirty tracking | 33 tests |
| `test_ui.js` | Toast, loading, dirty indicator | 23 tests |
| `test_api.js` | Load, save, export, validate | 17 tests |
| `test_templates.js` | Template loading, selection | 16 tests |
| `test_form_fields.js` | All field creators | 15 tests |
| `test_form_arrays.js` | Array add, remove, rerender | 11 tests |
| `test_wizard.js` | Wizard flow, mode switching | 16 tests |
| `test_expert_navigation.js` | Section navigation | 6 tests |
| `test_wizard_steps_3_4_5.js` | Steps 3, 4, 5 rendering & CRUD | 47 tests |
| **Total** | | **184 tests** |

**Test patterns:**
1. **Mocking modules:** Use `vi.mock()` to mock entire module; override specific exports if needed
2. **DOM testing:** Create elements with `document.createElement()`, append to body in `beforeEach()`, clean up in `afterEach()`
3. **Async testing:** Use `async/await`, mock `fetch()` or dynamic imports
4. **State isolation:** Call `state.resetXyz()` in `beforeEach()` to isolate tests
5. **Inline handlers:** Test via direct function call (handlers exposed to window are tested via DOM simulation)
6. **String array testing:** Create container with id `array-container-${fieldName}` to test array operations

**Example test:**
```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import * as arrays from '../form/arrays.js';

describe('Form Arrays Module', () => {
    beforeEach(() => {
        document.body.innerHTML = '';
        vi.clearAllMocks();
    });

    it('should add new item to array', () => {
        const container = document.createElement('div');
        container.id = 'array-container-cities';  // Pattern: array-container-${fieldName}
        document.body.appendChild(container);

        arrays.addArrayItem('cities');

        expect(container.children).toHaveLength(1);
        expect(container.querySelector('input')).toBeTruthy();
        expect(container.querySelector('button')).toBeTruthy();  // Remove button
    });
});
```

### Dependencies

**Web optional-dependencies** (installed with `uv sync --extra web`):
- `fastapi>=0.109.0` - Async web framework
- `uvicorn[standard]>=0.27.0` - ASGI server
- `pyyaml>=6.0` - YAML parsing/generation
- `python-multipart>=0.0.6` - Form data parsing

## Examples Reference

All in `examples/`:
- `babylon_civilization.py` - Scientific civ (full features)
- `babylon_civilization.yml` - YAML config (editable via web editor)
- `unlock_builder.py` - Unlock config


