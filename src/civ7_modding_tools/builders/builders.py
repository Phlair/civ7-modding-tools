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
    ConstructibleNode,
    ConstructibleYieldChangeNode,
    CityNameNode,
    DatabaseNode,
    TypeNode,
    TraitNode,
    StartBiasBiomeNode,
    StartBiasTerrainNode,
    IconDefinitionNode,
    LegacyCivilizationNode,
    LegacyCivilizationTraitNode,
    EnglishTextNode,
)
from civ7_modding_tools.localizations import BaseLocalization

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

    def fill(self, payload: Dict[str, Any]) -> "CivilizationBuilder":
        """Fill civilization builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "CivilizationBuilder":
        """Migrate and populate all database variants."""
        if not self.civilization_type:
            return self
        
        # Generate trait types from civilization type if not provided
        if not self.trait:
            trait_base = self.civilization_type.replace('CIVILIZATION_', '')
            self.trait = {"trait_type": f"TRAIT_{trait_base}"}
        if not self.trait_ability:
            self.trait_ability = {"trait_type": f"{self.trait.get('trait_type', 'TRAIT')}_ABILITY"}
        
        trait_type = self.trait.get("trait_type", "TRAIT_CUSTOM")
        trait_ability_type = self.trait_ability.get("trait_type", "TRAIT_CUSTOM_ABILITY")
        
        # ==== POPULATE _current DATABASE ====
        # Types section
        self._current.types = [
            TypeNode(type_type=trait_type, kind="KIND_TRAIT"),
            TypeNode(type_type=trait_ability_type, kind="KIND_TRAIT"),
        ]
        
        # Traits section
        self._current.traits = [
            TraitNode(trait_type=trait_type, internal_only=True),
            TraitNode(trait_type=trait_ability_type, internal_only=True),
        ]
        
        # Civilizations section
        civ_node = CivilizationNode(civilization_type=self.civilization_type)
        for key, value in self.civilization.items():
            if key not in ['civilization_type']:  # Skip the key we already set
                setattr(civ_node, key, value)
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
        
        # Start biases - biome_type should be mapped to biome_type attribute
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
        
        # City names
        city_name_nodes = []
        for city_name in self.city_names:
            city_name_nodes.append(
                CityNameNode(
                    civilization_type=self.civilization_type,
                    city_name=city_name
                )
            )
        if city_name_nodes:
            self._current.city_names = city_name_nodes
        
        # ==== POPULATE _shell DATABASE ====
        shell_civ_node = CivilizationNode(civilization_type=self.civilization_type)
        for key, value in self.civilization.items():
            if key != 'civilization_type':
                setattr(shell_civ_node, key, value)
        self._shell.civilizations = [shell_civ_node]
        
        # ==== POPULATE _legacy DATABASE ====
        self._legacy.types = [
            TypeNode(type_type=self.civilization_type, kind="KIND_CIVILIZATION"),
            TypeNode(type_type=trait_type, kind="KIND_TRAIT"),
            TypeNode(type_type=trait_ability_type, kind="KIND_TRAIT"),
        ]
        
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
        self.unit_replace: Optional[Dict[str, Any]] = None
        self.unit_upgrade: Optional[Dict[str, Any]] = None
        self.unit_advisories: list[Dict[str, Any]] = []
        self.visual_remap: Optional[Dict[str, Any]] = None
        self.icon: Dict[str, Any] = {}
        self.localizations: list[Dict[str, Any]] = []

    def fill(self, payload: Dict[str, Any]) -> "UnitBuilder":
        """Fill unit builder from payload."""
        for key, value in payload.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def migrate(self) -> "UnitBuilder":
        """Migrate and populate all database variants."""
        if not self.unit_type:
            return self
        
        # ==== POPULATE _current DATABASE ====
        self._current.types = [
            TypeNode(type_type=self.unit_type, kind="KIND_UNIT"),
        ]
        
        # Unit definition
        unit_node = UnitNode(unit_type=self.unit_type)
        for key, value in self.unit.items():
            setattr(unit_node, key, value)
        self._current.units = [unit_node]
        
        # Unit stats
        if self.unit_stats:
            self._current.unit_stats = [
                UnitStatNode(unit_type=self.unit_type, **stat)
                for stat in self.unit_stats
            ]
        
        # Unit costs
        if self.unit_costs:
            self._current.unit_costs = [
                UnitCostNode(unit_type=self.unit_type, **cost)
                for cost in self.unit_costs
            ]
        
        # Unit replace
        if self.unit_replace:
            node_data = {"civUniqueUnitType": self.unit_type}
            node_data.update(self.unit_replace)
            # TODO: Add UnitReplaceNode when available
        
        # Unit upgrade
        if self.unit_upgrade:
            node_data = {"unit": self.unit_type}
            node_data.update(self.unit_upgrade)
            # TODO: Add UnitUpgradeNode when available
        
        # Unit advisories
        for advisory in self.unit_advisories:
            # TODO: Add UnitAdvisoryNode when available
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
                prefix = self.unit_type
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
        self._current = DatabaseNode()
        self._icons = DatabaseNode()
        self._localizations = DatabaseNode()
        self._game_effects: Optional[DatabaseNode] = None
        
        self.constructible_type: Optional[str] = None
        self.constructible: Dict[str, Any] = {}
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
        if not self.constructible_type:
            return self
        
        # ==== POPULATE _current DATABASE ====
        self._current.types = [
            TypeNode(type_type=self.constructible_type, kind="KIND_CONSTRUCTIBLE"),
        ]
        
        # Constructible definition
        const_node = ConstructibleNode(constructible_type=self.constructible_type)
        for key, value in self.constructible.items():
            setattr(const_node, key, value)
        self._current.constructibles = [const_node]
        
        # Yield changes
        if self.yield_changes:
            self._current.constructible_yield_changes = [
                ConstructibleYieldChangeNode(
                    constructible_type=self.constructible_type,
                    **yield_change
                )
                for yield_change in self.yield_changes
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
                prefix = self.constructible_type
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
        
        if localization_rows:
            self._localizations.english_text = localization_rows
        
        # ==== POPULATE _game_effects DATABASE ====
        if self.modifiers:
            self._game_effects = DatabaseNode()
            modifier_nodes = []
            for modifier in self.modifiers:
                mod_node = {
                    "modifier_id": modifier.get("modifier_id", f"MOD_{self.constructible_type}"),
                    "effect": modifier.get("effect"),
                }
                mod_node.update(modifier)
                modifier_nodes.append(mod_node)
            self._game_effects.modifiers = modifier_nodes
        
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
        self.progression_tree_type: Optional[str] = None
        self.progression_tree: Dict[str, Any] = {}
        self.progression_tree_nodes: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build progression tree files."""
        from civ7_modding_tools.nodes import (
            ProgressionTreeNode,
            ProgressionTreeNodeNode,
            ProgressionTreePrereqNode,
        )
        from civ7_modding_tools.nodes.database import DatabaseNode
        from civ7_modding_tools.utils import trim, kebab_case
        
        files: list[BaseFile] = []
        
        if not self.progression_tree_type:
            return files
        
        tree_nodes: list[BaseNode] = []
        effects_nodes: list[BaseNode] = []
        
        # Add main progression tree row
        tree_node = ProgressionTreeNode()
        tree_node.progression_tree_type = self.progression_tree_type
        for key, value in self.progression_tree.items():
            setattr(tree_node, key, value)
        tree_nodes.append(tree_node)
        
        # Add progression tree nodes and prerequisites
        for node_data in self.progression_tree_nodes:
            node_obj = ProgressionTreeNodeNode()
            node_obj.progression_tree_type = self.progression_tree_type
            for key, value in node_data.items():
                if key == "prerequisites":
                    continue  # Handle separately
                setattr(node_obj, key, value)
            tree_nodes.append(node_obj)
            
            # Add prerequisites for this node
            if "prerequisites" in node_data:
                for prereq in node_data["prerequisites"]:
                    prereq_node = ProgressionTreePrereqNode()
                    prereq_node.progression_tree_type = self.progression_tree_type
                    prereq_node.progression_tree_node_type = node_data.get("progression_tree_node_type")
                    for key, value in prereq.items():
                        setattr(prereq_node, key, value)
                    tree_nodes.append(prereq_node)
        
        # Create current database
        current_db = DatabaseNode()
        current_db.progression_trees = [tree_nodes[0]] if tree_nodes else []
        if len(tree_nodes) > 1:
            current_db.progression_tree_nodes = tree_nodes[1:]
        
        # Create effects database (for modifiers if any)
        effects_db = None
        # Note: modifiers would be added here if ProgressionTreeBuilder supported them
        
        # Generate path (trimmed + kebab-case)
        trimmed = trim(self.progression_tree_type)
        path = f"/progression-trees/{kebab_case(trimmed)}/"
        
        # Create current.xml file
        files.append(XmlFile(
            path=path,
            name="current.xml",
            content=current_db,
            action_group=self.action_group_bundle.current
        ))
        
        # Create game-effects.xml if there are modifiers
        if effects_db:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=effects_db,
                action_group=self.action_group_bundle.current
            ))
        
        return files


