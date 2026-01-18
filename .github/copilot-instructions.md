# Civ7 Modding Tools - Copilot Instructions

## Project Overview

**Civ7 Modding Tools** is a TypeScript-based code generation library for creating Civilization 7 mods. It provides strongly-typed builders and nodes that abstract the complexity of manual XML/mod file creation, allowing developers to programmatically generate complete mod packages with civilizations, units, buildings, progression trees, and other game entities.

- **Repository**: https://github.com/Phlair/civ7-modding-tools
- **License**: MIT
- **TypeScript Version**: 5.7.3
- **Target**: ES6 / CommonJS

## Architecture Overview

The project follows a **builder pattern** for mod generation:

```
User Code (build.ts, scripts)
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

1. **Type Safety**: Full TypeScript support with strict typing throughout
2. **Builder Pattern**: Fluent API for constructing mod entities with `fill()` method
3. **Separation of Concerns**: Builders create files, nodes represent XML elements, files write to disk
4. **Modular Constants**: Game-specific constants (TRAIT, UNIT_CLASS, EFFECT, etc.) for type-safe references
5. **Localization Support**: Built-in localization system for English and internationalized text

## Directory Structure

```
civ7-modding-tools/
├── src/
│   ├── core/
│   │   ├── Mod.ts              # Main orchestrator class
│   │   ├── ActionGroupBundle.ts # Action group bundling for game ages
│   │   └── index.ts
│   │
│   ├── builders/
│   │   ├── BaseBuilder.ts       # Abstract base for all builders
│   │   ├── CivilizationBuilder.ts
│   │   ├── CivilizationUnlockBuilder.ts
│   │   ├── LeaderUnlockBuilder.ts
│   │   ├── UnitBuilder.ts
│   │   ├── ConstructibleBuilder.ts    # Buildings, improvements, quarters
│   │   ├── UniqueQuarterBuilder.ts
│   │   ├── ProgressionTreeBuilder.ts  # Civics progression trees
│   │   ├── ProgressionTreeNodeBuilder.ts
│   │   ├── ModifierBuilder.ts         # Game modifiers/effects
│   │   ├── TraditionBuilder.ts
│   │   ├── UnlockBuilder.ts
│   │   ├── ImportFileBuilder.ts       # Custom file imports (images, SQL)
│   │   └── index.ts
│   │
│   ├── nodes/
│   │   ├── BaseNode.ts          # Abstract base node (converts to XML)
│   │   ├── CivilizationNode.ts
│   │   ├── UnitNode.ts
│   │   ├── ConstructibleNode.ts
│   │   ├── GameEffectNode.ts
│   │   ├── ProgressionTreeNode.ts
│   │   ├── TraditionNode.ts
│   │   ├── ModifierNode.ts
│   │   ├── RequirementNode.ts   # Game requirements/conditions
│   │   ├── RequirementSetNode.ts
│   │   ├── (40+ specialized node types)
│   │   ├── slices/              # Sub-node collections for complex entities
│   │   └── index.ts
│   │
│   ├── files/
│   │   ├── BaseFile.ts          # Abstract file base class
│   │   ├── XmlFile.ts           # XML file generation (primary output)
│   │   ├── ImportFile.ts        # Import handler for images/SQL/etc
│   │   └── index.ts
│   │
│   ├── localizations/
│   │   ├── BaseLocalization.ts  # Base localization structure
│   │   ├── CivilizationLocalization.ts
│   │   ├── UnitLocalization.ts
│   │   ├── ConstructibleLocalization.ts
│   │   ├── ProgressionTreeLocalization.ts
│   │   ├── (7+ specialized localization types)
│   │   └── index.ts
│   │
│   ├── constants/
│   │   ├── TRAIT.ts             # Civilization traits
│   │   ├── TAG_TRAIT.ts         # Trait tags (ECONOMIC, CULTURAL, etc)
│   │   ├── UNIT_CLASS.ts        # Unit classifications (RECON, MELEE, etc)
│   │   ├── UNIT_MOVEMENT_CLASS.ts
│   │   ├── UNIT_CULTURE.ts
│   │   ├── CONSTRUCTIBLE_TYPE_TAG.ts
│   │   ├── CONSTRUCTIBLE_CLASS.ts
│   │   ├── EFFECT.ts            # Game effects/modifiers
│   │   ├── REQUIREMENT.ts       # Game conditions
│   │   ├── REQUIREMENT_SET.ts
│   │   ├── ACTION_GROUP.ts
│   │   ├── ACTION_GROUP_ACTION.ts
│   │   ├── ACTION_GROUP_BUNDLE.ts  # Age groupings
│   │   ├── AGE.ts               # Game ages
│   │   ├── YIELD.ts             # Resource yields
│   │   ├── TERRAIN.ts
│   │   ├── BIOME.ts
│   │   ├── FEATURE.ts
│   │   ├── FEATURE_CLASS.ts
│   │   ├── RESOURCE.ts
│   │   ├── ICON.ts
│   │   ├── DISTRICT.ts
│   │   ├── DOMAIN.ts
│   │   ├── COLLECTION.ts
│   │   ├── LANGUAGE.ts
│   │   ├── PLUNDER.ts
│   │   ├── ADVISORY.ts
│   │   ├── BUILDING_CULTURES.ts
│   │   ├── CIVILIZATION_DOMAIN.ts
│   │   ├── (20+ additional constants)
│   │   └── index.ts
│   │
│   ├── types/
│   │   ├── TClassProperties.ts   # Extract class properties as interface
│   │   ├── TObjectValues.ts      # Extract object values as union type
│   │   ├── TLocalizationProperties.ts
│   │   ├── TPartialNullable.ts
│   │   ├── TPartialRequired.ts
│   │   └── index.ts
│   │
│   ├── utils/
│   │   ├── fill.ts              # Generic object property filler
│   │   ├── locale.ts            # Localization utilities
│   │   ├── trim.ts              # String trimming utilities
│   │   └── index.ts
│   │
│   ├── presets/
│   │   ├── createGodConstructible.ts  # Preset helper for god buildings
│   │   └── index.ts
│   │
│   └── index.ts                 # Main export barrel
│
├── examples/
│   ├── civilization.ts          # Full civilization example with all features
│   ├── unit.ts
│   ├── progression-tree.ts
│   ├── unique-quarter.ts
│   ├── unlock-builder.ts
│   ├── import-sql-file.ts
│   └── import-custom-icon.ts
│
├── example-generated-mod/       # Generated output example
│   ├── mod-test.modinfo         # Mod metadata file (XML)
│   ├── civilizations/
│   ├── units/
│   ├── constructibles/
│   ├── progression-trees/
│   └── imports/
│
├── assets/                      # Example assets for import
│   └── example.sql
│
├── build.ts                     # Example build script
├── package.json
├── tsconfig.json
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

