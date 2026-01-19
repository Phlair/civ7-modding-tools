"""DatabaseNode and supporting node types for complete mod database structure."""

from typing import Optional
from civ7_modding_tools.nodes.base import BaseNode


# ============================================================================
# TYPE SYSTEM NODES
# ============================================================================

class KindNode(BaseNode):
    """Represents a Kind definition (category/classification)."""
    _name: str = "InsertOrIgnore"
    kind: Optional[str] = None
    
    def to_xml_element(self) -> dict | None:
        """Override to use KIND (all caps) instead of Kind."""
        result = super().to_xml_element()
        if result and '_attrs' in result and 'Kind' in result['_attrs']:
            # Rename Kind to KIND (all uppercase)
            result['_attrs']['KIND'] = result['_attrs'].pop('Kind')
        return result


class TypeNode(BaseNode):
    """Represents a Type definition."""
    _name: str = "Row"
    # Using 'type_' to avoid conflict with Python built-in 'type'
    # Will be serialized as 'Type' in XML
    type_: Optional[str] = None
    kind: Optional[str] = None


class TagNode(BaseNode):
    """Represents a Tag definition."""
    _name: str = "Row"
    tag: Optional[str] = None
    tag_string: Optional[str] = None
    category: Optional[str] = None


class TypeTagNode(BaseNode):
    """Represents a Type-Tag relationship."""
    _name: str = "Row"
    type_: Optional[str] = None
    tag: Optional[str] = None
    category: Optional[str] = None


# ============================================================================
# TRAIT & MODIFIER NODES
# ============================================================================

class TraitNode(BaseNode):
    """Represents a Trait definition."""
    _name: str = "Row"
    trait_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    internal_only: Optional[bool] = None


class TraitModifierNode(BaseNode):
    """Represents a Trait-Modifier relationship."""
    _name: str = "Row"
    trait_type: Optional[str] = None
    modifier_id: Optional[str] = None


# ============================================================================
# CIVILIZATION NODES
# ============================================================================

class CivilizationItemNode(BaseNode):
    """Represents a Civilization item (unit/building reference)."""
    _name: str = "Row"
    civilization_domain: Optional[str] = None
    civilization_type: Optional[str] = None
    type: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


class CivilizationTagNode(BaseNode):
    """Represents a Civilization-Tag relationship."""
    _name: str = "Row"
    civilization_domain: Optional[str] = None
    civilization_type: Optional[str] = None
    tag: Optional[str] = None


# ============================================================================
# BUILDING & IMPROVEMENT NODES
# ============================================================================

class BuildingNode(BaseNode):
    """Represents a Building definition."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    movable: Optional[bool] = False
    trait_type: Optional[str] = None


class ImprovementNode(BaseNode):
    """Represents an Improvement definition."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    improvement_type: Optional[str] = None
    improvement_class: Optional[str] = None


# ============================================================================
# CONSTRUCTIBLE CONSTRAINT NODES
# ============================================================================

class ConstructibleValidDistrictNode(BaseNode):
    """Represents constructible-district validity constraint."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    district_type: Optional[str] = None


class ConstructibleValidBiomeNode(BaseNode):
    """Represents constructible-biome validity constraint."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    biome_type: Optional[str] = None


class ConstructibleValidFeatureNode(BaseNode):
    """Represents constructible-feature validity constraint."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    feature_type: Optional[str] = None


class ConstructibleValidTerrainNode(BaseNode):
    """Represents constructible-terrain validity constraint."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    terrain_type: Optional[str] = None


class ConstructibleValidResourceNode(BaseNode):
    """Represents constructible-resource validity constraint."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    resource_type: Optional[str] = None


class ConstructibleMaintenanceNode(BaseNode):
    """Represents building maintenance requirements."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    yield_type: Optional[str] = None
    amount: Optional[int] = None


class ConstructiblePlunderNode(BaseNode):
    """Represents plunder from constructible."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    plunder_type: Optional[str] = None
    amount: Optional[int] = None


# ============================================================================
# ADJACENCY NODES
# ============================================================================

class ConstructibleAdjacencyNode(BaseNode):
    """Represents adjacency yield constraints for constructible."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    adjacency_type: Optional[str] = None


class WarehouseYieldChangeNode(BaseNode):
    """Represents warehouse-based yield changes."""
    _name: str = "Row"
    warehouse_type: Optional[str] = None
    yield_type: Optional[str] = None
    amount: Optional[int] = None


