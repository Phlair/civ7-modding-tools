"""Base node class for XML element representation."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, PrivateAttr
from civ7_modding_tools.utils import camel_to_pascal


class BaseNode(BaseModel):
    """
    Abstract base class representing an XML element.
    
    All XML elements in the generated files extend this class.
    Properties are automatically converted to XML attributes via camelCase -> PascalCase.
    """

    model_config = ConfigDict(extra="allow")
    
    # Private attributes (not included in model_dump)
    _name: str = PrivateAttr(default="Row")
    _insert_or_ignore: bool = PrivateAttr(default=False)

    def fill(self, payload: Dict[str, Any]) -> "BaseNode":
        """
        Fill node properties from a dictionary payload.
        
        Uses pydantic's model_validate to safely set properties.
        
        Args:
            payload: Dictionary of properties to set
            
        Returns:
            Self for fluent API chaining
        """
        for key, value in payload.items():
            setattr(self, key, value)
        return self

    def insert_or_ignore(self) -> "BaseNode":
        """
        Mark this node as INSERT OR IGNORE.
        
        Used in database operations to skip duplicates.
        
        Returns:
            Self for fluent API chaining
        """
        self._insert_or_ignore = True
        return self

    def to_xml_element(self) -> Optional[Dict[str, Any]]:
        """
        Convert this node to an XML element dictionary compatible with xmltodict.
        
        Properties are serialized as XML attributes with the following rules:
        - Properties starting with '_' are excluded
        - camelCase properties are converted to PascalCase
        - None, empty string, and False values are omitted
        - All other values are stringified
        
        Returns:
            Dictionary suitable for xmltodict serialization, or None if node is empty
        """
        attributes: Dict[str, str] = {}
        
        # Get all model fields, excluding those marked as exclude=True
        model_data = self.model_dump(exclude_none=False, exclude_unset=False)
        
        for key, value in model_data.items():
            # Skip private properties (those starting with '_')
            if key.startswith("_"):
                continue
            
            # Skip None, empty string, and False values
            if value is None or value == "" or value is False:
                continue
            
            # Convert boolean True to string
            if value is True:
                value = "true"
            
            # Convert property name from camelCase/snake_case to PascalCase
            # Handle snake_case by converting back to camelCase first if needed
            if "_" in key:
                # Convert snake_case to camelCase
                parts = key.split("_")
                camel_key = parts[0] + "".join(p.capitalize() for p in parts[1:])
            else:
                camel_key = key
            
            xml_key = camel_to_pascal(camel_key)
            
            # Stringify all values
            attributes[xml_key] = str(value)
        
        # Return None if no attributes (empty node)
        if not attributes:
            return None
        
        # Return as xmltodict-compatible element
        return {self._name: attributes}

    def __repr__(self) -> str:
        """String representation of the node."""
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({attrs})"
