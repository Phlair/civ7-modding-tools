# Civ7 Modding Tools - Python Library
Python library for programmatically generating Civilization 7 mods with full type safety and builder patterns.

- [Features](#features)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Documentation](#documentation)
- [Development](#development)

## Features
- **Type-safe builders** for civilizations, units, buildings, and progression trees
- **Automatic XML generation** with proper formatting and structure
- **Action group support** for age-specific content loading
- **Localization support** for multiple languages
- **Asset imports** for custom icons and files
- **Mod orchestration** via simple, fluent API

## Getting Started

### Installation

Using `uv` (recommended):
```bash
uv add civ7-modding-tools
```

Using pip:
```bash
pip install civ7-modding-tools
```

### Quick Start

```python
from civ7_modding_tools import Mod, CivilizationBuilder, Trait

mod = Mod(id='my-mod', version='1.0', name='My Mod')

civ = CivilizationBuilder({
    'civilization': {'civilization_type': 'CIVILIZATION_CUSTOM'},
    'civilization_traits': [Trait.ECONOMIC],
    'localizations': [{'name': 'Custom Civ', 'city_names': ['Capital']}]
})

mod.add(civ)
mod.build('./dist')
```

## Examples

See [examples/](examples/) folder for complete working examples:

- **[babylon_civilization.py](examples/babylon_civilization.py)** - Full civilization with units, buildings, and progression trees (scientific focus)
- **[gondor_civilization.py](examples/gondor_civilization.py)** - Complete Middle Earth civilization example
- **[unit.py](examples/unit.py)** - Create custom military units
- **[progression_tree.py](examples/progression_tree.py)** - Build civics progression trees
- **[unique_quarter.py](examples/unique_quarter.py)** - Create civilization-unique districts
- **[import_custom_icon.py](examples/import_custom_icon.py)** - Import custom asset files
- **[import_sql_file.py](examples/import_sql_file.py)** - Integrate SQL database modifications
- **[unlock_builder.py](examples/unlock_builder.py)** - Define game progression unlocks

## Documentation

- **[API.md](docs/API.md)** - Complete API reference with all builders, nodes, and utilities
- **[GUIDE.md](docs/GUIDE.md)** - User guide with common patterns and architecture
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Example walkthroughs and explanations
- **[INDEX.md](docs/INDEX.md)** - Project structure and file organization

## Development

### Setup
```bash
uv sync
```

### Testing
```bash
uv run pytest              # Run all tests
uv run pytest --cov        # With coverage report
```

### Build
The library generates Civilization 7 mods by creating XML files and metadata. Mods are built to a specified output directory with:
- ModInfo configuration file
- Automatically organized XML files
- Asset imports and localization

For detailed development info, see [.github/instructions/python.instructions.md](.github/instructions/python.instructions.md)