```typescript
const mod = new Mod({
    id: 'my-mod',
    version: '1.0',
    name: 'My Civilization 7 Mod',
    description: 'Custom mod description',
    authors: 'Your Name',
    affectsSavedGames: true
});

// Add builders
mod.add(civilizationBuilder);
mod.add([unitBuilder1, unitBuilder2]);
mod.addFiles(importFileBuilder);

// Generate output
mod.build('./dist');  // Generates .modinfo + XML files to ./dist
```

**Key Methods**:
- `add(builder | builder[])`: Register builders
- `addFiles(file | file[])`: Register import files
- `build(dist, clear)`: Generate mod files to disk

### 2. Builders (Abstract Factory Pattern)

All builders extend `BaseBuilder` and implement the builder pattern:

```typescript
export class BaseBuilder<T = object> {
    actionGroupBundle: ActionGroupBundle = new ActionGroupBundle();
    
    fill<T>(payload: Partial<T>): this  // Populate properties
    migrate(): this                       // Hook for version migrations
    build(): BaseFile[]                  // Generate output files
}
```

**Key Builders**:
- **CivilizationBuilder**: Full civilization with traits, tags, unlocks, start biases, AI bias, localizations
- **UnitBuilder**: Unit definition with stats, costs, abilities, visual remaps
- **ConstructibleBuilder**: Buildings, improvements, quarters with yield/maintenance/plunder (auto-detects type)
- **UniqueQuarterBuilder**: District-specific buildings with unique properties
- **ProgressionTreeBuilder**: Tech/civics trees with nodes, prereqs, advisories
- **ModifierBuilder**: Game effects applied to collections (players, units, buildings). Supports detached modifiers.
- **TraditionBuilder**: Cultural traditions with modifiers
- **UnlockBuilder**: Generic unlock configurations
- **LeaderUnlockBuilder**: Leader-civilization pairings with bias and localizations
- **CivilizationUnlockBuilder**: Age-based civilization progressions
- **ImportFileBuilder**: Import/Copy external files (images, SQL scripts, etc)

