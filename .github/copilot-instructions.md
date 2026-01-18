# Civ7 Modding Tools - Copilot Instructions

## Project Overview

**Civ7 Modding Tools** is a Python code generation library for creating Civilization 7 mods. It provides strongly-typed builders and nodes that abstract the complexity of manual XML/mod file creation, allowing developers to programmatically generate complete mod packages with civilizations, units, buildings, progression trees, and other game entities.

**Status**: ✅ Python implementation achieves 100% parity with TypeScript (v1.3.0), with identical file structure, naming, and output format.

- **Repository**: https://github.com/Phlair/civ7-modding-tools
- **License**: MIT
- **Python Version**: 3.12+
- **Package Manager**: uv
- **Latest Version**: 2.0.0-py (March 2025)

## Architecture Overview

The project follows a **builder pattern** for mod generation:

```
User Code (build.py)
    ↓
Builders (CivilizationBuilder, UnitBuilder, etc.)
    ↓
Nodes (CivilizationNode, UnitNode, etc.) - XML element representations
    ↓
Files (XmlFile, ImportFile) - Physical output files
    ↓
Mod.build() → generates .modinfo + XML files to disk
```

### Key Design Principles

1. **Type Safety**: Full Python type hints with pydantic models
2. **Builder Pattern**: Fluent API for constructing mod entities with `fill()` method
3. **Separation of Concerns**: Builders create files, nodes represent XML elements, files write to disk
4. **Modular Constants**: Game-specific constants (TRAIT, UNIT_CLASS, EFFECT, etc.) as Enum classes for type-safe references
5. **Localization Support**: Built-in localization system for multi-language text

## Directory Structure

```
civ7-modding-tools/
├── src/civ7_modding_tools/
│   ├── core/
│   │   ├── mod.py              # Main orchestrator class
│   │   ├── action_groups.py    # Action group bundling for game ages
│   │   └── __init__.py
│   │
│   ├── builders/
│   │   ├── builders.py         # All builder implementations (13 classes)
│   │   └── __init__.py
│   │
│   ├── nodes/
│   │   ├── base.py             # Abstract base node (converts to XML)
│   │   ├── nodes.py            # Basic node types
│   │   ├── database.py         # DatabaseNode (master container)
│   │   ├── action_groups.py    # ActionGroup nodes
│   │   └── __init__.py
│   │
│   ├── files/
│   │   ├── __init__.py         # BaseFile, XmlFile, ImportFile classes
│   │
│   ├── localizations/
│   │   ├── __init__.py         # All localization classes (11 types)
│   │
│   ├── constants/
│   │   ├── __init__.py         # 24 Enum classes with 182 values
│   │
│   ├── utils/
│   │   ├── __init__.py         # Utility functions (fill, without, uniq_by, etc.)
│   │
│   └── __init__.py             # Main export barrel
│
├── tests/
│   ├── test_builders.py
│   ├── test_files.py
│   ├── test_nodes.py
│   ├── test_localizations_*.py
│   ├── test_constants_*.py
│   ├── test_mod.py
│   ├── test_utils.py
│   ├── test_integration_e2e.py
│   └── ... (12+ test files, 324 total tests)
│
├── examples/
│   ├── gondor_civilization.py   # Full parity test example (matches build.ts exactly)
│   ├── civilization.py         # Full civilization example
│   ├── unit.py
│   ├── progression_tree.py
│   ├── unique_quarter.py
│   ├── unlock_builder.py
│   ├── import_sql_file.py
│   └── import_custom_icon.py
│
├── docs/
│   ├── INDEX.md               # Documentation navigation hub
│   ├── GUIDE.md               # Getting started tutorial
│   ├── API.md                 # Complete API reference
│   ├── EXAMPLES.md            # 7 practical examples
│   └── MIGRATION.md           # TypeScript to Python guide (for reference)
│
├── pyproject.toml            # Project configuration
├── README.md
├── CHANGELOG.md
├── LICENSE
└── .github/
    └── instructions/
        └── python.instructions.md
```

## Core Concepts

### 1. The Mod Class

The root orchestrator for mod creation:

