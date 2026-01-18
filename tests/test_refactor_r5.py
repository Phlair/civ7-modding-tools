"""Tests for Refactor 5: Localization Integration.

Tests the get_nodes() methods on all localization classes,
verifying proper conversion to EnglishText node data.
"""

import pytest

from civ7_modding_tools.localizations import (
    CivilizationLocalization,
    UnitLocalization,
    ConstructibleLocalization,
    ProgressionTreeLocalization,
    ProgressionTreeNodeLocalization,
    ModifierLocalization,
    TraditionLocalization,
    LeaderUnlockLocalization,
    CivilizationUnlockLocalization,
    UniqueQuarterLocalization,
)


class TestCivilizationLocalization:
    """Test CivilizationLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = CivilizationLocalization()
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        assert nodes == []
    
    def test_name_only(self):
        """Single name field generates correct node."""
        loc = CivilizationLocalization(name="Rome")
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        assert len(nodes) == 1
        assert nodes[0]["tag"] == "LOC_CIVILIZATION_ROME_NAME"
        assert nodes[0]["text"] == "Rome"
    
    def test_full_civilization(self):
        """Full civilization localization generates all nodes."""
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient empire",
            full_name="The Roman Empire",
            adjective="Roman",
            city_names=["Rome", "Milan", "Venice"]
        )
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        
        # Should have 7 nodes: name, description, full_name, adjective, 3 cities
        assert len(nodes) == 7
        
        tags = [n["tag"] for n in nodes]
        assert "LOC_CIVILIZATION_ROME_NAME" in tags
        assert "LOC_CIVILIZATION_ROME_DESCRIPTION" in tags
        assert "LOC_CIVILIZATION_ROME_FULL_NAME" in tags
        assert "LOC_CIVILIZATION_ROME_ADJECTIVE" in tags
        assert "LOC_CITY_ROME_0" in tags
        assert "LOC_CITY_ROME_1" in tags
        assert "LOC_CITY_ROME_2" in tags
    
    def test_multiple_cities(self):
        """Multiple cities generate correct indexed nodes."""
        loc = CivilizationLocalization(
            city_names=["Rome", "Milan", "Venice", "Naples"]
        )
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        assert len(nodes) == 4
        
        for i, city in enumerate(["Rome", "Milan", "Venice", "Naples"]):
            assert nodes[i]["tag"] == f"LOC_CITY_ROME_{i}"
            assert nodes[i]["text"] == city


class TestUnitLocalization:
    """Test UnitLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = UnitLocalization()
        nodes = loc.get_nodes("UNIT_ARCHER")
        assert nodes == []
    
    def test_full_unit(self):
        """Full unit localization generates all nodes."""
        loc = UnitLocalization(
            name="Archer",
            description="Ranged unit",
            unique_name="Roman Archer"
        )
        nodes = loc.get_nodes("UNIT_ARCHER")
        
        assert len(nodes) == 3
        tags = [n["tag"] for n in nodes]
        assert "LOC_UNIT_ARCHER_NAME" in tags
        assert "LOC_UNIT_ARCHER_DESCRIPTION" in tags
        assert "LOC_UNIT_ARCHER_UNIQUE_NAME" in tags


class TestConstructibleLocalization:
    """Test ConstructibleLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = ConstructibleLocalization()
        nodes = loc.get_nodes("BUILDING_LIBRARY")
        assert nodes == []
    
    def test_building_localization(self):
        """Building localization generates proper nodes."""
        loc = ConstructibleLocalization(
            name="Library",
            description="Science building",
            unique_name="Roman Library"
        )
        nodes = loc.get_nodes("BUILDING_LIBRARY")
        
        assert len(nodes) == 3
        assert nodes[0]["tag"] == "LOC_CONSTRUCTIBLE_LIBRARY_NAME"
        assert nodes[1]["tag"] == "LOC_CONSTRUCTIBLE_LIBRARY_DESCRIPTION"
        assert nodes[2]["tag"] == "LOC_CONSTRUCTIBLE_LIBRARY_UNIQUE_NAME"


class TestProgressionTreeLocalization:
    """Test ProgressionTreeLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = ProgressionTreeLocalization()
        nodes = loc.get_nodes("PROGRESSION_TREE_TECH")
        assert nodes == []
    
    def test_progression_tree(self):
        """Progression tree generates proper nodes."""
        loc = ProgressionTreeLocalization(
            name="Technology Tree",
            description="Research tree"
        )
        nodes = loc.get_nodes("PROGRESSION_TREE_TECH")
        
        assert len(nodes) == 2
        assert "LOC_PROGRESSION_PROGRESSION_TREE_TECH_NAME" in [n["tag"] for n in nodes]
        assert "LOC_PROGRESSION_PROGRESSION_TREE_TECH_DESCRIPTION" in [n["tag"] for n in nodes]


