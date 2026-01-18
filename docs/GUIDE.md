# Phlair's Civ VII Modding Tools - Getting Started Guide

Welcome to **Phlair's Civ VII Modding Tools**, a Python library for creating Civilization 7 mods programmatically. This guide will walk you through building your first mod from scratch.

> **Note**: This project is a complete rework of the original toolset. Original fork from [izica](https://github.com/izica).

> ✅ **Python v1.3.0**: Pure Python implementation with full builder pattern support. All 13 builders, 79 nodes, 21 constants, and 11 localization classes fully implemented with 94% test coverage (324 tests passing).

## Table of Contents

1. [Installation](#installation)
2. [Your First Mod](#your-first-mod)
3. [Core Concepts](#core-concepts)
4. [Building a Civilization](#building-a-civilization)
5. [Adding Units](#adding-units)
6. [Adding Buildings](#adding-buildings)
7. [Next Steps](#next-steps)

## Installation

### Prerequisites

- Python 3.12+ (tested on 3.14.2)
- pip or uv package manager

### Install via PyPI

```bash
pip install civ7-modding-tools
```

Or with uv:

```bash
uv add civ7-modding-tools
```

### Development Installation

For development or contributing:

```bash
git clone https://github.com/Phlair/civ7-modding-tools.git
cd civ7-modding-tools
uv sync  # Install with all dev dependencies
```

## Your First Mod

Let's create a simple mod with one civilization:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    ACTION_GROUP_BUNDLE,
    TRAIT,
)

# 1. Create the mod container
mod = Mod(
    id="my-first-mod",
    version="1.0.0",
    name="My First Civilization Mod",
    description="A simple custom civilization",
    authors="Your Name"
)

# 2. Create a civilization builder
civilization = CivilizationBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    "civilization": {
        "civilization_type": "CIVILIZATION_CUSTOM_001",
        "civilization_name": "CIVILIZATION_CUSTOM_001",
    },
    "civilization_traits": [Trait.ECONOMIC],
    "localizations": [
        {
            "name": "My Custom Civ",
            "description": "A custom civilization",
            "full_name": "The Custom Empire",
            "adjective": "Custom",
            "city_names": ["Capital", "City 2", "City 3"]
        }
    ]
})

# 3. Add civilization to mod
mod.add(civilization)

# 4. Build and generate files
mod.build("./dist")
```

**Output Files Generated:**
```
dist/
├── mod-test.modinfo           # Mod metadata
└── civilizations/custom_001/
    ├── current.xml            # Civilization definition
    ├── unlocks.xml           # Civilization unlocks
    ├── legacy.xml            # Civilization legacy
    └── icons.xml             # Civilization icons
```

## Core Concepts

### 1. The Mod Class

The `Mod` class is your main container for mod creation:

```python
mod = Mod(
    id="unique-mod-id",           # Unique identifier
    version="1.0.0",               # Version number
    name="Display Name",           # User-facing name
    description="What this mod does",
    authors="Your Name",
    affects_saved_games=False      # Optional: affects existing saves?
)
```

### 2. Builders

Builders create specific mod entities. The builder pattern provides a fluent API:

```python
# Long form
builder = CivilizationBuilder()
builder.fill({
    "civilization": {"civilization_type": "CIV_ROME"},
    "civilization_traits": [TRAIT.MILITARY_CIV]
})

# Short form (constructor with dict)
builder = CivilizationBuilder({
    "civilization": {"civilization_type": "CIV_ROME"},
    "civilization_traits": [TRAIT.MILITARY_CIV]
})
```

### 3. Action Groups

Action groups control when content loads in the game:

```python
# Always loaded
CivilizationBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    ...
})

# Loaded in specific age (e.g., Ancient Age)
CivilizationBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
    ...
})
```

### 4. Constants

Type-safe game constants replace magic strings:

```python
from civ7_modding_tools import (
    Trait,              # Civilization traits
    UnitClass,          # Unit classifications
    Effect,             # Game modifiers
    Requirement,        # Game conditions
    Yield,              # Resource production
    Age,                # Game eras
)

# Examples:
Trait.ECONOMIC                  # Trait
UnitClass.RECON                 # Unit type
Effect.UNIT_ADJUST_MOVEMENT     # Game effect
Yield.CULTURE                   # Resource
Age.EXPLORATION                 # Game era
```

## Building a Civilization

Create a complete civilization with all features:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    ACTION_GROUP_BUNDLE,
    TRAIT,
    TAG_TRAIT,
)

mod = Mod(
    id="rome-mod",
    version="1.0",
    name="Roman Civilization"
)

civilization = CivilizationBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    
    # Main civilization properties
    "civilization": {
        "civilization_type": "CIVILIZATION_ROME_CUSTOM",
        "civilization_name": "CIVILIZATION_ROME_CUSTOM",
        "base_tourism": 5,
        "capital": "Rome",
    },
    
    # Civilization traits
    "civilization_traits": [
        Trait.ECONOMIC,
        Trait.SCIENTIFIC,
    ],
    "trait_tags": [
        TagTrait.ECONOMIC,
        TagTrait.DIPLOMATIC,
    ],
    
    # Start location preferences
    "start_bias_biomes": ["BIOME_PLAINS"],
    "start_bias_terrains": ["TERRAIN_GRASSLAND"],
    "start_bias_resources": ["RESOURCE_WHEAT"],
    
    # Localization (multiple languages)
    "localizations": [
        {
            "name": "Rome",
            "description": "Ancient Roman Empire",
            "full_name": "The Roman Empire",
            "adjective": "Roman",
            "city_names": [
                "Rome",
                "Milan",
                "Venice",
                "Naples",
                "Florence"
            ]
        }
    ]
})

mod.add(civilization)
mod.build("./dist")
```

## Adding Units

Create custom units for your civilization:

```python
from civ7_modding_tools import (
    UnitBuilder,
    UnitClass,
    UnitMovementClass,
    ActionGroupBundle,
)

# Create a custom unit
unit = UnitBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    
    # Unit basic properties
    "unit": {
        "unit_type": "UNIT_ROMAN_LEGIONNAIRE",
        "unit_name": "UNIT_ROMAN_LEGIONNAIRE",
        "unit_class": UnitClass.MELEE,
        "unit_movement_class": UnitMovementClass.LAND,
        "base_movement": 2,
        "base_sight": 2,
    },
    
    # Unit combat statistics
    "unit_stats": {
        "melee_strength": 38,
        "ranged_strength": 0,
        "bombard_strength": 0,
    },
    
    # Unit costs
    "unit_costs": {
        "production": 60,
        "resource_cost": [],
    },
    
    # Abilities
    "unit_abilities": [
        {"name": "ABILITY_TEST", "level": 1}
    ],
    
    # Localization
    "localizations": [
        {
            "name": "Roman Legionnaire",
            "description": "Elite Roman infantry unit"
        }
    ]
})

mod.add(unit)
```

## Adding Buildings

Create custom buildings and improvements:

```python
from civ7_modding_tools import (
    ConstructibleBuilder,
    ConstructibleClass,
    ActionGroupBundle,
    Yield,
)

# Create a building
building = ConstructibleBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    
    # Constructible properties
    "building": {
        "building_type": "BUILDING_ROMAN_TEMPLE",
        "building_name": "BUILDING_ROMAN_TEMPLE",
        "building_class": ConstructibleClass.ECONOMIC,
    },
    
    # Production cost
    "production_cost": 150,
    "resource_cost": [],
    
    # Yields (what it produces)
    "constructible_yield_changes": [
        {
            "yield_type": Yield.FAITH,
            "yield_change": 4,
        }
    ],
    
    # Maintenance cost
    "maintenance": {
        Yield.GOLD: 1,
    },
    
    # Localization
    "localizations": [
        {
            "name": "Roman Temple",
            "description": "Provides Faith to this city"
        }
    ]
})

mod.add(building)
```

## Adding Multiple Entities

Build a complete mod with multiple entities:

```python
from civ7_modding_tools import Mod, CivilizationBuilder, UnitBuilder, ConstructibleBuilder

mod = Mod(
    id="complete-rome",
    version="1.0",
    name="Complete Roman Mod"
)

# Add civilization
mod.add(CivilizationBuilder({...}))

# Add multiple units at once
units = [
    UnitBuilder({...}),  # Legionnaire
    UnitBuilder({...}),  # Ballista
    UnitBuilder({...}),  # Trireme
]
mod.add(units)

# Add buildings
mod.add([
    ConstructibleBuilder({...}),  # Temple
    ConstructibleBuilder({...}),  # Forum
])

# Generate all files
mod.build("./dist")
```

## Working with Files

### Project Structure

```
my-mod/
├── build.py              # Your build script
├── dist/                 # Generated output
│   ├── mod-test.modinfo
│   ├── civilizations/
│   ├── units/
│   ├── constructibles/
│   └── imports/
└── assets/               # Your custom assets
    ├── icons/
    └── scripts/
```

### Run Your Build Script

```bash
# Using uv
uv run build.py

# Using Python
python build.py

# The build creates mod files in ./dist ready to use with Civilization 7
```

### Installing Your Mod

1. Build your mod: `python build.py`
2. Copy `dist/` to your Civ7 mods directory:
   - Windows: `%USERPROFILE%\Documents\My Games\Civilization VII\Mods\`
   - macOS: `~/Library/Application Support/Civilization VII/Mods/`
   - Linux: `~/.config/Civilization VII/Mods/`
3. Restart Civ7 and enable your mod

## Common Patterns

### Conditional Content (Age-Based Loading)

```python
# Modern age unit
UnitBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.AGE_MODERN,
    # Loaded only in Modern Age
    ...
})
```

### Shared Properties

```python
# Create a dict with common properties
base_unit = {
    "unit_class": UNIT_CLASS.MELEE,
    "unit_movement_class": UNIT_MOVEMENT_CLASS.LAND,
}

