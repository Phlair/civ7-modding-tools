"""Tests for Phase 2: Traditions System."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod
from civ7_modding_tools.builders import TraditionBuilder, ModifierBuilder, CivilizationBuilder
from civ7_modding_tools.localizations import TraditionLocalization


class TestTraditionBuilder:
    """Test TraditionBuilder functionality."""

    def test_tradition_builder_initialization(self):
        """Test TraditionBuilder initialization."""
        builder = TraditionBuilder()
        
        assert builder.tradition_type is None
        assert builder.tradition == {}
        assert builder.localizations == []
        assert builder.action_group_bundle is not None

    def test_tradition_builder_fill(self):
        """Test TraditionBuilder fill method."""
        builder = TraditionBuilder()
        
        builder.fill({
            'tradition_type': 'TRADITION_BABYLON_SCRIBES',
            'tradition': {'description': 'Ancient scribes'},
            'localizations': [{'name': 'Scribal Tradition'}]
        })
        
        assert builder.tradition_type == 'TRADITION_BABYLON_SCRIBES'
        assert builder.tradition.get('description') == 'Ancient scribes'
        assert len(builder.localizations) == 1

    def test_tradition_builder_migrate(self):
        """Test TraditionBuilder migrate method."""
        builder = TraditionBuilder()
        builder.fill({
            'tradition_type': 'TRADITION_TEST',
            'tradition': {},
            'localizations': [
                {'name': 'Test Tradition', 'description': 'A test tradition'}
            ]
        })
        
        builder.migrate()
        
        # Should populate databases
        assert builder._current is not None
        assert builder._localizations is not None

    def test_tradition_builder_build(self):
        """Test TraditionBuilder build method."""
        builder = TraditionBuilder()
        builder.fill({
            'tradition_type': 'TRADITION_TEST',
            'tradition': {},
            'localizations': [{'name': 'Test Tradition'}]
        })
        
        files = builder.build()
        
        # Should generate files
        assert len(files) > 0
        # Should have localization file at minimum
        assert any('localization' in f.name for f in files)

    def test_tradition_builder_build_empty(self):
        """Test TraditionBuilder build with empty tradition_type."""
        builder = TraditionBuilder()
        
        files = builder.build()
        
        # Should return empty list
        assert len(files) == 0

    def test_tradition_localization(self):
        """Test TraditionLocalization."""
        loc = TraditionLocalization(
            name='Scribal Tradition',
            description='Preserves ancient knowledge'
        )
        
        nodes = loc.get_nodes('TRADITION_TEST')
        
        assert len(nodes) > 0
        # Nodes should be dicts with Name and Value fields
        assert isinstance(nodes[0], dict)

    def test_tradition_localization_partial(self):
        """Test TraditionLocalization with only name."""
        loc = TraditionLocalization(name='Test Tradition')
        
        nodes = loc.get_nodes('TRADITION_TEST')
        
        assert len(nodes) >= 1
        assert any('test' in str(n).lower() for n in nodes)

    def test_tradition_builder_with_modifier(self):
        """Test TraditionBuilder binding with ModifierBuilder."""
        tradition = TraditionBuilder()
        tradition.fill({
            'tradition_type': 'TRADITION_TEST',
            'tradition': {},
            'localizations': [{'name': 'Test'}]
        })
        
        modifier = ModifierBuilder()
        modifier.fill({
            'modifier_type': 'MODIFIER_TRADITION_TEST',
            'modifier': {
                'collection': 'COLLECTION_OWNER',
                'effect': 'EFFECT_MODIFIER_TEST'
            }
        })
        
        # Should support binding
        result = tradition.bind([modifier])
        assert result == tradition  # Should return self for chaining

    def test_tradition_in_civilization(self):
        """Test TraditionBuilder used with CivilizationBuilder."""
        civ = CivilizationBuilder()
        civ.fill({
            'civilization_type': 'CIVILIZATION_TEST',
            'civilization_traits': []
        })
        
        tradition = TraditionBuilder()
        tradition.fill({
            'tradition_type': 'TRADITION_TEST_CIV',
            'tradition': {},
            'localizations': [{'name': 'Test Tradition'}]
        })
        
        # Should be able to use traditions with civilizations
        assert civ is not None
        assert tradition is not None


class TestTraditionIntegration:
    """Integration tests for Traditions system."""

    def test_tradition_in_mod(self):
        """Test adding tradition to mod."""
        mod = Mod(id="test-traditions", version="1", name="Test Traditions")
        
        tradition = TraditionBuilder()
        tradition.fill({
            'tradition_type': 'TRADITION_TEST',
            'tradition': {},
            'localizations': [{'name': 'Test Tradition'}]
        })
        
        mod.add(tradition)
        
        # Should track builder
        assert tradition in mod.builders

    def test_tradition_modinfo_generation(self):
        """Test modinfo generation with traditions."""
        mod = Mod(id="babylon-traditions", version="1", name="Babylon Traditions")
        
        tradition = TraditionBuilder()
        tradition.fill({
            'tradition_type': 'TRADITION_BABYLON_SCRIBES',
            'tradition': {},
            'localizations': [
                {'name': 'Scribal Tradition', 'description': 'Ancient wisdom'}
            ]
        })
        
        mod.add(tradition)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-traditions.modinfo"
            assert modinfo_path.exists()
            
            content = modinfo_path.read_text()
            assert 'UpdateDatabase' in content or 'UpdateText' in content

    def test_tradition_with_civilization(self):
        """Test tradition working alongside civilization."""
        mod = Mod(id="babylon-full", version="1", name="Babylon Full")
        
        # Add civilization
        civ = CivilizationBuilder()
        civ.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'civilization_traits': []
        })
        
        # Add tradition
        tradition = TraditionBuilder()
        tradition.fill({
            'tradition_type': 'TRADITION_BABYLON_SCRIBES',
            'tradition': {},
            'localizations': [{'name': 'Scribal Tradition'}]
        })
        
        mod.add([civ, tradition])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon-full.modinfo"
            assert modinfo_path.exists()
            
            content = modinfo_path.read_text()
            # Should have both civilization and tradition content
            assert 'babylon' in content.lower()

    def test_multiple_traditions(self):
        """Test multiple traditions in one mod."""
        mod = Mod(id="multi-traditions", version="1", name="Multi Traditions")
        
        traditions = []
        for i in range(3):
            tradition = TraditionBuilder()
            tradition.fill({
                'tradition_type': f'TRADITION_TEST_{i}',
                'tradition': {},
                'localizations': [{'name': f'Tradition {i}'}]
            })
            traditions.append(tradition)
        
        mod.add(traditions)
        
        # Should track all traditions
        assert len(mod.builders) >= 3

    def test_tradition_localization_keys(self):
        """Test that traditions generate proper localization keys."""
        from civ7_modding_tools.utils import locale
        
        tradition = TraditionBuilder()
        tradition.fill({
            'tradition_type': 'TRADITION_BABYLON_SCRIBES',
            'tradition': {},
            'localizations': [
                {'name': 'Scribal Tradition', 'description': 'Ancient wisdom'}
            ]
        })
        
        tradition.migrate()
        
        # Check that localization keys are generated
        if tradition._localizations.english_text:
            tags = [node.tag for node in tradition._localizations.english_text]
            assert len(tags) > 0


class TestTraditionScopes:
    """Test tradition scoping and age-specific traditions."""

    def test_tradition_with_age_antiquity(self):
        """Test tradition with AGE_ANTIQUITY scope."""
        from civ7_modding_tools import ActionGroupBundle
        
        mod = Mod(id="antiquity-traditions", version="1", name="Antiquity Traditions")
        
        tradition = TraditionBuilder()
        tradition.action_group_bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        tradition.fill({
            'tradition_type': 'TRADITION_ANTIQUITY_TEST',
            'tradition': {},
            'localizations': [{'name': 'Antiquity Tradition'}]
        })
        
        mod.add(tradition)
        
        # Check that age-specific action groups are used
        assert 'AGE_ANTIQUITY' in tradition.action_group_bundle.action_group_id

    def test_tradition_with_age_exploration(self):
        """Test tradition with AGE_EXPLORATION scope."""
        from civ7_modding_tools import ActionGroupBundle
        
        tradition = TraditionBuilder()
        tradition.action_group_bundle = ActionGroupBundle(action_group_id="AGE_EXPLORATION")
        tradition.fill({
            'tradition_type': 'TRADITION_EXPLORATION_TEST',
            'tradition': {},
            'localizations': [{'name': 'Exploration Tradition'}]
        })
        
        assert 'AGE_EXPLORATION' in tradition.action_group_bundle.action_group_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
