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

Visual web interface for editing YAML civilization mod configurations. **The Wizard (guided mode) is the primary frontend**, designed to walk users through the mod creation process step-by-step. The "Expert Mode" (legacy) is available for direct access to all configuration sections but is considered an advanced/legacy feature.

Key Features:
- **Wizard-First Workflow**: Guided 5-step process for creating mods
- **AI Icon Generation**: Integrated OpenAI-powered generation for Civ/Unit/Building icons
- **Dark Theme UI**: Optimized for modding workflows with Tailwind CSS
- **No Build Step**: Native ES6 modules

### Architecture

```
Browser (Client) ←→ FastAPI REST API ←→ File System + Reference Data
    - ES6 Modules      - 15+ endpoints      - YAML load/save
    - Tailwind CSS     - OpenAI Integration - 33 JSON data files
    - HTMX             - Settings Config    - civ7_modding_tools/data
```

### File Organization (Modular)

**Frontend Structure (ES6 Modules):**

```
web/static/js/
├── main.js              # Entry point, exposes functions to window via Object.defineProperty()
├── state.js             # Global state + config objects (AUTOCOMPLETE_MAPPINGS, FIELD_HELP_TEXT)
├── api.js               # Backend communication (15+ functions for file ops, reference data)
├── ui.js                # Shared UI utilities (toast, loading, dirty indicator)
├── settings.js          # User preferences (OpenAI keys, export paths)
├── icons.js             # AI Icon generation with reference style selection
├── data/
│   └── loader.js        # Reference data loader with caching
├── wizard/              # PRIMARY UI - Guided 5-step workflow
│   ├── wizard.js        # Wizard flow engine: initializeMode(), switchMode(), navigation
│   ├── step1.js         # Metadata (mod ID, version, name), Module Localization, Starting Age
│   ├── step2.js         # Civ Core (type, traits, city names, icon), Localizations
│   ├── step3.js         # Units & Buildings with inline CRUD forms
│   ├── step4.js         # Modifiers & Traditions configuration
│   └── step5.js         # Review, validation summary, progression tree generation
├── expert/              # LEGACY / ADVANCED UI - 13 collapsible sections
│   ├── sections.js      # renderAllSections() + updateFieldValue() for dot-notation paths
│   ├── civilization.js  # 9 civ-specific sub-renderers (biases, unlocks, localizations, etc.)
│   └── navigation.js    # getAvailableSections() returns 13 section definitions
└── form/
    ├── fields.js        # Field creators with autocomplete (fuzzy search, usage tracking)
    ├── arrays.js        # Array CRUD: addArrayItem(), removeArrayItem(), rerenderArrayField()
    └── validation.js    # validateModData(), validateFieldBlur() with reference data checks
```

### Module Architecture & Patterns

**Event Handling Pattern (Critical):**
Interactive functions are exposed to `window` via `Object.defineProperty()` in `main.js` or through side-effects in their respective modules to support inline `onclick` handlers in dynamically rendered content.

**1. Main & State (main.js, state.js)**
- `main.js`: Initializes API, sets up file listeners, exposes 15+ functions to `window` via `Object.defineProperty()` including `switchMode`, `createNew`, `saveFile`, `exportYAML`, `exportBuiltMod`, and all icon/settings handlers.
- `state.js`: Central store for all application data. Exports mutable globals (`currentData`, `wizardData`, `isDirty`, `dataCache`), setter functions (`setCurrentData()`, `markDirty()`, etc.), and configuration objects (`AUTOCOMPLETE_MAPPINGS`, `FIELD_HELP_TEXT`, `REQUIRED_FIELDS`).

**2. Wizard (Primary Interface)**
- Located in `web/static/js/wizard/`.
- **Default Mode**: Application always initializes in Guided Mode.
- `wizard.js`: Manages step transitions and data synchronization.
- Steps 1-5: Modular renderers for each stage of the mod creation process.