# Reuse for multiple units
for name, strength in [("Warrior", 10), ("Legionnaire", 38)]:
    unit = UnitBuilder({
        "unit": {
            "unit_type": f"UNIT_{name.upper()}",
            **base_unit  # Include base properties
        }
    })
    mod.add(unit)
```

## Troubleshooting

### Issue: No files generated

**Solution**: Ensure you call `mod.build("./dist")` after adding builders:

```python
mod.add(civilization)
mod.build("./dist")  # Don't forget this!
```

### Issue: Missing localization

**Solution**: Each builder should have localizations matching its entity type:

```python
CivilizationBuilder({
    "localizations": [{
        "name": "My Civ",           # Required
        "description": "My civ",    # Optional but recommended
        ...
    }]
})
```

### Issue: Type errors in IDE

**Solution**: Import types from the library:

```python
from civ7_modding_tools import TRAIT, UNIT_CLASS, EFFECT
# Now IDE can provide autocomplete
```

## Next Steps

- **[API Reference](API.md)**: Complete reference for all classes and methods
- **[Examples](EXAMPLES.md)**: More complex examples and use cases
- **[Migration Guide](MIGRATION.md)**: Coming from TypeScript? See the migration guide
- **[Contributing](../CONTRIBUTING.md)**: Help improve the library

## Resources

- **GitHub**: https://github.com/Phlair/civ7-modding-tools
- **Issue Tracker**: Report bugs or request features
- **Civilization 7 Modding**: https://civilization.fandom.com/wiki/Modding

---

**Happy Modding!** 🎮

