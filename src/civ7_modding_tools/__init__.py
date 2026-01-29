"""Civ7 Modding Tools - TypeScript-based code generation library for Civilization 7 mods."""

__version__ = "1.3.0"

# Core exports
from civ7_modding_tools.core import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
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
from civ7_modding_tools.nodes import BaseNode
from civ7_modding_tools.files import BaseFile, XmlFile, ImportFile, JsFile
from civ7_modding_tools.localizations import BaseLocalization

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
    "JsFile",
    # Localizations
    "BaseLocalization",
]
