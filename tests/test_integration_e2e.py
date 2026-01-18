"""Integration/E2E Tests for Civ7 Modding Tools.

These tests verify end-to-end mod generation and ensure parity with TypeScript version.
Tests create actual mod structures, validate XML output, and ensure inter-builder compatibility.
"""

import pytest
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET

from civ7_modding_tools.core import Mod
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    CivilizationUnlockBuilder,
    LeaderUnlockBuilder,
    ProgressionTreeBuilder,
    ModifierBuilder,
)
from civ7_modding_tools.constants import (
    Trait,
    UnitClass,
    Yield,
)
from civ7_modding_tools.localizations import (
    CivilizationLocalization,
    UnitLocalization,
    ConstructibleLocalization,
)
from civ7_modding_tools.files import XmlFile


class TestEndToEndModGeneration:
    """End-to-end integration tests for complete mod generation."""

    def test_single_civilization_mod_generation(self):
        """Test generating a mod with single civilization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({
                "id": "test_mod_single_civ",
                "version": "1.0",
                "name": "Test Single Civilization",
                "description": "Test mod with single civilization",
            })
            
            civ_builder = CivilizationBuilder().fill({
                "civilization_type": "CIVILIZATION_TEST",
                "civilization": {
                    "base_tourism": 2,
                    "base_loyalty": 3,
                },
                "civilization_traits": [Trait.ECONOMIC.value],
                "localizations": [
                    CivilizationLocalization(
                        name="Test Civilization",
                        description="A test civilization",
                        city_names=["TestCity1", "TestCity2"],
                    )
                ]
            })
            
            mod.add(civ_builder)
            mod.build(tmpdir)
            
            # Verify files were generated
            modinfo_file = Path(tmpdir) / "test_mod_single_civ.modinfo"
            assert modinfo_file.exists(), "modinfo file not created"
            
            # Verify XML structure
            tree = ET.parse(modinfo_file)
            root = tree.getroot()
            assert root.tag == "Mod"

    def test_civilization_with_multiple_units_mod(self):
        """Test mod with civilization and multiple unit types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({
                "id": "test_mod_civ_units",
                "version": "1.0",
                "name": "Civilization with Units",
            })
            
            # Add civilization
            civ = CivilizationBuilder().fill({
                "civilization_type": "CIVILIZATION_GONDOR",
                "civilization": {"base_tourism": 1},
                "civilization_traits": [Trait.MILITARY.value],
                "localizations": [CivilizationLocalization(name="Gondor")]
            })
            
            # Add multiple units
            unit1 = UnitBuilder().fill({
                "unit_type": "UNIT_GONDOR_RANGER",
                "unit": {
                    "unit_class": UnitClass.RECON.value,
                    "combat": 20,
                    "movement": 3,
                },
                "unit_costs": [
                    {"yield_type": Yield.PRODUCTION.value, "amount": 50}
                ],
                "localizations": [UnitLocalization(name="Gondor Ranger")]
            })
            
            unit2 = UnitBuilder().fill({
                "unit_type": "UNIT_GONDOR_KNIGHT",
                "unit": {
                    "unit_class": UnitClass.MELEE.value,
                    "combat": 35,
                    "movement": 2,
                },
                "unit_costs": [
                    {"yield_type": Yield.PRODUCTION.value, "amount": 75}
                ],
                "localizations": [UnitLocalization(name="Gondor Knight")]
            })
            
            mod.add(civ)
            mod.add([unit1, unit2])
            mod.build(tmpdir)
            
            # Verify output structure
            modinfo_file = Path(tmpdir) / "test_mod_civ_units.modinfo"
            assert modinfo_file.exists()
            
            # Verify units were written
            units_dir = Path(tmpdir) / "units"
            assert units_dir.exists()
            assert (units_dir / "unit_gondor_ranger").exists()
            assert (units_dir / "unit_gondor_knight").exists()

    def test_constructible_buildings_mod(self):
        """Test mod with various constructible types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({
                "id": "test_mod_buildings",
                "version": "1.0",
                "name": "Buildings and Improvements",
            })
            
            # Create building
            building = ConstructibleBuilder().fill({
                "constructible_type": "BUILDING_GONDOR_ARMORY",
                "constructible": {
                    "cost": 100,
                    "maintenance": 2,
                    "district_type": "DISTRICT_ENCAMPMENT",
                },
                "yield_changes": [
                    {"yield_type": Yield.PRODUCTION.value, "amount": 3},
                    {"yield_type": Yield.CULTURE.value, "amount": 1},
                ],
                "localizations": [
                    ConstructibleLocalization(name="Gondor Armory")
                ]
            })
            
            mod.add(building)
            mod.build(tmpdir)
            
            # Verify constructible generated
            constructibles_dir = Path(tmpdir) / "constructibles"
            assert constructibles_dir.exists()
            assert (constructibles_dir / "building_gondor_armory").exists()

    def test_complex_mod_with_multiple_builder_types(self):
        """Test comprehensive mod using multiple builder types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({
                "id": "test_mod_comprehensive",
                "version": "1.0",
                "name": "Comprehensive Test Mod",
                "description": "Tests all builder types together",
            })
            
            # Add civilization
            civ = CivilizationBuilder().fill({
                "civilization_type": "CIVILIZATION_TEST",
                "civilization": {"base_tourism": 2},
                "civilization_traits": [Trait.ECONOMIC.value],
                "localizations": [CivilizationLocalization(name="Test")]
            })
            
            # Add unit
            unit = UnitBuilder().fill({
                "unit_type": "UNIT_TEST",
                "unit": {"unit_class": UnitClass.MELEE.value, "combat": 25},
                "localizations": [UnitLocalization(name="Test Unit")]
            })
            
            # Add building
            building = ConstructibleBuilder().fill({
                "constructible_type": "BUILDING_TEST",
                "constructible": {"cost": 150, "district_type": "DISTRICT_COMMERCIAL_HUB"},
                "yield_changes": [{"yield_type": Yield.GOLD.value, "amount": 5}],
                "localizations": [ConstructibleLocalization(name="Test Building")]
            })
            
            # Add progression tree
            tree = ProgressionTreeBuilder().fill({
                "progression_tree_type": "CIVICS_TEST",
                "progression_tree": {"civic_tree_type": "CIVICS_TEST"},
            })
            
            # Add modifier
            modifier = ModifierBuilder().fill({
                "modifier_type": "MOD_TEST",
                "modifier": {"modifier_type": "MOD_TEST"},
            })
            
            mod.add(civ)
            mod.add(unit)
            mod.add(building)
            mod.add(tree)
            mod.add(modifier)
            mod.build(tmpdir)
            
            # Verify all directories created
            assert (Path(tmpdir) / "civilizations" / "civilization_test").exists()
            assert (Path(tmpdir) / "units" / "unit_test").exists()
            assert (Path(tmpdir) / "constructibles" / "building_test").exists()
            assert (Path(tmpdir) / "progression-trees" / "civics_test").exists()
            assert (Path(tmpdir) / "modifiers" / "mod_test").exists()


