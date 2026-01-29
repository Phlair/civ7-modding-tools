"""Tests for automatic improvement model script generation."""

import tempfile
from pathlib import Path

from civ7_modding_tools import Mod, ConstructibleBuilder, JsFile


def test_improvement_with_visual_remap_generates_js():
    """Test that improvements with visual_remap generate JavaScript model placement script."""
    mod = Mod(id='test-mod', version='1.0.0')
    
    # Create improvement with visual_remap
    improvement = ConstructibleBuilder().fill({
        'constructible_type': 'IMPROVEMENT_TEST_STONES',
        'is_building': False,
        'improvement': {},
        'visual_remap': {'to': 'IMPROVEMENT_MEGALITH'}
    })
    
    mod.add(improvement)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        generated_files = mod.build(tmpdir)
        
        # Find the JS file
        js_files = [f for f in generated_files if isinstance(f, JsFile)]
        assert len(js_files) == 1, "Should generate one JavaScript file"
        
        js_file = js_files[0]
        assert js_file.name == 'test-mod-improvement-models.js'
        assert js_file.path == '/ui/'
        
        # Check content contains required elements
        content = js_file.content
        assert 'TestModImprovementModels' in content
        assert 'IMPROVEMENT_TEST_STONES' in content
        assert 'IMPROVEMENT_MEGALITH' in content
        assert 'WorldUI.createModelGroup' in content
        assert 'ConstructibleAddedToMap' in content
        assert 'ConstructibleRemovedFromMap' in content
        assert 'GameStarted' in content


def test_building_with_visual_remap_does_not_generate_js():
    """Test that buildings with visual_remap do NOT generate JS script."""
    mod = Mod(id='test-mod', version='1.0.0')
    
    # Create building with visual_remap
    building = ConstructibleBuilder().fill({
        'constructible_type': 'BUILDING_TEST',
        'is_building': True,
        'building': {},
        'visual_remap': {'to': 'BUILDING_LIBRARY'}
    })
    
    mod.add(building)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        generated_files = mod.build(tmpdir)
        
        # Should NOT generate JS file
        js_files = [f for f in generated_files if isinstance(f, JsFile)]
        assert len(js_files) == 0, "Should not generate JavaScript for buildings"


def test_multiple_improvements_consolidated_in_single_js():
    """Test that multiple improvements are handled in a single JS file."""
    mod = Mod(id='test-mod', version='1.0.0')
    
    # Create two improvements with visual_remap (use valid base game IDs)
    improvement1 = ConstructibleBuilder().fill({
        'constructible_type': 'IMPROVEMENT_STONES',
        'is_building': False,
        'improvement': {},
        'visual_remap': {'to': 'IMPROVEMENT_MEGALITH'}  # Valid base game improvement
    })
    
    improvement2 = ConstructibleBuilder().fill({
        'constructible_type': 'IMPROVEMENT_GROVE',
        'is_building': False,
        'improvement': {},
        'visual_remap': {'to': 'IMPROVEMENT_PLANTATION'}  # Valid base game improvement
    })
    
    mod.add([improvement1, improvement2])
    
    with tempfile.TemporaryDirectory() as tmpdir:
        generated_files = mod.build(tmpdir)
        
        # Find the JS file
        js_files = [f for f in generated_files if isinstance(f, JsFile)]
        assert len(js_files) == 1, "Should generate single consolidated JS file"
        
        js_file = js_files[0]
        content = js_file.content
        
        # Both improvements should be in the script
        assert 'IMPROVEMENT_STONES' in content
        assert 'IMPROVEMENT_MEGALITH' in content
        assert 'IMPROVEMENT_GROVE' in content
        assert 'IMPROVEMENT_PLANTATION' in content


def test_improvement_without_visual_remap_no_js():
    """Test that improvements without visual_remap don't generate JS."""
    mod = Mod(id='test-mod', version='1.0.0')
    
    # Create improvement WITHOUT visual_remap
    improvement = ConstructibleBuilder().fill({
        'constructible_type': 'IMPROVEMENT_NORMAL',
        'is_building': False,
        'improvement': {}
    })
    
    mod.add(improvement)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        generated_files = mod.build(tmpdir)
        
        # Should NOT generate JS file
        js_files = [f for f in generated_files if isinstance(f, JsFile)]
        assert len(js_files) == 0, "Should not generate JS without visual_remap"


def test_js_file_written_to_disk():
    """Test that JS file is actually written to disk."""
    mod = Mod(id='test-mod', version='1.0.0')
    
    improvement = ConstructibleBuilder().fill({
        'constructible_type': 'IMPROVEMENT_TEST',
        'is_building': False,
        'improvement': {},
        'visual_remap': {'to': 'IMPROVEMENT_FARM'}  # Valid base game ID
    })
    
    mod.add(improvement)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Check file exists on disk
        js_path = Path(tmpdir) / 'ui' / 'test-mod-improvement-models.js'
        assert js_path.exists(), "JS file should be written to disk"
        
        # Check content is not empty
        content = js_path.read_text()
        assert len(content) > 0
        assert 'class TestModImprovementModels' in content


def test_modinfo_includes_uiscripts_action_group():
    """Test that modinfo includes UIScripts action group for JS file."""
    mod = Mod(id='test-mod', version='1.0.0')
    
    improvement = ConstructibleBuilder().fill({
        'constructible_type': 'IMPROVEMENT_TEST',
        'is_building': False,
        'improvement': {},
        'visual_remap': {'to': 'IMPROVEMENT_FARM'}  # Valid base game ID
    })
    
    mod.add(improvement)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mod.build(tmpdir)
        
        # Read modinfo
        modinfo_path = Path(tmpdir) / 'test-mod.modinfo'
        assert modinfo_path.exists()
        
        modinfo_content = modinfo_path.read_text()
        
        # Check for UIScripts action
        assert '<UIScripts>' in modinfo_content
        assert 'ui/test-mod-improvement-models.js' in modinfo_content
