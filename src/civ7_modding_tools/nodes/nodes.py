"""Specialized node classes for Civ7 mod entities."""

from typing import Optional
from civ7_modding_tools.nodes.base import BaseNode


# Civilization Nodes
class CivilizationNode(BaseNode):
    """Represents a Civilization database row (adaptive for game/shell scope)."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    # Game scope properties
    name: Optional[str] = None
    adjective: Optional[str] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    capital_name: Optional[str] = None
    starting_civilization_level_type: Optional[str] = None
    unique_culture_progression_tree: Optional[str] = None
    random_city_name_depth: Optional[int] = None
    base_tourism: Optional[int] = None
    legacy_modifier: Optional[bool] = None
    # Shell scope properties (optional, used for UI display)
    domain: Optional[str] = None
    civilization_name: Optional[str] = None
    civilization_full_name: Optional[str] = None
    civilization_description: Optional[str] = None
    civilization_icon: Optional[str] = None


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
    base_moves: Optional[int] = None
    base_sight_range: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    trait_type: Optional[str] = None
    core_class: Optional[str] = None
    domain: Optional[str] = None
    formation_class: Optional[str] = None
    unit_movement_class: Optional[str] = None
    air_slots: Optional[int] = None
    maintenance: Optional[int] = None
    promotion_class: Optional[str] = None
    cost: Optional[int] = None
    movement_range: Optional[int] = None
    power: Optional[int] = None
    ranged_power: Optional[int] = None
    ranged_range: Optional[int] = None
    origin_boost_modulus: Optional[int] = None
    tier: Optional[int] = None
    zone_of_control: Optional[bool] = None
    cost_progression_model: Optional[str] = None
    cost_progression_param1: Optional[int] = None
    can_train: Optional[bool] = None
    can_purchase: Optional[bool] = None
    can_earn_experience: Optional[bool] = None
    found_city: Optional[bool] = None
    make_trade_route: Optional[bool] = None
    prereq_population: Optional[int] = None


class UnitStatNode(BaseNode):
    """Represents unit stats."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    combat: Optional[int] = None
    ranged_combat: Optional[int] = None
    bombard_combat: Optional[int] = None
    anti_air_combat: Optional[int] = None
    range_: Optional[int] = None


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
    constructible_class: Optional[str] = "BUILDING"
    name: Optional[str] = None
    description: Optional[str] = None
    tooltip: Optional[str] = None
    cost: Optional[int] = 1
    population: Optional[int] = 1
    construction_cost: Optional[int] = None
    maintenance: Optional[int] = None


