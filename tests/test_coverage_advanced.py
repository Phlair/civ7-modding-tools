"""Tests for action_groups and advanced builder scenarios for coverage."""

import pytest
from civ7_modding_tools.nodes.action_groups import CriteriaNode, ActionGroupNode
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
)
from civ7_modding_tools.constants import Trait, Age


# ============================================================================
# ActionGroup and Criteria Node Tests (currently 34% coverage)
# ============================================================================

class TestCriteriaNode:
    """Tests for CriteriaNode class."""
    
    def test_criteria_node_initialization(self):
        """Test CriteriaNode initializes with UUID."""
        node = CriteriaNode()
        assert node._name == "Criteria"
        assert node.id is not None
        assert isinstance(node.id, str)
        assert len(node.id) > 0
    
    def test_criteria_node_with_payload(self):
        """Test CriteriaNode initializes with payload."""
        payload = {
            'id': 'test-id-123',
            'any': True,
            'ages': ['AGE_CLASSICAL', 'AGE_MEDIEVAL']
        }
        node = CriteriaNode(payload)
        assert node.id == 'test-id-123'
        assert node.any is True
        assert node.ages == ['AGE_CLASSICAL', 'AGE_MEDIEVAL']
    
    def test_criteria_node_to_xml_element_empty(self):
        """Test CriteriaNode XML generation with no ages (AlwaysMet)."""
        node = CriteriaNode()
        xml = node.to_xml_element()
        
        assert xml['_name'] == 'Criteria'
        assert 'id' in xml['_attrs']
        assert 'AlwaysMet' in xml['_content']
    
    def test_criteria_node_to_xml_element_with_ages(self):
        """Test CriteriaNode XML generation with ages."""
        node = CriteriaNode({
            'ages': ['AGE_ANTIQUITY', 'AGE_CLASSICAL']
        })
        xml = node.to_xml_element()
        
        assert xml['_name'] == 'Criteria'
        assert 'AgeInUse' in xml['_content']
        assert len(xml['_content']['AgeInUse']) == 2
    
    def test_criteria_node_to_xml_element_with_any(self):
        """Test CriteriaNode XML generation with 'any' flag."""
        node = CriteriaNode({
            'any': True,
            'ages': ['AGE_MODERN', 'AGE_ATOMIC']
        })
        xml = node.to_xml_element()
        
        assert xml['_attrs'].get('any') == 'true'
    
    def test_criteria_node_fill_method(self):
        """Test CriteriaNode fill() method."""
        node = CriteriaNode()
        result = node.fill({
            'any': True,
            'ages': ['AGE_RENAISSANCE']
        })
        
        assert result is node
        assert node.any is True
        assert 'AGE_RENAISSANCE' in node.ages


class TestActionGroupNode:
    """Tests for ActionGroupNode class."""
    
    def test_action_group_node_initialization(self):
        """Test ActionGroupNode initializes with defaults."""
        node = ActionGroupNode()
        assert node._name == 'ActionGroup'
        assert node.id is not None
        assert node.scope == 'game'
        assert isinstance(node.criteria, CriteriaNode)
    
    def test_action_group_node_with_payload(self):
        """Test ActionGroupNode initializes with payload."""
        payload = {
            'id': 'action-group-1',
            'scope': 'shell'
        }
        node = ActionGroupNode(payload)
        assert node.id == 'action-group-1'
        assert node.scope == 'shell'
    
    def test_action_group_node_to_xml_element(self):
        """Test ActionGroupNode XML generation."""
        node = ActionGroupNode({
            'id': 'test-ag',
            'scope': 'game'
        })
        xml = node.to_xml_element()
        
        assert xml['_name'] == 'ActionGroup'
        assert xml['_attrs']['id'] == 'test-ag'
        assert xml['_attrs']['scope'] == 'game'
        assert 'Criteria' in xml['_content']
    
    def test_action_group_node_with_complex_criteria(self):
        """Test ActionGroupNode with complex criteria."""
        criteria = CriteriaNode({
            'any': True,
            'ages': ['AGE_CLASSICAL', 'AGE_MEDIEVAL', 'AGE_RENAISSANCE']
        })
        node = ActionGroupNode({
            'id': 'complex-ag',
            'scope': 'shell',
            'criteria': criteria
        })
        xml = node.to_xml_element()
        
        criteria_xml = xml['_content']['Criteria']
        assert criteria_xml['_attrs'].get('any') == 'true'
        assert len(criteria_xml['_content']['AgeInUse']) == 3
    
    def test_action_group_node_fill_method(self):
        """Test ActionGroupNode fill() method."""
        node = ActionGroupNode()
        result = node.fill({
            'id': 'filled-ag',
            'scope': 'shell'
        })
        
        assert result is node
        assert node.id == 'filled-ag'
        assert node.scope == 'shell'


# ============================================================================
# Advanced CivilizationBuilder Tests (covering missing lines)
# ============================================================================

