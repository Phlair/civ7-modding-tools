"""Tests for all builder implementations."""

import pytest
import tempfile
from pathlib import Path
from typing import Any

from civ7_modding_tools.builders import (
    BaseBuilder,
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
    ProgressionTreeBuilder,
    ModifierBuilder,
    TraditionBuilder,
    UniqueQuarterBuilder,
    LeaderUnlockBuilder,
    CivilizationUnlockBuilder,
    ProgressionTreeNodeBuilder,
    UnlockBuilder,
    ImportFileBuilder,
)
from civ7_modding_tools.core import ActionGroupBundle
from civ7_modding_tools.files import XmlFile, ImportFile
from civ7_modding_tools.nodes import (
    CivilizationNode,
    CivilizationTraitNode,
    UnitNode,
    CityNameNode,
    DatabaseNode,
    BaseNode,
)
from civ7_modding_tools.localizations import (
    ProgressionTreeLocalization,
    ModifierLocalization,
    TraditionLocalization,
    UniqueQuarterLocalization,
    LeaderUnlockLocalization,
    ProgressionTreeNodeLocalization,
)


# ============================================================================
# BaseBuilder Tests
# ============================================================================

def test_base_builder_fill():
    """Test fill() method on builder."""
    class DummyBuilder(BaseBuilder):
        def build(self): return []
    
    builder = DummyBuilder()
    result = builder.fill({"test_prop": "value"})
    
    # Should return self for chaining
    assert result is builder
    # Verify property was set via setattr
    assert hasattr(builder, "test_prop")
    assert builder.test_prop == "value"


def test_base_builder_action_group_bundle():
    """Test action group bundle initialization."""
    builder = CivilizationBuilder()
    assert builder.action_group_bundle is not None
    assert isinstance(builder.action_group_bundle, ActionGroupBundle)
    assert builder.action_group_bundle.action_group_id == "ALWAYS"


def test_base_builder_migrate():
    """Test migrate() hook."""
    builder = CivilizationBuilder()
    result = builder.migrate()
    
    # Should return self
    assert result is builder


def test_base_builder_build_returns_list():
    """Test that build() returns a list."""
    builder = CivilizationBuilder()
    files = builder.build()
    
    assert isinstance(files, list)


# ============================================================================
# CivilizationBuilder Tests
# ============================================================================

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
        
        # Should have 5 civilization files (current, legacy, shell, icons, localization)
        # game-effects.xml only generated when there are trait modifiers
        assert len(files) == 5
        assert all(isinstance(f, XmlFile) for f in files)
        assert "rome" in files[0].path  # Path is kebab-case of trimmed type
        assert files[0].name in ["current.xml", "legacy.xml", "shell.xml", "icons.xml", "localization.xml"]

    def test_civilization_builder_build_content(self):
        """Test that built civilization file contains correct nodes."""
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
        builder = CivilizationBuilder()
        builder.fill({
            "civilization_type": "CIVILIZATION_ROME",
            "civilization": {},
            "localizations": [{"city_names": ["Rome", "Milan", "Venice"]}],
        })
        
        files = builder.build()
        
        # Should have 5 civilization files
        assert len(files) == 5
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
        
        assert len(files) == 5


# ============================================================================
# UnitBuilder Tests
# ============================================================================

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


# ============================================================================
# ConstructibleBuilder Tests
# ============================================================================

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


# ============================================================================
# ProgressionTreeBuilder Tests
# ============================================================================

