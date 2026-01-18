"""
Comprehensive End-to-End Integration Tests for Coverage Enhancement.

This test file aims to simulate a complete mod creation process involving
complex interactions between different builders, specifically targeting
uncovered integration paths in builders.py and mod.py.
"""

import os
import pytest
from pathlib import Path
from civ7_modding_tools import Mod
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ModifierBuilder,
    ProgressionTreeBuilder,
    UnlockBuilder,
    ImportFileBuilder,
    TraditionBuilder,
    UniqueQuarterBuilder,
    CivilizationUnlockBuilder,
    LeaderUnlockBuilder,
    ProgressionTreeNodeBuilder,
)
from civ7_modding_tools.constants import (
    Trait, UnitClass, Age, Effect, Requirement, District, Yield, Terrain, Feature
)
from civ7_modding_tools.utils import trim, kebab_case


class TestFullModIntegration:
    """End-to-End tests simulating full mod generation."""

    def test_comprehensive_mod_build_flow(self, tmp_path):
        """
        Build a large, complex mod with all builder types interacting.
        
        Targets:
        - Mod.build() orchestrating multiple builders
        - CivilizationBuilder.migrate() handling bound modifiers, units, buildings
        - UnlockBuilder complex logic
        - File generation
        """
        # 1. Setup Mod
        mod = Mod(
            "guid-coverage-test",
            "1.0.0",
            "Coverage Test Mod",
            "Testing E2E coverage",
            "Tester",
            True,
        )

        # 2. Create Complex Components
        
        # Modifiers (Stand-alone and Attached)
        # Hitting ModifierBuilder logic
        mod_strength = ModifierBuilder().fill({
            'modifier_id': 'MOD_STRENGTH_BONUS',
            'modifier': {
                'effect_type': Effect.UNIT_ADJUST_COMBAT_STRENGTH,
                'arguments': {'Amount': 10}
            },
            'requirements': [
                {'requirement_type': Requirement.UNIT_TAG_MATCHES, 'arguments': {'Tag': 'CLASS_MELEE'}}
            ]
        })

        mod_culture = ModifierBuilder().fill({
            'modifier_id': 'MOD_CULTURE_YIELD',
            'modifier': {
                'effect_type': Effect.BUILDING_ADJUST_YIELD,
                'arguments': {'YieldType': Yield.CULTURE, 'Amount': 5}
            }
        })

        # Units with detailed stats
        # Hitting UnitBuilder complex branches
        unit_elite = UnitBuilder().fill({
            'unit_type': 'UNIT_COVERAGE_ELITE',
            'unit': {
                'name': 'Elite Guard',
                'description': 'Test Description',
                'maintenance': 5,
                'cost': 200,
                'combat': 60
            },
            'unit_class': UnitClass.MELEE,
            'unit_stats': [
                {'stat_type': 'Combat', 'value': 60},
                {'stat_type': 'Movement', 'value': 3}
            ],
            'unit_costs': [
                {'cost_type': 'Production', 'amount': 200},
                {'cost_type': 'Gold', 'amount': 800}
            ],
            'unit_replaces': [
                {'replaces_unit_type': 'UNIT_WARRIOR'}
            ],
            'combat_ranges': [
                {'range': 1, 'damage': 60}
            ],
            'origin_boosts': [
                {'boost_type': 'Promotion', 'amount': 1}
            ],
            # Attach modifier to unit logic check
            'modifier': mod_strength
        })

        # Buildings
        # Hitting ConstructibleBuilder complex branches
        building_academy = ConstructibleBuilder().fill({
            'constructible_type': 'BUILDING_COVERAGE_ACADEMY',
            'constructible': {
                'name': 'Great Academy',
                'cost': 400
            },
            'yield_changes': [
                {'yield_type': Yield.SCIENCE, 'amount': 10},
                {'yield_type': Yield.CULTURE, 'amount': 5}
            ],
            'valid_districts': [District.CAMPUS, District.GOVERNMENT_PLAZA],
            'prerequisites': [
                {'prerequisite_type': 'Building', 'prerequisite_id': 'BUILDING_LIBRARY'}
            ],
            'unlocks': [
                {'unlock_type': 'Unit', 'unlock_id': 'UNIT_SCIENTIST'}
            ],
            # Attach modifier to building
            'modifier': mod_culture
        })

        # Progression Tree
        # Hitting ProgressionTreeBuilder logic
        node_1 = ProgressionTreeNodeBuilder().fill({
            'node_id': 'NODE_START',
            'node': {'name': 'Start Node'}
        })
        
        tree = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'TREE_COVERAGE_TECH',
            'progression_tree': {'name': 'Tech Tree'},
            'nodes': [node_1]
        })

        # Unlock Builder
        # Hitting UnlockBuilder complex branches
        unlock_bundle = UnlockBuilder().fill({
            'unlock_id': 'UNLOCK_TEST_BUNDLE',
            'unlock': {'name': 'Test Bundle'},
            'unit_unlocks': [{'unit_type': 'UNIT_COVERAGE_ELITE'}],
            'building_unlocks': [{'constructible_type': 'BUILDING_COVERAGE_ACADEMY'}],
            'tech_unlocks': [{'tech_type': 'TECH_WRITING'}],
            'civic_unlocks': [{'civic_type': 'CIVIC_CODE_OF_LAWS'}],
            'district_unlocks': [{'district_type': 'DISTRICT_CAMPUS'}]
        })

        # Tradition
        tradition = TraditionBuilder().fill({
            'tradition_id': 'TRADITION_TEST',
            'tradition': {'name': 'Test Tradition'},
            'effects': [{'effect_type': Effect.CITY_ADJUST_CULTURE, 'arguments': {'Amount': 1}}]
        })
        
        # Unique Quarter
        unique_quarter = UniqueQuarterBuilder().fill({
            'unique_quarter_type': 'QUARTER_TEST',
            'unique_quarter': {'name': 'Test Quarter'},
            'district': District.CAMPUS
        })

        # Civilization - The Hub
        # Binding everything together to test migration logic
        civ = CivilizationBuilder().fill({
            'civilization_type': 'CIVILIZATION_COVERAGE',
            'civilization': {
                'name': 'Coverage Civ',
                'description': 'Civ for tests',
                'adjective': 'Covered'
            },
            'civilization_traits': [Trait.SCIENTIFIC, Trait.CULTURAL],
            'start_bias_biomes': [
                {'biome': 'BIOME_GRASSLAND', 'bias': 5}
            ],
            'start_bias_terrains': [
                {'terrain': 'TERRAIN_PLAINS', 'bias': 3}
            ],
            'localizations': [{
                'name': 'Coverage Civ',
                'description': 'A test civ',
                'city_names': ['TestCity1', 'TestCity2']
            }]
        })

        # File Import
        # Create a dummy file to import
        src_file = tmp_path / "test_icon.png"
        src_file.write_bytes(b"fake image data")
        
        import_file = ImportFileBuilder().fill({
            'source_path': str(src_file),
            'target_name': 'test_icon.png',
            'target_directory': '/imports/icons/'
        })

        # 3. Add Everything to Mod
        # Group 1: The Civ and its bound entities (Simulating how users might structure it)
        civ.bind([unit_elite, building_academy, unique_quarter])
        mod.add([civ, unit_elite, building_academy, unique_quarter])
        
        # Group 2: Loose entities
        mod.add([
            mod_strength,
            mod_culture,
            tree,
            unlock_bundle,
            tradition,
            import_file
        ])
        
        # 4. Build
        output_dir = tmp_path / "build_output"
        mod.build(str(output_dir))

        # 5. Verify Output and Consistency
        # Check Directory Structure
        assert output_dir.exists()
        
        # Check .modinfo
        modinfo = list(output_dir.glob("*.modinfo"))
        assert len(modinfo) == 1
        assert (output_dir / f"{mod.mod_id}.modinfo").exists()
        
        # Check Generated XMLs
        # Civ Output location: /civilizations/coverage-civ/
        civ_dir = output_dir / "civilizations" / kebab_case(trim("CIVILIZATION_COVERAGE"))
        assert civ_dir.exists()
        assert (civ_dir / "current.xml").exists()
        assert (civ_dir / "localization.xml").exists()
        
        # Unit output
        # Should be influenced by civ bind (might be in separate folder or same base depending on logic)
        # Based on naming convention: /units/coverage-elite/
        unit_dir = output_dir / "units" / kebab_case(trim("UNIT_COVERAGE_ELITE"))
        assert unit_dir.exists()
        assert (unit_dir / "current.xml").exists()
        
        # Constructible output
        building_dir = output_dir / "constructibles" / kebab_case(trim("BUILDING_COVERAGE_ACADEMY"))
        assert building_dir.exists()
        
        # Imports
        # Should be in imports folder
        import_dir = output_dir / "imports"
        assert import_dir.exists()
        
    def test_leader_and_civ_unlocks(self, tmp_path):
        """Test the specific Unlock Builders for Leaders and Civs."""
        
        mod = Mod("test-unlocks", "1.0", "Unlock Test")
        
        leader_unlock = LeaderUnlockBuilder().fill({
            'leader_type': 'LEADER_TEST',
            'leader': {},
            'trait_type': 'TRAIT_LEADER_TEST'
        })
        
        civ_unlock = CivilizationUnlockBuilder().fill({
            'civilization_type': 'CIVILIZATION_TEST_UNLOCK',
            'civilization': {},
            'starting_era': Age.ANTIQUITY
        })
        
        mod.add([leader_unlock, civ_unlock])
        
        mod.build(str(tmp_path / "unlocks_out"))
        
        assert (tmp_path / "unlocks_out" / f"{mod.mod_id}.modinfo").exists()


    def test_import_file_builder_edge_cases(self, tmp_path):
        """Test specific edge cases in file importing."""
        
        # Create source
        src = tmp_path / "image.dds"
        src.write_text("fake dds content")
        
        # Case 1: Custom subfolder
        builder1 = ImportFileBuilder().fill({
            'source_path': str(src),
            'target_name': 'image.dds',
            'target_directory': '/imports/ui/icons/'
        })
        
        files = builder1.build()
        assert len(files) == 1
        # ImportFile uses 'name' property, not 'destination'
        assert files[0].name == 'image.dds'
        
        # Case 2: Just filename
        builder2 = ImportFileBuilder().fill({
            'source_path': str(src),
            'target_name': 'root_image.dds'
        })
        
        files2 = builder2.build()
        assert len(files2) == 1
        assert files2[0].name == 'root_image.dds'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
