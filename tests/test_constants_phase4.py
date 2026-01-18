"""Tests for Phase 4: Game constants implementation."""

import pytest
from civ7_modding_tools.constants import (
    # Traits
    Trait,
    TagTrait,
    # Units
    UnitClass,
    UnitMovementClass,
    UnitCulture,
    # Constructibles
    ConstructibleTypeTag,
    ConstructibleClass,
    District,
    # Resources
    Yield,
    Resource,
    # Progression
    Age,
    ActionGroup,
    ActionGroupAction,
    # Map
    Terrain,
    Biome,
    Feature,
    FeatureClass,
    # Mechanics
    Effect,
    Requirement,
    RequirementSet,
    Collection,
    # Display
    Icon,
    Language,
    # Domains
    Domain,
    CivilizationDomain,
    # Other
    Plunder,
    Advisory,
)


class TestTraitConstants:
    """Tests for Trait constants."""

    def test_trait_economic(self):
        """Test TRAIT_ECONOMIC constant."""
        assert Trait.ECONOMIC.value == "TRAIT_ECONOMIC"

    def test_trait_cultural(self):
        """Test TRAIT_CULTURAL constant."""
        assert Trait.CULTURAL.value == "TRAIT_CULTURAL"

    def test_trait_military(self):
        """Test TRAIT_MILITARY constant."""
        assert Trait.MILITARY.value == "TRAIT_MILITARY"

    def test_all_traits_are_valid(self):
        """Test that all traits have string values."""
        for trait in Trait:
            assert isinstance(trait.value, str)
            assert trait.value.startswith("TRAIT_")


class TestUnitConstants:
    """Tests for Unit-related constants."""

    def test_unit_class_melee(self):
        """Test UNIT_CLASS_MELEE constant."""
        assert UnitClass.MELEE.value == "UNIT_CLASS_MELEE"

    def test_unit_class_ranged(self):
        """Test UNIT_CLASS_RANGED constant."""
        assert UnitClass.RANGED.value == "UNIT_CLASS_RANGED"

    def test_unit_movement_class_land(self):
        """Test UNIT_MOVEMENT_CLASS_LAND constant."""
        assert UnitMovementClass.LAND.value == "UNIT_MOVEMENT_CLASS_LAND"

    def test_unit_culture_unique(self):
        """Test UNIT_CULTURE_UNIQUE constant."""
        assert UnitCulture.UNIQUE.value == "UNIT_CULTURE_UNIQUE"

    def test_all_unit_classes_valid(self):
        """Test that all unit classes are valid."""
        assert len(UnitClass) >= 5
        for uc in UnitClass:
            assert isinstance(uc.value, str)


class TestConstructibleConstants:
    """Tests for Constructible-related constants."""

    def test_constructible_type_building(self):
        """Test CONSTRUCTIBLE_TYPE_TAG_BUILDING constant."""
        assert ConstructibleTypeTag.BUILDING.value == "CONSTRUCTIBLE_TYPE_TAG_BUILDING"

    def test_district_commercial_hub(self):
        """Test DISTRICT_COMMERCIAL_HUB constant."""
        assert District.COMMERCIAL_HUB.value == "DISTRICT_COMMERCIAL_HUB"

    def test_district_holy_site(self):
        """Test DISTRICT_HOLY_SITE constant."""
        assert District.HOLY_SITE.value == "DISTRICT_HOLY_SITE"

    def test_constructible_class_economic(self):
        """Test CONSTRUCTIBLE_CLASS_ECONOMIC constant."""
        assert ConstructibleClass.ECONOMIC.value == "CONSTRUCTIBLE_CLASS_ECONOMIC"


class TestYieldConstants:
    """Tests for Yield constants."""

    def test_yield_production(self):
        """Test YIELD_PRODUCTION constant."""
        assert Yield.PRODUCTION.value == "YIELD_PRODUCTION"

    def test_yield_gold(self):
        """Test YIELD_GOLD constant."""
        assert Yield.GOLD.value == "YIELD_GOLD"

    def test_yield_culture(self):
        """Test YIELD_CULTURE constant."""
        assert Yield.CULTURE.value == "YIELD_CULTURE"

    def test_yield_science(self):
        """Test YIELD_SCIENCE constant."""
        assert Yield.SCIENCE.value == "YIELD_SCIENCE"

    def test_yield_faith(self):
        """Test YIELD_FAITH constant."""
        assert Yield.FAITH.value == "YIELD_FAITH"

    def test_all_yields_valid(self):
        """Test that all yields are valid."""
        assert len(Yield) >= 10
        for yield_type in Yield:
            assert isinstance(yield_type.value, str)
            assert yield_type.value.startswith("YIELD_")


