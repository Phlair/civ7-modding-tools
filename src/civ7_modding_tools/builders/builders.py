"""Concrete builder implementations for Civilization 7 mods."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
from civ7_modding_tools.core.mod import ActionGroupBundle
from civ7_modding_tools.files import BaseFile, XmlFile
from civ7_modding_tools.nodes import (
    BaseNode,
    CivilizationNode,
    CivilizationTraitNode,
    CivilizationTagNode,
    CivilizationItemNode,
    CivilizationUnlockNode,
    UnitNode,
    UnitCostNode,
    UnitStatNode,
    UnitReplaceNode,
    UnitUpgradeNode,
    UnitAdvisoryNode,
    ConstructibleNode,
    ConstructibleYieldChangeNode,
    ConstructibleValidDistrictNode,
    ConstructibleValidTerrainNode,
    ConstructibleValidBiomeNode,
    ConstructibleValidFeatureNode,
    ConstructibleMaintenanceNode,
    ConstructiblePlunderNode,
    ConstructibleBuildingCostProgressionNode,
    ConstructibleAdvisoryNode,
    ConstructibleAdjacencyNode,
    AdjacencyYieldChangeNode,
    UniqueQuarterNode,
    UniqueQuarterModifierNode,
    ProgressionTreeNode,
    ProgressionTreeNodeNode,
    ProgressionTreePrereqNode,
    ProgressionTreeAdvisoryNode,
    ProgressionTreeNodeUnlockNode,
    ProgressionTreeQuoteNode,
    GameModifierNode,
    ModifierNode,
    ModifierStringNode,
    StringNode,
    TraditionNode,
    TraditionModifierNode,
    GreatPersonNode,
    NamedPlaceNode,
    NamedPlaceYieldChangeNode,
    NamedRiverNode,
    NamedVolcanoNode,
    NamedRiverCivilizationNode,
    NamedVolcanoCivilizationNode,
    CityNameNode,
    CivilizationCitizenNameNode,
    DatabaseNode,
    KindNode,
    TypeNode,
    TraitNode,
    TagNode,
    TypeTagNode,
    BuildingNode,
    ImprovementNode,
    StartBiasBiomeNode,
    StartBiasTerrainNode,
    StartBiasRiverNode,
    IconDefinitionNode,
    LegacyCivilizationNode,
    LegacyCivilizationTraitNode,
    EnglishTextNode,
    AiListTypeNode,
    AiListNode,
    AiFavoredItemNode,
    LeaderCivPriorityNode,
    LoadingInfoCivilizationNode,
    CivilizationFavoredWonderNode,
    VisArtCivilizationBuildingCultureNode,
    VisArtCivilizationUnitCultureNode,
    RequirementSetNode,
    RequirementSetRequirementNode,
    RequirementNode,
    RequirementArgumentNode,
    LeaderUnlockNode,
    LeaderCivilizationBiasNode,
)
from civ7_modding_tools.localizations import BaseLocalization
from civ7_modding_tools.utils import locale

T = TypeVar("T")


class BaseBuilder(ABC):
    """
    Abstract base class for all mod entity builders.
    
    Implements the builder pattern with fluent API for constructing mod entities.
    All concrete builders (CivilizationBuilder, UnitBuilder, etc.) extend this class.
    """

    action_group_bundle: ActionGroupBundle

    def __init__(self) -> None:
        """Initialize the builder with default action group bundle."""
        self.action_group_bundle = ActionGroupBundle()

    def fill(self, payload: Dict[str, Any]) -> "BaseBuilder":
        """
        Fill builder properties from a dictionary payload.
        
        Enables fluent API pattern: builder.fill({...}).build()
        
        Args:
            payload: Dictionary of properties to set
            
        Returns:
            Self for fluent API chaining
        """
        for key, value in payload.items():
            setattr(self, key, value)
        return self

    def with_dict(self, payload: Dict[str, Any]) -> "BaseBuilder":
        """
        Alias for fill() method using 'with' naming convention.
        
        Args:
            payload: Dictionary of properties to set
            
        Returns:
            Self for fluent API chaining
        """
        return self.fill(payload)

    @abstractmethod
    def build(self) -> list[BaseFile]:
        """
        Build and generate output files.
        
        Must be implemented by subclasses to create and return
        the files that represent the mod entity.
        
        Returns:
            List of BaseFile objects to be written to disk
        """
        pass

    def migrate(self) -> "BaseBuilder":
        """
        Hook for version migrations and transformations.
        
        Subclasses can override to implement migrations between versions.
        
        Returns:
            Self for fluent API chaining
        """
        return self

    def __repr__(self) -> str:
        """String representation of the builder."""
        return f"{self.__class__.__name__}()"


class CivilizationBuilder(BaseBuilder):
    """Builder for creating civilizations with full file generation."""
    
    def __init__(self) -> None:
        """Initialize civilization builder with all database variants."""
        super().__init__()
        # Database variants for different scopes and ages
        self._always = DatabaseNode()          # Always/base scope data
        self._current = DatabaseNode()         # Current age data
        self._shell = DatabaseNode()           # UI/shell scope data
        self._legacy = DatabaseNode()          # Legacy compatibility (INSERT OR IGNORE)
        self._icons = DatabaseNode()           # Icon definitions
        self._localizations = DatabaseNode()   # Localized text
        self._game_effects: Optional['GameEffectNode'] = None  # Modifiers and effects
        
        # Builder configuration
        self.civilization_type: Optional[str] = None
        self.civilization: Dict[str, Any] = {}
        self.civilization_traits: List[str] = []
        self.civilization_tags: List[str] = []
        self.localizations: List[Dict[str, Any]] = []
        self.start_bias_biomes: List[Dict[str, Any]] = []
        self.start_bias_terrains: List[Dict[str, Any]] = []
        self.start_bias_resources: List[Dict[str, Any]] = []
        self.start_bias_rivers: Optional[int] = None
        self.start_bias_adjacent_coasts: Optional[int] = None
        self.start_bias_feature_classes: List[Dict[str, Any]] = []
        self.city_names: List[str] = []
        self.icon: Dict[str, Any] = {}
        self.civilization_items: List[Dict[str, Any]] = []
        self.civilization_unlocks: List[Dict[str, Any]] = []
        self.leader_unlocks: List[Dict[str, Any]] = []
        self.leader_civilization_biases: List[Dict[str, Any]] = []
        self.modifiers: List[Dict[str, Any]] = []
        self.trait: Dict[str, str] = {}
        self.trait_ability: Dict[str, str] = {}
        self.civilization_legacy: Dict[str, Any] = {}
        
        # AI Configuration
        self.ai_list_types: List[Dict[str, Any]] = []
        self.ai_lists: List[Dict[str, Any]] = []
        self.ai_favored_items: List[Dict[str, Any]] = []
        self.leader_civ_priorities: List[Dict[str, Any]] = []
        self.loading_info_civilizations: List[Dict[str, Any]] = []
        self.civilization_favored_wonders: List[Dict[str, Any]] = []
        self.named_rivers: List[Dict[str, Any]] = []
        self.named_volcanoes: List[Dict[str, Any]] = []
        
        # Visual Art Configuration
        self.vis_art_building_cultures: List[str] = []
        self.vis_art_unit_cultures: List[str] = []
        self.building_culture_base: Optional[str] = None
        
        # Store bound items for processing during migration
        self._bound_items: List[BaseBuilder] = []

    def fill(self, payload: Dict[str, Any]) -> "CivilizationBuilder":
        """Fill civilization builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def _infer_civilization_domain(self) -> Optional[str]:
        """Infer the CivilizationDomain for shell UI tables."""
        explicit_domain = self.civilization.get("domain")
        if explicit_domain:
            return explicit_domain

        action_group_id = None
        if hasattr(self, "action_group_bundle") and self.action_group_bundle:
            action_group_id = self.action_group_bundle.action_group_id

        age_map = {
            "AGE_ANTIQUITY": "AntiquityAgeCivilizations",
            "AGE_EXPLORATION": "ExplorationAgeCivilizations",
            "AGE_MODERN": "ModernAgeCivilizations",
        }
        return age_map.get(action_group_id)

    def _infer_civilization_icon(self) -> Optional[str]:
        """Infer the CivilizationIcon for shell UI tables."""
        if not self.icon:
            return None

        if "path" in self.icon and self.icon.get("path"):
            return str(self.icon.get("path"))
        if "icon" in self.icon and self.icon.get("icon"):
            return str(self.icon.get("icon"))
        if "name" in self.icon and self.icon.get("name"):
            return str(self.icon.get("name"))
        return None

    def migrate(self) -> "CivilizationBuilder":
        """Migrate and populate all database variants with full localization."""
        if not self.civilization_type:
            self.civilization_type = self.civilization.get('civilization_type', 'CIVILIZATION_CUSTOM')
        
        # Auto-generate age trait from action_group_bundle
        age_trait_type = None
        if hasattr(self, 'action_group_bundle') and self.action_group_bundle:
            action_group_id = self.action_group_bundle.action_group_id
            if action_group_id and action_group_id.startswith('AGE_'):
                age = action_group_id.replace('AGE_', '')
                age_trait_type = f"TRAIT_{age}_CIV"
        
        # Generate trait types from civilization type if not provided
        if not self.trait:
            trait_base = self.civilization_type.replace('CIVILIZATION_', '')
            self.trait = {"trait_type": f"TRAIT_{trait_base}"}
        if not self.trait_ability:
            self.trait_ability = {"trait_type": f"{self.trait.get('trait_type', 'TRAIT')}_ABILITY"}
        
        trait_type = self.trait.get("trait_type", "TRAIT_CUSTOM")
        trait_ability_type = self.trait_ability.get("trait_type", "TRAIT_CUSTOM_ABILITY")
        
        # Create civilization node with full localisation
        civ_node = CivilizationNode(
            civilization_type=self.civilization_type,
            adjective=locale(self.civilization_type, 'adjective'),
            capital_name=locale(self.civilization_type, 'cityNames_1'),
            description=locale(self.civilization_type, 'description'),
            full_name=locale(self.civilization_type, 'fullName'),
            name=locale(self.civilization_type, 'name'),
            starting_civilization_level_type='CIVILIZATION_LEVEL_FULL_CIV',
        )
        shell_domain = self._infer_civilization_domain()
        shell_civ_node = CivilizationNode(
            civilization_type=self.civilization_type,
            domain=shell_domain,
            civilization_name=locale(self.civilization_type, 'name'),
            civilization_full_name=locale(self.civilization_type, 'fullName'),
            civilization_description=locale(self.civilization_type, 'description'),
            civilization_icon=self._infer_civilization_icon(),
        )
        # Apply any overrides from self.civilization dict
        for key, value in self.civilization.items():
            # Don't apply 'domain' to the current node (only for shell)
            if key != 'civilization_type' and key != 'domain' and hasattr(civ_node, key):
                setattr(civ_node, key, value)
        
        # For shell, only apply shell-specific properties (domain, civ names, icon)
        shell_domain_override = self.civilization.get('domain')
        if shell_domain_override:
            shell_civ_node.domain = shell_domain_override
        shell_civ_icon_override = self.civilization.get('civilization_icon')
        if shell_civ_icon_override:
            shell_civ_node.civilization_icon = shell_civ_icon_override
        
        # Create trait nodes
        trait_node = TraitNode(
            trait_type=trait_type,
            internal_only=True
        )
        
        # Get civ ability name from civilization dict (set in wizard Step 2)
        civ_ability_name = self.civilization.get('civ_ability_name', '')
        
        trait_ability_node = TraitNode(
            trait_type=trait_ability_type,
            name=locale(self.civilization_type + '_ABILITY', 'name'),
            description=locale(self.civilization_type + '_ABILITY', 'description'),
            internal_only=True
        )
        
        # Create age trait node if auto-generated
        age_trait_node = None
        if age_trait_type:
            age_trait_node = TraitNode(
                trait_type=age_trait_type,
                internal_only=True
            )
        
        # ==== POPULATE _current DATABASE ====
        # Types section
        types_list = [TypeNode(type_=trait_ability_type, kind="KIND_TRAIT")]
        # Add age trait type if auto-generated
        if age_trait_type:
            types_list.append(TypeNode(type_=age_trait_type, kind="KIND_TRAIT"))
        self._current.types = types_list
        
        # Traits section
        # Civilization ability trait with localization
        traits_list = [trait_ability_node]
        # Add age trait definition if auto-generated
        if age_trait_node:
            traits_list.append(age_trait_node)
        self._current.traits = traits_list
        
        # Handle civ_ability_modifier_ids from wizard Step 2
        # These link the TRAIT_{CIV}_ABILITY to the modifiers selected in the UI
        civ_ability_modifier_ids = self.civilization.get('civ_ability_modifier_ids', [])
        if civ_ability_modifier_ids:
            from civ7_modding_tools.nodes import TraitModifierNode
            if not self._current.trait_modifiers:
                self._current.trait_modifiers = []
            for modifier_id in civ_ability_modifier_ids:
                self._current.trait_modifiers.append(
                    TraitModifierNode(
                        trait_type=trait_ability_type,
                        modifier_id=modifier_id
                    )
                )
        
        # Civilizations section
        self._current.civilizations = [civ_node]
        
        # Civilization-Trait relationships
        civ_trait_nodes = [
            CivilizationTraitNode(
                civilization_type=self.civilization_type,
                trait_type=trait_type
            ),
            CivilizationTraitNode(
                civilization_type=self.civilization_type,
                trait_type=trait_ability_type
            ),
        ]
        # Add age trait if auto-generated
        if age_trait_type:
            civ_trait_nodes.append(
                CivilizationTraitNode(
                    civilization_type=self.civilization_type,
                    trait_type=age_trait_type
                )
            )
        # Add additional traits specified by user (attribute traits)
        for trait in self.civilization_traits:
            civ_trait_nodes.append(
                CivilizationTraitNode(
                    civilization_type=self.civilization_type,
                    trait_type=trait
                )
            )
        self._current.civilization_traits = civ_trait_nodes
        
        # Start biases - biomes
        start_bias_biomes = []
        for bias in self.start_bias_biomes:
            node = StartBiasBiomeNode(civilization_type=self.civilization_type)
            for key, value in bias.items():
                setattr(node, key, value)
            start_bias_biomes.append(node)
        self._current.start_bias_biomes = start_bias_biomes
        
        # Start biases - terrain
        start_bias_terrains = []
        for bias in self.start_bias_terrains:
            node = StartBiasTerrainNode(civilization_type=self.civilization_type)
            for key, value in bias.items():
                setattr(node, key, value)
            start_bias_terrains.append(node)
        self._current.start_bias_terrains = start_bias_terrains
        
        # Start biases - rivers
        if self.start_bias_rivers is not None:
            river_node = StartBiasRiverNode(
                civilization_type=self.civilization_type,
                score=self.start_bias_rivers
            )
            self._current.start_bias_rivers = [river_node]
        
        # City names - extract from localizations
        city_name_count = 0
        for loc in self.localizations:
            if isinstance(loc, dict) and 'city_names' in loc:
                city_name_count = max(city_name_count, len(loc['city_names']))
        
        if city_name_count > 0:
            city_name_nodes = []
            for i in range(1, city_name_count + 1):
                loc_key = locale(self.civilization_type, f'cityNames_{i}')
                city_name_nodes.append(
                    CityNameNode(
                        civilization_type=self.civilization_type,
                        city_name=loc_key
                    )
                )
            self._current.city_names = city_name_nodes
        
        # Citizen names - extract from localizations
        citizen_name_nodes = []
        for loc in self.localizations:
            if isinstance(loc, dict) and 'citizen_names' in loc:
                citizen_names = loc['citizen_names']
                if isinstance(citizen_names, dict):
                    male_names = citizen_names.get('male', [])
                    female_names = citizen_names.get('female', [])
                    for i, male_name in enumerate(male_names, 1):
                        loc_key = locale(self.civilization_type, f'citizenNames_male_{i}')
                        citizen_name_nodes.append(
                            CivilizationCitizenNameNode(
                                civilization_type=self.civilization_type,
                                citizen_name=loc_key
                                # Male entries: omit Female attribute entirely (game schema requirement)
                            )
                        )
                    for i, female_name in enumerate(female_names, 1):
                        loc_key = locale(self.civilization_type, f'citizenNames_female_{i}')
                        citizen_name_nodes.append(
                            CivilizationCitizenNameNode(
                                civilization_type=self.civilization_type,
                                citizen_name=loc_key,
                                female=True  # Only set Female="true" for female entries
                            )
                        )
        if citizen_name_nodes:
            self._current.civilization_citizen_names = citizen_name_nodes
        
        # Requirements & Requirement Sets
        requirement_set_nodes = [
            RequirementSetNode(
                requirement_set_id=f'REQSET_PLAYER_IS_{self.civilization_type.replace("CIVILIZATION_", "")}',
                requirement_set_type='REQUIREMENTSET_TEST_ALL'
            )
        ]
        self._current.requirement_sets = requirement_set_nodes
        
        req_set_req_nodes = [
            RequirementSetRequirementNode(
                requirement_set_id=f'REQSET_PLAYER_IS_{self.civilization_type.replace("CIVILIZATION_", "")}',
                requirement_id=f'REQ_PLAYER_HAS_TRAIT_{self.civilization_type.replace("CIVILIZATION_", "")}'
            )
        ]
        self._current.requirement_set_requirements = req_set_req_nodes
        
        req_nodes = [
            RequirementNode(
                requirement_id=f'REQ_PLAYER_HAS_TRAIT_{self.civilization_type.replace("CIVILIZATION_", "")}',
                requirement_type='REQUIREMENT_PLAYER_HAS_CIVILIZATION_OR_LEADER_TRAIT'
            )
        ]
        self._current.requirements = req_nodes
        
        req_arg_nodes = [
            RequirementArgumentNode(
                requirement_id=f'REQ_PLAYER_HAS_TRAIT_{self.civilization_type.replace("CIVILIZATION_", "")}',
                name='TraitType',
                value=trait_type
            )
        ]
        self._current.requirement_arguments = req_arg_nodes
        
        # AI Configuration - list types
        ai_list_type_nodes = []
        for config in self.ai_list_types:
            node = AiListTypeNode()
            for key, value in config.items():
                setattr(node, key, value)
            ai_list_type_nodes.append(node)
        self._current.ai_list_types = ai_list_type_nodes
        
        # AI Configuration - lists
        ai_list_nodes = []
        for config in self.ai_lists:
            node = AiListNode()
            for key, value in config.items():
                setattr(node, key, value)
            ai_list_nodes.append(node)
        self._current.ai_lists = ai_list_nodes
        
        # AI Configuration - favored items
        ai_favored_item_nodes = []
        for config in self.ai_favored_items:
            node = AiFavoredItemNode()
            for key, value in config.items():
                setattr(node, key, value)
            ai_favored_item_nodes.append(node)
        self._current.ai_favored_items = ai_favored_item_nodes
        
        # AI Configuration - leader civilization priorities
        # Auto-generate from leader_civilization_biases if not explicitly provided
        leader_civ_priority_nodes = []
        if self.leader_civ_priorities:
            # Use explicitly provided priorities
            for config in self.leader_civ_priorities:
                node = LeaderCivPriorityNode(civilization=self.civilization_type)
                for key, value in config.items():
                    if key != 'civilization_type':
                        # Map civilization_type to civilization, leader_type to leader
                        if key == 'civilization_type':
                            setattr(node, 'civilization', value)
                        elif key == 'leader_type':
                            setattr(node, 'leader', value)
                        else:
                            setattr(node, key, value)
                leader_civ_priority_nodes.append(node)
        elif self.leader_civilization_biases:
            # Auto-generate from leader_civilization_biases
            for bias in self.leader_civilization_biases:
                leader_type = bias.get('leader_type')
                bias_value = bias.get('bias', 2)
                if leader_type:
                    node = LeaderCivPriorityNode(
                        leader=leader_type,
                        civilization=self.civilization_type,
                        priority=bias_value
                    )
                    leader_civ_priority_nodes.append(node)
        self._current.leader_civ_priorities = leader_civ_priority_nodes
        
        # Loading Info - Civilizations
        loading_info_nodes = []
        for config in self.loading_info_civilizations:
            node = LoadingInfoCivilizationNode(civilization_type=self.civilization_type)
            for key, value in config.items():
                if key != 'civilization_type':
                    setattr(node, key, value)
            loading_info_nodes.append(node)
        self._current.loading_info_civilizations = loading_info_nodes
        
        # Civilization Favored Wonders
        favored_wonder_nodes = []
        for config in self.civilization_favored_wonders:
            node = CivilizationFavoredWonderNode(civilization_type=self.civilization_type)
            for key, value in config.items():
                if key != 'civilization_type':
                    # Map wonder_type to favored_wonder_type for backward compatibility
                    if key == 'wonder_type':
                        setattr(node, 'favored_wonder_type', value)
                    else:
                        setattr(node, key, value)
            favored_wonder_nodes.append(node)
        self._current.civilization_favored_wonders = favored_wonder_nodes
        
        # Named Places (Rivers & Volcanoes)
        # Generate separate definition and association tables per game schema
        named_river_definition_nodes = []
        named_river_civilization_nodes = []
        named_volcano_definition_nodes = []
        named_volcano_civilization_nodes = []
        
        # Process named rivers
        for river_config in self.named_rivers:
            named_place_type = river_config.get('named_place_type')
            if named_place_type:
                # Ensure uniqueness by prepending civ name if not already present
                civ_short_name = self.civilization_type.replace('CIVILIZATION_', '')
                if not named_place_type.startswith(f'{civ_short_name}_'):
                    named_place_type = f'{civ_short_name}_{named_place_type}'
                
                # Extract localization from config
                loc_key = None
                if 'localizations' in river_config:
                    for loc in river_config['localizations']:
                        if isinstance(loc, dict) and 'name' in loc:
                            # Use the civ-specific localization key (civ name already in named_place_type)
                            loc_key = f'LOC_{named_place_type}_NAME'
                            break
                
                # Definition table entry
                named_river_definition_nodes.append(
                    NamedRiverNode(
                        named_river_type=named_place_type,
                        name=loc_key
                    )
                )
                
                # Association table entry
                named_river_civilization_nodes.append(
                    NamedRiverCivilizationNode(
                        named_river_type=named_place_type,
                        civilization_type=self.civilization_type
                    )
                )
        
        # Process named volcanoes
        for volcano_config in self.named_volcanoes:
            named_place_type = volcano_config.get('named_place_type')
            if named_place_type:
                # Ensure uniqueness by prepending civ name if not already present
                civ_short_name = self.civilization_type.replace('CIVILIZATION_', '')
                if not named_place_type.startswith(f'{civ_short_name}_'):
                    named_place_type = f'{civ_short_name}_{named_place_type}'
                
                # Extract localization from config
                loc_key = None
                if 'localizations' in volcano_config:
                    for loc in volcano_config['localizations']:
                        if isinstance(loc, dict) and 'name' in loc:
                            # Use the civ-specific localization key (civ name already in named_place_type)
                            loc_key = f'LOC_{named_place_type}_NAME'
                            break
                
                # Definition table entry
                named_volcano_definition_nodes.append(
                    NamedVolcanoNode(
                        named_volcano_type=named_place_type,
                        name=loc_key
                    )
                )
                
                # Association table entry
                named_volcano_civilization_nodes.append(
                    NamedVolcanoCivilizationNode(
                        named_volcano_type=named_place_type,
                        civilization_type=self.civilization_type
                    )
                )
        
        # Assign to database nodes
        # Definitions go in "always" (they're map features that exist regardless of age)
        # Associations go in "current" (they reference CIVILIZATION_X which is defined there)
        if named_river_definition_nodes:
            self._always.named_rivers = named_river_definition_nodes
        if named_river_civilization_nodes:
            self._current.named_river_civilizations = named_river_civilization_nodes
        if named_volcano_definition_nodes:
            self._always.named_volcanoes = named_volcano_definition_nodes
        if named_volcano_civilization_nodes:
            self._current.named_volcano_civilizations = named_volcano_civilization_nodes
        
        # Visual Art Configuration - Building Cultures
        # Expand building_culture_base into all 3 ages if provided
        building_cultures_to_use = [
            culture for culture in self.vis_art_building_cultures if culture
        ]
        if self.building_culture_base:
            building_cultures_to_use.extend([
                f'ANT_{self.building_culture_base}',
                f'EXP_{self.building_culture_base}',
                f'MOD_{self.building_culture_base}',
            ])
        
        seen_cultures: set[str] = set()
        building_cultures_to_use = [
            culture
            for culture in building_cultures_to_use
            if not (culture in seen_cultures or seen_cultures.add(culture))
        ]
        
        vis_art_building_culture_nodes = []
        for building_culture in building_cultures_to_use:
            vis_art_building_culture_nodes.append(
                VisArtCivilizationBuildingCultureNode(
                    civilization_type=self.civilization_type,
                    building_culture=building_culture
                )
            )
        self._current.vis_art_civilization_building_cultures = vis_art_building_culture_nodes
        
        # Visual Art Configuration - Unit Cultures
        vis_art_unit_culture_nodes = []
        for unit_culture in self.vis_art_unit_cultures:
            vis_art_unit_culture_nodes.append(
                VisArtCivilizationUnitCultureNode(
                    civilization_type=self.civilization_type,
                    unit_culture=unit_culture
                )
            )
        self._current.vis_art_civilization_unit_cultures = vis_art_unit_culture_nodes
        
        # ==== POPULATE _shell DATABASE ====
        self._shell.civilizations = [shell_civ_node]
        
        # Civilization tags for shell
        civ_tag_nodes = []
        for tag_type in self.civilization_tags:
            civ_tag_nodes.append(
                CivilizationTagNode(
                    civilization_domain=shell_domain,
                    civilization_type=self.civilization_type,
                    tag_type=tag_type
                )
            )
        self._shell.civilization_tags = civ_tag_nodes
        
        # Civilization items for shell
        civ_item_nodes = []
        
        # Add civilization ability first
        if trait_ability_type:
            ability_item = CivilizationItemNode(
                civilization_domain=shell_domain,
                civilization_type=self.civilization_type,
                type=trait_ability_type,
                kind='KIND_TRAIT',
                name=locale(self.civilization_type + '_ABILITY', 'name'),
                description=locale(self.civilization_type + '_ABILITY', 'description')
            )
            civ_item_nodes.append(ability_item)
        
        # Add bound items (units, buildings, quarters)
        for item in self.civilization_items:
            node = CivilizationItemNode(
                civilization_domain=shell_domain,
                civilization_type=self.civilization_type
            )
            for key, value in item.items():
                if key != 'civilization_type':
                    setattr(node, key, value)
            civ_item_nodes.append(node)
        
        self._shell.civilization_items = civ_item_nodes
        
        # Civilization unlocks for age transitions (e.g., Babylon → Spain in Exploration Age)
        civ_unlock_nodes = []
        for unlock in self.civilization_unlocks:
            unlock_node = CivilizationUnlockNode(
                civilization_domain=shell_domain,
                civilization_type=self.civilization_type,
                age_domain=unlock.get('age_domain', 'StandardAges'),
                age_type=unlock.get('age_type'),
                type=unlock.get('type'),
                kind=unlock.get('kind', 'KIND_CIVILIZATION'),
                name=unlock.get('name'),
                description=unlock.get('description'),
                icon=unlock.get('icon')
            )
            civ_unlock_nodes.append(unlock_node)
        self._shell.civilization_unlocks = civ_unlock_nodes
        
        # Leader unlocks for shell (age transitions for leaders to play this civ)
        leader_unlock_nodes = []
        for unlock in self.leader_unlocks:
            unlock_node = LeaderUnlockNode(
                leader_domain=unlock.get('leader_domain', 'StandardLeaders'),
                leader_type=unlock.get('leader_type'),
                age_domain=unlock.get('age_domain', 'StandardAges'),
                age_type=unlock.get('age_type'),
                type=unlock.get('type'),
                kind=unlock.get('kind', 'KIND_CIVILIZATION'),
                name=unlock.get('name'),
                description=unlock.get('description'),
                icon=unlock.get('icon')
            )
            leader_unlock_nodes.append(unlock_node)
        self._shell.leader_unlocks = leader_unlock_nodes
        
        # Leader civilization biases for shell (UI leader affinity display)
        leader_civ_bias_nodes = []
        for bias in self.leader_civilization_biases:
            bias_node = LeaderCivilizationBiasNode(
                civilization_domain=shell_domain,
                civilization_type=self.civilization_type,
                leader_domain=bias.get('leader_domain', 'StandardLeaders'),
                leader_type=bias.get('leader_type'),
                bias=bias.get('bias', 0),
                reason_type=bias.get('reason_type'),
                choice_type=bias.get('choice_type')
            )
            leader_civ_bias_nodes.append(bias_node)
        self._shell.leader_civilization_bias = leader_civ_bias_nodes
        
        # ==== POPULATE _always DATABASE ====
        # Always scope: Base trait Type and Traits definitions available from game start
        # This ensures the base trait is available before age-specific content loads
        self._always.kinds = [
            KindNode(kind="KIND_TRAIT"),
        ]
        
        self._always.types = [
            TypeNode(type_=trait_type, kind="KIND_TRAIT"),
        ]
        
        # Base trait only (must be in always scope)
        always_trait = TraitNode(trait_type=trait_type, internal_only=True)
        self._always.traits = [always_trait]
        
        # ==== POPULATE _legacy DATABASE ====
        # Legacy system uses regular Row elements (game convention)
        legacy_civ_type = TypeNode(type_=self.civilization_type, kind="KIND_CIVILIZATION")
        self._legacy.types = [
            legacy_civ_type,
        ]
        
        legacy_civ = LegacyCivilizationNode(
            civilization_type=self.civilization_type,
            age=self.civilization_legacy.get("age", "AGE_ANTIQUITY"),
            name=locale(self.civilization_type, 'name'),
            adjective=locale(self.civilization_type, 'adjective'),
            full_name=locale(self.civilization_type, 'fullName')
        )
        self._legacy.legacy_civilizations = [legacy_civ]
        
        legacy_civ_trait = LegacyCivilizationTraitNode(
            civilization_type=self.civilization_type,
            trait_type=trait_type
        )
        self._legacy.legacy_civilization_traits = [legacy_civ_trait]
        
        # ==== POPULATE _icons DATABASE ====
        if self.icon:
            icon_node = IconDefinitionNode(id=self.civilization_type)
            for key, value in self.icon.items():
                setattr(icon_node, key, value)
            self._icons.icon_definitions = [icon_node]
        
        # ==== POPULATE _localizations DATABASE ====
        # Note: This will be populated as generic Row elements
        # In practice, localization is more complex in real mods
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                # Use entity_id if provided, otherwise use civilization_type
                prefix = loc.get("entity_id", self.civilization_type)
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=locale(prefix, "name"),
                        text=loc["name"]
                    ))
                if "description" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=locale(prefix, "description"),
                        text=loc["description"]
                    ))
                if "full_name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=locale(prefix, "fullName"),
                        text=loc["full_name"]
                    ))
                if "adjective" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=locale(prefix, "adjective"),
                        text=loc["adjective"]
                    ))
                if "city_names" in loc:
                    for i, city_name in enumerate(loc["city_names"], 1):
                        localization_rows.append(EnglishTextNode(
                            tag=locale(prefix, f"cityNames_{i}"),
                            text=city_name
                        ))
                if "citizen_names" in loc:
                    citizen_names = loc["citizen_names"]
                    if isinstance(citizen_names, dict):
                        male_names = citizen_names.get('male', [])
                        female_names = citizen_names.get('female', [])
                        for i, male_name in enumerate(male_names, 1):
                            localization_rows.append(EnglishTextNode(
                                tag=locale(prefix, f"citizenNames_male_{i}"),
                                text=male_name
                            ))
                        for i, female_name in enumerate(female_names, 1):
                            localization_rows.append(EnglishTextNode(
                                tag=locale(prefix, f"citizenNames_female_{i}"),
                                text=female_name
                            ))
        
        # Add civilization ability localization if civ_ability_name is provided
        if civ_ability_name:
            ability_loc_prefix = self.civilization_type + '_ABILITY'
            localization_rows.append(EnglishTextNode(
                tag=locale(ability_loc_prefix, 'name'),
                text=civ_ability_name
            ))
            # Add description if civ_ability_description is provided
            civ_ability_description = self.civilization.get('civ_ability_description', '')
            if civ_ability_description:
                localization_rows.append(EnglishTextNode(
                    tag=locale(ability_loc_prefix, 'description'),
                    text=civ_ability_description
                ))
        
        # Named Places Localizations (Rivers & Volcanoes)
        # Include civilization name in tag for uniqueness: LOC_ICENI_RIVER_XXX_NAME
        civ_short_name = self.civilization_type.replace('CIVILIZATION_', '')
        
        for river_config in self.named_rivers:
            named_place_type = river_config.get('named_place_type')
            if named_place_type and 'localizations' in river_config:
                # Ensure uniqueness by prepending civ name if not already present
                if not named_place_type.startswith(f'{civ_short_name}_'):
                    named_place_type = f'{civ_short_name}_{named_place_type}'
                
                for loc in river_config['localizations']:
                    if isinstance(loc, dict) and 'name' in loc:
                        # LOC key format: LOC_ICENI_RIVER_XXX_NAME (civ name already in named_place_type)
                        localization_rows.append(EnglishTextNode(
                            tag=f'LOC_{named_place_type}_NAME',
                            text=loc['name']
                        ))
        
        for volcano_config in self.named_volcanoes:
            named_place_type = volcano_config.get('named_place_type')
            if named_place_type and 'localizations' in volcano_config:
                # Ensure uniqueness by prepending civ name if not already present
                if not named_place_type.startswith(f'{civ_short_name}_'):
                    named_place_type = f'{civ_short_name}_{named_place_type}'
                
                for loc in volcano_config['localizations']:
                    if isinstance(loc, dict) and 'name' in loc:
                        # LOC key format: LOC_ICENI_VOLCANO_XXX_NAME (civ name already in named_place_type)
                        localization_rows.append(EnglishTextNode(
                            tag=f'LOC_{named_place_type}_NAME',
                            text=loc['name']
                        ))
        
        # Leader Civilization Bias Localizations (reason tooltips)
        for bias in self.leader_civilization_biases:
            reason_type = bias.get('reason_type')
            leader_type = bias.get('leader_type', '')
            if reason_type:
                # Generate a default tooltip if not provided in bias config
                # Extract leader name from LEADER_XXX format
                leader_name = leader_type.replace('LEADER_', '').replace('_', ' ').title() if leader_type else 'this leader'
                civ_name = self.civilization_type.replace('CIVILIZATION_', '').replace('_', ' ').title()
                
                # Check if there's a custom tooltip text in the bias config
                tooltip_text = bias.get('reason_text')
                if not tooltip_text:
                    # Generate default tooltip based on choice type
                    choice_type = bias.get('choice_type', '')
                    if 'GEOGRAPHIC' in choice_type:
                        tooltip_text = f"{leader_name} has a geographic affinity for {civ_name}."
                    elif 'HISTORICAL' in choice_type:
                        tooltip_text = f"{leader_name} has a historical connection to {civ_name}."
                    elif 'STRATEGIC' in choice_type:
                        tooltip_text = f"{leader_name}'s playstyle aligns well with {civ_name}."
                    else:
                        tooltip_text = f"{leader_name} favors {civ_name}."
                
                localization_rows.append(EnglishTextNode(
                    tag=reason_type,
                    text=tooltip_text
                ))
        
        # Civilization Favored Wonders Localizations
        for wonder_config in self.civilization_favored_wonders:
            favored_wonder_name_key = wonder_config.get('favored_wonder_name')
            favored_wonder_type = wonder_config.get('favored_wonder_type', '')
            if favored_wonder_name_key:
                # Extract wonder name from WONDER_XXX format for display
                wonder_display_name = favored_wonder_type.replace('WONDER_', '').replace('_', ' ').title()
                localization_rows.append(EnglishTextNode(
                    tag=favored_wonder_name_key,
                    text=wonder_display_name
                ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        # ==== PROCESS BOUND ITEMS (after migration) ====
        if self._bound_items:
            from civ7_modding_tools.nodes import TraitModifierNode, GameModifierNode
            
            trait_type = self.trait.get("trait_type", "TRAIT_CUSTOM")
            trait_ability_type = self.trait_ability.get("trait_type", "TRAIT_CUSTOM_ABILITY")
            
            for item in self._bound_items:
                # Handle ModifierBuilder
                if hasattr(item, 'modifier') and hasattr(item, '_game_effects'):
                    if hasattr(item, 'migrate'):
                        item.migrate()
                    
                    # Merge game effects from ModifierBuilder
                    if item._game_effects and hasattr(item._game_effects, 'modifiers'):
                        # Add modifiers to civilization's game-effects.xml
                        if not self._game_effects:
                            from civ7_modding_tools.nodes import GameEffectNode
                            self._game_effects = GameEffectNode()
                            self._game_effects.modifiers = []
                        
                        # Add the modifier nodes directly
                        self._game_effects.modifiers.extend(item._game_effects.modifiers)
                        
                        # Link modifiers to trait (if not detached)
                        # TraitModifiers must be in always scope since modifiers are loaded in always action group
                        # Bind to base TRAIT_{CIV}, not TRAIT_{CIV}_ABILITY
                        if not getattr(item, 'is_detached', False):
                            if not self._always.trait_modifiers:
                                self._always.trait_modifiers = []
                            for modifier in item._game_effects.modifiers:
                                self._always.trait_modifiers.append(
                                    TraitModifierNode(
                                        trait_type=trait_type,  # Use base trait, not ability trait
                                        modifier_id=modifier.id
                                    )
                                )
                    
                    # Merge localizations
                    if hasattr(item, '_localizations') and item._localizations:
                        if item._localizations.english_text:
                            if not self._localizations.english_text:
                                self._localizations.english_text = []
                            self._localizations.english_text.extend(item._localizations.english_text)
                
                # Handle UnitBuilder
                elif hasattr(item, 'unit_type') and item.unit_type:
                    if hasattr(item, '_current') and item._current:
                        for unit in getattr(item._current, 'units', []):
                            unit.trait_type = trait_type
                
                # Handle ConstructibleBuilder
                elif hasattr(item, 'constructible_type') and item.constructible_type:
                    if hasattr(item, 'migrate'):
                        item.migrate()
                    if hasattr(item, '_always') and item._always:
                        for building in getattr(item._always, 'buildings', []):
                            building.trait_type = trait_type
                        for improvement in getattr(item._always, 'improvements', []):
                            improvement.trait_type = trait_type
                
                # Handle UniqueQuarterBuilder
                elif hasattr(item, 'unique_quarter_type') and item.unique_quarter_type:
                    if hasattr(item, 'migrate'):
                        item.migrate()
                    if hasattr(item, '_always') and item._always:
                        for unique_quarter in getattr(item._always, 'unique_quarters', []):
                            unique_quarter.trait_type = trait_type
                
                # Handle ProgressionTreeBuilder - add reveal modifier
                elif hasattr(item, 'progression_tree_type') and item.progression_tree_type:
                    # Generate culture tree reveal modifier for the civilization
                    from civ7_modding_tools.nodes import GameEffectNode
                    from civ7_modding_tools.nodes.nodes import ModifierNode
                    
                    reveal_modifier = ModifierNode()
                    reveal_modifier.id = f'MOD_TREE_{item.progression_tree_type.replace("TREE_", "")}_REVEAL'
                    reveal_modifier.collection = 'COLLECTION_OWNER'
                    reveal_modifier.effect = 'EFFECT_PLAYER_REVEAL_CULTURE_TREE'
                    reveal_modifier.requirements = [{
                        'type': 'REQUIREMENT_PLAYER_HAS_CIVILIZATION_OR_LEADER_TRAIT',
                        'arguments': [{'name': 'TraitType', 'value': trait_type}]
                    }]
                    reveal_modifier.arguments = [
                        {'name': 'ProgressionTreeType', 'value': item.progression_tree_type}
                    ]
                    
                    # Add to civilization's game effects
                    if not self._game_effects:
                        self._game_effects = GameEffectNode()
                        self._game_effects.modifiers = []
                    self._game_effects.modifiers.append(reveal_modifier)
                    
                    # Also add to trait modifiers (must be in always scope)
                    if not self._always.trait_modifiers:
                        self._always.trait_modifiers = []
                    self._always.trait_modifiers.append(
                        TraitModifierNode(
                            trait_type=trait_ability_type,
                            modifier_id=reveal_modifier.id
                        )
                    )
        
        return self

    def _extract_icon_path(self, icon_dict: Optional[Dict[str, Any]]) -> Optional[str]:
        """Extract icon filename from full path. Auto-converts fs://... paths."""
        if not icon_dict:
            return None
        
        path = icon_dict.get('path') or icon_dict.get('icon')
        if not path:
            return None
        
        # Convert fs://game/babylon/civ_sym_babylon -> civ_sym_babylon
        if isinstance(path, str) and 'fs://' in path:
            return path.split('/')[-1]
        
        return str(path)
    
    def _infer_kind(self, builder: BaseBuilder) -> str:
        """Auto-detect KIND based on builder type."""
        if isinstance(builder, UnitBuilder):
            return 'KIND_UNIT'
        elif isinstance(builder, ConstructibleBuilder):
            if hasattr(builder, 'unique_quarter_type') and builder.unique_quarter_type:
                return 'KIND_QUARTER'
            return 'KIND_BUILDING'
        elif isinstance(builder, UniqueQuarterBuilder):
            return 'KIND_QUARTER'
        return 'KIND_BUILDING'
    
    def bind(self, items: List[BaseBuilder]) -> "CivilizationBuilder":
        """Bind entities to this civilization and auto-register as CivilizationItems."""
        # Store items for processing during migration
        self._bound_items.extend(items)
        
        # Auto-register bound items as civilization items for UI display
        for item in items:
            item_type = None
            kind = None
            icon = None
            
            if isinstance(item, UnitBuilder) and item.unit_type:
                item_type = item.unit_type
                kind = 'KIND_UNIT'
                icon = self._extract_icon_path(item.icon)
                # Set civilization_type on unit for automatic trait assignment
                item.civilization_type = self.civilization_type
                # Skip adding to CivilizationItems if show_in_civ_picker is False
                if not getattr(item, 'show_in_civ_picker', True):
                    continue
            elif isinstance(item, ConstructibleBuilder) and item.constructible_type:
                item_type = item.constructible_type
                if item.constructible_type.startswith('QUARTER_'):
                    kind = 'KIND_QUARTER'
                else:
                    kind = 'KIND_BUILDING'
                icon = self._extract_icon_path(item.icon)
            elif isinstance(item, UniqueQuarterBuilder) and item.unique_quarter_type:
                item_type = item.unique_quarter_type
                kind = 'KIND_QUARTER'
                icon = 'city_uniquequarter'
            elif isinstance(item, ProgressionTreeBuilder):
                continue
            else:
                continue
            
            if item_type and kind:
                loc_name = locale(item_type, 'name')
                loc_description = locale(item_type, 'description')
                
                self.civilization_items.append({
                    'type': item_type,
                    'kind': kind,
                    'name': loc_name,
                    'description': loc_description,
                    'icon': icon
                })
        
        return self

    def build(self) -> list[BaseFile]:
        """Build civilization files."""
        if not self.civilization_type:
            return []
        
        self.migrate()
        
        # Generate path from civilization type (trimmed + kebab-case)
        from civ7_modding_tools.utils import trim, kebab_case
        trimmed = trim(self.civilization_type)
        path = f"/civilizations/{kebab_case(trimmed)}/"
        
        files: list[BaseFile] = [
            XmlFile(
                path=path,
                name="always.xml",
                content=self._always,
                action_group=self.action_group_bundle.always
            ),
            XmlFile(
                path=path,
                name="current.xml",
                content=self._current,
                action_group=self.action_group_bundle.current
            ),
            XmlFile(
                path=path,
                name="legacy.xml",
                content=self._legacy,
                action_group=self.action_group_bundle.always
            ),
            XmlFile(
                path=path,
                name="shell.xml",
                content=self._shell,
                action_group=self.action_group_bundle.shell
            ),
            XmlFile(
                path=path,
                name="icons.xml",
                content=self._icons,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
            XmlFile(
                path=path,
                name="localization.xml",
                content=self._localizations,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
            XmlFile(
                path=path,
                name="game-effects.xml",
                content=self._game_effects,
                action_group=self.action_group_bundle.always
            ),
        ]
        
        # Filter out empty files (content is None)
        files = [f for f in files if f.content is not None]
        
        return files


class UnitBuilder(BaseBuilder):
    """Builder for creating units with multiple file generation."""
    
    def __init__(self) -> None:
        """Initialize unit builder with database variants."""
        super().__init__()
        self._current = DatabaseNode()
        self._icons = DatabaseNode()
        self._localizations = DatabaseNode()
        self._visual_remap: Optional[DatabaseNode] = None
        
        self.unit_type: Optional[str] = None
        self.base_unit_type: Optional[str] = None  # For grouping upgrade chains in same folder
        self.civilization_type: Optional[str] = None  # Parent civilization for trait assignment
        self.unit: Dict[str, Any] = {}
        self.unit_stats: list[Dict[str, Any]] = []
        self.unit_costs: list[Dict[str, Any]] = []
        self.unit_cost: Dict[str, Any] = {}  # Support single cost format
        self.unit_stat: Dict[str, Any] = {}  # Support single stat format
        self.unit_replace: Optional[Dict[str, Any]] = None
        self.unit_upgrade: Optional[Dict[str, Any]] = None
        self.unit_advisories: list[Dict[str, Any]] = []
        self.tier_variants: list[Dict[str, Any]] = []  # Phase 5: Unit tier variants
        self.visual_remap: Optional[Dict[str, Any]] = None
        self.icon: Dict[str, Any] = {}
        self.localizations: list[Dict[str, Any]] = []
        self.type_tags: list[str] = []  # Additional type tags (e.g., UNIT_CLASS_RECON)
        self.unlock_tech: Optional[str] = None  # Tech node that unlocks this unit
        self.unlock_civic: Optional[str] = None  # Civic node that unlocks this unit
        self.auto_infer_unlock: bool = True  # Auto-detect unlock from replaced unit
        self.show_in_civ_picker: bool = True  # Display in civilization selection screen
        self.unit_abilities: list[Dict[str, Any]] = []  # Simple dict-based abilities
        self._bound_abilities: List['UnitAbilityBuilder'] = []  # Builder-based abilities
        self._bound_modifiers: List['ModifierBuilder'] = []  # Modifiers for unit abilities

    def fill(self, payload: Dict[str, Any]) -> "UnitBuilder":
        """Fill unit builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "UnitBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        
        if not self.unit_type:
            return self
        
        # Generate localization keys
        loc_name = locale(self.unit_type, 'name')
        loc_description = locale(self.unit_type, 'description')
        
        # ==== POPULATE _current DATABASE ====
        # Types
        self._current.types = [
            TypeNode(type_=self.unit_type, kind="KIND_UNIT"),
        ]
        
        # Tags - create unit class tag
        unit_class_tag = self.unit_type.replace('UNIT_', 'UNIT_CLASS_')
        self._current.tags = [
            TagNode(tag=unit_class_tag, category='UNIT_CLASS')
        ]
        
        # TypeTags - link unit to its class tag and any additional type tags
        type_tags = [
            TypeTagNode(type_=self.unit_type, tag=unit_class_tag)
        ]
        # Add user-specified type tags (like UNIT_CLASS_RECON)
        if hasattr(self, 'type_tags') and self.type_tags:
            for tag in self.type_tags:
                type_tags.append(TypeTagNode(type_=self.unit_type, tag=tag))
        
        # Auto-generate additional type tags based on unit properties
        type_tags.extend(self._generate_type_tags())
        
        self._current.type_tags = type_tags
        
        # Unit definition with full properties and localization
        unit_node = UnitNode(
            unit_type=self.unit_type,
            name=loc_name,
            description=loc_description,
        )
        # Apply all user-provided unit properties
        for key, value in self.unit.items():
            setattr(unit_node, key, value)
        
        # Auto-set trait_type from civilization_type if not explicitly set
        if self.civilization_type and not unit_node.trait_type:
            unit_node.trait_type = self.civilization_type.replace('CIVILIZATION_', 'TRAIT_')
        
        self._current.units = [unit_node]
        
        # Unit costs
        if self.unit_costs:
            cost_nodes = []
            for cost in self.unit_costs:
                cost_node = UnitCostNode(unit_type=self.unit_type)
                for key, value in cost.items():
                    setattr(cost_node, key, value)
                cost_nodes.append(cost_node)
            self._current.unit_costs = cost_nodes
        elif hasattr(self, 'unit_cost') and self.unit_cost:
            # Support single cost format
            cost_node = UnitCostNode(unit_type=self.unit_type)
            for key, value in self.unit_cost.items():
                setattr(cost_node, key, value)
            self._current.unit_costs = [cost_node]
        
        # Unit replace
        if self.unit_replace:
            replace_node = UnitReplaceNode(
                civ_unique_unit_type=self.unit_type,
                replaces_unit_type=self.unit_replace.get('replaces_unit_type') or self.unit_replace.get('replacesUnitType')
            )
            self._current.unit_replaces = [replace_node]
        
        # Unit stats
        if self.unit_stats:
            stat_nodes = []
            for stat in self.unit_stats:
                stat_node = UnitStatNode(unit_type=self.unit_type)
                for key, value in stat.items():
                    setattr(stat_node, key, value)
                stat_nodes.append(stat_node)
            self._current.unit_stats = stat_nodes
        elif hasattr(self, 'unit_stat') and self.unit_stat:
            # Support single stat format
            stat_node = UnitStatNode(unit_type=self.unit_type)
            for key, value in self.unit_stat.items():
                setattr(stat_node, key, value)
            self._current.unit_stats = [stat_node]
        
        # Unit upgrade
        if self.unit_upgrade:
            upgrade_node = UnitUpgradeNode(
                unit=self.unit_type,
                upgrade_unit=self.unit_upgrade.get('upgrade_unit') or self.unit_upgrade.get('upgradeUnit')
            )
            self._current.unit_upgrades = [upgrade_node]
        
        # Unit advisories
        if self.unit_advisories:
            advisory_nodes = []
            for advisory in self.unit_advisories:
                advisory_node = UnitAdvisoryNode(
                    unit_type=self.unit_type,
                    advisory_class_type=advisory.get('advisory_class_type') or advisory.get('advisoryClassType')
                )
                advisory_nodes.append(advisory_node)
            self._current.unit_advisories = advisory_nodes
        
        # Unit abilities (process both dict-based and builder-based)
        if self.unit_abilities or self._bound_abilities:
            from civ7_modding_tools.nodes import (
                UnitAbilityNode,
                UnitClassAbilityNode,
                UnitAbilityModifierNode,
                ChargedUnitAbilityNode,
            )
            
            ability_nodes = []
            unit_class_ability_nodes = []
            ability_modifier_nodes = []
            charged_ability_nodes = []
            activation_modifiers = []  # For auto-activating inactive abilities
            
            # Get unit class tag for linking abilities
            unit_class_tag = self.unit_type.replace('UNIT_', 'UNIT_CLASS_')
            
            # Process builder-based abilities
            for ability_builder in self._bound_abilities:
                # Migrate the ability builder
                ability_builder.migrate()
                
                ability_type = ability_builder.ability_type
                if not ability_type:
                    continue
                
                # Add Types
                if ability_builder._current.types:
                    if not self._current.types:
                        self._current.types = []
                    self._current.types.extend(ability_builder._current.types)
                
                # Collect UnitAbilities
                if ability_builder._current.unit_abilities:
                    ability_nodes.extend(ability_builder._current.unit_abilities)
                
                # Link ability to unit class
                unit_class_ability_nodes.append(UnitClassAbilityNode(
                    unit_ability_type=ability_type,
                    unit_class_type=unit_class_tag,
                ))
                
                # Collect UnitAbilityModifiers
                if ability_builder._current.unit_ability_modifiers:
                    ability_modifier_nodes.extend(ability_builder._current.unit_ability_modifiers)
                
                # Collect ChargedUnitAbilities
                if ability_builder._current.charged_unit_abilities:
                    charged_ability_nodes.extend(ability_builder._current.charged_unit_abilities)
                
                # Merge game effects
                if ability_builder._game_effects and hasattr(ability_builder._game_effects, 'modifiers'):
                    if not hasattr(self._current, '_game_effects') or not self._current._game_effects:
                        from civ7_modding_tools.nodes.nodes import GameEffectNode
                        self._current._game_effects = GameEffectNode()
                    if not hasattr(self._current._game_effects, 'modifiers'):
                        self._current._game_effects.modifiers = []
                    self._current._game_effects.modifiers.extend(ability_builder._game_effects.modifiers)
                
                # Merge localizations
                if ability_builder._localizations.english_text:
                    if not self._localizations.english_text:
                        self._localizations.english_text = []
                    self._localizations.english_text.extend(ability_builder._localizations.english_text)
                
                # Auto-activate inactive abilities
                if ability_builder.inactive:
                    activation_modifiers.append(self._create_ability_activation_modifier(ability_type))
            
            # Process dict-based abilities (simple format)
            for ability_config in self.unit_abilities:
                ability_id = ability_config.get('ability_id')
                ability_type = ability_config.get('ability_type')
                if not ability_id or not ability_type:
                    continue
                
                # Create ability node (using unique ability_id)
                ability_node = UnitAbilityNode(
                    unit_ability_type=ability_id,
                    name=ability_config.get('name', locale(ability_id, 'name')),
                    description=ability_config.get('description', locale(ability_id, 'description')),
                    inactive=ability_config.get('inactive', False) if ability_config.get('inactive') else None,
                )
                ability_nodes.append(ability_node)
                
                # Add Type (for unique ability ID)
                if not self._current.types:
                    self._current.types = []
                self._current.types.append(TypeNode(type_=ability_id, kind="KIND_ABILITY"))
                
                # Link to unit class
                unit_class_ability_nodes.append(UnitClassAbilityNode(
                    unit_ability_type=ability_id,
                    unit_class_type=unit_class_tag,
                ))
                
                # Link modifiers if provided
                if 'modifiers' in ability_config:
                    for modifier_id in ability_config['modifiers']:
                        ability_modifier_nodes.append(UnitAbilityModifierNode(
                            unit_ability_type=ability_id,
                            modifier_id=modifier_id,
                        ))
                
                # Charged ability config
                if 'charged_config' in ability_config:
                    charged_ability_nodes.append(ChargedUnitAbilityNode(
                        unit_ability_type=ability_id,
                        recharge_turns=ability_config['charged_config'].get('recharge_turns'),
                    ))
                
                # Auto-activate if inactive
                if ability_config.get('inactive'):
                    activation_modifiers.append(self._create_ability_activation_modifier(ability_id))
            
            # Store all ability-related nodes
            if ability_nodes:
                self._current.unit_abilities = ability_nodes
            if unit_class_ability_nodes:
                self._current.unit_class_abilities = unit_class_ability_nodes
            if ability_modifier_nodes:
                self._current.unit_ability_modifiers = ability_modifier_nodes
            if charged_ability_nodes:
                self._current.charged_unit_abilities = charged_ability_nodes
            
            # Add activation modifiers to game effects
            if activation_modifiers:
                if not hasattr(self._current, '_game_effects') or not self._current._game_effects:
                    from civ7_modding_tools.nodes.nodes import GameEffectNode
                    self._current._game_effects = GameEffectNode()
                if not hasattr(self._current._game_effects, 'modifiers'):
                    self._current._game_effects.modifiers = []
                self._current._game_effects.modifiers.extend(activation_modifiers)
        
        # Merge bound modifier builders (for unit ability modifiers)
        if self._bound_modifiers:
            if not hasattr(self._current, '_game_effects') or not self._current._game_effects:
                from civ7_modding_tools.nodes.nodes import GameEffectNode
                self._current._game_effects = GameEffectNode()
            if not hasattr(self._current._game_effects, 'modifiers'):
                self._current._game_effects.modifiers = []
            
            for modifier_builder in self._bound_modifiers:
                # Migrate the modifier builder
                modifier_builder.migrate()
                # Merge its game effects into the unit's game effects
                if modifier_builder._game_effects and hasattr(modifier_builder._game_effects, 'modifiers'):
                    self._current._game_effects.modifiers.extend(modifier_builder._game_effects.modifiers)
                # Merge localizations
                if modifier_builder._localizations and hasattr(modifier_builder._localizations, 'english_text'):
                    if not hasattr(self._localizations, 'english_text') or not self._localizations.english_text:
                        self._localizations.english_text = []
                    self._localizations.english_text.extend(modifier_builder._localizations.english_text)
        
        # Progression tree unlocks (tech/civic unlock requirements)
        unlock_node_type = None
        
        # Priority 1: Explicit unlock_civic (takes precedence)
        if self.unlock_civic:
            unlock_node_type = self.unlock_civic
        # Priority 2: Explicit unlock_tech
        elif self.unlock_tech:
            unlock_node_type = self.unlock_tech
        # Priority 3: Auto-infer from replaced unit
        elif self.auto_infer_unlock and self.unit_replace:
            unlock_node_type = self._get_unlock_from_replaces()
        
        # Generate unlock node if we have a node type
        if unlock_node_type:
            from civ7_modding_tools.nodes.database import ProgressionTreeNodeUnlockNode
            
            unlock_node = ProgressionTreeNodeUnlockNode(
                progression_tree_node_type=unlock_node_type,
                target_kind='KIND_UNIT',
                target_type=self.unit_type,
                unlock_depth=1
            )
            
            # Add required_trait_type if unit has trait_type
            # This ensures civ-specific units only unlock for that civ
            if self.civilization_type:
                unlock_node.required_trait_type = self.civilization_type.replace('CIVILIZATION_', 'TRAIT_')
            
            # Store in progression_tree_node_unlocks (create list if doesn't exist)
            if not hasattr(self._current, 'progression_tree_node_unlocks'):
                self._current.progression_tree_node_unlocks = []
            self._current.progression_tree_node_unlocks.append(unlock_node)
        
        # ==== POPULATE _icons DATABASE ====
        if self.icon:
            icon_node = IconDefinitionNode(id=self.unit_type)
            for key, value in self.icon.items():
                setattr(icon_node, key, value)
            self._icons.icon_definitions = [icon_node]
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc["name"]
                    ))
                
                # Build description with auto-appended ability descriptions
                description_text = loc.get("summary_description") or loc.get("description")
                if description_text:
                    # Collect ability descriptions from reference data
                    ability_descriptions = []
                    
                    # Collect from dict-based abilities
                    for ability_config in self.unit_abilities:
                        ability_type = ability_config.get('ability_type')
                        if ability_type:
                            # Try to get description_text from ability config, then description, then reference data
                            desc_text = ability_config.get('description_text')
                            if not desc_text:
                                # Try description field as fallback
                                desc_text = ability_config.get('description')
                            if not desc_text:
                                # Load from reference data
                                from civ7_modding_tools.data import get_unit_abilities
                                abilities_data = {a['id']: a for a in get_unit_abilities()}
                                if ability_type in abilities_data:
                                    desc_text = abilities_data[ability_type].get('description_text', '')
                            
                            if desc_text:  # Only append if we have actual text
                                ability_descriptions.append(desc_text)
                    
                    # Collect from builder-based abilities (custom abilities)
                    for ability_builder in self._bound_abilities:
                        # Look for description in ability_builder's localizations
                        for ability_loc in ability_builder.localizations:
                            desc_text = ability_loc.get('description')
                            if desc_text:
                                ability_descriptions.append(desc_text)
                                break  # Only use first description found
                    
                    # Append ability descriptions if any exist
                    if ability_descriptions:
                        combined_description = description_text + '\n' + '\n'.join(ability_descriptions)
                    else:
                        combined_description = description_text
                    
                    localization_rows.append(EnglishTextNode(
                        tag=loc_description,
                        text=combined_description
                    ))
                
                # Add historical context for Civilopedia
                if "historical_description" in loc:
                    # Extract unit type from loc_name (e.g., LOC_UNIT_DRUID_NAME -> DRUID)
                    unit_type_part = loc_name.replace("LOC_UNIT_", "").replace("_NAME", "")
                    pedia_tag = f"LOC_PEDIA_PAGE_UNIT_{unit_type_part}_CHAPTER_HISTORY_PARA_1"
                    localization_rows.append(EnglishTextNode(
                        tag=pedia_tag,
                        text=loc["historical_description"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        # ==== POPULATE _visual_remap DATABASE ====
        if self.visual_remap:
            from civ7_modding_tools.nodes import VisualRemapRowNode
            from civ7_modding_tools.utils import locale
            from civ7_modding_tools.data import get_units
            
            remap_to = self.visual_remap.get('to')
            
            # Validate that the base unit exists
            if remap_to:
                valid_units = {u['id'] for u in get_units()}
                if remap_to not in valid_units:
                    raise ValueError(
                        f"Invalid visual_remap base unit: {remap_to}. "
                        f"Must be a valid base game unit ID."
                    )
            
            remap_id = f"REMAP_{self.unit_type}"
            remap_row = VisualRemapRowNode()
            remap_row.id = remap_id
            remap_row.display_name = locale(self.unit_type, 'name')
            remap_row.kind = 'UNIT'
            remap_row.from_ = self.unit_type
            remap_row.to = remap_to
            
            self._visual_remap = DatabaseNode()
            self._visual_remap.visual_remaps = [remap_row]
        
        return self

    def _generate_type_tags(self) -> list:
        """
        Auto-generate TypeTag nodes based on unit properties.
        
        Maps unit properties to standard classification tags following
        data-EXAMPLE patterns (e.g., CORE_CLASS_COMBAT → UNIT_CLASS_COMBAT).
        
        Returns:
            List of TypeTagNode instances
        """
        from civ7_modding_tools.nodes import TypeTagNode
        
        tags = []
        
        # Get unit properties (either from self.unit dict or unit_node)
        core_class = self.unit.get('core_class')
        formation_class = self.unit.get('formation_class')
        unit_movement_class = self.unit.get('unit_movement_class')
        domain = self.unit.get('domain')
        tier = self.unit.get('tier')
        
        # Map CORE_CLASS_* to UNIT_CLASS_* tags
        if core_class == 'CORE_CLASS_COMBAT':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_COMBAT'))
        elif core_class == 'CORE_CLASS_CIVILIAN':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_NON_COMBAT'))
        elif core_class == 'CORE_CLASS_SUPPORT':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_NON_COMBAT'))
        
        # Map FORMATION_CLASS_* to specific combat tags
        if formation_class == 'FORMATION_CLASS_MELEE':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_MELEE'))
        elif formation_class == 'FORMATION_CLASS_RANGED':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_RANGED'))
        elif formation_class == 'FORMATION_CLASS_SIEGE':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_SIEGE'))
        elif formation_class == 'FORMATION_CLASS_RECON':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_RECON'))
        
        # Map UNIT_MOVEMENT_CLASS_* to unit type tags
        if unit_movement_class == 'UNIT_MOVEMENT_CLASS_MOUNTED':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_MOUNTED'))
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_CAVALRY'))
        elif unit_movement_class == 'UNIT_MOVEMENT_CLASS_FOOT':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_INFANTRY'))
        elif unit_movement_class == 'UNIT_MOVEMENT_CLASS_WHEELED':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_WHEELED'))
        
        # Domain tags
        if domain == 'DOMAIN_SEA':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_NAVAL'))
        elif domain == 'DOMAIN_AIR':
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_AIR'))
        
        # Tier-based elite tags (tier 3+ for infantry/cavalry)
        if tier and int(tier) >= 3:
            if 'UNIT_CLASS_INFANTRY' in [t.tag for t in tags]:
                tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_ELITE_INFANTRY'))
            if 'UNIT_CLASS_CAVALRY' in [t.tag for t in tags]:
                tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_ELITE_CAVALRY'))
        
        # Capability-based tags
        if self.unit.get('found_city'):
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_CREATE_TOWN'))
        if self.unit.get('make_trade_route'):
            tags.append(TypeTagNode(type_=self.unit_type, tag='UNIT_CLASS_MAKE_TRADE_ROUTE'))
        
        return tags

    def _get_unlock_from_replaces(self) -> Optional[str]:
        """
        Auto-detect unlock node from replaced unit.
        
        Looks up the replaced unit in units.json reference data
        and returns the first unlock node.
        
        Returns:
            Progression tree node ID (e.g., 'NODE_TECH_AQ_WHEEL') or None
        """
        if not self.unit_replace:
            return None
        
        replaces_unit_type = self.unit_replace.get('replaces_unit_type') or \
                            self.unit_replace.get('replacesUnitType')
        
        if not replaces_unit_type:
            return None
        
        try:
            from civ7_modding_tools.data import get_units
            units_data = get_units()
            
            # Find the replaced unit
            for unit in units_data:
                if unit['id'] == replaces_unit_type:
                    unlocked_by = unit.get('unlocked_by', [])
                    if unlocked_by:
                        return unlocked_by[0]  # Return first unlock node
                    break
        except Exception:
            # If data loading fails, return None
            pass
        
        return None

    def _create_ability_activation_modifier(self, ability_type: str) -> 'ModifierNode':
        """
        Create a modifier to auto-activate an inactive ability.
        
        Uses EFFECT_GRANT_ABILITY_CHARGE to grant the ability to units on creation.
        
        Args:
            ability_type: The ability type to activate
            
        Returns:
            ModifierNode for activating the ability
        """
        from civ7_modding_tools.nodes.nodes import ModifierNode
        
        modifier_id = f"{ability_type}_AUTO_ACTIVATION"
        
        modifier = ModifierNode()
        modifier.id = modifier_id
        modifier.collection = "COLLECTION_OWNER"
        modifier.effect = "EFFECT_GRANT_ABILITY_CHARGE"
        modifier.permanent = True
        modifier.run_once = False
        modifier.arguments = [
            {"name": "AbilityType", "value": ability_type},
            {"name": "Amount", "value": "1"},
        ]
        
        return modifier

    def bind(self, items: List['UnitAbilityBuilder']) -> "UnitBuilder":
        """
        Bind UnitAbilityBuilder items to this unit.
        
        Enables fluent API pattern:
            ability = UnitAbilityBuilder().fill({...})
            unit.bind([ability])
        
        Args:
            items: List of UnitAbilityBuilder instances
            
        Returns:
            Self for fluent API chaining
        """
        for item in items:
            if not isinstance(item, UnitAbilityBuilder):
                raise TypeError(f"Can only bind UnitAbilityBuilder to UnitBuilder, got {type(item)}")
            self._bound_abilities.append(item)
        return self

    def build(self) -> list[BaseFile]:
        """Build unit files with multiple variants."""
        if not self.unit_type:
            return []
        
        self.migrate()
        
        # Generate path from base_unit_type if set (for upgrade chains), otherwise unit_type
        from civ7_modding_tools.utils import trim, kebab_case
        path_unit_type = self.base_unit_type if self.base_unit_type else self.unit_type
        trimmed = trim(path_unit_type)
        path = f"/units/{kebab_case(trimmed)}/"
        
        files: list[BaseFile] = [
            XmlFile(
                path=path,
                name="current.xml",
                content=self._current,
                action_group=self.action_group_bundle.current
            ),
            XmlFile(
                path=path,
                name="icons.xml",
                content=self._icons,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.current]
            ),
            XmlFile(
                path=path,
                name="localization.xml",
                content=self._localizations,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
        ]

        # Add game-effects if present (for unit ability modifiers)
        if hasattr(self._current, '_game_effects') and self._current._game_effects:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=self._current._game_effects,
                action_group=self.action_group_bundle.current
            ))

        # Add visual-remap if present
        if self._visual_remap:
            files.append(XmlFile(
                path=path,
                name="visual-remap.xml",
                content=self._visual_remap,
                action_group=self.action_group_bundle.current
            ))
        
        # Filter out empty files
        files = [f for f in files if f.content is not None]
        
        return files


class ConstructibleBuilder(BaseBuilder):
    """Builder for creating buildings and improvements with multiple file generation."""
    
    def __init__(self) -> None:
        """Initialize constructible builder with database variants."""
        super().__init__()
        self._always = DatabaseNode()
        self._icons = DatabaseNode()
        self._localizations = DatabaseNode()
        self._game_effects: Optional['GameEffectNode'] = None
        self._visual_remap: Optional[DatabaseNode] = None
        
        self.constructible_type: Optional[str] = None
        self.is_building: bool = True  # Default to building
        self.constructible: Dict[str, Any] = {}
        self.building: Optional[Dict[str, Any]] = None
        self.improvement: Optional[Dict[str, Any]] = None
        self.building_attributes: Dict[str, Any] = {}
        
        # Top-level constructible attributes (can also be in constructible dict)
        self.age: Optional[str] = None
        self.cost: Optional[int] = None
        self.population: Optional[int] = None
        self.repairable: Optional[bool] = None
        self.adjacent_river: Optional[bool] = None
        self.adjacent_terrain: Optional[str] = None
        self.adjacent_district: Optional[str] = None
        
        # Cost structure from wizard (will be converted to cost in migrate)
        self.constructible_cost: Optional[Dict[str, Any]] = None
        
        # Visual remapping (same format as units: {to: base_constructible_id})
        self.visual_remap: Optional[Dict[str, Any]] = None
        
        self.type_tags: list[str] = []
        self.constructible_valid_districts: list[str] = []
        self.constructible_valid_terrains: list[str] = []
        self.constructible_valid_biomes: list[str] = []
        self.constructible_valid_features: list[str] = []
        self.constructible_maintenances: list[Dict[str, Any]] = []
        self.yield_changes: list[Dict[str, Any]] = []
        self.adjacencies: list[Dict[str, Any]] = []
        self.plunders: list[Dict[str, Any]] = []
        self.cost_progressions: list[Dict[str, Any]] = []
        self.advisories: list[Dict[str, Any]] = []
        self.adjacency_bonuses: list[Dict[str, Any]] = []  # Phase 5: Custom adjacency bonuses
        self.building_suite: Optional[Dict[str, Any]] = None  # Phase 5: Multi-tile buildings
        self.localizations: list[Dict[str, Any]] = []
        self.modifiers: list[Dict[str, Any]] = []
        self.icon: Dict[str, Any] = {'path': 'fs://game/civ_sym_han'}

    def fill(self, payload: Dict[str, Any]) -> "ConstructibleBuilder":
        """Fill constructible builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def _generate_unit_healing_modifier(self, amount: int) -> None:
        """
        Generate unit healing modifier for improvements following the Pairidaeza pattern.
        
        Creates two modifiers:
        1. Parent modifier attached to cities that have this improvement
        2. Child modifier that adjusts heal per turn for units in friendly territory
        
        Args:
            amount: Healing amount per turn
        """
        from civ7_modding_tools.nodes.nodes import ModifierNode, GameEffectNode
        from civ7_modding_tools.nodes.database import ConstructibleModifierNode
        
        # Generate modifier IDs
        parent_modifier_id = f"MOD_{self.constructible_type}_SETTLEMENT_HEAL"
        child_modifier_id = f"ATTACH_MOD_{self.constructible_type}_SETTLEMENT_HEAL"
        
        # Initialize game_effects as GameEffectNode if needed
        if self._game_effects is None:
            self._game_effects = GameEffectNode()
        
        # Ensure modifiers list exists
        if not hasattr(self._game_effects, 'modifiers'):
            self._game_effects.modifiers = []
        
        # Check if modifier already exists to prevent duplicates
        existing_ids = [m.id for m in self._game_effects.modifiers]
        if parent_modifier_id in existing_ids:
            return  # Already generated, skip
        
        # Parent modifier: Attached to cities that have this improvement
        parent_modifier = ModifierNode(
            id=parent_modifier_id,
            collection="COLLECTION_PLAYER_CITIES",
            effect="EFFECT_ATTACH_MODIFIERS",
            requirements=[
                {
                    'type': 'REQUIREMENT_CITY_HAS_BUILDING',
                    'arguments': [
                        {'name': 'BuildingType', 'value': self.constructible_type}
                    ]
                }
            ],
            arguments=[
                {'name': 'ModifierId', 'value': child_modifier_id}
            ]
        )
        
        # Child modifier: Heals units in friendly territory
        child_modifier = ModifierNode(
            id=child_modifier_id,
            collection="COLLECTION_PLAYER_UNITS",
            effect="EFFECT_UNIT_ADJUST_HEAL_PER_TURN",
            arguments=[
                {'name': 'Amount', 'value': str(amount)},
                {'name': 'TerritoryTypes', 'value': 'FRIENDLY_TERRITORY'}
            ]
        )
        
        # Add modifiers to GameEffectNode
        self._game_effects.modifiers.extend([parent_modifier, child_modifier])
        
        # Also add to constructible_modifiers table to link improvement to modifier
        constructible_modifier = ConstructibleModifierNode(
            constructible_type=self.constructible_type,
            modifier_id=parent_modifier_id
        )
        
        if not hasattr(self._always, 'constructible_modifiers'):
            self._always.constructible_modifiers = []
        
        # Check for duplicate in constructible_modifiers too
        existing_constructible_modifiers = [
            (cm.constructible_type, cm.modifier_id) 
            for cm in self._always.constructible_modifiers
        ]
        if (self.constructible_type, parent_modifier_id) not in existing_constructible_modifiers:
            self._always.constructible_modifiers.append(constructible_modifier)

    def migrate(self) -> "ConstructibleBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        
        if not self.constructible_type:
            return self
        
        # Auto-detect building vs improvement from type
        if not self.building and not self.improvement:
            if self.constructible_type.startswith('BUILDING_'):
                self.building = {}
            elif self.constructible_type.startswith('IMPROVEMENT_'):
                self.improvement = {}
        
        # Handle constructible_cost structure (from wizard)
        # Convert {yield_type: "YIELD_PRODUCTION", cost: 30} to just cost: 30
        if hasattr(self, 'constructible_cost') and self.constructible_cost:
            if isinstance(self.constructible_cost, dict):
                cost_value = self.constructible_cost.get('cost')
                if cost_value is not None and 'cost' not in self.constructible:
                    self.constructible['cost'] = cost_value
        
        # Migrate top-level fields to constructible dict for convenience
        # Fields like 'age', 'repairable', 'cost', etc. can be at top level in YAML
        top_level_constructible_fields = ['age', 'cost', 'population', 'repairable', 
                                           'adjacent_river', 'adjacent_terrain', 'adjacent_district']
        for field in top_level_constructible_fields:
            if hasattr(self, field):
                value = getattr(self, field, None)
                if value is not None and field not in self.constructible:
                    self.constructible[field] = value
        
        # Generate localization keys
        loc_name = locale(self.constructible_type, 'name')
        loc_description = locale(self.constructible_type, 'description')
        loc_tooltip = locale(self.constructible_type, 'tooltip')
        
        # ==== POPULATE _always DATABASE ====
        # Types
        self._always.types = [
            TypeNode(type_=self.constructible_type, kind="KIND_CONSTRUCTIBLE"),
        ]
        
        # TypeTags
        type_tags = list(self.type_tags) if self.type_tags else []
        
        # Handle AGELESS: It's a TAG, not an Age. Convert age='AGELESS' to tag
        if self.constructible.get('age') == 'AGELESS':
            if 'AGELESS' not in type_tags:
                type_tags.append('AGELESS')
            # Remove age field - AGELESS is not a valid age value
            self.constructible.pop('age', None)
        
        # Auto-add UNIQUE_IMPROVEMENT tag for improvements with trait_type
        if not self.is_building:
            # Check if trait_type is set in improvement dict
            has_trait = self.improvement and self.improvement.get('trait_type')
            if has_trait and 'UNIQUE_IMPROVEMENT' not in type_tags:
                type_tags.append('UNIQUE_IMPROVEMENT')
        
        if type_tags:
            self._always.type_tags = [
                TypeTagNode(type_=self.constructible_type, tag=tag)
                for tag in type_tags
            ]
        
        # Building (if this is a building)
        if self.building is not None:
            # Preserve existing trait_type if already set (by parent civilization)
            existing_trait_type = None
            if self._always.buildings:
                existing_trait_type = self._always.buildings[0].trait_type
            
            building_node = BuildingNode(constructible_type=self.constructible_type)
            # Set movable to False by default for all buildings
            building_node.movable = False
            
            if existing_trait_type is not None:
                building_node.trait_type = existing_trait_type
            
            # Apply custom building attributes (can override defaults)
            for key, value in self.building_attributes.items():
                setattr(building_node, key, value)
            
            for key, value in self.building.items():
                setattr(building_node, key, value)
            self._always.buildings = [building_node]
        
        # Improvement (if this is an improvement)
        if self.improvement is not None:
            # Preserve existing trait_type if already set (by parent civilization)
            existing_trait_type = None
            if self._always.improvements:
                existing_trait_type = self._always.improvements[0].trait_type
            
            # Auto-correct trait_type if needed
            if 'trait_type' in self.improvement:
                trait = self.improvement['trait_type']
                # Fix common incorrect patterns: TRAIT_CULTURAL -> TRAIT_ATTRIBUTE_CULTURAL
                if trait and trait.startswith('TRAIT_') and not trait.startswith('TRAIT_ATTRIBUTE_'):
                    # Check if it's a simple attribute name that needs ATTRIBUTE prefix
                    simple_attrs = ['CULTURAL', 'ECONOMIC', 'SCIENTIFIC', 'MILITARISTIC', 'POLITICAL', 'EXPANSIONIST']
                    trait_suffix = trait.replace('TRAIT_', '')
                    if trait_suffix in simple_attrs:
                        self.improvement['trait_type'] = f'TRAIT_ATTRIBUTE_{trait_suffix}'
            
            improvement_node = ImprovementNode(constructible_type=self.constructible_type)
            if existing_trait_type is not None:
                improvement_node.trait_type = existing_trait_type
            
            # Set sensible defaults for improvements
            if 'resource_tier' not in self.improvement:
                improvement_node.resource_tier = 0
            if 'city_buildable' not in self.improvement:
                improvement_node.city_buildable = True
            
            # Extract unit_healing for modifier generation (removed from improvement dict)
            unit_healing_value = None
            improvement_data = dict(self.improvement)  # Create copy
            if 'unit_healing' in improvement_data:
                unit_healing_value = improvement_data.pop('unit_healing')
            
            for key, value in improvement_data.items():
                setattr(improvement_node, key, value)
            self._always.improvements = [improvement_node]
            
            # Generate unit healing modifier if specified
            if unit_healing_value is not None:
                self._generate_unit_healing_modifier(unit_healing_value)
        
        # Constructible definition with localization
        const_node = ConstructibleNode(
            constructible_type=self.constructible_type,
            name=loc_name,
            description=loc_description,
            tooltip=loc_tooltip,
        )
        # Set constructible_class based on is_building flag
        if not self.is_building:
            const_node.constructible_class = "IMPROVEMENT"
        
        for key, value in self.constructible.items():
            setattr(const_node, key, value)
        self._always.constructibles = [const_node]
        
        # Valid districts
        # Auto-add DISTRICT_RURAL for improvements if not specified
        valid_districts = self.constructible_valid_districts
        if not valid_districts and not self.is_building:
            valid_districts = ['DISTRICT_RURAL']
        
        if valid_districts:
            self._always.constructible_valid_districts = [
                ConstructibleValidDistrictNode(
                    constructible_type=self.constructible_type,
                    district_type=district
                )
                for district in valid_districts
            ]
        
        # Valid terrains
        if self.constructible_valid_terrains:
            self._always.constructible_valid_terrains = [
                ConstructibleValidTerrainNode(
                    constructible_type=self.constructible_type,
                    terrain_type=terrain
                )
                for terrain in self.constructible_valid_terrains
            ]
        
        # Valid biomes
        if self.constructible_valid_biomes:
            self._always.constructible_valid_biomes = [
                ConstructibleValidBiomeNode(
                    constructible_type=self.constructible_type,
                    biome_type=biome
                )
                for biome in self.constructible_valid_biomes
            ]
        
        # Valid features
        if self.constructible_valid_features:
            self._always.constructible_valid_features = [
                ConstructibleValidFeatureNode(
                    constructible_type=self.constructible_type,
                    feature_type=feature
                )
                for feature in self.constructible_valid_features
            ]
        
        # Maintenances
        if self.constructible_maintenances:
            self._always.constructible_maintenances = [
                ConstructibleMaintenanceNode(
                    constructible_type=self.constructible_type,
                    yield_type=maint.get('yield_type'),
                    amount=maint.get('amount')
                )
                for maint in self.constructible_maintenances
            ]
        
        # Yield changes
        if self.yield_changes:
            self._always.constructible_yield_changes = [
                ConstructibleYieldChangeNode(
                    constructible_type=self.constructible_type,
                    yield_type=yc.get('yield_type'),
                    yield_change=yc.get('yield_change')
                )
                for yc in self.yield_changes
            ]
        
        # Advisories
        if self.advisories:
            self._always.constructible_advisories = [
                ConstructibleAdvisoryNode(
                    constructible_type=self.constructible_type,
                    advisory_class_type=adv if isinstance(adv, str) else adv.get('advisory_class_type')
                )
                for adv in self.advisories
            ]
        
        # Adjacencies with custom yield changes
        if self.adjacencies:
            adjacency_refs = []
            adjacency_defs = []
            
            for adj in self.adjacencies:
                # Get the adjacency pattern ID or custom definition
                pattern_id = adj.get('pattern_id') or adj.get('yield_change_id')
                
                if pattern_id:
                    # Reference existing adjacency pattern
                    adj_ref = ConstructibleAdjacencyNode(
                        constructible_type=self.constructible_type,
                        yield_change_id=pattern_id,
                        requires_activation=adj.get('requires_activation')
                    )
                    adjacency_refs.append(adj_ref)
                
                # If custom adjacency definition provided, create the yield change node
                if adj.get('custom'):
                    custom_id = adj.get('id') or f"{self.constructible_type}_Custom_{len(adjacency_defs)}"
                    
                    adj_def = AdjacencyYieldChangeNode(
                        id=custom_id,
                        yield_type=adj.get('yield_type'),
                        yield_change=adj.get('yield_change'),
                        tiles_required=adj.get('tiles_required', 1),
                        project_max_yield=adj.get('project_max_yield'),
                        adjacent_terrain=adj.get('adjacent_terrain'),
                        adjacent_biome=adj.get('adjacent_biome'),
                        adjacent_district=adj.get('adjacent_district'),
                        adjacent_quarter=adj.get('adjacent_quarter'),
                        adjacent_resource=adj.get('adjacent_resource'),
                        adjacent_river=adj.get('adjacent_river'),
                        adjacent_constructible=adj.get('adjacent_constructible'),
                        adjacent_constructible_tag=adj.get('adjacent_constructible_tag')
                    )
                    adjacency_defs.append(adj_def)
                    
                    # Also add reference to this custom adjacency
                    adj_ref = ConstructibleAdjacencyNode(
                        constructible_type=self.constructible_type,
                        yield_change_id=custom_id,
                        requires_activation=adj.get('requires_activation')
                    )
                    adjacency_refs.append(adj_ref)
            
            if adjacency_refs:
                self._always.constructible_adjacencies = adjacency_refs
            if adjacency_defs:
                self._always.adjacency_yield_changes = adjacency_defs
        
        # Plunders
        if self.plunders:
            self._always.constructible_plunders = [
                ConstructiblePlunderNode(
                    constructible_type=self.constructible_type,
                    plunder_type=plunder.get('plunder_type'),
                    amount=plunder.get('amount')
                )
                for plunder in self.plunders
            ]
        
        # Cost progressions
        if self.cost_progressions:
            self._always.constructible_building_cost_progressions = [
                ConstructibleBuildingCostProgressionNode(
                    constructible_type=self.constructible_type,
                    percent=prog.get('percent')
                )
                for prog in self.cost_progressions
            ]
        
        # ==== POPULATE _icons DATABASE ====
        icon_node = IconDefinitionNode(id=self.constructible_type)
        if self.icon:
            for key, value in self.icon.items():
                setattr(icon_node, key, value)
        self._icons.icon_definitions = [icon_node]
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc["name"]
                    ))
                if "description" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_description,
                        text=loc["description"]
                    ))
                if "tooltip" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_tooltip,
                        text=loc["tooltip"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        # ==== POPULATE _visual_remap DATABASE ====
        if self.visual_remap:
            from civ7_modding_tools.nodes import VisualRemapRowNode
            from civ7_modding_tools.utils import locale
            from civ7_modding_tools.data import get_constructibles
            
            remap_to = self.visual_remap.get('to') if isinstance(self.visual_remap, dict) else self.visual_remap
            
            # Validate that the base constructible exists
            if remap_to:
                valid_constructibles = set(c['id'] for c in get_constructibles())
                if remap_to not in valid_constructibles:
                    raise ValueError(
                        f"Invalid visual_remap base constructible: {remap_to}. "
                        f"Must be a valid base game constructible ID."
                    )
            
            remap_id = f"REMAP_{self.constructible_type}"
            remap_row = VisualRemapRowNode()
            remap_row.id = remap_id
            remap_row.display_name = locale(self.constructible_type, 'name')
            remap_row.kind = 'BUILDING' if self.is_building else 'IMPROVEMENT'
            remap_row.from_ = self.constructible_type
            remap_row.to = remap_to
            
            self._visual_remap = DatabaseNode()
            self._visual_remap.visual_remaps = [remap_row]
        
        # ==== POPULATE _game_effects DATABASE ====
        if self.modifiers:
            self._game_effects = DatabaseNode()
            # Note: Full modifier integration would be here
        
        return self

    def build(self) -> list[BaseFile]:
        """Build constructible files with multiple variants."""
        if not self.constructible_type:
            return []
        
        self.migrate()
        
        # Generate path from constructible type (trimmed + kebab-case)
        from civ7_modding_tools.utils import trim, kebab_case
        trimmed = trim(self.constructible_type)
        path = f"/constructibles/{kebab_case(trimmed)}/"
        
        files: list[BaseFile] = [
            XmlFile(
                path=path,
                name="current.xml",
                content=self._always,
                action_group=self.action_group_bundle.current
            ),
            XmlFile(
                path=path,
                name="icons.xml",
                content=self._icons,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
            XmlFile(
                path=path,
                name="localization.xml",
                content=self._localizations,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
        ]
        
        # Add game-effects if present
        if self._game_effects:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=self._game_effects,
                action_group=self.action_group_bundle.current
            ))
        
        # Add visual-remap if present (but skip for improvements - they use JS instead)
        if self._visual_remap and self.is_building:
            files.append(XmlFile(
                path=path,
                name="visual-remap.xml",
                content=self._visual_remap,
                action_group=self.action_group_bundle.current
            ))
        
        # Filter out empty files
        files = [f for f in files if f.content is not None]
        
        return files


class ProgressionTreeBuilder(BaseBuilder):
    """Builder for creating progression trees (tech/civic trees)."""
    
    def __init__(self) -> None:
        """Initialize progression tree builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._game_effects: Optional['GameEffectNode'] = None
        self._localizations = DatabaseNode()
        
        self.progression_tree_type: Optional[str] = None
        self.progression_tree: Dict[str, Any] = {}
        self.progression_tree_nodes: list[Dict[str, Any]] = []
        self.progression_tree_prereqs: List[Dict[str, Any]] = []
        self.progression_tree_quotes: list[Dict[str, Any]] = []
        self.localizations: List[Dict[str, Any]] = []

    def fill(self, payload: Dict[str, Any]) -> "ProgressionTreeBuilder":
        """Fill progression tree builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "ProgressionTreeBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import (
            ProgressionTreeNode,
            ProgressionTreePrereqNode,
        )
        
        if not self.progression_tree_type:
            return self
        
        # Generate localization keys
        loc_name = locale(self.progression_tree_type, 'name')
        
        # ==== POPULATE _current DATABASE ====
        # Types
        tree_type_node = TypeNode(type_=self.progression_tree_type, kind="KIND_TREE")
        if self._current.types:
            self._current.types.append(tree_type_node)
        else:
            self._current.types = [tree_type_node]
        
        # Progression tree definition with localization
        tree_node = ProgressionTreeNode(
            progression_tree_type=self.progression_tree_type,
            name=loc_name,
        )
        for key, value in self.progression_tree.items():
            setattr(tree_node, key, value)
        self._current.progression_trees = [tree_node]
        
        # Prerequisites
        if self.progression_tree_prereqs:
            self._current.progression_tree_prereqs = [
                ProgressionTreePrereqNode(
                    node=prereq.get('node'),
                    prereq_node=prereq.get('prereq_node')
                )
                for prereq in self.progression_tree_prereqs
            ]
        
        # Progression tree quotes
        if self.progression_tree_quotes:
            self._current.progression_tree_quotes = [
                ProgressionTreeQuoteNode(
                    progression_tree_type=self.progression_tree_type,
                    quote_type=quote.get('quote_type'),
                    text=quote.get('text')
                )
                for quote in self.progression_tree_quotes
            ]
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc["name"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self

    def bind(self, items: List["ProgressionTreeNodeBuilder"]) -> "ProgressionTreeBuilder":
        """Bind ProgressionTreeNodeBuilder items to this tree.
        
        This merges all nodes from the child node builders into this tree.
        """
        for item in items:
            if hasattr(item, 'migrate'):
                item.migrate()
            # Fill progression tree reference on all nodes
            if hasattr(item, '_current') and item._current:
                for node in getattr(item._current, 'progression_tree_nodes', []):
                    node.progression_tree = self.progression_tree_type
                
                # Merge types
                if item._current.types:
                    self._current.types = self._current.types + item._current.types
                
                # Merge progression_tree_nodes
                if item._current.progression_tree_nodes:
                    if not self._current.progression_tree_nodes:
                        self._current.progression_tree_nodes = []
                    self._current.progression_tree_nodes = self._current.progression_tree_nodes + item._current.progression_tree_nodes
                
                # Merge progression_tree_advisories
                if item._current.progression_tree_advisories:
                    if not self._current.progression_tree_advisories:
                        self._current.progression_tree_advisories = []
                    self._current.progression_tree_advisories = self._current.progression_tree_advisories + item._current.progression_tree_advisories
                
                # Merge progression_tree_node_unlocks
                if item._current.progression_tree_node_unlocks:
                    if not self._current.progression_tree_node_unlocks:
                        self._current.progression_tree_node_unlocks = []
                    self._current.progression_tree_node_unlocks = self._current.progression_tree_node_unlocks + item._current.progression_tree_node_unlocks
                
                # Merge progression_tree_prereqs
                if item._current.progression_tree_prereqs:
                    if not self._current.progression_tree_prereqs:
                        self._current.progression_tree_prereqs = []
                    self._current.progression_tree_prereqs = self._current.progression_tree_prereqs + item._current.progression_tree_prereqs
            
            # Merge game_effects modifiers
            if hasattr(item, '_game_effects') and item._game_effects:
                if hasattr(item._game_effects, 'modifiers') and item._game_effects.modifiers:
                    if not self._game_effects:
                        from civ7_modding_tools.nodes import GameEffectNode
                        self._game_effects = GameEffectNode()
                        self._game_effects.modifiers = []
                    self._game_effects.modifiers.extend(item._game_effects.modifiers)
            
            # Merge localizations
            if hasattr(item, '_localizations') and item._localizations:
                if item._localizations.english_text:
                    if not self._localizations.english_text:
                        self._localizations.english_text = []
                    self._localizations.english_text = self._localizations.english_text + item._localizations.english_text
        
        return self

    def build(self) -> list[BaseFile]:
        """Build progression tree files."""
        from civ7_modding_tools.utils import trim, kebab_case
        
        files: list[BaseFile] = []
        
        if not self.progression_tree_type:
            return files
        
        self.migrate()
        
        # Generate path (trimmed + kebab-case)
        trimmed = trim(self.progression_tree_type)
        path = f"/progression-trees/{kebab_case(trimmed)}/"
        
        # Create current.xml file
        files.append(XmlFile(
            path=path,
            name="current.xml",
            content=self._current,
            action_group=self.action_group_bundle.current
        ))
        
        # Create game-effects.xml if there are modifiers
        if self._game_effects and hasattr(self._game_effects, 'modifiers') and self._game_effects.modifiers:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=self._game_effects,
                action_group=self.action_group_bundle.current
            ))
        
        # Create localization.xml
        files.append(XmlFile(
            path=path,
            name="localization.xml",
            content=self._localizations,
            action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
        ))
        
        # Filter out empty files
        files = [f for f in files if f.content is not None]
        
        return files


