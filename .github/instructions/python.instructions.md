---
description: "Python coding conventions for Phlair's Civ VII Modding Tools"
applyTo: "**/*.py"
---

# Python Coding Conventions for Phlair's Civ VII Modding Tools

## Project-Specific Style

### Overview

Phlair's Civ VII Modding Tools is a strongly-typed Python library for generating Civilization 7 mod files. All code must follow these conventions to maintain consistency with the builder pattern, pydantic models, and type-safe API.

> **Credit**: This project is a complete rework of the original toolset by [izica](https://github.com/izica).

### Core Principles

1. **Type Safety First**: Use comprehensive type hints throughout all code
2. **Builder Pattern**: Fluent API with `fill()` method for all builders
3. **Pydantic Models**: Use pydantic for all data validation and serialization
4. **Snake Case for Python**: All Python identifiers use snake_case (methods, properties, functions)
5. **British English**: Use British spelling in docstrings and comments
6. **100 Character Line Limit**: Respect the 100 character line limit (not 79)

## Type Hints

### Required Type Hints

All functions and methods must have complete type hints:

```python
from typing import Any, TypeVar, Callable

T = TypeVar("T")

def fill(obj: T, payload: dict[str, Any]) -> T:
    """Populate object properties from a dictionary, preserving type."""
    ...

def without(lst: list[T], *values: T) -> list[T]:
    """Return list with specified values removed, preserving type."""
    ...

def uniq_by(
    lst: list[T],
    key_func: Callable[[T], Any] | None = None
) -> list[T]:
    """Return unique items by key function, preserving type."""
    ...
```

### Use Union Type Syntax

- Modern union syntax: `T | None` instead of `Optional[T]`
- Explicit union types: `str | int | float` instead of `Union[str, int, float]`
- Return type annotations always required: `-> None`, `-> dict`, `-> list[BaseFile]`

### TypeVar for Generic Functions

Use TypeVar for functions that preserve type:

```python
T = TypeVar("T")

def fill(obj: T, payload: Dict[str, Any]) -> T:
    """T preserved as input/output type."""
    ...
```

## Builder Pattern Implementation

### All Builders Must Follow This Structure

```python
from typing import Any
from civ7_modding_tools.builders.builders import BaseBuilder
from civ7_modding_tools.files import BaseFile, XmlFile

class MyBuilder(BaseBuilder):
    """Builder for MyEntity, following builder pattern."""
    
    my_property: str = 'default'
    another_property: int = 0
    
    def fill(self, payload: dict[str, Any]) -> "MyBuilder":
        """Set properties from dictionary and return self for chaining."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def build(self) -> list[BaseFile]:
        """Generate output files for this builder."""
        # Implementation here
        return [file1, file2]
```

### The fill() Method

- Must return `self` for method chaining
- Must accept `Dict[str, Any]` payload
- Must handle both constructor and fill() method patterns
- Should be documented with usage examples

```python
# Usage Pattern 1: Constructor
builder = MyBuilder({
    'my_property': 'value',
    'another_property': 42
})

# Usage Pattern 2: fill() method
builder = MyBuilder()
builder.fill({
    'my_property': 'value',
    'another_property': 42
})
```

## Pydantic Models

### Localization Classes

All localization classes extend pydantic BaseModel:

```python
from pydantic import BaseModel, ConfigDict, Field

class MyLocalization(BaseModel):
    """Localization for my entity."""
    
    model_config = ConfigDict(extra='forbid')  # Disallow unknown fields
    
    name: str = ''
    description: str = ''
    my_field: str = Field(default='', alias='myField')
```

### Node Classes

All nodes inherit from BaseNode and use pydantic validation:

```python
from civ7_modding_tools.nodes.base import BaseNode

class MyNode(BaseNode):
    """XML element representation."""
    
    _name: str = 'MyElement'
    my_attribute: str = ''
    my_number: int = 0
    optional_value: str | None = None
    
    def to_xml_element(self) -> dict | None:
        """Convert to XML element dictionary."""
        # Implementation
        ...
```

## Naming Conventions

### Classes

- PascalCase: `CivilizationBuilder`, `BaseNode`, `XmlFile`
- Descriptive names: `UnitStatNode` not `USNode`
- Append descriptive suffix: `Builder`, `Node`, `File`, `Localization`

### Methods and Properties

- snake_case: `civilization_type`, `build_civilization`, `get_attributes`
- Descriptive names: `fill()`, `build()`, `to_xml_element()`, `write()`
- Avoid abbreviations: `unit_cost` not `u_cost`

### Constants and Enums

- UPPER_SNAKE_CASE: `TRAIT.ECONOMIC_CIV`, `UNIT_CLASS.RECON`
- Group in Enum classes: `TRAIT(str, Enum)`, `UNIT_CLASS(str, Enum)`
- Export from constants module for type safety

```python
from enum import Enum

class TRAIT(str, Enum):
    """Civilization trait types."""
    ECONOMIC_CIV = 'ECONOMIC_CIV'
    MILITARY_CIV = 'MILITARY_CIV'
    CULTURAL_CIV = 'CULTURAL_CIV'
```

### Private Methods

- Leading underscore: `_get_attributes()`, `_validate_property()`
- Document purpose clearly in docstring

## Docstrings and Comments

### Docstring Format

Follow PEP 257 with clear description:

```python
def fill(self, payload: dict[str, Any]) -> "MyBuilder":
    """
    Populate builder properties from a dictionary.
    
    Args:
        payload: Dictionary with property values to set.
    
    Returns:
        Self for method chaining.
    
    Example:
        >>> builder = MyBuilder()
        >>> builder.fill({'property': 'value'})
        >>> builder.build()
    """
```

### Module-Level Docstrings

```python
"""Module for builder implementations.

This module contains all builder classes for creating Civ7 mod entities:
- CivilizationBuilder: Full civilization
- UnitBuilder: Unit definitions
- ConstructibleBuilder: Buildings, improvements, quarters
"""
```

### Class Docstrings

```python
class CivilizationBuilder(BaseBuilder):
    """Builder for Civilization entities.
    
    Handles civilization definition, traits, unlocks, and start biases.
    Uses builder pattern with fluent API for configuration.
    """
```

### Inline Comments

- Use sparingly, prioritize clear code over comments
- Explain *why*, not *what*: code should be self-documenting
- Use British English spelling

```python
# Builders are processed in order to respect action group dependencies
for builder in self.builders:
    builder.migrate()
```

## XML Node Serialization

### Property Conversion

Properties automatically convert:
- snake_case → PascalCase: `civilization_type` → `CivilizationType`
- `bool` → string: `True` → `"true"`, `False` → `"false"`
- `None` → omitted from XML: `None` properties excluded
- All types stringified: `10` → `"10"`, `3.14` → `"3.14"`

### Example

```python
node = CivilizationNode(
    civilization_type='CIVILIZATION_ROME',  # snake_case
    base_tourism=10,                        # int converted to string
    legacy_modifier=True,                   # bool converted to "true"
    display_name=None                       # omitted from output
)

# XML Output:
# <Row CivilizationType="CIVILIZATION_ROME" BaseTourism="10" LegacyModifier="true"/>
```

## Code Organization

### Module Structure

```python
# 1. Imports (stdlib, third-party, local)
from typing import Any
from pydantic import BaseModel
from civ7_modding_tools.nodes import BaseNode

# 2. Module docstring
"""Module description."""

# 3. Constants
DEFAULT_ACTION_GROUP = 'ALWAYS'

# 4. Classes (in logical order)
class MyNode(BaseNode):
    """First class."""
    ...

class MyBuilder(BaseBuilder):
    """Second class."""
    ...

# 5. Functions (if any)
def helper_function() -> None:
    """Helper function."""
    ...
```

### Imports Organization

```python
# Standard library
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Callable
from pathlib import Path

# Third-party
from pydantic import BaseModel, Field
import xmltodict

# Local
from civ7_modding_tools.nodes import BaseNode
from civ7_modding_tools.files import BaseFile
```

## File I/O

### XML Generation

Use xmltodict for serialization:

```python
from xmltodict import unparse

xml_str = unparse(
    content,
    pretty=True,
    full_document=True,
    indent='    '  # 4-space indentation
)
```

### File Writing

```python
from pathlib import Path

def write(self, dist: str) -> None:
    """Write file to disk."""
    path = Path(dist) / self.path / self.name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(self.content, encoding='utf-8')
```

## Edge Cases and Testing

### Error Handling

```python
def build(self) -> list[BaseFile]:
    """Generate output files.
    
    Raises:
        ValueError: If required property is missing.
        FileNotFoundError: If import file not found.
    """
    if not self.civilization_type:
        raise ValueError('civilization_type is required')
    
    if self.icon_file and not Path(self.icon_file).exists():
        raise FileNotFoundError(f'Icon file not found: {self.icon_file}')
    
    return [...]
```

### Test Structure

```python
import pytest
from civ7_modding_tools import CivilizationBuilder

def test_civilization_builder_fill():
    """Builder should populate properties via fill() method."""
    builder = CivilizationBuilder()
    builder.fill({
        'civilization': {'civilization_type': 'CIV_ROME'},
        'localizations': [{'name': 'Rome'}]
    })
    
    assert builder.civilization['civilization_type'] == 'CIV_ROME'
    assert builder.localizations[0]['name'] == 'Rome'

def test_civilization_builder_build():
    """Builder should generate output files."""
    builder = CivilizationBuilder({...})
    files = builder.build()
    
    assert len(files) > 0
    assert all(isinstance(f, BaseFile) for f in files)
```

## Code Style and Formatting

### Line Length

- Maintain 100 character line limit (not 79)
- Break long lines logically

```python
# Good: Break at logical point
builder = CivilizationBuilder({
    'civilization_type': 'CIV_ROME',
    'civilization_traits': [TRAIT.ECONOMIC_CIV, TRAIT.MILITARY_CIV]
})

# Good: Long function calls
result = modifier_builder.fill({
    'collection': COLLECTION.PLAYER_UNITS,
    'effect': EFFECT.UNIT_ADJUST_MOVEMENT
})
```

### Blank Lines

- Two blank lines between classes
- One blank line between methods
- One blank line before return statements in multi-statement functions

```python
class CivilizationBuilder(BaseBuilder):
    """First class."""
    
    def build(self) -> list[BaseFile]:
        """Method one."""
        ...
    
    def _helper_method(self) -> None:
        """Helper method."""
        ...


class UnitBuilder(BaseBuilder):
    """Second class."""
    ...
```

## Examples

### Complete Builder Implementation

```python
from typing import Any
from civ7_modding_tools.builders.builders import BaseBuilder
from civ7_modding_tools.files import BaseFile, XmlFile
from civ7_modding_tools.nodes import MyNode

class MyBuilder(BaseBuilder):
    """Builder for MyEntity with full feature set.
    
    Demonstrates builder pattern, type hints, pydantic integration,
    and XML file generation.
    """
    
    my_property: str = ''
    another_property: int = 0
    optional_list: list[dict[str, Any]] = []
    
    def fill(self, payload: dict[str, Any]) -> "MyBuilder":
        """
        Populate properties from dictionary.
        
        Args:
            payload: Dictionary with property values.
        
        Returns:
            Self for method chaining.
        """
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def build(self) -> list[BaseFile]:
        """
        Generate output files.
        
        Returns:
            List of BaseFile instances ready to write to disk.
        """
        nodes = []
        for item in self.optional_list:
            node = MyNode(**item)
            nodes.append(node)
        
        file = XmlFile(
            path='/my-path/',
            name='my-file.xml',
            content={'Nodes': nodes}
        )
        
        return [file]
```

## Web Backend Development (web/app.py)

### FastAPI Endpoint Structure

Define endpoints with explicit type annotations and use Pydantic models for request/response serialization:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any

class YAMLLoadResponse(BaseModel):
    """Response structure for YAML load operations."""
    data: dict[str, Any]
    file_path: str
    success: bool

@app.post("/api/civilization/load", response_model=YAMLLoadResponse)
async def load_civilization_yaml(
    file_path: str
) -> YAMLLoadResponse:
    """
    Load and parse YAML civilization configuration.
    
    Args:
        file_path: Absolute path to YAML file
        
    Returns:
        YAMLLoadResponse with parsed data and metadata
        
    Raises:
        HTTPException: If file not found or YAML invalid
    """
    try:
        # Implementation
        pass
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
```

### YAML Processing (Safe)

Always use `yaml.safe_load()` and `yaml.dump()` with safe serialization:

```python
import yaml
from pathlib import Path

def load_yaml_safely(file_path: str) -> dict[str, Any]:
    """Load YAML with safety checks."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return data if data else {}

def save_yaml_safely(file_path: str, data: dict[str, Any]) -> None:
    """Save YAML with formatting."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
```

### Validation Models (Pydantic)

Use Pydantic models for input validation and response serialisation:

```python
from pydantic import BaseModel, field_validator

class ValidationErrorDetail(BaseModel):
    """Individual validation error with severity."""
    field: str
    message: str
    severity: str = Field(..., pattern="^(error|warning)$")

class ValidationResult(BaseModel):
    """Result of multi-level validation."""
    is_valid: bool
    errors: list[ValidationErrorDetail] = []
    warnings: list[ValidationErrorDetail] = []
    
    def add_error(self, field: str, message: str) -> None:
        """Add validation error."""
        self.errors.append(
            ValidationErrorDetail(field=field, message=message, 
                                  severity="error")
        )
```

### Reference Data Caching

Cache loaded JSON reference files to avoid repeated I/O operations:

```python
from functools import lru_cache
from pathlib import Path

_reference_data_cache: dict[str, Any] = {}
data_dir = Path(__file__).parent.parent / "data"

def load_reference_data(data_type: str) -> list[str]:
    """Load and cache reference data JSON file."""
    if data_type in _reference_data_cache:
        return _reference_data_cache[data_type]
    
    file_path = data_dir / f"{data_type}.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Reference data not found: {data_type}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    _reference_data_cache[data_type] = data
    return data
```

### Type-Safe Responses

Always return Pydantic models with explicit response_model parameter:

```python
from typing import Any

@app.get("/api/data/list", response_model=dict[str, list[str]])
async def list_reference_data() -> dict[str, list[str]]:
    """List all available reference data files."""
    files = sorted([f.stem for f in data_dir.glob("*.json")])
    return {"data_types": files}

@app.get("/api/data/{data_type}")
async def get_reference_data(
    data_type: str
) -> dict[str, Any]:
    """Get reference data with validation."""
    data = load_reference_data(data_type)
    return {"data": data}
```

## Best Practices Summary

1. **Always use type hints** - enables IDE support and catches errors
2. **Follow builder pattern** - fluent API with `fill()` method
3. **Use pydantic models** - automatic validation and serialisation
4. **Use constants enums** - type-safe game references
5. **Write comprehensive docstrings** - PEP 257 format with examples
6. **Test edge cases** - 90%+ coverage target
7. **Snake case for Python** - `my_property` not `myProperty`
8. **British English** - in comments and docstrings
9. **100 character limit** - split long lines logically
10. **Validate early** - catch errors in __init__ or fill() methods
11. **Use FastAPI response_model** - enables auto-generated documentation
12. **Cache reference data** - avoid repeated I/O from JSON files
13. **Implement multi-level validation** - client-side, server-side, enum checks
14. **Handle file operations safely** - use context managers, check paths