class ConstructibleWarehouseYieldNode(BaseNode):
    """Represents constructible-warehouse yield relationship."""
    _name: str = "Row"
    constructible_type: Optional[str] = None
    warehouse_type: Optional[str] = None


# ============================================================================
# UNLOCK & REWARD NODES
# ============================================================================

class UnlockNode(BaseNode):
    """Represents an Unlock configuration."""
    _name: str = "Row"
    unlock_id: Optional[str] = None
    unlock_era: Optional[str] = None


class UnlockRewardNode(BaseNode):
    """Represents a reward from an unlock."""
    _name: str = "Row"
    unlock_id: Optional[str] = None
    reward_type: Optional[str] = None
    reward_value: Optional[str] = None


class UnlockRequirementNode(BaseNode):
    """Represents a requirement for an unlock."""
    _name: str = "Row"
    unlock_id: Optional[str] = None
    requirement_set_id: Optional[str] = None


class UnlockConfigurationValueNode(BaseNode):
    """Represents unlock configuration value."""
    _name: str = "Row"
    unlock_id: Optional[str] = None
    config_key: Optional[str] = None
    config_value: Optional[str] = None


# ============================================================================
# REQUIREMENT NODES
# ============================================================================

class RequirementSetNode(BaseNode):
    """Represents a RequirementSet."""
    _name: str = "Row"
    requirement_set_id: Optional[str] = None
    requirement_set_type: Optional[str] = None


class RequirementNode(BaseNode):
    """Represents a Requirement."""
    _name: str = "Row"
    requirement_id: Optional[str] = None
    requirement_type: Optional[str] = None
    inverse: Optional[bool] = None


class RequirementArgumentNode(BaseNode):
    """Represents a Requirement argument."""
    _name: str = "Row"
    requirement_id: Optional[str] = None
    argument_name: Optional[str] = None
    argument_value: Optional[str] = None


class RequirementSetRequirementNode(BaseNode):
    """Represents a Requirement in a RequirementSet."""
    _name: str = "Row"
    requirement_set_id: Optional[str] = None
    requirement_id: Optional[str] = None


# ============================================================================
# MODIFIER & GAME EFFECT NODES
# ============================================================================

class ModifierNode(BaseNode):
    """Represents a Modifier."""
    _name: str = "Row"
    modifier_id: Optional[str] = None
    modifier_type: Optional[str] = None
    owner_type: Optional[str] = None
    owner_id: Optional[str] = None


class GameModifierNode(BaseNode):
    """Represents a game-wide modifier."""
    _name: str = "Row"
    modifier_id: Optional[str] = None


class ModifierStringNode(BaseNode):
    """Represents a modifier preview string for UI display."""
    _name: str = "Row"
    modifier_type: Optional[str] = None
    string_type: Optional[str] = None
    text: Optional[str] = None


class ArgumentNode(BaseNode):
    """Represents a modifier/effect argument."""
    _name: str = "Row"
    modifier_id: Optional[str] = None
    argument_name: Optional[str] = None
    argument_value: Optional[str] = None


# ============================================================================
# PROGRESSION TREE NODES
# ============================================================================

class ProgressionTreeAdvisoryNode(BaseNode):
    """Represents progression tree advisory."""
    _name: str = "Row"
    progression_tree_node_type: Optional[str] = None
    advisory_class_type: Optional[str] = None


class ProgressionTreeNodeUnlockNode(BaseNode):
    """Represents unlock in progression tree node."""
    _name: str = "Row"
    progression_tree_node_type: Optional[str] = None
    target_kind: Optional[str] = None
    target_type: Optional[str] = None
    unlock_depth: Optional[int] = None
    hidden: Optional[bool] = None


class ProgressionTreeQuoteNode(BaseNode):
    """Represents a narrative quote in progression tree."""
    _name: str = "Row"
    progression_tree_type: Optional[str] = None
    quote_type: Optional[str] = None
    text: Optional[str] = None


# ============================================================================
# TRADITION NODES
# ============================================================================

class TraditionModifierNode(BaseNode):
    """Represents a Tradition-Modifier relationship."""
    _name: str = "Row"
    tradition_type: Optional[str] = None
    modifier_id: Optional[str] = None


# ============================================================================
# LEADER UNLOCK NODES
# ============================================================================

class LeaderUnlockNode(BaseNode):
    """Represents a leader unlock - age transition for leader/civilization."""
    _name: str = "Row"
    leader_domain: Optional[str] = None
    leader_type: Optional[str] = None
    age_domain: Optional[str] = None
    age_type: Optional[str] = None
    type: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


