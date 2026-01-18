"""Tests for Phase 4: AI configuration node support."""

import pytest
from civ7_modding_tools.nodes import (
    AiListTypeNode,
    AiListNode,
    AiFavoredItemNode,
    LeaderCivPriorityNode,
    DatabaseNode,
)
from civ7_modding_tools import Mod, CivilizationBuilder


class TestAiConfigurationNodes:
    """Test AI configuration node types."""

    def test_ai_list_type_node_creation(self):
        """Test AiListTypeNode creates correct structure."""
        node = AiListTypeNode(list_type="NAVAL_INFRASTRUCTURE")
        xml = node.to_xml_element()
        assert xml["_name"] == "Row"
        assert xml["_attrs"]["ListType"] == "NAVAL_INFRASTRUCTURE"

    def test_ai_list_node_creation(self):
        """Test AiListNode creates correct structure."""
        node = AiListNode(
            list_type="NAVAL_INFRASTRUCTURE",
            leader_type="TRAIT_LEADER_FOCUS_NAVAL",
            system="Infrastructure",
        )
        xml = node.to_xml_element()
        assert xml["_name"] == "Row"
        assert xml["_attrs"]["ListType"] == "NAVAL_INFRASTRUCTURE"
        assert xml["_attrs"]["LeaderType"] == "TRAIT_LEADER_FOCUS_NAVAL"
        assert xml["_attrs"]["System"] == "Infrastructure"

    def test_ai_favored_item_node_creation(self):
        """Test AiFavoredItemNode creates correct structure."""
        node = AiFavoredItemNode(
            list_type="NAVAL_INFRASTRUCTURE", item="BUILDING_WHARF", favored=True
        )
        xml = node.to_xml_element()
        assert xml["_name"] == "Row"
        assert xml["_attrs"]["ListType"] == "NAVAL_INFRASTRUCTURE"
        assert xml["_attrs"]["Item"] == "BUILDING_WHARF"
        assert xml["_attrs"]["Favored"] == "true"

    def test_ai_favored_item_node_value_field(self):
        """Test AiFavoredItemNode with value and string_val."""
        node = AiFavoredItemNode(
            list_type="NAVAL_INFRASTRUCTURE",
            item="BUILDING_WHARF",
            favored=True,
            value=25,
            string_val="Maritime Power",
            tooltip_string="LOC_TOOLTIP_NAVAL_INFRASTRUCTURE",
        )
        xml = node.to_xml_element()
        assert xml["_name"] == "Row"
        assert xml["_attrs"]["ListType"] == "NAVAL_INFRASTRUCTURE"
        assert xml["_attrs"]["Item"] == "BUILDING_WHARF"
        assert xml["_attrs"]["Favored"] == "true"
        assert xml["_attrs"]["Value"] == "25"
        assert xml["_attrs"]["StringVal"] == "Maritime Power"
        assert xml["_attrs"]["TooltipString"] == "LOC_TOOLTIP_NAVAL_INFRASTRUCTURE"

    def test_leader_civ_priority_node_creation(self):
        """Test LeaderCivPriorityNode creates correct structure."""
        node = LeaderCivPriorityNode(
            civilization_type="CIVILIZATION_CARTHAGE",
            leader_type="TRAIT_LEADER_FOCUS_NAVAL",
            priority=50,
        )
        xml = node.to_xml_element()
        assert xml["_name"] == "Row"
        assert xml["_attrs"]["CivilizationType"] == "CIVILIZATION_CARTHAGE"
        assert xml["_attrs"]["LeaderType"] == "TRAIT_LEADER_FOCUS_NAVAL"
        assert xml["_attrs"]["Priority"] == "50"