```python
from civ7_modding_tools import Mod, CivilizationBuilder

mod = Mod(
    id='my-mod',
    version='1.0',
    name='My Civilization 7 Mod',
    description='Custom mod description',
    authors='Your Name',
    affects_saved_games=True
)

# Add builders
mod.add(civilization_builder)
mod.add([unit_builder1, unit_builder2])
mod.add_files(import_file_builder)

# Generate output
mod.build('./dist')  # Generates .modinfo + XML files to ./dist
```

**Key Methods**:
- `add(builder: BaseBuilder | list[BaseBuilder]) -> Mod`: Register builders
- `add_files(file: BaseFile | list[BaseFile]) -> Mod`: Register import files
- `build(dist: str, clear: bool = True) -> None`: Generate mod files to disk

### 2. Builders (Abstract Factory Pattern)

All builders extend `BaseBuilder` and implement the builder pattern:

```python
from abc import ABC, abstractmethod
from civ7_modding_tools.builders.builders import BaseBuilder
from civ7_modding_tools.files import BaseFile
from civ7_modding_tools.core import ActionGroupBundle

class BaseBuilder(ABC):
    def __init__(self) -> None:
        self.action_group_bundle: ActionGroupBundle = ActionGroupBundle()
        
    def fill(self, payload: dict[str, Any]) -> "BaseBuilder":
        """Populate properties and return self for chaining"""
        
    def build(self) -> list[BaseFile]:
        """Generate output files (implemented by subclasses)"""
```

**Key Builders** (13 total):
- **CivilizationBuilder**: Full civilization with traits, tags, unlocks, start biases
- **UnitBuilder**: Unit definition with stats, costs, abilities
- **ConstructibleBuilder**: Buildings, improvements, quarters with yield/maintenance
- **UniqueQuarterBuilder**: District-specific buildings
- **ProgressionTreeBuilder**: Tech/civics trees with nodes, prerequisites
- **ModifierBuilder**: Game effects applied to collections
- **TraditionBuilder**: Cultural traditions with modifiers
- **UnlockBuilder**: Generic unlock configurations
- **LeaderUnlockBuilder**: Leader-civilization pairings
- **CivilizationUnlockBuilder**: Age-based civilization progressions
- **ImportFileBuilder**: Import/copy external files
- Plus 2 additional specialized builders

### 3. Nodes (XML Element Representation)

Nodes represent XML elements. All extend `BaseNode`:

```python
from abc import abstractmethod
from civ7_modding_tools.nodes.base import BaseNode

class BaseNode(ABC):
    _name: str = 'Row'
    
    def fill(self, payload: dict[str, Any]) -> "BaseNode":
        """Set node properties"""
        
    def to_xml_element(self) -> dict | None:
        """Convert node to XML element dictionary"""
        
    def insert_or_ignore(self) -> "BaseNode":
        """Transform to INSERT OR IGNORE statement"""
```

Node properties become XML attributes via snake_case → PascalCase conversion:
```python
from civ7_modding_tools.nodes import CivilizationNode

node = CivilizationNode(
    civilization_type='CIVILIZATION_ROME',
    base_tourism=10,
    legacy_modifier=True  # becomes LegacyModifier="true" in XML
)
```

**Node Categories** (78 total):
- **Entity Nodes**: CivilizationNode, UnitNode, ConstructibleNode, LeaderUnlockNode, etc.
- **Stat/Config Nodes**: UnitStatNode, UnitCostNode, ConstructibleYieldChangeNode, etc.
- **Requirement Nodes**: RequirementNode, RequirementSetNode, RequirementArgumentNode
- **Modifier Nodes**: ModifierNode, GameModifierNode, TraitModifierNode
- **Game Effect Nodes**: GameEffectNode, AdjacencyYieldChangeNode
- **Localization Nodes**: LocalizationNode, CityNameNode
- **Progression Nodes**: ProgressionTreeNode, ProgressionTreeNodeNode
- **Database Node**: DatabaseNode (master container with 67 properties)

### 4. Files (Output Generation)

Files represent physical outputs:

