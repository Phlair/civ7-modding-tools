# Civ7 Modding Tools - Examples

Practical examples for common modding scenarios.

> 💡 **Parity Test Example**: See [examples/gondor_civilization.py](../examples/gondor_civilization.py) for a complete example that generates identical output to the TypeScript reference implementation (22 files with exact path/naming parity).

## Table of Contents

1. [Example 1: Simple Civilization](#example-1-simple-civilization)
2. [Example 2: Complete Civilization with All Features](#example-2-complete-civilization)
3. [Example 3: Custom Unit with Abilities](#example-3-custom-unit-with-abilities)
4. [Example 4: Building a Tech Tree](#example-4-building-a-tech-tree)
5. [Example 5: Game Modifiers and Effects](#example-5-game-modifiers-and-effects)
6. [Example 6: Importing External Assets](#example-6-importing-external-assets)
7. [Example 7: Mod with Multiple Entities](#example-7-mod-with-multiple-entities)

---

## Example 1: Simple Civilization

The simplest possible mod—just one basic civilization:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    ActionGroupBundle,
    Trait,
)

# Create mod container
mod = Mod(
    id="simple-mod",
    version="1.0",
    name="Simple Civilization",
    description="A minimal custom civilization",
    authors="Modder Name"
)

# Create civilization
civ = CivilizationBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    "civilization": {
        "civilization_type": "CIVILIZATION_CUSTOM_001",
        "civilization_name": "CIVILIZATION_CUSTOM_001",
    },
    "civilization_traits": [TRAIT.ECONOMIC_CIV],
    "localizations": [{
        "name": "Custom Civilization",
        "description": "A custom civilization",
        "full_name": "The Custom Empire",
        "adjective": "Custom",
        "city_names": ["Capital", "City 2", "City 3"]
    }]
})

# Add and build
mod.add(civ)
mod.build("./dist")

print("✅ Mod generated in ./dist/")
```

**Output Files:**
```
dist/mod-test.modinfo
dist/civilizations/custom-001/current.xml
dist/civilizations/custom-001/unlocks.xml
dist/civilizations/custom-001/legacy.xml
dist/civilizations/custom-001/icons.xml
dist/civilizations/custom-001/shell.xml
dist/civilizations/custom-001/game-effects.xml
dist/civilizations/custom-001/localization.xml
```

---

## Example 2: Complete Civilization with All Features

A fully-featured civilization with all possible properties:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    ActionGroupBundle,
    Trait,
    TagTrait,
)

mod = Mod(
    id="rome-complete",
    version="2.0",
    name="Complete Roman Civilization",
    description="A full-featured Roman civilization with all features",
    authors="John Doe"
)

rome = CivilizationBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    
    # Main civilization definition
    "civilization": {
        "civilization_type": "CIVILIZATION_ROME_CUSTOM",
        "civilization_name": "CIVILIZATION_ROME_CUSTOM",
        "capital": "Rome",
        "base_tourism": 3,
        "legacy_modifier": True,
    },
    
    # Traits and tags
    "civilization_traits": [
        Trait.ECONOMIC,
        Trait.MILITARY,
    ],
    "trait_tags": [
        TagTrait.ECONOMIC,
        TagTrait.DIPLOMATIC,
    ],
    
    # Start location preferences
    "start_bias_biomes": [
        {"biome": "BIOME_TEMPERATE"},
        {"biome": "BIOME_PLAINS"},
    ],
    "start_bias_terrains": [
        {"terrain": "TERRAIN_GRASSLAND"},
        {"terrain": "TERRAIN_PLAINS"},
    ],
    "start_bias_resources": [
        {"resource": "RESOURCE_WHEAT"},
        {"resource": "RESOURCE_IRON"},
    ],
    "start_bias_rivers": [{"river": "RIVER"}],
    "start_bias_adjacent_to_coast": [{"adjacent_to_coast": True}],
    
    # Visual arts configuration
    "vis_art_civilization_building_cultures": [
        {"vis_art_type": "VISART_ROMAN_BUILDINGS"}
    ],
    "vis_art_civilization_unit_cultures": [
        {"vis_art_type": "VISART_ROMAN_UNITS"}
    ],
    
    # Multi-language localization
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
                "Florence",
                "Ravenna",
                "Pompeii",
                "Amalfi",
            ]
        }
    ]
})

mod.add(rome)
mod.build("./dist")
```

---

## Example 3: Custom Unit with Abilities

Create a unique unit with special abilities and upgrades:

```python
from civ7_modding_tools import (
    Mod,
    UnitBuilder,
    ActionGroupBundle,
    UnitClass,
    UnitMovementClass,
)

mod = Mod(
    id="roman-legionnaire",
    version="1.0",
    name="Roman Legionnaire Unit",
    authors="Modder"
)

# Create Legionnaire unit
legionnaire = UnitBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    
    "unit": {
        "unit_type": "UNIT_ROMAN_LEGIONNAIRE",
        "unit_name": "UNIT_ROMAN_LEGIONNAIRE",
        "unit_class": UnitClass.MELEE,
        "unit_movement_class": UnitMovementClass.LAND,
        "base_movement": 2,
        "base_sight": 2,
        "era": "ERA_CLASSICAL",
    },
    
    "unit_stats": {
        "melee_strength": 38,      # Stronger than base warrior (20)
        "ranged_strength": 0,
        "bombard_strength": 0,
        "combat_experience_modifier": 25,
    },
    
    "unit_costs": {
        "production": 60,
        "resource_cost": [
            {"resource_type": "RESOURCE_IRON", "cost": 1}
        ],
    },
    
    "unit_abilities": [
        {
            "name": "ABILITY_PHALANX",
            "level": 1,
            "description": "Defensive formation bonus"
        }
    ],
    
    "unit_upgrades": [
        {
            "unit_type": "UNIT_ROMAN_PRAETORIAN",
            "era": "ERA_MEDIEVAL"
        }
    ],
    
    "unit_advisories": [
        {
            "advisory_type": "ADVISORY_MILITARY",
            "level": 3
        }
    ],
    
    "localizations": [{
        "name": "Roman Legionnaire",
        "description": "Elite Roman infantry with phalanx formation",
        "type_name": "Melee Unit"
    }]
})

mod.add(legionnaire)
mod.build("./dist")
```

---

## Example 4: Building a Tech Tree

Create a simple progression tree (tech tree):

```python
from civ7_modding_tools import (
    Mod,
    ProgressionTreeBuilder,
    ActionGroupBundle,
)

mod = Mod(
    id="tech-tree",
    version="1.0",
    name="Custom Tech Tree",
    authors="Modder"
)

# Create progression tree
tree = ProgressionTreeBuilder({
    "action_group_bundle": ACTION_GROUP_BUNDLE.ALWAYS,
    
    "progression_tree_type": "PROGRESSION_TREE_TECHNOLOGY",
    
    "progression_tree_nodes": [
        {
            "progression_tree_node_type": "TECH_AGRICULTURE",
            "row": 1,
            "column": 1,
            "era": "ERA_ANCIENT",
        },
        {
            "progression_tree_node_type": "TECH_ANIMAL_HUSBANDRY",
            "row": 1,
            "column": 2,
            "era": "ERA_ANCIENT",
            "prerequisites": ["TECH_AGRICULTURE"],
        },
        {
            "progression_tree_node_type": "TECH_ANIMAL_HUSBANDRY",
            "row": 2,
            "column": 1,
            "era": "ERA_ANCIENT",
            "prerequisites": ["TECH_AGRICULTURE"],
        },
    ],
    
    "localizations": [{
        "name": "Custom Technology Tree",
        "description": "A custom technology progression"
    }]
})

mod.add(tree)
mod.build("./dist")
```

---

## Example 5: Game Modifiers and Effects

Create gameplay modifiers that affect units, buildings, or players:

```python
from civ7_modding_tools import (
    Mod,
    ModifierBuilder,
    ActionGroupBundle,
    Collection,
    Effect,
    Requirement,
)

mod = Mod(
    id="modifiers",
    version="1.0",
    name="Custom Game Modifiers",
    authors="Modder"
)

# Modifier 1: Increase movement for all units
unit_movement_mod = ModifierBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    
    "collection": Collection.PLAYER_UNITS,
    "effect": Effect.UNIT_ADJUST_MOVEMENT,
    "is_detached": False,  # Attached to specific units
    
    "arguments": [
        {"name": "Amount", "value": 1}
    ],
    
    "requirements": [
        {
            "type": Requirement.UNIT_TAG_MATCHES,
            "arguments": [
                {"name": "Tag", "value": "UNIT_CLASS_MELEE"}
            ]
        }
    ],
    
    "localizations": [{
        "name": "Bonus Movement",
        "description": "All melee units gain +1 movement"
    }]
})

# Modifier 2: Player-level bonus to production
player_production_mod = ModifierBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    
    "collection": Collection.PLAYER_CITIES,
    "effect": Effect.CITY_ADJUST_GROWTH,
    "is_detached": True,  # Detached global modifier
    
    "arguments": [
        {"name": "Amount", "value": 10}  # +10% production
    ],
    
    "localizations": [{
        "name": "Production Boost",
        "description": "All players gain +10% production"
    }]
})

mod.add([unit_movement_mod, player_production_mod])
mod.build("./dist")
```

---

## Example 6: Importing External Assets

Import custom images, SQL scripts, and other files:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    ImportFileBuilder,
    ActionGroupBundle,
    Trait,
)

mod = Mod(
    id="civ-with-assets",
    version="1.0",
    name="Mod with Custom Assets",
    authors="Modder"
)

# Add civilization
civ = CivilizationBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    "civilization": {
        "civilization_type": "CIVILIZATION_CUSTOM",
        "civilization_name": "CIVILIZATION_CUSTOM",
    },
    "civilization_traits": [Trait.ECONOMIC],
    "localizations": [{
        "name": "Custom Civ",
        "description": "Civ with custom assets"
    }]
})

# Import custom civilization icon
civ_icon = ImportFileBuilder({
    "path": "/imports/",
    "name": "civ_symbol",
    "content": "./assets/custom_civ_icon.png"
})

# Import custom SQL database script
sql_file = ImportFileBuilder({
    "path": "/imports/",
    "name": "custom_data",
    "content": "./assets/custom_data.sql"
})

mod.add(civ)
mod.add_files([civ_icon, sql_file])
mod.build("./dist")

print("✅ Mod with assets generated in ./dist/")
print("   Assets copied to dist/imports/")
```

**File Structure:**
```
assets/
  ├── custom_civ_icon.png
  └── custom_data.sql

dist/
  ├── mod-test.modinfo
  ├── civilizations/
  └── imports/
      ├── civ_symbol (copied from custom_civ_icon.png)
      └── custom_data (copied from custom_data.sql)
```

---

## Example 7: Mod with Multiple Entities

Create a complete mod with civilization, units, and buildings:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ActionGroupBundle,
    Trait,
    UnitClass,
    UnitMovementClass,
    ConstructibleClass,
    Yield,
)

# Create mod
mod = Mod(
    id="rome-complete-mod",
    version="1.0",
    name="Complete Roman Mod",
    description="Rome with unique units and buildings",
    authors="Modder"
)

# ============ CIVILIZATION ============
rome = CivilizationBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    "civilization": {
        "civilization_type": "CIVILIZATION_ROME",
        "civilization_name": "CIVILIZATION_ROME",
    },
    "civilization_traits": [Trait.MILITARY],
    "localizations": [{
        "name": "Rome",
        "description": "Ancient Roman Empire",
        "full_name": "The Roman Empire",
        "adjective": "Roman",
        "city_names": ["Rome", "Milan", "Venice"]
    }]
})

# ============ UNITS ============
legionnaire = UnitBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    "unit": {
        "unit_type": "UNIT_LEGIONNAIRE",
        "unit_name": "UNIT_LEGIONNAIRE",
        "unit_class": UnitClass.MELEE,
        "unit_movement_class": UnitMovementClass.LAND,
        "base_movement": 2,
    },
    "unit_stats": {
        "melee_strength": 38,
        "ranged_strength": 0,
    },
    "unit_costs": {
        "production": 60,
    },
    "localizations": [{
        "name": "Legionnaire",
        "description": "Elite Roman infantry"
    }]
})

ballista = UnitBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    "unit": {
        "unit_type": "UNIT_BALLISTA",
        "unit_name": "UNIT_BALLISTA",
        "unit_class": UnitClass.RANGED,
        "unit_movement_class": UnitMovementClass.LAND,
        "base_movement": 2,
    },
    "unit_stats": {
        "melee_strength": 15,
        "ranged_strength": 40,
    },
    "unit_costs": {
        "production": 80,
        "resource_cost": [
            {"resource_type": "RESOURCE_IRON", "cost": 1}
        ],
    },
    "localizations": [{
        "name": "Ballista",
        "description": "Roman siege weapon"
    }]
})

# ============ BUILDINGS ============
forum = ConstructibleBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    "building": {
        "building_type": "BUILDING_FORUM",
        "building_name": "BUILDING_FORUM",
        "building_class": ConstructibleClass.ECONOMIC,
    },
    "production_cost": 120,
    "constructible_yield_changes": [
        {"yield_type": Yield.GOLD, "yield_change": 2},
    ],
    "maintenance": {Yield.GOLD: 1},
    "localizations": [{
        "name": "Forum",
        "description": "Increases trade routes and gold"
    }]
})

aqueduct = ConstructibleBuilder({
    "action_group_bundle": ActionGroupBundle.ALWAYS,
    "building": {
        "building_type": "BUILDING_AQUEDUCT",
        "building_name": "BUILDING_AQUEDUCT",
        "building_class": ConstructibleClass.ECONOMIC,
    },
    "production_cost": 100,
    "constructible_yield_changes": [
        {"yield_type": Yield.HOUSING, "yield_change": 3},
    ],
    "maintenance": {Yield.GOLD: 2},
    "localizations": [{
        "name": "Aqueduct",
        "description": "Increases housing"
    }]
})

# ============ ADD TO MOD ============
mod.add(rome)
mod.add([legionnaire, ballista])
mod.add([forum, aqueduct])

# ============ BUILD ============
mod.build("./dist")

print("✅ Complete Roman mod generated!")
print(f"   - 1 civilization")
print(f"   - 2 units")
print(f"   - 2 buildings")
print(f"   Output: ./dist/")
```

**Generated Files:**
```
dist/
├── mod-test.modinfo
├── civilizations/rome/
│   ├── current.xml
│   ├── unlocks.xml
│   ├── legacy.xml
│   └── icons.xml
├── units/
│   ├── legionnaire/
│   │   └── current.xml
│   └── ballista/
│       └── current.xml
└── constructibles/
    ├── forum/
    │   └── current.xml
    └── aqueduct/
        └── current.xml
```

---

## Running Your Examples

### Method 1: Create a Python file

```bash
# my_mod.py
from civ7_modding_tools import Mod, CivilizationBuilder, ...

mod = Mod(...)
# ... build your mod ...
mod.build("./dist")
```

Run with:
```bash
python my_mod.py
```

### Method 2: Using uv

```bash
uv run my_mod.py
```

### Method 3: Python interactive shell

```bash
python
>>> from civ7_modding_tools import *
>>> mod = Mod(...)
>>> mod.build("./dist")
```

---

## Testing Your Mod

1. **Generate files**: Run your build script to create `dist/mod-test.modinfo`
2. **Check output**: Verify files are created in `dist/`
3. **Validate XML**: Check generated XML is well-formed
4. **Install**: Copy `dist/` contents to Civ7 mods folder
5. **Test in-game**: Load the mod and verify it works

---

## Troubleshooting

### No files generated
- Ensure you call `mod.build("./dist")`
- Check write permissions to `./dist`

### Missing localizations
- Add `localizations` list to each builder
- Ensure all required fields are present

### Type errors in IDE
- Import constants from the library
- Use type hints for better IDE support

### XML errors in Civ7
- Validate XML files are well-formed
- Check attribute names match expected format
- Verify all required fields are present

---

## More Examples

See the [examples/](../examples/) directory in the repository for additional working examples:
- `examples/babylon_civilization.py` - Scientific civilization example
- `examples/gondor_civilization.py` - Complete civilization with all features
- `examples/unit.py` - Create custom units
- `examples/progression_tree.py` - Build civics trees
- `examples/unique_quarter.py` - Civilization-unique districts
- `examples/import_custom_icon.py` - Import custom assets
- `examples/import_sql_file.py` - SQL database imports
- `examples/unlock_builder.py` - Game progression unlocks

---

## Next Steps

- **[API Reference](API.md)**: Complete API documentation
- **[Getting Started](GUIDE.md)**: Detailed tutorial
- **[Migration Guide](MIGRATION.md)**: Coming from TypeScript?

Happy modding! 🎮

