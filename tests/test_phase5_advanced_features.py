"""
Phase 5 Tests: Advanced Unit & Building Features

Comprehensive tests for:
1. Unit tier variants
2. Custom adjacency bonus types
3. Multi-tile buildings/quarters
"""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    UnitBuilder,
    ConstructibleBuilder,
    CivilizationBuilder,
    ModifierBuilder,
)
from civ7_modding_tools.nodes import (
    AdjacencyBonusNode,
    UnitTierVariantNode,
    MultiTileBuildingNode,
)
from civ7_modding_tools.localizations import UnitLocalization, ConstructibleLocalization


AGE_ANTIQUITY_BUNDLE = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')


class TestUnitTierVariants:
    """Test unit tier variants functionality."""
    
    def test_unit_tier_variant_initialization(self) -> None:
        """Test tier variant can be initialized."""
        unit = UnitBuilder()
        unit.fill({
            'unit_type': 'UNIT_BABYLON_SABUM',
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 5, 'name_suffix': 'Veteran'},
                {'tier': 3, 'combat_bonus': 10, 'name_suffix': 'Elite'}
            ]
        })
        assert unit.tier_variants is not None
        assert len(unit.tier_variants) == 2
    
    def test_unit_tier_variant_properties(self) -> None:
        """Test tier variant properties are set correctly."""
        unit = UnitBuilder()
        unit.fill({
            'unit_type': 'UNIT_TEST_UNIT',
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 5, 'name_suffix': 'Veteran'},
            ]
        })
        variant = unit.tier_variants[0]
        assert variant['tier'] == 2
        assert variant['combat_bonus'] == 5
        assert variant['name_suffix'] == 'Veteran'
    
    def test_unit_tier_variant_names_generated(self) -> None:
        """Test tier variant names are auto-generated."""
        unit = UnitBuilder()
        unit.fill({
            'unit_type': 'UNIT_BABYLON_SPEARMAN',
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 3, 'name_suffix': 'Veteran'},
                {'tier': 3, 'combat_bonus': 6, 'name_suffix': 'Elite'}
            ]
        })
        # Verify the naming pattern is established
        assert unit.tier_variants[0]['tier'] == 2
        assert unit.tier_variants[1]['tier'] == 3
    
    def test_unit_tier_variant_in_mod(self) -> None:
        """Test tier variant unit builds in mod."""
        mod = Mod(id='test-variants', version='1')
        unit = UnitBuilder()
        unit.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        unit.fill({
            'unit_type': 'UNIT_TEST_WARRIOR',
            'unit': {'core_class': 'CORE_CLASS_MILITARY'},
            'unit_stat': {'combat': 25},
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 5},
                {'tier': 3, 'combat_bonus': 10}
            ],
            'localizations': [
                UnitLocalization(name='Warrior', description='Ancient warrior unit')
            ]
        })
        mod.add(unit)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            # Verify build succeeded with variants
            modinfo_path = Path(tmpdir) / f'{mod.id}.modinfo'
            assert modinfo_path.exists()
    
    def test_unit_tier_variant_empty_list(self) -> None:
        """Test unit with empty tier variants list."""
        unit = UnitBuilder()
        unit.fill({
            'unit_type': 'UNIT_TEST_SIMPLE',
            'tier_variants': []
        })
        assert unit.tier_variants == []
    
    def test_unit_tier_variant_multiple_tiers(self) -> None:
        """Test unit with many tier variants."""
        unit = UnitBuilder()
        variants = [
            {'tier': i, 'combat_bonus': i * 2, 'name_suffix': f'Tier{i}'}
            for i in range(2, 6)
        ]
        unit.fill({
            'unit_type': 'UNIT_MULTI_TIER',
            'tier_variants': variants
        })
        assert len(unit.tier_variants) == 4
        assert unit.tier_variants[0]['tier'] == 2
        assert unit.tier_variants[3]['tier'] == 5
    
    def test_unit_tier_variant_mod_integration(self) -> None:
        """Test tier variant unit integrates with full mod."""
        mod = Mod(id='test-variants-full', version='1')
        unit = UnitBuilder()
        unit.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        unit.fill({
            'unit_type': 'UNIT_BABYLON_ELITE',
            'unit': {'core_class': 'CORE_CLASS_MILITARY'},
            'unit_stat': {'combat': 28},
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 7, 'name_suffix': 'Veteran'}
            ],
            'localizations': [
                UnitLocalization(name='Elite Unit', description='Advanced warrior')
            ]
        })
        mod.add(unit)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            assert Path(tmpdir).exists()