class TestCivilizationBuilderAdvanced:
    """Advanced tests for CivilizationBuilder edge cases."""
    
    def test_civilization_with_start_bias_biomes(self):
        """Test civilization with start bias biomes."""
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_CUSTOM',
            'civilization': {},
            'start_bias_biomes': [
                {'biome': 'BIOME_GRASSLAND', 'bias': 5},
                {'biome': 'BIOME_PLAINS', 'bias': 3}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0
        assert any(f.name == 'current.xml' for f in files)
    
    def test_civilization_with_start_bias_terrains(self):
        """Test civilization with start bias terrains."""
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_DESERT',
            'civilization': {},
            'start_bias_terrains': [
                {'terrain': 'TERRAIN_DESERT', 'bias': 8},
                {'terrain': 'TERRAIN_SAND', 'bias': 5}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0
    
    def test_civilization_with_multiple_city_names(self):
        """Test civilization with multiple city names from localizations."""
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_ROME',
            'civilization': {},
            'localizations': [{
                'city_names': ['Rome', 'Milan', 'Venice', 'Florence', 'Genoa']
            }]
        })
        
        files = builder.build()
        current_xml = [f for f in files if f.name == 'current.xml'][0]
        
        from civ7_modding_tools.nodes import DatabaseNode
        assert isinstance(current_xml.content, DatabaseNode)
        assert len(current_xml.content.city_names) == 5
    
    def test_civilization_with_empty_city_names(self):
        """Test civilization without city names."""
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_SPARTA',
            'civilization': {}
        })
        
        files = builder.build()
        current_xml = [f for f in files if f.name == 'current.xml'][0]
        
        from civ7_modding_tools.nodes import DatabaseNode
        assert isinstance(current_xml.content, DatabaseNode)
        assert len(current_xml.content.city_names) == 0
    
    def test_civilization_with_vis_art_modifications(self):
        """Test civilization with visual art modifications."""
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_CUSTOM',
            'civilization': {},
            'vis_art_building_culture': 'BUILDING_CULTURE_CUSTOM',
            'vis_art_unit_culture': 'UNIT_CULTURE_CUSTOM'
        })
        
        files = builder.build()
        assert len(files) > 0


# ============================================================================
# Advanced UnitBuilder Tests (covering missing lines)
# ============================================================================