### 3. Nodes (XML Element Representation)

Nodes represent XML elements. All extend `BaseNode`:

```typescript
export class BaseNode<T = object> {
    _name: string = 'Row';
    
    fill<T>(payload: Partial<T>): this
    insertOrIgnore(): this                // Transform to INSERT OR IGNORE
    toXmlElement(): XmlElement | null     // Convert to jstoxml format
}
```

Node properties become XML attributes via camelCase → PascalCase conversion:
```typescript
new CivilizationNode({
    civilizationType: 'CIVILIZATION_ROME',
    baseTourism: 10,
    legacyModifier: true  // becomes LegacyModifier="true" in XML
});
```

**Node Categories**:
- **Entity Nodes**: CivilizationNode, UnitNode, ConstructibleNode, LeaderUnlockNode, UniqueQuarterNode, etc.
- **Stat/Config Nodes**: UnitStatNode, UnitCostNode, ConstructibleYieldChangeNode, StartBiasBiomeNode, etc.
- **Requirement Nodes**: RequirementNode, RequirementSetNode, RequirementArgumentNode
- **Modifier Nodes**: ModifierNode, GameModifierNode, TraitModifierNode
- **Game Effect Nodes**: GameEffectNode, AdjacencyYieldChangeNode, WarehouseYieldChangeNode
- **Localization Nodes**: EnglishTextNode, CityNameNode
- **Progression Nodes**: ProgressionTreeNode, ProgressionTreeNodeNode, ProgressionTreePrereqNode
- **Slice Nodes** (in `slices/`): Nested node collections for complex hierarchies

### 4. Files (Output Generation)

Files represent physical outputs:

```typescript
export class BaseFile<T = any> {
    path: string = '/';              // Directory path
    name: string = 'file.txt';       // Filename
    content: any = null;              // Content (nodes, arrays, etc)
    actionGroups: ActionGroupNode[]; // Associated action groups
    actionGroupActions: string[];    // Action types (UpdateDatabase, etc)
    
    write(dist: string): void        // Write to disk
    isEmpty: boolean                  // Computed property
    modInfoPath: string              // Path for .modinfo reference
}
```

**File Types**:
- **XmlFile**: Primary output for Civ7 XML files (uses `jstoxml` for serialization)
- **ImportFile**: Import handler for images, SQL, custom files

### 5. Action Groups & Criteria

Mods use action groups to scope content loading:

```typescript
mod.add(builder.with({
    actionGroupBundle: ACTION_GROUP_BUNDLE.AGE_ANTIQUITY
}));
```

This links content to specific ages, ensuring it loads at the right time:
- `AGE_ANTIQUITY` → Ancient age
- `AGE_EXPLORATION` → Classical age
- `ACTION_GROUP_BUNDLE.ALWAYS` → Always loaded

## Localization System

Localizations provide multi-language support:

