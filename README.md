# Phlair's Civ VII Modding Tools

A Python library for programmatically generating Civilization VII mods using type-safe builders and automatic XML generation.

> **Attribution**: This project is a complete rework of the original codebase. Original fork from [izica](https://github.com/izica).

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Build complete Civilization VII mods using Python instead of handwriting XML. This library provides:

- **13 Builder classes** for civilizations, units, buildings, progression trees, modifiers, and more
- **79 Node types** covering all game data structures
- **21 Enum constants** for traits, yields, effects, districts, ages, and unit classes
- **11 Localization classes** with Pydantic validation
- **Automatic XML generation** with proper formatting and structure
- **Action group management** for age-specific content loading
- **Asset imports** for custom icons, SQL files, and other resources

## Quick Start

### Installation

```bash
pip install civ7-modding-tools
```

Or with `uv` (recommended):

```bash
uv add civ7-modding-tools
```

### Your First Mod

```python
from civ7_modding_tools import Mod, CivilizationBuilder, ActionGroupBundle
from civ7_modding_tools.constants import Trait

# Create mod container
mod = Mod(
    id='my-first-mod',
    version='1.0.0',
    name='My Custom Civilization',
    description='A simple test civilization',
    authors='Your Name'
)

# Create civilization
civ = CivilizationBuilder()
civ.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
civ.fill({
    'civilization_type': 'CIVILIZATION_CUSTOM',
    'civilization': {
        'domain': 'AntiquityAgeCivilizations',
        'civilization_type': 'CIVILIZATION_CUSTOM',
    },
    'civilization_traits': ['TRAIT_ANTIQUITY_CIV', Trait.ECONOMIC.value],
    'localizations': [{
        'name': 'Custom Civilization',
        'description': 'A test civilization',
        'adjective': 'Custom',
        'city_names': ['Capital City', 'Second City', 'Third City']
    }]
})

# Build mod
mod.add(civ)
mod.build('./dist')
```

**Output**: Generates `.modinfo` file and properly structured XML files in `./dist/`

## Features

### Comprehensive Builder System

**Entity Builders:**
- `CivilizationBuilder` - Complete civilizations with traits, unlocks, icons, AI config
- `UnitBuilder` - Military and civilian units with stats, costs, abilities
- `ConstructibleBuilder` - Buildings and improvements with yields, requirements
- `ProgressionTreeBuilder` - Civic/tech trees with node unlocks
- `UniqueQuarterBuilder` - Civilization-unique districts

**Support Builders:**
- `ModifierBuilder` - Game modifiers for abilities and bonuses
- `TraditionBuilder` - Cultural traditions and legacy bonuses
- `LeaderUnlockBuilder` & `CivilizationUnlockBuilder` - Age transitions
- `ProgressionTreeNodeBuilder` - Individual civic/tech nodes
- `UnlockBuilder` - Generic unlock configurations
- `ImportFileBuilder` - Asset imports (icons, SQL files)

### Type Safety

Full type hints with Pydantic models ensure correctness:

```python
from civ7_modding_tools.constants import UnitClass, Yield, Effect
from civ7_modding_tools.localizations import UnitLocalization

unit = UnitBuilder().fill({
    'unit_type': 'UNIT_CUSTOM_WARRIOR',
    'type_tags': [UnitClass.MELEE.value],  # Type-safe enum
    'unit_cost': {'yield_type': Yield.PRODUCTION.value, 'cost': 30},
    'localizations': [
        UnitLocalization(name='Custom Warrior', description='A brave fighter')
    ]
})
```

### Action Groups

Control when content loads (by age/era):

```python
from civ7_modding_tools import ActionGroupBundle

# Load in Antiquity age only
AGE_ANTIQUITY = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')

# Load in all ages
ALWAYS = ActionGroupBundle(action_group_id='ALWAYS')

builder.action_group_bundle = AGE_ANTIQUITY
```

### Asset Management

Import custom icons, textures, and data files:

```python
from civ7_modding_tools.builders import ImportFileBuilder

icon = ImportFileBuilder().fill({
    'source_path': './assets/civ-icon.png',
    'target_name': 'civ_sym_myciv'
})

mod.add_files(icon)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Mod (Orchestrator)                     │
│  - Manages builders, files, action groups                       │
│  - Generates .modinfo + organizes XML output                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
         ┌──────────▼──────────┐   ┌─────────▼─────────┐
         │  Builders (13)      │   │  Files (3)        │
         │  - BaseBuilder      │   │  - BaseFile       │
         │  - Civilization     │   │  - XmlFile        │
         │  - Unit             │   │  - ImportFile     │
         │  - Constructible    │   │                   │
         │  - ProgressionTree  │   └───────────────────┘
         │  - Modifier, etc.   │
         └─────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
┌────────▼────────┐   ┌────────▼────────┐
│ Nodes (79)      │   │ Localizations   │
│ - BaseNode      │   │   (11 classes)  │
│ - DatabaseNode  │   │ - Pydantic      │
│ - Specialized   │   │   models        │
│   nodes for     │   │ - Type-safe     │
│   game data     │   │   validation    │
└─────────────────┘   └─────────────────┘
```

**Flow**: `Builder` → `Nodes` → `Files` → `Mod.build()` → `.modinfo + XML files`

## Documentation

- **[docs/INDEX.md](docs/INDEX.md)** - Documentation hub and navigation
- **[docs/GUIDE.md](docs/GUIDE.md)** - Comprehensive getting started guide
- **[docs/API.md](docs/API.md)** - Complete API reference
- **[docs/EXAMPLES.md](docs/EXAMPLES.md)** - Practical examples and patterns
- **[docs/MIGRATION.md](docs/MIGRATION.md)** - TypeScript to Python migration guide

## Examples

The [`examples/`](examples/) directory contains complete working mods:

- **[babylon_civilization.py](examples/babylon_civilization.py)** - Scientific civilization with custom units, buildings, and progression trees
- **[unit.py](examples/unit.py)** - Simple custom unit creation
- **[progression_tree.py](examples/progression_tree.py)** - Civic/tech tree example
- **[unique_quarter.py](examples/unique_quarter.py)** - Civilization-unique district
- **[import_custom_icon.py](examples/import_custom_icon.py)** - Asset import example
- **[import_sql_file.py](examples/import_sql_file.py)** - SQL database integration
- **[unlock_builder.py](examples/unlock_builder.py)** - Game unlock configurations

Run any example:
```bash
python examples/babylon_civilization.py
```

## Development

### Setup

```bash
git clone https://github.com/Phlair/civ7-modding-tools.git
cd civ7-modding-tools
uv sync  # Install with all dev dependencies
```

### Testing

```bash
uv run pytest              # Run all tests
uv run pytest --cov        # With coverage report (94% coverage)
uv run pytest -v           # Verbose output
```

### Project Structure

```
src/civ7_modding_tools/
├── core/mod.py           # Mod orchestrator + ActionGroupBundle
├── builders/builders.py  # All 13 builder classes
├── nodes/                # 79 node types for XML elements
│   ├── base.py           # BaseNode
│   ├── nodes.py          # Game entity nodes
│   ├── database.py       # Database operation nodes
│   └── action_groups.py  # Action group/criteria nodes
├── files/                # File generation
│   └── __init__.py       # BaseFile, XmlFile, ImportFile
├── localizations/        # 11 Pydantic localization models
│   └── __init__.py
├── constants/            # 21 Enum classes
│   └── __init__.py       # Trait, UnitClass, Effect, Yield, etc.
├── utils/                # Utility functions
│   └── __init__.py       # locale(), fill(), trim(), etc.
└── xml_builder.py        # XML generation utilities
```

### Code Conventions

- **Python 3.12+** with full type hints
- **PEP 8 style** with 100-character line limit
- **British English** in docstrings and comments
- **Builder pattern** with `.fill()` method chaining
- **Pydantic models** for data validation

See [.github/instructions/python.instructions.md](.github/instructions/python.instructions.md) for detailed conventions.

## Requirements

- **Python**: 3.12 or higher
- **Dependencies**:
  - `pydantic` (≥2.0.0) - Data validation and models
  - `xmltodict` (≥0.13.0) - XML generation and parsing

## License

MIT No Distribution License

Copyright (c) 2025 [izica](https://github.com/izica) (original), Phlair (rework)

See [LICENSE](LICENSE) for full terms.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run `pytest` to ensure all tests pass
5. Submit a pull request

All contributions must follow the coding conventions in [.github/instructions/python.instructions.md](.github/instructions/python.instructions.md).

## Support

- **Issues**: [GitHub Issues](https://github.com/Phlair/civ7-modding-tools/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Phlair/civ7-modding-tools/discussions)
- **Documentation**: [docs/INDEX.md](docs/INDEX.md)

---

**Built with ❤️ for the Civilization VII modding community**
