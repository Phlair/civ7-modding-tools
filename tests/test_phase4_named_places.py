"""Tests for Phase 4: Named Places System."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    NamedPlaceBuilder,
    ModifierBuilder,
    CivilizationBuilder,
)


class TestNamedPlaceBuilder:
    """Test NamedPlaceBuilder functionality."""

    def test_named_place_builder_initialization(self):
        """Test NamedPlaceBuilder initialization."""
        builder = NamedPlaceBuilder()
        
        assert builder.named_place_type is None
        assert builder.placement is None
        assert builder.yield_changes == []

    def test_named_place_builder_fill(self):
        """Test NamedPlaceBuilder fill method."""
        builder = NamedPlaceBuilder()
        
        builder.fill({
            'named_place_type': 'NAMED_PLACE_HANGING_GARDENS',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 10}
            ]
        })
        
        assert builder.named_place_type == 'NAMED_PLACE_HANGING_GARDENS'
        assert builder.placement == 'PLACEMENT_RIVER'
        assert len(builder.yield_changes) == 1

    def test_named_place_builder_build(self):
        """Test NamedPlaceBuilder build method."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_TEST',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 5}
            ],
            'localizations': [
                {'name': 'Test Place', 'description': 'A test location'}
            ]
        })
        
        files = builder.build()
        
        # Should generate files
        assert len(files) > 0

    def test_named_place_builder_build_empty(self):
        """Test NamedPlaceBuilder build with empty type."""
        builder = NamedPlaceBuilder()
        
        files = builder.build()
        
        # Should return empty list
        assert len(files) == 0

    def test_named_place_with_modifiers(self):
        """Test NamedPlaceBuilder with bound modifiers."""
        named_place = NamedPlaceBuilder()
        named_place.fill({
            'named_place_type': 'NAMED_PLACE_TEST',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 5}
            ],
            'localizations': [{'name': 'Test'}]
        })
        
        modifier = ModifierBuilder()
        modifier.fill({
            'modifier_type': 'MODIFIER_NAMED_PLACE_TEST',
            'modifier': {
                'collection': 'COLLECTION_OWNER',
                'effect': 'EFFECT_MODIFIER_TEST'
            }
        })
        
        # Should support binding modifiers
        result = named_place.bind([modifier])
        assert result == named_place

    def test_named_place_localization(self):
        """Test NamedPlaceBuilder with localizations."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_HANGING_GARDENS',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [],
            'localizations': [
                {'name': 'Hanging Gardens', 'description': 'Legendary gardens of Babylon'}
            ]
        })
        
        assert len(builder.localizations) > 0
        assert builder.localizations[0]['name'] == 'Hanging Gardens'

    def test_named_place_placement_types(self):
        """Test different placement types."""
        placements = [
            'PLACEMENT_RIVER',
            'PLACEMENT_MOUNTAIN',
            'PLACEMENT_COAST',
            'PLACEMENT_FOREST'
        ]
        
        for placement in placements:
            builder = NamedPlaceBuilder()
            builder.fill({
                'named_place_type': f'NAMED_PLACE_TEST_{placement}',
                'placement': placement,
                'yield_changes': []
            })
            
            assert builder.placement == placement

    def test_named_place_multiple_yield_changes(self):
        """Test named place with multiple yield changes."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_FERTILE_DELTA',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 10},
                {'yield_type': 'YIELD_PRODUCTION', 'yield_change': 5},
                {'yield_type': 'YIELD_GOLD', 'yield_change': 3}
            ]
        })
        
        assert len(builder.yield_changes) == 3