```python
from abc import ABC, abstractmethod
from civ7_modding_tools.files import BaseFile

class BaseFile(ABC):
    path: str = "/"              # Directory path
    name: str = "file.txt"       # Filename
    content: Any = None          # Content (nodes, dicts, etc)
    action_groups: list[str] = []
    action_group_actions: list[str] = []
    
    @abstractmethod
    def write(self, dist: str) -> None:
        """Write this file to disk"""
        
    @property
    def is_empty(self) -> bool:
        """Check if file should be written"""
        
    @property
    def mod_info_path(self) -> str:
        """Path for .modinfo reference"""
```

**File Types**:
- **XmlFile**: XML file generation for Civ7 mod files (uses xmltodict)
- **ImportFile**: Import handler for images, SQL, custom files

### 5. Action Groups & Criteria

Mods use action groups to scope content loading:

```python
from civ7_modding_tools import UnitBuilder, ACTION_GROUP_BUNDLE

unit = UnitBuilder(
    action_group_bundle=ACTION_GROUP_BUNDLE.AGE_EXPLORATION,
    unit={...}
)
```

This links content to specific ages:
- `ACTION_GROUP_BUNDLE.ALWAYS` → Always loaded
- `ACTION_GROUP_BUNDLE.AGE_ANTIQUITY` → Ancient age
- `ACTION_GROUP_BUNDLE.AGE_EXPLORATION` → Classical age
- Plus 7 additional age options

## Localization System

Localizations provide multi-language support using pydantic:

```python
from civ7_modding_tools import CivilizationBuilder

civilization = CivilizationBuilder(
    localizations=[
        {
            'name': 'Rome',
            'description': 'Ancient empire',
            'full_name': 'The Roman Empire',
            'adjective': 'Roman',
            'city_names': ['Rome', 'Milan', 'Venice']
        }
    ]
)
```

Each builder type has a corresponding localization class (pydantic BaseModel).

## Workflow

### Development Workflow

```bash
# Setup environment
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/civ7_modding_tools

# Type checking (optional)
uv run mypy src/

# Format code (optional)
uv run black src/ tests/
```

### Creating a Mod

1. **Initialize Mod**:
   ```python
   from civ7_modding_tools import Mod
   
   mod = Mod(
       id='my-custom-mod',
       version='1.0'
   )
   ```

2. **Create Builders**:
   ```python
   from civ7_modding_tools import (
       CivilizationBuilder,
       ACTION_GROUP_BUNDLE,
       TRAIT
   )
   
   civilization = CivilizationBuilder(
       action_group_bundle=ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
       civilization={'civilization_type': 'CIVILIZATION_CUSTOM', ...},
       civilization_traits=[TRAIT.ECONOMIC_CIV, ...],
       localizations=[{'name': 'Custom Civ', ...}]
   )
   ```

3. **Register Builders**:
   ```python
   mod.add(civilization)
   mod.add([unit_builder1, unit_builder2])
   ```

4. **Build Output**:
   ```python
   mod.build('./dist')  # Generates /dist/mod-test.modinfo + XML files
   ```

5. **Output Structure**:
   ```
   dist/
   ├── mod-test.modinfo           # Mod metadata
   ├── civilizations/custom/
   │   ├── current.xml
   │   ├── unlocks.xml
   │   ├── legacy.xml
   │   └── icons.xml
   ├── units/
   ├── constructibles/
   ├── progression-trees/
   └── imports/
   ```

## Code Conventions

### Python

- **Language**: Python 3.12+
- **Type Hints**: Full type annotations using `typing` module
- **Style**: PEP 8 compliant, 4-space indentation
- **Line Length**: Max 100 characters
- **Docstrings**: PEP 257 convention

### Naming Conventions

- **Classes**: PascalCase (CivilizationBuilder, BaseNode)
- **Functions/Methods**: snake_case (build_civilization, civilization_type)
- **Constants**: UPPER_SNAKE_CASE (TRAIT.ECONOMIC_CIV, UNIT_CLASS.RECON)
- **Private Methods**: Leading underscore (_get_attributes)
- **File Paths**: kebab-case with trimmed IDs (`civilizations/gondor/`, `units/gondor-scout/`)
- **File Names**: Standardized (`always.xml`, `current.xml`, `game-effects.xml`, `icons.xml`, `localization.xml`)

