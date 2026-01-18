"""Tests for Phase 3: Localization implementations."""

import pytest
from civ7_modding_tools.localizations import (
    BaseLocalization,
    CivilizationLocalization,
    UnitLocalization,
    ConstructibleLocalization,
    ProgressionTreeLocalization,
    ProgressionTreeNodeLocalization,
    ModifierLocalization,
    TraditionLocalization,
    LeaderUnlockLocalization,
    CivilizationUnlockLocalization,
    UniqueQuarterLocalization,
)


class TestBaseLocalization:
    """Tests for BaseLocalization."""

    def test_base_localization_creation(self):
        """Test creating a base localization."""
        loc = BaseLocalization()
        assert isinstance(loc, BaseLocalization)

    def test_base_localization_extra_allow(self):
        """Test that extra fields are allowed."""
        loc = BaseLocalization(custom_field="value")
        assert loc.custom_field == "value"

    def test_base_localization_repr(self):
        """Test string representation."""
        loc = BaseLocalization()
        repr_str = repr(loc)
        assert "BaseLocalization" in repr_str

    def test_base_localization_fill(self):
        """Test filling with arbitrary data."""
        loc = BaseLocalization(
            field1="value1",
            field2="value2",
        )
        data = loc.model_dump()
        assert data["field1"] == "value1"
        assert data["field2"] == "value2"


class TestCivilizationLocalization:
    """Tests for CivilizationLocalization."""

    def test_civilization_localization_creation(self):
        """Test creating civilization localization."""
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient Roman Empire",
            full_name="The Roman Empire",
            adjective="Roman",
        )
        assert loc.name == "Rome"
        assert loc.description == "Ancient Roman Empire"
        assert loc.full_name == "The Roman Empire"
        assert loc.adjective == "Roman"

    def test_civilization_localization_with_city_names(self):
        """Test civilization localization with city names."""
        cities = ["Rome", "Milan", "Venice", "Florence"]
        loc = CivilizationLocalization(
            name="Rome",
            city_names=cities,
        )
        assert loc.city_names == cities

    def test_civilization_localization_partial(self):
        """Test civilization localization with partial data."""
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient empire",
        )
        assert loc.name == "Rome"
        assert loc.description == "Ancient empire"
        assert loc.full_name is None
        assert loc.city_names is None

    def test_civilization_localization_model_dump(self):
        """Test model_dump excludes None values."""
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient empire",
        )
        data = loc.model_dump(exclude_none=True)
        assert "name" in data
        assert "description" in data
        assert "full_name" not in data


class TestUnitLocalization:
    """Tests for UnitLocalization."""

    def test_unit_localization_creation(self):
        """Test creating unit localization."""
        loc = UnitLocalization(
            name="Warrior",
            description="Basic melee unit",
        )
        assert loc.name == "Warrior"
        assert loc.description == "Basic melee unit"

    def test_unit_localization_with_unique_name(self):
        """Test unit localization with unique name."""
        loc = UnitLocalization(
            name="Legionnaire",
            unique_name="Roman Legionnaire",
            description="Elite Roman melee unit",
        )
        assert loc.unique_name == "Roman Legionnaire"


class TestConstructibleLocalization:
    """Tests for ConstructibleLocalization."""

    def test_constructible_localization_creation(self):
        """Test creating constructible localization."""
        loc = ConstructibleLocalization(
            name="Temple",
            description="Religious building",
        )
        assert loc.name == "Temple"
        assert loc.description == "Religious building"

    def test_constructible_localization_with_unique(self):
        """Test constructible with unique name."""
        loc = ConstructibleLocalization(
            name="Temple",
            unique_name="Roman Temple",
            description="Religious building",
        )
        assert loc.unique_name == "Roman Temple"


class TestProgressionTreeLocalization:
    """Tests for ProgressionTreeLocalization."""

    def test_progression_tree_localization(self):
        """Test creating progression tree localization."""
        loc = ProgressionTreeLocalization(
            name="Technology Tree",
            description="Discovery and innovation",
        )
        assert loc.name == "Technology Tree"
        assert loc.description == "Discovery and innovation"


class TestProgressionTreeNodeLocalization:
    """Tests for ProgressionTreeNodeLocalization."""

    def test_progression_tree_node_localization(self):
        """Test creating progression tree node localization."""
        loc = ProgressionTreeNodeLocalization(
            name="Writing",
            description="Develop written communication",
            quote="The written word is civilization.",
        )
        assert loc.name == "Writing"
        assert loc.description == "Develop written communication"
        assert loc.quote == "The written word is civilization."

    def test_progression_tree_node_without_quote(self):
        """Test progression tree node without quote."""
        loc = ProgressionTreeNodeLocalization(
            name="Writing",
            description="Develop written communication",
        )
        assert loc.quote is None


