"""Utility functions for property filling and manipulation."""

from typing import Any, Callable, Dict, TypeVar, Generic
import re

T = TypeVar("T")


def locale(prefix: str | None, variable: str) -> str:
    """
    Generate localization key from prefix and variable name.
    
    Matches TypeScript locale() function behavior:
    Converts to LOC_<PREFIX>_<VARIABLE_IN_UPPER_SNAKE_CASE>
    
    Examples:
        locale('CIVILIZATION_GONDOR', 'name') -> 'LOC_CIVILIZATION_GONDOR_NAME'
        locale('CIVILIZATION_GONDOR', 'cityNames_1') -> 'LOC_CIVILIZATION_GONDOR_CITY_NAMES_1'
        locale('UNIT_GONDOR_SCOUT', 'description') -> 'LOC_UNIT_GONDOR_SCOUT_DESCRIPTION'
    
    Args:
        prefix: Prefix for the localization key (e.g., 'CIVILIZATION_GONDOR')
        variable: Variable name in camelCase or snake_case
        
    Returns:
        Localization key string
    """
    if prefix is None:
        prefix = ''
    
    # Convert camelCase to snake_case
    # Handle sequences like 'cityNames_1' -> 'city_names_1'
    snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', variable)
    snake = snake.upper()
    
    return f"LOC_{prefix}_{snake}"


def fill(obj: T, payload: Dict[str, Any]) -> T:
    """
    Fill object properties from a dictionary payload.
    
    Similar to TypeScript fill() method - updates object properties
    from a partial dictionary and returns the object for chaining.
    
    Args:
        obj: Object to fill
        payload: Dictionary of properties to set
        
    Returns:
        The same object (for fluent API chaining)
    """
    for key, value in payload.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    return obj


def camel_to_pascal(name: str) -> str:
    """
    Convert camelCase to PascalCase.
    
    Examples:
        civilizationType -> CivilizationType
        baseTourism -> BaseTourism
        
    Args:
        name: camelCase string
        
    Returns:
        PascalCase string
    """
    if not name:
        return name
    return name[0].upper() + name[1:]


def start_case(name: str) -> str:
    """
    Convert camelCase to Start Case (space-separated title case).
    
    Examples:
        civilizationType -> Civilization Type
        myProperty -> My Property
        
    Args:
        name: camelCase string
        
    Returns:
        Space-separated title case string
    """
    if not name:
        return name
    
    result = [name[0].upper()]  # Capitalize first letter
    for i, char in enumerate(name[1:], 1):
        if char.isupper():
            result.append(" ")
        result.append(char)
    return "".join(result)


def without(lst: list[T], *values: T) -> list[T]:
    """
    Return a copy of list without specified values.
    
    Args:
        lst: Original list
        values: Values to exclude
        
    Returns:
        New list without the specified values
    """
    exclude_set = set(values)
    return [item for item in lst if item not in exclude_set]


def uniq_by(lst: list[T], key_func: Callable[[T], Any] | None = None) -> list[T]:
    """
    Return unique items from list based on a key function or identity.
    
    Args:
        lst: Original list
        key_func: Function to extract comparison key (default: identity)
        
    Returns:
        List with unique items (preserves order)
    """
    if key_func is None:
        key_func = lambda x: x
    
    seen = set()
    result = []
    for item in lst:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def flatten(lst: list[Any]) -> list[Any]:
    """
    Flatten a list of lists/tuples by one level.
    
    Args:
        lst: List of iterables
        
    Returns:
        Single flattened list
    """
    result = []
    for item in lst:
        if isinstance(item, (list, tuple)):
            result.extend(item)
        else:
            result.append(item)
    return result


def trim(s: str) -> str:
    """
    Remove common game entity prefixes from an ID string.
    
    Removes prefixes like CIVILIZATION_, UNIT_, BUILDING_, etc. to
    get the base entity name for use in file paths and configurations.
    
    Args:
        s: The ID string (e.g., "CIVILIZATION_ROME", "UNIT_ARCHER")
        
    Returns:
        Trimmed string without prefix (e.g., "ROME", "ARCHER")
        
    Examples:
        trim("CIVILIZATION_ROME") -> "ROME"
        trim("UNIT_ROMAN_ARCHER") -> "ROMAN_ARCHER"
        trim("BUILDING_FORUM") -> "FORUM"
        trim("TREE_CIVICS_GONDOR") -> "CIVICS_GONDOR"
    """
    prefixes_to_remove = [
        "CIVILIZATION_",
        "UNIT_",
        "BUILDING_",
        "IMPROVEMENT_",
        "DISTRICT_",
        "TRADITION_",
        "TECH_",
        "CIVIC_",
        "TRAIT_",
        "LEADER_",
        "GOLD_",
        "WONDER_",
        "GOVERNOR_",
        "TREE_",
        "QUARTER_",
    ]
    
    for prefix in prefixes_to_remove:
        if s.startswith(prefix):
            return s[len(prefix):]
    
    return s


def kebab_case(s: str) -> str:
    """
    Convert a string to kebab-case (lowercase with hyphens).
    
    Used for generating file paths and URLs from game entity names.
    Converts snake_case or PascalCase to kebab-case.
    
    Args:
        s: The input string (e.g., "RomanLegion", "roman_legion", "ROMAN_LEGION", "GONDOR2")
        
    Returns:
        Kebab-cased string (e.g., "roman-legion", "gondor-2")
        
    Examples:
        kebab_case("RomanLegion") -> "roman-legion"
        kebab_case("roman_legion") -> "roman-legion"
        kebab_case("ROMAN_LEGION") -> "roman-legion"
        kebab_case("GONDOR2") -> "gondor-2"
    """
    if not s:
        return s
    
    # First, replace underscores with hyphens
    result = s.replace('_', '-')
    
    # Insert hyphens before uppercase letters and digits (for PascalCase)
    # but only if previous character is lowercase or next is lowercase (camelCase detection)
    final = []
    for i, char in enumerate(result):
        if i > 0:
            prev_char = result[i - 1]
            next_char = result[i + 1] if i + 1 < len(result) else ''
            
            # Insert hyphen before uppercase if previous is lowercase or digit
            if char.isupper() and (prev_char.islower() or prev_char.isdigit()):
                if prev_char != '-':  # Don't add hyphen if already there
                    final.append('-')
            # Insert hyphen before digit if previous is letter
            elif char.isdigit() and prev_char.isalpha():
                if prev_char != '-':  # Don't add hyphen if already there
                    final.append('-')
            # Insert hyphen for acronym transition (e.g., "XMLParser" -> "xml-parser")
            elif char.isupper() and next_char.islower() and prev_char.isupper():
                if prev_char != '-':
                    final.append('-')
        
        final.append(char)
    
    result = ''.join(final).lower()
    
    # Replace multiple hyphens with single hyphen
    while '--' in result:
        result = result.replace('--', '-')
    
    return result