```typescript
civilization.localizations = [
    {
        name: 'Rome',
        description: 'Ancient empire',
        fullName: 'The Roman Empire',
        adjective: 'Roman',
        cityNames: ['Rome', 'Milan', 'Venice']
    }
];
```

Each builder type has a corresponding localization class (CivilizationLocalization, UnitLocalization, etc.).

## Workflow

### Development Workflow

```bash
# Install dependencies
npm install

# Develop with TypeScript watching
npm run dev

# Compile TypeScript
npm run compile

# Build mod (run build.ts)
npm run build
```

### Creating a Mod

1. **Initialize Mod**:
   ```typescript
   const mod = new Mod({
       id: 'my-custom-mod',
       version: '1.0'
   });
   ```

2. **Create Builders**:
   ```typescript
   const civilization = new CivilizationBuilder({
       actionGroupBundle: ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
       civilization: { civilizationType: 'CIVILIZATION_CUSTOM', ... },
       civilizationTraits: [TRAIT.ECONOMIC_CIV, ...],
       localizations: [{ name: 'Custom Civ', ... }]
   });
   ```

3. **Register Builders**:
   ```typescript
   mod.add(civilization);
   mod.add([unitBuilder1, unitBuilder2]);
   ```

4. **Build Output**:
   ```typescript
   mod.build('./dist');  // Generates /dist/mod-test.modinfo + XML files
   ```

5. **Output Structure**:
   ```
   dist/
   ├── mod-test.modinfo           # Mod metadata
   ├── civilizations/gondor/
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

### TypeScript

- **Language**: TypeScript 5.7.3
- **Target**: ES6 / CommonJS
- **Strict Mode**: Enabled (`strict: true`)
- **File Extensions**: `.ts` for library, `.ts` for examples/build scripts
- **Type Definitions**: Generated in `dist/` with `declaration: true`

### Naming Conventions

- **Classes**: PascalCase (CivilizationBuilder, BaseNode)
- **Methods/Properties**: camelCase (buildCivilization, civilizationType)
- **Constants**: UPPER_SNAKE_CASE (TRAIT.ECONOMIC_CIV, UNIT_CLASS.RECON)
- **Private Methods**: Leading underscore (_getAttributes)

### Builder Pattern Usage

All builders follow the fluent builder pattern:

```typescript
const builder = new CivilizationBuilder()
    .fill({
        actionGroupBundle: ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
        civilization: { ... }
    });
    // or
    
const builder = new CivilizationBuilder({
    actionGroupBundle: ACTION_GROUP_BUNDLE.AGE_ANTIQUITY,
    civilization: { ... }
});
```

The `fill()` method populates properties from a partial object.

### Constants Usage

Constants are organized by game concept and exported from `src/constants/`:

```typescript
import {
    TRAIT,           // Civilization traits
    UNIT_CLASS,      // Unit classifications
    EFFECT,          // Game effects
    REQUIREMENT,     // Game conditions
    YIELD,           // Resource yields
    ACTION_GROUP_BUNDLE,  // Age groupings
    AGE              // Game ages
} from 'civ7-modding-tools';
```

Use constants instead of magic strings for:
- Unit classifications: `UNIT_CLASS.RECON`, `UNIT_CLASS.MELEE`
- Effects: `EFFECT.UNIT_ADJUST_MOVEMENT`, `EFFECT.PLAYER_ADJUST_GREAT_PERSON_RATE`
- Requirements: `REQUIREMENT.UNIT_TAG_MATCHES`, `REQUIREMENT.PLAYER_HAS_TECH`
- Yields: `YIELD.SCIENCE`, `YIELD.CULTURE`, `YIELD.GOLD`
- Ages: `AGE.ANTIQUITY`, `AGE.EXPLORATION`, `AGE.MODERN`

### Node Serialization

Nodes convert to XML via `toXmlElement()`:

```typescript
// TypeScript
new CivilizationNode({
    civilizationType: 'CIVILIZATION_ROME',
    baseTourism: 10,
    legacyModifier: true
})