class TestModifierLocalization:
    """Tests for ModifierLocalization."""

    def test_modifier_localization(self):
        """Test creating modifier localization."""
        loc = ModifierLocalization(
            name="Economic Boost",
            description="Increases gold production",
        )
        assert loc.name == "Economic Boost"
        assert loc.description == "Increases gold production"


class TestTraditionLocalization:
    """Tests for TraditionLocalization."""

    def test_tradition_localization(self):
        """Test creating tradition localization."""
        loc = TraditionLocalization(
            name="Classical Legacy",
            description="Inherit ancient wisdom",
        )
        assert loc.name == "Classical Legacy"
        assert loc.description == "Inherit ancient wisdom"


class TestLeaderUnlockLocalization:
    """Tests for LeaderUnlockLocalization."""

    def test_leader_unlock_localization(self):
        """Test creating leader unlock localization."""
        loc = LeaderUnlockLocalization(
            leader_name="Julius Caesar",
            description="Legendary military commander",
        )
        assert loc.leader_name == "Julius Caesar"
        assert loc.description == "Legendary military commander"


class TestCivilizationUnlockLocalization:
    """Tests for CivilizationUnlockLocalization."""

    def test_civilization_unlock_localization(self):
        """Test creating civilization unlock localization."""
        loc = CivilizationUnlockLocalization(
            name="Roman Expansion",
            description="Unlock new Roman civilization variant",
        )
        assert loc.name == "Roman Expansion"
        assert loc.description == "Unlock new Roman civilization variant"


class TestUniqueQuarterLocalization:
    """Tests for UniqueQuarterLocalization."""

    def test_unique_quarter_localization(self):
        """Test creating unique quarter localization."""
        loc = UniqueQuarterLocalization(
            name="Roman Forum",
            description="Unique commercial quarter",
        )
        assert loc.name == "Roman Forum"
        assert loc.description == "Unique commercial quarter"


class TestLocalizationIntegration:
    """Integration tests for localizations."""

    def test_localization_with_builders(self):
        """Test using localizations with builders."""
        from civ7_modding_tools.builders import CivilizationBuilder
        
        builder = CivilizationBuilder()
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient empire",
            city_names=["Rome", "Milan"],
        )
        
        # Builder should accept localizations
        builder.localizations = [loc]
        assert len(builder.localizations) == 1
        assert builder.localizations[0].name == "Rome"

    def test_multiple_localizations(self):
        """Test using multiple localization types."""
        civ_loc = CivilizationLocalization(name="Rome")
        unit_loc = UnitLocalization(name="Legionnaire")
        building_loc = ConstructibleLocalization(name="Forum")
        
        # Should all be distinct types
        assert isinstance(civ_loc, CivilizationLocalization)
        assert isinstance(unit_loc, UnitLocalization)
        assert isinstance(building_loc, ConstructibleLocalization)
        
        # But all extend BaseLocalization
        assert isinstance(civ_loc, BaseLocalization)
        assert isinstance(unit_loc, BaseLocalization)
        assert isinstance(building_loc, BaseLocalization)

    def test_localization_serialization(self):
        """Test that localizations can be serialized to dict."""
        loc = CivilizationLocalization(
            name="Rome",
            description="Ancient empire",
            city_names=["Rome", "Milan"],
        )
        
        data = loc.model_dump()
        assert data["name"] == "Rome"
        assert data["city_names"] == ["Rome", "Milan"]

    def test_localization_partial_serialization(self):
        """Test excluding None values during serialization."""
        loc = CivilizationLocalization(
            name="Rome",
            description=None,
        )
        
        data_all = loc.model_dump()
        data_filtered = loc.model_dump(exclude_none=True)
        
        # All version should include None values
        assert "description" in data_all
        # Filtered should not
        assert "description" not in data_filtered


class TestLocalizationTypes:
    """Type safety tests for localizations."""

    def test_all_localization_types_are_models(self):
        """Test that all localization types are pydantic models."""
        from pydantic import BaseModel
        
        loc_types = [
            BaseLocalization,
            CivilizationLocalization,
            UnitLocalization,
            ConstructibleLocalization,
            ProgressionTreeLocalization,
            ProgressionTreeNodeLocalization,
            ModifierLocalization,
            TraditionLocalization,
            LeaderUnlockLocalization,
            CivilizationUnlockLocalization,
            UniqueQuarterLocalization,
        ]
        
        for loc_type in loc_types:
            assert issubclass(loc_type, BaseModel)

    def test_localization_field_validation(self):
        """Test that localization fields are properly typed."""
        # Should accept strings
        loc = CivilizationLocalization(name="Rome")
        assert loc.name == "Rome"
        
        # Should accept list of strings for city_names
        loc2 = CivilizationLocalization(
            city_names=["Rome", "Milan", "Venice"]
        )
        assert len(loc2.city_names) == 3
        assert all(isinstance(name, str) for name in loc2.city_names)
