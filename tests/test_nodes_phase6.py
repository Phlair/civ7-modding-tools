"""Tests for Phase 6 New Node Types.

Covers the 8 new node implementations added for full TypeScript parity:
- ModifierRequirementNode
- StartBiasAdjacentToCoastNode
- StartBiasFeatureClassNode
- StartBiasRiverNode
- StringNode
- UnitReplaceNode
- VisArtCivilizationBuildingCultureNode
- VisArtCivilizationUnitCultureNode

These nodes complete the full 73-node set from the TypeScript version.
"""

import pytest

from civ7_modding_tools.nodes import (
    ModifierRequirementNode,
    StartBiasAdjacentToCoastNode,
    StartBiasFeatureClassNode,
    StartBiasRiverNode,
    StringNode,
    UnitReplaceNode,
    VisArtCivilizationBuildingCultureNode,
    VisArtCivilizationUnitCultureNode,
    BaseNode,
)


class TestModifierRequirementNode:
    """Tests for ModifierRequirementNode."""

    def test_modifier_requirement_node_initialization(self):
        """Test ModifierRequirementNode initializes correctly."""
        node = ModifierRequirementNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.modifier_type is None
        assert node.requirement_type is None
        assert node.requirement_set_type is None

    def test_modifier_requirement_node_with_data(self):
        """Test ModifierRequirementNode with data."""
        node = ModifierRequirementNode()
        node.modifier_type = "MOD_GONDOR_BONUS"
        node.requirement_type = "TECH_MATCHED"
        
        assert node.modifier_type == "MOD_GONDOR_BONUS"
        assert node.requirement_type == "TECH_MATCHED"

    def test_modifier_requirement_node_to_xml(self):
        """Test ModifierRequirementNode XML serialization."""
        node = ModifierRequirementNode()
        node.modifier_type = "MOD_GONDOR"
        node.requirement_set_type = "REQ_SET_1"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "ModifierType" in str(xml)
        assert "MOD_GONDOR" in str(xml)


class TestStartBiasAdjacentToCoastNode:
    """Tests for StartBiasAdjacentToCoastNode."""

    def test_start_bias_adjacent_to_coast_initialization(self):
        """Test StartBiasAdjacentToCoastNode initializes correctly."""
        node = StartBiasAdjacentToCoastNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.bias is None

    def test_start_bias_adjacent_to_coast_with_data(self):
        """Test StartBiasAdjacentToCoastNode with data."""
        node = StartBiasAdjacentToCoastNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.bias = 50
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.bias == 50

    def test_start_bias_adjacent_to_coast_to_xml(self):
        """Test StartBiasAdjacentToCoastNode XML serialization."""
        node = StartBiasAdjacentToCoastNode()
        node.civilization_type = "CIVILIZATION_ROME"
        node.bias = 25
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "CivilizationType" in str(xml)


class TestStartBiasFeatureClassNode:
    """Tests for StartBiasFeatureClassNode."""

    def test_start_bias_feature_class_initialization(self):
        """Test StartBiasFeatureClassNode initializes correctly."""
        node = StartBiasFeatureClassNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.feature_class is None
        assert node.bias is None

    def test_start_bias_feature_class_with_data(self):
        """Test StartBiasFeatureClassNode with data."""
        node = StartBiasFeatureClassNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.feature_class = "FEATURE_FOREST"
        node.bias = 75
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.feature_class == "FEATURE_FOREST"
        assert node.bias == 75

    def test_start_bias_feature_class_to_xml(self):
        """Test StartBiasFeatureClassNode XML serialization."""
        node = StartBiasFeatureClassNode()
        node.civilization_type = "CIVILIZATION_PARIS"
        node.feature_class = "FEATURE_MOUNTAIN"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "FeatureClass" in str(xml)


class TestStartBiasRiverNode:
    """Tests for StartBiasRiverNode."""

    def test_start_bias_river_initialization(self):
        """Test StartBiasRiverNode initializes correctly."""
        node = StartBiasRiverNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.bias is None

    def test_start_bias_river_with_data(self):
        """Test StartBiasRiverNode with data."""
        node = StartBiasRiverNode()
        node.civilization_type = "CIVILIZATION_EGYPT"
        node.bias = 100
        
        assert node.civilization_type == "CIVILIZATION_EGYPT"
        assert node.bias == 100

    def test_start_bias_river_to_xml(self):
        """Test StartBiasRiverNode XML serialization."""
        node = StartBiasRiverNode()
        node.civilization_type = "CIVILIZATION_NILE_VALLEY"
        node.bias = 90
        
        xml = node.to_xml_element()
        assert xml is not None