// Generated XML Attribute
// <Row CivilizationType="CIVILIZATION_ROME" BaseTourism="10" LegacyModifier="true"/>
```

Property conversion rules:
- camelCase → PascalCase
- `boolean` → "true" / "false" (string)
- `null/undefined/""` → omitted from output
- All other types → stringified

## Adding New Features

### Adding a New Builder

1. **Create Builder Class** in `src/builders/MyBuilder.ts`:
   ```typescript
   import { BaseBuilder } from './BaseBuilder';
   import { BaseFile } from '../files';
   
   export class MyBuilder extends BaseBuilder {
       myProperty: string = 'default';
       
       build(): BaseFile[] {
           // Create and return files
           const file = new XmlFile({
               path: '/my-path/',
               name: 'my-file.xml',
               content: { /* nodes here */ }
           });
           return [file];
       }
   }
   ```

2. **Export from** `src/builders/index.ts`:
   ```typescript
   export { MyBuilder } from './MyBuilder';
   ```

3. **Create Localization Class** in `src/localizations/MyLocalization.ts`:
   ```typescript
   import { BaseLocalization } from './BaseLocalization';
   
   export class MyLocalization extends BaseLocalization {
       myLocalizedField: string = '';
   }
   ```

4. **Export from** `src/localizations/index.ts`

5. **Use in build.ts**:
   ```typescript
   const myBuilder = new MyBuilder({
       myProperty: 'value',
       localizations: [{ myLocalizedField: 'Localized Text' }]
   });
   mod.add(myBuilder);
   ```

### Adding New Nodes

1. **Create Node Class** in `src/nodes/MyNode.ts`:
   ```typescript
   import { BaseNode } from './BaseNode';
   
   export class MyNode extends BaseNode {
       _name = 'MyElement';
       myAttribute: string = '';
       myNumber: number = 0;
   }
   ```

2. **Export from** `src/nodes/index.ts`

3. **Use in Builders**:
   ```typescript
   import { MyNode } from '../nodes';
   
   // In builder's build() method
   const node = new MyNode({ myAttribute: 'value' });
   ```

### Adding New Constants

1. **Create** `src/constants/MY_CONSTANT.ts`:
   ```typescript
   export const MY_CONSTANT = {
       VALUE_ONE: 'VALUE_ONE',
       VALUE_TWO: 'VALUE_TWO',
       VALUE_THREE: 'VALUE_THREE'
   } as const;
   ```

2. **Export from** `src/constants/index.ts`:
   ```typescript
   export { MY_CONSTANT } from './MY_CONSTANT';
   ```

3. **Use in code**:
   ```typescript
   import { MY_CONSTANT } from 'civ7-modding-tools';
   
   builder.fill({ myProperty: MY_CONSTANT.VALUE_ONE });
   ```

## Key Implementation Details

### XML Generation

Uses `jstoxml` library for XML serialization:

```typescript
import { toXML } from 'jstoxml';

const xml = toXML(content, {
    header: true,
    indent: '    '
});
```

Output includes header and pretty-printing with 4-space indentation.

### Action Group Management

The `Mod` class automatically:
1. Extracts unique criteria from all builders
2. Creates ActionCriteria elements in .modinfo
3. Groups files by action group ID
4. Generates ActionGroup elements with appropriate Actions

This allows content to be conditionally loaded based on game state (age, technology, etc).

### Property Type System

Custom TypeScript utility types enable type-safe property extraction:

- `TClassProperties<T>`: Extracts class properties as interface
- `TObjectValues<T>`: Extracts object literal values as union type
- `TLocalizationProperties<T>`: Specific for localization types
- `TPartialRequired<T, K>`: Make specific properties required in partial types

## Testing & Quality

### Building

```bash
npm run build
npm run compile    # Just TypeScript check
npm run dev        # Watch mode
```

### Output Validation

Generated mods produce:
1. `.modinfo` file with proper XML structure, criteria, action groups
2. Organized XML files in expected directories
3. Imported assets in the `imports/` directory

Validate against Civilization 7 mod format documentation.

## File Structure Best Practices

### For Custom Mods Using Library

```typescript
// build.ts - Main mod entry point
import { Mod, CivilizationBuilder, ... } from 'civ7-modding-tools';