class ModifierBuilder(BaseBuilder):
    """Builder for creating game modifiers and effects."""
    
    def __init__(self) -> None:
        """Initialize modifier builder."""
        super().__init__()
        self.modifier_type: Optional[str] = None
        self.modifier: Dict[str, Any] = {}
        self.game_modifiers: List[Dict[str, Any]] = []
        self.requirements: List[Dict[str, Any]] = []
        self.arguments: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
        self.is_detached: bool = False  # Detached modifiers not bound to specific entity
    
    def build(self) -> list[BaseFile]:
        """Build modifier files."""
        from civ7_modding_tools.nodes import (
            ModifierNode,
            GameModifierNode,
            RequirementNode,
            ArgumentNode,
        )
        
        files: list[BaseFile] = []
        
        if not self.modifier_type:
            return files
        
        modifier_nodes: list[BaseNode] = []
        
        # Add main modifier row
        modifier_node = ModifierNode()
        modifier_node.modifier_type = self.modifier_type
        for key, value in self.modifier.items():
            setattr(modifier_node, key, value)
        modifier_nodes.append(modifier_node)
        
        # Add game modifiers
        for game_mod in self.game_modifiers:
            game_mod_node = GameModifierNode()
            game_mod_node.modifier_type = self.modifier_type
            for key, value in game_mod.items():
                setattr(game_mod_node, key, value)
            modifier_nodes.append(game_mod_node)
        
        # Add requirements
        for req in self.requirements:
            req_node = RequirementNode()
            req_node.modifier_type = self.modifier_type
            for key, value in req.items():
                setattr(req_node, key, value)
            modifier_nodes.append(req_node)
        
        # Add arguments
        for arg in self.arguments:
            arg_node = ArgumentNode()
            arg_node.modifier_type = self.modifier_type
            for key, value in arg.items():
                setattr(arg_node, key, value)
            modifier_nodes.append(arg_node)
        
        # Create modifier file
        modifier_file = XmlFile(
            path="/modifiers/" if self.is_detached else f"/modifiers/{self.modifier_type.lower()}/",
            name="modifier.xml",
            content=modifier_nodes
        )
        files.append(modifier_file)
        
        return files


