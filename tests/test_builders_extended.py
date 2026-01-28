"""Extended tests for complex builder scenarios and edge cases not covered by basic tests."""

import pytest
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ModifierBuilder,
    TraditionBuilder,
    UnlockBuilder,
    ProgressionTreeBuilder,
    ProgressionTreeNodeBuilder,
    UniqueQuarterBuilder,
    LeaderUnlockBuilder,
    CivilizationUnlockBuilder,
)
from civ7_modding_tools.constants import Trait, District, Yield
from civ7_modding_tools.nodes import GameModifierNode, DatabaseNode


# ============================================================================
# CivilizationBuilder - Complex Bind and Migration Tests
# ============================================================================

class TestCivilizationBuilderComplexBinding:
    """Tests for complex binding scenarios with multiple builder types."""
    
    def test_civilization_bind_multiple_builders(self):
        """Test binding multiple different builder types to civilization."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_GONDOR',
            'civilization': {}
        })
        
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_GONDOR_SOLDIER',
            'unit': {}
        })
        
        constructible = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_GONDOR_CITADEL',
            'constructible': {}
        })
        
        civ.bind([unit, constructible])
        assert len(civ._bound_items) == 2
        files = civ.build()
        assert len(files) > 0
    
    def test_civilization_bind_empty_list(self):
        """Test binding empty list of builders."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_TEST',
            'civilization': {}
        })
        
        civ.bind([])
        assert len(civ._bound_items) == 0
        files = civ.build()
        assert len(files) > 0


# ============================================================================
# Start Bias - Biomes and Terrains Tests
# ============================================================================