### Builder Pattern Usage

All builders follow the fluent builder pattern:

```python
from civ7_modding_tools import CivilizationBuilder, ACTION_GROUP_BUNDLE

# Method 1: Constructor with dict
builder = CivilizationBuilder(
    action_group_bundle=ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
    civilization={'civilization_type': 'CIV_ROME'}
)

# Method 2: Using fill() method
builder = CivilizationBuilder()
builder.fill({
    'action_group_bundle': ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
    'civilization': {'civilization_type': 'CIV_ROME'}
})
```

### Constants Usage

Constants are organized by game concept as Enum classes:

```python
from civ7_modding_tools import (
    TRAIT,              # Civilization traits
    UNIT_CLASS,         # Unit classifications
    EFFECT,             # Game effects
    REQUIREMENT,        # Game conditions
    YIELD,              # Resource yields
    ACTION_GROUP_BUNDLE,  # Age groupings
    AGE                 # Game ages
)

# Use constants instead of magic strings
builder.fill({
    'civilization_traits': [TRAIT.ECONOMIC_CIV, TRAIT.MILITARY_CIV],
    'unit_class': UNIT_CLASS.MELEE,
    'effect': EFFECT.UNIT_ADJUST_MOVEMENT
})
```

### Node Serialization

Nodes convert to XML via `to_xml_element()`:

```python
from civ7_modding_tools.nodes import CivilizationNode

# Python
node = CivilizationNode(
    civilization_type='CIVILIZATION_ROME',
    base_tourism=10,
    legacy_modifier=True
)

# Generated XML attribute
# <Row CivilizationType="CIVILIZATION_ROME" BaseTourism="10" LegacyModifier="true"/>
```

Property conversion rules:
- snake_case → PascalCase
- `bool` → "true" / "false" (string)
- `None` → omitted from output
- All other types → stringified

## Adding New Features

### Adding a New Builder

1. **Add to** `src/civ7_modding_tools/builders/builders.py`:
   ```python
   from civ7_modding_tools.builders.builders import BaseBuilder
   from civ7_modding_tools.files import XmlFile, BaseFile
   
   class MyBuilder(BaseBuilder):
       my_property: str = 'default'
       
       def build(self) -> list[BaseFile]:
           """Generate output files"""
           file = XmlFile(
               path='/my-path/',
               name='my-file.xml',
               content={...}  # nodes here
           )
           return [file]
   ```

2. **Create Localization in** `src/civ7_modding_tools/localizations/__init__.py`:
   ```python
   from pydantic import BaseModel
   
   class MyLocalization(BaseModel):
       name: str = ''
       my_localized_field: str = ''
   ```

3. **Update** `src/civ7_modding_tools/builders/__init__.py` to export the builder

4. **Use in build.py**:
   ```python
   from civ7_modding_tools import MyBuilder
   
   my_builder = MyBuilder(
       my_property='value',
       localizations=[{'name': 'My Item', 'my_localized_field': 'Text'}]
   )
   mod.add(my_builder)
   ```

### Adding New Nodes

1. **Add to** `src/civ7_modding_tools/nodes/nodes.py`:
   ```python
   from civ7_modding_tools.nodes.base import BaseNode
   
   class MyNode(BaseNode):
       _name: str = 'MyElement'
       my_attribute: str = ''
       my_number: int = 0
   ```

2. **Export from** `src/civ7_modding_tools/nodes/__init__.py`

3. **Use in Builders**:
   ```python
   from civ7_modding_tools.nodes import MyNode
   
   # In builder's build() method
   node = MyNode(my_attribute='value')
   ```

### Adding New Constants

1. **Add to** `src/civ7_modding_tools/constants/__init__.py`:
   ```python
   from enum import Enum
   
   class MY_CONSTANT(str, Enum):
       VALUE_ONE = 'VALUE_ONE'
       VALUE_TWO = 'VALUE_TWO'
       VALUE_THREE = 'VALUE_THREE'
   ```

