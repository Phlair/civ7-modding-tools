"""Phase 5: AI leader priorities integration tests.

Tests for AI configuration support in CivilizationBuilder, ensuring
civilization AI behavior can be configured with leader traits and priorities.
"""

import pytest
from civ7_modding_tools.builders import CivilizationBuilder
from civ7_modding_tools.nodes import (
    AiListTypeNode,
    AiListNode,
    AiFavoredItemNode,
    LeaderCivPriorityNode,
)
from civ7_modding_tools.files import XmlFile


class TestCivilizationBuilderAiConfiguration:
    """Test AI configuration in CivilizationBuilder."""

    def test_civilization_builder_with_ai_list_types(self):
        """Test builder can accept AI list types."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_list_types = [
            {
                "list_type": "NAVAL_INFRASTRUCTURE",
            },
            {
                "list_type": "COMMERCIAL_FOCUS",
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
        assert "AiListTypes" in xml["Database"]
        assert len(xml["Database"]["AiListTypes"]) == 2

    def test_civilization_builder_with_ai_lists(self):
        """Test builder can accept AI lists with leader traits."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_lists = [
            {
                "list_type": "NAVAL_INFRASTRUCTURE",
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "system": "Infrastructure",
            }
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "AiLists" in xml["Database"]
        ai_list = xml["Database"]["AiLists"][0]
        assert ai_list["_attrs"]["ListType"] == "NAVAL_INFRASTRUCTURE"
        assert ai_list["_attrs"]["LeaderType"] == "TRAIT_LEADER_FOCUS_NAVAL"
        assert ai_list["_attrs"]["System"] == "Infrastructure"

    def test_civilization_builder_with_ai_favored_items(self):
        """Test builder can accept AI favored items."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_favored_items = [
            {
                "list_type": "NAVAL_INFRASTRUCTURE",
                "item": "BUILDING_WHARF",
                "favored": True,
            },
            {
                "list_type": "NAVAL_INFRASTRUCTURE",
                "item": "BUILDING_LIGHTHOUSE",
                "favored": True,
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "AiFavoredItems" in xml["Database"]
        assert len(xml["Database"]["AiFavoredItems"]) == 2
        for item in xml["Database"]["AiFavoredItems"]:
            assert item["_attrs"]["Favored"] == "true"

    def test_civilization_builder_with_leader_civ_priorities(self):
        """Test builder can accept leader civilization priorities."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.leader_civ_priorities = [
            {
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "priority": 50,
            },
            {
                "leader_type": "TRAIT_LEADER_FOCUS_GOLD",
                "priority": 30,
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "LeaderCivPriorities" in xml["Database"]
        assert len(xml["Database"]["LeaderCivPriorities"]) == 2

        # Check first priority
        first_priority = xml["Database"]["LeaderCivPriorities"][0]
        assert first_priority["_attrs"]["Civilization"] == "CIVILIZATION_CARTHAGE"
        assert first_priority["_attrs"]["Leader"] == "TRAIT_LEADER_FOCUS_NAVAL"
        assert first_priority["_attrs"]["Priority"] == "50"

    def test_civilization_builder_complete_ai_configuration(self):
        """Test builder with all AI configuration components."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_list_types = [
            {"list_type": "NAVAL_INFRASTRUCTURE"},
            {"list_type": "COMMERCIAL_FOCUS"},
        ]
        builder.ai_lists = [
            {
                "list_type": "NAVAL_INFRASTRUCTURE",
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "system": "Infrastructure",
            }
        ]
        builder.ai_favored_items = [
            {
                "list_type": "NAVAL_INFRASTRUCTURE",
                "item": "BUILDING_WHARF",
                "favored": True,
            },
            {
                "list_type": "COMMERCIAL_FOCUS",
                "item": "BUILDING_MARKET",
                "favored": True,
            },
        ]
        builder.leader_civ_priorities = [
            {
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "priority": 50,
            },
            {
                "leader_type": "TRAIT_LEADER_FOCUS_GOLD",
                "priority": 40,
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        files = builder.build()
        current_file = next((f for f in files if f.name == "current.xml"), None)

        assert current_file is not None
        assert isinstance(current_file, XmlFile)
        # Verify it's the current age action group (not checking exact string as it may vary)
        assert current_file.action_groups is not None

    def test_civilization_builder_ai_configuration_with_fill(self):
        """Test AI configuration via fill() method."""
        builder = CivilizationBuilder().fill({
            "civilization_type": "CIVILIZATION_CARTHAGE",
            "civilization": {"civilization_type": "CIVILIZATION_CARTHAGE"},
            "localizations": [{"name": "Carthage"}],
            "ai_list_types": [{"list_type": "NAVAL_INFRASTRUCTURE"}],
            "ai_lists": [
                {
                    "list_type": "NAVAL_INFRASTRUCTURE",
                    "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                    "system": "Infrastructure",
                }
            ],
            "ai_favored_items": [
                {
                    "list_type": "NAVAL_INFRASTRUCTURE",
                    "item": "BUILDING_WHARF",
                    "favored": True,
                }
            ],
            "leader_civ_priorities": [
                {
                    "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                    "priority": 50,
                }
            ],
        })

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "AiListTypes" in xml["Database"]
        assert "AiLists" in xml["Database"]
        assert "AiFavoredItems" in xml["Database"]
        assert "LeaderCivPriorities" in xml["Database"]

    def test_civilization_builder_ai_configuration_optional(self):
        """Test AI configuration is optional (backward compatibility)."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_ROME"
        builder.civilization = {"civilization_type": "CIVILIZATION_ROME"}
        builder.localizations = [{"name": "Rome"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # AI configuration should not be present if not specified
        db = xml.get("Database", {})
        assert "AiListTypes" not in db or len(db.get("AiListTypes", [])) == 0
        assert "AiLists" not in db or len(db.get("AiLists", [])) == 0
        assert "AiFavoredItems" not in db or len(db.get("AiFavoredItems", [])) == 0
        assert "LeaderCivPriorities" not in db or len(db.get("LeaderCivPriorities", [])) == 0


class TestCarthageAiPatternIntegration:
    """Test that builder output matches Carthage AI configuration patterns."""

    def test_carthage_pattern_ai_list_types(self):
        """Test AI list types match Carthage pattern."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_list_types = [
            {"list_type": "Carthaginian_Favoured_Infrastructure"},
            {"list_type": "Carthaginian_Favoured_Commercial"},
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        ai_types = xml["Database"]["AiListTypes"]
        assert any(
            node["_attrs"]["ListType"] == "Carthaginian_Favoured_Infrastructure"
            for node in ai_types
        )
        assert any(
            node["_attrs"]["ListType"] == "Carthaginian_Favoured_Commercial"
            for node in ai_types
        )

    def test_carthage_pattern_ai_lists_with_leader_traits(self):
        """Test AI lists with leader traits match Carthage pattern."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_lists = [
            {
                "list_type": "Carthaginian_Favoured_Infrastructure",
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "system": "Infrastructure",
            },
            {
                "list_type": "Carthaginian_Favoured_Commercial",
                "leader_type": "TRAIT_LEADER_FOCUS_GOLD",
                "system": "Commerce",
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        ai_lists = xml["Database"]["AiLists"]
        assert len(ai_lists) == 2

        # Verify both systems are present
        systems = {node["_attrs"]["System"] for node in ai_lists}
        assert "Infrastructure" in systems
        assert "Commerce" in systems

    def test_carthage_pattern_favored_buildings(self):
        """Test favored buildings match Carthage pattern."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.ai_favored_items = [
            {
                "list_type": "Carthaginian_Favoured_Infrastructure",
                "item": "BUILDING_WHARF",
                "favored": True,
            },
            {
                "list_type": "Carthaginian_Favoured_Infrastructure",
                "item": "BUILDING_LIGHTHOUSE",
                "favored": True,
            },
            {
                "list_type": "Carthaginian_Favoured_Commercial",
                "item": "BUILDING_MARKET",
                "favored": True,
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        favored_items = xml["Database"]["AiFavoredItems"]
        assert len(favored_items) == 3

        # All should have Favored="true"
        for item in favored_items:
            assert item["_attrs"]["Favored"] == "true"

        # Check specific items
        item_types = {node["_attrs"]["Item"] for node in favored_items}
        assert "BUILDING_WHARF" in item_types
        assert "BUILDING_LIGHTHOUSE" in item_types
        assert "BUILDING_MARKET" in item_types

    def test_carthage_pattern_leader_priorities(self):
        """Test leader priorities match Carthage pattern."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.leader_civ_priorities = [
            {
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "priority": 50,
            },
            {
                "leader_type": "TRAIT_LEADER_FOCUS_GOLD",
                "priority": 40,
            },
            {
                "leader_type": "TRAIT_LEADER_FOCUS_SCIENCE",
                "priority": 20,
            },
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        priorities = xml["Database"]["LeaderCivPriorities"]
        assert len(priorities) == 3

        # All should have Civilization="CIVILIZATION_CARTHAGE"
        for priority in priorities:
            assert priority["_attrs"]["Civilization"] == "CIVILIZATION_CARTHAGE"

        # Check priority values
        priority_values = sorted(
            [int(node["_attrs"]["Priority"]) for node in priorities], reverse=True
        )
        assert priority_values == [50, 40, 20]


class TestAiConfigurationIntegration:
    """Test AI configuration integrated with other civilization features."""

    def test_civilization_with_start_bias_and_ai_config(self):
        """Test AI config works alongside start biases."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.start_bias_biomes = [
            {"biome_type": "BIOME_DESERT", "bias": 5}
        ]
        builder.ai_list_types = [
            {"list_type": "NAVAL_INFRASTRUCTURE"}
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        # Start bias biomes are in StartBiasBiomes
        assert "StartBiasBiomes" in db
        assert "AiListTypes" in db

    def test_civilization_with_traits_and_ai_config(self):
        """Test AI config works with civilization traits."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.civilization_traits = [
            "TRAIT_ECONOMIC",
            "TRAIT_MILITARY"
        ]
        builder.leader_civ_priorities = [
            {
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "priority": 50,
            }
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "CivilizationTraits" in db
        assert "LeaderCivPriorities" in db

    def test_civilization_builder_fluent_api_with_ai(self):
        """Test fluent API works with AI configuration."""
        builder = (
            CivilizationBuilder()
            .fill({
                "civilization_type": "CIVILIZATION_CARTHAGE",
                "civilization": {"civilization_type": "CIVILIZATION_CARTHAGE"},
                "localizations": [{"name": "Carthage"}],
            })
            .fill({
                "ai_list_types": [{"list_type": "NAVAL_INFRASTRUCTURE"}],
                "leader_civ_priorities": [
                    {"leader_type": "TRAIT_LEADER_FOCUS_NAVAL", "priority": 50}
                ],
            })
        )

        files = builder.build()
        assert len(files) > 0

        # Verify current.xml was generated
        current = next((f for f in files if f.name == "current.xml"), None)
        assert current is not None


class TestAiConfigurationEdgeCases:
    """Test edge cases and error handling for AI configuration."""

    def test_empty_ai_configuration(self):
        """Test builder with empty AI configuration lists."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_ROME"
        builder.civilization = {"civilization_type": "CIVILIZATION_ROME"}
        builder.ai_list_types = []
        builder.ai_lists = []
        builder.ai_favored_items = []
        builder.leader_civ_priorities = []
        builder.localizations = [{"name": "Rome"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml.get("Database", {})
        # Empty lists should not appear in XML or be empty
        assert not db.get("AiListTypes", [])
        assert not db.get("AiLists", [])
        assert not db.get("AiFavoredItems", [])
        assert not db.get("LeaderCivPriorities", [])

    def test_ai_configuration_with_partial_data(self):
        """Test AI configuration with only some fields populated."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        # Only populate ai_list_types and leader_civ_priorities
        builder.ai_list_types = [
            {"list_type": "NAVAL_INFRASTRUCTURE"}
        ]
        builder.leader_civ_priorities = [
            {"leader_type": "TRAIT_LEADER_FOCUS_NAVAL", "priority": 50}
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "AiListTypes" in db
        assert "LeaderCivPriorities" in db
        # Others should be empty or absent
        assert not db.get("AiLists", [])
        assert not db.get("AiFavoredItems", [])

    def test_ai_list_node_direct_creation(self):
        """Test AiListNode creation with various attribute combinations."""
        node = AiListNode(
            list_type="TEST_LIST",
            leader_type="TRAIT_TEST_LEADER",
            system="TestSystem",
        )
        xml = node.to_xml_element()

        assert xml["_name"] == "Row"
        assert xml["_attrs"]["ListType"] == "TEST_LIST"
        assert xml["_attrs"]["LeaderType"] == "TRAIT_TEST_LEADER"
        assert xml["_attrs"]["System"] == "TestSystem"

    def test_ai_favored_item_with_optional_fields(self):
        """Test AiFavoredItemNode with optional value and string_val."""
        node = AiFavoredItemNode(
            list_type="TEST_LIST",
            item="TEST_ITEM",
            favored=True,
            value=100,
            string_val="Test String",
        )
        xml = node.to_xml_element()

        attrs = xml["_attrs"]
        assert attrs["ListType"] == "TEST_LIST"
        assert attrs["Item"] == "TEST_ITEM"
        assert attrs["Favored"] == "true"
        assert attrs["Value"] == "100"
        assert attrs["StringVal"] == "Test String"

    def test_leader_civ_priority_inherits_civilization_type(self):
        """Test LeaderCivPriorityNode properly handles civilization attribute."""
        builder = CivilizationBuilder()
        builder.civilization_type = "CIVILIZATION_CARTHAGE"
        builder.civilization = {"civilization_type": "CIVILIZATION_CARTHAGE"}
        builder.leader_civ_priorities = [
            {
                "leader_type": "TRAIT_LEADER_FOCUS_NAVAL",
                "priority": 50,
            }
        ]
        builder.localizations = [{"name": "Carthage"}]

        builder.migrate()

        # Check that civilization was properly set
        priority_node = builder._current.leader_civ_priorities[0]
        assert priority_node.civilization == "CIVILIZATION_CARTHAGE"
