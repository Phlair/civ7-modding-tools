"""Tests for upgrade chain bundling functionality."""

import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from civ7_modding_tools import Mod
from civ7_modding_tools.builders import UnitBuilder, ModifierBuilder


def test_upgrade_chain_shares_folder():
    """Units in an upgrade chain should share the same folder."""
    mod = Mod(id='test', version='1.0.0')
    
    # Create a 3-unit upgrade chain
    unit1 = UnitBuilder()
    unit1.unit_type = 'UNIT_WARRIOR_CUSTOM'
    unit1.base_unit_type = 'UNIT_WARRIOR_CUSTOM'  # Set explicitly
    unit1.unit = {'tier': 1}
    unit1.unit_stat = {'combat': 20}
    unit1.unit_upgrade = {'upgrade_unit': 'UNIT_WARRIOR_CUSTOM_2'}
    unit1.localizations = [{'name': 'Warrior T1'}]
    
    unit2 = UnitBuilder()
    unit2.unit_type = 'UNIT_WARRIOR_CUSTOM_2'
    unit2.base_unit_type = 'UNIT_WARRIOR_CUSTOM'  # Share same base
    unit2.unit = {'tier': 2}
    unit2.unit_stat = {'combat': 25}
    unit2.unit_upgrade = {'upgrade_unit': 'UNIT_WARRIOR_CUSTOM_3'}
    unit2.localizations = [{'name': 'Warrior T2'}]
    
    unit3 = UnitBuilder()
    unit3.unit_type = 'UNIT_WARRIOR_CUSTOM_3'
    unit3.base_unit_type = 'UNIT_WARRIOR_CUSTOM'  # Share same base
    unit3.unit = {'tier': 3}
    unit3.unit_stat = {'combat': 30}
    unit3.localizations = [{'name': 'Warrior T3'}]
    
    mod.add([unit1, unit2, unit3])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Should only have ONE warrior folder
        units_dir = Path(tmpdir) / 'units'
        warrior_folders = [d for d in units_dir.iterdir() if d.is_dir() and 'warrior' in d.name.lower()]
        
        assert len(warrior_folders) == 1, f"Expected 1 folder, got {len(warrior_folders)}: {[d.name for d in warrior_folders]}"
        assert warrior_folders[0].name == 'warrior-custom'


def test_upgrade_chain_merges_xml_files():
    """Units in upgrade chain should have merged current.xml with all tier definitions."""
    mod = Mod(id='test', version='1.0.0')
    
    unit1 = UnitBuilder()
    unit1.unit_type = 'UNIT_SWORDSMAN_T1'
    unit1.base_unit_type = 'UNIT_SWORDSMAN_T1'
    unit1.unit = {'tier': 1}
    unit1.unit_stat = {'combat': 20}
    unit1.unit_upgrade = {'upgrade_unit': 'UNIT_SWORDSMAN_T2'}
    unit1.localizations = [{'name': 'Swordsman T1'}]
    
    unit2 = UnitBuilder()
    unit2.unit_type = 'UNIT_SWORDSMAN_T2'
    unit2.base_unit_type = 'UNIT_SWORDSMAN_T1'
    unit2.unit = {'tier': 2}
    unit2.unit_stat = {'combat': 25}
    unit2.localizations = [{'name': 'Swordsman T2'}]
    
    mod.add([unit1, unit2])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Note: kebab_case converts UNIT_SWORDSMAN_T1 to swordsman-t-1
        current_xml = Path(tmpdir) / 'units' / 'swordsman-t-1' / 'current.xml'
        assert current_xml.exists()
        
        # Parse XML and check for both units
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        units_table = root.find('.//Units')
        assert units_table is not None
        
        unit_rows = units_table.findall('Row')
        assert len(unit_rows) == 2, f"Expected 2 unit rows, got {len(unit_rows)}"
        
        unit_types = {row.get('UnitType') for row in unit_rows}
        assert 'UNIT_SWORDSMAN_T1' in unit_types
        assert 'UNIT_SWORDSMAN_T2' in unit_types