class TraditionBuilder(BaseBuilder):
    """Builder for creating cultural traditions."""
    
    def __init__(self) -> None:
        """Initialize tradition builder."""
        super().__init__()
        self.tradition_type: Optional[str] = None
        self.tradition: Dict[str, Any] = {}
        self.tradition_modifiers: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build tradition files."""
        from civ7_modding_tools.nodes import (
            TraditionNode,
            TraditionModifierNode,
        )
        
        files: list[BaseFile] = []
        
        if not self.tradition_type:
            return files
        
        tradition_nodes: list[BaseNode] = []
        
        # Add main tradition row
        tradition_node = TraditionNode()
        tradition_node.tradition_type = self.tradition_type
        for key, value in self.tradition.items():
            setattr(tradition_node, key, value)
        tradition_nodes.append(tradition_node)
        
        # Add tradition modifiers
        for trad_mod in self.tradition_modifiers:
            trad_mod_node = TraditionModifierNode()
            trad_mod_node.tradition_type = self.tradition_type
            for key, value in trad_mod.items():
                setattr(trad_mod_node, key, value)
            tradition_nodes.append(trad_mod_node)
        
        # Create tradition file
        tradition_file = XmlFile(
            path=f"/traditions/{self.tradition_type.lower()}/",
            name="tradition.xml",
            content=tradition_nodes
        )
        files.append(tradition_file)
        
        return files


class UniqueQuarterBuilder(BaseBuilder):
    """Builder for creating unique quarters (district-specific buildings)."""
    
    def __init__(self) -> None:
        """Initialize unique quarter builder."""
        super().__init__()
        self.unique_quarter_type: Optional[str] = None
        self.unique_quarter: Dict[str, Any] = {}
        self.unique_quarter_modifiers: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build unique quarter files."""
        from civ7_modding_tools.nodes import (
            UniqueQuarterNode,
            UniqueQuarterModifierNode,
        )
        from civ7_modding_tools.nodes.database import DatabaseNode
        from civ7_modding_tools.utils import trim, kebab_case
        
        files: list[BaseFile] = []
        
        if not self.unique_quarter_type:
            return files
        
        # Split modifiers into always and game-effects databases
        always_nodes: list[BaseNode] = []
        effects_nodes: list[BaseNode] = []
        
        # Add main unique quarter row to always database
        quarter_node = UniqueQuarterNode()
        quarter_node.unique_quarter_type = self.unique_quarter_type
        for key, value in self.unique_quarter.items():
            setattr(quarter_node, key, value)
        always_nodes.append(quarter_node)
        
        # Add unique quarter modifiers to appropriate database
        for quarter_mod in self.unique_quarter_modifiers:
            quarter_mod_node = UniqueQuarterModifierNode()
            quarter_mod_node.unique_quarter_type = self.unique_quarter_type
            for key, value in quarter_mod.items():
                setattr(quarter_mod_node, key, value)
            effects_nodes.append(quarter_mod_node)
        
        # Create database wrappers
        always_db = DatabaseNode()
        always_db.unique_quarters = always_nodes
        
        effects_db = None
        if effects_nodes:
            effects_db = DatabaseNode()
            effects_db.unique_quarter_modifiers = effects_nodes
        
        # Generate path (trimmed + kebab-case)
        trimmed = trim(self.unique_quarter_type)
        path = f"/constructibles/{kebab_case(trimmed)}/"
        
        # Create files
        files.append(XmlFile(
            path=path,
            name="always.xml",
            content=always_db,
            action_group=self.action_group_bundle.always
        ))
        
        if effects_db:
            files.append(XmlFile(
                path=path,
                name="game-effects.xml",
                content=effects_db,
                action_group=self.action_group_bundle.current
            ))
        
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


