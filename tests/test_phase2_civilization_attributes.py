"""Tests for Phase 2: Civilization attributes enhancement."""

import pytest
from civ7_modding_tools import CivilizationBuilder
from civ7_modding_tools.nodes import CivilizationNode


class TestCivilizationAttributesPhase2:
    """Test new civilization attributes added in Phase 2."""

    def test_civilization_description_attribute(self):
        """Test that CivilizationNode supports description attribute."""
        node = CivilizationNode()
        node.civilization_type = "CIVILIZATION_CARTHAGE"
        node.description = "LOC_CIVILIZATION_CARTHAGE_DESCRIPTION"
        
        assert node.description == "LOC_CIVILIZATION_CARTHAGE_DESCRIPTION"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "Description" in xml['_attrs']
        assert xml['_attrs']['Description'] == "LOC_CIVILIZATION_CARTHAGE_DESCRIPTION"

    def test_civilization_unique_culture_progression_tree_attribute(self):
        """Test that CivilizationNode supports unique_culture_progression_tree attribute."""
        node = CivilizationNode()
        node.civilization_type = "CIVILIZATION_CARTHAGE"
        node.unique_culture_progression_tree = "TREE_CIVICS_AQ_CARTHAGE"
        
        assert node.unique_culture_progression_tree == "TREE_CIVICS_AQ_CARTHAGE"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "UniqueCultureProgressionTree" in xml['_attrs']
        assert xml['_attrs']['UniqueCultureProgressionTree'] == "TREE_CIVICS_AQ_CARTHAGE"

    def test_civilization_random_city_name_depth_attribute(self):
        """Test that CivilizationNode supports random_city_name_depth attribute."""
        node = CivilizationNode()
        node.civilization_type = "CIVILIZATION_CARTHAGE"
        node.random_city_name_depth = 10
        
        assert node.random_city_name_depth == 10
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "RandomCityNameDepth" in xml['_attrs']
        assert xml['_attrs']['RandomCityNameDepth'] == "10"

    def test_civilization_builder_with_all_new_attributes(self):
        """Test CivilizationBuilder can pass all new attributes through civilization dict."""
        builder = CivilizationBuilder()
        builder.civilization_type = 'CIVILIZATION_CARTHAGE'
        builder.civilization = {
            'description': 'LOC_CIVILIZATION_CARTHAGE_DESCRIPTION',
            'unique_culture_progression_tree': 'TREE_CIVICS_AQ_CARTHAGE',
            'random_city_name_depth': 10
        }
        
        files = builder.build()
        
        # Find the current.xml file
        current_file = [f for f in files if f.name == 'current.xml'][0]
        db = current_file.content
        
        # Check that civilization node has the new attributes
        assert len(db.civilizations) == 1
        civ = db.civilizations[0]
        
        assert civ.description == 'LOC_CIVILIZATION_CARTHAGE_DESCRIPTION'
        assert civ.unique_culture_progression_tree == 'TREE_CIVICS_AQ_CARTHAGE'
        assert civ.random_city_name_depth == 10

    def test_civilization_builder_matches_carthage_pattern(self):
        """Test that builder can create a civilization similar to Carthage."""
        builder = CivilizationBuilder()
        builder.civilization_type = 'CIVILIZATION_MY_CIV'
        builder.civilization_traits = ['TRAIT_ECONOMIC']
        builder.civilization = {
            'description': 'LOC_CIVILIZATION_MY_CIV_DESCRIPTION',
            'unique_culture_progression_tree': 'TREE_CIVICS_AQ_MY_CIV',
            'random_city_name_depth': 30,
            'base_tourism': 0,
        }
        builder.localizations = [
            {
                'name': 'My Civilization',
                'full_name': 'The Great Civilization of Mine',
                'description': 'A powerful civilization',
                'city_names': ['Capital', 'Second City', 'Third City']
            }
        ]
        
        files = builder.build()
        current_file = [f for f in files if f.name == 'current.xml'][0]
        db = current_file.content
        
        civ = db.civilizations[0]
        assert civ.civilization_type == 'CIVILIZATION_MY_CIV'
        assert civ.description == 'LOC_CIVILIZATION_MY_CIV_DESCRIPTION'
        assert civ.unique_culture_progression_tree == 'TREE_CIVICS_AQ_MY_CIV'
        assert civ.random_city_name_depth == 30
        assert civ.base_tourism == 0
        
        # Should have 3 city names
        assert len(db.city_names) == 3

    def test_new_attributes_are_optional(self):
        """Test that new attributes are optional and don't break existing code."""
        builder = CivilizationBuilder()
        builder.civilization_type = 'CIVILIZATION_SIMPLE'
        
        files = builder.build()
        
        # Should still build successfully
        assert len(files) == 5
        
        current_file = [f for f in files if f.name == 'current.xml'][0]
        db = current_file.content
        civ = db.civilizations[0]
        
        # New attributes should be None (and thus omitted from XML)
        assert civ.description is None
        assert civ.unique_culture_progression_tree is None
        assert civ.random_city_name_depth is None
        
        # Verify they don't appear in XML
        xml = civ.to_xml_element()
        assert 'Description' not in xml['_attrs']
        assert 'UniqueCultureProgressionTree' not in xml['_attrs']
        assert 'RandomCityNameDepth' not in xml['_attrs']
