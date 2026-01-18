"""Specialized node classes for Civ7 mod entities."""

from typing import Optional
from civ7_modding_tools.nodes.base import BaseNode


# Civilization Nodes
class CivilizationNode(BaseNode):
    """Represents a Civilization database row."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    base_tourism: Optional[int] = None
    legacy_modifier: Optional[bool] = None


class CivilizationTraitNode(BaseNode):
    """Represents a Civilization-Trait relationship."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    trait_type: Optional[str] = None


# Unit Nodes
class UnitNode(BaseNode):
    """Represents a Unit database row."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    base_movement: Optional[int] = None
    unit_class: Optional[str] = None
    cost: Optional[int] = None
    maintenance: Optional[int] = None


class UnitStatNode(BaseNode):
    """Represents unit stats."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    state: Optional[str] = None
    amount: Optional[int] = None


class UnitCostNode(BaseNode):
    """Represents unit production cost."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    yield_type: Optional[str] = None
    cost: Optional[int] = None


# Constructible Nodes (Buildings, Improvements)
class ConstructibleNode(BaseNode):
    """Represents a Building/Improvement database row."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    constructible_class: Optional[str] = None
    construction_cost: Optional[int] = None
    maintenance: Optional[int] = None


class ConstructibleYieldChangeNode(BaseNode):
    """Represents yield changes from constructibles."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    yield_type: Optional[str] = None
    yield_change: Optional[int] = None


# Localization Nodes
class EnglishTextNode(BaseNode):
    """Represents English text localization."""
    _name: str = "Row"
    tag: Optional[str] = None
    text: Optional[str] = None


class CityNameNode(BaseNode):
    """Represents a city name."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    city_name: Optional[str] = None


# Progression Tree Nodes
class ProgressionTreeNode(BaseNode):
    """Represents a progression tree."""
    _name: str = "Row"
    progression_tree_type: Optional[str] = None


class ProgressionTreeNodeNode(BaseNode):
    """Represents a node in a progression tree."""
    _name: str = "Row"
    progression_tree_type: Optional[str] = None
    node_id: Optional[str] = None
    tech_or_civic_type: Optional[str] = None


# Modifier/Effect Nodes
class ModifierNode(BaseNode):
    """Represents a game modifier."""
    _name: str = "Row"
    modifier_type: Optional[str] = None
    modifier_id: Optional[str] = None
    collection: Optional[str] = None


class GameEffectNode(BaseNode):
    """Represents a game effect."""
    _name: str = "Row"
    effect_type: Optional[str] = None
    amount: Optional[int] = None


class RequirementNode(BaseNode):
    """Represents a requirement."""
    _name: str = "Row"
    requirement_type: Optional[str] = None


# Start Bias Nodes
class StartBiasBiomeNode(BaseNode):
    """Represents a start bias for a biome."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    biome_type: Optional[str] = None
    bias_value: Optional[int] = None


class StartBiasTerrainNode(BaseNode):
    """Represents a start bias for terrain."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    terrain_type: Optional[str] = None
    bias_value: Optional[int] = None


# Import/Visual Nodes
class ImportNode(BaseNode):
    """Represents an imported resource."""
    _name: str = "Row"
    import_type: Optional[str] = None
    source_file: Optional[str] = None


class VisArtNode(BaseNode):
    """Represents visual art configuration."""
    _name: str = "Row"
    art_id: Optional[str] = None
    culture_type: Optional[str] = None
    path: Optional[str] = None


class ProgressionTreePrereqNode(BaseNode):
    """Represents a prerequisite for a progression tree node."""
    _name: str = "Row"
    progression_tree_type: Optional[str] = None
    from_progression_tree_node_type: Optional[str] = None


class TraditionNode(BaseNode):
    """Represents a cultural tradition."""
    _name: str = "Row"
    tradition_type: Optional[str] = None
    description: Optional[str] = None
    loyalty_per_turn: Optional[int] = None


class UniqueQuarterNode(BaseNode):
    """Represents a district-specific unique quarter building."""
    _name: str = "Row"
    unique_quarter_type: Optional[str] = None
    constructible_type: Optional[str] = None
    district_type: Optional[str] = None


class LeaderUnlockNode(BaseNode):
    """Represents a leader unlock configuration."""
    _name: str = "Row"
    leader_unlock_type: Optional[str] = None
    leader_type: Optional[str] = None
    civilization_type: Optional[str] = None
    start_bias: Optional[int] = None


class ModifierRequirementNode(BaseNode):
    """Represents a requirement for a modifier."""
    _name: str = "Row"
    modifier_type: Optional[str] = None
    requirement_type: Optional[str] = None
    requirement_set_type: Optional[str] = None


class StartBiasAdjacentToCoastNode(BaseNode):
    """Represents coast adjacency preference for civilization start bias."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    bias: Optional[int] = None


class StartBiasFeatureClassNode(BaseNode):
    """Represents feature class preference for civilization start bias."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    feature_class: Optional[str] = None
    bias: Optional[int] = None


class StartBiasRiverNode(BaseNode):
    """Represents river preference for civilization start bias."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    bias: Optional[int] = None


class StringNode(BaseNode):
    """Represents a generic string value."""
    _name: str = "Row"
    value: Optional[str] = None


class UnitReplaceNode(BaseNode):
    """Represents a unit replacement configuration."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    replaces_unit_type: Optional[str] = None
    era: Optional[str] = None


class VisArtCivilizationBuildingCultureNode(BaseNode):
    """Represents visual art configuration for civilization building culture."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    building_culture_type: Optional[str] = None
    visual_parent_type: Optional[str] = None


class VisArtCivilizationUnitCultureNode(BaseNode):
    """Represents visual art configuration for civilization unit culture."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    unit_culture_type: Optional[str] = None
    visual_parent_type: Optional[str] = None