class TestDatabaseNodeAiIntegration:
    """Test DatabaseNode integration of AI configuration nodes."""

    def test_database_node_ai_list_types(self):
        """Test DatabaseNode with AI list types."""
        db = DatabaseNode({
            'ai_list_types': [
                AiListTypeNode(list_type="NAVAL_INFRASTRUCTURE"),
                AiListTypeNode(list_type="COMMERCIAL_FOCUS"),
            ]
        })
        xml = db.to_xml_element()
        assert "Database" in xml
        assert "AiListTypes" in xml["Database"]
        assert len(xml["Database"]["AiListTypes"]) == 2

    def test_database_node_ai_lists(self):
        """Test DatabaseNode with AI lists."""
        db = DatabaseNode({
            'ai_lists': [
                AiListNode(
                    list_type="NAVAL_INFRASTRUCTURE",
                    leader_type="TRAIT_LEADER_FOCUS_NAVAL",
                    system="Infrastructure",
                )
            ]
        })
        xml = db.to_xml_element()
        assert "Database" in xml
        assert "AiLists" in xml["Database"]
        assert xml["Database"]["AiLists"][0]["_attrs"]["System"] == "Infrastructure"

    def test_database_node_ai_favored_items(self):
        """Test DatabaseNode with AI favored items."""
        db = DatabaseNode({
            'ai_favored_items': [
                AiFavoredItemNode(
                    list_type="NAVAL_INFRASTRUCTURE", item="BUILDING_WHARF", favored=True
                )
            ]
        })
        xml = db.to_xml_element()
        assert "Database" in xml
        assert "AiFavoredItems" in xml["Database"]
        assert xml["Database"]["AiFavoredItems"][0]["_attrs"]["Favored"] == "true"

    def test_database_node_leader_civ_priorities(self):
        """Test DatabaseNode with leader civilization priorities."""
        db = DatabaseNode({
            'leader_civ_priorities': [
                LeaderCivPriorityNode(
                    civilization_type="CIVILIZATION_CARTHAGE",
                    leader_type="TRAIT_LEADER_FOCUS_NAVAL",
                    priority=50,
                )
            ]
        })
        xml = db.to_xml_element()
        assert "Database" in xml
        assert "LeaderCivPriorities" in xml["Database"]
        assert xml["Database"]["LeaderCivPriorities"][0]["_attrs"]["Priority"] == "50"

    def test_database_node_complete_ai_configuration(self):
        """Test DatabaseNode with complete AI configuration."""
        db = DatabaseNode({
            'ai_list_types': [AiListTypeNode(list_type="NAVAL_INFRASTRUCTURE")],
            'ai_lists': [
                AiListNode(
                    list_type="NAVAL_INFRASTRUCTURE",
                    leader_type="TRAIT_LEADER_FOCUS_NAVAL",
                    system="Infrastructure",
                )
            ],
            'ai_favored_items': [
                AiFavoredItemNode(
                    list_type="NAVAL_INFRASTRUCTURE", item="BUILDING_WHARF", favored=True
                ),
                AiFavoredItemNode(
                    list_type="NAVAL_INFRASTRUCTURE",
                    item="BUILDING_LIGHTHOUSE",
                    favored=True,
                ),
            ],
            'leader_civ_priorities': [
                LeaderCivPriorityNode(
                    civilization_type="CIVILIZATION_CARTHAGE",
                    leader_type="TRAIT_LEADER_FOCUS_NAVAL",
                    priority=50,
                )
            ],
        })
        xml = db.to_xml_element()
        assert "Database" in xml
        db_content = xml["Database"]
        assert "AiListTypes" in db_content
        assert "AiLists" in db_content
        assert "AiFavoredItems" in db_content
        assert "LeaderCivPriorities" in db_content
        assert len(db_content["AiFavoredItems"]) == 2


class TestCarthageAiPattern:
    """Test that our nodes match Carthage AI configuration patterns."""

    def test_carthage_ai_list_pattern(self):
        """Test AI list matches Carthage pattern."""
        # Carthage has:
        # <AiLists>
        #   <Row ListType="Carthaginian_Favoured_Infrastructure" LeaderType="TRAIT_LEADER_FOCUS_NAVAL" System="Infrastructure"/>
        # </AiLists>

        node = AiListNode(
            list_type="Carthaginian_Favoured_Infrastructure",
            leader_type="TRAIT_LEADER_FOCUS_NAVAL",
            system="Infrastructure",
        )
        xml = node.to_xml_element()
        assert xml["_attrs"]["ListType"] == "Carthaginian_Favoured_Infrastructure"
        assert xml["_attrs"]["LeaderType"] == "TRAIT_LEADER_FOCUS_NAVAL"
        assert xml["_attrs"]["System"] == "Infrastructure"

    def test_carthage_ai_favored_items_pattern(self):
        """Test AI favored items matches Carthage pattern."""
        # Carthage has multiple favored items like:
        # <Row ListType="Carthaginian_Favoured_Infrastructure" Item="BUILDING_WHARF" Favored="true"/>

        node = AiFavoredItemNode(
            list_type="Carthaginian_Favoured_Infrastructure",
            item="BUILDING_WHARF",
            favored=True,
        )
        xml = node.to_xml_element()
        assert xml["_attrs"]["Favored"] == "true"
        assert xml["_attrs"]["Item"] == "BUILDING_WHARF"

    def test_carthage_leader_civ_priority_pattern(self):
        """Test leader civ priority matches Carthage pattern."""
        # Carthage has:
        # <Row CivilizationType="CIVILIZATION_CARTHAGE" LeaderType="TRAIT_LEADER_FOCUS_NAVAL" Priority="50"/>

        node = LeaderCivPriorityNode(
            civilization_type="CIVILIZATION_CARTHAGE",
            leader_type="TRAIT_LEADER_FOCUS_NAVAL",
            priority=50,
        )
        xml = node.to_xml_element()
        assert xml["_attrs"]["CivilizationType"] == "CIVILIZATION_CARTHAGE"
        assert xml["_attrs"]["LeaderType"] == "TRAIT_LEADER_FOCUS_NAVAL"
        assert xml["_attrs"]["Priority"] == "50"
