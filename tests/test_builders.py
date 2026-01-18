"""Tests for builder functionality."""

import pytest
from civ7_modding_tools.builders import BaseBuilder, CivilizationBuilder
from civ7_modding_tools.core import ActionGroupBundle


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
