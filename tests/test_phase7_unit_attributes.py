"""Phase 7: Unit attribute enhancements tests.

Tests for additional unit XML attributes in UnitBuilder, including
movement modifiers, combat properties, and special abilities.
"""

import pytest
from civ7_modding_tools.builders import UnitBuilder
from civ7_modding_tools.nodes import UnitNode, UnitStatNode
from civ7_modding_tools.files import XmlFile


class TestUnitAttributeEnhancements:
    """Test enhanced unit attributes in UnitBuilder."""

    def test_unit_builder_with_movement_range(self):
        """Test unit can have custom movement range."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_RANGER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_RANGER",
            "movement_range": 3,
        }
        builder.localizations = [{"name": "Gondor Ranger"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
        db = xml["Database"]
        assert "Units" in db
        units = db["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "3"

    def test_unit_builder_with_power_attribute(self):
        """Test unit can have power (combat strength)."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_WARRIOR"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_WARRIOR",
            "power": 45,
        }
        builder.localizations = [{"name": "Gondor Warrior"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["Power"] == "45"

    def test_unit_builder_with_ranged_power(self):
        """Test unit can have ranged combat power."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_ARCHER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_ARCHER",
            "ranged_power": 35,
        }
        builder.localizations = [{"name": "Gondor Archer"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["RangedPower"] == "35"

    def test_unit_builder_with_ranged_range(self):
        """Test unit can have ranged combat range."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_BALLISTA"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_BALLISTA",
            "ranged_range": 2,
        }
        builder.localizations = [{"name": "Gondor Ballista"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["RangedRange"] == "2"

    def test_unit_builder_with_multiple_enhanced_attributes(self):
        """Test unit with multiple enhanced attributes."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_KNIGHT"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_KNIGHT",
            "movement_range": 4,
            "power": 50,
            "ranged_power": 25,
        }
        builder.localizations = [{"name": "Gondor Knight"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "4"
        assert attrs["Power"] == "50"
        assert attrs["RangedPower"] == "25"

    def test_unit_builder_with_origin_boost(self):
        """Test unit can have origin boost for starting era."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_SOLDIER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_SOLDIER",
            "origin_boost_modulus": 10,
        }
        builder.localizations = [{"name": "Gondor Soldier"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["OriginBoostModulus"] == "10"

    def test_unit_builder_enhanced_attributes_with_fill(self):
        """Test enhanced attributes via fill() method."""
        builder = UnitBuilder().fill({
            "unit_type": "UNIT_GONDOR_ELITE",
            "unit": {
                "unit_type": "UNIT_GONDOR_ELITE",
                "movement_range": 5,
                "power": 60,
                "ranged_power": 40,
                "ranged_range": 2,
                "origin_boost_modulus": 15,
            },
            "localizations": [{"name": "Gondor Elite"}],
        })

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "5"
        assert attrs["Power"] == "60"
        assert attrs["RangedPower"] == "40"
        assert attrs["RangedRange"] == "2"
        assert attrs["OriginBoostModulus"] == "15"

    def test_unit_builder_enhanced_attributes_optional(self):
        """Test enhanced attributes are optional (backward compatible)."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_ROME_LEGIONNAIRE"
        builder.unit = {
            "unit_type": "UNIT_ROME_LEGIONNAIRE",
        }
        builder.localizations = [{"name": "Roman Legionnaire"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # Should still generate valid unit without enhanced attributes
        units = xml["Database"]["Units"]
        assert len(units if isinstance(units, list) else [units]) >= 1


class TestCarthageUnitPattern:
    """Test that enhanced attributes match Carthage unit patterns."""

    def test_carthage_naval_unit_attributes(self):
        """Test naval unit matches Carthage pattern."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_CARTHAGE_QUINQUEREME"
        builder.unit = {
            "unit_type": "UNIT_CARTHAGE_QUINQUEREME",
            "movement_range": 3,
            "power": 40,
            "ranged_power": 30,
            "ranged_range": 1,
        }
        builder.localizations = [{"name": "Carthaginian Quinquereme"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "3"
        assert attrs["Power"] == "40"
        assert attrs["RangedPower"] == "30"
        assert attrs["RangedRange"] == "1"

    def test_carthage_melee_unit_pattern(self):
        """Test melee unit pattern."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_CARTHAGE_HOPLITE"
        builder.unit = {
            "unit_type": "UNIT_CARTHAGE_HOPLITE",
            "movement_range": 2,
            "power": 35,
        }
        builder.localizations = [{"name": "Carthaginian Hoplite"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "2"
        assert attrs["Power"] == "35"


class TestUnitAttributeIntegration:
    """Test enhanced attributes integrated with other unit features."""

    def test_unit_with_stats_and_enhanced_attributes(self):
        """Test enhanced attributes work with unit stats."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_CAPTAIN"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_CAPTAIN",
            "movement_range": 4,
            "power": 55,
        }
        builder.unit_stats = [
            {"stat_type": "STAT_EXPERIENCE", "stat_value": 2}
        ]
        builder.localizations = [{"name": "Gondor Captain"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "Units" in db
        assert "Unit_Stats" in db

    def test_unit_with_costs_and_enhanced_attributes(self):
        """Test enhanced attributes work with unit costs."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_GUARD"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_GUARD",
            "movement_range": 3,
            "power": 45,
        }
        builder.unit_costs = [
            {"yield_type": "YIELD_PRODUCTION", "cost": 100}
        ]
        builder.localizations = [{"name": "Gondor Guard"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "Units" in db
        assert "Unit_Costs" in db

    def test_unit_builder_fluent_api_with_enhanced_attributes(self):
        """Test fluent API works with enhanced attributes."""
        builder = (
            UnitBuilder()
            .fill({
                "unit_type": "UNIT_GONDOR_LORD",
                "unit": {
                    "unit_type": "UNIT_GONDOR_LORD",
                    "movement_range": 5,
                    "power": 70,
                },
                "localizations": [{"name": "Gondor Lord"}],
            })
        )

        files = builder.build()
        assert len(files) > 0

        # Verify current.xml was generated
        current = next((f for f in files if f.name == "current.xml"), None)
        assert current is not None

    def test_unit_with_all_enhanced_attributes_and_costs(self):
        """Test comprehensive unit with all enhancements."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_SUPREME"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_SUPREME",
            "movement_range": 6,
            "power": 80,
            "ranged_power": 50,
            "ranged_range": 2,
            "origin_boost_modulus": 20,
        }
        builder.unit_costs = [
            {"yield_type": "YIELD_PRODUCTION", "cost": 500},
            {"yield_type": "YIELD_GOLD", "cost": 100}
        ]
        builder.unit_stats = [
            {"stat_type": "STAT_EXPERIENCE", "stat_value": 5}
        ]
        builder.localizations = [{"name": "Gondor Supreme"}]

        files = builder.build()
        assert len(files) > 0


class TestUnitAttributeEdgeCases:
    """Test edge cases for enhanced unit attributes."""

    def test_unit_with_zero_movement_range(self):
        """Test unit with zero movement range (valid for ranged units)."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_TOWER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_TOWER",
            "movement_range": 0,
            "ranged_power": 60,
            "ranged_range": 3,
        }
        builder.localizations = [{"name": "Gondor Tower"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "0"

    def test_unit_with_high_ranged_range(self):
        """Test unit with extended ranged range."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_CATAPULT"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_CATAPULT",
            "ranged_power": 45,
            "ranged_range": 4,
        }
        builder.localizations = [{"name": "Gondor Catapult"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["RangedRange"] == "4"

    def test_unit_with_partial_enhanced_attributes(self):
        """Test unit with only some enhanced attributes specified."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_ARCHER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_ARCHER",
            "movement_range": 3,
            "ranged_power": 28,
        }
        builder.localizations = [{"name": "Gondor Archer"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["MovementRange"] == "3"
        assert attrs["RangedPower"] == "28"
        # RangedRange should not be present if not specified
        assert "RangedRange" not in attrs or attrs.get("RangedRange") is None

    def test_unit_empty_enhanced_attributes(self):
        """Test unit with no enhanced attributes specified."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_ROME_CITIZEN"
        builder.unit = {
            "unit_type": "UNIT_ROME_CITIZEN",
        }
        builder.localizations = [{"name": "Roman Citizen"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # Should still generate valid unit
        units = xml["Database"]["Units"]
        assert len(units if isinstance(units, list) else [units]) >= 1

    def test_unit_builder_with_multiple_units_enhanced(self):
        """Test multiple units with various enhanced attributes."""
        builder1 = UnitBuilder().fill({
            "unit_type": "UNIT_A",
            "unit": {"unit_type": "UNIT_A", "movement_range": 2, "power": 30},
            "localizations": [{"name": "Unit A"}],
        })

        builder2 = UnitBuilder().fill({
            "unit_type": "UNIT_B",
            "unit": {"unit_type": "UNIT_B", "movement_range": 4, "power": 50},
            "localizations": [{"name": "Unit B"}],
        })

        files1 = builder1.build()
        files2 = builder2.build()

        assert len(files1) > 0
        assert len(files2) > 0


class TestUnitAttributeTypes:
    """Test correct type handling for enhanced attributes."""

    def test_movement_range_integer_serialization(self):
        """Test movement range serializes as integer."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_TEST"
        builder.unit = {
            "unit_type": "UNIT_TEST",
            "movement_range": 3,
        }
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        # Should be serialized as string "3"
        assert attrs["MovementRange"] == "3"
        assert isinstance(attrs["MovementRange"], str)

    def test_power_integer_serialization(self):
        """Test power serializes as integer."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_TEST"
        builder.unit = {
            "unit_type": "UNIT_TEST",
            "power": 45,
        }
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["Power"] == "45"
        assert isinstance(attrs["Power"], str)

    def test_ranged_attributes_serialization(self):
        """Test ranged attributes serialize correctly."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_TEST"
        builder.unit = {
            "unit_type": "UNIT_TEST",
            "ranged_power": 35,
            "ranged_range": 2,
        }
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["RangedPower"] == "35"
        assert attrs["RangedRange"] == "2"


class TestNewUnitProperties:
    """Test newly added unit properties."""

    def test_unit_builder_with_tier(self):
        """Test unit can have tier property."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_SPEARMAN"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_SPEARMAN",
            "tier": 2,
        }
        builder.localizations = [{"name": "Gondor Spearman"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["Tier"] == "2"

    def test_unit_builder_with_maintenance(self):
        """Test unit can have maintenance (upkeep) property."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_CAVALRY"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_CAVALRY",
            "maintenance": 4,
        }
        builder.localizations = [{"name": "Gondor Cavalry"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["Maintenance"] == "4"

    def test_unit_builder_with_zone_of_control(self):
        """Test unit can have zone of control property."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_WARRIOR"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_WARRIOR",
            "zone_of_control": True,
        }
        builder.localizations = [{"name": "Gondor Warrior"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["ZoneOfControl"] == "true"

    def test_unit_builder_with_cost_progression(self):
        """Test unit can have cost progression properties."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_SETTLER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_SETTLER",
            "cost_progression_model": "COST_PROGRESSION_NUM_SETTLEMENTS",
            "cost_progression_param1": 30,
        }
        builder.localizations = [{"name": "Gondor Settler"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["CostProgressionModel"] == "COST_PROGRESSION_NUM_SETTLEMENTS"
        assert attrs["CostProgressionParam1"] == "30"

    def test_unit_builder_with_capability_flags(self):
        """Test unit can have capability flags."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_GREATPERSON"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_GREATPERSON",
            "can_train": False,
            "can_purchase": False,
            "can_earn_experience": False,
        }
        builder.localizations = [{"name": "Great Person"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["CanTrain"] == "false"
        assert attrs["CanPurchase"] == "false"
        assert attrs["CanEarnExperience"] == "false"

    def test_unit_builder_with_special_capabilities(self):
        """Test unit can have special capabilities like found_city."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_COLONIST"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_COLONIST",
            "found_city": True,
            "prereq_population": 5,
        }
        builder.localizations = [{"name": "Gondor Colonist"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["FoundCity"] == "true"
        assert attrs["PrereqPopulation"] == "5"

    def test_unit_builder_with_promotion_class(self):
        """Test unit can have promotion class."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_COMMANDER"
        builder.unit = {
            "unit_type": "UNIT_GONDOR_COMMANDER",
            "promotion_class": "PROMOTION_CLASS_LAND_COMMANDER",
        }
        builder.localizations = [{"name": "Gondor Commander"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        units = xml["Database"]["Units"]
        if isinstance(units, list):
            unit_row = units[0]
        else:
            unit_row = units

        attrs = unit_row["_attrs"]
        assert attrs["PromotionClass"] == "PROMOTION_CLASS_LAND_COMMANDER"

    def test_unit_builder_with_upgrade(self):
        """Test unit can have upgrade path."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_WARRIOR"
        builder.unit_upgrade = {
            "upgrade_unit": "UNIT_GONDOR_SWORDSMAN"
        }
        builder.localizations = [{"name": "Gondor Warrior"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
        db = xml["Database"]
        assert "UnitUpgrades" in db
        upgrades = db["UnitUpgrades"]
        
        if isinstance(upgrades, list):
            upgrade_row = upgrades[0]
        else:
            upgrade_row = upgrades

        attrs = upgrade_row["_attrs"]
        assert attrs["Unit"] == "UNIT_GONDOR_WARRIOR"
        assert attrs["UpgradeUnit"] == "UNIT_GONDOR_SWORDSMAN"

    def test_unit_builder_with_advisory(self):
        """Test unit can have advisory classification."""
        builder = UnitBuilder()
        builder.unit_type = "UNIT_GONDOR_SCOUT"
        builder.unit_advisories = [{
            "advisory_class_type": "ADVISORY_CLASS_MILITARY"
        }]
        builder.localizations = [{"name": "Gondor Scout"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
        db = xml["Database"]
        assert "Unit_Advisories" in db
        advisories = db["Unit_Advisories"]
        
        if isinstance(advisories, list):
            advisory_row = advisories[0]
        else:
            advisory_row = advisories

        attrs = advisory_row["_attrs"]
        assert attrs["UnitType"] == "UNIT_GONDOR_SCOUT"
        assert attrs["AdvisoryClassType"] == "ADVISORY_CLASS_MILITARY"
