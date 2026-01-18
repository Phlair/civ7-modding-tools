# Documentation Index - Phlair's Civ VII Modding Tools

Welcome to the comprehensive documentation for **Phlair's Civ VII Modding Tools**, a Python library for programmatically creating Civilization VII mods.

> **Attribution**: This project is a complete rework of the original codebase. Original fork from [izica](https://github.com/izica).

## 📚 Documentation Guide

### [Getting Started Guide](GUIDE.md) 🚀
**Start here if you're new to the library**

Complete beginner-friendly guide covering:
- Installation and setup
- Your first civilization mod (5-minute tutorial)
- Core concepts explained
- Builder pattern walkthrough
- Common patterns and best practices
- Troubleshooting common issues

**Time to complete**: 30-60 minutes for beginners

### [API Reference](API.md) 📖
**Complete technical reference**

Comprehensive API documentation:
- All 13 builder classes with examples
- 79 node types fully documented
- 21 constant enums (Trait, UnitClass, Effect, Yield, etc.)
- 11 localization classes
- Utility functions (locale(), fill(), trim(), etc.)
- Full type signatures

**Use when**: You need detailed technical information about a specific class or method

### [Examples](EXAMPLES.md) 💡
**Practical, ready-to-use code examples**

Working examples covering:
- Simple civilization (minimal setup)
- Complete civilization (all features)
- Custom units with abilities
- Buildings and improvements
- Progression trees (civics/tech)
- Game modifiers and effects
- Asset imports
- Multi-entity mods

**Use when**: You want to copy/adapt working code for your mod

### [Migration Guide](MIGRATION.md) 🔄
**For TypeScript users**

Porting guide from TypeScript version:
- Syntax differences (camelCase → snake_case)
- Type system comparison
- Side-by-side code examples
- Full migration walkthrough
- Common pitfalls

**Use when**: Migrating from the TypeScript implementation

---

## 🎯 Quick Navigation by Task

### I want to...

#### Create my first mod
1. **Read**: [Getting Started Guide - Your First Mod](GUIDE.md#your-first-mod)
2. **Run**: Copy the code and execute it
3. **Verify**: Check the generated files in `./dist/`

#### Create a civilization
1. **Example**: [Simple Civilization](EXAMPLES.md#example-1-simple-civilization)
2. **API Reference**: [CivilizationBuilder](API.md#civilizationbuilder)
3. **Constants**: [Trait enums](API.md#trait)

#### Add custom units
1. **Example**: [Custom Unit](EXAMPLES.md#example-3-custom-unit-with-abilities)
2. **API Reference**: [UnitBuilder](API.md#unitbuilder)
3. **Constants**: [UnitClass enums](API.md#unitclass)

#### Add buildings or improvements
1. **Example**: [Buildings](EXAMPLES.md#example-2-complete-civilization)
2. **API Reference**: [ConstructibleBuilder](API.md#constructiblebuilder)
3. **Constants**: [Yield enums](API.md#yield)

#### Create progression trees (civics/tech)
1. **Example**: [Progression Tree](EXAMPLES.md#example-4-building-a-tech-tree)
2. **API Reference**: [ProgressionTreeBuilder](API.md#progressiontreebuilder)
3. **Related**: [ProgressionTreeNodeBuilder](API.md#progressiontreenodebuilder)

#### Import custom assets (icons, SQL)
1. **Example**: [Asset Imports](EXAMPLES.md#example-6-importing-external-assets)
2. **API Reference**: [ImportFileBuilder](API.md#importfilebuilder)

#### Add game modifiers/effects
1. **Example**: [Modifiers and Effects](EXAMPLES.md#example-5-game-modifiers-and-effects)
2. **API Reference**: [ModifierBuilder](API.md#modifierbuilder)
3. **Constants**: [Effect enums](API.md#effect)

#### Understand action groups (age loading)
1. **Guide**: [Action Groups](GUIDE.md#action-groups)
2. **API**: [ActionGroupBundle](API.md#actiongroupbundle)
3. **Example**: See any civilization example

#### Create unique quarters (districts)
1. **Example**: [Unique Quarter](EXAMPLES.md#unique-quarter-example)
2. **API Reference**: [UniqueQuarterBuilder](API.md#uniquequarterbuilder)

---

## 📖 Learning Path

### Beginner (30-60 minutes)
**Goal**: Create your first simple mod

1. Read [Getting Started Guide](GUIDE.md) (15 min)
2. Copy and run [Simple Civilization Example](EXAMPLES.md#example-1-simple-civilization) (5 min)
3. Modify the civilization name and rebuild (10 min)
4. Experiment with traits and city names (20 min)

**Outcome**: Working civilization mod with basic understanding

### Intermediate (2-4 hours)
**Goal**: Build a complete, feature-rich mod

1. Review [Core Concepts](GUIDE.md#core-concepts) (30 min)
2. Study [Complete Civilization Example](EXAMPLES.md#example-2-complete-civilization) (30 min)
3. Reference [API docs](API.md) for specific builders (60 min)
4. Build your own civilization with units and buildings (1-2 hours)

**Outcome**: Multi-entity mod with custom content

### Advanced (4+ hours)
**Goal**: Master all features and complex patterns

1. Study full [API Reference](API.md) (2 hours)
2. Review all [Examples](EXAMPLES.md) (1 hour)
3. Examine [babylon_civilization.py](../examples/babylon_civilization.py) source (30 min)
4. Experiment with modifiers, progression trees, AI config (1+ hour)

**Outcome**: Expert-level understanding, ability to create complex mods

### TypeScript Migrators (1-2 hours)
**Goal**: Port existing TypeScript mods to Python

1. Read [Migration Guide](MIGRATION.md) overview (15 min)
2. Study [syntax differences](MIGRATION.md#key-differences) (15 min)
3. Review [side-by-side comparison](MIGRATION.md#side-by-side-comparison) (20 min)
4. Follow [migration checklist](MIGRATION.md#migration-checklist) (20-40 min)

**Outcome**: Successfully ported mod

---

## 🔍 Reference by Component

### Core Classes
- [Mod](API.md#mod) - Main orchestrator
- [ActionGroupBundle](API.md#actiongroupbundle) - Age-based loading
- [BaseBuilder](API.md#basebuilder) - Builder base class

### Builders (13 classes)
- [CivilizationBuilder](API.md#civilizationbuilder)
- [UnitBuilder](API.md#unitbuilder)
- [ConstructibleBuilder](API.md#constructiblebuilder)
- [ProgressionTreeBuilder](API.md#progressiontreebuilder)
- [ProgressionTreeNodeBuilder](API.md#progressiontreenodebuilder)
- [ModifierBuilder](API.md#modifierbuilder)
- [TraditionBuilder](API.md#traditionbuilder)
- [UniqueQuarterBuilder](API.md#uniquequarterbuilder)
- [LeaderUnlockBuilder](API.md#leaderunlockbuilder)
- [CivilizationUnlockBuilder](API.md#civilizationunlockbuilder)
- [UnlockBuilder](API.md#unlockbuilder)
- [ImportFileBuilder](API.md#importfilebuilder)

### Constants (21 Enums)
- [Trait](API.md#trait) - Civilization traits
- [UnitClass](API.md#unitclass) - Unit classifications
- [Yield](API.md#yield) - Resource yields
- [Effect](API.md#effect) - Game effects
- [Requirement](API.md#requirement) - Game requirements
- [District](API.md#district) - District types
- [Age](API.md#age) - Game ages
- And more...

### Localizations (11 Classes)
- [CivilizationLocalization](API.md#civilizationlocalization)
- [UnitLocalization](API.md#unitlocalization)
- [ConstructibleLocalization](API.md#constructiblelocalization)
- [ProgressionTreeLocalization](API.md#progressiontreelocalization)
- And more...

### Files & Nodes
- [XmlFile](API.md#xmlfile) - XML file generation
- [ImportFile](API.md#importfile) - Asset imports
- [BaseNode](API.md#basenode) - XML element base class
- [79 specialized nodes](API.md#nodes)

### Utilities
- [locale()](API.md#locale) - Generate localization keys
- [fill()](API.md#fill) - Fill object properties
- [trim()](API.md#trim) - Remove prefixes
- [kebab_case()](API.md#kebab-case) - Convert to kebab-case
- And more...

---

## 🛠️ Common Workflows

### Creating a New Mod from Scratch

```python
# 1. Create mod container
from civ7_modding_tools import Mod

mod = Mod(
    id='my-mod',
    version='1.0.0',
    name='My Amazing Mod',
    authors='Your Name'
)

# 2. Create builders (civilization, units, buildings, etc.)
# See examples in EXAMPLES.md

# 3. Add builders to mod
mod.add([builder1, builder2, builder3])

# 4. Build output files
mod.build('./dist')
```

### Adding Content to Existing Mod

```python
# Create new builders
new_unit = UnitBuilder().fill({...})
new_building = ConstructibleBuilder().fill({...})

# Add to existing mod
mod.add([new_unit, new_building])

# Rebuild
mod.build('./dist')
```

### Testing Your Mod

```bash
# 1. Generate mod files
python my_mod.py

# 2. Copy to Civ VII mods folder
# (Location varies by platform)

# 3. Enable in game mod manager

# 4. Start new game to test
```

---

## ❓ Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'civ7_modding_tools'`
- **Solution**: Install the package: `pip install civ7-modding-tools`

**Problem**: XML files not generated
- **Solution**: Check `mod.build()` was called with valid path

**Problem**: Mod not appearing in game
- **Solution**: Verify `.modinfo` file exists and is valid XML

**Problem**: Type errors with constants
- **Solution**: Use `.value` on enum constants: `Trait.ECONOMIC.value`

**Problem**: Localization not working
- **Solution**: Ensure `localizations` list contains proper Pydantic models

See [Getting Started Guide - Troubleshooting](GUIDE.md#troubleshooting) for more details.

---

## 📦 Project Structure

```
civ7-modding-tools/
├── src/civ7_modding_tools/       # Source code
│   ├── core/                     # Mod orchestrator
│   ├── builders/                 # 13 builder classes
│   ├── nodes/                    # 79 node types
│   ├── files/                    # File generators
│   ├── localizations/            # 11 localization models
│   ├── constants/                # 21 enum classes
│   └── utils/                    # Utility functions
├── examples/                     # 8 working examples
├── tests/                        # 324 passing tests
├── docs/                         # Documentation (you are here)
│   ├── INDEX.md                  # This file
│   ├── GUIDE.md                  # Getting started guide
│   ├── API.md                    # API reference
│   ├── EXAMPLES.md               # Example code
│   └── MIGRATION.md              # TypeScript migration
└── README.md                     # Project overview
```

---

## 🤝 Contributing

Want to improve the documentation?

1. Fork the repository
2. Edit documentation files
3. Submit pull request

All documentation should:
- Use British English spelling
- Include working code examples
- Follow Markdown best practices
- Be beginner-friendly

---

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Phlair/civ7-modding-tools/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/Phlair/civ7-modding-tools/discussions)
- **Examples**: [See working code](../examples/)

---

**Happy modding! 🎮**

