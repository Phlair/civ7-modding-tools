"""Tests for Phase 3: Great People System."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import (
    GreatPersonBuilder,
    UnitBuilder,
    ModifierBuilder,
    CivilizationBuilder,
)
from civ7_modding_tools.localizations import UnitLocalization


class TestGreatPersonBuilder:
    """Test GreatPersonBuilder functionality."""

    def test_great_person_builder_initialization(self):
        """Test GreatPersonBuilder initialization."""
        builder = GreatPersonBuilder()
        
        assert builder.great_person_type is None
        assert builder.great_person_class is None
        assert builder.base_unit is None

    def test_great_person_builder_fill(self):
        """Test GreatPersonBuilder fill method."""
        builder = GreatPersonBuilder()
        
        builder.fill({
            'great_person_type': 'GREAT_PERSON_HAMMURABI',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_HAMMURABI',
        })
        
        assert builder.great_person_type == 'GREAT_PERSON_HAMMURABI'
        assert builder.great_person_class == 'GREAT_PERSON_CLASS_GENERAL'
        assert builder.base_unit == 'UNIT_GREAT_GENERAL'

    def test_great_person_builder_build(self):
        """Test GreatPersonBuilder build method."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_TEST',
            'localizations': [
                {'name': 'Test Great Person', 'description': 'A test great person'}
            ]
        })
        
        files = builder.build()
        
        # Should generate files
        assert len(files) > 0

    def test_great_person_builder_build_empty(self):
        """Test GreatPersonBuilder build with empty type."""
        builder = GreatPersonBuilder()
        
        files = builder.build()
        
        # Should return empty list
        assert len(files) == 0

    def test_great_person_with_modifiers(self):
        """Test GreatPersonBuilder with bound modifiers."""
        great_person = GreatPersonBuilder()
        great_person.fill({
            'great_person_type': 'GREAT_PERSON_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_TEST',
            'localizations': [{'name': 'Test'}]
        })
        
        modifier = ModifierBuilder()
        modifier.fill({
            'modifier_type': 'MODIFIER_GREAT_PERSON_TEST',
            'modifier': {
                'collection': 'COLLECTION_OWNER',
                'effect': 'EFFECT_MODIFIER_TEST'
            }
        })
        
        # Should support binding modifiers
        result = great_person.bind([modifier])
        assert result == great_person

    def test_great_person_localization(self):
        """Test GreatPersonBuilder with localizations."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_HAMMURABI',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_HAMMURABI',
            'localizations': [
                UnitLocalization(
                    name='Hammurabi',
                    description='Legendary lawgiver and king of Babylon.'
                )
            ]
        })
        
        assert len(builder.localizations) > 0
        assert builder.localizations[0].name == 'Hammurabi'

    def test_great_person_inherits_from_unit_builder(self):
        """Test that GreatPersonBuilder inherits unit properties."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_TEST',
            'unit_stat': {'combat': 20},
            'unit_cost': {'yield_type': 'YIELD_PRODUCTION', 'cost': 100},
        })
        
        # Should have unit-level properties
        assert builder.unit_type == 'UNIT_GREAT_GENERAL_TEST'
        assert builder.unit_stat is not None
        assert builder.unit_cost is not None