const mod = new Mod({ /* ... */ });
// Define builders, add to mod
mod.build('./dist');
```

### Project Layout

```
my-civ7-mod/
├── src/
│   └── build.ts           # Main build script
├── assets/                # Images, SQL files for import
│   ├── civ-icon.png
│   └── units-data.sql
├── dist/                  # Generated mod output
└── package.json
```

## Version History

See [CHANGELOG.md](../CHANGELOG.md) for version history.

Current version: 1.3.0

Notable versions:
- **1.0**: Initial release
- **1.1**: Import files, expanded constants, progression tree nodes
- **1.2**: UniqueQuarterBuilder added
- **1.3**: Current - Additional node types and refinements

## Performance Considerations

- Builders are lightweight; performance bottleneck is file I/O
- Node serialization is lazy (only via toXmlElement())
- Large mods with 100+ entities generate quickly
- XML generation is synchronous using jstoxml

## Common Patterns

### Conditional Content

```typescript
// Load content in specific ages
const builder = new CivilizationBuilder({
    actionGroupBundle: ACTION_GROUP_BUNDLE.AGE_EXPLORATION  // Not loaded until Exploration age
});
```

### Multiple Units/Buildings

```typescript
const units = [
    new UnitBuilder({ /* unit 1 */ }),
    new UnitBuilder({ /* unit 2 */ }),
    new UnitBuilder({ /* unit 3 */ })
];
mod.add(units);
```

### Requirements and Effects

```typescript
const modifier = new ModifierBuilder({
    collection: COLLECTION.PLAYER_UNITS,
    effect: EFFECT.UNIT_ADJUST_MOVEMENT,
    requirements: [{
        type: REQUIREMENT.UNIT_TAG_MATCHES,
        arguments: [{ name: 'Tag', value: UNIT_CLASS.RECON }]
    }],
    arguments: [{ name: 'Amount', value: 2 }]
});
```

## External Dependencies

- **jstoxml** (5.0.2): XML serialization
- **lodash** (4.17.21): Utility functions (startCase, uniqBy, etc.)
- **TypeScript** (5.7.3): Compilation
- **tsx** (4.19.3): TypeScript execution (replaces ts-node)
- **tsup** (8.4.0): Build tool

## Troubleshooting

### ModInfo not generating

Ensure `Mod.build()` is called after all builders are added:
```typescript
mod.add(builders);
mod.build('./dist');  // Don't forget!
```

### Missing localization keys

Ensure localization objects match builder expectations. Check the corresponding Localization class definition.

### XML attribute not appearing

Properties that are `null`, `undefined`, or `''` are omitted. Verify property is set to a valid value.

### Import file not copied

ImportFileBuilder content must be a valid file path (e.g., `'./assets/icon.png'`). The file is read and written to the `imports/` directory.

## Resources

- **GitHub**: https://github.com/Phlair/civ7-modding-tools
- **Examples**: See `examples/` directory for full working examples
- **Generated Example**: `example-generated-mod/` shows expected output structure
- **Civilization 7 Modding**: https://civilization.fandom.com/wiki/Modding (general reference)

## Language

- Use **British English** in code comments and documentation

## Design Philosophy

This library prioritizes:

1. **Type Safety**: Catch errors at compile time via TypeScript
2. **Discoverability**: IDE autocomplete guides users through available options
3. **Abstraction**: Hide XML complexity behind intuitive builders
4. **Flexibility**: Low-level node access for advanced use cases
5. **Extensibility**: Easy to add new builders, nodes, constants

