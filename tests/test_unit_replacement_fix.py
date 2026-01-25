"""
Test suite for unit replacement system fixes.

Tests TraitType assignment, progression tree unlocks, and TypeTags auto-generation.
"""

import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from civ7_modding_tools import Mod, ActionGroupBundle, UnitBuilder, CivilizationBuilder
from civ7_modding_tools.nodes import UnitNode


class TestTraitTypeAssignment:
    """Test automatic TraitType assignment to units."""
    
    def test_trait_type_set_from_civilization(self):
        """Unit should inherit trait_type from parent civilization."""
        mod = Mod(id='test-trait', version='1.0.0')
        
        civ = CivilizationBuilder()
        civ.civilization_type = 'CIVILIZATION_ICENI'
        civ.civilization = {'domain': 'AntiquityAgeCivilizations'}
        civ.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        unit = UnitBuilder()
        unit.unit_type = 'UNIT_WAR_CHARIOT_ICENI'
        unit.unit = {
            'base_moves': 3,
            'core_class': 'CORE_CLASS_COMBAT',
        }
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        civ.bind([unit])
        # Important: Mod must have both civ and unit builders
        mod.add([civ, unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            # Check generated XML
            unit_xml = Path(tmpdir) / 'units' / 'war-chariot-iceni' / 'current.xml'
            assert unit_xml.exists()
            
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            # Find Units table
            units_table = root.find('.//Units')
            assert units_table is not None
            
            # Find unit row
            unit_row = units_table.find('.//Row[@UnitType="UNIT_WAR_CHARIOT_ICENI"]')
            assert unit_row is not None
            
            # Verify TraitType is set
            assert unit_row.get('TraitType') == 'TRAIT_ICENI'
    
    def test_trait_type_explicit_override(self):
        """Explicitly set trait_type should not be overridden."""
        mod = Mod(id='test-trait-explicit', version='1.0.0')
        
        unit = UnitBuilder()
        unit.civilization_type = 'CIVILIZATION_ROME'
        unit.unit_type = 'UNIT_LEGION'
        unit.unit = {
            'base_moves': 2,
            'trait_type': 'TRAIT_CUSTOM',  # Explicit override
        }
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'legion' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            unit_row = root.find('.//Units/Row[@UnitType="UNIT_LEGION"]')
            assert unit_row.get('TraitType') == 'TRAIT_CUSTOM'


class TestProgressionTreeUnlocks:
    """Test automatic generation of progression tree unlock nodes."""
    
    def test_auto_infer_unlock_from_replaces(self):
        """Unit should auto-infer unlock from replaced unit's tech/civic."""
        mod = Mod(id='test-auto-unlock', version='1.0.0')
        
        unit = UnitBuilder()
        unit.civilization_type = 'CIVILIZATION_ICENI'
        unit.unit_type = 'UNIT_WAR_CHARIOT_ICENI'
        unit.unit = {
            'base_moves': 3,
            'tier': 2,
        }
        unit.unit_replace = {
            'replaces_unit_type': 'UNIT_CHARIOT',  # Unlocked by NODE_TECH_AQ_WHEEL
        }
        unit.auto_infer_unlock = True
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'war-chariot-iceni' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            # Find ProgressionTreeNodeUnlocks table
            unlocks_table = root.find('.//ProgressionTreeNodeUnlocks')
            assert unlocks_table is not None, "ProgressionTreeNodeUnlocks table should exist"
            
            # Find unlock row
            unlock_row = unlocks_table.find('.//Row[@TargetType="UNIT_WAR_CHARIOT_ICENI"]')
            assert unlock_row is not None, "Unlock row should exist"
            
            # Verify unlock details
            assert unlock_row.get('ProgressionTreeNodeType') == 'NODE_TECH_AQ_WHEEL'
            assert unlock_row.get('TargetKind') == 'KIND_UNIT'
            assert unlock_row.get('UnlockDepth') == '1'
            assert unlock_row.get('RequiredTraitType') == 'TRAIT_ICENI'
    
    def test_explicit_unlock_tech(self):
        """Explicitly set unlock_tech should take priority."""
        mod = Mod(id='test-explicit-unlock', version='1.0.0')
        
        unit = UnitBuilder()
        unit.civilization_type = 'CIVILIZATION_ROME'
        unit.unit_type = 'UNIT_LEGION'
        unit.unit = {'base_moves': 2}
        unit.unlock_tech = 'NODE_TECH_AQ_IRON_WORKING'
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'legion' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            unlock_row = root.find('.//ProgressionTreeNodeUnlocks/Row[@TargetType="UNIT_LEGION"]')
            assert unlock_row is not None
            assert unlock_row.get('ProgressionTreeNodeType') == 'NODE_TECH_AQ_IRON_WORKING'
    
    def test_unlock_civic_priority(self):
        """unlock_civic should override unlock_tech."""
        mod = Mod(id='test-civic-priority', version='1.0.0')
        
        unit = UnitBuilder()
        unit.unit_type = 'UNIT_UNIQUE'
        unit.unit = {}
        unit.unlock_tech = 'NODE_TECH_AQ_WHEEL'
        unit.unlock_civic = 'NODE_CIVICS_CUSTOM_1'  # Should win
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'unique' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            unlock_row = root.find('.//ProgressionTreeNodeUnlocks/Row')
            assert unlock_row.get('ProgressionTreeNodeType') == 'NODE_CIVICS_CUSTOM_1'


class TestTypeTagsAutoGeneration:
    """Test automatic generation of comprehensive TypeTags."""
    
    def test_combat_unit_tags(self):
        """Combat units should get UNIT_CLASS_COMBAT tag."""
        mod = Mod(id='test-combat-tags', version='1.0.0')
        
        unit = UnitBuilder()
        unit.unit_type = 'UNIT_WARRIOR'
        unit.unit = {
            'core_class': 'CORE_CLASS_COMBAT',
            'formation_class': 'FORMATION_CLASS_MELEE',
            'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
        }
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'warrior' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            # Find TypeTags table
            type_tags = root.findall('.//TypeTags/Row[@Type="UNIT_WARRIOR"]')
            tags = [row.get('Tag') for row in type_tags]
            
            # Should have: custom class, COMBAT, MELEE, INFANTRY
            assert 'UNIT_CLASS_WARRIOR' in tags
            assert 'UNIT_CLASS_COMBAT' in tags
            assert 'UNIT_CLASS_MELEE' in tags
            assert 'UNIT_CLASS_INFANTRY' in tags
    
    def test_cavalry_unit_tags(self):
        """Mounted units should get CAVALRY and MOUNTED tags."""
        mod = Mod(id='test-cavalry-tags', version='1.0.0')
        
        unit = UnitBuilder()
        unit.unit_type = 'UNIT_CHARIOT'
        unit.unit = {
            'core_class': 'CORE_CLASS_COMBAT',
            'unit_movement_class': 'UNIT_MOVEMENT_CLASS_MOUNTED',
            'tier': 2,
        }
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'chariot' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            type_tags = root.findall('.//TypeTags/Row[@Type="UNIT_CHARIOT"]')
            tags = [row.get('Tag') for row in type_tags]
            
            assert 'UNIT_CLASS_MOUNTED' in tags
            assert 'UNIT_CLASS_CAVALRY' in tags
    
    def test_elite_tags_tier3(self):
        """Tier 3+ infantry/cavalry should get ELITE tags."""
        mod = Mod(id='test-elite-tags', version='1.0.0')
        
        unit = UnitBuilder()
        unit.unit_type = 'UNIT_PHALANX'
        unit.unit = {
            'core_class': 'CORE_CLASS_COMBAT',
            'formation_class': 'FORMATION_CLASS_MELEE',
            'unit_movement_class': 'UNIT_MOVEMENT_CLASS_FOOT',
            'tier': 3,
        }
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'phalanx' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            type_tags = root.findall('.//TypeTags/Row[@Type="UNIT_PHALANX"]')
            tags = [row.get('Tag') for row in type_tags]
            
            assert 'UNIT_CLASS_ELITE_INFANTRY' in tags
    
    def test_naval_unit_tags(self):
        """Naval units should get NAVAL tag."""
        mod = Mod(id='test-naval-tags', version='1.0.0')
        
        unit = UnitBuilder()
        unit.unit_type = 'UNIT_GALLEY'
        unit.unit = {
            'core_class': 'CORE_CLASS_COMBAT',
            'domain': 'DOMAIN_SEA',
        }
        unit.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        mod.add([unit])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'galley' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            type_tags = root.findall('.//TypeTags/Row[@Type="UNIT_GALLEY"]')
            tags = [row.get('Tag') for row in type_tags]
            
            assert 'UNIT_CLASS_NAVAL' in tags


class TestComprehensiveIceniFix:
    """Full integration test for Iceni war chariot replacement fix."""
    
    def test_iceni_war_chariot_complete(self):
        """Iceni war chariot should have all fixes applied."""
        mod = Mod(id='iceni-fixed', version='1.0.0')
        
        civ = CivilizationBuilder()
        civ.civilization_type = 'CIVILIZATION_ICENI'
        civ.civilization = {'domain': 'AntiquityAgeCivilizations'}
        civ.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        # Tier 2 war chariot
        chariot_t2 = UnitBuilder()
        chariot_t2.unit_type = 'UNIT_BOUDICAN_WAR_CHARIOT_ICENI'
        chariot_t2.unit = {
            'base_moves': 3,
            'tier': 2,
            'maintenance': 2,
            'zone_of_control': True,
            'core_class': 'CORE_CLASS_COMBAT',
            'unit_movement_class': 'UNIT_MOVEMENT_CLASS_MOUNTED',
        }
        chariot_t2.unit_replace = {'replaces_unit_type': 'UNIT_CHARIOT'}
        chariot_t2.unit_upgrade = {'upgrade_unit': 'UNIT_BOUDICAN_WAR_CHARIOT_ICENI_2'}
        chariot_t2.auto_infer_unlock = True
        chariot_t2.action_group_bundle = ActionGroupBundle(action_group_id='AGE_ANTIQUITY')
        
        civ.bind([chariot_t2])
        # Important: Add both civ and unit to mod
        mod.add([civ, chariot_t2])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            unit_xml = Path(tmpdir) / 'units' / 'boudican-war-chariot-iceni' / 'current.xml'
            tree = ET.parse(unit_xml)
            root = tree.getroot()
            
            # Verify TraitType
            unit_row = root.find('.//Units/Row[@UnitType="UNIT_BOUDICAN_WAR_CHARIOT_ICENI"]')
            assert unit_row.get('TraitType') == 'TRAIT_ICENI', "TraitType must be set for replacement to work"
            
            # Verify UnitReplaces
            replace_row = root.find('.//UnitReplaces/Row[@CivUniqueUnitType="UNIT_BOUDICAN_WAR_CHARIOT_ICENI"]')
            assert replace_row is not None
            assert replace_row.get('ReplacesUnitType') == 'UNIT_CHARIOT'
            
            # Verify Progression unlock
            unlock_row = root.find('.//ProgressionTreeNodeUnlocks/Row[@TargetType="UNIT_BOUDICAN_WAR_CHARIOT_ICENI"]')
            assert unlock_row is not None, "Unit must have unlock requirement"
            assert unlock_row.get('ProgressionTreeNodeType') == 'NODE_TECH_AQ_WHEEL'
            assert unlock_row.get('RequiredTraitType') == 'TRAIT_ICENI'
            
            # Verify TypeTags
            type_tags = root.findall('.//TypeTags/Row[@Type="UNIT_BOUDICAN_WAR_CHARIOT_ICENI"]')
            tags = [row.get('Tag') for row in type_tags]
            assert 'UNIT_CLASS_COMBAT' in tags
            assert 'UNIT_CLASS_MOUNTED' in tags
            assert 'UNIT_CLASS_CAVALRY' in tags
            
            # Verify UnitUpgrades
            upgrade_row = root.find('.//UnitUpgrades/Row[@Unit="UNIT_BOUDICAN_WAR_CHARIOT_ICENI"]')
            assert upgrade_row is not None
            assert upgrade_row.get('UpgradeUnit') == 'UNIT_BOUDICAN_WAR_CHARIOT_ICENI_2'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