class TestAgeConstants:
    """Tests for Age constants."""

    def test_age_antiquity(self):
        """Test AGE_ANTIQUITY constant."""
        assert Age.ANTIQUITY.value == "AGE_ANTIQUITY"

    def test_age_classical(self):
        """Test AGE_CLASSICAL constant."""
        assert Age.CLASSICAL.value == "AGE_CLASSICAL"

    def test_age_industrial(self):
        """Test AGE_INDUSTRIAL constant."""
        assert Age.INDUSTRIAL.value == "AGE_INDUSTRIAL"

    def test_all_ages_valid(self):
        """Test that all ages are valid."""
        assert len(Age) >= 6


class TestActionGroupConstants:
    """Tests for ActionGroup constants."""

    def test_action_group_always(self):
        """Test ACTION_GROUP_ALWAYS constant."""
        assert ActionGroup.ALWAYS.value == "ACTION_GROUP_ALWAYS"

    def test_action_group_age_antiquity(self):
        """Test ACTION_GROUP_AGE_ANTIQUITY constant."""
        assert ActionGroup.AGE_ANTIQUITY.value == "ACTION_GROUP_AGE_ANTIQUITY"

    def test_action_group_action_update_database(self):
        """Test UpdateDatabase action."""
        assert ActionGroupAction.UPDATE_DATABASE.value == "UpdateDatabase"


class TestTerrainConstants:
    """Tests for Terrain constants."""

    def test_terrain_grass(self):
        """Test TERRAIN_GRASS constant."""
        assert Terrain.GRASS.value == "TERRAIN_GRASS"

    def test_terrain_ocean(self):
        """Test TERRAIN_OCEAN constant."""
        assert Terrain.OCEAN.value == "TERRAIN_OCEAN"

    def test_all_terrains_valid(self):
        """Test that all terrains are valid."""
        assert len(Terrain) >= 10


class TestBiomeConstants:
    """Tests for Biome constants."""

    def test_biome_grassland(self):
        """Test BIOME_GRASSLAND constant."""
        assert Biome.GRASSLAND.value == "BIOME_GRASSLAND"

    def test_biome_desert(self):
        """Test BIOME_DESERT constant."""
        assert Biome.DESERT.value == "BIOME_DESERT"


class TestFeatureConstants:
    """Tests for Feature constants."""

    def test_feature_forest(self):
        """Test FEATURE_FOREST constant."""
        assert Feature.FOREST.value == "FEATURE_FOREST"

    def test_feature_jungle(self):
        """Test FEATURE_JUNGLE constant."""
        assert Feature.JUNGLE.value == "FEATURE_JUNGLE"


class TestEffectConstants:
    """Tests for Effect constants."""

    def test_effect_unit_adjust_movement(self):
        """Test EFFECT_UNIT_ADJUST_MOVEMENT constant."""
        assert Effect.UNIT_ADJUST_MOVEMENT.value == "EFFECT_UNIT_ADJUST_MOVEMENT"

    def test_effect_building_adjust_yield(self):
        """Test EFFECT_BUILDING_ADJUST_YIELD constant."""
        assert Effect.BUILDING_ADJUST_YIELD.value == "EFFECT_BUILDING_ADJUST_YIELD"

    def test_all_effects_valid(self):
        """Test that all effects are valid."""
        assert len(Effect) >= 5


class TestRequirementConstants:
    """Tests for Requirement constants."""

    def test_requirement_unit_tag_matches(self):
        """Test REQUIREMENT_UNIT_TAG_MATCHES constant."""
        assert Requirement.UNIT_TAG_MATCHES.value == "REQUIREMENT_UNIT_TAG_MATCHES"

    def test_requirement_player_has_tech(self):
        """Test REQUIREMENT_PLAYER_HAS_TECH constant."""
        assert Requirement.PLAYER_HAS_TECH.value == "REQUIREMENT_PLAYER_HAS_TECH"

    def test_requirement_set_all(self):
        """Test REQUIREMENT_SET_ALL constant."""
        assert RequirementSet.ALL.value == "REQUIREMENT_SET_ALL"


class TestCollectionConstants:
    """Tests for Collection constants."""

    def test_collection_player_units(self):
        """Test COLLECTION_PLAYER_UNITS constant."""
        assert Collection.PLAYER_UNITS.value == "COLLECTION_PLAYER_UNITS"

    def test_collection_all_units(self):
        """Test COLLECTION_ALL_UNITS constant."""
        assert Collection.ALL_UNITS.value == "COLLECTION_ALL_UNITS"


