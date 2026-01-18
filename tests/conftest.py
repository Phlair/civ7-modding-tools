"""Test configuration and shared fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_mod_dir(tmp_path):
    """Provide a temporary directory for mod generation tests."""
    return tmp_path / "test_mod"


@pytest.fixture
def example_xml_dir():
    """Provide path to example generated mod XML files."""
    return Path(__file__).parent.parent / "example-generated-mod"
