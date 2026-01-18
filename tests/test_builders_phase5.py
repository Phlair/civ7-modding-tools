"""Tests for Phase 5 Remaining Builders.

Covers the 9 remaining builder implementations required for full mod generation:
- ProgressionTreeBuilder
- ModifierBuilder
- TraditionBuilder
- UniqueQuarterBuilder
- LeaderUnlockBuilder
- CivilizationUnlockBuilder
- ProgressionTreeNodeBuilder
- UnlockBuilder
- ImportFileBuilder

These builders complete the builder pattern implementation for all core mod entities.
"""

import pytest
from pathlib import Path
from typing import Any

from civ7_modding_tools.builders import (
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
from civ7_modding_tools.files import XmlFile, ImportFile
from civ7_modding_tools.localizations import (
    ProgressionTreeLocalization,
    ModifierLocalization,
    TraditionLocalization,
    UniqueQuarterLocalization,
    LeaderUnlockLocalization,
    ProgressionTreeNodeLocalization,
)
from civ7_modding_tools.nodes import BaseNode


class TestProgressionTreeBuilder:
    """Tests for ProgressionTreeBuilder."""

    def test_progression_tree_builder_initialization(self):
        """Test ProgressionTreeBuilder initializes with correct defaults."""
        builder = ProgressionTreeBuilder()
        assert builder.progression_tree_type is None
        assert builder.progression_tree == {}
        assert builder.progression_tree_nodes == []
        assert builder.localizations == []

    def test_progression_tree_builder_fill(self):
        """Test ProgressionTreeBuilder.fill() populates properties."""
        builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
            'progression_tree_nodes': [
                {'Type': 'NODE_1', 'NodeType': 'CIVIC'},
                {'Type': 'NODE_2', 'NodeType': 'CIVIC'},
            ]
        })
        assert builder.progression_tree_type == 'CIVICS_GONDOR'
        assert builder.progression_tree['CivicTreeType'] == 'CIVICS_GONDOR'
        assert len(builder.progression_tree_nodes) == 2

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
            'progression_tree_nodes': [
                {'Type': 'NODE_1', 'NodeType': 'CIVIC'},
            ]
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/progression-trees/civics_gondor/' in files[0].path
        assert files[0].name == 'tree.xml'

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


class TestModifierBuilder:
    """Tests for ModifierBuilder."""

    def test_modifier_builder_initialization(self):
        """Test ModifierBuilder initializes with correct defaults."""
        builder = ModifierBuilder()
        assert builder.modifier_type is None
        assert builder.modifier == {}
        assert builder.game_modifiers == []
        assert builder.requirements == []
        assert builder.arguments == []
        assert builder.localizations == []

    def test_modifier_builder_fill(self):
        """Test ModifierBuilder.fill() populates properties."""
        builder = ModifierBuilder().fill({
            'modifier_type': 'MOD_GONDOR_BONUS',
            'modifier': {'ModifierType': 'MOD_GONDOR_BONUS'},
            'game_modifiers': [{'ModifierType': 'MOD_GONDOR_BONUS'}],
            'requirements': [{'Type': 'REQ_TECH_MATCHED'}],
            'arguments': [{'Name': 'Amount', 'Value': '5'}],
        })
        assert builder.modifier_type == 'MOD_GONDOR_BONUS'
        assert len(builder.game_modifiers) == 1
        assert len(builder.requirements) == 1
        assert len(builder.arguments) == 1

    def test_modifier_builder_build_empty(self):
        """Test ModifierBuilder.build() with no modifier_type returns empty."""
        builder = ModifierBuilder()
        files = builder.build()
        assert files == []

    def test_modifier_builder_build_with_data(self):
        """Test ModifierBuilder.build() generates correct XmlFile."""
        builder = ModifierBuilder().fill({
            'modifier_type': 'MOD_GONDOR_BONUS',
            'modifier': {'ModifierType': 'MOD_GONDOR_BONUS'},
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/modifiers/mod_gondor_bonus/' in files[0].path

    def test_modifier_builder_detached_modifier(self):
        """Test ModifierBuilder handles detached modifiers."""
        builder = ModifierBuilder().fill({
            'modifier_type': 'MOD_GONDOR_GLOBAL',
            'modifier': {'ModifierType': 'MOD_GONDOR_GLOBAL'},
            'is_detached': True,
        })
        files = builder.build()
        assert len(files) == 1
        # Detached modifiers use different path
        assert '/modifiers/' in files[0].path


class TestTraditionBuilder:
    """Tests for TraditionBuilder."""

    def test_tradition_builder_initialization(self):
        """Test TraditionBuilder initializes with correct defaults."""
        builder = TraditionBuilder()
        assert builder.tradition_type is None
        assert builder.tradition == {}
        assert builder.tradition_modifiers == []
        assert builder.localizations == []

    def test_tradition_builder_fill(self):
        """Test TraditionBuilder.fill() populates properties."""
        builder = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_GONDOR',
            'tradition': {'TraditionType': 'TRADITION_GONDOR'},
            'tradition_modifiers': [{'ModifierType': 'MOD_GONDOR_TRADITION'}],
        })
        assert builder.tradition_type == 'TRADITION_GONDOR'
        assert len(builder.tradition_modifiers) == 1

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
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/traditions/tradition_gondor/' in files[0].path
        assert files[0].name == 'tradition.xml'

    def test_tradition_builder_with_localizations(self):
        """Test TraditionBuilder supports localizations."""
        localization = TraditionLocalization()
        localization.name = 'Gondor Tradition'
        builder = TraditionBuilder().fill({
            'tradition_type': 'TRADITION_GONDOR',
            'localizations': [localization]
        })
        assert len(builder.localizations) == 1


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
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/unique-quarters/quarter_gondor_unique/' in files[0].path


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


