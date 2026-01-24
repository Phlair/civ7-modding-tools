"""Tests for Phase 1.3: Multi-Resolution Icon Support."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod
from civ7_modding_tools.builders import CivilizationBuilder
from civ7_modding_tools.nodes import IconDefinitionNode


class TestIconDefinitionNode:
    """Test IconDefinitionNode for multi-resolution icon support."""

    def test_icon_definition_node_basic(self):
        """Test basic IconDefinitionNode creation."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png"
        )
        
        assert node.id == "CIVILIZATION_BABYLON"
        assert node.path == "icons/civs/civ_sym_babylon.png"
        assert node.context is None
        assert node.icon_size is None

    def test_icon_definition_node_with_context(self):
        """Test IconDefinitionNode with context."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png",
            context="DEFAULT"
        )
        
        assert node.id == "CIVILIZATION_BABYLON"
        assert node.context == "DEFAULT"

    def test_icon_definition_node_with_icon_size(self):
        """Test IconDefinitionNode with icon size."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png",
            icon_size="256"
        )
        
        assert node.icon_size == "256"

    def test_icon_definition_node_with_all_properties(self):
        """Test IconDefinitionNode with all properties."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png",
            context="BACKGROUND",
            icon_size="1080"
        )
        
        assert node.id == "CIVILIZATION_BABYLON"
        assert node.path == "icons/civs/civ_sym_babylon.png"
        assert node.context == "BACKGROUND"
        assert node.icon_size == "1080"

    def test_icon_definition_node_to_xml_basic(self):
        """Test IconDefinitionNode XML generation."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png"
        )
        
        xml = node.to_xml_element()
        assert xml is not None
        assert xml['_name'] == 'Row'
        assert xml['_content'] is not None

    def test_icon_definition_node_to_xml_with_context(self):
        """Test IconDefinitionNode XML generation with context."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png",
            context="DEFAULT"
        )
        
        xml = node.to_xml_element()
        assert xml is not None
        assert len(xml['_content']) > 2  # ID, Path, and Context

    def test_icon_definition_node_to_xml_with_size(self):
        """Test IconDefinitionNode XML generation with size."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON",
            path="icons/civs/civ_sym_babylon.png",
            icon_size="256"
        )
        
        xml = node.to_xml_element()
        assert xml is not None
        assert len(xml['_content']) > 2  # ID, Path, and IconSize

    def test_icon_definition_node_without_id(self):
        """Test IconDefinitionNode returns None when ID is missing."""
        node = IconDefinitionNode(
            path="icons/civs/civ_sym_babylon.png"
        )
        
        xml = node.to_xml_element()
        assert xml is None

    def test_icon_definition_node_without_path(self):
        """Test IconDefinitionNode returns None when path is missing."""
        node = IconDefinitionNode(
            id="CIVILIZATION_BABYLON"
        )
        
        xml = node.to_xml_element()
        assert xml is None


class TestMultiResolutionIcons:
    """Test multi-resolution icon support in builders."""

    def test_civilization_builder_with_multiple_icon_resolutions(self):
        """Test CivilizationBuilder can accept icon with multiple resolutions."""
        builder = CivilizationBuilder()
        
        # Icon with resolution information
        icon_dict = {
            "path": "icons/civs/civ_sym_babylon.png",
            "context": "DEFAULT",
            "icon_size": "256"
        }
        
        builder.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'icon': icon_dict
        })
        
        assert builder.icon == icon_dict
        assert builder.icon.get('icon_size') == '256'

    def test_icon_definition_node_multiple_resolutions(self):
        """Test creating multiple icon nodes for different resolutions."""
        resolutions = [
            {"icon_size": "1080", "context": "BACKGROUND"},
            {"icon_size": "256", "context": "DEFAULT"},
            {"icon_size": "128", "context": "DEFAULT"},
            {"icon_size": "80", "context": "DEFAULT"},
        ]
        
        icon_nodes = []
        for res in resolutions:
            node = IconDefinitionNode(
                id="CIVILIZATION_BABYLON",
                path=f"icons/civs/civ_sym_babylon_{res['icon_size']}.png",
                context=res.get("context"),
                icon_size=res.get("icon_size")
            )
            icon_nodes.append(node)
        
        # All nodes should be valid
        assert len(icon_nodes) == 4
        for node in icon_nodes:
            assert node.to_xml_element() is not None

    def test_icon_contexts(self):
        """Test different icon contexts."""
        contexts = ["DEFAULT", "BACKGROUND", "PORTRAIT", "BACKGROUND_SHADOW"]
        
        for context in contexts:
            node = IconDefinitionNode(
                id="TEST_ICON",
                path="test/icon.png",
                context=context
            )
            
            assert node.context == context
            xml = node.to_xml_element()
            assert xml is not None

    def test_icon_sizes(self):
        """Test different icon sizes."""
        sizes = ["80", "128", "256", "512", "1080", "2160"]
        
        for size in sizes:
            node = IconDefinitionNode(
                id="TEST_ICON",
                path="test/icon.png",
                icon_size=size
            )
            
            assert node.icon_size == size
            xml = node.to_xml_element()
            assert xml is not None


class TestIconIntegration:
    """Integration tests for multi-resolution icons."""

    def test_civilization_with_multi_resolution_icons_in_modinfo(self):
        """Test mod with multi-resolution icons generates valid modinfo."""
        mod = Mod(id="babylon-icons", version="1", name="Babylon Icons Test")
        
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'civilization_traits': [],
            'icon': {
                'path': 'icons/civs/babylon_256',
                'context': 'DEFAULT',
                'icon_size': '256'
            }
        })
        
        mod.add(builder)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-icons.modinfo"
            assert modinfo_path.exists()
            
            # Should generate valid XML
            content = modinfo_path.read_text()
            assert '<?xml' in content
            assert 'babylon-icons' in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