class ProgressionTreeNodeBuilder(BaseBuilder):
    """Builder for creating progression tree nodes (tech/civic nodes)."""
    
    def __init__(self) -> None:
        """Initialize progression tree node builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._game_effects: Optional['GameEffectNode'] = None
        self._localizations = DatabaseNode()
        
        self.progression_tree_node_type: Optional[str] = None
        self.progression_tree_node: Dict[str, Any] = {}
        self.progression_tree_advisories: List[str] = []
        self.localizations: List[Dict[str, Any]] = []

    def fill(self, payload: Dict[str, Any]) -> "ProgressionTreeNodeBuilder":
        """Fill progression tree node builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "ProgressionTreeNodeBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import (
            ProgressionTreeNodeNode,
        )
        
        if not self.progression_tree_node_type:
            return self
        
        # Generate localization keys
        loc_name = locale(self.progression_tree_node_type, 'name')
        
        # ==== POPULATE _current DATABASE ====
        # Types
        self._current.types = [
            TypeNode(type_=self.progression_tree_node_type, kind="KIND_TREE_NODE"),
        ]
        
        # Progression tree node definition with localization
        node = ProgressionTreeNodeNode(
            progression_tree_node_type=self.progression_tree_node_type,
            name=loc_name,
        )
        for key, value in self.progression_tree_node.items():
            setattr(node, key, value)
        self._current.progression_tree_nodes = [node]
        
        # Advisories
        if self.progression_tree_advisories:
            self._current.progression_tree_advisories = [
                ProgressionTreeAdvisoryNode(
                    progression_tree_node_type=self.progression_tree_node_type,
                    advisory_class_type=advisory
                )
                for advisory in self.progression_tree_advisories
            ]
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc["name"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self

    def bind(self, items: List[BaseBuilder], unlock_depth: int = 1, hidden: Optional[bool] = None) -> "ProgressionTreeNodeBuilder":
        """Bind builders to this node, creating unlock entries.
        
        Args:
            items: List of ModifierBuilder, ConstructibleBuilder, UnitBuilder, or TraditionBuilder
            unlock_depth: Depth of unlock (default 1)
            hidden: Whether unlock is hidden (optional)
        """
        for item in items:
            # Check for ModifierBuilder (has 'modifier' dict attribute)
            if hasattr(item, 'modifier') and hasattr(item, '_game_effects'):
                item.migrate()  # Ensure migration is done
                if item._game_effects and hasattr(item._game_effects, 'modifiers'):
                    # Initialize game effects if needed
                    if not self._game_effects:
                        from civ7_modding_tools.nodes import GameEffectNode
                        self._game_effects = GameEffectNode()
                        self._game_effects.modifiers = []
                    
                    # Add modifiers directly to game effects
                    self._game_effects.modifiers.extend(item._game_effects.modifiers)
                    
                    # Add unlocks for each modifier
                    for modifier in item._game_effects.modifiers:
                        if not self._current.progression_tree_node_unlocks:
                            self._current.progression_tree_node_unlocks = []
                        self._current.progression_tree_node_unlocks.append(
                            ProgressionTreeNodeUnlockNode(
                                progression_tree_node_type=self.progression_tree_node_type,
                                target_kind="KIND_MODIFIER",
                                target_type=modifier.id,
                                unlock_depth=unlock_depth,
                                hidden=hidden
                            )
                        )
                
                # Merge localizations
                if hasattr(item, '_localizations') and item._localizations:
                    if item._localizations.english_text:
                        if not self._localizations.english_text:
                            self._localizations.english_text = []
                        self._localizations.english_text.extend(item._localizations.english_text)
            
            # Check for ConstructibleBuilder
            elif hasattr(item, 'constructible_type') and item.constructible_type:
                if hasattr(item, 'migrate'):
                    item.migrate()
                if hasattr(item, '_always') and item._always:
                    for constructible in getattr(item._always, 'constructibles', []):
                        const_type = getattr(constructible, 'constructible_type', None)
                        if const_type:
                            if not self._current.progression_tree_node_unlocks:
                                self._current.progression_tree_node_unlocks = []
                            self._current.progression_tree_node_unlocks.append(
                                ProgressionTreeNodeUnlockNode(
                                    progression_tree_node_type=self.progression_tree_node_type,
                                    target_kind="KIND_CONSTRUCTIBLE",
                                    target_type=const_type,
                                    unlock_depth=unlock_depth,
                                    hidden=hidden
                                )
                            )
            
            # Check for UnitBuilder
            elif hasattr(item, 'unit_type') and item.unit_type:
                if hasattr(item, 'migrate'):
                    item.migrate()
                if hasattr(item, '_current') and item._current:
                    for unit in getattr(item._current, 'units', []):
                        unit_type = getattr(unit, 'unit_type', None)
                        if unit_type:
                            if not self._current.progression_tree_node_unlocks:
                                self._current.progression_tree_node_unlocks = []
                            self._current.progression_tree_node_unlocks.append(
                                ProgressionTreeNodeUnlockNode(
                                    progression_tree_node_type=self.progression_tree_node_type,
                                    target_kind="KIND_UNIT",
                                    target_type=unit_type,
                                    unlock_depth=unlock_depth,
                                    hidden=hidden
                                )
                            )
            
            # Check for TraditionBuilder
            elif hasattr(item, 'tradition_type') and item.tradition_type:
                if hasattr(item, '_current') and item._current:
                    for tradition in getattr(item._current, 'traditions', []):
                        trad_type = getattr(tradition, 'tradition_type', None)
                        if trad_type:
                            if not self._current.progression_tree_node_unlocks:
                                self._current.progression_tree_node_unlocks = []
                            self._current.progression_tree_node_unlocks.append(
                                ProgressionTreeNodeUnlockNode(
                                    progression_tree_node_type=self.progression_tree_node_type,
                                    target_kind="KIND_TRADITION",
                                    target_type=trad_type,
                                    unlock_depth=unlock_depth,
                                    hidden=hidden
                                )
                            )
        
        return self

    def build(self) -> list[BaseFile]:
        """Build progression tree node files.
        
        Note: ProgressionTreeNodeBuilder doesn't generate files directly.
        Instead, it's meant to be bound to a ProgressionTreeBuilder which
        generates the combined output.
        """
        return []


class ModifierBuilder(BaseBuilder):
    """Builder for creating game modifiers and effects."""
    
    def __init__(self) -> None:
        """Initialize modifier builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._game_effects: Optional['GameEffectNode'] = None
        self._localizations = DatabaseNode()
        
        self.modifier_type: Optional[str] = None
        self.modifier: Dict[str, Any] = {}
        self.modifier_strings: list[Dict[str, Any]] = []
        self.localizations: List[Dict[str, Any]] = []
        self.requirements: list[Dict[str, Any]] = []
        self.is_detached: bool = False  # Detached modifiers not bound to specific entity

    def fill(self, payload: Dict[str, Any]) -> "ModifierBuilder":
        """Fill modifier builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "ModifierBuilder":
        """Migrate and populate all database variants."""
        import uuid
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import GameEffectNode, EnglishTextNode
        from civ7_modding_tools.nodes.nodes import ModifierNode
        
        # Use modifier_type if available, otherwise generate from modifier dict
        modifier_type_or_id = self.modifier_type or self.modifier.get('modifier_type')
        
        # Generate unique modifier ID if not provided
        if not modifier_type_or_id:
            if 'id' not in self.modifier and 'modifier_id' not in self.modifier:
                self.modifier['id'] = 'MOD_' + uuid.uuid4().hex.upper()
            elif 'modifier_id' in self.modifier:
                self.modifier['id'] = self.modifier.pop('modifier_id')
            modifier_type_or_id = self.modifier['id']
        else:
            self.modifier['modifier_type'] = modifier_type_or_id
        
        # Create modifier node with full structure
        modifier_node = ModifierNode()
        modifier_node.id = self.modifier.get('id')
        modifier_node.collection = self.modifier.get('collection')
        modifier_node.effect = self.modifier.get('effect')
        modifier_node.permanent = self.modifier.get('permanent')
        modifier_node.run_once = self.modifier.get('run_once')
        modifier_node.requirements = self.modifier.get('requirements', [])
        modifier_node.arguments = self.modifier.get('arguments', [])
        
        # Do not populate strings in the modifier node; localizations should
        # only appear in the localization.xml file, not in game-effects.xml
        modifier_node.strings = []
        
        # Populate game_effects with modifier
        self._game_effects = GameEffectNode()
        self._game_effects.modifiers = [modifier_node]
        
        # ==== POPULATE _current DATABASE ====
        # Populate modifier_strings if provided
        if self.modifier_strings:
            modifier_string_nodes = []
            for string_info in self.modifier_strings:
                if isinstance(string_info, dict):
                    string_node = ModifierStringNode(
                        modifier_type=modifier_type_or_id,
                        string_type=string_info.get('string_type'),
                        text=string_info.get('text')
                    )
                    modifier_string_nodes.append(string_node)
            if modifier_string_nodes:
                self._current.modifier_strings = modifier_string_nodes
        
        # ==== POPULATE _localizations DATABASE ====
        # Populate localizations
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                modifier_id = modifier_node.id
                for key, text in loc.items():
                    localization_rows.append(EnglishTextNode(
                        tag=locale(modifier_id, key),
                        text=text
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self
    
    def build(self) -> list[BaseFile]:
        """
        Build modifier files with preview strings in current.xml.
        
        Note: ModifierBuilder typically doesn't generate standalone files.
        Modifiers are usually bound to other builders (CivilizationBuilder, etc.)
        and their content is merged into the parent builder's files.
        Returns empty list as modifiers are merged into parent builders.
        """
        # ModifierBuilder content is merged into parent builders via bind()
        # No standalone files should be generated
        return []


class GameModifierBuilder(BaseBuilder):
    """Builder for creating game-wide modifiers with preview strings."""
    
    def __init__(self) -> None:
        """Initialize game modifier builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._localizations = DatabaseNode()
        
        self.modifier_type: Optional[str] = None
        self.modifier: Dict[str, Any] = {}
        self.modifier_strings: list[Dict[str, Any]] = []
        self.localizations: List[Dict[str, Any]] = []

    def fill(self, payload: Dict[str, Any]) -> "GameModifierBuilder":
        """Fill game modifier builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "GameModifierBuilder":
        """Migrate and populate game modifier database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import EnglishTextNode
        
        modifier_type = self.modifier_type or self.modifier.get('modifier_type')
        if not modifier_type:
            return self
        
        # ==== POPULATE _current DATABASE ====
        # Populate modifier_strings if provided
        if self.modifier_strings:
            modifier_string_nodes = []
            for string_info in self.modifier_strings:
                if isinstance(string_info, dict):
                    string_node = ModifierStringNode(
                        modifier_type=modifier_type,
                        string_type=string_info.get('string_type'),
                        text=string_info.get('text')
                    )
                    modifier_string_nodes.append(string_node)
            if modifier_string_nodes:
                self._current.modifier_strings = modifier_string_nodes
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                for key, text in loc.items():
                    localization_rows.append(EnglishTextNode(
                        tag=locale(modifier_type, key),
                        text=text
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self
    
    def build(self) -> list[BaseFile]:
        """Build game modifier files."""
        files = []
        
        # Generate current.xml if we have modifier_strings
        if self.modifier_strings and hasattr(self, '_current'):
            xml_file = XmlFile(
                name="current.xml",
                action_group=self.action_group_bundle.current,
                root_element="Database"
            )
            xml_file.add_element(self._current)
            files.append(xml_file)
        
        # Generate localizations.xml if we have localizations
        if self.localizations and hasattr(self, '_localizations'):
            xml_file = XmlFile(
                name="localization.xml",
                action_group=self.action_group_bundle.always,
                root_element="Database"
            )
            xml_file.add_element(self._localizations)
            files.append(xml_file)
        
        return files


class UnitAbilityBuilder(BaseBuilder):
    """Builder for creating unit abilities with modifier integration."""
    
    def __init__(self) -> None:
        """Initialize unit ability builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._game_effects: Optional[DatabaseNode] = None
        self._localizations = DatabaseNode()
        
        self.ability_type: Optional[str] = None
        self.ability: Dict[str, Any] = {}
        self.inactive: bool = False
        self.charged_config: Optional[Dict[str, Any]] = None  # {'recharge_turns': 5}
        self.localizations: List[Dict[str, Any]] = []
        self._bound_modifiers: List['ModifierBuilder'] = []

    def fill(self, payload: Dict[str, Any]) -> "UnitAbilityBuilder":
        """Fill unit ability builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "UnitAbilityBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import (
            UnitAbilityNode,
            UnitAbilityModifierNode,
            ChargedUnitAbilityNode,
            EnglishTextNode,
            GameEffectNode,
        )
        
        if not self.ability_type:
            raise ValueError("ability_type is required for UnitAbilityBuilder")
        
        # Generate localization keys
        loc_name = locale(self.ability_type, 'name')
        loc_description = locale(self.ability_type, 'description')
        
        # ==== POPULATE _current DATABASE ====
        # Types
        self._current.types = [
            TypeNode(type_=self.ability_type, kind="KIND_ABILITY"),
        ]
        
        # Unit ability definition
        ability_node = UnitAbilityNode(
            unit_ability_type=self.ability_type,
            name=loc_name,
            description=loc_description,
            inactive=self.inactive if self.inactive else None,
        )
        # Apply additional ability properties
        for key, value in self.ability.items():
            setattr(ability_node, key, value)
        
        self._current.unit_abilities = [ability_node]
        
        # Charged ability configuration
        if self.charged_config:
            charged_node = ChargedUnitAbilityNode(
                unit_ability_type=self.ability_type,
                recharge_turns=self.charged_config.get('recharge_turns'),
            )
            self._current.charged_unit_abilities = [charged_node]
        
        # ==== POPULATE _game_effects DATABASE ====
        # Process bound modifiers and link them to this ability
        if self._bound_modifiers:
            ability_modifier_nodes = []
            all_game_effect_modifiers = []
            
            for modifier_builder in self._bound_modifiers:
                # Ensure modifier is migrated
                modifier_builder.migrate()
                
                # Get modifier ID from builder
                modifier_id = modifier_builder.modifier_type or modifier_builder.modifier.get('id')
                if not modifier_id:
                    continue
                
                # Create UnitAbilityModifier junction entry
                ability_modifier_nodes.append(UnitAbilityModifierNode(
                    unit_ability_type=self.ability_type,
                    modifier_id=modifier_id,
                ))
                
                # Collect game effect modifiers from bound builders
                if modifier_builder._game_effects and hasattr(modifier_builder._game_effects, 'modifiers'):
                    all_game_effect_modifiers.extend(modifier_builder._game_effects.modifiers)
            
            self._current.unit_ability_modifiers = ability_modifier_nodes
            
            # Merge all game effects
            if all_game_effect_modifiers:
                if not self._game_effects:
                    from civ7_modding_tools.nodes.nodes import GameEffectNode
                    self._game_effects = GameEffectNode()
                self._game_effects.modifiers = all_game_effect_modifiers
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if 'name' in loc:
                localization_rows.append(EnglishTextNode(
                    tag=loc_name,
                    text=loc['name']
                ))
            if 'description' in loc:
                localization_rows.append(EnglishTextNode(
                    tag=loc_description,
                    text=loc['description']
                ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self

    def bind(self, items: List['ModifierBuilder']) -> "UnitAbilityBuilder":
        """
        Bind ModifierBuilder items to this ability.
        
        Creates UnitAbilityModifiers junction entries and merges game effects.
        
        Args:
            items: List of ModifierBuilder instances to attach
            
        Returns:
            Self for fluent API chaining
        """
        for item in items:
            if not isinstance(item, ModifierBuilder):
                raise TypeError(f"Can only bind ModifierBuilder to UnitAbilityBuilder, got {type(item)}")
            self._bound_modifiers.append(item)
        return self

    def build(self) -> list[BaseFile]:
        """
        Build unit ability files.
        
        Note: UnitAbilityBuilder doesn't generate files directly.
        Instead, it's meant to be bound to a UnitBuilder which
        generates the combined output.
        """
        return []


class TraditionBuilder(BaseBuilder):
    """Builder for creating cultural traditions."""
    
    def __init__(self) -> None:
        """Initialize tradition builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._game_effects = DatabaseNode()
        self._localizations = DatabaseNode()
        
        self.tradition_type: Optional[str] = None
        self.tradition: Dict[str, Any] = {}
        self.localizations: List[Dict[str, Any]] = []

    def fill(self, payload: Dict[str, Any]) -> "TraditionBuilder":
        """Fill tradition builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "TraditionBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import TraditionNode
        
        if not self.tradition_type:
            return self
        
        # Generate localization keys
        loc_name = locale(self.tradition_type, 'name')
        loc_description = locale(self.tradition_type, 'description')
        
        # ==== POPULATE _current DATABASE ====
        # Types
        self._current.types = [
            TypeNode(type_=self.tradition_type, kind="KIND_TRADITION"),
        ]
        
        # Tradition definition with localization
        tradition_node = TraditionNode(
            tradition_type=self.tradition_type,
            name=loc_name,
            description=loc_description,
        )
        for key, value in self.tradition.items():
            setattr(tradition_node, key, value)
        self._current.traditions = [tradition_node]
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            # Handle both dict and TraditionLocalization objects
            loc_dict = loc.model_dump() if hasattr(loc, 'model_dump') else loc
            
            if isinstance(loc_dict, dict):
                if "name" in loc_dict:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc_dict["name"]
                    ))
                if "description" in loc_dict:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_description,
                        text=loc_dict["description"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self

    def bind(self, items: List[BaseBuilder]) -> "TraditionBuilder":
        """Bind ModifierBuilder items to this tradition."""
        from civ7_modding_tools.nodes import TraditionModifierNode
        
        for item in items:
            # Check for ModifierBuilder
            if hasattr(item, 'modifier') and hasattr(item, '_game_effects'):
                # Merge modifiers from game_effects
                if hasattr(item._game_effects, 'modifiers') and item._game_effects.game_modifiers:
                    if not self._game_effects.game_modifiers:
                        self._game_effects.game_modifiers = []
                    self._game_effects.game_modifiers.extend(item._game_effects.game_modifiers)
                    
                    # Add tradition modifiers if not detached
                    if not getattr(item, 'is_detached', False):
                        if not self._current.tradition_modifiers:
                            self._current.tradition_modifiers = []
                        for modifier in item._game_effects.game_modifiers:
                            modifier_id = getattr(modifier, 'id', None)
                            if modifier_id:
                                self._current.tradition_modifiers.append(
                                    TraditionModifierNode(
                                        tradition_type=self.tradition_type,
                                        modifier_id=modifier_id
                                    )
                                )
                
                # Merge localizations
                if hasattr(item, '_localizations') and item._localizations:
                    if item._localizations.english_text:
                        if not self._localizations.english_text:
                            self._localizations.english_text = []
                        self._localizations.english_text.extend(item._localizations.english_text)
        
        return self
    
    def build(self) -> list[BaseFile]:
        """Build tradition files."""
        from civ7_modding_tools.utils import trim, kebab_case
        
        files: list[BaseFile] = []
        
        if not self.tradition_type:
            return files
        
        self.migrate()
        
        # Generate path (trimmed + kebab-case)
        trimmed = trim(self.tradition_type)
        path = f"/traditions/{kebab_case(trimmed)}/"
        
        # Create files
        files.append(XmlFile(
            path=path,
            name="current.xml",
            content=self._current,
            action_group=self.action_group_bundle.current
        ))
        
        if self._game_effects and len(self._game_effects.game_modifiers) > 0:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=self._game_effects,
                action_group=self.action_group_bundle.current
            ))
        
        files.append(XmlFile(
            path=path,
            name="localization.xml",
            content=self._localizations,
            action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
        ))
        
        # Filter out empty files
        files = [f for f in files if f.content is not None]
        
        return files


class UniqueQuarterBuilder(BaseBuilder):
    """Builder for creating unique quarters (district-specific buildings)."""
    
    def __init__(self) -> None:
        """Initialize unique quarter builder."""
        super().__init__()
        self._always = DatabaseNode()
        self._icons = DatabaseNode()
        self._localizations = DatabaseNode()
        self._game_effects: Optional['GameEffectNode'] = None
        
        self.unique_quarter_type: Optional[str] = None
        self.unique_quarter: Dict[str, Any] = {}
        self.unique_quarter_modifiers: List[Dict[str, Any]] = []
        self.game_modifiers: List[Dict[str, Any]] = []
        self.localizations: List[Dict[str, Any]] = []
        self.icon: Dict[str, Any] = {'path': 'fs://game/civ_sym_han'}

    def fill(self, payload: Dict[str, Any]) -> "UniqueQuarterBuilder":
        """Fill unique quarter builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "UniqueQuarterBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import (
            UniqueQuarterNode,
            UniqueQuarterModifierNode,
        )
        
        if not self.unique_quarter_type:
            return self
        
        # Generate localization keys
        loc_name = locale(self.unique_quarter_type, 'name')
        loc_description = locale(self.unique_quarter_type, 'description')
        
        # ==== POPULATE _always DATABASE ====
        # Types
        self._always.types = [
            TypeNode(type_=self.unique_quarter_type, kind="KIND_QUARTER"),
        ]
        
        # Main unique quarter row with localization
        # Preserve existing trait_type if already set (by parent civilization)
        existing_trait_type = None
        if self._always.unique_quarters:
            existing_trait_type = self._always.unique_quarters[0].trait_type
        
        quarter_node = UniqueQuarterNode(
            unique_quarter_type=self.unique_quarter_type,
            name=loc_name,
            description=loc_description,
        )
        if existing_trait_type is not None:
            quarter_node.trait_type = existing_trait_type
        
        for key, value in self.unique_quarter.items():
            setattr(quarter_node, key, value)
        self._always.unique_quarters = [quarter_node]
        
        # Unique quarter modifiers (linked to effects)
        if self.unique_quarter_modifiers:
            self._always.unique_quarter_modifiers = [
                UniqueQuarterModifierNode(
                    unique_quarter_type=self.unique_quarter_type,
                    modifier_id=mod.get('modifier_id')
                )
                for mod in self.unique_quarter_modifiers
            ]
        
        # ==== POPULATE _icons DATABASE ====
        icon_node = IconDefinitionNode(id=self.unique_quarter_type)
        if self.icon:
            for key, value in self.icon.items():
                setattr(icon_node, key, value)
        self._icons.icon_definitions = [icon_node]
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc["name"]
                    ))
                if "description" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_description,
                        text=loc["description"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self

    def bind(self, items: List[BaseBuilder]) -> "UniqueQuarterBuilder":
        """Bind ModifierBuilder items to this unique quarter."""
        from civ7_modding_tools.nodes import UniqueQuarterModifierNode, GameModifierNode, GameEffectNode
        
        for item in items:
            # Check for ModifierBuilder
            if hasattr(item, 'modifier') and hasattr(item, '_game_effects'):
                item.migrate()  # Ensure migration is done
                
                # Merge modifiers from game_effects
                if item._game_effects and hasattr(item._game_effects, 'modifiers'):
                    # Initialize game effects if needed
                    if not self._game_effects:
                        self._game_effects = GameEffectNode()
                        self._game_effects.modifiers = []
                    
                    # Add modifier nodes directly to game effects
                    self._game_effects.modifiers.extend(item._game_effects.modifiers)
                    
                    # Add unique quarter modifiers and game modifiers if not detached
                    if not getattr(item, 'is_detached', False):
                        # Add to UniqueQuarterModifiers table
                        if not self._always.unique_quarter_modifiers:
                            self._always.unique_quarter_modifiers = []
                        for modifier in item._game_effects.modifiers:
                            self._always.unique_quarter_modifiers.append(
                                UniqueQuarterModifierNode(
                                    unique_quarter_type=self.unique_quarter_type,
                                    modifier_id=modifier.id
                                )
                            )
                        
                        # Add to GameModifiers table
                        if not hasattr(self._always, 'game_modifiers') or not self._always.game_modifiers:
                            self._always.game_modifiers = []
                        for modifier in item._game_effects.modifiers:
                            self._always.game_modifiers.append(
                                GameModifierNode(modifier_id=modifier.id)
                            )
                
                # Merge localizations
                if hasattr(item, '_localizations') and item._localizations:
                    if item._localizations.english_text:
                        if not self._localizations.english_text:
                            self._localizations.english_text = []
                        self._localizations.english_text.extend(item._localizations.english_text)
        
        return self

    def build(self) -> list[BaseFile]:
        """Build unique quarter files."""
        from civ7_modding_tools.utils import kebab_case
        
        files: list[BaseFile] = []
        
        if not self.unique_quarter_type:
            return files
        
        self.migrate()
        
        # Generate path (kebab-case only, no trim)
        path = f"/constructibles/{kebab_case(self.unique_quarter_type)}/"
        
        # Create files
        files.append(XmlFile(
            path=path,
            name="always.xml",
            content=self._always,
            action_groups=[self.action_group_bundle.always]
        ))
        
        files.append(XmlFile(
            path=path,
            name="icons.xml",
            content=self._icons,
            action_groups=[self.action_group_bundle.always]
        ))
        
        files.append(XmlFile(
            path=path,
            name="localization.xml",
            content=self._localizations,
            action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
        ))
        
        if self._game_effects:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=self._game_effects,
                action_group=self.action_group_bundle.always
            ))
        
        # Filter out empty files
        files = [f for f in files if f.content is not None]
        
        return files


