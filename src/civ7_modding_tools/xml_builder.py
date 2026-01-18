"""Custom XML builder for attribute-based XML generation matching TypeScript output."""

from typing import Any, Dict, List, Union, Optional
import xml.etree.ElementTree as ET


class XmlBuilder:
    """
    Custom XML builder that generates attribute-based compact XML.
    
    Matches TypeScript jstoxml output format with attributes instead of child elements.
    Implements proper table grouping and formatting.
    """
    
    @staticmethod
    def build(data: Union[Dict[str, Any], List[Dict[str, Any]]], 
              header: bool = True,
              indent: str = '    ',
              footer_comment: Optional[str] = None) -> str:
        """
        Build XML string from jstoxml-format dictionary structure.
        
        Expected format:
            {'Database': {'Types': [{'_name': 'Row', '_attrs': {...}}], 'Units': [...]}}
        
        Args:
            data: Dictionary with root element and nested structure
            header: Whether to include XML declaration
            indent: Indentation string (default 4 spaces)
            footer_comment: Optional comment to append at end of file
            
        Returns:
            Formatted XML string
        """
        if not data:
            return ""
        
        # Create root element
        root = XmlBuilder._dict_to_element(data)
        
        # Convert to string with proper formatting
        xml_str = XmlBuilder._element_to_string(root, indent)
        
        # Add header
        if header:
            xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
        
        # Add footer comment if provided
        if footer_comment:
            xml_str += '\n' + footer_comment
        
        return xml_str
    
    @staticmethod
    def _element_to_string(element: ET.Element, indent: str = '    ', level: int = 0) -> str:
        """
        Convert Element to pretty-printed XML string.
        
        Args:
            element: Element to convert
            indent: Indentation string
            level: Current indentation level
            
        Returns:
            Formatted XML string
        """
        # Build opening tag with attributes
        attrs_str = ""
        if element.attrib:
            attrs_list = [f'{k}="{v}"' for k, v in element.attrib.items()]
            attrs_str = " " + " ".join(attrs_list)
        
        current_indent = indent * level
        
        # Handle self-closing tags (no children, no text)
        if len(element) == 0 and not (element.text and element.text.strip()):
            return f"{current_indent}<{element.tag}{attrs_str}/>"
        
        # Has children or text
        result = f"{current_indent}<{element.tag}{attrs_str}>"
        
        # Add text content if present
        if element.text and element.text.strip():
            result += element.text.strip()
        
        # Add children
        if len(element) > 0:
            result += "\n"
            for child in element:
                result += XmlBuilder._element_to_string(child, indent, level + 1) + "\n"
            result += current_indent
        
        result += f"</{element.tag}>"
        
        return result
    
    @staticmethod
    def _dict_to_element(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> ET.Element:
        """
        Convert jstoxml-format dictionary to XML Element.
        
        Expected formats:
        1. Root element: {'Database': {...}}
        2. Table with rows: {'Types': [{'_name': 'Row', '_attrs': {...}}, ...]}
        3. Single row: {'_name': 'Row', '_attrs': {'Type': 'VALUE'}}
        
        Args:
            data: jstoxml-format dictionary or list
            
        Returns:
            XML Element tree
        """
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")
        
        # Handle root element (should have single key for root tag)
        root_keys = list(data.keys())
        
        # Check if this is a node element (has _name and _attrs)
        if '_name' in data and '_attrs' in data:
            # This is a single node element
            elem = ET.Element(data['_name'])
            for key, value in data['_attrs'].items():
                elem.set(key, str(value))
            return elem
        
        # This is a container element - find root tag
        if len(root_keys) == 1:
            root_tag = root_keys[0]
            root_content = data[root_tag]
            root = ET.Element(root_tag)
            
            # Process root content
            if isinstance(root_content, dict):
                # Root content is a dictionary of child elements/tables
                for table_name, table_content in root_content.items():
                    if isinstance(table_content, list):
                        # Table with multiple rows
                        table_elem = ET.SubElement(root, table_name)
                        for row in table_content:
                            row_elem = XmlBuilder._create_row_element(row)
                            table_elem.append(row_elem)
                    elif isinstance(table_content, dict):
                        # Single child or nested structure
                        if '_name' in table_content and '_attrs' in table_content:
                            # Single row element
                            table_elem = ET.SubElement(root, table_name)
                            row_elem = XmlBuilder._create_row_element(table_content)
                            table_elem.append(row_elem)
                        else:
                            # Nested structure
                            child_elem = XmlBuilder._dict_to_element({table_name: table_content})
                            root.append(child_elem)
            
            return root
        else:
            raise ValueError(f"Root should have single key, got {root_keys}")
    
    @staticmethod
    def _create_row_element(row_data: Dict[str, Any]) -> ET.Element:
        """
        Create a Row element from jstoxml row data.
        
        Expected format: {'_name': 'Row', '_attrs': {'Type': 'VALUE', ...}}
        
        Args:
            row_data: Row data dictionary
            
        Returns:
            XML Element for the row
        """
        if not isinstance(row_data, dict):
            raise ValueError(f"Expected dict for row, got {type(row_data)}")
        
        # Get element name (_name) and attributes (_attrs)
        elem_name = row_data.get('_name', 'Row')
        attrs = row_data.get('_attrs', {})
        
        # Create element
        elem = ET.Element(elem_name)
        
        # Add attributes
        for key, value in attrs.items():
            elem.set(key, str(value))
        
        return elem