class TestProgressionTreeBuilder:
    """Tests for ProgressionTreeBuilder."""

    def test_progression_tree_builder_initialization(self):
        """Test ProgressionTreeBuilder initializes with correct defaults."""
        builder = ProgressionTreeBuilder()
        assert builder.progression_tree_type is None
        assert builder.progression_tree == {}
        assert builder.localizations == []

    def test_progression_tree_builder_fill(self):
        """Test ProgressionTreeBuilder.fill() populates properties."""
        builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
        })
        assert builder.progression_tree_type == 'CIVICS_GONDOR'
        assert builder.progression_tree['CivicTreeType'] == 'CIVICS_GONDOR'

    def test_progression_tree_builder_build_empty(self):
        """Test ProgressionTreeBuilder.build() with no progression_tree_type returns empty."""
        builder = ProgressionTreeBuilder()
        files = builder.build()
        assert files == []

    def test_progression_tree_builder_build_with_data(self):
        """Test ProgressionTreeBuilder.build() generates correct XmlFile."""
        builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
        })
        files = builder.build()
        assert len(files) == 2  # current.xml + localization.xml
        assert isinstance(files[0], XmlFile)
        assert '/progression-trees/civics-gondor/' in files[0].path
        assert files[0].name == 'current.xml'

    def test_progression_tree_builder_with_localizations(self):
        """Test ProgressionTreeBuilder supports localizations."""
        localization = ProgressionTreeLocalization()
        localization.name = 'Gondor Civics'
        builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'localizations': [localization]
        })
        assert len(builder.localizations) == 1
        assert builder.localizations[0].name == 'Gondor Civics'


# ============================================================================
# ModifierBuilder Tests
# ============================================================================

class TestModifierBuilder:
    """Tests for ModifierBuilder."""

    def test_modifier_builder_initialization(self):
        """Test ModifierBuilder initializes with correct defaults."""
        builder = ModifierBuilder()
        assert builder.modifier == {}
        assert builder.localizations == []
        assert builder.is_detached == False

    def test_modifier_builder_fill(self):
        """Test ModifierBuilder.fill() populates properties."""
        builder = ModifierBuilder().fill({
            'modifier': {'ModifierType': 'MOD_GONDOR_BONUS', 'Id': 'MOD_GONDOR_BONUS'},
            'is_detached': False,
        })
        assert builder.modifier['ModifierType'] == 'MOD_GONDOR_BONUS'
        assert builder.is_detached == False

    def test_modifier_builder_build_empty(self):
        """Test ModifierBuilder.build() with no modifier_type returns empty."""
        builder = ModifierBuilder()
        files = builder.build()
        assert files == []

    def test_modifier_builder_build_with_data(self):
        """Test ModifierBuilder.build() returns empty (modifiers are bound to other builders)."""
        builder = ModifierBuilder().fill({
            'modifier': {'ModifierType': 'MOD_GONDOR_BONUS'},
        })
        files = builder.build()
        assert files == []

    def test_modifier_builder_detached_modifier(self):
        """Test ModifierBuilder handles detached modifiers."""
        builder = ModifierBuilder().fill({
            'modifier': {'ModifierType': 'MOD_GONDOR_GLOBAL'},
            'is_detached': True,
        })
        files = builder.build()
        assert files == []


# ============================================================================
# TraditionBuilder Tests
# ============================================================================

class TestTraditionBuilder:
    """Tests for TraditionBuilder."""

    def test_tradition_builder_initialization(self):
        """Test TraditionBuilder initializes with correct defaults."""
        builder = TraditionBuilder()
        assert builder.tradition_type is None
        assert builder.tradition == {}
        assert builder.localizations == []

    def test_tradition_builder_fill(self):
        """Test TraditionBuilder.fill() populates properties."""
        builder = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_GONDOR',
            'tradition': {'TraditionType': 'TRADITION_GONDOR'},
        })
        assert builder.tradition_type == 'TRADITION_GONDOR'

    def test_tradition_builder_build_empty(self):
        """Test TraditionBuilder.build() with no tradition_type returns empty."""
        builder = TraditionBuilder()
        files = builder.build()
        assert files == []

    def test_tradition_builder_build_with_data(self):
        """Test TraditionBuilder.build() generates correct XmlFile."""
        builder = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_GONDOR',
            'tradition': {'TraditionType': 'TRADITION_GONDOR'},
        })
        files = builder.build()
        assert len(files) == 2  # current.xml + localization.xml
        assert isinstance(files[0], XmlFile)
        assert '/traditions/gondor/' in files[0].path
        assert files[0].name == 'current.xml'

    def test_tradition_builder_with_localizations(self):
        """Test TraditionBuilder supports localizations."""
        localization = TraditionLocalization()
        localization.name = 'Gondor Tradition'
        builder = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_GONDOR',
            'localizations': [localization]
        })
        assert len(builder.localizations) == 1


