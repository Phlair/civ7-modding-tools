"""Base classes for file output generation."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING
import shutil
import xmltodict
from civ7_modding_tools.nodes import BaseNode

if TYPE_CHECKING:
    from civ7_modding_tools.nodes import DatabaseNode


class BaseFile(ABC):
    """
    Abstract base class for output files.
    
    Represents a physical file that will be written to disk.
    Subclasses implement specific file formats (XML, imports, etc).
    """

    def __init__(
        self,
        path: str = "/",
        name: str = "file.txt",
        content: Union[list[BaseNode], BaseNode, dict, str, None] = None,
        action_group: Optional[dict] = None,
        action_groups: Optional[list] = None,
    ) -> None:
        """
        Initialize a base file.
        
        Args:
            path: Directory path relative to mod root (e.g., "/civilizations/rome/")
            name: Filename (e.g., "current.xml")
            content: File content (format depends on subclass)
            action_group: Single action group (dict with id, scope, criteria info)
            action_groups: List of action groups this file belongs to
        """
        self.path = path
        self.name = name
        self.content = content
        self.action_groups: list[dict] = []
        self.action_group_actions: list[str] = []
        
        # Handle action group assignment
        if action_group:
            self.action_groups.append(action_group)
        if action_groups:
            self.action_groups.extend(action_groups)

    @property
    def is_empty(self) -> bool:
        """
        Check if this file is empty and should not be written.
        
        Returns:
            True if file has no content
        """
        return self.content is None

    @property
    def mod_info_path(self) -> str:
        """
        Get the path for referencing this file in .modinfo.
        
        Returns:
            Relative path from mod root (e.g., "civilizations/rome/current.xml")
        """
        path = self.path.strip("/")
        return f"{path}/{self.name}" if path else self.name

    @abstractmethod
    def write(self, dist: str) -> None:
        """
        Write this file to disk.
        
        Args:
            dist: Absolute path to distribution directory
        """
        pass

    def __repr__(self) -> str:
        """String representation of the file."""
        return f"{self.__class__.__name__}(path={self.path!r}, name={self.name!r})"


class XmlFile(BaseFile):
    """
    XML file generator for Civilization 7 mod files.
    
    Converts node hierarchies to XML using xmltodict.
    Each file typically contains a single root element with child rows.
    """

    def __init__(
        self,
        path: str = "/",
        name: str = "file.xml",
        content: Union[list[BaseNode], BaseNode, dict, None] = None,
        action_group: Optional[dict] = None,
        action_groups: Optional[list] = None,
    ) -> None:
        """
        Initialize an XML file.
        
        Args:
            path: Directory path
            name: XML filename
            content: List of BaseNode objects or nested structure
            action_group: Single action group this file belongs to
            action_groups: List of action groups this file belongs to
        """
        super().__init__(path, name, content, action_group, action_groups)

    def write(self, dist: str) -> None:
        """
        Write XML file to disk.
        
        Converts node hierarchy to XML and writes with proper formatting.
        Creates directory structure as needed.
        
        Args:
            dist: Absolute path to distribution directory
        """
        if self.is_empty:
            return
        
        # Build output directory
        output_dir = Path(dist) / self.path.strip("/")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Build output file path
        output_file = output_dir / self.name
        
        # Serialize content to XML
        xml_content = self._serialize_content(self.content)
        
        # Write to file with XML declaration and formatting
        with open(output_file, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            # Strip any existing XML declarations from xmltodict
            lines = xml_content.split('\n')
            if lines and lines[0].startswith('<?xml'):
                xml_content = '\n'.join(lines[1:])
            f.write(xml_content)

    def _serialize_content(self, content: Union["DatabaseNode", list[BaseNode], BaseNode, dict, None]) -> str:
        """
        Serialize content to XML string.
        
        Priority order:
        1. DatabaseNode - Uses proper semantic table structure (PREFERRED)
        2. List of nodes - Flat Table/Row structure (legacy support)
        3. Single node - Single row structure
        4. Dict - Custom structure
        
        Args:
            content: Content to serialize
            
        Returns:
            XML string
        """
        # Import here to avoid circular dependency
        from civ7_modding_tools.nodes.database import DatabaseNode
        
        # Priority 1: DatabaseNode (proper semantic structure)
        if isinstance(content, DatabaseNode):
            xml_elem = content.to_xml_element()
            if not xml_elem:
                return ""
            
            xml_str = xmltodict.unparse(
                xml_elem,
                pretty=True,
                indent="    "
            )
            return xml_str
        
        # Priority 2: List of nodes (legacy support - flat structure)
        elif isinstance(content, list):
            # Convert list of nodes to Database structure
            rows = []
            for item in content:
                if isinstance(item, BaseNode):
                    xml_elem = item.to_xml_element()
                    if xml_elem:
                        # Extract the row content from {_name: attributes}
                        rows.append(list(xml_elem.values())[0])
                elif isinstance(item, dict):
                    rows.append(item)
            
            if not rows:
                return ""
            
            # Wrap rows in Database -> Table -> Row structure (flat)
            # Each row becomes a Row element
            row_elements = [{"@" + k: v for k, v in row.items()} for row in rows]
            
            xml_dict = {
                "Database": {
                    "Table": {
                        "Row": row_elements
                    }
                }
            }
            
            xml_str = xmltodict.unparse(
                xml_dict,
                pretty=True,
                indent="    "
            )
            return xml_str
        
        elif isinstance(content, BaseNode):
            # Single node
            xml_elem = content.to_xml_element()
            if not xml_elem:
                return ""
            
            # Extract row content
            row_content = list(xml_elem.values())[0]
            xml_dict = {
                "Database": {
                    "Table": {
                        "Row": {"@" + k: v for k, v in row_content.items()}
                    }
                }
            }
            xml_str = xmltodict.unparse(
                xml_dict,
                pretty=True,
                indent="    "
            )
            return xml_str
        
        elif isinstance(content, dict):
            # Already a dictionary structure
            xml_str = xmltodict.unparse(
                content,
                pretty=True,
                indent="    "
            )
            return xml_str
        
        else:
            return ""


class ImportFile(BaseFile):
    """
    Import file handler for copying assets into the mod.
    
    Handles images, SQL scripts, and other files that need to be
    included in the mod but not generated.
    """

    def __init__(
        self,
        path: str = "/",
        name: str = "file",
        content: str = "",
    ) -> None:
        """
        Initialize an import file.
        
        Args:
            path: Directory path in mod
            name: Output filename (without extension)
            content: Source file path to copy from
        """
        super().__init__(path, name, content)
        self.source_path = content  # content is the source file path

    @property
    def is_empty(self) -> bool:
        """Check if source file exists."""
        if not self.source_path:
            return True
        return not Path(self.source_path).exists()

    def write(self, dist: str) -> None:
        """
        Copy import file to mod directory.
        
        Args:
            dist: Absolute path to distribution directory
            
        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        source = Path(self.source_path)
        
        # Always check source exists
        if not source.exists():
            raise FileNotFoundError(f"Import source not found: {source}")
        
        # Build output path
        output_dir = Path(dist) / self.path.strip("/")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / source.name
        
        # Copy file
        shutil.copy2(source, output_file)
