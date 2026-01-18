"""Tests for file output generation."""

import pytest
from pathlib import Path
from civ7_modding_tools.files import XmlFile, ImportFile
from civ7_modding_tools.nodes import BaseNode


def test_xml_file_creation():
    """Test creating an XML file."""
    xml_file = XmlFile(
        path="/test/",
        name="test.xml",
        content=[]
    )
    
    assert xml_file.path == "/test/"
    assert xml_file.name == "test.xml"
    assert xml_file.mod_info_path == "test/test.xml"


def test_xml_file_write(tmp_path):
    """Test writing XML file to disk."""
    node = BaseNode()
    node.test_attr = "value"
    
    xml_file = XmlFile(
        path="/output/",
        name="data.xml",
        content=[node]
    )
    
    xml_file.write(str(tmp_path))
    
    output_file = tmp_path / "output" / "data.xml"
    assert output_file.exists()
    
    content = output_file.read_text()
    assert '<?xml version="1.0" encoding="UTF-8"?>' in content
    assert "TestAttr" in content


def test_xml_file_is_empty():
    """Test is_empty property."""
    xml_file_with_content = XmlFile(content=[BaseNode()])
    assert not xml_file_with_content.is_empty
    
    xml_file_empty = XmlFile(content=None)
    assert xml_file_empty.is_empty


def test_xml_file_strips_path_slashes():
    """Test that path slashes are handled correctly."""
    xml_file = XmlFile(path="/test/path/")
    assert xml_file.mod_info_path == "test/path/file.xml"
    
    xml_file2 = XmlFile(path="test/path")
    assert xml_file2.mod_info_path == "test/path/file.xml"
    
    xml_file3 = XmlFile(path="/")
    assert xml_file3.mod_info_path == "file.xml"


def test_import_file_creation(tmp_path):
    """Test creating an import file."""
    # Create source file
    source_file = tmp_path / "source.txt"
    source_file.write_text("test content")
    
    import_file = ImportFile(
        path="/imports/",
        name="imported",
        content=str(source_file)
    )
    
    assert import_file.source_path == str(source_file)


def test_import_file_write(tmp_path):
    """Test copying import file."""
    # Create source
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "icon.png"
    source_file.write_bytes(b"fake image data")
    
    # Create import file
    import_file = ImportFile(
        path="/imports/",
        name="icon.png",
        content=str(source_file)
    )
    
    # Write to destination
    dest_dir = tmp_path / "dest"
    import_file.write(str(dest_dir))
    
    # Check file was copied
    copied_file = dest_dir / "imports" / "icon.png"
    assert copied_file.exists()
    assert copied_file.read_bytes() == b"fake image data"


def test_import_file_source_not_found():
    """Test error when import source doesn't exist."""
    import_file = ImportFile(content="/nonexistent/file.txt")
    
    with pytest.raises(FileNotFoundError):
        import_file.write("/tmp")
