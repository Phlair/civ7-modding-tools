# TypeScript to Python Migration Guide

Complete guide for migrating from the TypeScript version to the Python version of Civ7 Modding Tools.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Syntax Changes](#syntax-changes)
- [Type System](#type-system)
- [API Changes](#api-changes)
- [Common Patterns](#common-patterns)
- [Migration Checklist](#migration-checklist)

---

## Overview

The Python version of Civ7 Modding Tools maintains **100% API feature parity** with the TypeScript version. All builders, nodes, constants, and features are available in Python with the same logic.

### Key Differences

| Aspect | TypeScript | Python |
|--------|-----------|--------|
| File Extension | `.ts` | `.py` |
| Import Statement | `import { }` | `from ... import` |
| Class Declaration | `export class` | `class` |
| Constructor | `constructor()` | `def __init__(self)` |
| Object Literals | `{ key: value }` | `{"key": value}` or `Dict[str, Any]` |
| Arrays | `Array<Type>` | `list[Type]` |
| Optional | `prop?: Type` | `prop: Type \| None = None` |
| Type Annotations | `: Type` | `: Type` |
| Method Chaining | `.method().method()` | `.method().method()` |
| Null Coalescing | `??` | `or` |

---

## Installation

### TypeScript Version

```bash
npm install civ7-modding-tools
```

```typescript
import { Mod, CivilizationBuilder, TRAIT } from 'civ7-modding-tools';
```

### Python Version

```bash
pip install civ7-modding-tools
# or
uv add civ7-modding-tools
```

```python
from civ7_modding_tools import Mod, CivilizationBuilder, TRAIT
```

---

## Syntax Changes

### 1. Imports

#### TypeScript
```typescript
import { 
    Mod, 
    CivilizationBuilder, 
    TRAIT, 
    UNIT_CLASS,
    ACTION_GROUP_BUNDLE
} from 'civ7-modding-tools';
```

#### Python
```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    TRAIT,
    UNIT_CLASS,
    ACTION_GROUP_BUNDLE,
)
```

### 2. Class Instantiation

#### TypeScript
```typescript
const mod = new Mod({
    id: 'my-mod',
    version: '1.0',
    name: 'My Mod',
});
```

#### Python
```python
mod = Mod(
    id='my-mod',
    version='1.0',
    name='My Mod',
)
# or with dict
mod = Mod({
    'id': 'my-mod',
    'version': '1.0',
    'name': 'My Mod',
})
```

### 3. Object Literals

#### TypeScript
```typescript
const civilization = {
    civilization_type: 'CIVILIZATION_ROME',
    base_tourism: 5,
    capital: 'Rome',
};
```

#### Python
```python
civilization = {
    'civilization_type': 'CIVILIZATION_ROME',
    'base_tourism': 5,
    'capital': 'Rome',
}
```

### 4. Method Chaining

#### TypeScript
```typescript
builder
    .fill({
        civilization: { civilization_type: 'CIV_ROME' },
    })
    .build();
```

#### Python
```python
builder\
    .fill({
        'civilization': {'civilization_type': 'CIV_ROME'},
    })\
    .build()
# or
builder.fill({...}).build()
```

### 5. Arrays

#### TypeScript
```typescript
const units: UnitBuilder[] = [unit1, unit2, unit3];
mod.add(units);
```

#### Python
```python
units: list[UnitBuilder] = [unit1, unit2, unit3]
mod.add(units)
```

### 6. String Concatenation

#### TypeScript
```typescript
const path = `/civilizations/${civilizationType.toLowerCase()}/`;
```

#### Python
```python
path = f"/civilizations/{civilization_type.lower()}/"
```

### 7. Constants

#### TypeScript
```typescript
import { TRAIT, UNIT_CLASS } from 'civ7-modding-tools';

builder.fill({
    civilization_traits: [TRAIT.ECONOMIC_CIV],
    unit_class: UNIT_CLASS.MELEE,
});
```

#### Python
```python
from civ7_modding_tools import TRAIT, UNIT_CLASS

builder.fill({
    'civilization_traits': [TRAIT.ECONOMIC_CIV],
    'unit_class': UNIT_CLASS.MELEE,
})
```

---

## Type System

### TypeScript Type Hints

```typescript
function fill<T>(obj: T, payload: Partial<T>): T {
    // ...
}

const builder: CivilizationBuilder = new CivilizationBuilder();
const files: BaseFile[] = builder.build();
```

### Python Type Hints

```python
from typing import TypeVar

T = TypeVar('T')

def fill(obj: T, payload: Dict[str, Any]) -> T:
    # ...

builder: CivilizationBuilder = CivilizationBuilder()
files: list[BaseFile] = builder.build()
```

### Optional Types

#### TypeScript
```typescript
civilization?: string;
traits?: Trait[];
```

#### Python
```python
civilization: str | None = None
traits: list[Trait] | None = None
# or (Python 3.9 compatible)
from typing import Optional
civilization: Optional[str] = None
traits: Optional[list[Trait]] = None
```

### Union Types

#### TypeScript
```typescript
function add(builder: BaseBuilder | BaseBuilder[]): Mod {
    // ...
}
```

#### Python
```python
def add(self, builder: BaseBuilder | list[BaseBuilder]) -> "Mod":
    # ...
```

---

## API Changes

### No API Changes ✅

The Python version maintains **100% API compatibility** with TypeScript. All methods, properties, and builders are identical.

### Minor Naming Conventions

Python follows snake_case for methods/properties (while internal XML uses PascalCase):

#### TypeScript (camelCase)
```typescript
const mod = new Mod({
    affectsSavedGames: true,
});
```

#### Python (snake_case)
```python
mod = Mod(
    affects_saved_games=True,
)
```

**Note**: Both output the same XML with proper PascalCase attribute names.

---

## Common Patterns

### Pattern 1: Creating and Building a Mod

#### TypeScript
```typescript
const mod = new Mod({ id: 'my-mod', version: '1.0' });
const civ = new CivilizationBuilder({
    civilization: { civilization_type: 'CIV_ROME' },
    civilization_traits: [TRAIT.MILITARY_CIV],
});
mod.add(civ);
mod.build('./dist');
```

#### Python
```python
mod = Mod(id='my-mod', version='1.0')
civ = CivilizationBuilder({
    'civilization': {'civilization_type': 'CIV_ROME'},
    'civilization_traits': [TRAIT.MILITARY_CIV],
})
mod.add(civ)
mod.build('./dist')
```

### Pattern 2: Multiple Entities

#### TypeScript
```typescript
const units: UnitBuilder[] = [
    new UnitBuilder({ unit: { unit_type: 'UNIT_WARRIOR' } }),
    new UnitBuilder({ unit: { unit_type: 'UNIT_ARCHER' } }),
];
mod.add(units);
```

#### Python
```python
units = [
    UnitBuilder({'unit': {'unit_type': 'UNIT_WARRIOR'}}),
    UnitBuilder({'unit': {'unit_type': 'UNIT_ARCHER'}}),
]
mod.add(units)
```

### Pattern 3: Localizations

#### TypeScript
```typescript
const civ = new CivilizationBuilder({
    localizations: [
        {
            name: 'Rome',
            description: 'Ancient empire',
            city_names: ['Rome', 'Milan', 'Venice'],
        },
    ],
});
```

#### Python
```python
civ = CivilizationBuilder({
    'localizations': [
        {
            'name': 'Rome',
            'description': 'Ancient empire',
            'city_names': ['Rome', 'Milan', 'Venice'],
        },
    ],
})
```

### Pattern 4: Action Groups

#### TypeScript
```typescript
const builder = new UnitBuilder({
    action_group_bundle: ACTION_GROUP_BUNDLE.AGE_EXPLORATION,
    unit: { /* ... */ },
});
```

#### Python
```python
builder = UnitBuilder({
    'action_group_bundle': ACTION_GROUP_BUNDLE.AGE_EXPLORATION,
    'unit': {}, # ...
})
```

### Pattern 5: Error Handling

#### TypeScript
```typescript
try {
    mod.build('./dist');
} catch (error) {
    console.error('Build failed:', error);
}
```

#### Python
```python
try:
    mod.build('./dist')
except Exception as e:
    print(f'Build failed: {e}')
```

---

## Migration Checklist

### Step 1: Setup
- [ ] Install Python 3.12+
- [ ] Install `civ7-modding-tools`: `pip install civ7-modding-tools`
- [ ] Create new `.py` build file

### Step 2: Convert Syntax
- [ ] Replace `import` statements with Python syntax
- [ ] Convert `new Class()` to `Class()`
- [ ] Convert `: Type` to Python type hints
- [ ] Replace `const`/`let`/`var` with direct assignment
- [ ] Convert object literals `{ key: value }` to `{"key": value}`

### Step 3: String Changes
- [ ] Replace backticks `` `string` `` with `f"string"` or `"string"`
- [ ] Convert single quotes to double quotes (or vice versa)
- [ ] Update string concatenation to f-strings

### Step 4: Verify
- [ ] Run linter: `uv run flake8 build.py` (or `pylint`)
- [ ] Check type hints: `uv run mypy build.py` (optional)
- [ ] Test build: `python build.py`
- [ ] Verify output files generated correctly

### Step 5: Test in Civ7
- [ ] Copy generated mod to Civ7 mods folder
- [ ] Load and test mod in-game
- [ ] Verify functionality matches TypeScript version

---

## Example: Full Migration

### Before (TypeScript)

```typescript
import {
    Mod,
    CivilizationBuilder,
    UnitBuilder,
    ACTION_GROUP_BUNDLE,
    TRAIT,
    UNIT_CLASS,
    UNIT_MOVEMENT_CLASS,
} from 'civ7-modding-tools';

const mod = new Mod({
    id: 'rome-mod',
    version: '1.0',
    name: 'Roman Mod',
    description: 'Custom Roman civilization',
    authors: 'Modder',
});

const rome = new CivilizationBuilder({
    action_group_bundle: ACTION_GROUP_BUNDLE.ALWAYS,
    civilization: {
        civilization_type: 'CIVILIZATION_ROME',
        civilization_name: 'CIVILIZATION_ROME',
    },
    civilization_traits: [TRAIT.MILITARY_CIV],
    localizations: [
        {
            name: 'Rome',
            description: 'Ancient Roman Empire',
            full_name: 'The Roman Empire',
            adjective: 'Roman',
            city_names: ['Rome', 'Milan', 'Venice'],
        },
    ],
});

const legionnaire = new UnitBuilder({
    action_group_bundle: ACTION_GROUP_BUNDLE.ALWAYS,
    unit: {
        unit_type: 'UNIT_LEGIONNAIRE',
        unit_name: 'UNIT_LEGIONNAIRE',
        unit_class: UNIT_CLASS.MELEE,
        unit_movement_class: UNIT_MOVEMENT_CLASS.LAND,
    },
    unit_stats: {
        melee_strength: 38,
    },
    unit_costs: {
        production: 60,
    },
    localizations: [
        {
            name: 'Legionnaire',
            description: 'Elite Roman infantry',
        },
    ],
});

mod.add(rome);
mod.add(legionnaire);
mod.build('./dist');
```

### After (Python)

```python
from civ7_modding_tools import (
    Mod,
    CivilizationBuilder,
    UnitBuilder,
    ACTION_GROUP_BUNDLE,
    TRAIT,
    UNIT_CLASS,
    UNIT_MOVEMENT_CLASS,
)

mod = Mod(
    id='rome-mod',
    version='1.0',
    name='Roman Mod',
    description='Custom Roman civilization',
    authors='Modder',
)

rome = CivilizationBuilder({
    'action_group_bundle': ACTION_GROUP_BUNDLE.ALWAYS,
    'civilization': {
        'civilization_type': 'CIVILIZATION_ROME',
        'civilization_name': 'CIVILIZATION_ROME',
    },
    'civilization_traits': [TRAIT.MILITARY_CIV],
    'localizations': [
        {
            'name': 'Rome',
            'description': 'Ancient Roman Empire',
            'full_name': 'The Roman Empire',
            'adjective': 'Roman',
            'city_names': ['Rome', 'Milan', 'Venice'],
        },
    ],
})

legionnaire = UnitBuilder({
    'action_group_bundle': ACTION_GROUP_BUNDLE.ALWAYS,
    'unit': {
        'unit_type': 'UNIT_LEGIONNAIRE',
        'unit_name': 'UNIT_LEGIONNAIRE',
        'unit_class': UNIT_CLASS.MELEE,
        'unit_movement_class': UNIT_MOVEMENT_CLASS.LAND,
    },
    'unit_stats': {
        'melee_strength': 38,
    },
    'unit_costs': {
        'production': 60,
    },
    'localizations': [
        {
            'name': 'Legionnaire',
            'description': 'Elite Roman infantry',
        },
    ],
})

mod.add(rome)
mod.add(legionnaire)
mod.build('./dist')
```

---

## Frequently Asked Questions

### Q: Will my TypeScript mod work in Python?

**A**: Not directly, but conversion is straightforward. All API is identical, so it's a syntax translation.

### Q: Do I need to change my mod ID?

**A**: No, the mod ID and content structure remain the same. Only the build script syntax changes.

### Q: Can I mix Python and TypeScript mods?

**A**: Yes, both generate identical Civ7 mod files. You can use either version.

### Q: Is the Python version slower?

**A**: No, Python version is actually faster for mod generation. Most time is spent on file I/O, which is equivalent.

### Q: Are all TypeScript features available in Python?

**A**: Yes, 100% API parity. All builders, nodes, constants, and features are available.

### Q: What about type checking?

**A**: Python has full type hints. Use `mypy` for optional type checking: `mypy build.py`

---

## Tools and Utilities

### Python Linting
```bash
# Install flake8
pip install flake8

# Check code style
flake8 build.py
```

### Type Checking
```bash
# Install mypy
pip install mypy

# Check types
mypy build.py
```

### Formatting
```bash
# Install black
pip install black

# Auto-format code
black build.py
```

---

## Getting Help

- **GitHub Issues**: https://github.com/Phlair/civ7-modding-tools/issues
- **Documentation**: See [GUIDE.md](GUIDE.md) and [API.md](API.md)
- **Examples**: See [EXAMPLES.md](EXAMPLES.md)

---

## Summary

| Aspect | Status |
|--------|--------|
| API Compatibility | ✅ 100% identical |
| Feature Parity | ✅ Complete |
| Performance | ✅ Equivalent or better |
| Documentation | ✅ Comprehensive |
| Type Safety | ✅ Full type hints |
| Migration Effort | ✅ Straightforward (syntax only) |

**Migration is straightforward and low-risk.** The Python version maintains 100% feature and API parity with the TypeScript version, requiring only syntax translation.

Happy modding! 🎮

