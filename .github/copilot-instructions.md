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
- `gondor_civilization.py` - TypeScript parity test
- `unit.py` - Simple unit
- `progression_tree.py` - Civics tree
- `unique_quarter.py` - Unique district
- `import_custom_icon.py` - Asset import
- `import_sql_file.py` - SQL integration
- `unlock_builder.py` - Unlock config

## Attribution

Always credit original author:
> Original fork from [izica](https://github.com/izica)

```
build.py → Builders → Nodes → Files → mod.build() → .modinfo + XML
```

**Builders** (13 classes): CivilizationBuilder, UnitBuilder, ConstructibleBuilder, ProgressionTreeBuilder, ModifierBuilder, TraditionBuilder, UniqueQuarterBuilder, LeaderUnlockBuilder, CivilizationUnlockBuilder, ProgressionTreeNodeBuilder, UnlockBuilder, ImportFileBuilder

**Nodes**: Python classes that serialize to XML elements (snake_case props → PascalCase attributes)

**Files**: XmlFile (uses xmltodict), ImportFile (copies external assets)

## Project Structure

```
src/civ7_modding_tools/
├── core/mod.py            # Mod class (orchestrator)
├── builders/builders.py   # All 13 builder classes
├── nodes/                 # BaseNode + 78 specialized nodes
├── files/__init__.py      # BaseFile, XmlFile, ImportFile
├── localizations/__init__.py  # 11 pydantic localization classes
├── constants/__init__.py  # 21 Enum classes (Trait, UnitClass, Age, Effect, etc.)
├── utils/__init__.py      # locale(), trim(), kebab_case(), fill(), etc.
└── xml_builder.py         # XML generation utilities

tests/                     # 12 test files
examples/                  # gondor_civilization.py + 7 others
docs/                      # INDEX.md, GUIDE.md, API.md, EXAMPLES.md
```

## Core Usage

```python
from civ7_modding_tools import Mod, CivilizationBuilder, Trait

mod = Mod(id='my-mod', version='1.0', name='My Mod')

civ = CivilizationBuilder({
    'civilization': {'civilization_type': 'CIVILIZATION_CUSTOM'},
    'civilization_traits': [Trait.ECONOMIC],
    'localizations': [{'name': 'Custom Civ', 'city_names': ['Capital']}]
})

mod.add(civ)
mod.build('./dist')  # Generates .modinfo + XML files
```

## Key Concepts

### Mod Class
- Constructor: `Mod(id, version, name, description, authors, affects_saved_games)`
- Methods: `add(builder|list)`, `add_files(file|list)`, `build(dist, clear=True)`
- Auto-generates ActionCriteria and ActionGroup elements

### Builders
- Extend `BaseBuilder` (abstract)
- Constructor accepts dict or use `fill(payload)` method
- All have `action_group_bundle` property (controls age loading)
- Implement `build() -> list[BaseFile]`

### ActionGroupBundle
- Controls when content loads (e.g., specific ages)
- Not exported in package - use `action_group_bundle` property on builders
- Ages: ALWAYS, AGE_ANTIQUITY, AGE_EXPLORATION, etc.

### Nodes
- Extend `BaseNode` with `_name` class variable
- Properties convert to XML: `civilization_type` → `CivilizationType="..."`
- Booleans → "true"/"false" strings
- `None` values omitted from output
- Method: `to_xml_element() -> dict | None`

### Localizations
- Pydantic BaseModel subclasses
- One per builder type: CivilizationLocalization, UnitLocalization, etc.
- Method: `get_nodes(entity_id) -> list[dict]`

### Constants (Enums)
21 Enum classes including:
- `Trait`: ECONOMIC, CULTURAL, MILITARY, DIPLOMATIC, SCIENTIFIC, RELIGIOUS
- `UnitClass`: MELEE, RANGED, SUPPORT, RECON, HEAVY_CAVALRY, etc.
- `Age`: ANTIQUITY, CLASSICAL, MEDIEVAL, RENAISSANCE, etc.
- `Effect`: Game modifiers (e.g., UNIT_ADJUST_MOVEMENT)
- `Requirement`: Game conditions
- `Yield`: PRODUCTION, GOLD, CULTURE, SCIENCE, FAITH, etc.
- `District`: COMMERCIAL_HUB, HOLY_SITE, CAMPUS, etc.

### Utils
- `locale(prefix, variable)`: Generate LOC_PREFIX_VARIABLE keys
- `trim(s)`: Remove CIVILIZATION_, UNIT_, BUILDING_ prefixes
- `kebab_case(s)`: Convert to kebab-case for paths
- `fill(obj, payload)`: Set properties from dict
- `without(lst, *values)`: Filter list
- `uniq_by(lst, key_func)`: Deduplicate by key

### Path Generation
Two-step process:
1. `trim("CIVILIZATION_GONDOR")` → `"GONDOR"`
2. `kebab_case("GONDOR")` → `"gondor"`

Result: `/civilizations/gondor/`

Examples:
- `UNIT_GONDOR_SCOUT` → `/units/gondor-scout/`
- `BUILDING_GONDOR2` → `/constructibles/gondor2/`

### File Naming
Standard names: `always.xml`, `current.xml`, `game-effects.xml`, `icons.xml`, `localization.xml`, `legacy.xml`, `shell.xml`, `visual-remap.xml`, `unlocks.xml`

ImportFileBuilder uses `target_name` parameter for output filename.

## Code Conventions

- **Language**: British English
- **Style**: PEP 8, 4-space indent, max 100 chars/line
- **Naming**: PascalCase (classes), snake_case (functions/vars), UPPER_SNAKE_CASE (constants)
- **Types**: Full type hints with pydantic models
- **Docstrings**: PEP 257

## Common Patterns

### Builder pattern
```python
# Constructor with dict
builder = CivilizationBuilder({
    'civilization': {'civilization_type': 'CIV_ROME'},
    'civilization_traits': [Trait.MILITARY]
})

# Or fill() method
builder = CivilizationBuilder().fill({...})
```

### Multiple entities
```python
mod.add([unit1, unit2, building1])
```

### Constants over strings
```python
from civ7_modding_tools import Trait, UnitClass, Effect

builder.fill({
    'civilization_traits': [Trait.ECONOMIC, Trait.MILITARY],
    'unit_class': UnitClass.MELEE,
    'effect': Effect.UNIT_ADJUST_MOVEMENT
})
```

## Development Workflow

```bash
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run pytest --cov        # With coverage
uv run mypy src/           # Type checking (optional)
```

## Adding Features

### New Builder
1. Add class in `builders/builders.py` extending `BaseBuilder`
2. Implement `build() -> list[BaseFile]`
3. Create corresponding localization in `localizations/__init__.py`
4. Export from `builders/__init__.py`

### New Node
1. Add class in `nodes/nodes.py` extending `BaseNode`
2. Set `_name` class variable
3. Export from `nodes/__init__.py`

### New Constant
1. Add Enum class in `constants/__init__.py`
2. Values inherit from `str, Enum`

## Implementation Details

- **XML**: Uses `xmltodict.unparse()` with `pretty=True`, 4-space indent
- **Action Groups**: Mod auto-extracts criteria, generates ActionCriteria/ActionGroup elements
- **Performance**: Mod generation <100ms, test suite <1s
- **Dependencies**: pydantic, xmltodict, pytest, pytest-cov

## Rate Limiting & Tool Usage Guidelines

### Tool Call Patterns to Avoid

**❌ DO NOT** parallelize expensive search operations:
- Never run multiple `semantic_search` calls simultaneously
- Never run multiple `grep_search` calls in parallel  
- Never batch multiple search tools together

**✓ DO** run lightweight operations in parallel:
- Multiple `read_file` calls can be parallelized (they're local)
- `list_dir` calls are safe to parallelize
- `copilot_getNotebookSummary` calls can be parallelized

### Rate-Limiting Best Practices

1. **Sequential search operations**: Run one semantic_search or grep_search at a time
2. **No over-searching**: If initial search doesn't yield results, refine query rather than running additional searches
3. **Context throttling**: Read large file sections (100+ lines) instead of making multiple small reads
4. **Backoff strategy**: If a search feels expensive, wait for results before launching next tool call
5. **Bounds on thoroughness**: "Gather context as needed" has implicit limits—stop after 2-3 searches if not finding target

### When to Stop Searching

- Initial semantic_search found relevant results → use those, don't search again
- grep_search with specific pattern matched → proceed with next step
- File found via file_search → read it, don't search for alternatives
- After 2-3 failed searches → ask user for clarification instead of continuing searches

## Resources

- **Docs**: `docs/INDEX.md`, `docs/GUIDE.md`, `docs/API.md`, `docs/EXAMPLES.md`
- **GitHub**: https://github.com/Phlair/civ7-modding-tools
- **Python Instructions**: `.github/instructions/python.instructions.md`

