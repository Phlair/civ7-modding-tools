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
        }
        self.civ_cache = defaultdict(dict)

    def scan_files(self) -> None:
        """Recursively scan all XML files in EXAMPLE and dist folders."""
        # Example folders
        for example_dir in self.root.glob('*-EXAMPLE'):
            self._scan_directory(example_dir, is_example=True)

        # dist-* folders
        for dist_dir in self.root.glob('dist-*'):
            self._scan_directory(dist_dir, is_example=False)

    def _scan_directory(self, directory: Path, is_example: bool = False) -> None:
        """Scan a directory for XML files."""
        for xml_file in directory.rglob('*.xml'):
            try:
                self._extract_from_file(xml_file)
            except Exception as e:
                print(f"Warning: Failed to parse {xml_file}: {e}")

    def _extract_from_file(self, file_path: Path) -> None:
        """Extract values from a single XML file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError:
            return

        # Get civilization name from folder structure if available
        civ_name = self._get_civ_name_from_path(file_path)

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

            # BuildingCulture
            if 'BuildingCulture' in attribs:
                bc = attribs['BuildingCulture']
                self.data['building_cultures'][bc].add(civ_name)

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
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Written {output_file}")

    def export_json_files(self) -> None:
        """Export all extracted data to JSON files."""
        # BuildingCulture with civ context
        building_cultures = {
            'values': [
                {
                    'id': bc,
                    'description': f"Building culture used by: {', '.join(sorted(civs))}",
                    'civilizations': sorted(civs)
                }
                for bc, civs in sorted(self.data['building_cultures'].items())
                if civs
            ]
        }
        self._write_json('building-cultures.json', building_cultures)

        # UnitCulture with civ context
        unit_cultures = {
            'values': [
                {
                    'id': uc,
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
    print("✓ Data extraction complete!")


if __name__ == '__main__':
    main()
