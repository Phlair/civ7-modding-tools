"""Tests for Phase 3: Start biases (already implemented, just verifying)."""

import pytest
from civ7_modding_tools import CivilizationBuilder
from civ7_modding_tools.nodes import StartBiasBiomeNode, StartBiasTerrainNode, StartBiasAdjacentToCoastNode


class TestStartBiasesPhase3:
    """Test start biases functionality (already implemented)."""

    def test_start_bias_biomes_in_builder(self):
        """Test that CivilizationBuilder supports start bias biomes."""
        builder = CivilizationBuilder()
        builder.civilization_type = 'CIVILIZATION_TEST'
        builder.start_bias_biomes = [
            {'biome': 'BIOME_GRASSLAND', 'bias': 3},
            {'biome': 'BIOME_PLAINS', 'bias': 2}
        ]
        
        files = builder.build()
        current_file = [f for f in files if f.name == 'current.xml'][0]
        db = current_file.content
        
        assert len(db.start_bias_biomes) == 2
        assert db.start_bias_biomes[0].biome == 'BIOME_GRASSLAND'
        assert db.start_bias_biomes[0].bias == 3
        assert db.start_bias_biomes[1].biome == 'BIOME_PLAINS'
        assert db.start_bias_biomes[1].bias == 2

    def test_start_bias_terrains_in_builder(self):
        """Test that CivilizationBuilder supports start bias terrains."""
        builder = CivilizationBuilder()
        builder.civilization_type = 'CIVILIZATION_TEST'
        builder.start_bias_terrains = [
            {'terrain': 'TERRAIN_COAST', 'bias': 5}
        ]
        
        files = builder.build()
        current_file = [f for f in files if f.name == 'current.xml'][0]
        db = current_file.content
        
        assert len(db.start_bias_terrains) == 1
        assert db.start_bias_terrains[0].terrain == 'TERRAIN_COAST'
        assert db.start_bias_terrains[0].bias == 5

    def test_start_bias_adjacent_coast_node(self):
        """Test StartBiasAdjacentToCoastNode serialization."""
        node = StartBiasAdjacentToCoastNode()
        node.civilization_type = 'CIVILIZATION_CARTHAGE'
        node.bias = 50
        
        xml = node.to_xml_element()
        assert xml is not None
        assert xml['_attrs']['CivilizationType'] == 'CIVILIZATION_CARTHAGE'
        assert xml['_attrs']['Bias'] == '50'

    def test_multiple_start_biases_carthage_pattern(self):
        """Test creating a civilization with multiple start biases like Carthage."""
        builder = CivilizationBuilder()
        builder.civilization_type = 'CIVILIZATION_COASTAL_CIV'
        builder.start_bias_biomes = [
            {'biome': 'BIOME_TEMPERATE', 'bias': 2}
        ]
        builder.start_bias_terrains = [
            {'terrain': 'TERRAIN_COAST', 'bias': 3},
            {'terrain': 'TERRAIN_OCEAN', 'bias': 1}
        ]
        
        files = builder.build()
        current_file = [f for f in files if f.name == 'current.xml'][0]
        db = current_file.content
        
        # Verify all biases are present
        assert len(db.start_bias_biomes) == 1
        assert len(db.start_bias_terrains) == 2
        
        # Check they have civilization_type set
        assert db.start_bias_biomes[0].civilization_type == 'CIVILIZATION_COASTAL_CIV'
        assert db.start_bias_terrains[0].civilization_type == 'CIVILIZATION_COASTAL_CIV'
        assert db.start_bias_terrains[1].civilization_type == 'CIVILIZATION_COASTAL_CIV'