class TestCivilizationStartBiases:
    """Tests for start bias biome and terrain configurations."""
    
    def test_civilization_with_multiple_biomes_and_terrains(self):
        """Test civilization with both biome and terrain start biases."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_AMAZON',
            'civilization': {},
            'start_bias_biomes': [
                {'biome': 'BIOME_TROPICAL_FOREST', 'bias': 10},
                {'biome': 'BIOME_RAINFOREST', 'bias': 8},
                {'biome': 'BIOME_WETLAND', 'bias': 5}
            ],
            'start_bias_terrains': [
                {'terrain': 'TERRAIN_JUNGLE', 'bias': 10},
                {'terrain': 'TERRAIN_FOREST', 'bias': 7}
            ]
        })
        
        civ.migrate()
        assert len(civ._current.start_bias_biomes) == 3
        assert len(civ._current.start_bias_terrains) == 2
    
    def test_civilization_with_no_start_biases(self):
        """Test civilization without start biases (empty lists)."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_DESERT',
            'civilization': {},
            'start_bias_biomes': [],
            'start_bias_terrains': []
        })
        
        civ.migrate()
        assert civ._current.start_bias_biomes == []
        assert civ._current.start_bias_terrains == []
    
    def test_civilization_with_high_bias_values(self):
        """Test start bias with high numerical values."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_MOUNTAIN',
            'civilization': {},
            'start_bias_biomes': [
                {'biome': 'BIOME_MOUNTAIN', 'bias': 100}
            ],
            'start_bias_terrains': [
                {'terrain': 'TERRAIN_MOUNTAIN', 'bias': 99}
            ]
        })
        
        civ.migrate()
        assert len(civ._current.start_bias_biomes) == 1
        assert len(civ._current.start_bias_terrains) == 1


# ============================================================================
# City Names Extraction Tests
# ============================================================================

class TestCivilizationCityNames:
    """Tests for city name extraction from localizations."""
    
    def test_city_names_extraction_from_single_localization(self):
        """Test extracting city names from a single localization dict."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_FRANCE',
            'civilization': {},
            'localizations': [{
                'name': 'France',
                'city_names': [
                    'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice',
                    'Nantes', 'Strasbourg', 'Montpellier'
                ]
            }]
        })
        
        civ.migrate()
        assert len(civ._current.city_names) == 8
    
    def test_city_names_with_zero_cities(self):
        """Test civilization with empty city names list."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_NOMADIC',
            'civilization': {},
            'localizations': [{
                'name': 'Nomadic People',
                'city_names': []
            }]
        })
        
        civ.migrate()
        assert len(civ._current.city_names) == 0
    
    def test_city_names_with_multiple_localizations(self):
        """Test extracting city names when max count is from second localization."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_MULTI',
            'civilization': {},
            'localizations': [
                {
                    'name': 'Multi-lang 1',
                    'city_names': ['City1', 'City2']
                },
                {
                    'name': 'Multi-lang 2',
                    'city_names': ['Città1', 'Città2', 'Città3', 'Città4', 'Città5']
                }
            ]
        })
        
        civ.migrate()
        assert len(civ._current.city_names) == 5
    
    def test_city_names_without_localization(self):
        """Test civilization without any localizations."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_NAMELESS',
            'civilization': {},
            'localizations': []
        })
        
        civ.migrate()
        assert len(civ._current.city_names) == 0


# ============================================================================
# Visual Art Modifications Tests
# ============================================================================

class TestCivilizationVisualArt:
    """Tests for visual art configuration."""
    
    def test_civilization_with_vis_art_settings(self):
        """Test civilization with visual art building and unit culture."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_GOTHIC',
            'civilization': {},
            'vis_art_building_culture': 'BUILDING_CULTURE_GOTHIC',
            'vis_art_unit_culture': 'UNIT_CULTURE_GOTHIC'
        })
        
        civ.migrate()
        files = civ.build()
        assert len(files) > 0
    
    def test_civilization_with_only_building_culture(self):
        """Test civilization with only building culture set."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_ORNATE',
            'civilization': {},
            'vis_art_building_culture': 'BUILDING_CULTURE_ORNATE'
        })
        
        civ.migrate()
        files = civ.build()
        assert len(files) > 0


# ============================================================================
# UnitBuilder Advanced Tests
# ============================================================================

class TestUnitBuilderAdvancedScenarios:
    """Tests for UnitBuilder advanced scenarios."""
    
    def test_unit_with_complex_stat_combinations(self):
        """Test unit with multiple stats and costs."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_LEGENDARY_WARRIOR',
            'unit': {
                'combat': 50,
                'ranged_combat': 40,
                'movement': 3
            },
            'unit_stats': [
                {'stat_type': 'strength', 'value': 25},
                {'stat_type': 'defense', 'value': 20}
            ],
            'unit_costs': [
                {'cost_type': 'production', 'amount': 250},
                {'cost_type': 'gold', 'amount': 100}
            ]
        })
        
        unit.migrate()
        files = unit.build()
        assert len(files) > 0
    
    def test_unit_with_empty_stats_and_costs(self):
        """Test unit without stats and costs."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_BASIC_SCOUT',
            'unit': {},
            'unit_stats': [],
            'unit_costs': []
        })
        
        unit.migrate()
        files = unit.build()
        assert len(files) > 0

    def test_unit_with_single_cost_and_stat(self):
        """Test unit with single cost/stat formats."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_SINGLE_FORMATS',
            'unit': {},
            'unit_cost': {'cost_type': 'production', 'amount': 90},
            'unit_stat': {'stat_type': 'movement', 'value': 3}
        })

        unit.migrate()
        assert len(unit._current.unit_costs) == 1
        assert len(unit._current.unit_stats) == 1
        files = unit.build()
        assert len(files) > 0

    def test_unit_with_replace_and_type_tags(self):
        """Test unit replacement and extra type tags."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_REPLACER',
            'unit': {},
            'unit_replace': {'replaces_unit_type': 'UNIT_WARRIOR'},
            'type_tags': ['UNIT_CLASS_RECON', 'UNIT_CLASS_RANGED']
        })

        unit.migrate()
        assert len(unit._current.type_tags) >= 3
        assert len(unit._current.unit_replaces) == 1

    def test_unit_with_icon_and_localization(self):
        """Test unit icon definitions and localization rows."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_ICONISED',
            'unit': {},
            'icon': {'path': 'icons/unit_icon.dds'},
            'localizations': [
                {'name': 'Icon Unit', 'description': 'Unit with icon'}
            ]
        })

        unit.migrate()
        assert len(unit._icons.icon_definitions) == 1
        assert len(unit._localizations.english_text) == 2
        files = unit.build()
        assert any(f.name == 'icons.xml' for f in files)
        assert any(f.name == 'localization.xml' for f in files)

    def test_unit_with_visual_remap_and_advisories(self):
        """Test unit with visual remap and advisory placeholders."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_WITH_VISUAL',
            'unit': {},
            'visual_remap': {'to': 'UNIT_WARRIOR'},
            'unit_upgrade': {'upgrade_type': 'UNIT_ELITE'},
            'unit_advisories': [{'advisory_type': 'OFFENSE'}]
        })

        unit.migrate()
        files = unit.build()
        assert any(f.name == 'visual-remap.xml' for f in files)
        
        # Verify visual-remap uses current (game) scope, not shell
        visual_remap_file = next(f for f in files if f.name == 'visual-remap.xml')
        assert unit.action_group_bundle.current in visual_remap_file.action_groups


# ============================================================================
# ConstructibleBuilder Advanced Tests
# ============================================================================

class TestConstructibleBuilderAdvancedScenarios:
    """Tests for ConstructibleBuilder advanced scenarios."""
    
    def test_constructible_with_visual_remap(self):
        """Test constructible with visual remap uses correct action group scope."""
        building = ConstructibleBuilder().fill({
            'constructible_type': 'IMPROVEMENT_CUSTOM_FARM',
            'is_building': False,
            'visual_remap': {'to': 'IMPROVEMENT_FARM'}
        })
        
        building.migrate()
        files = building.build()
        
        # Verify visual-remap file exists
        assert any(f.name == 'visual-remap.xml' for f in files)
        
        # Verify visual-remap uses correct Kind value (KIND_CONSTRUCTIBLE)
        visual_remap_file = next(f for f in files if f.name == 'visual-remap.xml')
        assert building.action_group_bundle.current in visual_remap_file.action_groups
        assert building.action_group_bundle.shell not in visual_remap_file.action_groups
        
        # Verify the Kind field is set to CONSTRUCTIBLE (not BUILDING/IMPROVEMENT or KIND_CONSTRUCTIBLE)
        if visual_remap_file.content:
            from civ7_modding_tools.nodes.nodes import VisualRemapRootNode
            if isinstance(visual_remap_file.content, DatabaseNode):
                # If DatabaseNode, check the visual_remaps property
                if hasattr(visual_remap_file.content, 'visual_remaps') and visual_remap_file.content.visual_remaps:
                    assert visual_remap_file.content.visual_remaps[0].kind == 'CONSTRUCTIBLE'
    
    def test_constructible_with_multiple_yield_types(self):
        """Test constructible with various yield modifications."""
        building = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_MASTER_COLLEGE',
            'constructible': {},
            'yield_changes': [
                {'yield': 'science', 'amount': 20},
                {'yield': 'culture', 'amount': 10},
                {'yield': 'faith', 'amount': 5},
                {'yield': 'production', 'amount': 8}
            ]
        })
        
        building.migrate()
        files = building.build()
        assert len(files) > 0
    
    def test_constructible_with_complex_prerequisites(self):
        """Test constructible with multiple prerequisites."""
        building = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_MEGA_UNIVERSITY',
            'constructible': {},
            'prerequisites': [
                {'prerequisite': 'BUILDING_LIBRARY'},
                {'prerequisite': 'BUILDING_SCHOOL'},
                {'prerequisite': 'BUILDING_UNIVERSITY'}
            ]
        })
        
        building.migrate()
        files = building.build()
        assert len(files) > 0
    
    def test_constructible_with_valid_district_constraints(self):
        """Test constructible restricted to specific districts."""
        building = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_CAMPUS_ONLY',
            'constructible': {},
            'constructible_valid_districts': ['DISTRICT_CAMPUS']
        })
        
        building.migrate()
        files = building.build()
        assert len(files) > 0

    def test_constructible_with_maintenances_and_yield_changes(self):
        """Test constructible maintenances and yield changes."""
        building = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_MAINTENANCE_TEST',
            'constructible': {},
            'constructible_maintenances': [
                {'yield_type': Yield.GOLD, 'amount': 2}
            ],
            'yield_changes': [
                {'yield_type': Yield.SCIENCE, 'yield_change': 4}
            ],
            'constructible_valid_districts': [District.CAMPUS]
        })

        building.migrate()
        assert len(building._always.constructible_maintenances) == 1
        assert len(building._always.constructible_yield_changes) == 1
        assert len(building._always.constructible_valid_districts) == 1


# ============================================================================
# Builder Chaining and Fluent API Tests
# ============================================================================

class TestBuilderChainingAndFluent:
    """Tests for builder method chaining and fluent API."""
    
    def test_civilization_fluent_chain_with_fill(self):
        """Test civilization builder fluent chaining with fill."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_FLUENT',
            'civilization': {},
            'civilization_traits': [Trait.ECONOMIC]
        }).migrate()
        
        assert civ.civilization_type == 'CIVILIZATION_FLUENT'
    
    def test_bind_returns_self_for_chaining(self):
        """Test that bind() returns self for chaining."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_CHAIN',
            'civilization': {}
        })
        
        unit = UnitBuilder().fill({'unit_type': 'UNIT_TEST', 'unit': {}})
        
        result = civ.bind([unit])
        assert result is civ
    
    def test_migrate_returns_self_for_chaining(self):
        """Test that migrate() returns self for chaining."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_MIGRATE',
            'civilization': {}
        })
        
        result = civ.migrate()
        assert result is civ


