"""Civ7 Modding Tools - TypeScript-based code generation library for Civilization 7 mods."""

__version__ = "1.3.0"

# Core exports
from .core import Mod, ActionGroupBundle
from .builders import (
    BaseBuilder,
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ProgressionTreeBuilder,
    ModifierBuilder,
    TraditionBuilder,
    UniqueQuarterBuilder,
    LeaderUnlockBuilder,
    CivilizationUnlockBuilder,
    ProgressionTreeNodeBuilder,
    UnlockBuilder,
    ImportFileBuilder,
)
from .nodes import BaseNode
from .files import BaseFile, XmlFile, ImportFile
from .localizations import BaseLocalization

__all__ = [
    # Core
    "Mod",
    "ActionGroupBundle",
    # Builders
    "BaseBuilder",
    "CivilizationBuilder",
    "UnitBuilder",
    "ConstructibleBuilder",
    "ProgressionTreeBuilder",
    "ModifierBuilder",
    "TraditionBuilder",
    "UniqueQuarterBuilder",
    "LeaderUnlockBuilder",
    "CivilizationUnlockBuilder",
    "ProgressionTreeNodeBuilder",
    "UnlockBuilder",
    "ImportFileBuilder",
    # Nodes
    "BaseNode",
    # Files
    "BaseFile",
    "XmlFile",
    "ImportFile",
    # Localizations
    "BaseLocalization",
]