class LeaderUnlockBuilder(BaseBuilder):
    """Builder for creating leader-civilization pairings with leader bias."""
    
    def __init__(self) -> None:
        """Initialize leader unlock builder."""
        super().__init__()
        self.leader_unlock_type: Optional[str] = None
        self.leader_unlock: Dict[str, Any] = {}
        self.leader_civilization_biases: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build leader unlock files."""
        from civ7_modding_tools.nodes import (
            LeaderUnlockNode,
            LeaderCivilizationBiasNode,
        )
        
        files: list[BaseFile] = []
        
        if not self.leader_unlock_type:
            return files
        
        leader_nodes: list[BaseNode] = []
        
        # Add main leader unlock row
        leader_node = LeaderUnlockNode()
        leader_node.leader_unlock_type = self.leader_unlock_type
        for key, value in self.leader_unlock.items():
            setattr(leader_node, key, value)
        leader_nodes.append(leader_node)
        
        # Add leader civilization biases
        for bias in self.leader_civilization_biases:
            bias_node = LeaderCivilizationBiasNode()
            bias_node.leader_unlock_type = self.leader_unlock_type
            for key, value in bias.items():
                setattr(bias_node, key, value)
            leader_nodes.append(bias_node)
        
        # Create leader unlock file
        leader_file = XmlFile(
            path=f"/leaders/{self.leader_unlock_type.lower()}/",
            name="leader.xml",
            content=leader_nodes
        )
        files.append(leader_file)
        
        return files


class CivilizationUnlockBuilder(BaseBuilder):
    """Builder for creating civilization unlocks (age-based progressions)."""
    
    def __init__(self) -> None:
        """Initialize civilization unlock builder."""
        super().__init__()
        self.civilization_unlock_type: Optional[str] = None
        self.civilization_unlock: Dict[str, Any] = {}
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build civilization unlock files."""
        from civ7_modding_tools.nodes import (
            CivilizationUnlockNode,
        )
        
        files: list[BaseFile] = []
        
        if not self.civilization_unlock_type:
            return files
        
        civ_unlock_nodes: list[BaseNode] = []
        
        # Add main civilization unlock row
        unlock_node = CivilizationUnlockNode()
        unlock_node.civilization_unlock_type = self.civilization_unlock_type
        for key, value in self.civilization_unlock.items():
            setattr(unlock_node, key, value)
        civ_unlock_nodes.append(unlock_node)
        
        # Create civilization unlock file
        unlock_file = XmlFile(
            path=f"/civilization-unlocks/{self.civilization_unlock_type.lower()}/",
            name="unlock.xml",
            content=civ_unlock_nodes
        )
        files.append(unlock_file)
        
        return files


