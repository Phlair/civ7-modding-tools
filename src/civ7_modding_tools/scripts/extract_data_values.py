#!/usr/bin/env python3
"""
Extract all reference values from Civ VII EXAMPLE folders and dist-* outputs.

Scans XML files to harvest valid values for:
- BuildingCulture, UnitCulture, TerrainType, DistrictType, YieldType
- AdvisoryClassType, Tag, CivilizationDomain, effect
- ConstructibleClass, UnitMovementClass, CoreClass, FormationClass, Domain
- CostProgressionModel, BiomeType, FeatureType, RiverPlacement, Age
- MilitaryDomain, PromotionClass, GovernmentType, ProjectType
- BeliefClassType, DifficultyType, ProgressionTree, GreatWorkObjectType
- Leader, LeaderAttribute, Unit
- And more!

Output: JSON files in src/civ7_modding_tools/data/ with kebab-case naming.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import xml.etree.ElementTree as ET


class CivVIIDataExtractor:
    """Extract reference values from Civ VII mod files."""

    def __init__(self, root_dir: Path):
        self.root = root_dir
        self.data = {
            # Original requested types
            'building_cultures': defaultdict(set),
            'building_cultures_by_era': defaultdict(lambda: defaultdict(set)),
            'terrain_types': set(),
            'unit_cultures': defaultdict(set),
            'effects': set(),
            'civilization_domains': set(),
            'tags': defaultdict(str),
            'district_types': set(),
            'yield_types': set(),
            'advisory_class_types': set(),
            'requirement_types': set(),
            'collection_types': set(),
            
            # Additional high-value types
            'constructible_classes': set(),
            'unit_movement_classes': set(),
            'core_classes': set(),
            'formation_classes': set(),
            'domains': set(),
            'cost_progression_models': set(),
            'biome_types': set(),
            'feature_types': set(),
            'river_placements': set(),
            'ages': set(),
            'military_domains': set(),
            'promotion_classes': set(),
            'government_types': set(),
            'project_types': set(),
            'belief_class_types': set(),
            'difficulty_types': set(),
            'progression_trees': set(),
            'great_work_object_types': set(),
            'resource_classes': set(),
            'handicap_system_types': set(),
            'leaders': set(),
            'leader_attributes': set(),
            'units': set(),
            'civilizations': set(),
            'civilization_traits': set(),
            'unit_abilities': {},  # {ability_id: {name, description, description_text}}
            'constructibles': set(),  # All building, improvement, and wonder types
            'traditions': {},  # {tradition_id: {name, description, age, trait_type, is_crisis, modifiers}}
            'modifiers': {},  # {modifier_id: {effect, collection, tooltip_loc, description, arguments}}
        }
        self.localization_texts = {}  # {LOC_TAG: english_text} - for resolving LOC_ keys
        self.civ_cache = defaultdict(dict)
        self.civilization_ages = {}  # {civ_id: age_id}
        self.civ_era_mapping = {}  # {civ_name: era_id} - maps civs to eras from filenames
        self.unit_ages = defaultdict(set)  # {unit_id: {age_ids}} - tracks which ages unlock each unit
        self.unit_unlocks = defaultdict(set)  # {unit_id: {node_types}} - progression nodes that unlock
        self.unit_replaces = {}  # {unique_unit_id: replaced_unit_id} - UnitReplaces mappings
        self._tree_ages = {}  # {progression_tree_id: age_id} - maps trees to ages

    def scan_files(self) -> None:
        """Recursively scan all XML files in EXAMPLE and dist folders."""
        # Example folders
        for example_dir in self.root.glob('*-EXAMPLE'):
            self._scan_directory(example_dir, is_example=True)

        # dist-* folders
        for dist_dir in self.root.glob('dist-*'):
            self._scan_directory(dist_dir, is_example=False)
        
        # Resolve LOC_ keys to English text for abilities
        self._resolve_ability_descriptions()
        
        # Resolve LOC_ keys to English text for modifiers
        self._resolve_modifier_descriptions()

    def _scan_directory(self, directory: Path, is_example: bool = False) -> None:
        """Scan a directory for XML files."""
        for xml_file in directory.rglob('*.xml'):
            try:
                self._extract_from_file(xml_file)
            except Exception as e:
                print(f"Warning: Failed to parse {xml_file}: {e}")    
    def _extract_english_text(self, file_path: Path) -> None:
        """Extract English localization text from EnglishText or LocalizedText nodes."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError:
            return
        
        # EnglishText format (used in text/en_us/ and modules/text/)
        for row in root.findall(".//EnglishText/Row"):
            tag = row.get('Tag')
            text_elem = row.find('Text')
            if tag and text_elem is not None and text_elem.text:
                self.localization_texts[tag] = text_elem.text
    
    def _resolve_ability_descriptions(self) -> None:
        """Resolve LOC_ description keys to actual English text."""
        for ability_id, ability_data in self.data['unit_abilities'].items():
            loc_key = ability_data.get('description', '')
            if loc_key and loc_key in self.localization_texts:
                ability_data['description_text'] = self.localization_texts[loc_key]
            else:
                ability_data['description_text'] = ''

    def _resolve_modifier_descriptions(self) -> None:
        """Resolve LOC_ tooltip and description keys to actual English text for modifiers."""
        for modifier_id, modifier_data in self.data['modifiers'].items():
            # Try tooltip_loc first (most common for modifiers)
            loc_key = modifier_data.get('tooltip_loc', '')
            if loc_key and loc_key in self.localization_texts:
                modifier_data['description'] = self.localization_texts[loc_key]
                continue
            
            # Try description_loc (String context="Description")
            loc_key = modifier_data.get('description_loc', '')
            if loc_key and loc_key in self.localization_texts:
                modifier_data['description'] = self.localization_texts[loc_key]
                continue
            
            # No localization found - leave description empty
            modifier_data['description'] = ''
    
    def _resolve_tradition_localizations(self) -> None:
        """Resolve LOC_ keys to actual English text for traditions."""
        for tradition_id, tradition_data in self.data['traditions'].items():
            # Resolve name
            name_loc = tradition_data.get('name_loc', '')
            if name_loc and name_loc in self.localization_texts:
                tradition_data['name'] = self.localization_texts[name_loc]
            else:
                # Fallback: generate name from ID
                tradition_data['name'] = tradition_id.replace('TRADITION_', '').replace('_', ' ').title()
            
            # Resolve description
            desc_loc = tradition_data.get('description_loc', '')
            if desc_loc and desc_loc in self.localization_texts:
                tradition_data['description'] = self.localization_texts[desc_loc]
            else:
                tradition_data['description'] = ''
    def _extract_english_text(self, file_path: Path) -> None:
        """Extract English localization text from EnglishText or LocalizedText nodes."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError:
            return
        
        # EnglishText format (used in text/en_us/ and modules/text/)
        for row in root.findall(".//EnglishText/Row"):
            tag = row.get('Tag')
            text_elem = row.find('Text')
            if tag and text_elem is not None and text_elem.text:
                self.localization_texts[tag] = text_elem.text

    def _extract_modifiers_from_file(self, file_path: Path) -> None:
        """Extract modifiers with full metadata including arguments and descriptions."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError:
            return
        
        # Handle XML namespaces - GameEffects files use xmlns="GameEffects"
        namespace = ''
        if '}' in root.tag:
            namespace = root.tag.split('}')[0] + '}'
        
        # Extract all Modifier elements with their children
        # Use namespace-aware search if namespace exists
        if namespace:
            modifiers_found = root.findall(f'.//{namespace}Modifier')
        else:
            modifiers_found = root.findall('.//Modifier')
        
        for modifier_elem in modifiers_found:
            modifier_id = modifier_elem.get('id')
            if not modifier_id:
                continue
            
            # Initialize modifier data if not exists
            if modifier_id not in self.data['modifiers']:
                self.data['modifiers'][modifier_id] = {
                    'effect': '',
                    'collection': '',
                    'permanent': False,
                    'tooltip_loc': '',
                    'description_loc': '',
                    'description': '',
                    'arguments': {}
                }
            
            # Extract attributes
            self.data['modifiers'][modifier_id]['effect'] = modifier_elem.get('effect', '')
            self.data['modifiers'][modifier_id]['collection'] = modifier_elem.get('collection', '')
            self.data['modifiers'][modifier_id]['permanent'] = modifier_elem.get('permanent', '').lower() == 'true'
            
            # Extract Argument elements (including Tooltip)
            if namespace:
                arg_elements = modifier_elem.findall(f'./{namespace}Argument')
            else:
                arg_elements = modifier_elem.findall('./Argument')
            
            for arg_elem in arg_elements:
                arg_name = arg_elem.get('name', '')
                arg_value = arg_elem.text or ''
                if arg_name:
                    if arg_name == 'Tooltip':
                        self.data['modifiers'][modifier_id]['tooltip_loc'] = arg_value
                    else:
                        self.data['modifiers'][modifier_id]['arguments'][arg_name] = arg_value
            
            # Extract String elements with context="Description"
            if namespace:
                string_elements = modifier_elem.findall(f'./{namespace}String')
            else:
                string_elements = modifier_elem.findall('./String')
            
            for string_elem in string_elements:
                if string_elem.get('context') == 'Description':
                    self.data['modifiers'][modifier_id]['description_loc'] = string_elem.text or ''
    
    def _extract_from_file(self, file_path: Path) -> None:
        """Extract values from a single XML file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError:
            return
        
        # Extract English text if this is a localization file
        if 'text' in str(file_path).lower() or 'localization' in str(file_path).lower():
            self._extract_english_text(file_path)
        
        # Extract modifiers from GameEffects files
        file_path_str = str(file_path).lower()
        if 'gameeffects' in file_path_str:
            self._extract_modifiers_from_file(file_path)

        # Get civilization name from folder structure if available
        civ_name = self._get_civ_name_from_path(file_path)
        
        # Extract era from filename (e.g., 'civilizations-antiquity.xml' -> 'ANTIQUITY')
        file_stem = file_path.stem.lower()
        era_id = None
        if '-antiquity' in file_stem:
            era_id = 'AGE_ANTIQUITY'
        elif '-exploration' in file_stem:
            era_id = 'AGE_EXPLORATION'
        elif '-modern' in file_stem:
            era_id = 'AGE_MODERN'
        
        # Also check folder path for era hints (e.g., 'data-EXPL-EXAMPLE', 'data-MODERN-EXAMPLE')
        # This helps us capture eras from central data files in era-specific folders
        if not era_id:
            path_str = str(file_path).lower()
            if 'data-expl-example' in path_str or 'data-exploration' in path_str:
                era_id = 'AGE_EXPLORATION'
            elif 'data-modern-example' in path_str or 'data-mod-example' in path_str:
                era_id = 'AGE_MODERN'
            elif 'data-example' in path_str and 'expl' not in path_str and 'modern' not in path_str and 'mod-example' not in path_str:
                # Generic 'data-EXAMPLE' folder implies Antiquity
                era_id = 'AGE_ANTIQUITY'

        # Handle XML namespaces
        namespaces = {}
        if '}' in root.tag:
            namespace = root.tag.split('}')[0] + '}'
            namespaces['ns'] = namespace[1:-1]

        # Scan for each data type
        for element in root.iter():
            tag = element.tag
            # Strip namespace from tag
            if '}' in tag:
                tag = tag.split('}')[1]
            
            attribs = element.attrib

            # BuildingCulture - track by era
            if 'BuildingCulture' in attribs:
                bc = attribs['BuildingCulture']
                self.data['building_cultures'][bc].add(civ_name)
                # Also track with era if available
                if era_id:
                    self.data['building_cultures_by_era'][bc][era_id].add(civ_name)

            # UnitCulture
            if 'UnitCulture' in attribs:
                uc = attribs['UnitCulture']
                self.data['unit_cultures'][uc].add(civ_name)

            # TerrainType
            if 'TerrainType' in attribs:
                self.data['terrain_types'].add(attribs['TerrainType'])

            # DistrictType
            if 'DistrictType' in attribs:
                self.data['district_types'].add(attribs['DistrictType'])

            # YieldType
            if 'YieldType' in attribs:
                self.data['yield_types'].add(attribs['YieldType'])

            # AdvisoryClassType
            if 'AdvisoryClassType' in attribs:
                self.data['advisory_class_types'].add(attribs['AdvisoryClassType'])

            # effect (from Modifier elements)
            if tag == 'Modifier' and 'effect' in attribs:
                self.data['effects'].add(attribs['effect'])

            # Requirements
            if 'type' in attribs and attribs.get('type', '').startswith('REQUIREMENT_'):
                self.data['requirement_types'].add(attribs['type'])

            # Collections
            if 'collection' in attribs and attribs.get('collection', '').startswith('COLLECTION_'):
                self.data['collection_types'].add(attribs['collection'])

            # Tags and Categories
            if tag == 'Row' and 'Tag' in attribs:
                category = attribs.get('Category', 'UNCATEGORIZED')
                self.data['tags'][attribs['Tag']] = category

            # CivilizationDomain (often in shell-scoped files with domain attribute)
            if 'domain' in attribs and 'Civilization' in attribs:
                self.data['civilization_domains'].add(attribs['domain'])

            # Additional types from constructibles, units, etc.
            
            # ConstructibleClass
            if 'ConstructibleClass' in attribs:
                self.data['constructible_classes'].add(attribs['ConstructibleClass'])
            
            # UnitMovementClass
            if 'UnitMovementClass' in attribs:
                self.data['unit_movement_classes'].add(attribs['UnitMovementClass'])
            
            # CoreClass
            if 'CoreClass' in attribs:
                self.data['core_classes'].add(attribs['CoreClass'])
            
            # FormationClass
            if 'FormationClass' in attribs:
                self.data['formation_classes'].add(attribs['FormationClass'])
            
            # Domain
            if 'Domain' in attribs:
                self.data['domains'].add(attribs['Domain'])
            
            # MilitaryDomain
            if 'MilitaryDomain' in attribs:
                self.data['military_domains'].add(attribs['MilitaryDomain'])
            
            # CostProgressionModel
            if 'CostProgressionModel' in attribs:
                self.data['cost_progression_models'].add(attribs['CostProgressionModel'])
            
            # BiomeType
            if 'BiomeType' in attribs:
                self.data['biome_types'].add(attribs['BiomeType'])
            
            # FeatureType
            if 'FeatureType' in attribs:
                self.data['feature_types'].add(attribs['FeatureType'])
            
            # RiverPlacement
            if 'RiverPlacement' in attribs:
                self.data['river_placements'].add(attribs['RiverPlacement'])
            
            # Age
            if 'Age' in attribs:
                self.data['ages'].add(attribs['Age'])
            
            # PromotionClass
            if 'PromotionClass' in attribs:
                self.data['promotion_classes'].add(attribs['PromotionClass'])
            
            # GovernmentType
            if 'GovernmentType' in attribs:
                self.data['government_types'].add(attribs['GovernmentType'])
            
            # ProjectType
            if 'ProjectType' in attribs:
                self.data['project_types'].add(attribs['ProjectType'])
            
            # BeliefClassType
            if 'BeliefClassType' in attribs:
                self.data['belief_class_types'].add(attribs['BeliefClassType'])
            
            # DifficultyType
            if 'DifficultyType' in attribs:
                self.data['difficulty_types'].add(attribs['DifficultyType'])
            
            # ProgressionTree
            if 'ProgressionTree' in attribs:
                self.data['progression_trees'].add(attribs['ProgressionTree'])
            
            # GreatWorkObjectType - from Type Kind
            if tag == 'Row' and 'Type' in attribs and 'Kind' in attribs:
                if attribs['Kind'] == 'KIND_GREATWORKOBJECT':
                    self.data['great_work_object_types'].add(attribs['Type'])
            
            # Unit - from Type Kind
            if tag == 'Row' and 'Type' in attribs and 'Kind' in attribs:
                if attribs['Kind'] == 'KIND_UNIT':
                    self.data['units'].add(attribs['Type'])
            
            # Constructibles - from ConstructibleType attribute
            if 'ConstructibleType' in attribs:
                constructible_type = attribs['ConstructibleType']
                if (constructible_type.startswith('BUILDING_') or 
                    constructible_type.startswith('IMPROVEMENT_') or 
                    constructible_type.startswith('WONDER_')):
                    self.data['constructibles'].add(constructible_type)
            
            # UnitAbilities - extract ability types from UnitAbilityType attribute
            # This captures abilities from UnitAbilities, UnitClass_Abilities, and UnitAbilityModifiers tables
            if 'UnitAbilityType' in attribs:
                ability_type = attribs['UnitAbilityType']
                if ability_type.startswith('ABILITY_') or ability_type.startswith('CHARGED_ABILITY_'):
                    # If this row has Name and Description, it's from UnitAbilities table - capture metadata
                    if 'Name' in attribs and 'Description' in attribs:
                        loc_description = attribs.get('Description', '')
                        # Resolve LOC_ key to English text (will be done in finalize phase)
                        self.data['unit_abilities'][ability_type] = {
                            'name': attribs.get('Name', ''),
                            'description': loc_description,
                            'description_text': ''  # Will be resolved later
                        }
                    # Otherwise just ensure the ability exists in the dict
                    elif ability_type not in self.data['unit_abilities']:
                        self.data['unit_abilities'][ability_type] = {'name': '', 'description': '', 'description_text': ''}
            
            # Track units unlocked by progression tree nodes (for age mapping)
            # ProgressionTreeNodeUnlocks table maps progression nodes to units
            if tag == 'Row' and 'ProgressionTreeNodeType' in attribs and \
               'TargetKind' in attribs and 'TargetType' in attribs:
                target_kind = attribs.get('TargetKind')
                target_type = attribs.get('TargetType')
                node_type = attribs.get('ProgressionTreeNodeType')
                
                if target_kind == 'KIND_UNIT' and target_type and node_type:
                    # Track both node type and age
                    if not hasattr(self, '_unit_unlock_nodes'):
                        self._unit_unlock_nodes = defaultdict(set)
                    self._unit_unlock_nodes[target_type].add(node_type)
                    self.unit_unlocks[target_type].add(node_type)
                    # Infer age from node name pattern
                    self._infer_node_age_from_name(node_type)

            # Traditions - extract from Traditions table
            if tag == 'Row' and 'TraditionType' in attribs:
                tradition_type = attribs['TraditionType']
                # Only add if this row has Name attribute (Traditions table, not TraditionModifiers)
                if 'Name' in attribs:
                    name_loc = attribs.get('Name', '')
                    desc_loc = attribs.get('Description', '')
                    is_crisis = attribs.get('IsCrisis', 'false').lower() == 'true'
                    age_type = attribs.get('AgeType', '')
                    trait_type = attribs.get('TraitType', '')
                    
                    # Store tradition data
                    self.data['traditions'][tradition_type] = {
                        'name_loc': name_loc,
                        'description_loc': desc_loc,
                        'is_crisis': is_crisis,
                        'age': age_type if age_type else era_id,  # Use file-inferred era if not explicit
                        'trait_type': trait_type,
                        'modifiers': []
                    }
            
            # TraditionModifiers - track which modifiers are attached to traditions
            if tag == 'Row' and 'TraditionType' in attribs and 'ModifierId' in attribs:
                tradition_type = attribs['TraditionType']
                modifier_id = attribs['ModifierId']
                # Add modifier to tradition if it exists
                if tradition_type in self.data['traditions']:
                    self.data['traditions'][tradition_type]['modifiers'].append(modifier_id)
                # Otherwise create a placeholder (modifier-only reference)
                elif not any(k in attribs for k in ['Name', 'Description']):
                    if tradition_type not in self.data['traditions']:
                        self.data['traditions'][tradition_type] = {
                            'name_loc': '',
                            'description_loc': '',
                            'is_crisis': False,
                            'age': era_id,
                            'trait_type': '',
                            'modifiers': [modifier_id]
                        }
                    else:
                        self.data['traditions'][tradition_type]['modifiers'].append(modifier_id)

            # UnitReplaces - extract unit replacement mappings
            if tag == 'Row' and 'CivUniqueUnitType' in attribs and 'ReplacesUnitType' in attribs:
                unique_unit = attribs['CivUniqueUnitType']
                replaces_unit = attribs['ReplacesUnitType']
                self.unit_replaces[unique_unit] = replaces_unit

            # ResourceClass - infer from resource type patterns
            if tag == 'Row' and 'Type' in attribs and 'Kind' in attribs:
                if attribs['Kind'] == 'KIND_RESOURCE':
                    resource_type = attribs['Type']
                    # Try to infer class from naming patterns
                    if 'STRATEGIC' in resource_type:
                        self.data['resource_classes'].add('RESOURCE_CLASS_STRATEGIC')
                    elif 'LUXURY' in resource_type:
                        self.data['resource_classes'].add('RESOURCE_CLASS_LUXURY')
                    elif 'BONUS' in resource_type:
                        self.data['resource_classes'].add('RESOURCE_CLASS_BONUS')
            
            # HandicapSystemType
            if 'HandicapSystemType' in attribs:
                self.data['handicap_system_types'].add(attribs['HandicapSystemType'])

            # Leader - from LeaderCivPriorities and similar tables
            if 'Leader' in attribs:
                leader = attribs['Leader']
                if leader.startswith('LEADER_'):
                    self.data['leaders'].add(leader)
            
            # TraitType - extract civilization traits (TRAIT_ATTRIBUTE_* and *_CIV variants)
            if tag == 'Row' and 'TraitType' in attribs:
                trait = attribs['TraitType']
                # Include civilization attribute traits and age-specific civ traits
                if (trait.startswith('TRAIT_ATTRIBUTE_') or 
                    trait.endswith('_CIV') or
                    'ABILITY' in trait):
                    self.data['civilization_traits'].add(trait)
                # Separate leader attributes for dedicated collection
                if 'TRAIT_LEADER_ATTRIBUTE_' in trait:
                    self.data['leader_attributes'].add(trait)

            # Civilization - ONLY from Civilizations table with UniqueCultureProgressionTree
            # This filters out unlock references to DLC/unreleased content
            if tag == 'Row' and 'CivilizationType' in attribs and 'UniqueCultureProgressionTree' in attribs:
                civ_type = attribs['CivilizationType']
                if civ_type.startswith('CIVILIZATION_'):
                    self.data['civilizations'].add(civ_type)
                    # Capture UniqueCultureProgressionTree to map age
                    tree_id = attribs['UniqueCultureProgressionTree']
                    self.civilization_ages[civ_type] = tree_id
                    
                    # Also track era if we're in an era-specific file
                    if era_id and civ_type not in self.civ_era_mapping:
                        self.civ_era_mapping[civ_type] = era_id
            
            # ProgressionTree age mapping
            if tag == 'Row' and 'ProgressionTreeType' in attribs and 'AgeType' in attribs:
                tree_id = attribs['ProgressionTreeType']
                age_id = attribs['AgeType']
                # Store mapping for later lookup
                self._tree_ages[tree_id] = age_id
            
            # Progression tree nodes - try to extract age information
            if tag == 'Row' and 'ProgressionTreeNodeType' in attribs:
                node_type = attribs['ProgressionTreeNodeType']
                # Infer age from node name pattern (e.g., NODE_TECH_AQ_AGRICULTURE)
                self._infer_node_age_from_name(node_type)

    def _get_civ_name_from_path(self, file_path: Path) -> str:
        """Extract civilization name from file path."""
        parts = file_path.parts
        for part in parts:
            if part.startswith('CIVILIZATION_'):
                return part
            # Match civilization folders like 'babylon', 'assyria', etc.
            for potential_civ in ['babylon', 'assyria', 'bulgaria', 'carthage', 'dal-viet',
                                   'great-britain', 'iceland', 'nepal', 'ottomans',
                                   'pirate-republic', 'qajar', 'tonga']:
                if potential_civ in part.lower():
                    return f"CIVILIZATION_{potential_civ.upper().replace('-', '_')}"
        return 'UNKNOWN'

    def _resolve_civ_age(self, civ_id: str) -> str:
        """Resolve civilization age from progression tree."""
        if civ_id not in self.civilization_ages:
            return None
        
        tree_id = self.civilization_ages[civ_id]
        
        # Try to look up age from tree mappings
        if tree_id in self._tree_ages:
            return self._tree_ages[tree_id]
        
        # Fallback: infer age from tree ID pattern
        if 'AQ' in tree_id or '_ANTIQUITY' in tree_id:
            return 'AGE_ANTIQUITY'
        elif 'EX' in tree_id or '_EXPLORATION' in tree_id:
            return 'AGE_EXPLORATION'
        elif 'MO' in tree_id or '_MODERN' in tree_id:
            return 'AGE_MODERN'
        
        return None
    
    def _infer_node_age(self, node_type: str, age_id: str) -> None:
        """Store inferred age for a progression tree node."""
        if not hasattr(self, '_node_ages'):
            self._node_ages = {}
        self._node_ages[node_type] = age_id
    
    def _infer_node_age_from_name(self, node_type: str) -> None:
        """Infer and store age from node type name pattern."""
        if not hasattr(self, '_node_ages'):
            self._node_ages = {}
        
        if node_type in self._node_ages:
            return  # Already mapped
        
        # Parse node name: NODE_TECH_AQ_*, NODE_CIVIC_AQ_*, NODE_TECH_EX_*, etc.
        if '_AQ_' in node_type or node_type.endswith('_AQ'):
            self._node_ages[node_type] = 'AGE_ANTIQUITY'
        elif '_EX_' in node_type or node_type.endswith('_EX'):
            self._node_ages[node_type] = 'AGE_EXPLORATION'
        elif '_MO_' in node_type or node_type.endswith('_MO'):
            self._node_ages[node_type] = 'AGE_MODERN'
    
    def _resolve_unit_ages(self) -> None:
        """Resolve ages for all units based on progression tree unlocks."""
        if not hasattr(self, '_unit_unlock_nodes'):
            return
        
        node_ages = getattr(self, '_node_ages', {})
        
        for unit_type, node_types in self._unit_unlock_nodes.items():
            for node_type in node_types:
                if node_type in node_ages:
                    self.unit_ages[unit_type].add(node_ages[node_type])

    def _write_json(self, filename: str, data: Dict | List | Set) -> None:
        """Write data to JSON file in kebab-case naming."""
        output_dir = self.root / 'src' / 'civ7_modding_tools' / 'data'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Convert sets to lists for JSON serialization
        if isinstance(data, dict):
            data = {k: sorted(list(v)) if isinstance(v, set) else v
                    for k, v in data.items()}
        elif isinstance(data, set):
            data = sorted(list(data))

        output_file = output_dir / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"[OK] Written {output_file}")

    def _guess_name(self, id_str: str) -> str:
        """Guess a human-readable name from the ID."""
        mappings = {
            # Building Cultures
            'ANT_MUD': 'Antiquity - Mud/Brick',
            'ANT_STONE': 'Antiquity - Stone',
            'BUILDING_CULTURE_EAS': 'East Asian',
            'BUILDING_CULTURE_EEU': 'Eastern European',
            'BUILDING_CULTURE_MED': 'Mediterranean',
            'BUILDING_CULTURE_MID': 'Middle Eastern',
            'BUILDING_CULTURE_MID_ANT': 'Middle Eastern (Antiquity)',
            'BUILDING_CULTURE_MID_MOD': 'Middle Eastern (Modern)',
            'BUILDING_CULTURE_NAF': 'North African',
            'BUILDING_CULTURE_NAM': 'North American',
            'BUILDING_CULTURE_NEU': 'Northern European',
            'BUILDING_CULTURE_PAC': 'Pacific',
            'BUILDING_CULTURE_PAC_EXP': 'Pacific (Exploration)',
            'BUILDING_CULTURE_SAM': 'South American',
            'BUILDING_CULTURE_SEA': 'Southeast Asian',
            'EXP_MUD': 'Exploration - Mud/Brick',
            'EXP_STONE': 'Exploration - Stone',
            'MOD_MUD': 'Modern - Mud/Brick',
            'MOD_STONE': 'Modern - Stone',

            # Unit Cultures
            'Afr': 'African',
            'Asian': 'Asian',
            'Euro': 'European',
            'IND': 'Indian',
            'Med': 'Mediterranean',
            'MidE': 'Middle Eastern',
            'NAmer': 'North American',
            'PAC': 'Pacific',
            'SAmer': 'South American',
            'SEA': 'Southeast Asian',
        }
        
        if id_str in mappings:
            return mappings[id_str]

        # Dynamic guessing
        if id_str.startswith('CIVILIZATION_'):
            name = id_str.replace('CIVILIZATION_', '').replace('_', ' ').lower().title()
            name = name.replace('Ip ', 'Independent Power ')
            return name
            
        return ""

    def export_json_files(self) -> None:
        """Export all extracted data to JSON files."""
        # Resolve unit ages before exporting
        self._resolve_unit_ages()
        # Resolve tradition localizations
        self._resolve_tradition_localizations()
        
        # BuildingCulture split into two categories:
        # 1. Palace/Premium styles (BUILDING_CULTURE_XXX)
        # 2. Age-specific variants (ANT_*, EXP_*, MOD_*)
        palace_cultures = []
        age_cultures = []
        
        for bc, civs in sorted(self.data['building_cultures'].items()):
            if not civs:
                continue
            
            # Determine which eras this building culture is used in
            eras = []
            if bc in self.data['building_cultures_by_era']:
                eras = sorted(self.data['building_cultures_by_era'][bc].keys())
            else:
                # Backfill: for each civ using this culture, look up its era
                eras_set = set()
                for civ_name in civs:
                    # Try to find the civilization in our era mapping
                    if civ_name in self.civ_era_mapping:
                        eras_set.add(self.civ_era_mapping[civ_name])
                    else:
                        # Try converting civ folder name to civ type and check again
                        civ_type = f"CIVILIZATION_{civ_name.upper().replace('-', '_')}"
                        if civ_type in self.civ_era_mapping:
                            eras_set.add(self.civ_era_mapping[civ_type])
                eras = sorted(eras_set)
            
            culture_entry = {
                'id': bc,
                'name': self._guess_name(bc),
                'description': f"Building culture used by: {', '.join(sorted(civs))}",
                'civilizations': sorted(civs)
            }
            
            # Add eras field for palace cultures only
            if bc.startswith('BUILDING_CULTURE_'):
                culture_entry['eras'] = eras
            
            # Categorise: palace styles start with BUILDING_CULTURE_
            # Age variants start with ANT_, EXP_, or MOD_
            if bc.startswith('BUILDING_CULTURE_'):
                palace_cultures.append(culture_entry)
            else:  # ANT_, EXP_, MOD_, or other age prefix
                age_cultures.append(culture_entry)
        
        # Export palace/premium building cultures
        building_cultures_palace = {'values': palace_cultures}
        self._write_json('building-cultures-palace.json', building_cultures_palace)
        
        # Export age-specific building cultures
        building_cultures_ages = {'values': age_cultures}
        self._write_json('building-cultures-ages.json', building_cultures_ages)

        # Export building material bases derived from age variants
        base_map: dict[str, str] = {}
        for culture in age_cultures:
            culture_id = culture['id']
            if '_' in culture_id:
                suffix = culture_id.split('_', 1)[1]
                if suffix not in base_map:
                    friendly_name = culture.get('name', suffix).split(' - ', 1)[-1]
                    base_map[suffix] = friendly_name

        building_culture_bases = {
            'values': [
                {'id': base_id, 'name': base_name}
                for base_id, base_name in sorted(base_map.items())
            ]
        }
        self._write_json('building-culture-bases.json', building_culture_bases)

        # UnitCulture with civ context
        unit_cultures = {
            'values': [
                {
                    'id': uc,
                    'name': self._guess_name(uc),
                    'description': f"Unit culture used by: {', '.join(sorted(civs))}",
                    'civilizations': sorted(civs)
                }
                for uc, civs in sorted(self.data['unit_cultures'].items())
                if civs
            ]
        }
        self._write_json('unit-cultures.json', unit_cultures)

        # TerrainType
        terrain_types = {
            'values': [{'id': tt} for tt in sorted(self.data['terrain_types'])]
        }
        self._write_json('terrain-types.json', terrain_types)

        # DistrictType
        district_types = {
            'values': [{'id': dt} for dt in sorted(self.data['district_types'])]
        }
        self._write_json('district-types.json', district_types)

        # YieldType
        yield_types = {
            'values': [{'id': yt} for yt in sorted(self.data['yield_types'])]
        }
        self._write_json('yield-types.json', yield_types)

        # AdvisoryClassType
        advisory_types = {
            'values': [{'id': act} for act in sorted(self.data['advisory_class_types'])]
        }
        self._write_json('advisory-class-types.json', advisory_types)

        # Effects
        effects = {
            'values': [{'id': e} for e in sorted(self.data['effects'])]
        }
        self._write_json('effects.json', effects)

        # Requirements
        requirements = {
            'values': [{'id': r} for r in sorted(self.data['requirement_types'])]
        }
        self._write_json('requirement-types.json', requirements)

        # Collections
        collections = {
            'values': [{'id': c} for c in sorted(self.data['collection_types'])]
        }
        self._write_json('collection-types.json', collections)

        # Tags
        tags = {
            'values': [
                {
                    'id': tag,
                    'category': category
                }
                for tag, category in sorted(self.data['tags'].items())
            ]
        }
        self._write_json('tags.json', tags)

        # CivilizationDomains
        domains = {
            'values': [{'id': d} for d in sorted(self.data['civilization_domains'])]
        }
        self._write_json('civilization-domains.json', domains)

        # ConstructibleClass
        constructible_classes = {
            'values': [{'id': cc} for cc in sorted(self.data['constructible_classes'])]
        }
        self._write_json('constructible-classes.json', constructible_classes)

        # UnitMovementClass
        unit_movement_classes = {
            'values': [{'id': umc} for umc in sorted(self.data['unit_movement_classes'])]
        }
        self._write_json('unit-movement-classes.json', unit_movement_classes)

        # CoreClass
        core_classes = {
            'values': [{'id': cc} for cc in sorted(self.data['core_classes'])]
        }
        self._write_json('core-classes.json', core_classes)

        # FormationClass
        formation_classes = {
            'values': [{'id': fc} for fc in sorted(self.data['formation_classes'])]
        }
        self._write_json('formation-classes.json', formation_classes)

        # Domain
        domains_list = {
            'values': [{'id': d} for d in sorted(self.data['domains'])]
        }
        self._write_json('domains.json', domains_list)

        # CostProgressionModel
        cost_progression_models = {
            'values': [{'id': cpm} for cpm in sorted(self.data['cost_progression_models'])]
        }
        self._write_json('cost-progression-models.json', cost_progression_models)

        # BiomeType
        biome_types = {
            'values': [{'id': bt} for bt in sorted(self.data['biome_types'])]
        }
        self._write_json('biome-types.json', biome_types)

        # FeatureType
        feature_types = {
            'values': [{'id': ft} for ft in sorted(self.data['feature_types'])]
        }
        self._write_json('feature-types.json', feature_types)

        # RiverPlacement
        river_placements = {
            'values': [{'id': rp} for rp in sorted(self.data['river_placements'])]
        }
        self._write_json('river-placements.json', river_placements)

        # Age
        ages = {
            'values': [{'id': a} for a in sorted(self.data['ages'])]
        }
        self._write_json('ages.json', ages)

        # MilitaryDomain
        military_domains = {
            'values': [{'id': md} for md in sorted(self.data['military_domains'])]
        }
        self._write_json('military-domains.json', military_domains)

        # PromotionClass
        promotion_classes = {
            'values': [{'id': pc} for pc in sorted(self.data['promotion_classes'])]
        }
        self._write_json('promotion-classes.json', promotion_classes)

        # GovernmentType
        government_types = {
            'values': [{'id': gt} for gt in sorted(self.data['government_types'])]
        }
        self._write_json('government-types.json', government_types)

        # ProjectType
        project_types = {
            'values': [{'id': pt} for pt in sorted(self.data['project_types'])]
        }
        self._write_json('project-types.json', project_types)

        # BeliefClassType
        belief_class_types = {
            'values': [{'id': bct} for bct in sorted(self.data['belief_class_types'])]
        }
        self._write_json('belief-class-types.json', belief_class_types)

        # DifficultyType
        difficulty_types = {
            'values': [{'id': dt} for dt in sorted(self.data['difficulty_types'])]
        }
        self._write_json('difficulty-types.json', difficulty_types)

        # ProgressionTree
        progression_trees = {
            'values': [{'id': pt} for pt in sorted(self.data['progression_trees'])]
        }
        self._write_json('progression-trees.json', progression_trees)

        # GreatWorkObjectType
        great_work_object_types = {
            'values': [{'id': gwot} for gwot in sorted(self.data['great_work_object_types'])]
        }
        self._write_json('great-work-object-types.json', great_work_object_types)

        # ResourceClass
        resource_classes = {
            'values': [{'id': rc} for rc in sorted(self.data['resource_classes'])]
        }
        self._write_json('resource-classes.json', resource_classes)

        # HandicapSystemType
        handicap_system_types = {
            'values': [{'id': hst} for hst in sorted(self.data['handicap_system_types'])]
        }
        self._write_json('handicap-system-types.json', handicap_system_types)

        # Leader
        leaders = {
            'values': [{'id': l} for l in sorted(self.data['leaders'])]
        }
        self._write_json('leaders.json', leaders)

        # Unit
        units = {
            'values': [
                {
                    'id': u,
                    'ages': sorted(list(self.unit_ages.get(u, set())))
                        if self.unit_ages.get(u)
                        else [],
                    'unlocked_by': sorted(list(self.unit_unlocks.get(u, set())))
                        if self.unit_unlocks.get(u)
                        else [],
                    'replaces': self.unit_replaces.get(u, None)
                }
                for u in sorted(self.data['units'])
            ]
        }
        self._write_json('units.json', units)

        # UnitAbilities
        unit_abilities = {
            'values': [
                {
                    'id': ability_id,
                    'name': ability_data.get('name', ''),
                    'description': ability_data.get('description', ''),
                    'description_text': ability_data.get('description_text', '')
                }
                for ability_id, ability_data in sorted(self.data['unit_abilities'].items())
            ]
        }
        self._write_json('unit-abilities.json', unit_abilities)

        # LeaderAttribute
        leader_attributes = {
            'values': [{'id': la} for la in sorted(self.data['leader_attributes'])]
        }
        self._write_json('leader-attributes.json', leader_attributes)

        # Civilization Traits (TRAIT_ATTRIBUTE_* and civilization variants)
        civilization_traits = {
            'values': [{'id': t} for t in sorted(self.data['civilization_traits'])]
        }
        self._write_json('civilization-traits.json', civilization_traits)

        # Civilization
        civilizations = {
            'values': [
                {
                    'id': c,
                    'age': self._resolve_civ_age(c)
                }
                for c in sorted(self.data['civilizations'])
                if not c.startswith('CIVILIZATION_NONE')  # Exclude placeholder civs
            ]
        }
        self._write_json('civilizations.json', civilizations)

        # Constructibles (Buildings, Improvements, Wonders)
        constructibles = {
            'values': [{'id': c} for c in sorted(self.data['constructibles'])]
        }
        self._write_json('constructibles.json', constructibles)

        # Traditions (policies)
        traditions = {
            'name': 'traditions',
            'description': 'Base game traditions (policies) available across all ages',
            'values': [
                {
                    'id': tradition_id,
                    'name': tradition_data.get('name', ''),
                    'description': tradition_data.get('description', ''),
                    'age': tradition_data.get('age', ''),
                    'trait_type': tradition_data.get('trait_type', ''),
                    'is_crisis': tradition_data.get('is_crisis', False),
                    'modifiers': tradition_data.get('modifiers', [])
                }
                for tradition_id, tradition_data in sorted(self.data['traditions'].items())
                if not tradition_data.get('is_crisis', False)  # Exclude crisis policies for cleaner UI
            ]
        }
        self._write_json('traditions.json', traditions)

        # Modifiers (game effects)
        modifiers = {
            'name': 'modifiers',
            'description': 'Base game modifiers available across all game elements',
            'values': [
                {
                    'id': modifier_id,
                    'effect': modifier_data.get('effect', ''),
                    'collection': modifier_data.get('collection', ''),
                    'description': modifier_data.get('description', ''),
                    'permanent': modifier_data.get('permanent', False),
                    'arguments': modifier_data.get('arguments', {})
                }
                for modifier_id, modifier_data in sorted(self.data['modifiers'].items())
                # Only include modifiers with descriptions for cleaner UI
                if modifier_data.get('description', '')
            ]
        }
        self._write_json('modifiers.json', modifiers)


def main() -> None:
    """Run the extractor."""
    # Use the repository root, not the script directory
    root_dir = Path(__file__).parent.parent.parent.parent
    print(f"Scanning Civ VII data files in {root_dir}...")
    print()

    extractor = CivVIIDataExtractor(root_dir)
    extractor.scan_files()
    extractor.export_json_files()

    print()
    print("Data extraction complete!")


if __name__ == '__main__':
    main()