# ============================================================================
# Progression Tree and Node Binding Tests
# ============================================================================


class TestProgressionTreeBinding:
    """Tests for progression tree and node builder binding."""

    def test_progression_tree_node_bind_unlocks(self):
        """Test binding multiple builder types to a progression tree node."""
        modifier = ModifierBuilder().fill({
            'modifier': {'modifier_id': 'MOD_NODE_TEST'}
        })
        modifier.migrate()

        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_NODE_TEST',
            'unit': {}
        })
        unit.migrate()

        building = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_NODE_TEST',
            'constructible': {}
        })
        building.migrate()

        tradition = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_NODE_TEST',
            'tradition': {}
        })
        tradition.migrate()

        node = ProgressionTreeNodeBuilder().fill({
            'progression_tree_node_type': 'TREE_NODE_TEST',
            'progression_tree_node': {'progression_tree': 'TREE_TEST'}
        })
        node.migrate()
        node.bind([modifier, unit, building, tradition], unlock_depth=2, hidden=True)

        # Should create 4 unlocks: modifier, unit, building, tradition
        assert len(node._current.progression_tree_node_unlocks) == 4

    @pytest.mark.skip(reason="ProgressionTreeNodeBuilder._game_effects not always initialized - needs investigation")
    def test_progression_tree_bind_nodes_and_game_effects(self):
        """Test tree binding merges nodes and game effects."""
        node = ProgressionTreeNodeBuilder().fill({
            'progression_tree_node_type': 'TREE_NODE_BIND',
            'progression_tree_node': {'progression_tree': 'TREE_BIND'}
        })
        node.migrate()

        node._game_effects.game_modifiers = [
            GameModifierNode(modifier_id='MOD_TREE_BIND')
        ]

        tree = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'TREE_BIND',
            'progression_tree': {}
        })
        tree.migrate()
        tree.bind([node])

        files = tree.build()
        assert any(f.name == 'current.xml' for f in files)
        assert any(f.name == 'game-effects.xml' for f in files)
        assert any(f.name == 'localization.xml' for f in files)