# ============================================================================
# UniqueQuarterBuilder Tests
# ============================================================================

class TestUniqueQuarterBuilder:
    """Tests for UniqueQuarterBuilder."""

    def test_unique_quarter_builder_initialization(self):
        """Test UniqueQuarterBuilder initializes with correct defaults."""
        builder = UniqueQuarterBuilder()
        assert builder.unique_quarter_type is None
        assert builder.unique_quarter == {}
        assert builder.unique_quarter_modifiers == []
        assert builder.localizations == []

    def test_unique_quarter_builder_fill(self):
        """Test UniqueQuarterBuilder.fill() populates properties."""
        builder = UniqueQuarterBuilder().fill({
            'unique_quarter_type': 'QUARTER_GONDOR_UNIQUE',
            'unique_quarter': {'UniqueQuarterType': 'QUARTER_GONDOR_UNIQUE'},
            'unique_quarter_modifiers': [{'ModifierType': 'MOD_GONDOR_QUARTER'}],
        })
        assert builder.unique_quarter_type == 'QUARTER_GONDOR_UNIQUE'
        assert len(builder.unique_quarter_modifiers) == 1

    def test_unique_quarter_builder_build_with_data(self):
        """Test UniqueQuarterBuilder.build() generates correct XmlFile."""
        builder = UniqueQuarterBuilder().fill({
            'unique_quarter_type': 'QUARTER_GONDOR_UNIQUE',
            'unique_quarter': {'UniqueQuarterType': 'QUARTER_GONDOR_UNIQUE'},
        })
        files = builder.build()
        assert len(files) == 3
        
        # Verify all files are XmlFile instances
        assert all(isinstance(f, XmlFile) for f in files)
        
        # Verify paths are correct - unique quarters are under /constructibles/
        assert all('/constructibles/quarter-gondor-unique/' in f.path for f in files)
        
        # Check specific filenames are present
        filenames = sorted([f.name for f in files])
        assert filenames == ['always.xml', 'icons.xml', 'localization.xml']


# ============================================================================
# LeaderUnlockBuilder Tests
# ============================================================================

