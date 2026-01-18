# Civ7 Modding Tools - Documentation Index

Welcome to the comprehensive documentation for **Civ7 Modding Tools**, a Python library for creating Civilization 7 mods programmatically.

## 📚 Main Documentation

### [Getting Started Guide](GUIDE.md) 🚀
**Best starting point for new users**
- Installation instructions
- Your first mod (5-minute tutorial)
- Core concepts explained
- Common patterns and best practices
- Troubleshooting guide

### [API Reference](API.md) 📖
**Complete technical reference**
- All classes and methods documented
- Properties and their types
- Usage examples for each API
- Constants and enums
- Type hints reference

### [Examples](EXAMPLES.md) 💡
**Practical, copy-paste ready examples**
- Simple civilization
- Complete civilization with all features
- Custom units with abilities
- Tech trees and progression
- Game modifiers and effects
- Importing external assets
- Multi-entity mods

### [Migration Guide](MIGRATION.md) 🔄
**For TypeScript users**
- Syntax conversion guide
- Type system differences
- Side-by-side comparisons
- Full migration example
- Migration checklist

---

## 🎯 Quick Start by Use Case

### I want to...

#### Create a simple mod
1. Read: [Getting Started Guide](GUIDE.md#your-first-mod)
2. Copy: [Simple Civilization Example](EXAMPLES.md#example-1-simple-civilization)
3. Run: `python build.py`

#### Create a complete mod with units and buildings
1. Read: [Core Concepts](GUIDE.md#core-concepts)
2. Copy: [Multi-Entity Mod Example](EXAMPLES.md#example-7-mod-with-multiple-entities)
3. Reference: [API for each builder type](API.md#builders)

#### Migrate from TypeScript
1. Read: [Migration Guide](MIGRATION.md)
2. Study: [Side-by-side comparison](MIGRATION.md#example-full-migration)
3. Follow: [Migration checklist](MIGRATION.md#migration-checklist)

#### Understand the full API
1. Start with: [API Reference](API.md#core-classes)
2. For details on a specific builder: [Builders section](API.md#builders)
3. Look up constants: [Constants section](API.md#constants)

#### Create complex game mechanics
1. Learn: [Game Modifiers](EXAMPLES.md#example-5-game-modifiers-and-effects)
2. Reference: [ModifierBuilder API](API.md#modifierbuilder)
3. Check: [Effect constants](API.md#game-constants)

#### Add custom assets to mod
1. Tutorial: [Importing Assets](EXAMPLES.md#example-6-importing-external-assets)
2. Reference: [ImportFileBuilder API](API.md#importfilebuilder)

---

## 📖 Learning Path

### Beginner (1-2 hours)
1. [Getting Started Guide](GUIDE.md) - Read full guide
2. [Example 1: Simple Civilization](EXAMPLES.md#example-1-simple-civilization) - Copy and run
3. Try modifying the example and rebuilding

### Intermediate (2-4 hours)
1. [Core Concepts](GUIDE.md#core-concepts) - Understand patterns
2. [Example 2: Complete Civilization](EXAMPLES.md#example-2-complete-civilization) - Run full example
3. [API Reference](API.md) - Reference specific builders
4. Create your own mod combining multiple features

### Advanced (4+ hours)
1. [API Reference](API.md) - Study all sections
2. [Examples 5-7](EXAMPLES.md) - Study complex examples
3. Review [Project Architecture](../README.md) documentation
4. Experiment with advanced features

### TypeScript Users (1-2 hours)
1. [Migration Guide Overview](MIGRATION.md#overview)
2. [Syntax Changes](MIGRATION.md#syntax-changes)
3. [Full Migration Example](MIGRATION.md#example-full-migration)
4. [Migration Checklist](MIGRATION.md#migration-checklist)

---

## 🔍 Finding Information

### By Topic

#### Builders
- Overview: [Builders section in Guide](GUIDE.md#building-a-civilization)
- API Docs: [All Builders](API.md#builders)
- Examples: [Each Example](EXAMPLES.md)

#### Constants
- All Constants: [Constants in API](API.md#constants)
- Usage: Throughout [Examples](EXAMPLES.md)

#### Nodes and Files
- Overview: [Builders and Nodes in API](API.md#nodes)
- File Output: [Files section in API](API.md#files)

#### Localizations
- Overview: [Localizations in API](API.md#localizations)
- Usage: Throughout [Examples](EXAMPLES.md)

#### Game Mechanics
- Modifiers: [Modifiers Example](EXAMPLES.md#example-5-game-modifiers-and-effects)
- Effects: [EFFECT constants](API.md#game-constants)

### By Difficulty

#### Easy
- [Getting Started](GUIDE.md)
- [Simple Example](EXAMPLES.md#example-1-simple-civilization)

#### Medium
- [Example 2-4](EXAMPLES.md)
- [API Builders](API.md#builders)

#### Hard
- [Example 5-7](EXAMPLES.md)
- [Full API Reference](API.md)

---

## 🆘 Troubleshooting

### Common Issues

#### "No files generated"
- **Solution**: See [Troubleshooting in Guide](GUIDE.md#troubleshooting)

#### "Missing localization"
- **Solution**: See [Localizations](GUIDE.md#building-a-civilization) section

#### "Type errors in IDE"
- **Solution**: Ensure imports match [API examples](API.md#type-hints)

#### "TypeScript to Python conversion"
- **Solution**: See [Migration Guide](MIGRATION.md)

---

## 📝 Reference Tables

### Quick API Reference

| Need | Find In |
|------|----------|
| Create civilization | [CivilizationBuilder](API.md#civilizationbuilder) in API |
| Create unit | [UnitBuilder](API.md#unitbuilder) in API |
| Create building | [ConstructibleBuilder](API.md#constructiblebuilder) in API |
| Get constants | [Constants](API.md#constants) in API |
| See example | [Examples](EXAMPLES.md) doc |
| TypeScript help | [Migration Guide](MIGRATION.md) |

### File Structure

```
docs/
├── INDEX.md (this file)        # Navigation hub
├── GUIDE.md                    # Getting started tutorial
├── API.md                      # Complete API reference
├── EXAMPLES.md                 # Practical examples
└── MIGRATION.md                # TypeScript migration
```

---

## 🚀 Getting Help

1. **Read the docs**: You're likely to find the answer here
2. **Check examples**: See [EXAMPLES.md](EXAMPLES.md) for similar use cases
3. **Review API**: See specific API in [API.md](API.md)
4. **GitHub Issues**: https://github.com/Phlair/civ7-modding-tools/issues

---

## 📚 Additional Resources

- **GitHub Repository**: https://github.com/Phlair/civ7-modding-tools
- **Project README**: [README.md](../README.md)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md) (if available)
- **Civ7 Modding**: https://civilization.fandom.com/wiki/Modding

---

## 📊 Documentation Status

- ✅ **Getting Started Guide**: Complete with 5-minute tutorial
- ✅ **API Reference**: Complete with all classes and methods
- ✅ **Examples**: 7 practical examples provided
- ✅ **Migration Guide**: Complete TypeScript→Python reference
- ✅ **Type Hints**: Full type annotations throughout
- ✅ **Test Coverage**: 94% (324/324 tests passing)

---

## 💡 Tips for Success

1. **Start Small**: Begin with [Simple Example](EXAMPLES.md#example-1-simple-civilization)
2. **Read Concepts**: Understand [Core Concepts](GUIDE.md#core-concepts)
3. **Refer to API**: Keep [API.md](API.md) handy
4. **Copy Examples**: Use [EXAMPLES.md](EXAMPLES.md) as templates
5. **Use Type Hints**: Enable IDE autocomplete with proper imports
6. **Test Often**: Build your mod frequently to catch issues early

---

## 🎮 Happy Modding!

You now have everything you need to create awesome Civilization 7 mods. Start with the [Getting Started Guide](GUIDE.md) and build your first mod today!

**Questions?** Check the [Troubleshooting section](GUIDE.md#troubleshooting) or the [FAQ in Migration Guide](MIGRATION.md#frequently-asked-questions).

**Ready to build?** Go to [Getting Started Guide](GUIDE.md) 🚀