class TestXmlOutputValidation:
    """Tests to validate XML output structure and content."""

    def test_civilization_xml_structure(self):
        """Test generated civilization XML has correct structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({"id": "test_xml_civ", "version": "1.0"})
            
            civ = CivilizationBuilder().fill({
                "civilization_type": "CIVILIZATION_ROME",
                "civilization": {
                    "base_tourism": 3,
                    "base_loyalty": 2,
                },
                "civilization_traits": [Trait.DIPLOMATIC.value],
                "localizations": [
                    CivilizationLocalization(
                        name="Rome",
                        description="Roman Empire",
                        city_names=["Rome", "Milan"]
                    )
                ]
            })
            
            mod.add(civ)
            mod.build(tmpdir)
            
            # Parse civilization XML
            civ_dir = Path(tmpdir) / "civilizations" / "civilization_rome"
            civ_file = civ_dir / "current.xml"
            
            assert civ_file.exists()
            
            tree = ET.parse(civ_file)
            root = tree.getroot()
            
            # Verify root is Database (Civ7 XML structure)
            assert root.tag == "Database"
            
            # Verify semantic tables exist (new structure)
            assert root.find(".//Civilizations") is not None, "Should have Civilizations table"
            assert root.find(".//Traits") is not None, "Should have Traits table"
            assert root.find(".//Types") is not None, "Should have Types table"
            
            # Verify civilization row exists in Civilizations table
            civ_rows = root.findall(".//Civilizations/Row")
            assert len(civ_rows) > 0
            assert any(
                row.find("CivilizationType").text == "CIVILIZATION_ROME" 
                for row in civ_rows if row.find("CivilizationType") is not None
            )

    def test_unit_xml_with_costs(self):
        """Test unit XML includes costs correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({"id": "test_xml_unit", "version": "1.0"})
            
            unit = UnitBuilder().fill({
                "unit_type": "UNIT_LEGIONARY",
                "unit": {
                    "unit_class": UnitClass.MELEE.value,
                    "combat": 30,
                },
                "unit_costs": [
                    {"yield_type": Yield.PRODUCTION.value, "amount": 75},
                    {"yield_type": Yield.GOLD.value, "amount": 10},
                ],
                "localizations": [UnitLocalization(name="Legionary")]
            })
            
            mod.add(unit)
            mod.build(tmpdir)
            
            unit_file = Path(tmpdir) / "units" / "unit_legionary" / "unit.xml"
            assert unit_file.exists()
            
            tree = ET.parse(unit_file)
            root = tree.getroot()
            
            # Verify semantic tables exist
            assert root.find(".//Units") is not None, "Should have Units table"
            assert root.find(".//Unit_Costs") is not None, "Should have Unit_Costs table"
            
            # Verify cost rows exist in Unit_Costs table
            cost_rows = root.findall(".//Unit_Costs/Row")
            assert len(cost_rows) >= 2

    def test_building_xml_with_yields(self):
        """Test building XML includes yield changes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({"id": "test_xml_building", "version": "1.0"})
            
            building = ConstructibleBuilder().fill({
                "constructible_type": "BUILDING_FORUM",
                "constructible": {
                    "cost": 100,
                    "maintenance": 2,
                    "district_type": "DISTRICT_COMMERCIAL_HUB",
                },
                "yield_changes": [
                    {"yield_type": Yield.GOLD.value, "amount": 4},
                    {"yield_type": Yield.CULTURE.value, "amount": 2},
                ],
                "localizations": [ConstructibleLocalization(name="Forum")]
            })
            
            mod.add(building)
            mod.build(tmpdir)
            
            building_file = Path(tmpdir) / "constructibles" / "building_forum" / "constructible.xml"
            assert building_file.exists()
            
            tree = ET.parse(building_file)
            root = tree.getroot()
            
            # Verify semantic tables exist
            assert root.find(".//Constructibles") is not None, "Should have Constructibles table"
            assert root.find(".//Constructible_YieldChanges") is not None, "Should have Constructible_YieldChanges table"
            
            # Verify yield rows exist in Constructible_YieldChanges table
            yield_rows = root.findall(".//Constructible_YieldChanges/Row")
            assert len(yield_rows) >= 2


class TestLocalizationIntegration:
    """Tests for localization integration across builders."""

    def test_civilization_localizations_stored(self):
        """Test civilization localizations are properly stored."""
        civ = CivilizationBuilder().fill({
            "civilization_type": "CIVILIZATION_EGYPT",
            "civilization": {"base_tourism": 2},
            "localizations": [
                CivilizationLocalization(
                    name="Egypt",
                    description="Gift of the Nile",
                    full_name="The Egyptian Kingdom",
                    adjective="Egyptian",
                    city_names=["Cairo", "Giza", "Luxor"]
                )
            ]
        })
        
        assert len(civ.localizations) == 1
        loc = civ.localizations[0]
        assert loc.name == "Egypt"
        assert loc.full_name == "The Egyptian Kingdom"
        assert len(loc.city_names) == 3

    def test_multiple_builders_with_different_localizations(self):
        """Test multiple builders can have different localization structures."""
        civ_loc = CivilizationLocalization(
            name="Civilization Name",
            city_names=["City1", "City2"]
        )
        
        unit_loc = UnitLocalization(
            name="Unit Name",
            unique_name="Unique Unit"
        )
        
        building_loc = ConstructibleLocalization(
            name="Building Name",
            unique_name="Unique Building"
        )
        
        civ = CivilizationBuilder().fill({
            "civilization_type": "CIV_TEST",
            "civilization": {},
            "localizations": [civ_loc]
        })
        
        unit = UnitBuilder().fill({
            "unit_type": "UNIT_TEST",
            "unit": {},
            "localizations": [unit_loc]
        })
        
        building = ConstructibleBuilder().fill({
            "constructible_type": "BUILDING_TEST",
            "constructible": {},
            "localizations": [building_loc]
        })
        
        assert civ.localizations[0].name == "Civilization Name"
        assert unit.localizations[0].unique_name == "Unique Unit"
        assert building.localizations[0].unique_name == "Unique Building"


class TestModFilesGeneration:
    """Tests for mod file generation and structure."""

    def test_modinfo_file_creation(self):
        """Test .modinfo file is created with correct structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({
                "id": "test_modinfo",
                "version": "1.5",
                "name": "Test ModInfo",
                "description": "Testing modinfo generation",
                "authors": "Test Author",
                "affects_saved_games": True,
            })
            
            civ = CivilizationBuilder().fill({
                "civilization_type": "CIVILIZATION_TEST",
                "civilization": {},
                "localizations": [CivilizationLocalization(name="Test")]
            })
            
            mod.add(civ)
            mod.build(tmpdir)
            
            modinfo_file = Path(tmpdir) / "test_modinfo.modinfo"
            assert modinfo_file.exists()
            
            # Parse and validate structure
            tree = ET.parse(modinfo_file)
            root = tree.getroot()
            assert root.tag == "Mod"

    def test_multiple_mod_generation_isolation(self):
        """Test multiple mods can be generated independently."""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                # Generate mod 1
                mod1 = Mod({"id": "mod_one", "version": "1.0"})
                civ1 = CivilizationBuilder().fill({
                    "civilization_type": "CIVILIZATION_A",
                    "civilization": {},
                    "localizations": [CivilizationLocalization(name="A")]
                })
                mod1.add(civ1)
                mod1.build(tmpdir1)
                
                # Generate mod 2
                mod2 = Mod({"id": "mod_two", "version": "2.0"})
                civ2 = CivilizationBuilder().fill({
                    "civilization_type": "CIVILIZATION_B",
                    "civilization": {},
                    "localizations": [CivilizationLocalization(name="B")]
                })
                mod2.add(civ2)
                mod2.build(tmpdir2)
                
                # Verify isolation
                assert (Path(tmpdir1) / "mod_one.modinfo").exists()
                assert not (Path(tmpdir1) / "mod_two.modinfo").exists()
                
                assert (Path(tmpdir2) / "mod_two.modinfo").exists()
                assert not (Path(tmpdir2) / "mod_one.modinfo").exists()