class ProgressionTreeNodeBuilder(BaseBuilder):
    """Builder for creating progression tree nodes (tech/civic nodes)."""
    
    def __init__(self) -> None:
        """Initialize progression tree node builder."""
        super().__init__()
        self.progression_tree_node_type: Optional[str] = None
        self.progression_tree_node: Dict[str, Any] = {}
        self.progression_tree_node_unlocks: List[Dict[str, Any]] = []
        self.localizations: List[BaseLocalization] = []
    
    def build(self) -> list[BaseFile]:
        """Build progression tree node files."""
        from civ7_modding_tools.nodes import (
            ProgressionTreeNodeNode,
            ProgressionTreeNodeUnlockNode,
        )
        
        files: list[BaseFile] = []
        
        if not self.progression_tree_node_type:
            return files
        
        node_nodes: list[BaseNode] = []
        
        # Add main progression tree node row
        node = ProgressionTreeNodeNode()
        node.progression_tree_node_type = self.progression_tree_node_type
        for key, value in self.progression_tree_node.items():
            setattr(node, key, value)
        node_nodes.append(node)
        
        # Add node unlocks
        for unlock in self.progression_tree_node_unlocks:
            unlock_node = ProgressionTreeNodeUnlockNode()
            unlock_node.progression_tree_node_type = self.progression_tree_node_type
            for key, value in unlock.items():
                setattr(unlock_node, key, value)
            node_nodes.append(unlock_node)
        
        # Create progression tree node file
        node_file = XmlFile(
            path=f"/progression-tree-nodes/{self.progression_tree_node_type.lower()}/",
            name="node.xml",
            content=node_nodes
        )
        files.append(node_file)
        
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
