"""Tests for utility functions."""

import pytest
from civ7_modding_tools.utils import (
    camel_to_pascal,
    start_case,
    without,
    uniq_by,
    flatten,
    fill,
)


class TestCamelToPascal:
    """Tests for camel_to_pascal conversion."""
    
    def test_basic_conversion(self):
        assert camel_to_pascal("civilizationType") == "CivilizationType"
        assert camel_to_pascal("baseTourism") == "BaseTourism"
    
    def test_single_char(self):
        assert camel_to_pascal("x") == "X"
    
    def test_empty_string(self):
        assert camel_to_pascal("") == ""
    
    def test_already_pascal(self):
        assert camel_to_pascal("Already") == "Already"


class TestStartCase:
    """Tests for start_case conversion."""
    
    def test_basic_conversion(self):
        assert start_case("civilizationType") == "Civilization Type"
        assert start_case("myProperty") == "My Property"
    
    def test_single_word(self):
        assert start_case("test") == "Test"
    
    def test_empty_string(self):
        assert start_case("") == ""


class TestWithout:
    """Tests for without function."""
    
    def test_remove_single_value(self):
        result = without([1, 2, 3, 4], 2)
        assert result == [1, 3, 4]
    
    def test_remove_multiple_values(self):
        result = without([1, 2, 3, 4, 5], 2, 4)
        assert result == [1, 3, 5]
    
    def test_empty_list(self):
        result = without([], 1)
        assert result == []
    
    def test_no_matches(self):
        result = without([1, 2, 3], 4)
        assert result == [1, 2, 3]


class TestUniqBy:
    """Tests for uniq_by function."""
    
    def test_basic_uniqueness(self):
        result = uniq_by([1, 2, 2, 3, 3, 3])
        assert result == [1, 2, 3]
    
    def test_with_key_function(self):
        items = [{"id": 1}, {"id": 2}, {"id": 1}]
        result = uniq_by(items, lambda x: x["id"])
        assert len(result) == 2
    
    def test_preserves_order(self):
        result = uniq_by([3, 1, 2, 1, 3])
        assert result == [3, 1, 2]


class TestFlatten:
    """Tests for flatten function."""
    
    def test_flatten_lists(self):
        result = flatten([[1, 2], [3, 4]])
        assert result == [1, 2, 3, 4]
    
    def test_flatten_mixed(self):
        result = flatten([[1, 2], [3], [4, 5]])
        assert result == [1, 2, 3, 4, 5]
    
    def test_flatten_with_scalars(self):
        result = flatten([1, [2, 3], 4])
        assert result == [1, 2, 3, 4]
    
    def test_empty_list(self):
        result = flatten([])
        assert result == []


class TestFill:
    """Tests for fill function."""
    
    def test_fill_object_properties(self):
        class Obj:
            x = None
            y = None
        
        obj = Obj()
        result = fill(obj, {"x": 1, "y": 2})
        
        assert result is obj  # Returns self
        assert obj.x == 1
        assert obj.y == 2
    
    def test_fill_returns_object(self):
        obj = {}
        result = fill(obj, {"key": "value"})
        assert result is obj
