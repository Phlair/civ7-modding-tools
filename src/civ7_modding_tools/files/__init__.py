"""Base classes for file output generation."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union, TYPE_CHECKING, Any, Dict, List
import shutil
from civ7_modding_tools.nodes import BaseNode
from civ7_modding_tools.xml_builder import XmlBuilder

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
        
        Converts node hierarchy to attribute-based compact XML matching TypeScript format.
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
        
        # Serialize content to XML using new XmlBuilder
        xml_content = self._serialize_content(self.content)
        
        # Write to file
        with open(output_file, "w", encoding="UTF-8") as f:
            f.write(xml_content)

    def _build_element_recursive(self, data: dict) -> Optional[Any]:
        """
        Recursively build XML elements from jstoxml-format dict.
        
        Args:
            data: Dict with _name, _attrs, and optionally _content
            
        Returns:
            ET.Element or None
        """
        import xml.etree.ElementTree as ET
        
        if not isinstance(data, dict):
            return None
        
        elem_name = data.get('_name')
        if not elem_name:
            return None
        
        elem = ET.Element(elem_name)
        
        # Add attributes
        attrs = data.get('_attrs', {})
        for key, value in attrs.items():
            elem.set(key, str(value))
        
        # Add text content or child elements
        content = data.get('_content')
        if content:
            if isinstance(content, str):
                elem.text = content
            elif isinstance(content, list):
                for child_data in content:
                    child_elem = self._build_element_recursive(child_data)
                    if child_elem is not None:
                        elem.append(child_elem)
        
        return elem

    def _element_to_string(self, elem: Any, indent: str = '    ', level: int = 0) -> str:
        """
        Convert ET.Element to pretty-printed XML string.
        
        Args:
            elem: Element to convert
            indent: Indentation string
            level: Current indentation level
            
        Returns:
            Formatted XML string
        """
        # Build opening tag with attributes
        attrs_str = ""
        if elem.attrib:
            attrs_list = [f'{k}="{v}"' for k, v in elem.attrib.items()]
            attrs_str = " " + " ".join(attrs_list)
        
        current_indent = indent * level
        
        # Handle self-closing tags (no children, no text)
        if len(elem) == 0 and not (elem.text and elem.text.strip()):
            return f"{current_indent}<{elem.tag}{attrs_str}/>"
        
        # Has children or text
        result = f"{current_indent}<{elem.tag}{attrs_str}>"
        
        # Add text content if present
        if elem.text and elem.text.strip():
            result += elem.text.strip()
        
        # Add children
        if len(elem) > 0:
            result += "\n"
            for child in elem:
                result += self._element_to_string(child, indent, level + 1) + "\n"
            result += current_indent
        
        result += f"</{elem.tag}>"
        
        return result

    def _serialize_content(self, content: Union["DatabaseNode", list[BaseNode], BaseNode, dict, None]) -> str:
        """
        Serialize content to XML string using attribute-based format matching TypeScript.
        
        Priority order:
        1. DatabaseNode - Uses proper semantic table structure (PREFERRED)
        2. Dict - Pre-formatted jstoxml structure
        3. List of nodes - Flat table/row structure (legacy support)
        4. Single node - Single row structure
        
        Args:
            content: Content to serialize
            
        Returns:
            XML string with <?xml> declaration and footer comment
        """
        # Import here to avoid circular dependency
        from civ7_modding_tools.nodes.database import DatabaseNode
        from civ7_modding_tools.nodes.nodes import GameEffectNode, VisualRemapRootNode
        
        # Priority 1: DatabaseNode (proper semantic structure)
        if isinstance(content, DatabaseNode):
            xml_elem = content.to_xml_element()
            if not xml_elem:
                return ""
            
            # xml_elem is in jstoxml format: {'Database': {table1: [rows...], table2: [rows...]}}
            xml_str = XmlBuilder.build(
                xml_elem,
                header=True,
                indent='    ',
                footer_comment='<!-- generated with https://github.com/Phlair/civ7-modding-tools -->'
            )
            return xml_str
        
        # Priority 1.5: Special nodes that generate root-level XML (GameEffects, VisualRemaps)
        elif isinstance(content, (GameEffectNode, VisualRemapRootNode)):
            xml_elem = content.to_xml_element()
            if not xml_elem:
                return ""
            
            # GameEffectNode and VisualRemapRootNode return {_name, _attrs, _content} format
            # We need to wrap it properly for XmlBuilder
            # Convert to root-key format: {'GameEffects': _content}
            root_name = xml_elem['_name']
            root_attrs = xml_elem.get('_attrs', {})
            root_content = xml_elem.get('_content', [])
            
            # Build XML manually using ElementTree for these special cases
            import xml.etree.ElementTree as ET
            root = ET.Element(root_name)
            for key, value in root_attrs.items():
                root.set(key, str(value))
            
            # Add child elements
            for child_data in root_content:
                child_elem = self._build_element_recursive(child_data)
                if child_elem is not None:
                    root.append(child_elem)
            
            # Convert to string with custom pretty printing
            xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
            xml_lines.append(self._element_to_string(root, indent='    '))
            xml_lines.append('<!-- generated with https://github.com/Phlair/civ7-modding-tools -->')
            xml_str = '\n'.join(xml_lines)
            
            return xml_str
        
        # Priority 2: Pre-formatted dict in jstoxml format
        elif isinstance(content, dict):
            xml_str = XmlBuilder.build(
                content,
                header=True,
                indent='    ',
                footer_comment='<!-- generated with https://github.com/Phlair/civ7-modding-tools -->'
            )
            return xml_str
        
        # Priority 3: List of nodes (legacy support - convert to DatabaseNode format)
        elif isinstance(content, list):
            # Convert list of nodes to jstoxml format
            rows = []
            for item in content:
                if isinstance(item, BaseNode):
                    xml_elem = item.to_xml_element()
                    if xml_elem:
                        rows.append(xml_elem)
            
            if not rows:
                return ""
            
            # Wrap in Database structure
            xml_dict = {
                'Database': {
                    'Table': rows  # Array of {'_name': 'Row', '_attrs': {...}}
                }
            }
            
            xml_str = XmlBuilder.build(
                xml_dict,
                header=True,
                indent='    ',
                footer_comment='<!-- generated with https://github.com/Phlair/civ7-modding-tools -->'
            )
            return xml_str
        
        # Priority 4: Single node
        elif isinstance(content, BaseNode):
            xml_elem = content.to_xml_element()
            if not xml_elem:
                return ""
            
            # Wrap in Database structure
            xml_dict = {
                'Database': {
                    'Table': [xml_elem]  # Single element array
                }
            }
            
            xml_str = XmlBuilder.build(
                xml_dict,
                header=True,
                indent='    ',
                footer_comment='<!-- generated with https://github.com/Phlair/civ7-modding-tools -->'
            )
            return xml_str
        
        else:
            return ""


class JsFile(BaseFile):
    """
    JavaScript file generator for UI scripts.
    
    Generates JavaScript files that can be loaded via UIScripts in modinfo.
    Used for dynamic model placement and other UI-layer modifications.
    """

    def __init__(
        self,
        path: str = "/ui/",
        name: str = "script.js",
        content: str = "",
        action_group: Optional[dict] = None,
        action_groups: Optional[list] = None,
    ) -> None:
        """
        Initialize a JavaScript file.
        
        Args:
            path: Directory path relative to mod root (e.g., "/ui/")
            name: Filename (e.g., "improvement-models.js")
            content: JavaScript source code as string
            action_group: Single action group (dict with id, scope, criteria info)
            action_groups: List of action groups this file belongs to
        """
        super().__init__(path, name, content, action_group, action_groups)

    @property
    def is_empty(self) -> bool:
        """Check if this file is empty and should not be written."""
        return not self.content or (isinstance(self.content, str) and not self.content.strip())

    def write(self, dist: str) -> None:
        """
        Write JavaScript file to disk.
        
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
        
        # Write to file
        with open(output_file, "w", encoding="UTF-8") as f:
            f.write(self.content)


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
        action_group: Optional[dict] = None,
        action_groups: Optional[list] = None,
    ) -> None:
        """
        Initialize an import file.
        
        Args:
            path: Directory path in mod
            name: Output filename (without extension)
            content: Source file path to copy from
            action_group: Single action group this file belongs to
            action_groups: List of action groups this file belongs to
        """
        super().__init__(path, name, content, action_group, action_groups)
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
        output_file = output_dir / self.name
        
        # Copy file
        shutil.copy2(source, output_file)