class TestTypeConsistency:
    """Tests to ensure type consistency across builders."""

    def test_builder_fill_returns_self(self):
        """Test all builders' fill() method returns self for chaining."""
        builders = [
            CivilizationBuilder(),
            UnitBuilder(),
            ConstructibleBuilder(),
            CivilizationUnlockBuilder(),
            LeaderUnlockBuilder(),
            ProgressionTreeBuilder(),
            ModifierBuilder(),
        ]
        
        for builder in builders:
            result = builder.fill({})
            assert result is builder, f"{builder.__class__.__name__}.fill() didn't return self"

    def test_build_returns_file_list(self):
        """Test all builders' build() method returns list of files."""
        builders = [
            CivilizationBuilder().fill({
                "civilization_type": "CIV_TEST",
                "civilization": {}
            }),
            UnitBuilder().fill({
                "unit_type": "UNIT_TEST",
                "unit": {}
            }),
            ConstructibleBuilder().fill({
                "constructible_type": "BUILDING_TEST",
                "constructible": {}
            }),
        ]
        
        for builder in builders:
            result = builder.build()
            assert isinstance(result, list)
            assert all(isinstance(f, XmlFile) for f in result if f is not None)


class TestErrorHandling:
    """Tests for proper error handling in mod generation."""

    def test_empty_mod_still_builds(self):
        """Test mod with no builders still generates modinfo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({
                "id": "empty_mod",
                "version": "1.0",
                "name": "Empty Mod",
            })
            
            mod.build(tmpdir)
            
            # Should create modinfo even with no builders
            modinfo_file = Path(tmpdir) / "empty_mod.modinfo"
            assert modinfo_file.exists()

    def test_builder_without_type_produces_empty_files(self):
        """Test builder without required type produces no files."""
        civ = CivilizationBuilder()
        # Don't fill - no civilization_type set
        
        files = civ.build()
        assert files == []

    def test_multiple_builders_empty_ones_ignored(self):
        """Test mod with mix of valid and empty builders."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mod = Mod({"id": "mixed_mod", "version": "1.0"})
            
            # Valid civilization
            valid_civ = CivilizationBuilder().fill({
                "civilization_type": "CIVILIZATION_VALID",
                "civilization": {},
                "localizations": [CivilizationLocalization(name="Valid")]
            })
            
            # Empty unit (no unit_type)
            empty_unit = UnitBuilder()
            
            mod.add(valid_civ)
            mod.add(empty_unit)
            mod.build(tmpdir)
            
            # Should generate civilization but not unit
            assert (Path(tmpdir) / "civilizations" / "civilization_valid").exists()
            units_dir = Path(tmpdir) / "units"
            # Units directory might not exist if empty
            if units_dir.exists():
                assert len(list(units_dir.iterdir())) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
