"""Tests for Unit Abilities System."""

import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import UnitBuilder, UnitAbilityBuilder, ModifierBuilder


def test_simple_passive_ability():
    """Test creating a unit with a simple passive ability."""
    mod = Mod(id='test-ability', version='1.0.0', name='Test', description='Test', authors='Test')
    
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_HOPLITE',
        'unit': {
            'core_class': 'CORE_CLASS_COMBAT',
            'domain': 'DOMAIN_LAND',
            'formation_class': 'FORMATION_CLASS_MELEE',
        },
        'unit_abilities': [{
            'ability_id': 'ABILITY_HOPLITE',
            'ability_type': 'ABILITY_HOPLITE',
            'name': 'Phalanx Formation',
            'description': '+2 Combat from adjacent Hoplites',
            'modifiers': ['HOPLITE_MOD_COMBAT_FROM_ADJACENT'],
        }],
        'localizations': [{'name': 'Hoplite', 'description': 'Greek heavy infantry'}],
    })
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Check current.xml has ability definitions
        current_xml = Path(tmpdir) / 'units' / 'hoplite' / 'current.xml'
        assert current_xml.exists()
        
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        # Check Types
        types = root.findall(".//Types/Row[@Type='ABILITY_HOPLITE']")
        assert len(types) == 1
        assert types[0].get('Kind') == 'KIND_ABILITY'
        
        # Check UnitAbilities
        abilities = root.findall(".//UnitAbilities/Row[@UnitAbilityType='ABILITY_HOPLITE']")
        assert len(abilities) == 1
        assert 'Phalanx Formation' in abilities[0].get('Name')
        
        # Check UnitClass_Abilities junction
        unit_class_abilities = root.findall(".//UnitClass_Abilities/Row[@UnitAbilityType='ABILITY_HOPLITE']")
        assert len(unit_class_abilities) == 1
        assert unit_class_abilities[0].get('UnitClassType') == 'UNIT_CLASS_HOPLITE'
        
        # Check UnitAbilityModifiers junction
        ability_modifiers = root.findall(".//UnitAbilityModifiers/Row[@UnitAbilityType='ABILITY_HOPLITE']")
        assert len(ability_modifiers) == 1
        assert ability_modifiers[0].get('ModifierId') == 'HOPLITE_MOD_COMBAT_FROM_ADJACENT'


def test_inactive_ability_auto_activation():
    """Test that inactive abilities generate auto-activation modifiers."""
    mod = Mod(id='test-inactive', version='1.0.0', name='Test', description='Test', authors='Test')
    
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_INFANTRY',
        'unit': {'core_class': 'CORE_CLASS_COMBAT'},
        'unit_abilities': [{
            'ability_id': 'ABILITY_TECH_INFANTRY',
            'ability_type': 'ABILITY_TECH_INFANTRY',
            'name': 'Tech Infantry',
            'description': 'Combat bonus',
            'inactive': True,
            'modifiers': ['TECH_INFANTRY_MOD_COMBAT'],
        }],
    })
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        current_xml = Path(tmpdir) / 'units' / 'infantry' / 'current.xml'
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        # Check inactive flag
        abilities = root.findall(".//UnitAbilities/Row[@UnitAbilityType='ABILITY_TECH_INFANTRY']")
        assert len(abilities) == 1
        assert abilities[0].get('Inactive') == 'true'


def test_charged_ability():
    """Test creating a unit with a charged ability."""
    mod = Mod(id='test-charged', version='1.0.0', name='Test', description='Test', authors='Test')
    
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_JAGUAR_SLAYER',
        'unit': {'core_class': 'CORE_CLASS_COMBAT'},
        'unit_abilities': [{
            'ability_id': 'ABILITY_STONE_TRAP',
            'ability_type': 'ABILITY_STONE_TRAP',
            'name': 'Stone Trap',
            'description': 'Limited use ability',
            'charged_config': {'recharge_turns': 5},
            'modifiers': ['STONE_TRAP_MOD'],
        }],
    })
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        current_xml = Path(tmpdir) / 'units' / 'jaguar-slayer' / 'current.xml'
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        # Check ChargedUnitAbilities
        charged = root.findall(".//ChargedUnitAbilities/Row[@UnitAbilityType='ABILITY_STONE_TRAP']")
        assert len(charged) == 1
        assert charged[0].get('RechargeTurns') == '5'