class ConstructibleYieldChangeNode(BaseNode):
    """Represents yield changes from constructibles."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    yield_type: Optional[str] = None
    yield_change: Optional[int] = None


class NamedPlaceYieldChangeNode(BaseNode):
    """Represents yield changes from named places."""
    _name: str = "Row"
    named_place_type: Optional[str] = None
    yield_type: Optional[str] = None
    yield_change: Optional[int] = None


# Localization Nodes
class EnglishTextNode(BaseNode):
    """Represents English text localization."""
    _name: str = "Row"
    tag: Optional[str] = None
    text: Optional[str] = None

    def to_xml_element(self) -> dict | None:
        """Convert English text node to XML with nested Text element."""
        if not self.tag:
            return None

        element: dict[str, object] = {
            "_name": self._name,
            "_attrs": {"Tag": self.tag},
        }

        if self.text is not None and self.text != "":
            element["_content"] = [
                {
                    "_name": "Text",
                    "_content": self.text,
                }
            ]

        return element


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
    age_type: Optional[str] = "AGE_ANTIQUITY"
    system_type: Optional[str] = "SYSTEM_CULTURE"
    name: Optional[str] = None


class ProgressionTreeNodeNode(BaseNode):
    """Represents a node in a progression tree."""
    _name: str = "Row"
    progression_tree_node_type: Optional[str] = None
    progression_tree: Optional[str] = None
    cost: Optional[int] = 150
    name: Optional[str] = None
    icon_string: Optional[str] = "cult_aksum"
    depth: Optional[int] = None
    index: Optional[int] = None


# Modifier/Effect Nodes
class ArgumentNode(BaseNode):
    """Represents a modifier argument."""
    _name: str = "Argument"
    name: Optional[str] = None
    value: Optional[str] = None
    
    def to_xml_element(self) -> dict | None:
        """Generate Argument XML with name attribute and text content."""
        if not self.name:
            return None
        return {
            '_name': 'Argument',
            '_attrs': {'name': self.name},
            '_content': str(self.value) if self.value is not None else ''
        }


class StringNode(BaseNode):
    """Represents a modifier string (for localization)."""
    _name: str = "String"
    context: Optional[str] = None
    value: Optional[str] = None
    
    def to_xml_element(self) -> dict | None:
        """Generate String XML with context attribute and text content."""
        if not self.context:
            return None
        return {
            '_name': 'String',
            '_attrs': {'context': self.context},
            '_content': str(self.value) if self.value is not None else ''
        }


class ModifierRequirementNode(BaseNode):
    """Represents a requirement for a modifier (in SubjectRequirements)."""
    _name: str = "Requirement"
    type_: Optional[str] = None  # Renamed to avoid conflict with builtin
    arguments: list[dict] = []
    
    def to_xml_element(self) -> dict | None:
        """Generate Requirement XML with nested Arguments."""
        if not self.type_:
            return None
        
        # Build argument elements
        arg_elements = []
        for arg in self.arguments:
            if isinstance(arg, dict) and 'name' in arg:
                arg_elements.append({
                    '_name': 'Argument',
                    '_attrs': {'name': arg['name']},
                    '_content': str(arg.get('value', ''))
                })
        
        return {
            '_name': 'Requirement',
            '_attrs': {'type': self.type_},
            '_content': arg_elements if arg_elements else None
        }


class ModifierNode(BaseNode):
    """Represents a complete game modifier with nested requirements and arguments."""
    _name: str = "Modifier"
    id: Optional[str] = None
    collection: Optional[str] = None
    effect: Optional[str] = None
    permanent: Optional[bool] = None
    run_once: Optional[bool] = None
    requirements: list[dict] = []
    arguments: list[dict] = []
    strings: list[dict] = []
    
    def to_xml_element(self) -> dict | None:
        """Generate Modifier XML with all nested elements."""
        if not self.id:
            return None
        
        # Build attributes
        attrs = {'id': self.id}
        if self.collection:
            attrs['collection'] = self.collection
        if self.effect:
            attrs['effect'] = self.effect
        if self.permanent is not None:
            attrs['permanent'] = 'true' if self.permanent else 'false'
        if self.run_once is not None:
            attrs['run-once'] = 'true' if self.run_once else 'false'
        
        # Build content elements
        content = []
        
        # Add SubjectRequirements if present
        if self.requirements:
            req_elements = []
            for req in self.requirements:
                if isinstance(req, dict) and 'type' in req:
                    req_node = ModifierRequirementNode()
                    req_node.type_ = req['type']
                    req_node.arguments = req.get('arguments', [])
                    req_elem = req_node.to_xml_element()
                    if req_elem:
                        req_elements.append(req_elem)
            
            if req_elements:
                content.append({
                    '_name': 'SubjectRequirements',
                    '_content': req_elements
                })
        
        # Add Arguments
        for arg in self.arguments:
            if isinstance(arg, dict) and 'name' in arg:
                content.append({
                    '_name': 'Argument',
                    '_attrs': {'name': arg['name']},
                    '_content': str(arg.get('value', ''))
                })
        
        # Add Strings
        for string in self.strings:
            if isinstance(string, dict) and 'context' in string:
                content.append({
                    '_name': 'String',
                    '_attrs': {'context': string['context']},
                    '_content': str(string.get('value', ''))
                })
        
        return {
            '_name': 'Modifier',
            '_attrs': attrs,
            '_content': content if content else None
        }


class GameEffectNode(BaseNode):
    """Represents the GameEffects root element containing modifiers."""
    _name: str = "GameEffects"
    modifiers: list[ModifierNode] = []
    
    def to_xml_element(self) -> dict | None:
        """Generate GameEffects XML root element."""
        if not self.modifiers:
            return None
        
        modifier_elements = []
        for modifier in self.modifiers:
            elem = modifier.to_xml_element()
            if elem:
                modifier_elements.append(elem)
        
        if not modifier_elements:
            return None
        
        return {
            '_name': 'GameEffects',
            '_attrs': {'xmlns': 'GameEffects'},
            '_content': modifier_elements
        }


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


# Visual Remap Nodes (special nested structure)
class VisualRemapRowNode(BaseNode):
    """Represents a visual remap with nested elements."""
    _name: str = "Row"
    id: Optional[str] = None
    display_name: Optional[str] = None
    kind: Optional[str] = None
    from_: Optional[str] = None  # 'from' is a keyword
    to: Optional[str] = None
    
    def to_xml_element(self) -> dict | None:
        """Generate Row XML with nested child elements (not attributes)."""
        if not self.id:
            return None
        
        # Build nested elements as children
        content = []
        if self.id:
            content.append({'_name': 'ID', '_content': self.id})
        if self.display_name:
            content.append({'_name': 'DisplayName', '_content': self.display_name})
        if self.kind:
            content.append({'_name': 'Kind', '_content': self.kind})
        if self.from_:
            content.append({'_name': 'From', '_content': self.from_})
        if self.to:
            content.append({'_name': 'To', '_content': self.to})
        
        return {
            '_name': 'Row',
            '_content': content if content else None
        }


class VisualRemapRootNode(BaseNode):
    """Root node for visual remaps."""
    _name: str = "VisualRemaps"
    rows: list[VisualRemapRowNode] = []
    
    def to_xml_element(self) -> dict | None:
        """Generate VisualRemaps XML root."""
        if not self.rows:
            return None
        
        row_elements = []
        for row in self.rows:
            elem = row.to_xml_element()
            if elem:
                row_elements.append(elem)
        
        if not row_elements:
            return None
        
        return {
            '_name': 'VisualRemaps',
            '_content': row_elements
        }


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
    node: Optional[str] = None
    prereq_node: Optional[str] = None


class TraditionNode(BaseNode):
    """Represents a cultural tradition."""
    _name: str = "Row"
    tradition_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    loyalty_per_turn: Optional[int] = None


class GreatPersonNode(BaseNode):
    """Represents a great person unit definition."""
    _name: str = "Row"
    great_person_type: Optional[str] = None
    great_person_class: Optional[str] = None
    base_unit_type: Optional[str] = None


class NamedPlaceNode(BaseNode):
    """Represents a named place location with regional effects."""
    _name: str = "Row"
    named_place_type: Optional[str] = None
    placement: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class UnitTierVariantNode(BaseNode):
    """Represents a unit tier variant (e.g., Veteran, Elite)."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    tier: Optional[int] = None
    combat_bonus: Optional[int] = None
    name_suffix: Optional[str] = None