class LeaderCivilizationBiasNode(BaseNode):
    """Represents leader-civilization bias."""
    _name: str = "Row"
    civilization_domain: Optional[str] = None
    civilization_type: Optional[str] = None
    leader_domain: Optional[str] = None
    leader_type: Optional[str] = None
    bias: Optional[int] = None
    reason_type: Optional[str] = None
    choice_type: Optional[str] = None


# ============================================================================
# DISTRICT FREE CONSTRUCTIBLES
# ============================================================================

class DistrictFreeConstructibleNode(BaseNode):
    """Represents free constructible from district."""
    _name: str = "Row"
    district_type: Optional[str] = None
    constructible_type: Optional[str] = None


# ============================================================================
# START BIAS NODES
# ============================================================================

class StartBiasResourceNode(BaseNode):
    """Represents start bias for resource placement."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    resource_type: Optional[str] = None
    bias: Optional[int] = None


# ============================================================================
# UNIT UPGRADE & ADVISORY NODES
# ============================================================================

class UnitUpgradeNode(BaseNode):
    """Represents unit upgrade path."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    upgrade_unit_type: Optional[str] = None


class UnitAdvisoryNode(BaseNode):
    """Represents unit advisory."""
    _name: str = "Row"
    unit_type: Optional[str] = None
    advisory_type: Optional[str] = None


# ============================================================================
# UNIQUE QUARTER NODES
# ============================================================================

class UniqueQuarterModifierNode(BaseNode):
    """Represents unique quarter modifier."""
    _name: str = "Row"
    unique_quarter_type: Optional[str] = None
    modifier_id: Optional[str] = None


# ============================================================================
# CIVILIZATION UNLOCK NODES
# ============================================================================

class CivilizationUnlockNode(BaseNode):
    """Represents civilization unlock (age progression)."""
    _name: str = "Row"
    civilization_unlock_id: Optional[str] = None
    unlock_id: Optional[str] = None
    era: Optional[str] = None
    civilization_domain: Optional[str] = None
    civilization_type: Optional[str] = None
    age_domain: Optional[str] = None
    age_type: Optional[str] = None
    type: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


# ============================================================================
# AI CONFIGURATION NODES
# ============================================================================

class AiListTypeNode(BaseNode):
    """Represents an AI list type definition."""
    _name: str = "Row"
    list_type: Optional[str] = None


class AiListNode(BaseNode):
    """Represents an AI list assignment to a leader/trait."""
    _name: str = "Row"
    list_type: Optional[str] = None
    leader_type: Optional[str] = None
    system: Optional[str] = None


class AiFavoredItemNode(BaseNode):
    """Represents an AI favored item (unit, building, etc)."""
    _name: str = "Row"
    list_type: Optional[str] = None
    item: Optional[str] = None
    value: Optional[int] = None
    favored: Optional[bool] = None
    string_val: Optional[str] = None
    tooltip_string: Optional[str] = None


class LeaderCivPriorityNode(BaseNode):
    """Represents AI leader civilization priorities."""
    _name: str = "Row"
    leader: Optional[str] = None
    civilization: Optional[str] = None
    priority: Optional[int] = None


class LoadingInfoCivilizationNode(BaseNode):
    """Represents loading screen information for a civilization."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    civilization_text: Optional[str] = None
    subtitle: Optional[str] = None
    tip: Optional[str] = None
    background_image_high: Optional[str] = None
    background_image_low: Optional[str] = None
    foreground_image: Optional[str] = None


class CivilizationFavoredWonderNode(BaseNode):
    """Represents wonders favored by a civilization."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    favored_wonder_type: Optional[str] = None
    favored_wonder_name: Optional[str] = None


# ============================================================================
# LEGACY NODES
# ============================================================================