def test_ability_with_multiple_modifiers():
    """Test ability with multiple modifier attachments."""
    mod = Mod(id='test-multi-mod', version='1.0.0', name='Test', description='Test', authors='Test')
    
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_CAVALRY',
        'unit': {'core_class': 'CORE_CLASS_COMBAT'},
        'unit_abilities': [{
            'ability_id': 'ABILITY_CAVALRY',
            'ability_type': 'ABILITY_CAVALRY',
            'name': 'Cavalry',
            'description': 'Multiple bonuses',
            'modifiers': ['CAVALRY_MOD_1', 'CAVALRY_MOD_2', 'CAVALRY_MOD_3'],
        }],
    })
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        current_xml = Path(tmpdir) / 'units' / 'cavalry' / 'current.xml'
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        # Check UnitAbilityModifiers has all 3 modifiers
        ability_modifiers = root.findall(".//UnitAbilityModifiers/Row[@UnitAbilityType='ABILITY_CAVALRY']")
        assert len(ability_modifiers) == 3
        modifier_ids = [m.get('ModifierId') for m in ability_modifiers]
        assert 'CAVALRY_MOD_1' in modifier_ids
        assert 'CAVALRY_MOD_2' in modifier_ids
        assert 'CAVALRY_MOD_3' in modifier_ids


def test_unit_ability_builder_with_modifiers():
    """Test UnitAbilityBuilder with bound ModifierBuilder."""
    mod = Mod(id='test-builder', version='1.0.0', name='Test', description='Test', authors='Test')
    
    # Create modifier
    modifier = ModifierBuilder().fill({
        'modifier': {
            'id': 'NUMIDIAN_CAVALRY_MOD_COMBAT',
            'collection': 'COLLECTION_OWNER',
            'effect': 'EFFECT_ADJUST_UNIT_RESOURCE_DAMAGE',
            'arguments': [
                {'name': 'Amount', 'value': '1'},
                {'name': 'ResourceClassType', 'value': 'RESOURCECLASS_CITY'},
            ],
        },
    })
    
    # Create ability and bind modifier
    ability = UnitAbilityBuilder().fill({
        'ability_id': 'ABILITY_NUMIDIAN_CAVALRY',
        'ability_type': 'ABILITY_NUMIDIAN_CAVALRY',
        'localizations': [
            {'name': 'Numidian Cavalry', 'description': '+1 combat per capital resource'},
        ],
    })
    ability.bind([modifier])
    
    # Create unit and bind ability
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_NUMIDIAN_CAVALRY',
        'unit': {'core_class': 'CORE_CLASS_COMBAT'},
    })
    unit.bind([ability])
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        current_xml = Path(tmpdir) / 'units' / 'numidian-cavalry' / 'current.xml'
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        # Check ability was added
        abilities = root.findall(".//UnitAbilities/Row[@UnitAbilityType='ABILITY_NUMIDIAN_CAVALRY']")
        assert len(abilities) == 1
        
        # Check modifier junction was created
        ability_modifiers = root.findall(".//UnitAbilityModifiers/Row[@UnitAbilityType='ABILITY_NUMIDIAN_CAVALRY']")
        assert len(ability_modifiers) == 1
        assert ability_modifiers[0].get('ModifierId') == 'NUMIDIAN_CAVALRY_MOD_COMBAT'


def test_multiple_abilities_on_same_unit():
    """Test unit with multiple abilities."""
    mod = Mod(id='test-multiple', version='1.0.0', name='Test', description='Test', authors='Test')
    
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_SPECIAL',
        'unit': {'core_class': 'CORE_CLASS_COMBAT'},
        'unit_abilities': [
            {
                'ability_id': 'ABILITY_SPECIAL_1',
                'ability_type': 'ABILITY_SPECIAL_1',
                'name': 'Ability 1',
                'description': 'First ability',
                'modifiers': ['MOD_1'],
            },
            {
                'ability_id': 'ABILITY_SPECIAL_2',
                'ability_type': 'ABILITY_SPECIAL_2',
                'name': 'Ability 2',
                'description': 'Second ability',
                'inactive': True,
                'modifiers': ['MOD_2'],
            },
        ],
    })
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        current_xml = Path(tmpdir) / 'units' / 'special' / 'current.xml'
        tree = ET.parse(current_xml)
        root = tree.getroot()
        
        # Check both abilities exist
        abilities = root.findall(".//UnitAbilities/Row")
        ability_types = [a.get('UnitAbilityType') for a in abilities]
        assert 'ABILITY_SPECIAL_1' in ability_types
        assert 'ABILITY_SPECIAL_2' in ability_types
        
        # Check both have junctions
        junctions = root.findall(".//UnitClass_Abilities/Row[@UnitClassType='UNIT_CLASS_SPECIAL']")
        assert len(junctions) == 2
