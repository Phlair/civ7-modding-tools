# Phlair's Civ VII Modding Tools - API Reference

Complete API documentation for the Phlair's Civ VII Modding Tools library.

## Table of Contents

- [Core Classes](#core-classes)
  - [Mod](#mod)
  - [ActionGroupBundle](#actiongroupbundle)
- [Builders](#builders)
  - [BaseBuilder](#basebuilder)
  - [CivilizationBuilder](#civilizationbuilder)
  - [UnitBuilder](#unitbuilder)
  - [ConstructibleBuilder](#constructiblebuilder)
  - [Other Builders](#other-builders)
- [Path Generation & File Naming](#path-generation--file-naming)
- [Nodes](#nodes)
  - [BaseNode](#basenode)
  - [DatabaseNode](#databasenode)
  - [Specialized Nodes](#specialized-nodes)
- [Localizations](#localizations)
- [Constants](#constants)
- [Files](#files)
- [Utilities](#utilities)

---

## Core Classes

### Mod

Main container for mod creation and file generation.

#### Constructor

```python
Mod(
    id: str,                          # Unique mod identifier
    version: str = "1.0",            # Version number
    name: str = "Mod",               # Display name
    description: str = "",           # Description
    authors: str = "",               # Creator(s)
    affects_saved_games: bool = False # Affects existing saves?
)
```

#### Methods

**`add(builder: BaseBuilder | list[BaseBuilder]) -> Mod`**

Add one or more builders to the mod.

```python
mod = Mod(id="my-mod")
mod.add(civilization)  # Single builder
mod.add([unit1, unit2, building1])  # Multiple builders
```

**`add_files(file: BaseFile | list[BaseFile]) -> Mod`**

Add import files to the mod.

```python
import_file = ImportFileBuilder(content="./assets/icon.png")
mod.add_files(import_file)
```

**`build(dist: str, clear: bool = True) -> None`**

Generate mod files to disk.

```python
mod.build("./dist")  # Creates ./dist/mod-test.modinfo + XML files
```

#### Properties

- `id: str` - Unique mod identifier
- `version: str` - Version number
- `name: str` - Display name
- `description: str` - Description
- `authors: str` - Creator(s)
- `affects_saved_games: bool` - Whether mod affects existing saves
- `builders: list[BaseBuilder]` - Registered builders
- `files: list[BaseFile]` - Generated files
- `action_groups: dict[str, dict]` - Action group definitions

---

### ActionGroupBundle

Represents action group configuration for mod content.

#### Constructor

```python
ActionGroupBundle(
    action_group_id: str = "",
    action_group_action: str = "UpdateDatabase"
)
```

#### Methods

**`to_mod_info_action_groups() -> list[ActionGroupNode]`**

Generate ActionGroup XML elements for .modinfo.

#### Class Constants

Predefined action group bundles:

```python
ACTION_GROUP_BUNDLE.ALWAYS           # Always loaded
ACTION_GROUP_BUNDLE.AGE_ANTIQUITY    # Ancient age
ACTION_GROUP_BUNDLE.AGE_EXPLORATION  # Classical age
ACTION_GROUP_BUNDLE.AGE_MEDIEVAL     # Medieval age
ACTION_GROUP_BUNDLE.AGE_RENAISSANCE  # Renaissance age
ACTION_GROUP_BUNDLE.AGE_INDUSTRIAL   # Industrial age
ACTION_GROUP_BUNDLE.AGE_MODERN       # Modern age
ACTION_GROUP_BUNDLE.AGE_ATOMIC       # Atomic age
ACTION_GROUP_BUNDLE.AGE_DIGITAL      # Digital age
```

---

## Builders

All builders extend `BaseBuilder` and follow the builder pattern.

### BaseBuilder

Abstract base class for all builders.

#### Methods

**`fill(payload: Dict[str, Any]) -> Self`**

Fluent API: set properties from dictionary.

```python
builder.fill({
    "civilization": {"civilization_type": "CIV_ROME"},
    "civilization_traits": [TRAIT.ECONOMIC_CIV]
})
```

**`build() -> list[BaseFile]`**

Generate output files. Must be implemented by subclasses.

#### Properties

- `action_group_bundle: ActionGroupBundle` - Content loading criteria

---

### CivilizationBuilder

Create custom civilizations.

#### Constructor

```python
CivilizationBuilder(payload: Dict[str, Any] | None = None)
```

#### Properties

```python
# Main civilization definition
civilization: Dict[str, Any] = {}

# Traits
civilization_traits: list[str] = []
trait_tags: list[str] = []

# Unlocks (technologies/civics to start with)
civilization_unlocks: list[Dict[str, Any]] = []

# Leader unlocks
leader_unlocks: list[Dict[str, Any]] = []

# Start location preferences
start_bias_biomes: list[Dict[str, Any]] = []
start_bias_terrains: list[Dict[str, Any]] = []
start_bias_resources: list[Dict[str, Any]] = []
start_bias_rivers: list[Dict[str, Any]] = []
start_bias_feature_classes: list[Dict[str, Any]] = []
start_bias_adjacent_to_coast: list[Dict[str, Any]] = []

# Visual arts
vis_art_civilization_building_cultures: list[Dict[str, Any]] = []
vis_art_civilization_unit_cultures: list[Dict[str, Any]] = []

# Localizations (multi-language)
localizations: list[Dict[str, Any]] = []
```

#### Example

```python
civ = CivilizationBuilder({
    "civilization": {
        "civilization_type": "CIVILIZATION_ROME",
        "civilization_name": "CIVILIZATION_ROME",
        "base_tourism": 5,
    },
    "civilization_traits": [Trait.ECONOMIC],
    "start_bias_biomes": [{"biome": "BIOME_PLAINS"}],
    "localizations": [{
        "name": "Rome",
        "description": "Ancient Roman Empire",
        "full_name": "The Roman Empire",
        "adjective": "Roman",
        "city_names": ["Rome", "Milan", "Venice"]
    }]
})
```

---

### UnitBuilder

Create custom military and civilian units.

#### Constructor

```python
UnitBuilder(payload: Dict[str, Any] | None = None)
```

#### Properties

```python
# Unit definition
unit: Dict[str, Any] = {}

# Combat statistics
unit_stats: Dict[str, Any] = {}

# Production costs
unit_costs: Dict[str, Any] = {}

# Abilities
unit_abilities: list[Dict[str, Any]] = []

# Upgrades
unit_upgrades: list[Dict[str, Any]] = []

# Advisories (help text)
unit_advisories: list[Dict[str, Any]] = []

# Localizations
localizations: list[Dict[str, Any]] = []
```

#### Example

```python
unit = UnitBuilder({
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
```

---

### ConstructibleBuilder

Create buildings, improvements, and districts.

#### Constructor

```python
ConstructibleBuilder(payload: Dict[str, Any] | None = None)
```

#### Properties

```python
# Building/improvement/quarter definition
building: Dict[str, Any] = {}
improvement: Dict[str, Any] = {}
unique_quarter: Dict[str, Any] = {}

# Production cost
production_cost: int = 0
resource_cost: list[Dict[str, Any]] = []

# Yields and maintenance
constructible_yield_changes: list[Dict[str, Any]] = []
maintenance: Dict[str, int] = {}

# Plunder
constructible_plunders: list[Dict[str, Any]] = []

# Validity constraints
constructible_valid_resources: list[Dict[str, Any]] = []
constructible_valid_biomes: list[Dict[str, Any]] = []
constructible_valid_features: list[Dict[str, Any]] = []
constructible_valid_terrains: list[Dict[str, Any]] = []

# Adjacency bonuses
adjacency_yield_changes: list[Dict[str, Any]] = []

# Localizations
localizations: list[Dict[str, Any]] = []
```

#### Example

```python
building = ConstructibleBuilder({
    "building": {
        "building_type": "BUILDING_TEMPLE",
        "building_name": "BUILDING_TEMPLE",
        "building_class": ConstructibleClass.ECONOMIC,
    },
    "production_cost": 150,
    "constructible_yield_changes": [{
        "yield_type": Yield.FAITH,
        "yield_change": 4,
    }],
    "maintenance": {YIELD.GOLD: 1},
    "localizations": [{
        "name": "Temple",
        "description": "Provides Faith"
    }]
})
```

---

### Other Builders

#### ProgressionTreeBuilder

Create tech trees and civic progression trees.

```python
tree = ProgressionTreeBuilder({
    "progression_tree_type": "PROGRESSION_TREE_TECHNOLOGY",
    "progression_tree_nodes": [
        {
            "progression_tree_node_type": "NODE_BRONZE_WORKING",
            "row": 1,
            "column": 1,
        }
    ],
    "localizations": [{...}]
})
```

#### ModifierBuilder

Create game modifiers and effects.

```python
modifier = ModifierBuilder({
    "collection": COLLECTION.PLAYER_UNITS,
    "effect": EFFECT.UNIT_ADJUST_MOVEMENT,
    "arguments": [{"name": "Amount", "value": 2}],
    "localizations": [{...}]
})
```

#### UniqueQuarterBuilder

Create unique district quarters.

```python
quarter = UniqueQuarterBuilder({
    "unique_quarter": {"unique_quarter_type": "QUARTER_CUSTOM"},
    "constructible_yield_changes": [{...}],
    "localizations": [{...}]
})
```

#### LeaderUnlockBuilder

Bind leaders to civilizations with bonuses.

```python
leader = LeaderUnlockBuilder({
    "leader": "LEADER_CLEOPATRA",
    "civilization": "CIVILIZATION_EGYPT",
    "localizations": [{...}]
})
```

#### ImportFileBuilder

Import external files (images, SQL, etc).

```python
import_file = ImportFileBuilder({
    "source_path": "./assets/custom_icon.png",
    "target_name": "my_custom_icon"  # Output filename
})
```

---

## Path Generation & File Naming

### Path Generation

Builders automatically generate file paths using the `trim()` and `kebab_case()` utilities:

```python
from civ7_modding_tools.utils import trim, kebab_case

# Automatic path generation in builders:
# CIVILIZATION_GONDOR → trim → GONDOR → kebab_case → gondor
# Path result: /civilizations/gondor/

# UNIT_GONDOR_SCOUT → trim → GONDOR_SCOUT → kebab_case → gondor-scout
# Path result: /units/gondor-scout/
```

**Path Generation Pattern:**
1. Remove entity type prefix (`CIVILIZATION_`, `UNIT_`, `BUILDING_`, etc.)
2. Convert remaining name to kebab-case (lowercase with hyphens for underscores)
3. Use as path segment in mod structure

### File Naming Convention

All builders generate standardized XML filenames:

- `always.xml` - Core entity data
- `current.xml` - Main content (tech trees, civilizations)
- `game-effects.xml` - Game modifiers and effects
- `icons.xml` - Icon asset definitions
- `localization.xml` - Localization data
- `legacy.xml` - Legacy game data (civilizations)
- `shell.xml` - Shell/framework data (civilizations)
- `unlocks.xml` - Unlock configurations (civilizations)
- `visual-remap.xml` - Visual remapping (units)

### ImportFileBuilder Naming

Use `target_name` to control the output filename:

```python
# Source: ./assets/civ_icon.png → Output: imports/civ_sym_gondor
import_file = ImportFileBuilder({
    "source_path": "./assets/civ_icon.png",
    "target_name": "civ_sym_gondor"
})

# Without target_name: uses source filename
```

---

## Nodes

Nodes represent XML elements in the generated mod files.

### BaseNode

Abstract base class for all nodes.

#### Methods

**`fill(payload: Dict[str, Any]) -> Self`**

Set node properties from dictionary.

**`to_xml_element() -> dict | None`**

Convert node to XML element dictionary.

**`insert_or_ignore() -> Self`**

Transform to INSERT OR IGNORE statement.

#### Properties

- `_name: str = "Row"` - XML element name

---

### DatabaseNode

Master container for database table rows.

#### Properties

```python
# Properties for each entity type
civilizations: list[BaseNode] = []
civilization_traits: list[BaseNode] = []
units: list[BaseNode] = []
unit_stats: list[BaseNode] = []
constructibles: list[BaseNode] = []
modifiers: list[BaseNode] = []
# ... 67 total properties
```

---

### Specialized Nodes

#### CivilizationNode

```python
civilization_type: str
civilization_name: str
base_tourism: int = 0
legacy_modifier: bool = False
```

#### UnitNode

```python
unit_type: str
unit_name: str
unit_class: str
unit_movement_class: str
base_movement: int
base_sight: int
```

#### ConstructibleNode

```python
constructible_type: str
constructible_name: str
production_cost: int
```

---

## Localizations

Localization classes provide multi-language support.

### BaseLocalization

Base class for all localizations.

#### Properties

- `name: str` - Localized name
- `description: str` - Localized description

### Specialized Localizations

#### CivilizationLocalization

```python
CivilizationLocalization(
    name: str,                    # Civilization name
    description: str = "",        # Description
    full_name: str = "",          # Full formal name
    adjective: str = "",          # Demonym (e.g., "Roman")
    city_names: list[str] = []   # City name suggestions
)
```

#### UnitLocalization

```python
UnitLocalization(
    name: str,
    description: str = "",
    type_name: str = ""
)
```

#### ConstructibleLocalization

```python
ConstructibleLocalization(
    name: str,
    description: str = "",
    effect_name: str = ""
)
```

---

## Constants

Type-safe constants for game entities.

### Civilization Constants

```python
Trait                      # Civilization traits (ECONOMIC, CULTURAL, MILITARY, etc.)
TagTrait                   # Trait tags for categorization
```

### Unit Constants

```python
UnitClass                  # Unit types (MELEE, RECON, etc)
UnitMovementClass         # Movement types (LAND, WATER, AIR)
UnitCulture               # Unit cultures
```

### Constructible Constants

```python
ConstructibleTypeTag      # Building/improvement categories
ConstructibleClass        # Building class types
District                  # Districts for quarters
```

### Game Constants

```python
Effect                    # Game modifiers
Requirement               # Conditions and checks
RequirementSet            # Requirement grouping logic
Collection                # Entity collections for modifiers
Yield                     # Resource types (GOLD, CULTURE, etc)
Age                       # Game eras
ActionGroup               # Action groups for mod loading
ActionGroupAction         # Action group actions
Advisory                  # Help text categories
```

### Map Constants

```python
Terrain                   # Terrain types
Biome                     # Biome types
Feature                   # Map features
FeatureClass              # Feature categories
Resource                  # Resource types
```

### Other Constants

```python
Icon                      # Icon identifiers
Language                  # Supported languages
Domain                    # Unit domains (LAND, SEA, AIR)
CivilizationDomain        # Civilization domain types
Plunder                   # Plunder types for conquered entities
```

---

## Files

### BaseFile

Abstract base class for output files.

#### Properties

```python
path: str = "/"                    # Directory path
name: str = "file.txt"             # Filename
content: Any = None                # File content
action_groups: list[str] = []      # Action group IDs
action_group_actions: list[str] = []  # Action types
```

#### Methods

**`write(dist: str) -> None`**

Write file to disk.

### XmlFile

XML file generator for mod files.

```python
file = XmlFile(
    path="/civilizations/rome/",
    name="current.xml",
    content=nodes_or_dict
)
```

### ImportFile

Import external files into the mod.

```python
file = ImportFile(
    path="/imports/",
    name="custom_icon",
    content="./assets/icon.png"
)
```

---

## Utilities

### fill()

Fill object properties from dictionary (fluent API).

```python
def fill(obj: T, payload: Dict[str, Any]) -> T:
    """Fill object properties and return for chaining."""
```

### without()

Remove items from list.

```python
def without(lst: list[T], *values: T) -> list[T]:
    """Return list without specified values."""

result = without([1, 2, 3, 2], 2)  # [1, 3]
```

### uniq_by()

Get unique items based on key function.

```python
def uniq_by(
    lst: list[T],
    key_func: Callable[[T], Any] | None = None
) -> list[T]:
    """Return unique items (preserves order)."""

# By identity
uniq_by([1, 2, 2, 3])  # [1, 2, 3]

# By key function
uniq_by(
    [{"id": 1}, {"id": 1}, {"id": 2}],
    key_func=lambda x: x["id"]
)  # [{"id": 1}, {"id": 2}]
```

### camel_to_pascal()

Convert camelCase to PascalCase.

```python
def camel_to_pascal(name: str) -> str:
    """civilizationType -> CivilizationType"""
```

### start_case()

Convert camelCase to Start Case.

```python
def start_case(name: str) -> str:
    """myProperty -> My Property"""
```

---

## Type Hints

All classes and functions have full type hints for IDE support:

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    UnitBuilder,
    Trait,
    UnitClass,
)

mod: Mod = Mod(id="my-mod")
builder: CivilizationBuilder = CivilizationBuilder()
mod.add(builder)
mod.build("./dist")
```

---

## Error Handling

### Common Errors

**ImportError: No module named 'civ7_modding_tools'**

Solution: Install the package with `pip install civ7-modding-tools`

**AttributeError: 'dict' object has no attribute 'build'**

Solution: Ensure you're calling `mod.build()` on a `Mod` object, not a dictionary

**FileNotFoundError: Output directory doesn't exist**

Solution: The library creates directories automatically, ensure write permissions

---

## Performance

- **Typical mod generation**: <100ms
- **Test suite (324 tests)**: <1s
- **File I/O dominates**: Most time spent writing files to disk

---

## More Information

- **GitHub**: https://github.com/Phlair/civ7-modding-tools
- **Getting Started**: See [GUIDE.md](GUIDE.md)
- **Examples**: See [EXAMPLES.md](EXAMPLES.md)
- **Migration**: See [MIGRATION.md](MIGRATION.md)