class UnlockBuilder(BaseBuilder):
    """Builder for creating generic unlock configurations."""
    
    def __init__(self) -> None:
        """Initialize unlock builder."""
        super().__init__()
        self.unlock_type: Optional[str] = None
        self.unlock: Dict[str, Any] = {}
        self.unlock_rewards: List[Dict[str, Any]] = []
        self.unlock_requirements: List[Dict[str, Any]] = []
        self.unlock_configs: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build unlock files."""
        from civ7_modding_tools.nodes import (
            UnlockNode,
            UnlockRewardNode,
            UnlockRequirementNode,
            UnlockConfigurationValueNode,
        )
        
        files: list[BaseFile] = []
        
        if not self.unlock_type:
            return files
        
        unlock_nodes: list[BaseNode] = []
        
        # Add main unlock row
        unlock_node = UnlockNode()
        unlock_node.unlock_type = self.unlock_type
        for key, value in self.unlock.items():
            setattr(unlock_node, key, value)
        unlock_nodes.append(unlock_node)
        
        # Add unlock rewards
        for reward in self.unlock_rewards:
            reward_node = UnlockRewardNode()
            reward_node.unlock_type = self.unlock_type
            for key, value in reward.items():
                setattr(reward_node, key, value)
            unlock_nodes.append(reward_node)
        
        # Add unlock requirements
        for req in self.unlock_requirements:
            req_node = UnlockRequirementNode()
            req_node.unlock_type = self.unlock_type
            for key, value in req.items():
                setattr(req_node, key, value)
            unlock_nodes.append(req_node)
        
        # Add unlock configuration values
        for config in self.unlock_configs:
            config_node = UnlockConfigurationValueNode()
            config_node.unlock_type = self.unlock_type
            for key, value in config.items():
                setattr(config_node, key, value)
            unlock_nodes.append(config_node)
        
        # Create unlock file
        unlock_file = XmlFile(
            path=f"/unlocks/{self.unlock_type.lower()}/",
            name="unlock.xml",
            content=unlock_nodes
        )
        files.append(unlock_file)
        
        return files


class ImportFileBuilder(BaseBuilder):
    """Builder for importing external files (images, SQL, custom data)."""
    
    def __init__(self) -> None:
        """Initialize import file builder."""
        super().__init__()
        self.source_path: Optional[str] = None
        self.target_name: Optional[str] = None
        self.target_directory: str = "/imports/"
        self.scope: str = "game"  # "shell" or "game" - determines ActionGroup placement
    
    def get_import_entries(self) -> list[str]:
        """
        Get import entries for modinfo ImportFiles block.
        
        Returns both folder and individual file entries for the imported asset.
        
        Returns:
            List of import paths (folder and file)
        """
        if not self.source_path or not self.target_name:
            return []
        
        from pathlib import Path
        source = Path(self.source_path)
        
        entries = []
        
        # Add folder entry (e.g., "icons")
        folder = self.target_directory.strip("/")
        if folder:
            entries.append(folder)
        
        # Add file entry (e.g., "icons/civs/civ_sym_babylon.png")
        if source.exists():
            file_entry = f"{folder}/{self.target_name}" if folder else self.target_name
            entries.append(file_entry)
        
        return entries
    
    def build(self) -> list[BaseFile]:
        """Build import files."""
        from civ7_modding_tools.files import ImportFile
        
        files: list[BaseFile] = []
        
        if not self.source_path or not self.target_name:
            return files
        
        # Use scope to determine which action groups to assign
        action_groups_to_use = []
        if self.scope == "shell":
            action_groups_to_use = [self.action_group_bundle.shell]
        elif self.scope == "always":
            action_groups_to_use = [self.action_group_bundle.always]
        else:  # "game" (default)
            action_groups_to_use = [self.action_group_bundle.shell, self.action_group_bundle.always]
        
        # Create import file
        import_file = ImportFile(
            path=self.target_directory,
            name=self.target_name,
            content=self.source_path,
            action_groups=action_groups_to_use
        )
        files.append(import_file)
        
        return files

class GreatPersonBuilder(UnitBuilder):
    """Builder for creating great people units."""
    
    def __init__(self) -> None:
        """Initialize great person builder."""
        super().__init__()
        self.great_person_type: Optional[str] = None
        self.great_person_class: Optional[str] = None
        self.base_unit: Optional[str] = None
    
    def fill(self, payload: Dict[str, Any]) -> "GreatPersonBuilder":
        """Fill great person builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def migrate(self) -> "GreatPersonBuilder":
        """Migrate great person properties."""
        from civ7_modding_tools.utils import locale
        
        if not self.unit_type or not self.great_person_type:
            return self
        
        # Call parent class migrate to handle unit properties
        super().migrate()
        
        # Add great person specific nodes to _current database
        if self.great_person_class and self.base_unit:
            # Create KindNode for great person
            self._current.kinds = [KindNode(
                kind='KIND_UNIT_GREAT_PERSON',
                sort_index=1
            )]
            
            # Create GreatPersonNode to link type and class
            gp_node = GreatPersonNode(
                great_person_type=self.great_person_type,
                great_person_class=self.great_person_class,
                base_unit_type=self.base_unit
            )
            self._current.great_persons = [gp_node]
        
        return self
    
    def bind(self, items: list[BaseBuilder]) -> "GreatPersonBuilder":
        """Bind ModifierBuilder items to this great person."""
        for item in items:
            # Check for ModifierBuilder
            if hasattr(item, '_game_effects'):
                # Merge modifiers
                if hasattr(item._game_effects, 'game_modifiers') and item._game_effects.game_modifiers:
                    if not self._current.modifiers:
                        self._current.modifiers = []
                    self._current.modifiers.extend(item._game_effects.game_modifiers)
        
        return self
    
    def build(self) -> list[BaseFile]:
        """Build great person files."""
        if not self.unit_type or not self.great_person_type:
            return []
        
        # Call parent migrate if not already done
        self.migrate()
        
        files: list[BaseFile] = []
        
        # Determine action groups based on bundle scope
        action_groups_to_use: list[ActionGroupNode] = []
        if self.action_group_bundle.action_group_id == 'ALWAYS':
            action_groups_to_use = [self.action_group_bundle.always]
        else:
            # Use descriptive ID with current/persist scopes
            action_groups_to_use = [
                self.action_group_bundle.current,
                self.action_group_bundle.persist,
            ]
        
        # Generate current.xml for great person unit definition
        current_file = XmlFile(
            path=f'/units/{self._kebab_case_path()}/',
            name='current.xml',
            content=self._current,
            action_groups=action_groups_to_use
        )
        files.append(current_file)
        
        # Generate icons.xml if icon definitions exist
        if self._icons.icon_definitions:
            icons_file = XmlFile(
                path=f'/units/{self._kebab_case_path()}/',
                name='icons.xml',
                content=self._icons,
                action_groups=action_groups_to_use
            )
            files.append(icons_file)
        
        # Generate localization.xml
        localization_file = XmlFile(
            path=f'/units/{self._kebab_case_path()}/',
            name='localization.xml',
            content=self._localizations,
            action_groups=[self.action_group_bundle.shell]
        )
        files.append(localization_file)
        
        # Generate visual-remap.xml if needed
        if self._visual_remap and self._visual_remap.visual_remaps:
            visual_file = XmlFile(
                path=f'/units/{self._kebab_case_path()}/',
                name='visual-remap.xml',
                content=self._visual_remap,
                action_groups=action_groups_to_use
            )
            files.append(visual_file)
        
        return files
    
    def _kebab_case_path(self) -> str:
        """Generate kebab-case path from unit type."""
        from civ7_modding_tools.utils import trim, kebab_case
        
        trimmed = trim(self.unit_type)
        return kebab_case(trimmed)


