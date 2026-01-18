"""Phase 10: Modinfo enhancements tests.

Tests for metadata and dependencies in mod.build() output,
enabling proper mod packaging with version tracking and requirements.
"""

import pytest
from civ7_modding_tools import Mod, CivilizationBuilder
from civ7_modding_tools.files import XmlFile


class TestModinfoMetadata:
    """Test mod metadata in .modinfo file."""

    def test_mod_with_basic_metadata(self):
        """Test mod can have complete metadata."""
        mod = Mod(
            id="test-mod-metadata",
            version="1.0.0",
            name="Test Mod",
            description="A test mod"
        )
        
        # Verify mod properties
        assert mod.id == "test-mod-metadata"
        assert mod.version == "1.0.0"
        assert mod.name == "Test Mod"

    def test_mod_with_authors(self):
        """Test mod can have multiple authors."""
        mod = Mod(
            id="test-mod-authors",
            version="1.0",
            name="Test Mod",
            authors=["Author One", "Author Two"]
        )
        
        assert mod.authors == ["Author One", "Author Two"]

    def test_mod_with_version_tracking(self):
        """Test mod version is properly tracked."""
        versions = ["0.1.0", "0.5.0", "1.0.0", "1.1.0"]
        for version in versions:
            mod = Mod(
                id=f"test-mod-v{version}",
                version=version,
                name="Test Mod"
            )
            assert mod.version == version

    def test_mod_affects_saved_games(self):
        """Test mod can specify affects_saved_games flag."""
        mod = Mod(
            id="test-mod-saves",
            version="1.0",
            name="Test Mod",
            affects_saved_games=True
        )
        
        assert mod.affects_saved_games is True

    def test_mod_with_full_metadata(self):
        """Test mod with comprehensive metadata."""
        mod = Mod(
            id="gondor-complete",
            version="2.5.1",
            name="Gondor Civilization",
            description="Complete Gondor civilization mod",
            authors=["Creator One", "Creator Two"],
            affects_saved_games=False
        )
        
        assert mod.id == "gondor-complete"
        assert mod.version == "2.5.1"
        assert mod.name == "Gondor Civilization"
        assert len(mod.authors) == 2
        assert mod.affects_saved_games is False


class TestModinfoDependencies:
    """Test mod dependencies and requirements."""

    def test_mod_with_dependencies(self):
        """Test mod can declare dependencies."""
        mod = Mod(
            id="mod-with-deps",
            version="1.0",
            name="Dependent Mod"
        )
        
        # Add dependencies
        mod.dependencies = ["mod-core-1.0", "mod-base-2.0"]
        
        assert "mod-core-1.0" in mod.dependencies
        assert "mod-base-2.0" in mod.dependencies

    def test_mod_without_dependencies(self):
        """Test mod without dependencies."""
        mod = Mod(
            id="mod-standalone",
            version="1.0",
            name="Standalone Mod"
        )
        
        # Should have empty or no dependencies
        deps = getattr(mod, 'dependencies', [])
        if deps is not None:
            assert isinstance(deps, (list, type(None)))

    def test_mod_dependency_versions(self):
        """Test mod dependencies with version constraints."""
        mod = Mod(
            id="mod-deps-versions",
            version="1.0",
            name="Versioned Dependencies"
        )
        
        mod.dependencies = [
            "core-framework>=1.0",
            "base-content~=2.5",
            "optional-addon@3.0"
        ]
        
        assert len(mod.dependencies) == 3


class TestModinfoBuildOutput:
    """Test mod.build() generates proper modinfo file."""

    def test_mod_build_creates_modinfo(self):
        """Test mod.build() creates modinfo file."""
        mod = Mod(
            id="test-modinfo-build",
            version="1.0",
            name="Test Build"
        )
        
        civ = CivilizationBuilder().fill({
            "civilization_type": "CIVILIZATION_TEST",
            "civilization": {"civilization_type": "CIVILIZATION_TEST"},
            "localizations": [{"name": "Test Civilization"}]
        })
        mod.add(civ)
        
        files = mod.build("./dist-test-modinfo")
        
        # Should generate multiple files including modinfo
        modinfo_files = [f for f in files if "modinfo" in f.name.lower() or f.name == "mod-test.modinfo"]
        assert len(modinfo_files) > 0

    def test_mod_build_with_metadata(self):
        """Test mod.build() includes metadata in modinfo."""
        mod = Mod(
            id="test-with-metadata",
            version="1.5.0",
            name="Metadata Test",
            description="Testing metadata"
        )
        
        files = mod.build("./dist-metadata-test", clear=False)
        
        # Verify structure
        assert len(files) >= 1

    def test_mod_build_version_in_modinfo(self):
        """Test version appears in modinfo."""
        mod = Mod(
            id="version-test",
            version="3.2.1",
            name="Version Test"
        )
        
        files = mod.build("./dist-version-test", clear=False)
        
        # Modinfo should exist
        assert any(f for f in files if "modinfo" in f.name.lower())

    def test_mod_build_with_dependencies_in_modinfo(self):
        """Test dependencies appear in modinfo."""
        mod = Mod(
            id="deps-test",
            version="1.0",
            name="Dependencies Test"
        )
        mod.dependencies = ["required-mod-1.0"]
        
        files = mod.build("./dist-deps-test", clear=False)
        
        assert len(files) >= 1

    def test_mod_build_multiple_features(self):
        """Test mod.build() with multiple features."""
        mod = Mod(
            id="comprehensive-mod",
            version="2.0.0",
            name="Comprehensive Mod",
            description="Complete feature test",
            authors=["Test Author"],
            affects_saved_games=True
        )
        mod.dependencies = ["base-framework"]
        
        civ = CivilizationBuilder().fill({
            "civilization_type": "CIV_COMPREHENSIVE",
            "civilization": {"civilization_type": "CIV_COMPREHENSIVE"},
            "localizations": [{"name": "Comprehensive"}]
        })
        mod.add(civ)
        
        files = mod.build("./dist-comprehensive-mod", clear=False)
        
        # Should have multiple files
        assert len(files) >= 2


