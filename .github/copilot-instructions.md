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

### Architecture

```
Browser (Client) ←→ FastAPI REST API ←→ File System + Reference Data
  - Tailwind CSS     - 8 endpoints        - YAML load/save
  - Vanilla JS       - Pydantic validation - 33 JSON data files
  - HTMX structure   - Caching system     - civ7_modding_tools/data
```

### Key Files

| Path | Purpose |
|------|---------|
| `web/app.py` | FastAPI backend, 8 REST endpoints, validation, caching |
| `web/run.py` | Development server launcher |
| `web/templates/index.html` | Main UI, 13 color-coded sections, sticky header |
| `web/templates/components.html` | 10 reusable form component templates |
| `web/static/js/editor.js` | Form management, YAML load/save, state tracking |
| `web/static/css/styles.css` | Tailwind extensions, animations, dark theme |

### REST API Endpoints

**File Operations:**
- `POST /api/civilization/load` - Load YAML, returns parsed data
- `POST /api/civilization/save` - Persist edited YAML to disk
- `POST /api/civilization/validate` - Validate configuration structure

**Reference Data:**
- `GET /api/data/{type}` - Get specific data (yield-types, effects, tags, etc.) with caching
- `GET /api/data/list` - List all 33 available data types
- `POST /api/field/validate` - Validate field value against reference data

**Utility:**
- `GET /api/health` - Health check
- `GET /docs` - Swagger UI (auto-generated)

### Running the Editor

```bash
# Install dependencies
uv sync --extra web

# Start server
python web/run.py
# Server runs at http://127.0.0.1:8000
# Auto-reloads on file changes
```

### Features

- **13 Collapsible Sections**: Metadata, civilization, units, buildings, modifiers, traditions, progressions, etc.
- **Color-Coded Navigation**: 13 unique colors for quick section identification
- **Dirty State Tracking** (Option C): Hybrid auto-detect + explicit save, prevents accidental loss
- **Real-Time Validation**: Against required fields, types, and reference data enums
- **Reference Data Integration**: Autocomplete dropdowns fetching from `/api/data/*`
- **Form Components**: Text, number, boolean, autocomplete selects, string arrays, nested objects
- **Dark Theme UI**: Optimized for modding workflows with Tailwind CSS
- **Single File Mode**: One YAML file at a time (multi-file tabs planned for future)
- **Export**: Download edited YAML to browser

### Form Field Types

| Type | Validation | Source |
|------|-----------|--------|
| Text Input | String type | User input |
| Number Input | Integer/float type | User input |
| Boolean Toggle | True/false | User input |
| Autocomplete Select | Enum validation | `/api/data/{type}` |
| String Array | Type validation per item | User input |
| Nested Objects | Type validation per property | User input |

### Validation Architecture

1. **Client-Side** (editor.js)
   - Real-time field type checking
   - Visual error display on blur/change
   - Dirty state management

2. **Server-Side** (app.py)
   - Pydantic model validation
   - Required field checks
   - Structure validation
   - Error/warning severity levels

3. **Reference Data** (JSON files)
   - Enum validation against game constants
   - Consistency checking
   - Autocomplete suggestions

### State Management

**Global State:**
```javascript
currentData = {}           // Parsed YAML object
currentFilePath = ""       // Current file path
isDirty = false            // Unsaved changes flag
dataCache = {}             // Reference data cache
```

**Dirty State (Option C):**
- Automatically set on any field change
- Visible in header as amber "Unsaved changes" indicator
- Save button only enabled when dirty
- Reset after successful save
- Prevents accidental saves

### Dependencies

**Web optional-dependencies** (installed with `uv sync --extra web`):
- `fastapi>=0.109.0` - Async web framework
- `uvicorn[standard]>=0.27.0` - ASGI server
- `pyyaml>=6.0` - YAML parsing/generation
- `python-multipart>=0.0.6` - Form data parsing

### Development

**Adding a new section:**
1. Add to sidebar in `index.html`
2. Create renderer function in `editor.js`
3. Form fields auto-update `currentData` on change

**Adding new form field type:**
1. Create component template in `components.html`
2. Add case in `createFormField()` in `editor.js`
3. Add styling to `styles.css` if needed

**Adding API endpoint:**
1. Create route in `app.py`
2. Use Pydantic models for requests/responses
3. Auto-documented at `/docs`

**Testing endpoints:**
```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/data/list
curl http://127.0.0.1:8000/api/data/yield-types
```

## Examples Reference

All in `examples/`:
- `babylon_civilization.py` - Scientific civ (full features)
- `babylon_civilization.yml` - YAML config (editable via web editor)
- `unlock_builder.py` - Unlock config


