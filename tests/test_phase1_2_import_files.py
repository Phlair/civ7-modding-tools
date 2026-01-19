"""Tests for Phase 1.2: ImportFiles in Modinfo."""

import pytest
import tempfile
from pathlib import Path
from civ7_modding_tools import Mod
from civ7_modding_tools.builders import ImportFileBuilder, CivilizationBuilder


class TestImportFilesInModinfo:
    """Test ImportFiles generation in modinfo."""

    def test_import_file_builder_scope_property(self):
        """Test ImportFileBuilder scope property."""
        builder = ImportFileBuilder()
        
        # Default scope should be "game"
        assert builder.scope == "game"
        
        # Scope should be settable
        builder.scope = "shell"
        assert builder.scope == "shell"

    def test_import_file_builder_get_import_entries(self):
        """Test get_import_entries method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file to import
            test_file = Path(tmpdir) / "test.png"
            test_file.write_text("test content")
            
            builder = ImportFileBuilder()
            builder.source_path = str(test_file)
            builder.target_name = "test-icon"
            builder.target_directory = "/icons/"
            
            entries = builder.get_import_entries()
            
            # Should have both folder and file entries
            assert len(entries) >= 1
            assert "icons" in entries or "/icons/" in entries or "icons/test-icon" in entries

    def test_import_file_builder_get_import_entries_without_source(self):
        """Test get_import_entries with missing source."""
        builder = ImportFileBuilder()
        builder.source_path = "/nonexistent/file.png"
        builder.target_name = "test-icon"
        
        entries = builder.get_import_entries()
        
        # Should handle gracefully
        assert isinstance(entries, list)

    def test_mod_tracks_import_file_builders(self):
        """Test that Mod tracks ImportFileBuilder instances."""
        mod = Mod(id="test-mod")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "icon.png"
            test_file.write_text("test")
            
            import_builder = ImportFileBuilder()
            import_builder.source_path = str(test_file)
            import_builder.target_name = "icon"
            
            mod.add(import_builder)
            
            # Mod should track this builder
            assert import_builder in mod.import_file_builders

    def test_mod_does_not_track_non_import_builders(self):
        """Test that non-ImportFileBuilder instances aren't tracked."""
        mod = Mod(id="test-mod")
        
        civ_builder = CivilizationBuilder()
        civ_builder.fill({'civilization_type': 'CIVILIZATION_TEST'})
        
        mod.add(civ_builder)
        
        # Civilization builder should not be in import_file_builders
        assert civ_builder not in mod.import_file_builders
        assert len(mod.import_file_builders) == 0

    def test_modinfo_includes_import_files_block(self):
        """Test that modinfo includes ImportFiles block when imports are present."""
        mod = Mod(id="test-mod", version="1", name="Test")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "icon.png"
            test_file.write_text("test")
            
            # Add import builder
            import_builder = ImportFileBuilder()
            import_builder.source_path = str(test_file)
            import_builder.target_name = "icon"
            import_builder.target_directory = "/icons/"
            import_builder.scope = "shell"
            
            mod.add(import_builder)
            
            # Build and check modinfo
            dist_dir = Path(tmpdir) / "dist"
            mod.build(str(dist_dir))
            
            modinfo_path = dist_dir / "test-mod.modinfo"
            assert modinfo_path.exists()
            
            content = modinfo_path.read_text()
            
            # Should contain ImportFiles action
            assert "ImportFiles" in content

    def test_multiple_import_builders(self):
        """Test multiple ImportFileBuilder instances."""
        mod = Mod(id="multi-import", version="1", name="Multi Import")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple test files
            file1 = Path(tmpdir) / "icon1.png"
            file1.write_text("test1")
            file2 = Path(tmpdir) / "icon2.png"
            file2.write_text("test2")
            
            # Add multiple import builders
            import1 = ImportFileBuilder()
            import1.source_path = str(file1)
            import1.target_name = "icon1"
            import1.scope = "shell"
            
            import2 = ImportFileBuilder()
            import2.source_path = str(file2)
            import2.target_name = "icon2"
            import2.scope = "game"
            
            mod.add([import1, import2])
            
            # Both should be tracked
            assert len(mod.import_file_builders) == 2
            
            # Build and verify
            dist_dir = Path(tmpdir) / "dist"
            mod.build(str(dist_dir))
            
            modinfo_path = dist_dir / "multi-import.modinfo"
            content = modinfo_path.read_text()
            
            # Should have ImportFiles entries
            assert "ImportFiles" in content

    def test_import_builder_scope_shell(self):
        """Test ImportFileBuilder with shell scope."""
        builder = ImportFileBuilder()
        builder.scope = "shell"
        
        assert builder.scope == "shell"

    def test_import_builder_scope_game(self):
        """Test ImportFileBuilder with game scope."""
        builder = ImportFileBuilder()
        builder.scope = "game"  # default
        
        assert builder.scope == "game"

    def test_import_builder_scope_always(self):
        """Test ImportFileBuilder with always scope."""
        builder = ImportFileBuilder()
        builder.scope = "always"
        
        assert builder.scope == "always"


class TestImportFilesIntegration:
    """Integration tests for ImportFiles in modinfo."""

    def test_import_and_civilization_together(self):
        """Test ImportFileBuilder and CivilizationBuilder in same mod."""
        mod = Mod(id="babylon-with-imports", version="1", name="Babylon Imports")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            icon_file = Path(tmpdir) / "babylon-icon.png"
            icon_file.write_text("icon data")
            
            # Add civilization
            civ_builder = CivilizationBuilder()
            civ_builder.fill({'civilization_type': 'CIVILIZATION_BABYLON'})
            
            # Add import
            import_builder = ImportFileBuilder()
            import_builder.source_path = str(icon_file)
            import_builder.target_name = "babylon-icon"
            import_builder.target_directory = "/icons/"
            
            mod.add([civ_builder, import_builder])
            
            # Verify tracking
            assert len(mod.builders) == 2
            assert len(mod.import_file_builders) == 1
            
            # Build and verify modinfo
            dist_dir = Path(tmpdir) / "dist"
            mod.build(str(dist_dir))
            
            modinfo_path = dist_dir / "babylon-with-imports.modinfo"
            content = modinfo_path.read_text()
            
            # Should have both UpdateDatabase (from civilization) and ImportFiles
            assert "UpdateDatabase" in content
            assert "ImportFiles" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