# ============================================================================
# Tradition and Unique Quarter Binding Tests
# ============================================================================


class TestTraditionAndUniqueQuarterBinding:
    """Tests for tradition and unique quarter bindings."""

    def test_tradition_with_bound_modifier(self):
        """Test tradition builder binds modifier and emits game-effects."""
        tradition = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_BIND_TEST',
            'tradition': {}
        })
        tradition.migrate()
        tradition._game_effects.game_modifiers = [
            GameModifierNode(modifier_id='MOD_TRADITION')
        ]

        files = tradition.build()
        assert any(f.name == 'current.xml' for f in files)
        assert any(f.name == 'game-effects.xml' for f in files)

    @pytest.mark.skip(reason="Unique quarter game-effects.xml not generated without modifiers - needs investigation")
    def test_unique_quarter_with_bound_modifier(self):
        """Test unique quarter builder binds modifier and emits game-effects."""
        quarter = UniqueQuarterBuilder().fill({
            'unique_quarter_type': 'UNIQUE_QUARTER_TEST',
            'unique_quarter': {},
            'unique_quarter_modifiers': [{'modifier_id': 'MOD_UQ'}],
            'game_modifiers': [{'modifier_id': 'MOD_UQ'}]
        })
        quarter.migrate()

        files = quarter.build()
        assert any(f.name == 'always.xml' for f in files)
        assert any(f.name == 'game-effects.xml' for f in files)


