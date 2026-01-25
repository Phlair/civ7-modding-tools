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


def test_custom_ability_description_appended_to_unit_summary():
    """Test that custom ability descriptions are appended to unit summary."""
    mod = Mod(id='test-custom-desc', version='1.0.0', name='Test', description='Test', authors='Test')
    
    # Create a custom ability with a description
    ability = UnitAbilityBuilder().fill({
        'ability_id': 'ABILITY_DRUID_SACRED_GROVE',
        'ability_type': 'ABILITY_DRUID_SACRED_GROVE',
        'localizations': [
            {
                'name': 'Sacred Grove',
                'description': '+2 Combat Strength when adjacent to forest or jungle tiles'
            }
        ],
    })
    
    # Create a unit with this custom ability
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_DRUID',
        'unit': {
            'core_class': 'CORE_CLASS_COMBAT',
            'domain': 'DOMAIN_LAND',
        },
        'localizations': [
            {
                'name': 'Druid',
                'description': 'Celtic religious warrior'
            }
        ],
    })
    unit.bind([ability])
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Check localization.xml has combined description
        loc_xml = Path(tmpdir) / 'units' / 'druid' / 'localization.xml'
        assert loc_xml.exists()
        
        tree = ET.parse(loc_xml)
        root = tree.getroot()
        
        # Find the unit description
        desc_rows = root.findall(".//EnglishText/Row[@Tag='LOC_UNIT_DRUID_DESCRIPTION']")
        assert len(desc_rows) == 1
        
        description_text = desc_rows[0].find('Text').text
        
        # Should contain both the unit description and the ability description
        assert 'Celtic religious warrior' in description_text
        assert '+2 Combat Strength when adjacent to forest or jungle tiles' in description_text
        
        # The ability description should be appended after the unit description
        assert description_text.index('Celtic religious warrior') < description_text.index('+2 Combat Strength')


def test_mixed_abilities_both_descriptions_appended():
    """Test that both dict-based and builder-based ability descriptions are appended."""
    mod = Mod(id='test-mixed-desc', version='1.0.0', name='Test', description='Test', authors='Test')
    
    # Create a custom ability
    custom_ability = UnitAbilityBuilder().fill({
        'ability_id': 'ABILITY_CUSTOM',
        'ability_type': 'ABILITY_CUSTOM',
        'localizations': [
            {
                'name': 'Custom Ability',
                'description': 'Custom ability description text'
            }
        ],
    })
    
    # Create a unit with both dict-based abilities (one with description_text, one with description) and custom abilities
    unit = UnitBuilder().fill({
        'unit_type': 'UNIT_MIXED',
        'unit': {'core_class': 'CORE_CLASS_COMBAT'},
        'unit_abilities': [
            {
                'ability_id': 'ABILITY_WITH_DESCRIPTION_TEXT',
                'ability_type': 'ABILITY_WITH_DESCRIPTION_TEXT',
                'name': 'Ability 1',
                'description': 'Dict ability 1',
                'description_text': 'Dict ability 1 description text for summary',
                'modifiers': [],
            },
            {
                'ability_id': 'ABILITY_WITH_DESCRIPTION_ONLY',
                'ability_type': 'ABILITY_WITH_DESCRIPTION_ONLY',
                'name': 'Ability 2',
                'description': '+{1_Amount} Combat Strength in Forest',
                'modifiers': [],
            }
        ],
        'localizations': [
            {
                'name': 'Mixed Unit',
                'description': 'Base unit description'
            }
        ],
    })
    unit.bind([custom_ability])
    
    mod.add(unit)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Check localization.xml
        loc_xml = Path(tmpdir) / 'units' / 'mixed' / 'localization.xml'
        assert loc_xml.exists()
        
        tree = ET.parse(loc_xml)
        root = tree.getroot()
        
        # Find the unit description
        desc_rows = root.findall(".//EnglishText/Row[@Tag='LOC_UNIT_MIXED_DESCRIPTION']")
        assert len(desc_rows) == 1
        
        description_text = desc_rows[0].find('Text').text
        
        # Should contain the base description
        assert 'Base unit description' in description_text
        
        # Should contain the first dict-based ability description (description_text takes precedence)
        assert 'Dict ability 1 description text for summary' in description_text
        
        # Should contain the second dict-based ability description (using description field)
        assert '+{1_Amount} Combat Strength in Forest' in description_text
        
        # Should contain the custom ability description
        assert 'Custom ability description text' in description_text
        
        # All should be in order
        base_idx = description_text.index('Base unit description')
        dict1_idx = description_text.index('Dict ability 1 description text for summary')
        dict2_idx = description_text.index('+{1_Amount} Combat Strength in Forest')
        custom_idx = description_text.index('Custom ability description text')
        
        assert base_idx < dict1_idx
        assert base_idx < dict2_idx
        assert base_idx < custom_idx