**3. Expert Mode (Legacy/Advanced)**
- Located in `web/static/js/expert/`.
- Provides a collapsible list of all 13 configuration sections.
- Accessible via "Switch to Expert Mode" toggle, but secondary to the Wizard.

**4. Feature Modules**
- **Settings (`settings.js`)**: Manages local configuration (OpenAI API key, export paths).
- **Icons (`icons.js`)**: Handles prompts and API calls for generating icons via OpenAI.
- **API (`api.js`)**: Wrapper for all fetch calls to the FastAPI backend.

**5. Form System**
- `form/fields.js`: Renders individual input components (Text, Number, Boolean, Autocomplete with fuzzy search and localStorage usage tracking).
- `form/arrays.js`: Manages dynamic lists with container pattern `array-container-${fieldName}`, exposes functions to window via side-effect import.
- `form/validation.js`: Field and mod-level validation against reference data, shows inline error messages.

### REST API Endpoints

**File Operations:**
- `POST /api/civilization/load` - Load YAML from disk path
- `POST /api/civilization/save` - Save YAML to disk path
- `POST /api/civilization/upload` - Upload YAML file via form data
- `POST /api/civilization/export` - Export as downloadable YAML blob
- `POST /api/civilization/export-disk` - Save YAML to specified directory
- `POST /api/civilization/export-built` - Build mod and return as ZIP
- `POST /api/civilization/export-built-disk` - Build mod and save to directory
- `POST /api/civilization/validate` - Validate configuration structure

**Reference Data:**
- `GET /api/data/list` - List all 33 available data types
- `GET /api/data/{type}` - Get specific data (yield-types, effects, tags, etc.) with caching
- `POST /api/field/validate` - Validate field value against reference data

**Icon Generation:**
- `POST /api/icons/generate` - Generate icon via OpenAI with reference style matching
- `POST /api/icons/save` - Save generated icon to disk
- `POST /api/icons/upload` - Upload custom icon file

**Utility:**
- `GET /` - Serve main editor page
- `GET /api/health` - Health check
- `GET /docs` - Swagger UI (auto-generated by FastAPI)

### Development Workflow

**Visual Editing**:
1. Run `python web/run.py`
2. Open `http://127.0.0.1:8000`
3. Use the **Wizard** to create or edit modifications.

**Adding New Features**:
1. Prefer adding to **Wizard** steps (`web/static/js/wizard/`) over Expert mode strategies.
2. If adding global features (like AI tools), create new modules in `web/static/js/`.
3. Ensure all interactive elements use `window.functionName()` pattern for event handlers.

### Testing

**Run tests:**
```bash
npx vitest                  # Watch mode
npx vitest run              # Single run with coverage
npx vitest web/tests/test_wizard_steps_3_4_5.js  # Specific file
```

**Test structure:**
- 8 test files in `web/tests/`: one per major module
- Use Vitest + jsdom for DOM testing
- Mock external dependencies: `vi.mock()` for modules, `vi.fn()` for functions
- Mock fetch calls: `global.fetch = vi.fn().mockResolvedValue(...)`
- Test exports (functions, not implementation)
- Use `beforeEach()` to reset DOM, mocks, state

**Test file mapping:**
| Test File | Covers | Test Count |
|-----------|--------|------------|
| `test_state.js` | State management, dirty tracking | 46 tests |
| `test_ui.js` | Toast, loading, dirty indicator | 23 tests |
| `test_api.js` | Load, save, export, validate | 17 tests |
| `test_form_fields.js` | All field creators | 15 tests |
| `test_form_arrays.js` | Array add, remove, rerender | 11 tests |
| `test_wizard.js` | Wizard flow, mode switching | 16 tests |
| `test_expert_navigation.js` | Section navigation | 6 tests |
| `test_wizard_steps_3_4_5.js` | Steps 3, 4, 5 rendering & CRUD | 47 tests |
| **Total** | | **181 tests** |

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
- `openai>=1.0.0` - AI integration for icon generation
- `pillow>=10.0.0` - Image processing
- `requests>=2.31.0` - HTTP client