def test_upgrade_chain_deduplicates_modifiers():
    """Shared modifiers in game-effects.xml should be deduplicated."""
    mod = Mod(id='test', version='1.0.0')
    
    # Create shared modifier
    forest_bonus = ModifierBuilder()
    forest_bonus.modifier_type = 'FOREST_COMBAT_BONUS'
    forest_bonus.modifier = {
        'effect': 'EFFECT_ADJUST_UNIT_STRENGTH_MODIFIER',
        'collection': 'COLLECTION_UNIT_COMBAT',
        'id': 'FOREST_COMBAT_BONUS',
    }
    forest_bonus.arguments = [
        {'name': 'Amount', 'value': '4'}
    ]
    
    # Create units that all reference the same modifier
    unit1 = UnitBuilder()
    unit1.unit_type = 'UNIT_CELTIC_WARRIOR_1'
    unit1.base_unit_type = 'UNIT_CELTIC_WARRIOR_1'
    unit1.unit = {'tier': 1}
    unit1.unit_stat = {'combat': 20}
    unit1.unit_upgrade = {'upgrade_unit': 'UNIT_CELTIC_WARRIOR_2'}
    unit1.unit_abilities = [{
        'ability_id': 'ABILITY_CELTIC_WARRIOR_1',
        'ability_type': 'ABILITY_FOREST_FIGHTER',
        'name': 'Forest Fighter',
        'description': '+4 Combat in Forest',
        'modifiers': ['FOREST_COMBAT_BONUS']
    }]
    unit1.localizations = [{'name': 'Celtic Warrior T1'}]
    
    unit2 = UnitBuilder()
    unit2.unit_type = 'UNIT_CELTIC_WARRIOR_2'
    unit2.base_unit_type = 'UNIT_CELTIC_WARRIOR_1'
    unit2.unit = {'tier': 2}
    unit2.unit_stat = {'combat': 24}
    unit2.unit_upgrade = {'upgrade_unit': 'UNIT_CELTIC_WARRIOR_3'}
    unit2.unit_abilities = [{
        'ability_id': 'ABILITY_CELTIC_WARRIOR_2',
        'ability_type': 'ABILITY_FOREST_FIGHTER',
        'name': 'Forest Fighter',
        'description': '+4 Combat in Forest',
        'modifiers': ['FOREST_COMBAT_BONUS']
    }]
    unit2.localizations = [{'name': 'Celtic Warrior T2'}]
    
    unit3 = UnitBuilder()
    unit3.unit_type = 'UNIT_CELTIC_WARRIOR_3'
    unit3.base_unit_type = 'UNIT_CELTIC_WARRIOR_1'
    unit3.unit = {'tier': 3}
    unit3.unit_stat = {'combat': 28}
    unit3.unit_abilities = [{
        'ability_id': 'ABILITY_CELTIC_WARRIOR_3',
        'ability_type': 'ABILITY_FOREST_FIGHTER',
        'name': 'Forest Fighter',
        'description': '+4 Combat in Forest',
        'modifiers': ['FOREST_COMBAT_BONUS']
    }]
    unit3.localizations = [{'name': 'Celtic Warrior T3'}]
    
    mod.add([forest_bonus, unit1, unit2, unit3])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Note: kebab_case converts UNIT_CELTIC_WARRIOR_1 to celtic-warrior-1
        game_effects_xml = Path(tmpdir) / 'units' / 'celtic-warrior-1' / 'game-effects.xml'
        assert game_effects_xml.exists()
        
        # Parse and check for single modifier definition
        tree = ET.parse(game_effects_xml)
        root = tree.getroot()
        
        modifiers_table = root.find('.//Modifiers')
        if modifiers_table is not None:
            modifier_rows = modifiers_table.findall('.//Row[@ModifierId="FOREST_COMBAT_BONUS"]')
            assert len(modifier_rows) == 1, f"Expected 1 modifier, got {len(modifier_rows)} (should be deduplicated)"


def test_yaml_upgrade_chain_detection():
    """YamlToPyConverter should detect upgrade chains and set base_unit_type."""
    from civ7_modding_tools.yml_to_py import YamlToPyConverter
    
    yaml_data = {
        'metadata': {'id': 'test', 'version': '1.0.0'},
        'units': [
            {
                'id': 'warrior1',
                'unit_type': 'UNIT_WARRIOR_1',
                'unit_upgrade': {'upgrade_unit': 'UNIT_WARRIOR_2'}
            },
            {
                'id': 'warrior2',
                'unit_type': 'UNIT_WARRIOR_2',
                'unit_upgrade': {'upgrade_unit': 'UNIT_WARRIOR_3'}
            },
            {
                'id': 'warrior3',
                'unit_type': 'UNIT_WARRIOR_3'
            }
        ]
    }
    
    converter = YamlToPyConverter(yaml_data)
    python_code = converter.convert()
    
    # Check that base_unit_type is set for all units in the chain
    assert "'base_unit_type': 'UNIT_WARRIOR_1'" in python_code
    
    # All three should point to the same root
    assert python_code.count("'base_unit_type': 'UNIT_WARRIOR_1'") == 3
