# Civ7 Modding Tools - Copilot Instructions

## Project Overview

Python library for programmatically generating Civilization 7 mods. Uses builders to create XML/modinfo files from type-safe Python code.

- **Version**: 1.3.0
- **Python**: 3.12+
- **Package Manager**: uv

## Architecture

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