class TestProgressionTreeNodeLocalization:
    """Test ProgressionTreeNodeLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = ProgressionTreeNodeLocalization()
        nodes = loc.get_nodes("TECH_WRITING")
        assert nodes == []
    
    def test_full_node(self):
        """Full progression node generates all nodes."""
        loc = ProgressionTreeNodeLocalization(
            name="Writing",
            description="Unlock writing",
            quote="The pen is mightier than the sword"
        )
        nodes = loc.get_nodes("TECH_WRITING")
        
        assert len(nodes) == 3
        tags = [n["tag"] for n in nodes]
        assert "LOC_TECH_WRITING_NAME" in tags
        assert "LOC_TECH_WRITING_DESCRIPTION" in tags
        assert "LOC_TECH_WRITING_QUOTE" in tags


class TestModifierLocalization:
    """Test ModifierLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = ModifierLocalization()
        nodes = loc.get_nodes("MODIFIER_BONUS")
        assert nodes == []
    
    def test_modifier(self):
        """Modifier generates proper nodes."""
        loc = ModifierLocalization(
            name="Bonus Effect",
            description="Grants bonus"
        )
        nodes = loc.get_nodes("MODIFIER_BONUS")
        
        assert len(nodes) == 2
        assert nodes[0]["tag"] == "LOC_MODIFIER_MODIFIER_BONUS_NAME"
        assert nodes[1]["tag"] == "LOC_MODIFIER_MODIFIER_BONUS_DESCRIPTION"


class TestTraditionLocalization:
    """Test TraditionLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = TraditionLocalization()
        nodes = loc.get_nodes("TRADITION_MILITARY")
        assert nodes == []
    
    def test_tradition(self):
        """Tradition generates proper nodes."""
        loc = TraditionLocalization(
            name="Military Tradition",
            description="Focus on military"
        )
        nodes = loc.get_nodes("TRADITION_MILITARY")
        
        assert len(nodes) == 2
        assert "LOC_TRADITION_MILITARY_NAME" in [n["tag"] for n in nodes]


class TestLeaderUnlockLocalization:
    """Test LeaderUnlockLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = LeaderUnlockLocalization()
        nodes = loc.get_nodes("LEADER_CAESAR")
        assert nodes == []
    
    def test_leader_unlock(self):
        """Leader unlock generates proper nodes."""
        loc = LeaderUnlockLocalization(
            leader_name="Julius Caesar",
            description="Great Roman general"
        )
        nodes = loc.get_nodes("LEADER_CAESAR")
        
        assert len(nodes) == 2
        assert nodes[0]["tag"] == "LOC_LEADER_CAESAR_NAME"
        assert nodes[0]["text"] == "Julius Caesar"
        assert nodes[1]["tag"] == "LOC_LEADER_CAESAR_DESCRIPTION"