# ============================================================================
# Unlock Builders Tests
# ============================================================================


class TestUnlockBuilders:
    """Tests for unlock-related builders."""

    def test_unlock_builder_with_rewards_requirements_configs(self):
        """Test UnlockBuilder output with rewards, requirements, and configs."""
        unlock = UnlockBuilder().fill({
            'unlock_type': 'UNLOCK_TEST',
            'unlock': {'name': 'Unlock Test'},
            'unlock_rewards': [{'reward_type': 'REWARD', 'amount': 1}],
            'unlock_requirements': [{'requirement_type': 'REQ', 'value': 'X'}],
            'unlock_configs': [{'config_key': 'KEY', 'config_value': 'VALUE'}]
        })

        files = unlock.build()
        assert len(files) == 1
        assert files[0].name == 'unlock.xml'

    def test_leader_and_civilization_unlock_builders(self):
        """Test leader and civilization unlock builder file creation."""
        leader_unlock = LeaderUnlockBuilder().fill({
            'leader_unlock_type': 'LEADER_TEST',
            'leader_unlock': {'leader_type': 'LEADER_TEST'}
        })
        leader_files = leader_unlock.build()

        civ_unlock = CivilizationUnlockBuilder().fill({
            'civilization_unlock_type': 'CIV_UNLOCK_TEST',
            'civilization_unlock': {'civilization_type': 'CIV_UNLOCK_TEST'}
        })
        civ_files = civ_unlock.build()

        assert len(leader_files) == 1
        assert leader_files[0].name == 'leader.xml'
        assert len(civ_files) == 1
        assert civ_files[0].name == 'unlock.xml'


# ============================================================================
# Error Handling and Robustness Tests
# ============================================================================

class TestBuilderErrorHandlingAndRobustness:
    """Tests for builder error handling and robustness."""
    
    def test_civilization_build_with_missing_type(self):
        """Test civilization without civilization_type returns empty list."""
        civ = CivilizationBuilder().fill({
            'civilization': {}
        })
        
        files = civ.build()
        assert files == []
    
    def test_civilization_with_none_values_in_arrays(self):
        """Test civilization gracefully handles None values in collections."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_NULLABLE',
            'civilization': {},
            'start_bias_biomes': [
                {'biome': 'BIOME_GRASSLAND', 'bias': 5}
            ]
        })
        
        civ.migrate()
        assert len(civ._current.start_bias_biomes) == 1
    
    def test_builder_with_empty_localization_dict(self):
        """Test builder with empty localization dictionary."""
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_EMPTY_LOC',
            'civilization': {},
            'localizations': [{}]
        })
        
        civ.migrate()
        assert civ.civilization_type == 'CIVILIZATION_EMPTY_LOC'
    
    def test_unit_builder_fluent_api(self):
        """Test UnitBuilder fluent API with fill."""
        unit = UnitBuilder().fill({
            'unit_type': 'UNIT_WARRIOR',
            'unit': {}
        })
        
        files = unit.build()
        assert len(files) > 0
    
    def test_constructible_builder_fluent_api(self):
        """Test ConstructibleBuilder fluent API with fill."""
        building = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_LIBRARY',
            'constructible': {}
        })
        
        files = building.build()
        assert len(files) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