class TestProgressionTreeNodeBuilder:
    """Tests for ProgressionTreeNodeBuilder."""

    def test_progression_tree_node_builder_initialization(self):
        """Test ProgressionTreeNodeBuilder initializes with correct defaults."""
        builder = ProgressionTreeNodeBuilder()
        assert builder.progression_tree_node_type is None
        assert builder.progression_tree_node == {}
        assert builder.progression_tree_node_unlocks == []
        assert builder.localizations == []

    def test_progression_tree_node_builder_fill(self):
        """Test ProgressionTreeNodeBuilder.fill() populates properties."""
        builder = ProgressionTreeNodeBuilder().fill({
            'progression_tree_node_type': 'NODE_GONDOR_UNIQUE',
            'progression_tree_node': {'NodeType': 'NODE_GONDOR_UNIQUE'},
            'progression_tree_node_unlocks': [{'UnlockType': 'UNIT_GONDOR'}],
        })
        assert builder.progression_tree_node_type == 'NODE_GONDOR_UNIQUE'
        assert len(builder.progression_tree_node_unlocks) == 1

    def test_progression_tree_node_builder_build_with_data(self):
        """Test ProgressionTreeNodeBuilder.build() generates correct XmlFile."""
        builder = ProgressionTreeNodeBuilder().fill({
            'progression_tree_node_type': 'NODE_GONDOR_UNIQUE',
            'progression_tree_node': {'NodeType': 'NODE_GONDOR_UNIQUE'},
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)
        assert '/progression-tree-nodes/node_gondor_unique/' in files[0].path


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


class TestPhase5BuildersIntegration:
    """Integration tests for Phase 5 builders working together."""

    def test_multiple_builders_create_different_files(self):
        """Test multiple Phase 5 builders generate separate files."""
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
        
        assert len(progression_files) == 1
        assert len(modifier_files) == 1
        assert progression_files[0].path != modifier_files[0].path

    def test_builders_follow_consistent_pattern(self):
        """Test all Phase 5 builders follow consistent builder pattern."""
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


class TestPhase5BuildersEdgeCases:
    """Edge case tests for Phase 5 builders."""

    def test_empty_detail_lists_handled_gracefully(self):
        """Test builders with empty detail lists generate valid output."""
        builder = ProgressionTreeBuilder().fill({
            'progression_tree_type': 'CIVICS_GONDOR',
            'progression_tree': {'CivicTreeType': 'CIVICS_GONDOR'},
            'progression_tree_nodes': [],
        })
        files = builder.build()
        assert len(files) == 1
        assert isinstance(files[0], XmlFile)

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
        assert len(files) == 1

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