2. **Use in code**:
   ```python
   from civ7_modding_tools import MY_CONSTANT
   
   builder.fill({'my_property': MY_CONSTANT.VALUE_ONE})
   ```

## Key Implementation Details

### XML Generation

Uses `xmltodict` library for XML serialization:

```python
from xmltodict import unparse

xml_str = unparse(
    content,
    pretty=True,
    full_document=True
)
```

Output includes XML declaration and pretty-printing with 4-space indentation.

### Action Group Management

The `Mod` class automatically:
1. Extracts unique criteria from all builders
2. Creates ActionCriteria elements in .modinfo
3. Groups files by action group ID
4. Generates ActionGroup elements with appropriate Actions

This allows content to be conditionally loaded based on game state (age, technology, etc).

### Type System

Full Python type hints with pydantic models:

```python
from typing import Any, Dict, List, Optional, Union, TypeVar, Callable
from pydantic import BaseModel

T = TypeVar("T")

def fill(obj: T, payload: Dict[str, Any]) -> T:
    """Generic fill function preserving input type"""
    ...

def without(lst: List[T], *values: T) -> List[T]:
    """Type-safe list filtering"""
    ...

def uniq_by(lst: List[T], key_func: Callable[[T], Any] | None = None) -> List[T]:
    """Type-safe uniqueness with optional key function"""
    ...
```

## Testing & Quality

### Running Tests

```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_builders.py

# With coverage
uv run pytest --cov=src/civ7_modding_tools --cov-report=html

# Quick run (quiet)
uv run pytest -q
```

### Coverage

- **Target**: 90%+
- **Current**: 94% (324/324 tests passing)
- **Report**: `htmlcov/index.html`

### Output Validation

Generated mods produce:
1. `.modinfo` file with proper XML structure, criteria, action groups
2. Organized XML files in expected directories
3. Imported assets in the `imports/` directory

Validate against Civilization 7 mod format documentation.

## Project Structure Best Practices

### For Custom Mods Using Library

```python
# build.py - Main mod entry point
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ACTION_GROUP_BUNDLE,
    TRAIT,
    UNIT_CLASS,
)

mod = Mod(
    id='my-mod',
    version='1.0',
    name='My Mod'
)

# Define builders
civilization = CivilizationBuilder({...})
mod.add(civilization)

# Build
mod.build('./dist')
```

### Project Layout

```
my-civ7-mod/
├── build.py              # Main build script
├── assets/               # Images, SQL files for import
│   ├── civ-icon.png
│   └── units-data.sql
├── dist/                 # Generated mod output
├── pyproject.toml        # Project config
└── requirements.txt      # Dependencies (if not using uv)
```

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for version history.

Current version: 2.0.0-py (Python port with full TypeScript parity)
Reference: 1.3.0 (TypeScript - API compatibility baseline)

Notable versions:
- **2.0.0-py**: Python port with 100% output parity (2025-03-20)
  - Identical file generation to TypeScript v1.3.0
  - 22 files generated for gondor example (matches TS exactly)
  - Path generation: kebab-case with trimmed IDs
  - Import file naming: Uses target_name from ImportFileBuilder
  - All 13 builders fully implemented and tested
- **1.3.0**: TypeScript reference implementation (2025-03-15)

## Performance Considerations

- Builders are lightweight; performance bottleneck is file I/O
- Node serialization is lazy (only via to_xml_element())
- Typical mod generation: <100ms
- Large mods with 100+ entities generate quickly
- Test suite (324 tests) executes in <1 second

## Path Generation & File Naming

### Path Generation with trim() and kebab_case()

All builders use a two-step process for generating file paths:

```python
from civ7_modding_tools.utils import trim, kebab_case

# Step 1: Remove prefixes (CIVILIZATION_, UNIT_, BUILDING_, etc.)
trimmed = trim("CIVILIZATION_GONDOR")  # "GONDOR"

# Step 2: Convert to kebab-case
path_segment = kebab_case(trimmed)  # "gondor"

# Result in file path
path = f"/civilizations/{path_segment}/"  # "/civilizations/gondor/"
```

