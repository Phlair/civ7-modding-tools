"""Tests for Phase 2: Builder implementations."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
)
from civ7_modding_tools.files import XmlFile
from civ7_modding_tools.nodes import (
    CivilizationNode,
    CivilizationTraitNode,
    UnitNode,
    CityNameNode,
)


class TestCivilizationBuilder:
    """Tests for CivilizationBuilder."""

    def test_civilization_builder_basic(self):
        """Test basic civilization builder setup."""
        builder = CivilizationBuilder()
        assert builder.civilization_type is None
        assert builder.civilization == {}
        assert builder.civilization_traits == []
        assert builder.city_names == []

    def test_civilization_builder_fill(self):
        """Test filling civilization builder with data."""
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {"base_tourism": 10},
            "civilization_traits": ["TRAIT_ECONOMIC"],
        })
        
        assert builder.civilization_type == "CIVILIZATION_ROME"
        assert builder.civilization == {"base_tourism": 10}
        assert builder.civilization_traits == ["TRAIT_ECONOMIC"]

    def test_civilization_builder_build_empty(self):
        """Test building with no civilization type returns empty files."""
        builder = CivilizationBuilder()
        files = builder.build()
        assert files == []

    def test_civilization_builder_build_basic(self):
        """Test building a basic civilization."""
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {
                "base_tourism": 10,
                "legacy_modifier": True,
            },
            "civilization_traits": ["TRAIT_ECONOMIC", "TRAIT_CULTURAL"],
        })
        
        files = builder.build()
        
        # Should have 6 civilization files (current, legacy, shell, icons, localization, game-effects)
        assert len(files) == 6
        assert all(isinstance(f, XmlFile) for f in files)
        assert "rome" in files[0].path  # Path is kebab-case of trimmed type
        assert files[0].name in ["current.xml", "legacy.xml", "shell.xml", "icons.xml", "localization.xml", "game-effects.xml"]

    def test_civilization_builder_build_content(self):
        """Test that built civilization file contains correct nodes."""
        from civ7_modding_tools.nodes import DatabaseNode
        
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {"base_tourism": 10},
            "civilization_traits": ["TRAIT_ECONOMIC"],
        })
        
        files = builder.build()
        file = files[0]  # current.xml
        
        # Check content is a DatabaseNode
        assert isinstance(file.content, DatabaseNode)
        
        # Should have proper table structure
        db = file.content
        assert len(db.civilizations) == 1
        assert db.civilizations[0].civilization_type == "CIVILIZATION_ROME"
        
        # Should have 2 traits (base trait + ability trait)
        assert len(db.traits) == 2
        assert db.civilization_traits  # At least the default trait + TRAIT_ECONOMIC + ability
        assert any(t.trait_type == "TRAIT_ECONOMIC" for t in db.civilization_traits)

    def test_civilization_builder_with_city_names(self):
        """Test civilization builder with city names."""
        from civ7_modding_tools.nodes import DatabaseNode
        
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {},
            "city_names": ["Rome", "Milan", "Venice"],
        })
        
        files = builder.build()
        
        # Should have 6 civilization files
        assert len(files) == 6
        current_file = [f for f in files if f.name == "current.xml"][0]
        
        # DatabaseNode should have city names
        db = current_file.content
        assert isinstance(db, DatabaseNode)
        assert len(db.city_names) == 3
        assert all(isinstance(node, CityNameNode) for node in db.city_names)

    def test_civilization_builder_fluent_api(self):
        """Test fluent API chaining."""
        files = (CivilizationBuilder()
                .fill({
                    "civilization_type": "CIVILIZATION_ROME",
                    "civilization": {},
                })
                .build())
        
        assert len(files) == 6


class TestUnitBuilder:
    """Tests for UnitBuilder."""

    def test_unit_builder_basic(self):
        """Test basic unit builder setup."""
        builder = UnitBuilder()
        assert builder.unit_type is None
        assert builder.unit == {}
        assert builder.unit_stats == []
        assert builder.unit_costs == []

    def test_unit_builder_fill(self):
        """Test filling unit builder with data."""
        builder = UnitBuilder()
        builder.fill({
            "unit_type": "UNIT_SCOUT",
            "unit": {"combat": 10},
            "unit_stats": [{"strength": 5}],
        })
        
        assert builder.unit_type == "UNIT_SCOUT"
        assert builder.unit == {"combat": 10}
        assert builder.unit_stats == [{"strength": 5}]

    def test_unit_builder_build_empty(self):
        """Test building with no unit type returns empty files."""
        builder = UnitBuilder()
        files = builder.build()
        assert files == []

    def test_unit_builder_build_basic(self):
        """Test building a basic unit."""
        builder = UnitBuilder()
        builder.fill({
            "unit_type": "UNIT_SCOUT",
            "unit": {"combat": 10},
        })
        
        files = builder.build()
        
        assert len(files) == 3  # current.xml, icons.xml, localization.xml
        assert all(isinstance(f, XmlFile) for f in files)
        assert "scout" in files[0].path
        assert files[0].name in ["current.xml", "icons.xml", "localization.xml"]

    def test_unit_builder_with_stats_and_costs(self):
        """Test unit builder with stats and costs."""
        from civ7_modding_tools.nodes import DatabaseNode
        
        builder = UnitBuilder()
        builder.fill({
            "unit_type": "UNIT_WARRIOR",
            "unit": {"combat": 20},
            "unit_stats": [{"strength": 10}],
            "unit_costs": [{"production": 40}],
        })
        
        files = builder.build()
        unit_file = files[0]
        
        # Should have DatabaseNode with semantic tables
        assert isinstance(unit_file.content, DatabaseNode)
        db = unit_file.content
        assert len(db.units) == 1
        assert len(db.unit_stats) == 1
        assert len(db.unit_costs) == 1

    def test_unit_builder_fluent_api(self):
        """Test fluent API chaining."""
        files = (UnitBuilder()
                .fill({
                    "unit_type": "UNIT_SCOUT",
                    "unit": {},
                })
                .build())
        
        assert len(files) == 3


class TestConstructibleBuilder:
    """Tests for ConstructibleBuilder."""

    def test_constructible_builder_basic(self):
        """Test basic constructible builder setup."""
        builder = ConstructibleBuilder()
        assert builder.constructible_type is None
        assert builder.constructible == {}
        assert builder.yield_changes == []

    def test_constructible_builder_fill(self):
        """Test filling constructible builder with data."""
        builder = ConstructibleBuilder()
        builder.fill({
            "constructible_type": "BUILDING_TEMPLE",
            "constructible": {"cost": 100},
            "yield_changes": [{"yield": "science", "amount": 2}],
        })
        
        assert builder.constructible_type == "BUILDING_TEMPLE"
        assert builder.constructible == {"cost": 100}
        assert builder.yield_changes == [{"yield": "science", "amount": 2}]

    def test_constructible_builder_build_empty(self):
        """Test building with no constructible type returns empty files."""
        builder = ConstructibleBuilder()
        files = builder.build()
        assert files == []

    def test_constructible_builder_build_basic(self):
        """Test building a basic constructible."""
        builder = ConstructibleBuilder()
        builder.fill({
            "constructible_type": "BUILDING_TEMPLE",
            "constructible": {"cost": 100},
        })
        
        files = builder.build()
        
        assert len(files) == 3  # always.xml, icons.xml, localization.xml
        assert all(isinstance(f, XmlFile) for f in files)
        assert "temple" in files[0].path
        assert files[0].name in ["always.xml", "icons.xml", "localization.xml"]

    def test_constructible_builder_with_yield_changes(self):
        """Test constructible builder with yield changes."""
        from civ7_modding_tools.nodes import DatabaseNode
        
        builder = ConstructibleBuilder()
        builder.fill({
            "constructible_type": "BUILDING_LIBRARY",
            "constructible": {"cost": 80},
            "yield_changes": [
                {"yield": "science", "amount": 2},
                {"yield": "culture", "amount": 1},
            ],
        })
        
        files = builder.build()
        const_file = files[0]
        
        # Should have DatabaseNode with semantic tables
        assert isinstance(const_file.content, DatabaseNode)
        db = const_file.content
        assert len(db.constructibles) == 1
        assert len(db.constructible_yield_changes) == 2

    def test_constructible_builder_fluent_api(self):
        """Test fluent API chaining."""
        files = (ConstructibleBuilder()
                .fill({
                    "constructible_type": "BUILDING_TEMPLE",
                    "constructible": {},
                })
                .build())
        
        assert len(files) == 3


class TestBuilderFileGeneration:
    """Tests for file generation from builders."""

    def test_civilization_builder_generates_valid_xml(self):
        """Test that civilization builder generates valid XML files."""
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {"base_tourism": 10},
        })
        
        files = builder.build()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for file in files:
                file.write(tmpdir)
            
            # Check file was created
            civ_file = Path(tmpdir) / "civilizations" / "rome" / "current.xml"
            assert civ_file.exists()
            
            # Check it's valid XML
            content = civ_file.read_text()
            assert "<?xml" in content
            assert "<Database" in content
            assert "CivilizationType" in content

    def test_unit_builder_generates_valid_xml(self):
        """Test that unit builder generates valid XML files."""
        builder = UnitBuilder()
        builder.fill({
            "unit_type": "UNIT_SCOUT",
            "unit": {"combat": 10},
        })
        
        files = builder.build()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for file in files:
                file.write(tmpdir)
            
            unit_file = Path(tmpdir) / "units" / "scout" / "current.xml"
            assert unit_file.exists()
            
            content = unit_file.read_text()
            assert "<?xml" in content
            assert "Combat" in content

    def test_constructible_builder_generates_valid_xml(self):
        """Test that constructible builder generates valid XML files."""
        builder = ConstructibleBuilder()
        builder.fill({
            "constructible_type": "BUILDING_TEMPLE",
            "constructible": {"cost": 100},
        })
        
        files = builder.build()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for file in files:
                file.write(tmpdir)
            
            const_file = Path(tmpdir) / "constructibles" / "temple" / "always.xml"
            assert const_file.exists()
            
            content = const_file.read_text()
            assert "<?xml" in content
            assert "Cost" in content


class TestBuilderIntegration:
    """Integration tests for builders."""

    def test_multiple_builders_with_mod(self):
        """Test creating multiple builders and adding to a mod."""
        from civ7_modding_tools.core import Mod
        
        mod = Mod(
            mod_id="test-mod",
            version="1.0",
            name="Test Mod",
        )
        
        civ_builder = CivilizationBuilder().fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {},
        })
        
        unit_builder = UnitBuilder().fill({
            "unit_type": "UNIT_SCOUT",
            "unit": {},
        })
        
        mod.add(civ_builder)
        mod.add(unit_builder)
        
        assert len(mod.builders) == 2

    def test_builder_migrate_hook(self):
        """Test that migrate hook returns self for chaining."""
        builder = CivilizationBuilder()
        result = builder.migrate()
        assert result is builder

    def test_builder_with_dict_alias(self):
        """Test with_dict alias for fill."""
        builder = CivilizationBuilder()
        result = builder.with_dict({
            "civilization_type": "CIVILIZATION_ROME",
        })
        
        assert result is builder
        assert builder.civilization_type == "CIVILIZATION_ROME"
