"""
End-to-end integration test for civilization ability feature.

Tests the complete pipeline:
1. Create Mod with CivilizationBuilder
2. Set civ_ability_name and civ_ability_modifier_ids
3. Build mod to disk
4. Verify XML files contain TraitModifiers and localizations
"""

import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from civ7_modding_tools import (
    ActionGroupBundle,
    CivilizationBuilder,
    Mod,
    ModifierBuilder,
)
from civ7_modding_tools.localizations import CivilizationLocalization


def test_civ_ability_e2e_xml_generation():
    """Test that civ ability generates correct XML output in built mod."""
    # Create a mod with civilization ability
    mod = Mod(
        id='test-civ-ability-e2e',
        version='1.0.0',
        name='Test Civ Ability E2E',
        description='Integration test for civilization ability',
        authors='Test'
    )
    
    # Create a modifier to reference
    modifier = ModifierBuilder().fill({
        'modifier_id': 'MOD_TEST_ABILITY_BONUS',
        'modifier_type': 'MODIFIER_PLAYER_CITIES_ADJUST_YIELD_CHANGE',
        'modifier_arguments': [
            {'name': 'YieldType', 'value': 'YIELD_SCIENCE'},
            {'name': 'Amount', 'value': '2'}
        ]
    })
    modifier.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
    
    # Create civilization with ability
    civ = CivilizationBuilder().fill({
        'civilization_type': 'CIVILIZATION_TEST_E2E',
        'civilization_traits': ['TRAIT_ATTRIBUTE_SCIENTIFIC'],
        'civilization': {
            'civ_ability_name': 'Scientific Prowess',
            'civ_ability_modifier_ids': ['MOD_TEST_ABILITY_BONUS']
        },
        'localizations': [
            CivilizationLocalization(
                name='Test E2E Civ',
                description='Test civilization for e2e testing',
                adjective='Test E2E',
                city_names=['TestCity']
            )
        ],
    })
    civ.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
    
    mod.add([modifier, civ])
    
    # Build to temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Find the actual civilization directory (uses trim + kebab_case)
        civ_dirs = list(Path(tmpdir).glob('civilizations/*'))
        assert len(civ_dirs) > 0, f"No civilization directories found in {tmpdir}/civilizations"
        civ_dir = civ_dirs[0]
        
        # Verify current.xml contains TraitModifiers
        current_xml_path = civ_dir / 'current.xml'
        assert current_xml_path.exists(), f"current.xml not found at {current_xml_path}"
        
        # Parse XML
        tree = ET.parse(str(current_xml_path))
        root = tree.getroot()
        
        # Check TraitModifiers section exists
        trait_modifiers = root.findall('.//TraitModifiers')
        assert len(trait_modifiers) > 0, "TraitModifiers section not found in current.xml"
        
        # Check specific TraitModifier row
        trait_modifier_rows = root.findall('.//TraitModifiers/Row')
        assert len(trait_modifier_rows) > 0, "No TraitModifier rows found"
        
        # Verify the modifier is linked to the ability trait
        ability_modifier_rows = [
            row for row in trait_modifier_rows
            if row.get('TraitType') == 'TRAIT_TEST_E2E_ABILITY'
            and row.get('ModifierId') == 'MOD_TEST_ABILITY_BONUS'
        ]
        assert len(ability_modifier_rows) == 1, (
            f"Expected 1 TraitModifier row for TRAIT_TEST_E2E_ABILITY -> MOD_TEST_ABILITY_BONUS, "
            f"found {len(ability_modifier_rows)}"
        )
        
        # Verify localization.xml contains ability name
        loc_xml_path = civ_dir / 'localization.xml'
        assert loc_xml_path.exists(), f"localization.xml not found at {loc_xml_path}"
        
        loc_tree = ET.parse(str(loc_xml_path))
        loc_root = loc_tree.getroot()
        
        # Check for ability name localization
        ability_name_loc = loc_root.findall(
            ".//EnglishText/Row[@Tag='LOC_CIVILIZATION_TEST_E2E_ABILITY_NAME']"
        )
        assert len(ability_name_loc) == 1, "Ability name localization not found"
        
        # Verify the text content
        text_elem = ability_name_loc[0].find('Text')
        assert text_elem is not None, "Text element not found in ability localization"
        assert text_elem.text == 'Scientific Prowess', (
            f"Expected 'Scientific Prowess', got '{text_elem.text}'"
        )


def test_civ_ability_e2e_multiple_modifiers():
    """Test that multiple modifier IDs are all linked correctly."""
    mod = Mod(
        id='test-multi-modifiers',
        version='1.0.0',
        name='Test Multi Modifiers',
        description='Test multiple modifiers',
        authors='Test'
    )
    
    # Create multiple modifiers
    mod1 = ModifierBuilder().fill({
        'modifier_id': 'MOD_TEST_1',
        'modifier_type': 'MODIFIER_PLAYER_CITIES_ADJUST_YIELD_CHANGE',
        'modifier_arguments': [
            {'name': 'YieldType', 'value': 'YIELD_SCIENCE'},
            {'name': 'Amount', 'value': '1'}
        ]
    })
    mod1.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
    
    mod2 = ModifierBuilder().fill({
        'modifier_id': 'MOD_TEST_2',
        'modifier_type': 'MODIFIER_PLAYER_CITIES_ADJUST_YIELD_CHANGE',
        'modifier_arguments': [
            {'name': 'YieldType', 'value': 'YIELD_CULTURE'},
            {'name': 'Amount', 'value': '1'}
        ]
    })
    mod2.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
    
    # Create civilization with multiple modifiers
    civ = CivilizationBuilder().fill({
        'civilization_type': 'CIVILIZATION_MULTI_TEST',
        'civilization': {
            'civ_ability_name': 'Dual Bonus',
            'civ_ability_modifier_ids': ['MOD_TEST_1', 'MOD_TEST_2']
        },
        'localizations': [
            CivilizationLocalization(
                name='Multi Test',
                description='Test',
                adjective='Multi',
                city_names=['City']
            )
        ],
    })
    civ.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
    
    mod.add([mod1, mod2, civ])
    
    # Build and verify
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Find the actual civilization directory
        civ_dirs = list(Path(tmpdir).glob('civilizations/*'))
        assert len(civ_dirs) > 0, "No civilization directories found"
        civ_dir = civ_dirs[0]
        
        current_xml_path = civ_dir / 'current.xml'
        tree = ET.parse(str(current_xml_path))
        root = tree.getroot()
        
        # Check both modifiers are linked
        trait_modifier_rows = root.findall(
            ".//TraitModifiers/Row[@TraitType='TRAIT_MULTI_TEST_ABILITY']"
        )
        assert len(trait_modifier_rows) == 2, (
            f"Expected 2 TraitModifier rows, found {len(trait_modifier_rows)}"
        )
        
        # Verify both modifier IDs are present
        modifier_ids = {row.get('ModifierId') for row in trait_modifier_rows}
        assert modifier_ids == {'MOD_TEST_1', 'MOD_TEST_2'}, (
            f"Expected MOD_TEST_1 and MOD_TEST_2, got {modifier_ids}"
        )
