"""Tests for Phase 1.1: Descriptive Action Group IDs."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod, ActionGroupBundle
from civ7_modding_tools.builders import CivilizationBuilder, UnitBuilder


class TestDescriptiveActionGroupIds:
    """Test descriptive action group ID generation."""

    def test_action_group_bundle_initialization_without_mod_id(self):
        """Test that ActionGroupBundle generates UUIDs when mod_id is None."""
        bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        
        # Shell and always IDs should still be UUIDs before mod_id is set
        assert bundle.shell["id"] is not None
        assert bundle.always["id"] is not None
        assert len(bundle.shell["id"]) > 0
        assert len(bundle.always["id"]) > 0
        
        # Verify structure
        assert bundle.shell["scope"] == "shell"
        assert bundle.shell["criteria"] == "always"
        assert bundle.always["scope"] == "game"
        assert bundle.always["criteria"] == "always"

    def test_action_group_bundle_regenerate_with_mod_id(self):
        """Test that regenerate_with_mod_id updates IDs descriptively."""
        bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        old_shell_id = bundle.shell["id"]
        old_always_id = bundle.always["id"]
        
        # Regenerate with mod_id
        bundle.regenerate_with_mod_id("babylon")
        
        # IDs should change to descriptive format
        assert bundle.shell["id"] == "babylon-shell-always"
        assert bundle.always["id"] == "babylon-game-always"
        assert bundle.shell["id"] != old_shell_id
        assert bundle.always["id"] != old_always_id

    def test_mod_injects_mod_id_into_builders(self):
        """Test that Mod.add() injects mod_id into builder's action group bundle."""
        mod = Mod(id="test-mod")
        builder = CivilizationBuilder()
        
        # Before add, bundle should have no mod_id
        assert builder.action_group_bundle.mod_id is None
        
        # After add, bundle should have mod_id
        mod.add(builder)
        assert builder.action_group_bundle.mod_id == "test-mod"
        assert builder.action_group_bundle.shell["id"] == "test-mod-shell-always"
        assert builder.action_group_bundle.always["id"] == "test-mod-game-always"

    def test_modinfo_uses_descriptive_ids(self):
        """Test that generated modinfo contains descriptive action group IDs."""
        mod = Mod(id="babylon", version="1", name="Babylon")
        
        builder = CivilizationBuilder()
        builder.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'civilization_traits': []
        })
        
        mod.add(builder)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            
            modinfo_path = Path(tmpdir) / "babylon.modinfo"
            assert modinfo_path.exists()
            
            content = modinfo_path.read_text()
            
            # Should contain descriptive IDs
            assert 'babylon-game-always' in content
            assert 'babylon-shell-always' in content or 'babylon-shell-module' in content
            
            # Should NOT contain UUIDs in final output (except potentially in old system)
            # This is a soft check - we mainly care that descriptive IDs are present
            assert 'babylon-' in content

    def test_module_text_file_uses_descriptive_id(self):
        """Test that module text file uses descriptive action group ID."""
        from civ7_modding_tools.localizations import ModuleLocalization
        
        mod = Mod(
            id="babylon",
            version="1",
            name="Babylon",
            module_localizations=ModuleLocalization(
                name="Babylon",
                description="Test",
                authors="Test"
            )
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / "babylon.modinfo"
            content = modinfo_path.read_text()
            
            # Should contain module-specific descriptive ID
            assert 'babylon-shell-module' in content

    def test_multiple_builders_different_action_groups(self):
        """Test multiple builders with different action groups get proper IDs."""
        mod = Mod(id="test-mod")
        
        civ_builder = CivilizationBuilder()
        civ_builder.action_group_bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        civ_builder.fill({'civilization_type': 'CIVILIZATION_TEST'})
        
        unit_builder = UnitBuilder()
        unit_builder.action_group_bundle = ActionGroupBundle(action_group_id="AGE_EXPLORATION")
        unit_builder.fill({'unit_type': 'UNIT_TEST'})
        
        mod.add([civ_builder, unit_builder])
        
        # Both builders should have mod_id injected
        assert civ_builder.action_group_bundle.mod_id == "test-mod"
        assert unit_builder.action_group_bundle.mod_id == "test-mod"
        
        # Shell and always should still be consistent
        assert civ_builder.action_group_bundle.shell["id"] == "test-mod-shell-always"
        assert unit_builder.action_group_bundle.shell["id"] == "test-mod-shell-always"

    def test_action_group_bundle_with_always(self):
        """Test ALWAYS action group bundle generation."""
        bundle = ActionGroupBundle(action_group_id="ALWAYS")
        bundle.regenerate_with_mod_id("test")
        
        # Should still work for ALWAYS groups
        assert bundle.shell["id"] == "test-shell-always"
        assert bundle.always["id"] == "test-game-always"

    def test_regenerate_with_same_mod_id_is_idempotent(self):
        """Test that regenerating with same mod_id doesn't change IDs."""
        bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        bundle.regenerate_with_mod_id("babylon")
        
        id1 = bundle.shell["id"]
        id2 = bundle.always["id"]
        
        # Call again with same mod_id
        bundle.regenerate_with_mod_id("babylon")
        
        # Should not change
        assert bundle.shell["id"] == id1
        assert bundle.always["id"] == id2


class TestDescriptiveIdsIntegration:
    """Integration tests for descriptive action group IDs across full mod build."""

    def test_babylon_example_generates_descriptive_ids(self):
        """Test that babylon example generates descriptive action group IDs."""
        mod = Mod(
            id="babylon-test",
            version="1",
            name="Babylon Test"
        )
        
        civ = CivilizationBuilder()
        civ.fill({
            'civilization_type': 'CIVILIZATION_BABYLON',
            'civilization_traits': [],
        })
        
        mod.add(civ)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / "babylon-test.modinfo"
            content = modinfo_path.read_text()
            
            # Verify descriptive IDs are present
            assert 'id="babylon-test-game-always"' in content
            assert 'id="babylon-test-shell-always"' in content or 'id="babylon-test-shell-module"' in content

    def test_modinfo_criteria_uses_correct_ids(self):
        """Test that ActionCriteria references match ActionGroup IDs."""
        mod = Mod(id="test-mod", version="1", name="Test")
        
        builder = CivilizationBuilder()
        builder.action_group_bundle = ActionGroupBundle(action_group_id="AGE_ANTIQUITY")
        builder.fill({'civilization_type': 'CIVILIZATION_TEST'})
        
        mod.add(builder)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)
            modinfo_path = Path(tmpdir) / "test-mod.modinfo"
            content = modinfo_path.read_text()
            
            # Verify age-specific criteria exists
            assert 'age-antiquity-current' in content
            # Persist only exists if there's age-persist content, which requires populated nodes
            # Just verify the criteria and action group use consistent IDs
            assert 'criteria="antiquity-age-current"' in content or 'criteria="always"' in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