class TestStringNode:
    """Tests for StringNode."""

    def test_string_node_initialization(self):
        """Test StringNode initializes correctly."""
        node = StringNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.value is None

    def test_string_node_with_data(self):
        """Test StringNode with string data."""
        node = StringNode()
        node.value = "test_string_value"
        
        assert node.value == "test_string_value"

    def test_string_node_with_empty_string(self):
        """Test StringNode with empty string."""
        node = StringNode()
        node.value = ""
        
        # Empty string should not appear in XML
        xml = node.to_xml_element()
        assert xml is None

    def test_string_node_to_xml(self):
        """Test StringNode XML serialization."""
        node = StringNode()
        node.value = "my_value"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "my_value" in str(xml)


class TestUnitReplaceNode:
    """Tests for UnitReplaceNode."""

    def test_unit_replace_node_initialization(self):
        """Test UnitReplaceNode initializes correctly."""
        node = UnitReplaceNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.unit_type is None
        assert node.replaces_unit_type is None
        assert node.era is None

    def test_unit_replace_node_with_data(self):
        """Test UnitReplaceNode with data."""
        node = UnitReplaceNode()
        node.unit_type = "UNIT_GONDOR_RANGER"
        node.replaces_unit_type = "UNIT_RANGER"
        node.era = "AGE_MEDIEVAL"
        
        assert node.unit_type == "UNIT_GONDOR_RANGER"
        assert node.replaces_unit_type == "UNIT_RANGER"
        assert node.era == "AGE_MEDIEVAL"

    def test_unit_replace_node_to_xml(self):
        """Test UnitReplaceNode XML serialization."""
        node = UnitReplaceNode()
        node.unit_type = "UNIT_KNIGHT"
        node.replaces_unit_type = "UNIT_HEAVY_CAVALRY"
        node.era = "AGE_MEDIEVAL"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "UnitType" in str(xml)
        assert "ReplacesUnitType" in str(xml)


class TestVisArtCivilizationBuildingCultureNode:
    """Tests for VisArtCivilizationBuildingCultureNode."""

    def test_vis_art_building_culture_initialization(self):
        """Test VisArtCivilizationBuildingCultureNode initializes correctly."""
        node = VisArtCivilizationBuildingCultureNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.building_culture_type is None
        assert node.visual_parent_type is None

    def test_vis_art_building_culture_with_data(self):
        """Test VisArtCivilizationBuildingCultureNode with data."""
        node = VisArtCivilizationBuildingCultureNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.building_culture_type = "BUILDING_CULTURE_GONDOR"
        node.visual_parent_type = "BUILDING_CULTURE_WESTERN"
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.building_culture_type == "BUILDING_CULTURE_GONDOR"
        assert node.visual_parent_type == "BUILDING_CULTURE_WESTERN"

    def test_vis_art_building_culture_to_xml(self):
        """Test VisArtCivilizationBuildingCultureNode XML serialization."""
        node = VisArtCivilizationBuildingCultureNode()
        node.civilization_type = "CIVILIZATION_ROME"
        node.building_culture_type = "BUILDING_CULTURE_ROME"
        node.visual_parent_type = "BUILDING_CULTURE_CLASSICAL"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "CivilizationType" in str(xml)


class TestVisArtCivilizationUnitCultureNode:
    """Tests for VisArtCivilizationUnitCultureNode."""

    def test_vis_art_unit_culture_initialization(self):
        """Test VisArtCivilizationUnitCultureNode initializes correctly."""
        node = VisArtCivilizationUnitCultureNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.unit_culture_type is None
        assert node.visual_parent_type is None

    def test_vis_art_unit_culture_with_data(self):
        """Test VisArtCivilizationUnitCultureNode with data."""
        node = VisArtCivilizationUnitCultureNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.unit_culture_type = "UNIT_CULTURE_GONDOR"
        node.visual_parent_type = "UNIT_CULTURE_WESTERN"
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.unit_culture_type == "UNIT_CULTURE_GONDOR"
        assert node.visual_parent_type == "UNIT_CULTURE_WESTERN"

    def test_vis_art_unit_culture_to_xml(self):
        """Test VisArtCivilizationUnitCultureNode XML serialization."""
        node = VisArtCivilizationUnitCultureNode()
        node.civilization_type = "CIVILIZATION_BARBARIAN"
        node.unit_culture_type = "UNIT_CULTURE_BARBARIAN"
        node.visual_parent_type = "UNIT_CULTURE_DEFAULT"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "CivilizationType" in str(xml)