class TestGreatPersonIntegration:
    """Integration tests for Great People system."""

    def test_great_person_in_mod(self):
        """Test adding great person to mod."""
        mod = Mod(id="test-great-people", version="1", name="Test Great People")
        
        great_person = GreatPersonBuilder()
        great_person.fill({
            'great_person_type': 'GREAT_PERSON_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_TEST',
            'localizations': [{'name': 'Test Great Person'}]
        })
        
        mod.add(great_person)
        
        # Should track builder
        assert great_person in mod.builders

    def test_great_person_modinfo_generation(self):
        """Test modinfo generation with great people."""
        mod = Mod(id="babylon-great-people", version="1", name="Babylon Great People")
        
        great_person = GreatPersonBuilder()
        great_person.fill({
            'great_person_type': 'GREAT_PERSON_HAMMURABI',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_HAMMURABI',
            'localizations': [
                {'name': 'Hammurabi', 'description': 'Legendary lawgiver'}
            ]
        })
        
        mod.add(great_person)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-great-people.modinfo"
            assert modinfo_path.exists()

    def test_great_person_with_civilization(self):
        """Test great person working alongside civilization."""
        mod = Mod(id="babylon-complete", version="1", name="Babylon Complete")
        
        # Add civilization
        civ = CivilizationBuilder()
        civ.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'civilization_traits': []
        })
        
        # Add great person
        great_person = GreatPersonBuilder()
        great_person.fill({
            'great_person_type': 'GREAT_PERSON_HAMMURABI',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_HAMMURABI',
            'localizations': [{'name': 'Hammurabi'}]
        })
        
        mod.add([civ, great_person])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-complete.modinfo"
            assert modinfo_path.exists()

    def test_multiple_great_people(self):
        """Test multiple great people in one mod."""
        mod = Mod(id="multi-great-people", version="1", name="Multi Great People")
        
        great_people = []
        for i in range(3):
            gp = GreatPersonBuilder()
            gp.fill({
                'great_person_type': f'GREAT_PERSON_TEST_{i}',
                'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
                'base_unit': 'UNIT_GREAT_GENERAL',
                'unit_type': f'UNIT_GREAT_GENERAL_TEST_{i}',
                'localizations': [{'name': f'Great Person {i}'}]
            })
            great_people.append(gp)
        
        mod.add(great_people)
        
        # Should track all great people
        assert len(mod.builders) >= 3

    def test_great_person_with_age_bundle(self):
        """Test great person with age-specific action group."""
        from civ7_modding_tools import ActionGroupBundle
        
        mod = Mod(id="antiquity-great-people", version="1", name="Antiquity Great People")
        
        great_person = GreatPersonBuilder()
        great_person.action_group_bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        great_person.fill({
            'great_person_type': 'GREAT_PERSON_ANTIQUITY_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_ANTIQUITY',
            'localizations': [{'name': 'Antiquity Great Person'}]
        })
        
        mod.add(great_person)
        
        # Check that age-specific action groups are used
        assert 'AGE_ANTIQUITY' in great_person.action_group_bundle.action_group_id

    def test_great_person_unit_conversion(self):
        """Test that great person extends unit system properly."""
        gp = GreatPersonBuilder()
        gp.fill({
            'great_person_type': 'GREAT_PERSON_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_TEST',
            'core_class': 'CORE_CLASS_MILITARY',
            'unit_stat': {'combat': 25},
            'unit_cost': {'yield_type': 'YIELD_PRODUCTION', 'cost': 200},
            'localizations': [{'name': 'Great General'}]
        })
        
        # Should have proper unit properties
        assert gp.unit_type == 'UNIT_GREAT_GENERAL_TEST'
        assert gp.unit_stat is not None
        assert gp.unit_cost is not None


class TestGreatPersonClasses:
    """Test different great person classes."""

    def test_great_person_class_general(self):
        """Test GREAT_PERSON_CLASS_GENERAL."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_GENERAL_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_GENERAL',
            'base_unit': 'UNIT_GREAT_GENERAL',
            'unit_type': 'UNIT_GREAT_GENERAL_TEST',
        })
        
        assert builder.great_person_class == 'GREAT_PERSON_CLASS_GENERAL'

    def test_great_person_class_merchant(self):
        """Test GREAT_PERSON_CLASS_MERCHANT."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_MERCHANT_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_MERCHANT',
            'base_unit': 'UNIT_GREAT_MERCHANT',
            'unit_type': 'UNIT_GREAT_MERCHANT_TEST',
        })
        
        assert builder.great_person_class == 'GREAT_PERSON_CLASS_MERCHANT'

    def test_great_person_class_scientist(self):
        """Test GREAT_PERSON_CLASS_SCIENTIST."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_SCIENTIST_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_SCIENTIST',
            'base_unit': 'UNIT_GREAT_SCIENTIST',
            'unit_type': 'UNIT_GREAT_SCIENTIST_TEST',
        })
        
        assert builder.great_person_class == 'GREAT_PERSON_CLASS_SCIENTIST'

    def test_great_person_class_writer(self):
        """Test GREAT_PERSON_CLASS_WRITER."""
        builder = GreatPersonBuilder()
        builder.fill({
            'great_person_type': 'GREAT_PERSON_WRITER_TEST',
            'great_person_class': 'GREAT_PERSON_CLASS_WRITER',
            'base_unit': 'UNIT_GREAT_WRITER',
            'unit_type': 'UNIT_GREAT_WRITER_TEST',
        })
        
        assert builder.great_person_class == 'GREAT_PERSON_CLASS_WRITER'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
