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
    ConstructibleNode,
    CityNameNode,
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
    """Builder for creating civilizations."""
    
    def __init__(self) -> None:
        """Initialize civilization builder."""
        super().__init__()
        self.civilization_type: Optional[str] = None
        self.civilization: Dict[str, Any] = {}
        self.civilization_traits: List[str] = []
        self.localizations: List[BaseLocalization] = []
        self.start_bias_biomes: List[Dict[str, Any]] = []
        self.start_bias_terrains: List[Dict[str, Any]] = []
        self.city_names: List[str] = []

    def build(self) -> list[BaseFile]:
        """Build civilization files."""
        files: list[BaseFile] = []
        
        if not self.civilization_type:
            return files
        
        # Build civilization data file
        civ_nodes: list[BaseNode] = []
        
        # Add civilization row
        civ_node = CivilizationNode()
        civ_node.civilization_type = self.civilization_type
        for key, value in self.civilization.items():
            setattr(civ_node, key, value)
        civ_nodes.append(civ_node)
        
        # Add traits
        for trait in self.civilization_traits:
            trait_node = CivilizationTraitNode()
            trait_node.civilization_type = self.civilization_type
            trait_node.trait_type = trait
            civ_nodes.append(trait_node)
        
        # Create civilization file
        civ_file = XmlFile(
            path=f"/civilizations/{self.civilization_type.lower()}/",
            name="current.xml",
            content=civ_nodes
        )
        files.append(civ_file)
        
        # Add city names localization if provided
        if self.city_names:
            city_name_nodes: list[BaseNode] = []
            for city_name in self.city_names:
                city_node = CityNameNode()
                city_node.civilization_type = self.civilization_type
                city_node.city_name = city_name
                city_name_nodes.append(city_node)
            
            city_file = XmlFile(
                path=f"/civilizations/{self.civilization_type.lower()}/",
                name="city_names.xml",
                content=city_name_nodes
            )
            files.append(city_file)
        
        return files


class UnitBuilder(BaseBuilder):
    """Builder for creating units."""
    
    def __init__(self) -> None:
        """Initialize unit builder."""
        super().__init__()
        self.unit_type: Optional[str] = None
        self.unit: Dict[str, Any] = {}
        self.unit_stats: list[Dict[str, Any]] = []
        self.unit_costs: list[Dict[str, Any]] = []
        self.localizations: list[BaseLocalization] = []

    def build(self) -> list[BaseFile]:
        """Build unit files."""
        files: list[BaseFile] = []
        
        if not self.unit_type:
            return files
        
        # Build unit data file
        unit_nodes: list[BaseNode] = []
        
        # Add unit row
        unit_node = UnitNode()
        unit_node.unit_type = self.unit_type
        for key, value in self.unit.items():
            setattr(unit_node, key, value)
        unit_nodes.append(unit_node)
        
        # Add unit stats
        for stat in self.unit_stats:
            stat_node = BaseNode()
            stat_node.unit_type = self.unit_type
            for key, value in stat.items():
                setattr(stat_node, key, value)
            unit_nodes.append(stat_node)
        
        # Add unit costs
        for cost in self.unit_costs:
            cost_node = BaseNode()
            cost_node.unit_type = self.unit_type
            for key, value in cost.items():
                setattr(cost_node, key, value)
            unit_nodes.append(cost_node)
        
        # Create unit file
        unit_file = XmlFile(
            path=f"/units/{self.unit_type.lower()}/",
            name="unit.xml",
            content=unit_nodes
        )
        files.append(unit_file)
        
        return files


class ConstructibleBuilder(BaseBuilder):
    """Builder for creating buildings and improvements."""
    
    def __init__(self) -> None:
        """Initialize constructible builder."""
        super().__init__()
        self.constructible_type: Optional[str] = None
        self.constructible: Dict[str, Any] = {}
        self.yield_changes: list[Dict[str, Any]] = []
        self.localizations: list[BaseLocalization] = []

    def build(self) -> list[BaseFile]:
        """Build constructible files."""
        files: list[BaseFile] = []
        
        if not self.constructible_type:
            return files
        
        # Build constructible data file
        const_nodes: list[BaseNode] = []
        
        # Add constructible row
        const_node = ConstructibleNode()
        const_node.constructible_type = self.constructible_type
        for key, value in self.constructible.items():
            setattr(const_node, key, value)
        const_nodes.append(const_node)
        
        # Add yield changes
        for yield_change in self.yield_changes:
            yield_node = BaseNode()
            yield_node.constructible_type = self.constructible_type
            for key, value in yield_change.items():
                setattr(yield_node, key, value)
            const_nodes.append(yield_node)
        
        # Create constructible file
        const_file = XmlFile(
            path=f"/constructibles/{self.constructible_type.lower()}/",
            name="constructible.xml",
            content=const_nodes
        )
        files.append(const_file)
        
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
        
        files: list[BaseFile] = []
        
        if not self.progression_tree_type:
            return files
        
        tree_nodes: list[BaseNode] = []
        
        # Add main progression tree row
        tree_node = ProgressionTreeNode()
        tree_node.progression_tree_type = self.progression_tree_type
        for key, value in self.progression_tree.items():
            setattr(tree_node, key, value)
        tree_nodes.append(tree_node)
        
        # Add progression tree nodes
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
        
        # Create tree file
        tree_file = XmlFile(
            path=f"/progression-trees/{self.progression_tree_type.lower()}/",
            name="tree.xml",
            content=tree_nodes
        )
        files.append(tree_file)
        
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
        
        files: list[BaseFile] = []
        
        if not self.unique_quarter_type:
            return files
        
        quarter_nodes: list[BaseNode] = []
        
        # Add main unique quarter row
        quarter_node = UniqueQuarterNode()
        quarter_node.unique_quarter_type = self.unique_quarter_type
        for key, value in self.unique_quarter.items():
            setattr(quarter_node, key, value)
        quarter_nodes.append(quarter_node)
        
        # Add unique quarter modifiers
        for quarter_mod in self.unique_quarter_modifiers:
            quarter_mod_node = UniqueQuarterModifierNode()
            quarter_mod_node.unique_quarter_type = self.unique_quarter_type
            for key, value in quarter_mod.items():
                setattr(quarter_mod_node, key, value)
            quarter_nodes.append(quarter_mod_node)
        
        # Create unique quarter file
        quarter_file = XmlFile(
            path=f"/unique-quarters/{self.unique_quarter_type.lower()}/",
            name="quarter.xml",
            content=quarter_nodes
        )
        files.append(quarter_file)
        
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