class TestDisplayConstants:
    """Tests for Display-related constants."""

    def test_language_english(self):
        """Test LANGUAGE_ENGLISH constant."""
        assert Language.ENGLISH.value == "LANGUAGE_ENGLISH"

    def test_icon_unit_generic(self):
        """Test ICON_UNIT_GENERIC constant."""
        assert Icon.UNIT_GENERIC.value == "ICON_UNIT_GENERIC"


class TestDomainConstants:
    """Tests for Domain constants."""

    def test_domain_land(self):
        """Test DOMAIN_LAND constant."""
        assert Domain.LAND.value == "DOMAIN_LAND"

    def test_domain_sea(self):
        """Test DOMAIN_SEA constant."""
        assert Domain.SEA.value == "DOMAIN_SEA"

    def test_civilization_domain_political(self):
        """Test CIVILIZATION_DOMAIN_POLITICAL constant."""
        assert CivilizationDomain.POLITICAL.value == "CIVILIZATION_DOMAIN_POLITICAL"


class TestOtherConstants:
    """Tests for miscellaneous constants."""

    def test_plunder_gold(self):
        """Test PLUNDER_GOLD constant."""
        assert Plunder.GOLD.value == "PLUNDER_GOLD"

    def test_advisory_military(self):
        """Test ADVISORY_MILITARY constant."""
        assert Advisory.MILITARY.value == "ADVISORY_MILITARY"


class TestConstantIntegration:
    """Integration tests for constants."""

    def test_constants_in_builders_example(self):
        """Test using constants from example mods."""
        # Should be able to use constants directly
        trait = Trait.ECONOMIC
        unit_class = UnitClass.MELEE
        yield_type = Yield.PRODUCTION
        
        assert trait.value == "TRAIT_ECONOMIC"
        assert unit_class.value == "UNIT_CLASS_MELEE"
        assert yield_type.value == "YIELD_PRODUCTION"

    def test_enum_iteration(self):
        """Test iterating over enum values."""
        traits = list(Trait)
        assert len(traits) >= 6
        
        yields = list(Yield)
        assert len(yields) >= 10

    def test_enum_comparison(self):
        """Test comparing enum values."""
        assert Trait.ECONOMIC == Trait.ECONOMIC
        assert Trait.ECONOMIC != Trait.MILITARY

    def test_enum_name_access(self):
        """Test accessing enum names."""
        trait = Trait.ECONOMIC
        assert trait.name == "ECONOMIC"
        assert trait.value == "TRAIT_ECONOMIC"

    def test_all_constants_exported(self):
        """Test that all constants are properly exported."""
        import civ7_modding_tools.constants as const
        
        # Should be accessible as module attributes
        assert hasattr(const, "Trait")
        assert hasattr(const, "UnitClass")
        assert hasattr(const, "Yield")
        assert hasattr(const, "Age")
        assert hasattr(const, "Effect")
        assert hasattr(const, "Requirement")


class TestConstantValues:
    """Validation tests for constant values."""

    def test_no_duplicate_values(self):
        """Test that enum values are unique within each enum."""
        # Trait values should be unique
        trait_values = [t.value for t in Trait]
        assert len(trait_values) == len(set(trait_values))
        
        # Yield values should be unique
        yield_values = [y.value for y in Yield]
        assert len(yield_values) == len(set(yield_values))

    def test_constant_naming_conventions(self):
        """Test that constants follow naming conventions."""
        # Traits should be uppercase with underscores
        for trait in Trait:
            assert trait.value.isupper()
            assert "_" in trait.value
            
        # Units should be uppercase with underscores
        for unit_class in UnitClass:
            assert unit_class.value.isupper()
            assert "_" in unit_class.value

    def test_constant_type_consistency(self):
        """Test that all constant values are strings."""
        enum_classes = [
            Trait, TagTrait, UnitClass, UnitMovementClass, UnitCulture,
            ConstructibleTypeTag, ConstructibleClass, District,
            Yield, Resource, Age, ActionGroup, ActionGroupAction,
            Terrain, Biome, Feature, FeatureClass,
            Effect, Requirement, RequirementSet, Collection,
            Icon, Language, Domain, CivilizationDomain,
            Plunder, Advisory
        ]
        
        for enum_class in enum_classes:
            for member in enum_class:
                assert isinstance(member.value, str), \
                    f"{enum_class.__name__}.{member.name} value is not a string"
