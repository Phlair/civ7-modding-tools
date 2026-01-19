#!/usr/bin/env python3
"""
Extract all reference values from Civ VII EXAMPLE folders and dist-* outputs.

Scans XML files to harvest valid values for:
- BuildingCulture
- TerrainType
- UnitCulture
- effect (from GameEffects modifiers)
- CivilizationDomain
- Tag
- DistrictType
- YieldType
- AdvisoryClassType

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
            'building_cultures': defaultdict(set),  # BuildingCulture -> {civs}
            'terrain_types': set(),
            'unit_cultures': defaultdict(set),  # UnitCulture -> {civs}
            'effects': set(),
            'civilization_domains': set(),
            'tags': defaultdict(str),  # Tag -> Category
            'district_types': set(),
            'yield_types': set(),
            'advisory_class_types': set(),
            'requirement_types': set(),
            'collection_types': set(),
        }
        self.civ_cache = defaultdict(dict)  # {folder: {BuildingCulture -> civ}}

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


def main() -> None:
    """Run the extractor."""
    root_dir = Path(__file__).parent
    print(f"Scanning Civ VII data files in {root_dir}...")
    print()

    extractor = CivVIIDataExtractor(root_dir)
    extractor.scan_files()
    extractor.export_json_files()

    print()
    print("✓ Data extraction complete!")


if __name__ == '__main__':
    main()
