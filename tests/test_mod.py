"""Tests for mod orchestrator."""

import pytest
from pathlib import Path
from civ7_modding_tools.core import Mod
from civ7_modding_tools.files import XmlFile
from civ7_modding_tools.nodes import BaseNode


def test_mod_creation():
    """Test creating a mod."""
    mod = Mod(
        mod_id="test-mod",
        version="1.0.0",
        name="Test Mod",
        description="A test mod",
        authors="Test Author"
    )
    
    assert mod.mod_id == "test-mod"
    assert mod.version == "1.0.0"
    assert mod.name == "Test Mod"


def test_mod_add_builder():
    """Test adding builders to mod."""
    from civ7_modding_tools.builders import CivilizationBuilder
    
    mod = Mod()
    builder = CivilizationBuilder()
    
    result = mod.add(builder)
    
    assert result is mod  # Fluent API
    assert builder in mod.builders


def test_mod_add_multiple_builders():
    """Test adding multiple builders at once."""
    from civ7_modding_tools.builders import CivilizationBuilder, UnitBuilder
    
    mod = Mod()
    builders = [CivilizationBuilder(), UnitBuilder()]
    
    result = mod.add(builders)
    
    assert result is mod
    assert len(mod.builders) == 2


def test_mod_build_creates_modinfo(tmp_path):
    """Test that mod.build() creates .modinfo file."""
    mod = Mod(mod_id="test-mod", version="1.0.0")
    mod.build(str(tmp_path))
    
    modinfo_file = tmp_path / "test-mod.modinfo"
    assert modinfo_file.exists()
    
    # Check content
    content = modinfo_file.read_text()
    assert '<?xml version="1.0" encoding="UTF-8"?>' in content
    assert '<Mod id="test-mod"' in content


def test_mod_build_with_files(tmp_path):
    """Test mod.build() with generated files."""
    mod = Mod(mod_id="test-mod")
    
    # Add a file with some content
    node = BaseNode()
    node.civilization_type = "TEST_CIV"
    
    xml_file = XmlFile(
        path="/test/",
        name="test.xml",
        content=[node]
    )
    mod.add_files(xml_file)
    
    mod.build(str(tmp_path))
    
    # Check files were created
    test_file = tmp_path / "test" / "test.xml"
    assert test_file.exists()
    
    content = test_file.read_text()
    assert "CivilizationType" in content
    assert "TEST_CIV" in content


def test_mod_build_clears_directory(tmp_path):
    """Test that build with clear=True removes old files."""
    mod = Mod(mod_id="test-mod")
    
    # Create old file
    old_file = tmp_path / "old.txt"
    old_file.write_text("old content")
    
    # Build with clear=True
    mod.build(str(tmp_path), clear=True)
    
    # Old file should be gone
    assert not old_file.exists()
    
    # .modinfo should exist
    modinfo = tmp_path / "test-mod.modinfo"
    assert modinfo.exists()