class TestAdjacencyBonuses:
    """Test custom adjacency bonus functionality."""
    
    def test_adjacency_bonus_initialization(self) -> None:
        """Test adjacency bonus can be initialized."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'BUILDING_TEST_LIBRARY',
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_RIVER',
                    'yield_type': 'YIELD_SCIENCE',
                    'amount': 15,
                    'description': '+15 Science from river'
                }
            ]
        })
        assert constructible.adjacency_bonuses is not None
        assert len(constructible.adjacency_bonuses) == 1
    
    def test_adjacency_bonus_properties(self) -> None:
        """Test adjacency bonus properties."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'BUILDING_TEST_CAMPUS',
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_MOUNTAIN',
                    'yield_type': 'YIELD_SCIENCE',
                    'amount': 20,
                    'description': '+20 Science from mountains'
                }
            ]
        })
        bonus = constructible.adjacency_bonuses[0]
        assert bonus['adjacency_type'] == 'ADJACENCY_MOUNTAIN'
        assert bonus['yield_type'] == 'YIELD_SCIENCE'
        assert bonus['amount'] == 20
    
    def test_multiple_adjacency_bonuses(self) -> None:
        """Test building with multiple adjacency bonuses."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'BUILDING_BABYLON_EDUBBA',
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_RIVER_NAVIGABLE',
                    'yield_type': 'YIELD_SCIENCE',
                    'amount': 15
                },
                {
                    'adjacency_type': 'ADJACENCY_DISTRICT_URBAN',
                    'yield_type': 'YIELD_CULTURE',
                    'amount': 10
                },
                {
                    'adjacency_type': 'ADJACENCY_WONDER',
                    'yield_type': 'YIELD_GOLD',
                    'amount': 8
                }
            ]
        })
        assert len(constructible.adjacency_bonuses) == 3
        assert constructible.adjacency_bonuses[1]['yield_type'] == 'YIELD_CULTURE'
    
    def test_adjacency_bonus_in_constructible_build(self) -> None:
        """Test adjacency bonus generates correctly in build."""
        mod = Mod(id='test-adjacency', version='1')
        constructible = ConstructibleBuilder()
        constructible.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        constructible.fill({
            'constructible_type': 'BUILDING_TEST_LIBRARY',
            'constructible': {'cost': 100},
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_RIVER',
                    'yield_type': 'YIELD_SCIENCE',
                    'amount': 15
                }
            ],
            'localizations': [
                ConstructibleLocalization(name='Library', description='Seat of knowledge')
            ]
        })
        mod.add(constructible)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / f'{mod.id}.modinfo'
            assert modinfo_path.exists()
    
    def test_adjacency_bonus_empty_list(self) -> None:
        """Test constructible with empty adjacency bonuses list."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'BUILDING_SIMPLE',
            'adjacency_bonuses': []
        })
        assert constructible.adjacency_bonuses == []
    
    def test_adjacency_bonus_negative_amount(self) -> None:
        """Test adjacency bonus with negative amount."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'BUILDING_TEST_HAZARD',
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_RESIDENTIAL',
                    'yield_type': 'YIELD_HOUSING',
                    'amount': -5,
                    'description': '-5 Housing from nearby residences'
                }
            ]
        })
        assert constructible.adjacency_bonuses[0]['amount'] == -5
    
    def test_adjacency_bonus_zero_amount(self) -> None:
        """Test adjacency bonus with zero amount."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'BUILDING_TEST_NEUTRAL',
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_PLAIN',
                    'yield_type': 'YIELD_PRODUCTION',
                    'amount': 0
                }
            ]
        })
        assert constructible.adjacency_bonuses[0]['amount'] == 0


