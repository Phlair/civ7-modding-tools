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

## Examples Reference

All in `examples/`:
- `babylon_civilization.py` - Scientific civ (full features)
- `unit.py` - Simple unit
- `progression_tree.py` - Civics tree
- `unique_quarter.py` - Unique district
- `import_custom_icon.py` - Asset import
- `import_sql_file.py` - SQL integration
- `unlock_builder.py` - Unlock config