class NamedPlaceBuilder(BaseBuilder):
    """Builder for creating named places (geographic locations with game effects)."""
    
    def __init__(self) -> None:
        """Initialize named place builder with database variants."""
        super().__init__()
        self._current = DatabaseNode()
        self._localizations = DatabaseNode()
        
        self.named_place_type: Optional[str] = None
        self.placement: Optional[str] = None
        self.yield_changes: list[Dict[str, Any]] = []
        self.icon: Dict[str, Any] = {}
        self.localizations: list[Dict[str, Any]] = []
    
    def fill(self, payload: Dict[str, Any]) -> "NamedPlaceBuilder":
        """Fill named place builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    def migrate(self) -> "NamedPlaceBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        
        if not self.named_place_type:
            return self
        
        # Generate localization keys
        loc_name = locale(self.named_place_type, 'name')
        loc_description = locale(self.named_place_type, 'description')
        
        # ==== POPULATE _current DATABASE ====
        # Types
        self._current.types = [
            TypeNode(type_=self.named_place_type, kind="KIND_NAMED_PLACE"),
        ]
        
        # Tags
        named_place_tag = self.named_place_type.replace('NAMED_PLACE_', 'NAMED_PLACE_CLASS_')
        self._current.tags = [
            TagNode(tag=named_place_tag, category='NAMED_PLACE_CLASS')
        ]
        
        # TypeTags
        self._current.type_tags = [
            TypeTagNode(type_=self.named_place_type, tag=named_place_tag)
        ]
        
        # Named place definition
        from civ7_modding_tools.nodes import NamedPlaceNode
        place_node = NamedPlaceNode(
            named_place_type=self.named_place_type,
            placement=self.placement,
            name=loc_name,
            description=loc_description
        )
        self._current.named_places = [place_node]
        
        # Yield changes
        if self.yield_changes:
            from civ7_modding_tools.nodes import NamedPlaceYieldChangeNode
            yield_nodes = []
            for change in self.yield_changes:
                yield_node = NamedPlaceYieldChangeNode(
                    named_place_type=self.named_place_type
                )
                for key, value in change.items():
                    setattr(yield_node, key, value)
                yield_nodes.append(yield_node)
            self._current.named_place_yields = yield_nodes
        
        # ==== POPULATE _localizations DATABASE ====
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_name,
                        text=loc["name"]
                    ))
                if "description" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_description,
                        text=loc["description"]
                    ))
        
        if localization_rows:
            self._localizations.english_texts = localization_rows
        
        return self
    
    def bind(self, items: list[BaseBuilder]) -> "NamedPlaceBuilder":
        """Bind ModifierBuilder items to this named place."""
        for item in items:
            # Check for ModifierBuilder
            if hasattr(item, '_game_effects'):
                # Merge modifiers
                if hasattr(item._game_effects, 'game_modifiers') and item._game_effects.game_modifiers:
                    if not self._current.modifiers:
                        self._current.modifiers = []
                    self._current.modifiers.extend(item._game_effects.game_modifiers)
        
        return self
    
    def build(self) -> list[BaseFile]:
        """Build named place files."""
        if not self.named_place_type:
            return []
        
        # Call migrate if not already done
        self.migrate()
        
        files: list[BaseFile] = []
        
        # Determine action groups based on bundle scope
        action_groups_to_use: list[ActionGroupNode] = []
        if self.action_group_bundle.action_group_id == 'ALWAYS':
            action_groups_to_use = [self.action_group_bundle.always]
        else:
            # Use descriptive ID with current/persist scopes
            action_groups_to_use = [
                self.action_group_bundle.current,
                self.action_group_bundle.persist,
            ]
        
        # Generate current.xml for named place definition
        current_file = XmlFile(
            path=f'/named-places/{self._kebab_case_path()}/',
            name='current.xml',
            content=self._current,
            action_groups=action_groups_to_use
        )
        files.append(current_file)
        
        # Generate localization.xml
        localization_file = XmlFile(
            path=f'/named-places/{self._kebab_case_path()}/',
            name='localization.xml',
            content=self._localizations,
            action_groups=[self.action_group_bundle.shell]
        )
        files.append(localization_file)
        
        return files
    
    def _kebab_case_path(self) -> str:
        """Generate kebab-case path from named place type."""
        from civ7_modding_tools.utils import trim, kebab_case
        
        trimmed = trim(self.named_place_type)
        return kebab_case(trimmed)