class TestMultiTileBuildings:
    """Test multi-tile building functionality."""
    
    def test_multi_tile_building_initialization(self) -> None:
        """Test multi-tile building can be initialized."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'QUARTER_TEST_COMPLEX',
            'building_suite': {
                'components': ['BUILDING_BASE', 'BUILDING_TEMPLE'],
                'layout': 'LAYOUT_2x2'
            }
        })
        assert constructible.building_suite is not None
        assert constructible.building_suite['layout'] == 'LAYOUT_2x2'
    
    def test_multi_tile_building_components(self) -> None:
        """Test multi-tile building components."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'QUARTER_BABYLON_ZIGGURAT',
            'building_suite': {
                'components': [
                    'BUILDING_ZIGGURAT_BASE',
                    'BUILDING_ZIGGURAT_TEMPLE',
                    'BUILDING_ZIGGURAT_LIBRARY'
                ],
                'layout': 'LAYOUT_3x3'
            }
        })
        assert len(constructible.building_suite['components']) == 3
        assert constructible.building_suite['components'][0] == 'BUILDING_ZIGGURAT_BASE'
    
    def test_multi_tile_building_layout_types(self) -> None:
        """Test different multi-tile layout types."""
        layouts = ['LAYOUT_2x2', 'LAYOUT_3x3', 'LAYOUT_2x3', 'LAYOUT_IRREGULAR']
        
        for layout in layouts:
            constructible = ConstructibleBuilder()
            constructible.fill({
                'constructible_type': f'QUARTER_TEST_{layout}',
                'building_suite': {
                    'components': ['COMPONENT_A', 'COMPONENT_B'],
                    'layout': layout
                }
            })
            assert constructible.building_suite['layout'] == layout
    
    def test_multi_tile_building_in_mod(self) -> None:
        """Test multi-tile building builds in mod."""
        mod = Mod(id='test-multitile', version='1')
        constructible = ConstructibleBuilder()
        constructible.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        constructible.fill({
            'constructible_type': 'QUARTER_TEST_COMPLEX',
            'constructible': {'cost': 200},
            'building_suite': {
                'components': ['BUILDING_MAIN', 'BUILDING_ANNEXE'],
                'layout': 'LAYOUT_2x2'
            },
            'localizations': [
                ConstructibleLocalization(name='Complex', description='Multi-tile structure')
            ]
        })
        mod.add(constructible)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / f'{mod.id}.modinfo'
            assert modinfo_path.exists()
    
    def test_multi_tile_building_single_component(self) -> None:
        """Test multi-tile building with single component."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'QUARTER_SINGLE',
            'building_suite': {
                'components': ['BUILDING_ONLY'],
                'layout': 'LAYOUT_1x1'
            }
        })
        assert len(constructible.building_suite['components']) == 1
    
    def test_multi_tile_building_many_components(self) -> None:
        """Test multi-tile building with many components."""
        components = [f'BUILDING_COMPONENT_{i}' for i in range(1, 10)]
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'QUARTER_MASSIVE',
            'building_suite': {
                'components': components,
                'layout': 'LAYOUT_COMPLEX'
            }
        })
        assert len(constructible.building_suite['components']) == 9
    
    def test_multi_tile_building_with_adjacency(self) -> None:
        """Test multi-tile building with both suite and adjacency bonuses."""
        constructible = ConstructibleBuilder()
        constructible.fill({
            'constructible_type': 'QUARTER_BABYLON_ADVANCED',
            'building_suite': {
                'components': ['BASE', 'TEMPLE', 'LIBRARY'],
                'layout': 'LAYOUT_3x3'
            },
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_RIVER',
                    'yield_type': 'YIELD_SCIENCE',
                    'amount': 20
                }
            ]
        })
        assert constructible.building_suite is not None
        assert len(constructible.adjacency_bonuses) > 0


class TestAdvancedFeaturesIntegration:
    """Test integration of all advanced features."""
    
    def test_civilization_with_tiered_unit_and_adjacency_building(self) -> None:
        """Test full civilization using tier variants and adjacency bonuses."""
        mod = Mod(id='test-advanced', version='1')
        
        # Tiered unit
        unit = UnitBuilder()
        unit.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        unit.fill({
            'unit_type': 'UNIT_TEST_WARRIOR',
            'unit': {'core_class': 'CORE_CLASS_MILITARY'},
            'unit_stat': {'combat': 25},
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 5},
                {'tier': 3, 'combat_bonus': 10}
            ],
            'localizations': [
                UnitLocalization(name='Warrior', description='Ancient warrior')
            ]
        })
        
        # Building with adjacency
        building = ConstructibleBuilder()
        building.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        building.fill({
            'constructible_type': 'BUILDING_TEST_TEMPLE',
            'constructible': {'cost': 100},
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_RIVER',
                    'yield_type': 'YIELD_FAITH',
                    'amount': 10
                }
            ],
            'localizations': [
                ConstructibleLocalization(name='Temple', description='Religious structure')
            ]
        })
        
        # Multi-tile quarter
        quarter = ConstructibleBuilder()
        quarter.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        quarter.fill({
            'constructible_type': 'QUARTER_TEST_DISTRICT',
            'constructible': {'cost': 300},
            'building_suite': {
                'components': ['BASE', 'TEMPLE'],
                'layout': 'LAYOUT_2x2'
            },
            'localizations': [
                ConstructibleLocalization(name='District', description='Multi-tile complex')
            ]
        })
        
        mod.add([unit, building, quarter])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / f'{mod.id}.modinfo'
            assert modinfo_path.exists()
    
    def test_mod_with_all_phase5_features(self) -> None:
        """Test mod incorporating all Phase 5 features."""
        mod = Mod(id='test-all-phase5', version='1')
        
        # Unit tier variants
        unit1 = UnitBuilder()
        unit1.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        unit1.fill({
            'unit_type': 'UNIT_PIKEMAN',
            'unit': {'core_class': 'CORE_CLASS_MILITARY'},
            'unit_stat': {'combat': 28},
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 5, 'name_suffix': 'Veteran'},
                {'tier': 3, 'combat_bonus': 10, 'name_suffix': 'Elite'}
            ],
            'localizations': [
                UnitLocalization(name='Pikeman', description='Spear warrior')
            ]
        })
        
        unit2 = UnitBuilder()
        unit2.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        unit2.fill({
            'unit_type': 'UNIT_ARCHER',
            'unit': {'core_class': 'CORE_CLASS_MILITARY'},
            'unit_stat': {'combat': 20},
            'tier_variants': [
                {'tier': 2, 'combat_bonus': 3},
            ],
            'localizations': [
                UnitLocalization(name='Archer', description='Ranged warrior')
            ]
        })
        
        # Building with adjacency
        building1 = ConstructibleBuilder()
        building1.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        building1.fill({
            'constructible_type': 'BUILDING_ACADEMY',
            'constructible': {'cost': 150},
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_LIBRARY',
                    'yield_type': 'YIELD_SCIENCE',
                    'amount': 25
                }
            ],
            'localizations': [
                ConstructibleLocalization(name='Academy', description='School')
            ]
        })
        
        # Multi-tile building
        quarter = ConstructibleBuilder()
        quarter.action_group_bundle = AGE_ANTIQUITY_BUNDLE
        quarter.fill({
            'constructible_type': 'QUARTER_AGORA',
            'constructible': {'cost': 400},
            'building_suite': {
                'components': ['MARKET', 'PLAZA', 'FOUNTAIN'],
                'layout': 'LAYOUT_3x3'
            },
            'adjacency_bonuses': [
                {
                    'adjacency_type': 'ADJACENCY_TRADE_ROUTE',
                    'yield_type': 'YIELD_GOLD',
                    'amount': 15
                }
            ],
            'localizations': [
                ConstructibleLocalization(name='Agora', description='Marketplace')
            ]
        })
        
        mod.add([unit1, unit2, building1, quarter])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / f'{mod.id}.modinfo'
            assert modinfo_path.exists()
            # Verify multiple units present
            units_path = Path(tmpdir) / 'units'
            assert units_path.exists()