class LegacyCivilizationNode(BaseNode):
    """Represents legacy civilization data."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    age: Optional[str] = None
    name: Optional[str] = None
    adjective: Optional[str] = None
    full_name: Optional[str] = None


class LegacyCivilizationTraitNode(BaseNode):
    """Represents legacy civilization-trait relationship."""
    _name: str = "Row"
    civilization_type: Optional[str] = None
    trait_type: Optional[str] = None


class UpdateWhereNode(BaseNode):
    """Represents a WHERE clause in an Update statement."""
    _name: str = "Where"
    independent_type: Optional[str] = None


class UpdateSetNode(BaseNode):
    """Represents a SET clause in an Update statement."""
    _name: str = "Set"
    name: Optional[str] = None


class LegacyIndependentsUpdateNode(BaseNode):
    """Represents an Update statement for LegacyIndependents."""
    _name: str = "Update"
    where_clause: Optional[UpdateWhereNode] = None
    set_clause: Optional[UpdateSetNode] = None

    def to_xml_element(self) -> Optional[dict]:
        """Override to generate nested Update structure."""
        if not self.where_clause or not self.set_clause:
            return None
        
        where_elem = self.where_clause.to_xml_element()
        set_elem = self.set_clause.to_xml_element()
        
        if not where_elem or not set_elem:
            return None
        
        return {
            '_name': 'Update',
            '_content': [where_elem, set_elem]
        }


# ============================================================================
# VISUAL & ICON NODES
# ============================================================================

class VisualRemapNode(BaseNode):
    """Represents visual remap configuration."""
    _name: str = "Row"
    visual_type: Optional[str] = None
    visual_key: Optional[str] = None
    visual_value: Optional[str] = None


class IconDefinitionNode(BaseNode):
    """Represents icon definition."""
    _name: str = "Row"
    id: Optional[str] = None
    path: Optional[str] = None

    def to_xml_element(self) -> dict | None:
        """Generate IconDefinitions row with nested ID/Path elements."""
        if not self.id or not self.path:
            return None

        return {
            '_name': 'Row',
            '_content': [
                {'_name': 'ID', '_content': self.id},
                {'_name': 'Path', '_content': self.path},
            ]
        }


# ============================================================================
# MAIN DATABASE NODE
# ============================================================================

class DatabaseNode(BaseNode):
    """
    Main container for all database entities.
    
    Represents the root <Database> element that contains all game data
    organized into logical tables. This is the foundational structure that
    all builders use to generate mod output.
    """
    
    _name: str = "Database"
    
    # Type System
    kinds: list['KindNode'] = []
    types: list['TypeNode'] = []
    tags: list['TagNode'] = []
    type_tags: list['TypeTagNode'] = []
    
    # Traits
    traits: list['TraitNode'] = []
    trait_modifiers: list['TraitModifierNode'] = []
    
    # Civilizations
    civilizations: list['BaseNode'] = []  # Can be CivilizationNode or slice types
    civilization_items: list['CivilizationItemNode'] = []
    civilization_tags: list['CivilizationTagNode'] = []
    civilization_traits: list = []
    civilization_unlocks: list['CivilizationUnlockNode'] = []
    legacy_civilization_traits: list['LegacyCivilizationTraitNode'] = []
    legacy_civilizations: list['LegacyCivilizationNode'] = []
    legacy_independents: list['LegacyIndependentsUpdateNode'] = []
    
    # Leaders
    leader_unlocks: list['BaseNode'] = []
    leader_civilization_bias: list['LeaderCivilizationBiasNode'] = []
    
    # Buildings & Improvements
    buildings: list['BuildingNode'] = []
    improvements: list['ImprovementNode'] = []
    constructibles: list['BaseNode'] = []
    constructible_maintenances: list['ConstructibleMaintenanceNode'] = []
    constructible_valid_districts: list['ConstructibleValidDistrictNode'] = []
    constructible_valid_biomes: list['ConstructibleValidBiomeNode'] = []
    constructible_valid_features: list['ConstructibleValidFeatureNode'] = []
    constructible_valid_terrains: list['ConstructibleValidTerrainNode'] = []
    constructible_valid_resources: list['ConstructibleValidResourceNode'] = []
    constructible_yield_changes: list['BaseNode'] = []
    adjacency_yield_changes: list['BaseNode'] = []
    constructible_adjacencies: list['ConstructibleAdjacencyNode'] = []
    warehouse_yield_changes: list['WarehouseYieldChangeNode'] = []
    constructible_warehouse_yields: list['ConstructibleWarehouseYieldNode'] = []
    constructible_plunders: list['ConstructiblePlunderNode'] = []
    
    # Cities
    city_names: list['BaseNode'] = []
    
    # Districts
    district_free_constructibles: list['DistrictFreeConstructibleNode'] = []
    
    # Progression Trees
    progression_tree_advisories: list['ProgressionTreeAdvisoryNode'] = []
    progression_trees: list['BaseNode'] = []
    progression_tree_nodes: list['BaseNode'] = []
    progression_tree_node_unlocks: list['ProgressionTreeNodeUnlockNode'] = []
    progression_tree_prereqs: list['BaseNode'] = []
    progression_tree_quotes: list['ProgressionTreeQuoteNode'] = []
    
    # Traditions
    traditions: list['BaseNode'] = []
    tradition_modifiers: list['TraditionModifierNode'] = []
    
    # Units
    units: list['BaseNode'] = []
    unit_costs: list['BaseNode'] = []
    unit_replaces: list['BaseNode'] = []
    unit_upgrades: list['UnitUpgradeNode'] = []
    unit_stats: list['BaseNode'] = []
    unit_advisories: list['UnitAdvisoryNode'] = []
    
    # Unlocks & Requirements
    unlocks: list['UnlockNode'] = []
    unlock_rewards: list['UnlockRewardNode'] = []
    unlock_requirements: list['UnlockRequirementNode'] = []
    unlock_configuration_values: list['UnlockConfigurationValueNode'] = []
    
    requirement_sets: list['RequirementSetNode'] = []
    requirements: list['RequirementNode'] = []
    requirement_arguments: list['RequirementArgumentNode'] = []
    requirement_set_requirements: list['RequirementSetRequirementNode'] = []
    
    # Text & Icons
    english_text: list['BaseNode'] = []
    icon_definitions: list['IconDefinitionNode'] = []
    visual_remaps: list['VisualRemapNode'] = []
    
    # Unique Quarters
    unique_quarters: list['BaseNode'] = []
    unique_quarter_modifiers: list['UniqueQuarterModifierNode'] = []
    
    # Modifiers
    game_modifiers: list['GameModifierNode'] = []
    modifier_strings: list['ModifierStringNode'] = []
    
    # Start Biases
    start_bias_biomes: list['BaseNode'] = []
    start_bias_resources: list['StartBiasResourceNode'] = []
    start_bias_terrains: list['BaseNode'] = []
    start_bias_rivers: list['BaseNode'] = []
    start_bias_feature_classes: list['BaseNode'] = []
    start_bias_adjacent_to_coasts: list['BaseNode'] = []
    
    # Visual Arts
    vis_art_civilization_building_cultures: list['BaseNode'] = []
    vis_art_civilization_unit_cultures: list['BaseNode'] = []
    
    # AI Configuration
    ai_list_types: list['AiListTypeNode'] = []
    ai_lists: list['AiListNode'] = []
    ai_favored_items: list['AiFavoredItemNode'] = []
    leader_civ_priorities: list['LeaderCivPriorityNode'] = []
    loading_info_civilizations: list['LoadingInfoCivilizationNode'] = []
    civilization_favored_wonders: list['CivilizationFavoredWonderNode'] = []

    def __init__(self, payload: dict | None = None) -> None:
        """Initialize DatabaseNode with optional payload."""
        super().__init__()
        if payload:
            self.fill(payload)

    def to_xml_element(self) -> dict | None:
        """
        Generate Database XML structure in jstoxml-compatible format.
        
        Converts all populated node arrays into table elements within
        the Database root element. Each table contains an array of Row elements.
        Skips empty arrays and handles special naming conventions for
        underscore-separated properties.
        
        Returns:
            XML element dict with Database structure matching TypeScript jstoxml format,
            or None if empty
            
        Format:
            {
                'Database': {
                    'Types': [
                        {'_name': 'Row', '_attrs': {'Type': 'VAL', 'Kind': 'KIND'}},
                        {'_name': 'Row', '_attrs': {'Type': 'VAL2', 'Kind': 'KIND2'}}
                    ],
                    'Units': [...]
                }
            }
        """
        # Check if all arrays are empty
        array_attrs = [
            attr for attr in dir(self)
            if not attr.startswith('_') and isinstance(getattr(self, attr), list)
        ]
        if all(len(getattr(self, attr, [])) == 0 for attr in array_attrs):
            return None

        data = {}
        
        # Custom table name mappings for TS compatibility
        table_name_mapping = {
            'constructible_maintenances': 'Constructible_Maintenances',
            'constructible_valid_districts': 'Constructible_ValidDistricts',
            'constructible_valid_biomes': 'Constructible_ValidBiomes',
            'constructible_valid_features': 'Constructible_ValidFeatures',
            'constructible_valid_terrains': 'Constructible_ValidTerrains',
            'constructible_valid_resources': 'Constructible_ValidResources',
            'constructible_yield_changes': 'Constructible_YieldChanges',
            'constructible_adjacencies': 'Constructible_Adjacencies',
            'constructible_plunders': 'Constructible_Plunders',
            'constructible_warehouse_yields': 'Constructible_WarehouseYields',
            'district_free_constructibles': 'District_FreeConstructibles',
            'adjacency_yield_changes': 'Adjacency_YieldChanges',
            'warehouse_yield_changes': 'Warehouse_YieldChanges',
            'progression_tree_advisories': 'ProgressionTree_Advisories',
            'progression_tree_nodes': 'ProgressionTreeNodes',
            'progression_tree_node_unlocks': 'ProgressionTreeNodeUnlocks',
            'progression_tree_prereqs': 'ProgressionTreePrereqs',
            'progression_tree_quotes': 'ProgressionTreeQuotes',
            'unit_costs': 'Unit_Costs',
            'unit_stats': 'Unit_Stats',
            'unit_advisories': 'Unit_Advisories',
            'unit_replaces': 'UnitReplaces',
            'unit_upgrades': 'Unit_Upgrades',
            'unlock_rewards': 'Unlock_Rewards',
            'unlock_requirements': 'Unlock_Requirements',
            'unlock_configuration_values': 'Unlock_ConfigurationValues',
            'requirement_sets': 'RequirementSets',
            'requirement_arguments': 'RequirementArguments',
            'requirement_set_requirements': 'RequirementSetRequirements',
            'legacy_civilizations': 'LegacyCivilizations',
            'legacy_civilization_traits': 'LegacyCivilizationTraits',
            'legacy_independents': 'LegacyIndependents',
            'civilization_items': 'CivilizationItems',
            'civilization_tags': 'CivilizationTags',
            'civilization_traits': 'CivilizationTraits',
            'civilization_unlocks': 'CivilizationUnlocks',
            'leader_unlocks': 'LeaderUnlocks',
            'leader_civilization_bias': 'LeaderCivilizationBias',
            'type_tags': 'TypeTags',
            'trait_modifiers': 'TraitModifiers',
            'tradition_modifiers': 'TraditionModifiers',
            'unique_quarters': 'UniqueQuarters',
            'unique_quarter_modifiers': 'UniqueQuarterModifiers',
            'game_modifiers': 'GameModifiers',
            'modifier_strings': 'ModifierStrings',
            'icon_definitions': 'IconDefinitions',
            'visual_remaps': 'VisualRemaps',
            'english_text': 'EnglishText',
            'city_names': 'CityNames',
            'start_bias_biomes': 'StartBiasBiomes',
            'start_bias_resources': 'StartBiasResources',
            'start_bias_terrains': 'StartBiasTerrains',
            'start_bias_rivers': 'StartBiasRivers',
            'start_bias_feature_classes': 'StartBiasFeatureClasses',
            'start_bias_adjacent_to_coasts': 'StartBiasAdjacentToCoasts',
            'vis_art_civilization_building_cultures': 'VisArt_CivilizationBuildingCultures',
            'vis_art_civilization_unit_cultures': 'VisArt_CivilizationUnitCultures',
            'ai_list_types': 'AiListTypes',
            'ai_lists': 'AiLists',
            'ai_favored_items': 'AiFavoredItems',
            'leader_civ_priorities': 'LeaderCivPriorities',
            'loading_info_civilizations': 'LoadingInfo_Civilizations',
            'civilization_favored_wonders': 'CivilizationFavoredWonders',
        }
        
        # Iterate through all properties
        for attr_name in self.model_fields:
            attr_value = getattr(self, attr_name, None)
            
            # Skip non-list attributes
            if not isinstance(attr_value, list) or len(attr_value) == 0:
                continue
            
            # Get table name (use mapping or convert from snake_case)
            if attr_name in table_name_mapping:
                table_name = table_name_mapping[attr_name]
            else:
                # Convert snake_case to PascalCase
                words = attr_name.split('_')
                table_name = ''.join(word.capitalize() for word in words)
            
            # Convert nodes to jstoxml format (array of {_name, _attrs})
            # Each node returns {'_name': 'Row', '_attrs': {...}}
            rows = []
            for node in attr_value:
                if node:
                    xml_elem = node.to_xml_element()
                    if xml_elem is not None:
                        rows.append(xml_elem)
            
            # Only add table if it has rows
            if rows:
                data[table_name] = rows
        
        return {'Database': data} if data else None