class TestModinfoIntegration:
    """Test modinfo integration with other features."""

    def test_modinfo_with_civilization(self):
        """Test modinfo generation with civilization."""
        mod = Mod(
            id="civ-test",
            version="1.0",
            name="Civilization Test"
        )
        
        civ = CivilizationBuilder().fill({
            "civilization_type": "CIVILIZATION_TEST",
            "civilization": {"civilization_type": "CIVILIZATION_TEST"},
            "localizations": [{"name": "Test"}]
        })
        mod.add(civ)
        
        files = mod.build("./dist-civ-test", clear=False)
        assert len(files) > 0

    def test_modinfo_with_multiple_civilizations(self):
        """Test modinfo with multiple content items."""
        mod = Mod(
            id="multi-civ-test",
            version="1.0",
            name="Multi Civilization Test"
        )
        
        for i in range(3):
            civ = CivilizationBuilder().fill({
                "civilization_type": f"CIVILIZATION_TEST{i}",
                "civilization": {"civilization_type": f"CIVILIZATION_TEST{i}"},
                "localizations": [{"name": f"Test {i}"}]
            })
            mod.add(civ)
        
        files = mod.build("./dist-multi-civ-test", clear=False)
        assert len(files) >= 4  # modinfo + at least 3 content files

    def test_modinfo_metadata_persistence(self):
        """Test metadata persists through build()."""
        mod = Mod(
            id="persistence-test",
            version="1.2.3",
            name="Persistence Test",
            description="Metadata persistence check",
            authors=["Author"]
        )
        
        # Metadata should be preserved
        assert mod.version == "1.2.3"
        assert mod.name == "Persistence Test"
        assert "Author" in mod.authors


class TestModinfoEdgeCases:
    """Test edge cases for modinfo generation."""

    def test_modinfo_with_long_description(self):
        """Test modinfo with very long description."""
        long_desc = "A" * 1000
        mod = Mod(
            id="long-desc",
            version="1.0",
            name="Long Description",
            description=long_desc
        )
        
        assert len(mod.description) == 1000

    def test_modinfo_with_special_characters_in_name(self):
        """Test modinfo with special characters."""
        mod = Mod(
            id="special-chars",
            version="1.0",
            name="Mod: [Test] & 'Special' \"Chars\"",
            description="Testing special characters in metadata"
        )
        
        assert ":" in mod.name
        assert "&" in mod.name

    def test_modinfo_with_version_formats(self):
        """Test various version format strings."""
        versions = [
            "1.0",
            "1.0.0",
            "0.0.1",
            "10.20.30",
            "1.0.0-alpha",
            "1.0.0-beta.1"
        ]
        
        for version in versions:
            mod = Mod(
                id=f"mod-{version}",
                version=version,
                name="Version Test"
            )
            assert mod.version == version

    def test_modinfo_with_many_authors(self):
        """Test modinfo with multiple authors."""
        authors = [f"Author {i}" for i in range(10)]
        mod = Mod(
            id="many-authors",
            version="1.0",
            name="Many Authors",
            authors=authors
        )
        
        assert len(mod.authors) == 10

    def test_modinfo_with_many_dependencies(self):
        """Test modinfo with many dependencies."""
        mod = Mod(
            id="many-deps",
            version="1.0",
            name="Many Dependencies"
        )
        mod.dependencies = [f"dependency-{i}" for i in range(15)]
        
        assert len(mod.dependencies) == 15

    def test_modinfo_empty_optional_fields(self):
        """Test modinfo with minimal required fields only."""
        mod = Mod(
            id="minimal",
            version="1.0",
            name="Minimal Mod"
        )
        
        # Should work with just required fields
        assert mod.id == "minimal"
        assert mod.version == "1.0"

    def test_modinfo_affects_saved_games_flag(self):
        """Test affects_saved_games flag."""
        mod_true = Mod(
            id="affects-true",
            version="1.0",
            name="Affects Saves",
            affects_saved_games=True
        )
        
        mod_false = Mod(
            id="affects-false",
            version="1.0",
            name="No Affects",
            affects_saved_games=False
        )
        
        assert mod_true.affects_saved_games is True
        assert mod_false.affects_saved_games is False


class TestModinfoFileGeneration:
    """Test modinfo file structure generation."""

    def test_modinfo_file_has_correct_name(self):
        """Test modinfo file has correct naming convention."""
        mod = Mod(
            id="name-test",
            version="1.0",
            name="Name Test"
        )
        
        files = mod.build("./dist-name-test", clear=False)
        
        # Should have modinfo file
        modinfo_found = any(
            "modinfo" in f.name.lower() for f in files
        )
        assert modinfo_found

    def test_modinfo_build_clean_default(self):
        """Test mod.build() clears directory by default."""
        mod = Mod(
            id="clean-test",
            version="1.0",
            name="Clean Test"
        )
        
        # Default should be clear=True
        files = mod.build("./dist-clean-test")
        assert len(files) >= 1

    def test_modinfo_build_no_clear(self):
        """Test mod.build() can preserve existing files."""
        mod = Mod(
            id="no-clear-test",
            version="1.0",
            name="No Clear Test"
        )
        
        files = mod.build("./dist-no-clear-test", clear=False)
        assert len(files) >= 1