class TestPhase6NodesIntegration:
    """Integration tests for Phase 6 nodes."""

    def test_all_phase6_nodes_inherit_from_basenode(self):
        """Test all Phase 6 nodes properly inherit from BaseNode."""
        nodes = [
            ModifierRequirementNode(),
            StartBiasAdjacentToCoastNode(),
            StartBiasFeatureClassNode(),
            StartBiasRiverNode(),
            StringNode(),
            UnitReplaceNode(),
            VisArtCivilizationBuildingCultureNode(),
            VisArtCivilizationUnitCultureNode(),
        ]
        
        for node in nodes:
            assert isinstance(node, BaseNode)
            assert hasattr(node, 'to_xml_element')
            assert callable(node.to_xml_element)

    def test_all_phase6_nodes_have_name(self):
        """Test all Phase 6 nodes have _name set to 'Row'."""
        nodes = [
            ModifierRequirementNode(),
            StartBiasAdjacentToCoastNode(),
            StartBiasFeatureClassNode(),
            StartBiasRiverNode(),
            StringNode(),
            UnitReplaceNode(),
            VisArtCivilizationBuildingCultureNode(),
            VisArtCivilizationUnitCultureNode(),
        ]
        
        for node in nodes:
            assert node._name == "Row"

    def test_phase6_nodes_xml_serialization_with_data(self):
        """Test Phase 6 nodes serialize to XML correctly with data."""
        test_cases = [
            (ModifierRequirementNode(), {"modifier_type": "MOD_TEST"}),
            (StartBiasAdjacentToCoastNode(), {"civilization_type": "CIV_TEST", "bias": 50}),
            (StartBiasFeatureClassNode(), {"civilization_type": "CIV_TEST", "feature_class": "FOREST"}),
            (StartBiasRiverNode(), {"civilization_type": "CIV_TEST", "bias": 100}),
            (StringNode(), {"value": "test_value"}),
            (UnitReplaceNode(), {"unit_type": "UNIT_TEST", "replaces_unit_type": "UNIT_OLD"}),
            (VisArtCivilizationBuildingCultureNode(), {"civilization_type": "CIV_TEST"}),
            (VisArtCivilizationUnitCultureNode(), {"civilization_type": "CIV_TEST"}),
        ]
        
        for node, data in test_cases:
            for key, value in data.items():
                setattr(node, key, value)
            
            xml = node.to_xml_element()
            # Nodes with data should serialize successfully
            # (may be None if all properties are None, but not with our test data)
            assert xml is not None or len(data) == 0


class TestPhase6NodesEdgeCases:
    """Edge case tests for Phase 6 nodes."""

    def test_string_node_with_special_characters(self):
        """Test StringNode handles special XML characters."""
        node = StringNode()
        node.value = "value_with_&_ampersand"
        
        # Should not raise an error
        xml = node.to_xml_element()
        assert xml is not None

    def test_unit_replace_node_without_era(self):
        """Test UnitReplaceNode works without era."""
        node = UnitReplaceNode()
        node.unit_type = "UNIT_A"
        node.replaces_unit_type = "UNIT_B"
        
        xml = node.to_xml_element()
        assert xml is not None

    def test_start_bias_nodes_all_properties_optional(self):
        """Test start bias nodes work with partial data."""
        # All properties optional
        node1 = StartBiasAdjacentToCoastNode()
        node1.civilization_type = "CIV_TEST"
        # bias is still None
        
        node2 = StartBiasRiverNode()
        node2.bias = 50
        # civilization_type is still None
        
        # Should still serialize without errors
        xml1 = node1.to_xml_element()
        xml2 = node2.to_xml_element()
        assert xml1 is not None
        assert xml2 is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
