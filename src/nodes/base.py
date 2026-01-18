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



    def to_xml_element(self) -> Optional[Dict[str, Any]]:
        """
        Convert this node to an XML element dictionary compatible with jstoxml format.
        
        Properties are serialized as XML attributes with the following rules:
        - Properties starting with '_' are excluded
        - snake_case properties are converted to PascalCase
        - None, empty string, and False values are omitted
        - Boolean True converted to "true", False is omitted
        - All other values are stringified
        
        Returns:
            Dictionary with _name and _attrs keys matching TypeScript jstoxml format,
            or None if node is empty
            
        Example:
            {'_name': 'Row', '_attrs': {'Type': 'VALUE', 'Kind': 'KIND_TYPE'}}
        """
        attributes: Dict[str, str] = {}
        
        # Get all model fields, excluding those marked as exclude=True
        model_data = self.model_dump(exclude_none=False, exclude_unset=False)
        
        for key, value in model_data.items():
            # Skip private properties (those starting with '_')
            if key.startswith("_"):
                continue
            
            # Skip None and empty string values
            if value is None or value == "":
                continue
            
            # Skip False boolean values (only True is serialized)
            if isinstance(value, bool) and not value:
                continue
            
            # Convert boolean values to strings
            if isinstance(value, bool):
                value = "true"  # We've already filtered out False above
            
            # Convert property name from snake_case to PascalCase
            # This matches TypeScript lodash.startCase behavior
            if "_" in key:
                # Split by underscore and capitalize each part
                parts = key.split("_")
                # PascalCase: capitalize each part (but skip empty trailing parts from trailing underscore)
                # Handle special case: 'type_' becomes 'Type' not 'Type' + empty
                xml_key = "".join(p.capitalize() for p in parts if p)
            else:
                # Already camelCase or single word - just capitalize first letter
                xml_key = key[0].upper() + key[1:] if key else key
            
            # Stringify all values
            attributes[xml_key] = str(value)
        
        # Return None if no attributes (empty node)
        if not attributes:
            return None
        
        # Return in jstoxml-compatible format
        # This matches TypeScript: {_name: this._name, _attrs: this.getAttributes()}
        return {
            '_name': self._name,
            '_attrs': attributes
        }

    def __repr__(self) -> str:
        """String representation of the node."""
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({attrs})"