class TestLeaderUnlockBuilder:
    """Tests for LeaderUnlockBuilder."""

    def test_leader_unlock_builder_initialization(self):
        """Test LeaderUnlockBuilder initializes with correct defaults."""
        builder = LeaderUnlockBuilder()
        assert builder.leader_unlock_type is None
        assert builder.leader_unlock == {}
        assert builder.leader_civilization_biases == []
        assert builder.localizations == []

    def test_leader_unlock_builder_fill(self):
        """Test LeaderUnlockBuilder.fill() populates properties."""
        builder = LeaderUnlockBuilder().fill({
            'leader_unlock_type': 'LEADER_ARAGORN',
            'leader_unlock': {'LeaderType': 'LEADER_ARAGORN'},
            'leader_civilization_biases': [{'CivilizationType': 'CIVILIZATION_GONDOR', 'Bias': 100}],
        })
        assert builder.leader_unlock_type == 'LEADER_ARAGORN'
        assert len(builder.leader_civilization_biases) == 1

    def test_leader_unlock_builder_build_with_data(self):
        """Test LeaderUnlockBuilder.build() generates correct XmlFile."""
        builder = LeaderUnlockBuilder().fill({
            'leader_unlock_type': 'LEADER_ARAGORN',
            'leader_unlock': {'LeaderType': 'LEADER_ARAGORN'},
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/leaders/leader_aragorn/' in files[0].path


# ============================================================================
# CivilizationUnlockBuilder Tests
# ============================================================================

class TestCivilizationUnlockBuilder:
    """Tests for CivilizationUnlockBuilder."""

    def test_civilization_unlock_builder_initialization(self):
        """Test CivilizationUnlockBuilder initializes with correct defaults."""
        builder = CivilizationUnlockBuilder()
        assert builder.civilization_unlock_type is None
        assert builder.civilization_unlock == {}
        assert builder.localizations == []

    def test_civilization_unlock_builder_fill(self):
        """Test CivilizationUnlockBuilder.fill() populates properties."""
        builder = CivilizationUnlockBuilder().fill({
            'civilization_unlock_type': 'CIVILIZATION_GONDOR_UNLOCK',
            'civilization_unlock': {'CivilizationType': 'CIVILIZATION_GONDOR', 'Age': 'AGE_CLASSICAL'},
        })
        assert builder.civilization_unlock_type == 'CIVILIZATION_GONDOR_UNLOCK'
        assert builder.civilization_unlock['CivilizationType'] == 'CIVILIZATION_GONDOR'

    def test_civilization_unlock_builder_build_with_data(self):
        """Test CivilizationUnlockBuilder.build() generates correct XmlFile."""
        builder = CivilizationUnlockBuilder().fill({
            'civilization_unlock_type': 'CIVILIZATION_GONDOR_UNLOCK',
            'civilization_unlock': {'CivilizationType': 'CIVILIZATION_GONDOR'},
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/civilization-unlocks/civilization_gondor_unlock/' in files[0].path


# ============================================================================
# ProgressionTreeNodeBuilder Tests
# ============================================================================

class TestProgressionTreeNodeBuilder:
    """Tests for ProgressionTreeNodeBuilder."""

    def test_progression_tree_node_builder_initialization(self):
        """Test ProgressionTreeNodeBuilder initializes with correct defaults."""
        builder = ProgressionTreeNodeBuilder()
        assert builder.progression_tree_node_type is None
        assert builder.progression_tree_node == {}
        assert builder.progression_tree_advisories == []
        assert builder.localizations == []

    def test_progression_tree_node_builder_fill(self):
        """Test ProgressionTreeNodeBuilder.fill() populates properties."""
        builder = ProgressionTreeNodeBuilder().fill({
            'progression_tree_node_type': 'NODE_GONDOR_UNIQUE',
            'progression_tree_node': {'NodeType': 'NODE_GONDOR_UNIQUE'},
            'progression_tree_advisories': ['ADVISORY_MILITARY'],
        })
        assert builder.progression_tree_node_type == 'NODE_GONDOR_UNIQUE'
        assert len(builder.progression_tree_advisories) == 1

    def test_progression_tree_node_builder_build_with_data(self):
        """Test ProgressionTreeNodeBuilder.build() returns empty list."""
        builder = ProgressionTreeNodeBuilder().fill({
            'progression_tree_node_type': 'NODE_GONDOR_UNIQUE',
            'progression_tree_node': {'NodeType': 'NODE_GONDOR_UNIQUE'},
        })
        files = builder.build()
        # ProgressionTreeNodeBuilder doesn't generate files directly
        # It's bound to ProgressionTreeBuilder which generates output
        assert len(files) == 0
        assert files == []


# ============================================================================
# UnlockBuilder Tests
# ============================================================================

class TestUnlockBuilder:
    """Tests for UnlockBuilder."""

    def test_unlock_builder_initialization(self):
        """Test UnlockBuilder initializes with correct defaults."""
        builder = UnlockBuilder()
        assert builder.unlock_type is None
        assert builder.unlock == {}
        assert builder.unlock_rewards == []
        assert builder.unlock_requirements == []
        assert builder.unlock_configs == []
        assert builder.localizations == []

    def test_unlock_builder_fill(self):
        """Test UnlockBuilder.fill() populates properties."""
        builder = UnlockBuilder().fill({
            'unlock_type': 'UNLOCK_GONDOR_UNIT',
            'unlock': {'UnlockType': 'UNLOCK_GONDOR_UNIT'},
            'unlock_rewards': [{'UnlockRewardType': 'REWARD_UNIT'}],
            'unlock_requirements': [{'RequirementType': 'TECH_MATCHED'}],
            'unlock_configs': [{'ConfigKey': 'Value'}],
        })
        assert builder.unlock_type == 'UNLOCK_GONDOR_UNIT'
        assert len(builder.unlock_rewards) == 1
        assert len(builder.unlock_requirements) == 1
        assert len(builder.unlock_configs) == 1

    def test_unlock_builder_build_empty(self):
        """Test UnlockBuilder.build() with no unlock_type returns empty."""
        builder = UnlockBuilder()
        files = builder.build()
        assert files == []

    def test_unlock_builder_build_with_data(self):
        """Test UnlockBuilder.build() generates correct XmlFile."""
        builder = UnlockBuilder().fill({
            'unlock_type': 'UNLOCK_GONDOR_UNIT',
            'unlock': {'UnlockType': 'UNLOCK_GONDOR_UNIT'},
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/unlocks/unlock_gondor_unit/' in files[0].path
        assert files[0].name == 'unlock.xml'

    def test_unlock_builder_complex_with_all_detail_types(self):
        """Test UnlockBuilder with all detail node types."""
        builder = UnlockBuilder().fill({
            'unlock_type': 'UNLOCK_GONDOR_COMPLEX',
            'unlock': {'UnlockType': 'UNLOCK_GONDOR_COMPLEX'},
            'unlock_rewards': [{'RewardType': 'GOLD'}],
            'unlock_requirements': [{'RequirementType': 'TECH'}],
            'unlock_configs': [{'ConfigType': 'CONFIG1'}, {'ConfigType': 'CONFIG2'}],
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)


# ============================================================================
# ImportFileBuilder Tests
# ============================================================================

class TestImportFileBuilder:
    """Tests for ImportFileBuilder."""

    def test_import_file_builder_initialization(self):
        """Test ImportFileBuilder initializes with correct defaults."""
        builder = ImportFileBuilder()
        assert builder.source_path is None
        assert builder.target_name is None
        assert builder.target_directory == "/imports/"

    def test_import_file_builder_fill(self):
        """Test ImportFileBuilder.fill() populates properties."""
        builder = ImportFileBuilder().fill({
            'source_path': './assets/example.sql',
            'target_name': 'database.sql',
            'target_directory': '/imports/sql/',
        })
        assert builder.source_path == './assets/example.sql'
        assert builder.target_name == 'database.sql'
        assert builder.target_directory == '/imports/sql/'

    def test_import_file_builder_build_empty(self):
        """Test ImportFileBuilder.build() with no source_path returns empty."""
        builder = ImportFileBuilder()
        files = builder.build()
        assert files == []

    def test_import_file_builder_build_with_data(self):
        """Test ImportFileBuilder.build() generates correct ImportFile."""
        # Use a real test file
        test_file = Path(__file__).parent / 'fixtures' / 'test_import.txt'
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_text('test content')
        
        try:
            builder = ImportFileBuilder().fill({
                'source_path': str(test_file),
                'target_name': 'test_import.txt',
            })
            files = builder.build()
            assert len(files) == 1
            assert isinstance(files[0], ImportFile)
            assert '/imports/' in files[0].path
            assert files[0].name == 'test_import.txt'
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_import_file_builder_custom_directory(self):
        """Test ImportFileBuilder with custom target directory."""
        test_file = Path(__file__).parent / 'fixtures' / 'test_image.png'
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_bytes(b'fake image data')
        
        try:
            builder = ImportFileBuilder().fill({
                'source_path': str(test_file),
                'target_name': 'test_image.png',
                'target_directory': '/imports/images/',
            })
            files = builder.build()
            assert len(files) == 1
            assert files[0].path == '/imports/images/'
        finally:
            if test_file.exists():
                test_file.unlink()


# ============================================================================
# Builder File Generation Tests
# ============================================================================

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


# ============================================================================
# Builder Integration Tests
# ============================================================================

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

    def test_multiple_builders_create_different_files(self):
        """Test multiple builders generate separate files."""
        progression_builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
        })
        
        modifier_builder = ModifierBuilder().fill({
            'modifier_type': 'MOD_GONDOR_BONUS',
            'modifier': {'ModifierType': 'MOD_GONDOR_BONUS'},
        })
        
        progression_files = progression_builder.build()
        modifier_files = modifier_builder.build()
        
        assert len(progression_files) == 2
        assert len(modifier_files) == 0
        assert progression_files[0].path == progression_files[1].path  # Same path, different files

    def test_builders_follow_consistent_pattern(self):
        """Test all builders follow consistent builder pattern."""
        builders = [
            ProgressionTreeBuilder(),
            ModifierBuilder(),
            TraditionBuilder(),
            UniqueQuarterBuilder(),
            LeaderUnlockBuilder(),
            CivilizationUnlockBuilder(),
            ProgressionTreeNodeBuilder(),
            UnlockBuilder(),
            ImportFileBuilder(),
        ]
        
        for builder in builders:
            # All should have fill() method
            assert hasattr(builder, 'fill')
            assert callable(builder.fill)
            
            # All should have build() method
            assert hasattr(builder, 'build')
            assert callable(builder.build)
            
            # All should return list from build()
            result = builder.build()
            assert isinstance(result, list)

    def test_builder_localization_support(self):
        """Test builders that support localizations work correctly."""
        progression_builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
            'localizations': [
                ProgressionTreeLocalization(name='Gondor Civics')
            ]
        })
        
        assert len(progression_builder.localizations) == 1
        assert progression_builder.localizations[0].name == 'Gondor Civics'


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestBuilderEdgeCases:
    """Edge case tests for builders."""

    def test_empty_detail_lists_handled_gracefully(self):
        """Test builders with empty detail lists generate valid output."""
        builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
            'progression_tree_nodes': [],
        })
        files = builder.build()
        assert len(files) == 2
        assert isinstance(files[0], XmlFile)
        assert isinstance(files[1], XmlFile)

    def test_modifier_with_multiple_requirements(self):
        """Test ModifierBuilder handles multiple requirements."""
        builder = ModifierBuilder().fill({
            'modifier_type': 'MOD_COMPLEX',
            'modifier': {'ModifierType': 'MOD_COMPLEX'},
            'requirements': [
                {'RequirementType': 'TECH_MATCHED'},
                {'RequirementType': 'PLAYER_STATE'},
                {'RequirementType': 'UNIT_TAG_MATCHES'},
            ]
        })
        files = builder.build()
        assert len(files) == 0

    def test_unlock_builder_with_all_optional_fields(self):
        """Test UnlockBuilder with all optional fields populated."""
        builder = UnlockBuilder().fill({
            'unlock_type': 'UNLOCK_FULL',
            'unlock': {
                'UnlockType': 'UNLOCK_FULL',
                'Description': 'Full unlock',
            },
            'unlock_rewards': [
                {'RewardType': 'GOLD', 'Amount': '100'},
                {'RewardType': 'SCIENCE', 'Amount': '50'},
            ],
            'unlock_requirements': [
                {'RequirementType': 'TECH'},
                {'RequirementType': 'ERA'},
            ],
            'unlock_configs': [
                {'Key': 'Value1'},
                {'Key': 'Value2'},
                {'Key': 'Value3'},
            ]
        })
        files = builder.build()
        assert len(files) == 1
        xml_file: XmlFile = files[0]
        # Ensure content has multiple rows
        assert isinstance(xml_file.content, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