Examples:
- `CIVILIZATION_GONDOR` → `gondor` (civilization path)
- `UNIT_GONDOR_SCOUT` → `gondor-scout` (unit path)
- `BUILDING_GONDOR2` → `gondor2` (constructible path)
- `TREE_CIVICS_GONDOR` → `civics-gondor` (progression tree path)

### File Naming Convention

Builders generate XML files with standardized names:
- `always.xml` - Core entity data (constructibles, buildings)
- `current.xml` - Main progression tree or core content
- `game-effects.xml` - Game modifiers and effects
- `icons.xml` - Icon asset definitions
- `localization.xml` - Localization data
- `legacy.xml` - Legacy game data
- `shell.xml` - Shell/framework data
- `visual-remap.xml` - Visual remapping (units)
- `unlocks.xml` - Unlock data (civilizations)

### ImportFileBuilder File Naming

Import files use `target_name` parameter for output filename:

```python
import_file = ImportFileBuilder()
import_file.fill({
    'source_path': './assets/civ-icon.png',
    'target_name': 'civ_sym_gondor'  # Output filename in imports/
})
```

Result: `imports/civ_sym_gondor` (not `imports/civ-icon.png`)

## Common Patterns

### Conditional Content

```python
# Load content in specific ages
unit = UnitBuilder(
    action_group_bundle=ACTION_GROUP_BUNDLE.AGE_EXPLORATION,
    # Loaded only in Exploration age
    ...
)
```

### Multiple Units/Buildings

```python
units = [
    UnitBuilder({...}),
    UnitBuilder({...}),
    UnitBuilder({...})
]
mod.add(units)
```

### Requirements and Effects

```python
from civ7_modding_tools import (
    ModifierBuilder,
    COLLECTION,
    EFFECT,
    REQUIREMENT,
    UNIT_CLASS
)

modifier = ModifierBuilder(
    collection=COLLECTION.PLAYER_UNITS,
    effect=EFFECT.UNIT_ADJUST_MOVEMENT,
    requirements=[{
        'type': REQUIREMENT.UNIT_TAG_MATCHES,
        'arguments': [{'name': 'Tag', 'value': UNIT_CLASS.RECON}]
    }],
    arguments=[{'name': 'Amount', 'value': 2}]
)
```

## External Dependencies

- **pydantic** (2.x): Data validation and models
- **xmltodict**: XML serialization
- **pytest**: Testing framework
- **pytest-cov**: Coverage measurement
- **mypy**: Optional type checking
- **black**: Optional code formatting

## Troubleshooting

### ModInfo not generating

Ensure `mod.build()` is called after all builders are added:
```python
mod.add(builders)
mod.build('./dist')  # Don't forget!
```

### Missing localization

Ensure localization objects have required fields matching the builder expectations. Check the corresponding Localization class definition.

### XML attribute not appearing

Properties that are `None`, empty string, or falsy are omitted. Verify property is set to a valid value.

### Import file not copied

ImportFileBuilder content must be a valid file path (e.g., `'./assets/icon.png'`). File is read and written to `imports/` directory.

## Resources

- **GitHub**: https://github.com/Phlair/civ7-modding-tools
- **Documentation**: See `docs/INDEX.md`
- **Getting Started**: See `docs/GUIDE.md`
- **API Reference**: See `docs/API.md`
- **Examples**: See `docs/EXAMPLES.md`
- **Civilization 7 Modding**: https://civilization.fandom.com/wiki/Modding

## Language

- Use **British English** in code comments and documentation

## Design Philosophy

This library prioritizes:

1. **Type Safety**: Catch errors at development time via Python type hints
2. **Discoverability**: IDE autocomplete guides users through available options
3. **Abstraction**: Hide XML complexity behind intuitive builders
4. **Flexibility**: Low-level node access for advanced use cases
5. **Extensibility**: Easy to add new builders, nodes, constants
6. **Testability**: Comprehensive test suite (324 tests, 94% coverage)
7. **Documentation**: Extensive guides and examples for all user levels