class TestCivilizationUnlockLocalization:
    """Test CivilizationUnlockLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = CivilizationUnlockLocalization()
        nodes = loc.get_nodes("CIV_UNLOCK_AGE")
        assert nodes == []
    
    def test_civ_unlock(self):
        """Civilization unlock generates proper nodes."""
        loc = CivilizationUnlockLocalization(
            name="Age Unlock",
            description="Unlock in age"
        )
        nodes = loc.get_nodes("CIV_UNLOCK_AGE")
        
        assert len(nodes) == 2
        assert "LOC_UNLOCK_CIV_UNLOCK_AGE_NAME" in [n["tag"] for n in nodes]


class TestUniqueQuarterLocalization:
    """Test UniqueQuarterLocalization.get_nodes()."""
    
    def test_empty_localization(self):
        """Empty localization returns no nodes."""
        loc = UniqueQuarterLocalization()
        nodes = loc.get_nodes("QUARTER_COLOSSEUM")
        assert nodes == []
    
    def test_unique_quarter(self):
        """Unique quarter generates proper nodes."""
        loc = UniqueQuarterLocalization(
            name="Colosseum Quarter",
            description="Roman entertainment"
        )
        nodes = loc.get_nodes("QUARTER_COLOSSEUM")
        
        assert len(nodes) == 2
        assert nodes[0]["tag"] == "LOC_QUARTER_QUARTER_COLOSSEUM_NAME"
        assert nodes[1]["tag"] == "LOC_QUARTER_QUARTER_COLOSSEUM_DESCRIPTION"


class TestLocalizationIntegration:
    """Integration tests for multiple localizations."""
    
    def test_all_localizations_implement_get_nodes(self):
        """All localization classes have get_nodes() method."""
        localization_classes = [
            CivilizationLocalization,
            UnitLocalization,
            ConstructibleLocalization,
            ProgressionTreeLocalization,
            ProgressionTreeNodeLocalization,
            ModifierLocalization,
            TraditionLocalization,
            LeaderUnlockLocalization,
            CivilizationUnlockLocalization,
            UniqueQuarterLocalization,
        ]
        
        for cls in localization_classes:
            loc = cls()
            assert hasattr(loc, "get_nodes")
            assert callable(loc.get_nodes)
    
    def test_get_nodes_returns_list(self):
        """All get_nodes() methods return lists."""
        locs = [
            CivilizationLocalization(name="Test"),
            UnitLocalization(name="Test"),
            ConstructibleLocalization(name="Test"),
            ProgressionTreeLocalization(name="Test"),
            ProgressionTreeNodeLocalization(name="Test"),
            ModifierLocalization(name="Test"),
            TraditionLocalization(name="Test"),
            LeaderUnlockLocalization(leader_name="Test"),
            CivilizationUnlockLocalization(name="Test"),
            UniqueQuarterLocalization(name="Test"),
        ]
        
        for loc in locs:
            nodes = loc.get_nodes("TEST_ENTITY")
            assert isinstance(nodes, list)
            if nodes:  # If any nodes exist
                assert isinstance(nodes[0], dict)
                assert "tag" in nodes[0]
                assert "text" in nodes[0]
    
    def test_node_structure(self):
        """All nodes have correct structure with tag and text."""
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient empire",
            full_name="Roman Empire",
            adjective="Roman"
        )
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        
        for node in nodes:
            assert isinstance(node, dict)
            assert "tag" in node
            assert "text" in node
            assert isinstance(node["tag"], str)
            assert isinstance(node["text"], str)
            assert len(node["tag"]) > 0
            assert len(node["text"]) > 0
    
    def test_partial_localization(self):
        """Partial localization fields skip empty values."""
        loc = CivilizationLocalization(
            name="Rome",
            description=None,
            full_name="Roman Empire",
            adjective=None,
            city_names=None
        )
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        
        # Should only have 2 nodes: name and full_name
        assert len(nodes) == 2
        tags = [n["tag"] for n in nodes]
        assert "LOC_CIVILIZATION_ROME_NAME" in tags
        assert "LOC_CIVILIZATION_ROME_FULL_NAME" in tags


class TestLocalizationWithVariations:
    """Test edge cases and special scenarios."""
    
    def test_civilization_with_empty_city_names_list(self):
        """Empty city_names list generates no city nodes."""
        loc = CivilizationLocalization(
            name="Rome",
            city_names=[]  # Empty list
        )
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        
        # Only name should be present
        assert len(nodes) == 1
        assert nodes[0]["tag"] == "LOC_CIVILIZATION_ROME_NAME"
    
    def test_entity_id_with_different_formats(self):
        """Different entity ID formats are handled correctly."""
        loc = CivilizationLocalization(name="Custom")
        
        # Test various formats - trim() should normalize them
        for entity_id in ["CIVILIZATION_CUSTOM", "civ_custom", "CUSTOM"]:
            nodes = loc.get_nodes(entity_id)
            assert len(nodes) == 1
            # All should normalize to "CUSTOM" after trimming
            assert "CUSTOM" in nodes[0]["tag"]
    
    def test_localization_with_special_characters(self):
        """Text with special characters is preserved."""
        loc = CivilizationLocalization(
            name="Rome's Empire",
            description="An \"Empire\" (really!)",
            full_name="The Roman Empire & Friends"
        )
        nodes = loc.get_nodes("CIVILIZATION_ROME")
        
        assert len(nodes) == 3
        assert nodes[0]["text"] == "Rome's Empire"
        assert nodes[1]["text"] == 'An "Empire" (really!)'
        assert nodes[2]["text"] == "The Roman Empire & Friends"
    
    def test_multiple_consecutive_spaces(self):
        """Text with multiple spaces is preserved."""
        loc = UnitLocalization(
            name="  Archer  ",
            description="Ranged   unit"
        )
        nodes = loc.get_nodes("UNIT_ARCHER")
        
        # Pydantic should preserve the exact strings
        assert nodes[0]["text"] == "  Archer  "
        assert nodes[1]["text"] == "Ranged   unit"
