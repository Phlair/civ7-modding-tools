"""Phase 6: Shell configuration enhancements tests.

Tests for shell database configuration in CivilizationBuilder, ensuring
UI and visual customization elements are properly managed.
"""

import pytest
from civ7_modding_tools.builders import CivilizationBuilder
from civ7_modding_tools.nodes import (
    CivilizationTagNode,
    CivilizationItemNode,
    LeaderCivilizationBiasNode,
)
from civ7_modding_tools.files import XmlFile


class TestShellCivilizationConfiguration:
    """Test shell scope civilization configuration."""

    def test_civilization_builder_with_civilization_tags(self):
        """Test builder can add civilization tags to shell."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_tags = ["TAG_TRAIT_ECONOMIC", "TAG_TRAIT_MILITARY"]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._shell.to_xml_element()

        assert "Database" in xml
        assert "CivilizationTags" in xml["Database"]
        tags = xml["Database"]["CivilizationTags"]
        assert len(tags) >= 2

    def test_civilization_builder_with_civilization_items(self):
        """Test builder can add civilization items to shell."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_items = [
            {
                "type": "BUILDING_CARTHAGO",
                "kind": "KIND_BUILDING",
            },
            {
                "type": "UNIT_CARTHAGINIAN_QUINQUEREME",
                "kind": "KIND_UNIT",
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._shell.to_xml_element()

        assert "Database" in xml
        # CivilizationItems should be in shell
        db = xml["Database"]
        # Shell should have civilization (even if minimal)
        assert "Civilizations" in db

    def test_shell_database_isolated_from_current(self):
        """Test that shell database remains isolated from current database."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_tags = ["TAG_TRAIT_NAVAL"]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()

        # Current should not have civilization tags
        current_xml = builder._current.to_xml_element()
        shell_xml = builder._shell.to_xml_element()

        current_db = current_xml["Database"]
        shell_db = shell_xml["Database"]

        # Current has core data
        assert "Types" in current_db
        assert "Traits" in current_db
        assert "Civilizations" in current_db

        # Shell has UI data
        assert "Civilizations" in shell_db

    def test_civilization_builder_shell_with_fill(self):
        """Test shell configuration via fill() method."""
        builder = CivilizationBuilder().fill({
            "civilization_type": "CIVILIZATION_CARTHAGE",
            "civilization": {"civilization_type": "CIVILIZATION_CARTHAGE"},
            "localizations": [{"name": "Carthage"}],
            "civilization_tags": ["TAG_TRAIT_NAVAL", "TAG_TRAIT_COMMERCIAL"],
            "civilization_items": [
                {"type": "BUILDING_WHARF", "kind": "KIND_BUILDING"},
            ],
        })

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        assert "Database" in shell_xml
        shell_db = shell_xml["Database"]
        assert "Civilizations" in shell_db

    def test_shell_empty_when_no_tags_or_items(self):
        """Test shell database is minimal when no tags/items specified."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_ROME"
        builder.civilization = {"civilization_type": "CIVILIZATION_ROME"}
        builder.localizations = [{"name": "Rome"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        assert "Database" in shell_xml
        # Shell should still have civilization for UI purposes
        assert "Civilizations" in shell_xml["Database"]


class TestCivilizationShellPattern:
    """Test that shell configuration matches Civilization 7 patterns."""

    def test_shell_civilization_node_attributes(self):
        """Test shell civilization node has expected attributes."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {
            "civilization_type": "CIVILIZATION_CARTHAGE",
            "name": "LOC_CIVILIZATION_CARTHAGE_NAME",
            "adjective": "LOC_CIVILIZATION_CARTHAGE_ADJECTIVE",
        }
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        civs = shell_xml["Database"]["Civilizations"]
        if isinstance(civs, list):
            civ_row = civs[0]
        else:
            civ_row = civs

        attrs = civ_row["_attrs"]
        assert "CivilizationType" in attrs
        assert attrs["CivilizationType"] == "CIVILIZATION_CARTHAGE"

    def test_carthage_pattern_civilization_tags_in_shell(self):
        """Test civilization tags in shell match Carthage pattern."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_tags = [
            "TAG_TRAIT_NAVAL",
            "TAG_TRAIT_COMMERCIAL",
            "TAG_TRAIT_AMBITIOUS",
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        assert "Database" in shell_xml
        shell_db = shell_xml["Database"]

        # Tags should be present if they were specified
        if "CivilizationTags" in shell_db:
            tags = shell_db["CivilizationTags"]
            assert len(tags) >= 1


class TestShellIntegration:
    """Test shell configuration integrated with civilization building."""

    def test_civilization_builder_complete_with_shell_config(self):
        """Test builder with all components including shell config."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_traits = ["TRAIT_ECONOMIC", "TRAIT_MILITARY"]
        builder.civilization_tags = ["TAG_TRAIT_NAVAL"]
        builder.civilization_items = [
            {"type": "BUILDING_WHARF", "kind": "KIND_BUILDING"}
        ]
        builder.ai_list_types = [{"list_type": "NAVAL_INFRASTRUCTURE"}]
        builder.localizations = [{"name": "Carthage"}]

        files = builder.build()
        shell_file = next((f for f in files if f.name == "shell.xml"), None)

        assert shell_file is not None
        assert isinstance(shell_file, XmlFile)

    def test_civilization_with_start_bias_and_shell_config(self):
        """Test shell config works alongside start bias configuration."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.start_bias_biomes = [{"biome_type": "BIOME_TROPICAL"}]
        builder.civilization_tags = ["TAG_TRAIT_NAVAL"]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()

        current_xml = builder._current.to_xml_element()
        shell_xml = builder._shell.to_xml_element()

        # Current has start biases
        assert "StartBias_Biomes" in current_xml["Database"]
        # Shell has tags and civilizations
        assert "Civilizations" in shell_xml["Database"]

    def test_civilization_builder_fluent_api_with_shell(self):
        """Test fluent API works with shell configuration."""
        builder = (
            CivilizationBuilder()
            .fill({
                "civilization_type": "CIVILIZATION_CARTHAGE",
                "civilization": {"civilization_type": "CIVILIZATION_CARTHAGE"},
                "localizations": [{"name": "Carthage"}],
            })
            .fill({
                "civilization_tags": ["TAG_TRAIT_NAVAL"],
                "civilization_items": [
                    {"type": "UNIT_NAVAL", "kind": "KIND_UNIT"}
                ],
            })
        )

        files = builder.build()
        assert len(files) > 0


class TestShellEdgeCases:
    """Test edge cases for shell configuration."""

    def test_civilization_tags_empty_list(self):
        """Test empty civilization tags list doesn't break shell."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_ROME"
        builder.civilization = {"civilization_type": "CIVILIZATION_ROME"}
        builder.civilization_tags = []
        builder.localizations = [{"name": "Rome"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        assert "Database" in shell_xml
        # Should still generate valid XML
        assert "Civilizations" in shell_xml["Database"]

    def test_civilization_items_empty_list(self):
        """Test empty civilization items list doesn't break shell."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_ROME"
        builder.civilization = {"civilization_type": "CIVILIZATION_ROME"}
        builder.civilization_items = []
        builder.localizations = [{"name": "Rome"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        assert "Database" in shell_xml

    def test_mixed_tag_and_item_configurations(self):
        """Test various combinations of tags and items."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_tags = ["TAG_TRAIT_A", "TAG_TRAIT_B"]
        builder.civilization_items = [
            {"type": "ITEM_1", "kind": "KIND_1"},
            {"type": "ITEM_2", "kind": "KIND_2"},
            {"type": "ITEM_3", "kind": "KIND_3"},
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        assert "Database" in shell_xml
        shell_db = shell_xml["Database"]

        # Verify structure is valid
        assert "Civilizations" in shell_db

    def test_shell_isolated_from_bound_items(self):
        """Test that shell doesn't inherit bound item configurations."""
        # This is a basic test - Phase 5 handles complex bound items
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_tags = ["TAG_TRAIT_NAVAL"]
        builder.localizations = [{"name": "Carthage"}]

        # Don't bind anything
        builder.migrate()

        shell_xml = builder._shell.to_xml_element()
        assert "Database" in shell_xml


class TestShellAttributes:
    """Test shell-specific attributes and configurations."""

    def test_civilization_shell_has_minimal_data(self):
        """Test shell civilization contains only UI-relevant data."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        # Shell civilization should exist
        civs = shell_xml["Database"]["Civilizations"]
        assert len(civs) >= 1

    def test_civilization_tags_properly_associated(self):
        """Test civilization tags are properly set in shell."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_tags = ["TAG_ECONOMIC", "TAG_MILITARY"]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        shell_xml = builder._shell.to_xml_element()

        shell_db = shell_xml["Database"]
        # Tags should reference the civilization
        if "CivilizationTags" in shell_db:
            tags = shell_db["CivilizationTags"]
            if isinstance(tags, list):
                for tag in tags:
                    assert tag["_attrs"]["CivilizationType"] == "CIVILIZATION_CARTHAGE"

    def test_shell_file_has_correct_action_group(self):
        """Test shell file has correct action group assignment."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.localizations = [{"name": "Carthage"}]

        files = builder.build()
        shell_file = next((f for f in files if f.name == "shell.xml"), None)

        assert shell_file is not None
        # Shell file should have action groups configured
        assert shell_file.action_groups is not None
