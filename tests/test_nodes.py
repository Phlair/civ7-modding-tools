"""Tests for base node functionality."""

import pytest
from civ7_modding_tools.nodes import BaseNode
from civ7_modding_tools.utils import camel_to_pascal


def test_base_node_creation():
    """Test creating a basic node."""
    node = BaseNode()
    assert node._name == "Row"
    assert node._insert_or_ignore is False


def test_base_node_fill():
    """Test fill() method for fluent API."""
    node = BaseNode()
    result = node.fill({"test_prop": "value", "another": 42})
    
    # Should return self
    assert result is node
    # Should set properties
    assert node.test_prop == "value"
    assert node.another == 42


def test_base_node_to_xml_element():
    """Test conversion to XML element dict."""
    node = BaseNode()
    node.civilization_type = "CIVILIZATION_ROME"
    node.base_tourism = 10
    node.legacy_modifier = True
    
    xml_elem = node.to_xml_element()
    
    assert xml_elem is not None
    assert "Row" in xml_elem
    attrs = xml_elem["Row"]
    
    # Check snake_case -> PascalCase conversion
    assert attrs["CivilizationType"] == "CIVILIZATION_ROME"
    assert attrs["BaseTourism"] == "10"
    assert attrs["LegacyModifier"] == "true"


def test_base_node_excludes_private_properties():
    """Test that private properties are excluded from XML."""
    node = BaseNode()
    node.public_prop = "visible"
    node._private_prop = "hidden"
    
    xml_elem = node.to_xml_element()
    attrs = xml_elem["Row"]
    
    assert "PublicProp" in attrs
    assert "_private_prop" not in attrs
    assert "_PrivateProp" not in attrs


def test_base_node_excludes_empty_values():
    """Test that None, empty string, and False are excluded."""
    node = BaseNode()
    node.has_value = True
    node.is_empty = None
    node.name = ""
    node.active = False
    
    xml_elem = node.to_xml_element()
    attrs = xml_elem["Row"]
    
    assert "HasValue" in attrs
    assert attrs["HasValue"] == "true"
    
    # These should be excluded
    assert "IsEmpty" not in attrs
    assert "Name" not in attrs
    assert "Active" not in attrs


def test_base_node_empty_returns_none():
    """Test that node with no attributes returns None."""
    node = BaseNode()
    node.nothing = None
    node.empty = ""
    
    xml_elem = node.to_xml_element()
    assert xml_elem is None


def test_base_node_insert_or_ignore():
    """Test insert_or_ignore() flag."""
    node = BaseNode()
    result = node.insert_or_ignore()
    
    assert result is node  # Fluent API
    assert node._insert_or_ignore is True


def test_camel_to_pascal():
    """Test camelCase to PascalCase conversion."""
    assert camel_to_pascal("civilizationType") == "CivilizationType"
    assert camel_to_pascal("baseTourism") == "BaseTourism"
    assert camel_to_pascal("x") == "X"
    assert camel_to_pascal("") == ""
    assert camel_to_pascal("already") == "Already"
