# TypeScript to Python Migration Guide

This guide helps users transition from the TypeScript implementation to the new Python implementation of civ7-modding-tools.

## Good News! 🎉

**100% output parity**: The Python implementation generates **identical** mod files as the TypeScript version. Your mods will work exactly the same way.

## Key Differences

### Package Installation

**TypeScript (Old)**:
```bash
npm install civ7-modding-tools
```

**Python (New)**:
```bash
uv add civ7-modding-tools
# or
pip install civ7-modding-tools
```

### Import Statements

**TypeScript**:
```typescript
import { Mod, CivilizationBuilder, Trait } from 'civ7-modding-tools';
```

**Python**:
```python
from civ7_modding_tools import Mod, CivilizationBuilder, Trait
```

### Constructor Syntax

**TypeScript**:
```typescript
const mod = new Mod({
    id: 'my-mod',
    version: '1.0',
    name: 'My Mod'
});
```

**Python**:
```python
mod = Mod(id='my-mod', version='1.0', name='My Mod')
```

### Builder Construction

**TypeScript**:
```typescript
const unit = new UnitBuilder({
    actionGroupBundle: ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
    unit: {
        unitType: 'UNIT_CUSTOM_SCOUT',
        baseMoves: 2
    }
});
```

**Python**:
```python
unit = UnitBuilder({
    'action_group_bundle': ActionGroupBundle.AGE_ANTIQUITY,
    'unit': {
        'unit_type': 'UNIT_CUSTOM_SCOUT',
        'base_moves': 2
    }
})
```

### Constants

**TypeScript**:
```typescript
import { Trait, UnitClass, Effect } from 'civ7-modding-tools';
```

**Python**:
```python
from civ7_modding_tools.constants import Trait, UnitClass, Effect
```

### Array vs List

**TypeScript**:
```typescript
mod.add([unit1, unit2, building]);
```

**Python**:
```python
mod.add([unit1, unit2, building])
```

Same syntax! Lists in Python work identically.

### Method Chaining

**TypeScript**:
```typescript
mod.add(unit).build('./dist');
```

**Python**:
```python
mod.add(unit)
mod.build('./dist')
```

Note: Method chaining not supported in Python version. Call methods sequentially instead.

### Mod Building

**TypeScript**:
```typescript
mod.build('./dist');
```

**Python**:
```python
mod.build('./dist')
```

Both generate identical output in the specified directory.

## Type System

**TypeScript**:
- Built-in static typing (compiled to JavaScript)
- Checked at compile time
- IDE autocomplete for properties

**Python**:
- Type hints via `pydantic` models
- Checked at runtime (optional static checking with `mypy`)
- IDE autocomplete for properties
- More flexible runtime behavior

## Running Your Code

**TypeScript**:
```bash
npm install
npm run build
# or
tsx build.ts
```

**Python**:
```bash
uv sync
uv run your_script.py
# or
python your_script.py
```

## Common Migration Patterns

### Pattern 1: Simple Civilization

**TypeScript**:
```typescript
const civ = new CivilizationBuilder({
    civilization: {
        civilizationType: 'CIVILIZATION_CUSTOM'
    },
    civilizationTraits: [TRAIT.ECONOMIC],
    localizations: [{
        name: 'Custom Civilization',
        cityNames: ['Capital', 'Secondary']
    }]
});
```

**Python**:
```python
civ = CivilizationBuilder({
    'civilization': {
        'civilization_type': 'CIVILIZATION_CUSTOM'
    },
    'civilization_traits': [Trait.ECONOMIC],
    'localizations': [{
        'name': 'Custom Civilization',
        'city_names': ['Capital', 'Secondary']
    }]
})
```

### Pattern 2: Multiple Builders

**TypeScript**:
```typescript
mod.add([unit, building, civ]);
```

**Python**:
```python
mod.add([unit, building, civ])
```

### Pattern 3: File Imports

**TypeScript**:
```typescript
const icon = new ImportFileBuilder({
    source: './assets/icon.png',
    targetName: 'civilizations/custom/icon.png'
});
```

**Python**:
```python
icon = ImportFileBuilder({
    'source': './assets/icon.png',
    'target_name': 'civilizations/custom/icon.png'
})
```

## Full Migration Example

**TypeScript**:
```typescript
import { Mod, CivilizationBuilder, UnitBuilder, TRAIT, UNIT_CLASS } from 'civ7-modding-tools';

const mod = new Mod({
    id: 'gondor',
    version: '1.0',
    name: 'Gondor Civilization'
});

const civ = new CivilizationBuilder({
    civilization: { civilizationType: 'CIVILIZATION_GONDOR' },
    civilizationTraits: [TRAIT.MILITARY, TRAIT.DIPLOMATIC],
    localizations: [{ name: 'Gondor', cityNames: ['Minas Tirith'] }]
});

const unit = new UnitBuilder({
    unit: { unitType: 'UNIT_GONDOR_SOLDIER', unitClass: UNIT_CLASS.MELEE },
    localizations: [{ name: 'Gondor Soldier' }]
});

mod.add([civ, unit]).build('./dist');
```

**Python**:
```python
from civ7_modding_tools import Mod
from civ7_modding_tools.builders import CivilizationBuilder, UnitBuilder
from civ7_modding_tools.constants import Trait, UnitClass

mod = Mod(id='gondor', version='1.0', name='Gondor Civilization')

civ = CivilizationBuilder({
    'civilization': {'civilization_type': 'CIVILIZATION_GONDOR'},
    'civilization_traits': [Trait.MILITARY, Trait.DIPLOMATIC],
    'localizations': [{'name': 'Gondor', 'city_names': ['Minas Tirith']}]
})

unit = UnitBuilder({
    'unit': {'unit_type': 'UNIT_GONDOR_SOLDIER', 'unit_class': UnitClass.MELEE},
    'localizations': [{'name': 'Gondor Soldier'}]
})

mod.add([civ, unit])
mod.build('./dist')
```

## Migration Checklist

- [ ] Install Python package: `uv add civ7-modding-tools`
- [ ] Update imports from `'civ7-modding-tools'` to `from civ7_modding_tools import ...`
- [ ] Convert `new ClassName({})` to `ClassName({})`
- [ ] Change camelCase properties to snake_case (e.g., `unitType` → `unit_type`)
- [ ] Change string constants to enum imports (e.g., `'TRAIT_MILITARY'` → `Trait.MILITARY`)
- [ ] Remove method chaining, call methods sequentially
- [ ] Test that mod builds: `python your_script.py`
- [ ] Verify generated mod files are identical

## Still Have Questions?

- **Getting Started**: Read [GUIDE.md](GUIDE.md)
- **API Reference**: See [API.md](API.md)
- **Examples**: Check [examples/](../examples/) folder
- **Full Index**: See [INDEX.md](INDEX.md)

## Why Python?

- Better performance for mod generation
- Simpler dependency management (`pip`/`uv` vs `npm`)
- Native support for file operations
- Type hints with `pydantic` for validation
- Easier cross-platform support
- Smaller binary footprint
- No Node.js runtime required
