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
        
        # Should have one civilization file
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert "civilization_rome" in files[0].path
        assert files[0].name == "current.xml"

    def test_civilization_builder_build_content(self):
        """Test that built civilization file contains correct nodes."""
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {"base_tourism": 10},
            "civilization_traits": ["TRAIT_ECONOMIC"],
        })
        
        files = builder.build()
        file = files[0]
        
        # Check content is a list of nodes
        assert isinstance(file.content, list)
        assert len(file.content) >= 2  # At least 1 civilization + 1 trait
        
        # First node should be CivilizationNode
        assert isinstance(file.content[0], CivilizationNode)
        assert file.content[0].civilization_type == "CIVILIZATION_ROME"
        
        # Second should be trait node
        assert isinstance(file.content[1], CivilizationTraitNode)

    def test_civilization_builder_with_city_names(self):
        """Test civilization builder with city names."""
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {},
            "city_names": ["Rome", "Milan", "Venice"],
        })
        
        files = builder.build()
        
        # Should have civilization file and city names file
        assert len(files) == 2
        assert files[0].name == "current.xml"
        assert files[1].name == "city_names.xml"
        
        # City names file should have city nodes
        city_file = files[1]
        assert len(city_file.content) == 3
        assert all(isinstance(node, CityNameNode) for node in city_file.content)

    def test_civilization_builder_fluent_api(self):
        """Test fluent API chaining."""
        files = (CivilizationBuilder()
                .fill({
                    "civilization_type": "CIVILIZATION_ROME",
                    "civilization": {},
                })
                .build())
        
        assert len(files) == 1


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
        
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert "unit_scout" in files[0].path
        assert files[0].name == "unit.xml"

    def test_unit_builder_with_stats_and_costs(self):
        """Test unit builder with stats and costs."""
        builder = UnitBuilder()
        builder.fill({
            "unit_type": "UNIT_WARRIOR",
            "unit": {"combat": 20},
            "unit_stats": [{"strength": 10}],
            "unit_costs": [{"production": 40}],
        })
        
        files = builder.build()
        unit_file = files[0]
        
        # Should have 1 unit + 1 stat + 1 cost = 3 nodes
        assert len(unit_file.content) == 3
        assert isinstance(unit_file.content[0], UnitNode)

    def test_unit_builder_fluent_api(self):
        """Test fluent API chaining."""
        files = (UnitBuilder()
                .fill({
                    "unit_type": "UNIT_SCOUT",
                    "unit": {},
                })
                .build())
        
        assert len(files) == 1


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
        
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert "building_temple" in files[0].path
        assert files[0].name == "constructible.xml"

    def test_constructible_builder_with_yield_changes(self):
        """Test constructible builder with yield changes."""
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
        
        # Should have 1 constructible + 2 yield changes = 3 nodes
        assert len(const_file.content) == 3

    def test_constructible_builder_fluent_api(self):
        """Test fluent API chaining."""
        files = (ConstructibleBuilder()
                .fill({
                    "constructible_type": "BUILDING_TEMPLE",
                    "constructible": {},
                })
                .build())
        
        assert len(files) == 1


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
            civ_file = Path(tmpdir) / "civilizations" / "civilization_rome" / "current.xml"
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
            
            unit_file = Path(tmpdir) / "units" / "unit_scout" / "unit.xml"
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
            
            const_file = Path(tmpdir) / "constructibles" / "building_temple" / "constructible.xml"
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
