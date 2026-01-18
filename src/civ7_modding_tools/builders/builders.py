"""Concrete builder implementations for Civilization 7 mods."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
from civ7_modding_tools.core.mod import ActionGroupBundle
from civ7_modding_tools.files import BaseFile, XmlFile
from civ7_modding_tools.nodes import (
    BaseNode,
    CivilizationNode,
    CivilizationTraitNode,
    UnitNode,
    UnitCostNode,
    UnitStatNode,
    UnitReplaceNode,
    ConstructibleNode,
    ConstructibleYieldChangeNode,
    ConstructibleValidDistrictNode,
    ConstructibleMaintenanceNode,
    UniqueQuarterNode,
    UniqueQuarterModifierNode,
    ProgressionTreeNode,
    ProgressionTreeNodeNode,
    ProgressionTreePrereqNode,
    ProgressionTreeAdvisoryNode,
    ProgressionTreeNodeUnlockNode,
    GameModifierNode,
    ModifierNode,
    StringNode,
    TraditionNode,
    TraditionModifierNode,
    CityNameNode,
    DatabaseNode,
    TypeNode,
    TraitNode,
    TagNode,
    TypeTagNode,
    BuildingNode,
    ImprovementNode,
    StartBiasBiomeNode,
    StartBiasTerrainNode,
    IconDefinitionNode,
    LegacyCivilizationNode,
    LegacyCivilizationTraitNode,
    EnglishTextNode,
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
        self._current = DatabaseNode()         # Current age data
        self._shell = DatabaseNode()           # UI/shell scope data
        self._legacy = DatabaseNode()          # Legacy compatibility (INSERT OR IGNORE)
        self._icons = DatabaseNode()           # Icon definitions
        self._localizations = DatabaseNode()   # Localized text
        self._game_effects = DatabaseNode()    # Modifiers and effects
        
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
        self.modifiers: List[Dict[str, Any]] = []
        self.trait: Dict[str, str] = {}
        self.trait_ability: Dict[str, str] = {}
        self.civilization_legacy: Dict[str, Any] = {}
        
        # Store bound items for processing during migration
        self._bound_items: List[BaseBuilder] = []

    def fill(self, payload: Dict[str, Any]) -> "CivilizationBuilder":
        """Fill civilization builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "CivilizationBuilder":
        """Migrate and populate all database variants with full localization."""
        if not self.civilization_type:
            self.civilization_type = self.civilization.get('civilization_type', 'CIVILIZATION_CUSTOM')
        
        # Generate trait types from civilization type if not provided
        if not self.trait:
            trait_base = self.civilization_type.replace('CIVILIZATION_', '')
            self.trait = {"trait_type": f"TRAIT_{trait_base}"}
        if not self.trait_ability:
            self.trait_ability = {"trait_type": f"{self.trait.get('trait_type', 'TRAIT')}_ABILITY"}
        
        trait_type = self.trait.get("trait_type", "TRAIT_CUSTOM")
        trait_ability_type = self.trait_ability.get("trait_type", "TRAIT_CUSTOM_ABILITY")
        
        # Create civilization node with full localization
        civ_node = CivilizationNode(
            civilization_type=self.civilization_type,
            adjective=locale(self.civilization_type, 'adjective'),
            capital_name=locale(self.civilization_type, 'cityNames_1'),
            full_name=locale(self.civilization_type, 'fullName'),
            name=locale(self.civilization_type, 'name'),
            starting_civilization_level_type='CIVILIZATION_LEVEL_FULL_CIV',
        )
        # Apply any overrides from self.civilization dict
        for key, value in self.civilization.items():
            if key != 'civilization_type' and hasattr(civ_node, key):
                setattr(civ_node, key, value)
        
        # Create trait nodes
        trait_node = TraitNode(
            trait_type=trait_type,
            internal_only=True
        )
        
        trait_ability_node = TraitNode(
            trait_type=trait_ability_type,
            name=locale(self.civilization_type + '_ABILITY', 'name'),
            description=locale(self.civilization_type + '_ABILITY', 'description'),
            internal_only=True
        )
        
        # ==== POPULATE _current DATABASE ====
        # Types section
        self._current.types = [
            TypeNode(type_=trait_type, kind="KIND_TRAIT"),
            TypeNode(type_=trait_ability_type, kind="KIND_TRAIT"),
        ]
        
        # Traits section
        self._current.traits = [trait_node, trait_ability_node]
        
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
        # Add additional traits specified by user
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
        
        # ==== POPULATE _shell DATABASE ====
        self._shell.civilizations = [civ_node]
        
        # ==== POPULATE _legacy DATABASE ====
        # Legacy types use insertOrIgnore
        legacy_civ_type = TypeNode(type_=self.civilization_type, kind="KIND_CIVILIZATION")
        legacy_civ_type.insert_or_ignore()
        legacy_trait_type = TypeNode(type_=trait_type, kind="KIND_TRAIT")
        legacy_trait_type.insert_or_ignore()
        legacy_trait_ability_type = TypeNode(type_=trait_ability_type, kind="KIND_TRAIT")
        legacy_trait_ability_type.insert_or_ignore()
        
        self._legacy.types = [
            legacy_civ_type,
            legacy_trait_type,
            legacy_trait_ability_type,
        ]
        
        # Legacy trait uses insertOrIgnore
        legacy_trait = TraitNode(trait_type=trait_type, internal_only=True)
        legacy_trait.insert_or_ignore()
        self._legacy.traits = [legacy_trait]
        
        legacy_civ = LegacyCivilizationNode(
            civilization_type=self.civilization_type,
            age=self.civilization_legacy.get("age", "AGE_ANTIQUITY")
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
                prefix = self.civilization_type
                if "name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=f"{prefix}_NAME",
                        text=loc["name"]
                    ))
                if "description" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=f"{prefix}_DESCRIPTION",
                        text=loc["description"]
                    ))
                if "full_name" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=f"{prefix}_FULL_NAME",
                        text=loc["full_name"]
                    ))
                if "adjective" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=f"{prefix}_ADJECTIVE",
                        text=loc["adjective"]
                    ))
                if "city_names" in loc:
                    for i, city_name in enumerate(loc["city_names"], 1):
                        localization_rows.append(EnglishTextNode(
                            tag=f"{prefix}_CITY_NAME_{i}",
                            text=city_name
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
                    
                    if hasattr(item._game_effects, 'modifiers') and item._game_effects.game_modifiers:
                        if not self._game_effects.game_modifiers:
                            self._game_effects.game_modifiers = []
                        for modifier in item._game_effects.game_modifiers:
                            modifier_id = getattr(modifier, 'id', None) or getattr(modifier, 'modifier_id', None)
                            if modifier_id:
                                self._game_effects.game_modifiers.append(
                                    GameModifierNode(modifier_id=modifier_id)
                                )
                        
                        if not getattr(item, 'is_detached', False):
                            if not self._current.trait_modifiers:
                                self._current.trait_modifiers = []
                            for modifier in item._game_effects.game_modifiers:
                                modifier_id = getattr(modifier, 'id', None) or getattr(modifier, 'modifier_id', None)
                                if modifier_id:
                                    self._current.trait_modifiers.append(
                                        TraitModifierNode(
                                            trait_type=trait_ability_type,
                                            modifier_id=modifier_id
                                        )
                                    )
                    
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
                    if hasattr(item, '_always') and item._always:
                        for building in getattr(item._always, 'buildings', []):
                            building.trait_type = trait_type
                        for improvement in getattr(item._always, 'improvements', []):
                            improvement.trait_type = trait_type
                
                # Handle UniqueQuarterBuilder
                elif hasattr(item, 'unique_quarter_type') and item.unique_quarter_type:
                    if hasattr(item, '_always') and item._always:
                        for unique_quarter in getattr(item._always, 'unique_quarters', []):
                            unique_quarter.trait_type = trait_type
                
                # Handle ProgressionTreeBuilder
                elif hasattr(item, 'progression_tree_type') and item.progression_tree_type:
                    if hasattr(item, '_game_effects') and item._game_effects:
                        if item._game_effects.game_modifiers:
                            if not self._game_effects.game_modifiers:
                                self._game_effects.game_modifiers = []
                            self._game_effects.game_modifiers.extend(item._game_effects.game_modifiers)
        
        return self

    def bind(self, items: List[BaseBuilder]) -> "CivilizationBuilder":
        """Bind entities to this civilization (units, buildings, modifiers, etc.)."""
        # Store items for processing during migration
        self._bound_items.extend(items)
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
                action_group=self.action_group_bundle.current
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
        self.unit: Dict[str, Any] = {}
        self.unit_stats: list[Dict[str, Any]] = []
        self.unit_costs: list[Dict[str, Any]] = []
        self.unit_cost: Dict[str, Any] = {}  # Support single cost format
        self.unit_stat: Dict[str, Any] = {}  # Support single stat format
        self.unit_replace: Optional[Dict[str, Any]] = None
        self.unit_upgrade: Optional[Dict[str, Any]] = None
        self.unit_advisories: list[Dict[str, Any]] = []
        self.visual_remap: Optional[Dict[str, Any]] = None
        self.icon: Dict[str, Any] = {}
        self.localizations: list[Dict[str, Any]] = []
        self.type_tags: list[str] = []  # Additional type tags (e.g., UNIT_CLASS_RECON)

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
            # TODO: Add UnitUpgradeNode when needed
            pass
        
        # Unit advisories
        if self.unit_advisories:
            # TODO: Add UnitAdvisoryNode when needed
            pass
        
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
                if "description" in loc:
                    localization_rows.append(EnglishTextNode(
                        tag=loc_description,
                        text=loc["description"]
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        # ==== POPULATE _visual_remap DATABASE ====
        if self.visual_remap:
            self._visual_remap = DatabaseNode()
            # TODO: Add VisualRemapNode when available
            pass
        
        return self

    def build(self) -> list[BaseFile]:
        """Build unit files with multiple variants."""
        if not self.unit_type:
            return []
        
        self.migrate()
        
        # Generate path from unit type (trimmed + kebab-case)
        from civ7_modding_tools.utils import trim, kebab_case
        trimmed = trim(self.unit_type)
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
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
            XmlFile(
                path=path,
                name="localization.xml",
                content=self._localizations,
                action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
            ),
        ]
        
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
        self._game_effects: Optional[DatabaseNode] = None
        
        self.constructible_type: Optional[str] = None
        self.constructible: Dict[str, Any] = {}
        self.building: Optional[Dict[str, Any]] = None
        self.improvement: Optional[Dict[str, Any]] = None
        self.type_tags: list[str] = []
        self.constructible_valid_districts: list[str] = []
        self.constructible_maintenances: list[Dict[str, Any]] = []
        self.yield_changes: list[Dict[str, Any]] = []
        self.localizations: list[Dict[str, Any]] = []
        self.modifiers: list[Dict[str, Any]] = []
        self.icon: Dict[str, Any] = {}

    def fill(self, payload: Dict[str, Any]) -> "ConstructibleBuilder":
        """Fill constructible builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

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
        if self.type_tags:
            self._always.type_tags = [
                TypeTagNode(type_=self.constructible_type, tag=tag)
                for tag in self.type_tags
            ]
        
        # Building (if this is a building)
        if self.building is not None:
            building_node = BuildingNode(constructible_type=self.constructible_type)
            for key, value in self.building.items():
                setattr(building_node, key, value)
            self._always.buildings = [building_node]
        
        # Improvement (if this is an improvement)
        if self.improvement is not None:
            improvement_node = ImprovementNode(constructible_type=self.constructible_type)
            for key, value in self.improvement.items():
                setattr(improvement_node, key, value)
            self._always.improvements = [improvement_node]
        
        # Constructible definition with localization
        const_node = ConstructibleNode(
            constructible_type=self.constructible_type,
            name=loc_name,
            description=loc_description,
            tooltip=loc_tooltip,
        )
        for key, value in self.constructible.items():
            setattr(const_node, key, value)
        self._always.constructibles = [const_node]
        
        # Valid districts
        if self.constructible_valid_districts:
            self._always.constructible_valid_districts = [
                ConstructibleValidDistrictNode(
                    constructible_type=self.constructible_type,
                    district_type=district
                )
                for district in self.constructible_valid_districts
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
        
        # ==== POPULATE _icons DATABASE ====
        if self.icon:
            icon_node = IconDefinitionNode(id=self.constructible_type)
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
                name="always.xml",
                content=self._always,
                action_groups=[self.action_group_bundle.always]
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
        
        # Filter out empty files
        files = [f for f in files if f.content is not None]
        
        return files


class ProgressionTreeBuilder(BaseBuilder):
    """Builder for creating progression trees (tech/civic trees)."""
    
    def __init__(self) -> None:
        """Initialize progression tree builder."""
        super().__init__()
        self._current = DatabaseNode()
        self._game_effects = DatabaseNode()
        self._localizations = DatabaseNode()
        
        self.progression_tree_type: Optional[str] = None
        self.progression_tree: Dict[str, Any] = {}
        self.progression_tree_prereqs: List[Dict[str, Any]] = []
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
        self._current.types = [
            TypeNode(type_=self.progression_tree_type, kind="KIND_TREE"),
        ]
        
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
            
            # Merge game_effects game_modifiers
            if hasattr(item, '_game_effects') and item._game_effects:
                if item._game_effects.game_modifiers:
                    if not self._game_effects.game_modifiers:
                        self._game_effects.game_modifiers = []
                    self._game_effects.game_modifiers = self._game_effects.game_modifiers + item._game_effects.game_modifiers
            
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
        
        # Create game-effects.xml if there are game_modifiers
        if self._game_effects and (
            (hasattr(self._game_effects, 'game_modifiers') and self._game_effects.game_modifiers) or
            (hasattr(self._game_effects, 'modifiers') and self._game_effects.game_modifiers)
        ):
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
        self._game_effects = DatabaseNode()
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
                if hasattr(item._game_effects, 'modifiers') and item._game_effects.game_modifiers:
                    for modifier in item._game_effects.game_modifiers:
                        modifier_id = getattr(modifier, 'id', None) or getattr(modifier, 'modifier_id', None)
                        if modifier_id:
                            if not self._current.progression_tree_node_unlocks:
                                self._current.progression_tree_node_unlocks = []
                            self._current.progression_tree_node_unlocks.append(
                                ProgressionTreeNodeUnlockNode(
                                    progression_tree_node_type=self.progression_tree_node_type,
                                    target_kind="KIND_MODIFIER",
                                    target_type=modifier_id,
                                    unlock_depth=unlock_depth,
                                    hidden=hidden
                                )
                            )
                    # Merge modifiers to game_effects
                    if not self._game_effects.game_modifiers:
                        self._game_effects.game_modifiers = []
                    # Convert modifiers to game_modifiers (GameModifierNode)
                    for modifier in item._game_effects.game_modifiers:
                        modifier_id = getattr(modifier, 'id', None) or getattr(modifier, 'modifier_id', None)
                        if modifier_id:
                            from civ7_modding_tools.nodes import GameModifierNode
                            self._game_effects.game_modifiers.append(
                                GameModifierNode(modifier_id=modifier_id)
                            )
                
                # Merge localizations
                if hasattr(item, '_localizations') and item._localizations:
                    if item._localizations.english_text:
                        if not self._localizations.english_text:
                            self._localizations.english_text = []
                        self._localizations.english_text.extend(item._localizations.english_text)
            
            # Check for ConstructibleBuilder
            elif hasattr(item, 'constructible_type') and item.constructible_type:
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
        self._game_effects = DatabaseNode()
        self._localizations = DatabaseNode()
        
        self.modifier: Dict[str, Any] = {}
        self.localizations: List[Dict[str, Any]] = []
        self.is_detached: bool = False  # Detached modifiers not bound to specific entity

    def fill(self, payload: Dict[str, Any]) -> "ModifierBuilder":
        """Fill modifier builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "ModifierBuilder":
        """Migrate and populate all database variants."""
        from civ7_modding_tools.utils import locale
        from civ7_modding_tools.nodes import ModifierNode, StringNode
        
        modifier_node = ModifierNode(**self.modifier)
        
        # Add localization strings to modifier (if modifier has attribute support)
        if self.localizations and hasattr(modifier_node, '__dict__'):
            for loc in self.localizations:
                if isinstance(loc, dict):
                    for key in loc.keys():
                        # Create string node for localization
                        # Note: strings may not be directly supported in current ModifierNode
                        # so we skip this for now
                        pass
        
        # Populate game_effects with modifier
        self._game_effects.game_modifiers = [modifier_node]
        
        # Populate localizations
        localization_rows = []
        for loc in self.localizations:
            if isinstance(loc, dict):
                modifier_id = modifier_node.modifier_id if hasattr(modifier_node, 'modifier_id') else modifier_node.id if hasattr(modifier_node, 'id') else 'MODIFIER'
                for key, text in loc.items():
                    localization_rows.append(EnglishTextNode(
                        tag=locale(modifier_id, key),
                        text=text
                    ))
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        return self
    
    def build(self) -> list[BaseFile]:
        """Build modifier files (returns empty as modifiers are bound to other builders)."""
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
        self._game_effects: Optional[DatabaseNode] = None
        
        self.unique_quarter_type: Optional[str] = None
        self.unique_quarter: Dict[str, Any] = {}
        self.unique_quarter_modifiers: List[Dict[str, Any]] = []
        self.game_modifiers: List[Dict[str, Any]] = []
        self.localizations: List[Dict[str, Any]] = []
        self.icon: Dict[str, Any] = {}

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
            TypeNode(type_=self.unique_quarter_type, kind="KIND_UNIQUE_QUARTER"),
        ]
        
        # Main unique quarter row with localization
        quarter_node = UniqueQuarterNode(
            unique_quarter_type=self.unique_quarter_type,
            name=loc_name,
            description=loc_description,
        )
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
        if self.icon:
            icon_node = IconDefinitionNode(id=self.unique_quarter_type)
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
        
        # ==== POPULATE _game_effects DATABASE ====
        if self.game_modifiers:
            self._game_effects = DatabaseNode()
            self._game_effects.game_modifiers = [
                GameModifierNode(
                    modifier_id=mod.get('modifier_id'),
                    target_type=mod.get('target_type', self.unique_quarter_type)
                )
                for mod in self.game_modifiers
            ]
        
        return self

    def bind(self, items: List[BaseBuilder]) -> "UniqueQuarterBuilder":
        """Bind ModifierBuilder items to this unique quarter."""
        from civ7_modding_tools.nodes import UniqueQuarterModifierNode, GameModifierNode
        
        for item in items:
            # Check for ModifierBuilder
            if hasattr(item, 'modifier') and hasattr(item, '_game_effects'):
                item.migrate()  # Ensure migration is done
                
                # Merge modifiers from game_effects
                if hasattr(item._game_effects, 'modifiers') and item._game_effects.game_modifiers:
                    if not self._game_effects:
                        self._game_effects = DatabaseNode()
                    if not self._game_effects.game_modifiers:
                        self._game_effects.game_modifiers = []
                    if not self._game_effects.game_modifiers:
                        self._game_effects.game_modifiers = []
                    
                    # Add modifiers for requirements/effects
                    self._game_effects.game_modifiers.extend(item._game_effects.game_modifiers)
                    
                    # Convert modifiers to game_modifiers (GameModifierNode)
                    for modifier in item._game_effects.game_modifiers:
                        modifier_id = getattr(modifier, 'id', None) or getattr(modifier, 'modifier_id', None)
                        if modifier_id:
                            self._game_effects.game_modifiers.append(
                                GameModifierNode(modifier_id=modifier_id)
                            )
                    
                    # Add unique quarter modifiers if not detached
                    if not getattr(item, 'is_detached', False):
                        if not self._always.unique_quarter_modifiers:
                            self._always.unique_quarter_modifiers = []
                        for modifier in item._game_effects.game_modifiers:
                            modifier_id = getattr(modifier, 'id', None) or getattr(modifier, 'modifier_id', None)
                            if modifier_id:
                                self._always.unique_quarter_modifiers.append(
                                    UniqueQuarterModifierNode(
                                        unique_quarter_type=self.unique_quarter_type,
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
            action_groups=[self.action_group_bundle.shell, self.action_group_bundle.always]
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
                action_group=self.action_group_bundle.current
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
    
    def build(self) -> list[BaseFile]:
        """Build import files."""
        from civ7_modding_tools.files import ImportFile
        
        files: list[BaseFile] = []
        
        if not self.source_path or not self.target_name:
            return files
        
        # Create import file
        import_file = ImportFile(
            path=self.target_directory,
            name=self.target_name,
            content=self.source_path
        )
        files.append(import_file)
        
        return files