class AdjacencyBonusNode(BaseNode):
    """Represents a custom adjacency bonus for buildings."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    adjacency_type: Optional[str] = None
    yield_type: Optional[str] = None
    amount: Optional[int] = None
    description: Optional[str] = None


class MultiTileBuildingNode(BaseNode):
    """Represents a multi-tile building/quarter component."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    component_building_type: Optional[str] = None
    layout: Optional[str] = None
    tile_index: Optional[int] = None


class UniqueQuarterNode(BaseNode):
    """Represents a district-specific unique quarter building."""
    _name: str = "Row"
    unique_quarter_type: Optional[str] = None
    building_type_1: Optional[str] = None
    building_type_2: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    trait_type: Optional[str] = None


class LeaderUnlockNode(BaseNode):
    """Represents a leader unlock configuration."""
    _name: str = "Row"
    leader_unlock_type: Optional[str] = None
    leader_type: Optional[str] = None
    civilization_type: Optional[str] = None
    start_bias: Optional[int] = None


# ModifierRequirementNode moved to Modifier/Effect section above


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


# StringNode moved to Modifier/Effect section above


class UnitReplaceNode(BaseNode):
    """Represents a unit replacement configuration."""
    _name: str = "Row"
    civ_unique_unit_type: Optional[str] = None
    replaces_unit_type: Optional[str] = None


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