class TestUnitBuilderAdvanced:
    """Advanced tests for UnitBuilder edge cases."""
    
    def test_unit_with_unit_replaces(self):
        """Test unit with unit replaces configuration."""
        builder = UnitBuilder()
        builder.fill({
            'unit_type': 'UNIT_CUSTOM_KNIGHT',
            'unit': {},
            'unit_replaces': [
                {'replaces_unit_type': 'UNIT_KNIGHT'}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0
    
    def test_unit_with_combat_ranges(self):
        """Test unit with combat ranges."""
        builder = UnitBuilder()
        builder.fill({
            'unit_type': 'UNIT_CATAPULT',
            'unit': {},
            'combat_ranges': [
                {'range': 3, 'damage': 30}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0
    
    def test_unit_with_origin_boosts(self):
        """Test unit with origin boosts."""
        builder = UnitBuilder()
        builder.fill({
            'unit_type': 'UNIT_ELITE_WARRIOR',
            'unit': {},
            'origin_boosts': [
                {'boost_type': 'STRENGTH', 'amount': 2}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0


# ============================================================================
# Advanced ConstructibleBuilder Tests (covering missing lines)
# ============================================================================

class TestConstructibleBuilderAdvanced:
    """Advanced tests for ConstructibleBuilder edge cases."""
    
    def test_constructible_with_valid_districts(self):
        """Test constructible with valid districts constraint."""
        builder = ConstructibleBuilder()
        builder.fill({
            'constructible_type': 'BUILDING_LIBRARY',
            'constructible': {},
            'valid_districts': ['DISTRICT_CAMPUS', 'DISTRICT_HOLY_SITE']
        })
        
        files = builder.build()
        assert len(files) > 0
    
    def test_constructible_with_prerequisites(self):
        """Test constructible with prerequisites."""
        builder = ConstructibleBuilder()
        builder.fill({
            'constructible_type': 'BUILDING_UNIVERSITY',
            'constructible': {},
            'prerequisites': [
                {'prerequisite': 'BUILDING_LIBRARY'}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0
    
    def test_constructible_with_unlocks(self):
        """Test constructible with unlocks."""
        builder = ConstructibleBuilder()
        builder.fill({
            'constructible_type': 'BUILDING_SCHOOL',
            'constructible': {},
            'unlocks': [
                {'unlock_type': 'UNIT_SCHOLAR'}
            ]
        })
        
        files = builder.build()
        assert len(files) > 0


# ============================================================================
# Integration Tests for ActionGroup Bundle
# ============================================================================

class TestActionGroupBundleIntegration:
    """Tests for ActionGroupBundle integration with builders."""
    
    def test_builder_default_action_group_bundle(self):
        """Test builder has default ActionGroupBundle set to ALWAYS."""
        builder = CivilizationBuilder()
        assert builder.action_group_bundle is not None
        assert builder.action_group_bundle.action_group_id == 'ALWAYS'
    
    def test_builder_can_modify_action_group_bundle(self):
        """Test builder ActionGroupBundle can be modified."""
        builder = CivilizationBuilder()
        builder.action_group_bundle.action_group_id = 'AGE_CLASSICAL'
        
        assert builder.action_group_bundle.action_group_id == 'AGE_CLASSICAL'
    
    def test_multiple_builders_independent_action_groups(self):
        """Test multiple builders have independent action group bundles."""
        builder1 = CivilizationBuilder()
        builder2 = UnitBuilder()
        
        builder1.action_group_bundle.action_group_id = 'AGE_MEDIEVAL'
        builder2.action_group_bundle.action_group_id = 'AGE_MODERN'
        
        assert builder1.action_group_bundle.action_group_id == 'AGE_MEDIEVAL'
        assert builder2.action_group_bundle.action_group_id == 'AGE_MODERN'


# ============================================================================
# Edge Case Tests for Builder Robustness
# ============================================================================

class TestBuilderEdgeCasesRobustness:
    """Tests for edge cases and robustness."""
    
    def test_civilization_with_all_optional_fields(self):
        """Test civilization builder with all optional fields populated."""
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_MAXED',
            'civilization': {'base_tourism': 10, 'legacy_modifier': True},
            'civilization_traits': [Trait.ECONOMIC, Trait.MILITARY],
            'start_bias_biomes': [{'biome': 'BIOME_TUNDRA', 'bias': 2}],
            'start_bias_terrains': [{'terrain': 'TERRAIN_SNOW', 'bias': 3}],
            'localizations': [{
                'name': 'Maxed Out',
                'city_names': ['Capital', 'Secondary', 'Tertiary']
            }],
            'vis_art_building_culture': 'BUILDING_CULTURE_MAXED',
            'vis_art_unit_culture': 'UNIT_CULTURE_MAXED'
        })
        
        files = builder.build()
        assert len(files) == 6  # always, current, legacy, shell, icons, localization
    
    def test_unit_with_all_optional_fields(self):
        """Test unit builder with all optional fields populated."""
        builder = UnitBuilder()
        builder.fill({
            'unit_type': 'UNIT_ELITE_KNIGHT',
            'unit': {'combat': 30, 'health': 100},
            'unit_stats': [{'stat': 'strength', 'value': 15}],
            'unit_costs': [{'cost_type': 'production', 'amount': 100}],
            'unit_replaces': [{'replaces_unit_type': 'UNIT_KNIGHT'}],
            'combat_ranges': [{'range': 2, 'damage': 25}],
            'origin_boosts': [{'boost': 'experience', 'amount': 5}],
            'localizations': [{
                'name': 'Elite Knight',
                'description': 'A very strong knight unit'
            }]
        })
        
        files = builder.build()
        assert len(files) == 3
    
    def test_constructible_with_all_optional_fields(self):
        """Test constructible builder with all optional fields populated."""
        builder = ConstructibleBuilder()
        builder.fill({
            'constructible_type': 'BUILDING_MEGA_LIBRARY',
            'constructible': {'cost': 500, 'maintenance': 10},
            'yield_changes': [
                {'yield': 'science', 'amount': 10},
                {'yield': 'culture', 'amount': 5}
            ],
            'valid_districts': ['DISTRICT_CAMPUS', 'DISTRICT_INDUSTRIAL_ZONE'],
            'prerequisites': [{'prerequisite': 'BUILDING_LIBRARY'}],
            'unlocks': [{'unlock': 'UNIT_SCIENTIST'}],
            'localizations': [{
                'name': 'Mega Library',
                'description': 'Advanced research facility'
            }]
        })
        
        files = builder.build()
        assert len(files) == 3
    
    def test_builder_migrate_is_called(self):
        """Test that migrate() hook can be called on builders."""
        builder = CivilizationBuilder()
        result = builder.migrate()
        
        assert result is builder
    
    def test_builder_with_dict_creates_correctly(self):
        """Test builder initialization with dict."""
        data = {
            'civilization_type': 'CIVILIZATION_EGYPT',
            'civilization': {'base_tourism': 5}
        }
        
        builder = CivilizationBuilder()
        builder.fill(data)
        
        files = builder.build()
        assert len(files) > 0
    
    def test_builder_properties_are_mutable(self):
        """Test builder properties can be modified after creation."""
        builder = CivilizationBuilder()
        
        # Modify internal properties
        builder.civilization_type = 'CIV_NEW'
        builder.civilization = {'trait': 'value'}
        builder.civilization_traits = ['TRAIT_ECONOMIC']
        
        assert builder.civilization_type == 'CIV_NEW'
        assert builder.civilization == {'trait': 'value'}
        assert len(builder.civilization_traits) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
