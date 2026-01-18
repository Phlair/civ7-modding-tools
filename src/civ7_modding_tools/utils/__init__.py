"""Utility functions for property filling and manipulation."""

from typing import Any, Callable, Dict, TypeVar, Generic

T = TypeVar("T")


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


def locale(tag: str, key: str) -> str:
    """
    Generate a localization key in the format TAG_KEY.
    
    Used for creating standardized localization keys that match
    game conventions. Converts input to uppercase and combines with tag.
    
    Args:
        tag: The localization tag (e.g., "LOC_UNIT", "LOC_BUILDING")
        key: The key name (e.g., "ROMAN_LEGION_NAME")
        
    Returns:
        Combined localization key (e.g., "LOC_UNIT_ROMAN_LEGION_NAME")
        
    Examples:
        locale("LOC_UNIT", "ROMAN_LEGION_NAME") -> "LOC_UNIT_ROMAN_LEGION_NAME"
        locale("LOC_BUILDING", "forum") -> "LOC_BUILDING_FORUM"
    """
    key_upper = key.upper() if isinstance(key, str) else str(key)
    return f"{tag}_{key_upper}"


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
        s: The input string (e.g., "RomanLegion", "roman_legion", "ROMAN_LEGION")
        
    Returns:
        Kebab-cased string (e.g., "roman-legion")
        
    Examples:
        kebab_case("RomanLegion") -> "roman-legion"
        kebab_case("roman_legion") -> "roman-legion"
        kebab_case("ROMAN_LEGION") -> "roman-legion"
    """
    if not s:
        return s
    
    # First, replace underscores with hyphens
    result = s.replace('_', '-')
    
    # Insert hyphens before uppercase letters (for PascalCase)
    # but only if previous character is lowercase or next is lowercase (camelCase detection)
    final = []
    for i, char in enumerate(result):
        if char.isupper() and i > 0:
            prev_char = result[i - 1]
            next_char = result[i + 1] if i + 1 < len(result) else ''
            
            # Insert hyphen if:
            # 1. Previous is lowercase or digit (camelCase transition)
            # 2. OR next is lowercase and this is part of an acronym transition (e.g., "XMLParser" -> "xml-parser")
            if (prev_char.islower() or prev_char.isdigit()) or (next_char.islower() and prev_char.isupper()):
                if prev_char != '-':  # Don't add hyphen if already there
                    final.append('-')
        
        final.append(char)
    
    result = ''.join(final).lower()
    
    # Replace multiple hyphens with single hyphen
    while '--' in result:
        result = result.replace('--', '-')
    
    return result
