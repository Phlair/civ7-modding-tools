"""Main Mod orchestrator for building Civilization 7 mods."""

from pathlib import Path
from typing import TYPE_CHECKING, Optional
from uuid import uuid4
import xmltodict
from civ7_modding_tools.files import BaseFile, XmlFile
from civ7_modding_tools.nodes.action_groups import ActionGroupNode, CriteriaNode

if TYPE_CHECKING:
    from civ7_modding_tools.builders.builders import BaseBuilder


class ActionGroupBundle:
    """
    Represents a bundling of action groups for a mod entity.
    
    Action groups control when mod content is loaded (e.g., specific ages).
    This class manages the relationship between entities and their loading criteria,
    including ActionGroupNode instances for shell, always, current, and persist groups.
    """

    def __init__(
        self,
        action_group_id: Optional[str] = None,
        criteria_id: Optional[str] = None,
    ) -> None:
        """
        Initialize action group bundle.
        
        Args:
            action_group_id: The action group identifier (e.g., "AGE_ANTIQUITY")
            criteria_id: The criteria for loading (optional)
        """
        self.action_group_id = action_group_id or "ALWAYS"
        self.criteria_id = criteria_id or str(uuid4())
        
        # Create ActionGroupNode instances for each scope
        self.shell = ActionGroupNode({
            "id": f"SHELL_{self.action_group_id}",
            "scope": "shell",
            "criteria": CriteriaNode({"id": f"CRITERIA_SHELL_{self.criteria_id}"}),
        })
        
        self.always = ActionGroupNode({
            "id": "ALWAYS",
            "scope": "game",
            "criteria": CriteriaNode({"id": "CRITERIA_ALWAYS"}),
        })
        
        self.current = ActionGroupNode({
            "id": self.action_group_id,
            "scope": "game",
            "criteria": CriteriaNode({
                "id": f"CRITERIA_{self.action_group_id}",
                "ages": [self.action_group_id] if (self.action_group_id and not self.action_group_id.startswith("AGE_")) else [self.action_group_id] if self.action_group_id else [],
            }),
        })
        
        self.persist = ActionGroupNode({
            "id": f"PERSIST_{self.action_group_id}",
            "scope": "game",
            "criteria": CriteriaNode({"id": f"CRITERIA_PERSIST_{self.criteria_id}"}),
        })

    def __repr__(self) -> str:
        """String representation."""
        return f"ActionGroupBundle(action_group_id={self.action_group_id!r})"


class Mod:
    """
    Main orchestrator class for creating Civilization 7 mods.
    
    Coordinates builders, files, and mod metadata generation.
    Produces .modinfo file and all mod content files.
    """

    def __init__(
        self,
        mod_id: str | dict[str, Any] = "my-mod",
        version: str = "1.0.0",
        name: str = "My Mod",
        description: str = "",
        authors: str = "",
        affects_saved_games: bool = True,
    ) -> None:
        """
        Initialize a mod.
        
        Can be called with:
        - Mod(mod_id="my-mod", version="1.0", ...) - keyword arguments
        - Mod({"id": "my-mod", "version": "1.0", ...}) - dictionary
        
        Args:
            mod_id: Unique identifier (used in filenames and .modinfo) or dict of properties
            version: Semantic version string
            name: Human-readable mod name
            description: Mod description
            authors: Comma-separated author list
            affects_saved_games: Whether mod affects saved games
        """
        # Handle dictionary initialization
        if isinstance(mod_id, dict):
            config = mod_id
            self.mod_id = config.get("id", "my-mod")
            self.version = config.get("version", "1.0.0")
            self.name = config.get("name", "My Mod")
            self.description = config.get("description", "")
            self.authors = config.get("authors", "")
            self.affects_saved_games = config.get("affects_saved_games", True)
        else:
            self.mod_id = mod_id
            self.version = version
            self.name = name
            self.description = description
            self.authors = authors
            self.affects_saved_games = affects_saved_games
        
        self.builders: list["BaseBuilder"] = []
        self.files: list[BaseFile] = []
        self.action_groups: dict[str, dict] = {}

    def add(self, builder: "BaseBuilder | list[BaseBuilder]") -> "Mod":
        """
        Add one or more builders to the mod.
        
        Args:
            builder: Single builder or list of builders
            
        Returns:
            Self for fluent API chaining
        """
        if isinstance(builder, list):
            self.builders.extend(builder)
        else:
            self.builders.append(builder)
        return self

    def add_files(self, file: BaseFile | list[BaseFile]) -> "Mod":
        """
        Add one or more import files to the mod.
        
        Args:
            file: Single file or list of files
            
        Returns:
            Self for fluent API chaining
        """
        if isinstance(file, list):
            self.files.extend(file)
        else:
            self.files.append(file)
        return self

    def build(self, dist: str = "./dist", clear: bool = True) -> None:
        """
        Build the mod and write files to disk.
        
        Processes all builders to generate files, creates .modinfo,
        and writes everything to the distribution directory.
        
        Args:
            dist: Output directory path
            clear: Whether to clear existing dist directory first
        """
        dist_path = Path(dist)
        
        # Clear existing directory if requested
        if clear and dist_path.exists():
            import shutil
            shutil.rmtree(dist_path)
        
        # Create distribution directory
        dist_path.mkdir(parents=True, exist_ok=True)
        
        # Build all builders to generate files
        builder_files = []
        for builder in self.builders:
            if hasattr(builder, "build"):
                generated_files = builder.build()
                if isinstance(generated_files, list):
                    builder_files.extend(generated_files)
                else:
                    builder_files.append(generated_files)
        
        # Combine all files
        all_files = builder_files + self.files
        
        # Filter empty files
        all_files = [f for f in all_files if not f.is_empty]
        
        # Generate .modinfo
        modinfo_content = self._generate_modinfo(all_files)
        modinfo_file = dist_path / f"{self.mod_id}.modinfo"
        
        with open(modinfo_file, "w", encoding="utf-8") as f:
            f.write(modinfo_content)
        
        # Write all generated files
        for file in all_files:
            file.write(str(dist_path))

    def _generate_modinfo(self, files: list[BaseFile]) -> str:
        """
        Generate .modinfo XML content.
        
        Creates the mod metadata file with references to all generated files.
        
        Args:
            files: List of generated files
            
        Returns:
            XML string for .modinfo file
        """
        # Build mod metadata structure with proper attributes
        properties_list = []
        if self.name:
            properties_list.append({"@name": "Name", "@value": self.name})
        if self.description:
            properties_list.append({"@name": "Description", "@value": self.description})
        if self.authors:
            properties_list.append({"@name": "Authors", "@value": self.authors})
        
        properties_list.append({
            "@name": "AffectsSavedGames",
            "@value": "true" if self.affects_saved_games else "false"
        })
        
        # Build files list
        files_list = []
        for file in files:
            files_list.append({"@path": file.mod_info_path})
        
        # Create mod structure
        mod_dict = {
            "@id": self.mod_id,
            "@version": self.version,
        }
        
        if properties_list:
            mod_dict["Properties"] = {"Property": properties_list}
        
        if files_list:
            mod_dict["Files"] = {"File": files_list}
        
        # Wrap in Mod element
        output = {"Mod": mod_dict}
        
        # Generate XML
        xml_str = xmltodict.unparse(output, pretty=True, indent="    ")
        
        # xmltodict.unparse already includes XML declaration, so don't add it again
        return xml_str

    def __repr__(self) -> str:
        """String representation."""
        return f"Mod(id={self.mod_id!r}, version={self.version!r})"