class TestNamedPlaceIntegration:
    """Integration tests for Named Places system."""

    def test_named_place_in_mod(self):
        """Test adding named place to mod."""
        mod = Mod(id="test-named-places", version="1", name="Test Named Places")
        
        named_place = NamedPlaceBuilder()
        named_place.fill({
            'named_place_type': 'NAMED_PLACE_TEST',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 5}
            ],
            'localizations': [{'name': 'Test Place'}]
        })
        
        mod.add(named_place)
        
        # Should track builder
        assert named_place in mod.builders

    def test_named_place_modinfo_generation(self):
        """Test modinfo generation with named places."""
        mod = Mod(id="babylon-named-places", version="1", name="Babylon Named Places")
        
        named_place = NamedPlaceBuilder()
        named_place.fill({
            'named_place_type': 'NAMED_PLACE_HANGING_GARDENS_SITE',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 10}
            ],
            'localizations': [
                {'name': 'Hanging Gardens', 'description': 'Legendary gardens'}
            ]
        })
        
        mod.add(named_place)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-named-places.modinfo"
            assert modinfo_path.exists()

    def test_named_place_with_civilization(self):
        """Test named place working alongside civilization."""
        mod = Mod(id="babylon-complete-v2", version="1", name="Babylon Complete V2")
        
        # Add civilization
        civ = CivilizationBuilder()
        civ.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'civilization_traits': []
        })
        
        # Add named place
        named_place = NamedPlaceBuilder()
        named_place.fill({
            'named_place_type': 'NAMED_PLACE_HANGING_GARDENS_SITE',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 10}
            ],
            'localizations': [{'name': 'Hanging Gardens'}]
        })
        
        mod.add([civ, named_place])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-complete-v2.modinfo"
            assert modinfo_path.exists()

    def test_multiple_named_places(self):
        """Test multiple named places in one mod."""
        mod = Mod(id="multi-named-places", version="1", name="Multi Named Places")
        
        named_places = []
        locations = [
            ('HANGING_GARDENS', 'RIVER', 10),
            ('TOWER_OF_BABEL', 'MOUNTAIN', 8),
            ('CEDAR_FOREST', 'FOREST', 6)
        ]
        
        for loc_name, placement, food_change in locations:
            np = NamedPlaceBuilder()
            np.fill({
                'named_place_type': f'NAMED_PLACE_{loc_name}',
                'placement': f'PLACEMENT_{placement}',
                'yield_changes': [
                    {'yield_type': 'YIELD_FOOD', 'yield_change': food_change}
                ],
                'localizations': [{'name': loc_name.replace('_', ' ')}]
            })
            named_places.append(np)
        
        mod.add(named_places)
        
        # Should track all named places
        assert len(mod.builders) >= 3

    def test_named_place_with_age_bundle(self):
        """Test named place with age-specific action group."""
        from civ7_modding_tools import ActionGroupBundle
        
        mod = Mod(id="antiquity-places", version="1", name="Antiquity Places")
        
        named_place = NamedPlaceBuilder()
        named_place.action_group_bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        named_place.fill({
            'named_place_type': 'NAMED_PLACE_ANTIQUITY_TEST',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 5}
            ],
            'localizations': [{'name': 'Antiquity Place'}]
        })
        
        mod.add(named_place)
        
        # Check that age-specific action groups are used
        assert 'AGE_ANTIQUITY' in named_place.action_group_bundle.action_group_id

    def test_named_place_with_modifiers_binding(self):
        """Test named place with bound modifiers and yields."""
        named_place = NamedPlaceBuilder()
        named_place.fill({
            'named_place_type': 'NAMED_PLACE_FERTILE_REGION',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 15},
                {'yield_type': 'YIELD_PRODUCTION', 'yield_change': 5}
            ],
            'localizations': [{'name': 'Fertile Region'}]
        })
        
        modifier = ModifierBuilder()
        modifier.fill({
            'modifier_type': 'MODIFIER_FERTILITY_BONUS',
            'modifier': {
                'collection': 'COLLECTION_OWNER',
                'effect': 'EFFECT_MODIFIER_TEST'
            }
        })
        
        result = named_place.bind([modifier])
        assert result == named_place
        assert len(named_place.yield_changes) == 2


class TestNamedPlacePlacements:
    """Test different named place placement scenarios."""

    def test_named_place_river_placement(self):
        """Test PLACEMENT_RIVER placement."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_NILE_DELTA',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 20}
            ],
        })
        
        assert builder.placement == 'PLACEMENT_RIVER'
        assert len(builder.yield_changes) == 1

    def test_named_place_mountain_placement(self):
        """Test PLACEMENT_MOUNTAIN placement."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_EVEREST',
            'placement': 'PLACEMENT_MOUNTAIN',
            'yield_changes': [
                {'yield_type': 'YIELD_PRODUCTION', 'yield_change': 15}
            ],
        })
        
        assert builder.placement == 'PLACEMENT_MOUNTAIN'

    def test_named_place_coast_placement(self):
        """Test PLACEMENT_COAST placement."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_LIGHTHOUSE',
            'placement': 'PLACEMENT_COAST',
            'yield_changes': [
                {'yield_type': 'YIELD_GOLD', 'yield_change': 12}
            ],
        })
        
        assert builder.placement == 'PLACEMENT_COAST'

    def test_named_place_forest_placement(self):
        """Test PLACEMENT_FOREST placement."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_CEDAR_FORESTS',
            'placement': 'PLACEMENT_FOREST',
            'yield_changes': [
                {'yield_type': 'YIELD_PRODUCTION', 'yield_change': 10}
            ],
        })
        
        assert builder.placement == 'PLACEMENT_FOREST'

    def test_named_place_with_icon(self):
        """Test named place with icon definition."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_TEST_ICON',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [],
            'icon': {
                'path': 'icons/civs/named_place_test.png'
            }
        })
        
        assert builder.icon is not None
        assert builder.icon['path'] == 'icons/civs/named_place_test.png'


class TestNamedPlaceYields:
    """Test yield change configurations for named places."""

    def test_single_yield_change(self):
        """Test single yield change."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_FOOD',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 10}
            ]
        })
        
        assert len(builder.yield_changes) == 1
        assert builder.yield_changes[0]['yield_type'] == 'YIELD_FOOD'

    def test_multiple_yield_changes(self):
        """Test multiple yield changes."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_MIXED',
            'placement': 'PLACEMENT_RIVER',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': 10},
                {'yield_type': 'YIELD_GOLD', 'yield_change': 5},
                {'yield_type': 'YIELD_SCIENCE', 'yield_change': 3}
            ]
        })
        
        assert len(builder.yield_changes) == 3

    def test_negative_yield_change(self):
        """Test negative yield change (penalty)."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_HARSH',
            'placement': 'PLACEMENT_MOUNTAIN',
            'yield_changes': [
                {'yield_type': 'YIELD_FOOD', 'yield_change': -5}
            ]
        })
        
        assert builder.yield_changes[0]['yield_change'] == -5

    def test_zero_yield_change(self):
        """Test zero yield change."""
        builder = NamedPlaceBuilder()
        builder.fill({
            'named_place_type': 'NAMED_PLACE_NEUTRAL',
            'placement': 'PLACEMENT_COAST',
            'yield_changes': [
                {'yield_type': 'YIELD_GOLD', 'yield_change': 0}
            ]
        })
        
        assert builder.yield_changes[0]['yield_change'] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
