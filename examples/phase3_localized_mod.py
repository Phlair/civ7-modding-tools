"""Phase 3 example: Using localizations for multi-language mod support."""

from civ7_modding_tools import Mod
from civ7_modding_tools.builders import (
    CivilizationBuilder,
    UnitBuilder,
    ConstructibleBuilder,
)
from civ7_modding_tools.localizations import (
    CivilizationLocalization,
    UnitLocalization,
    ConstructibleLocalization,
)


def main():
    """Create a mod with comprehensive localization support."""
    
    # Initialize the mod
    mod = Mod(
        mod_id="localized-rome",
        version="1.0.0",
        name="Localized Roman Mod",
        description="Demonstrates comprehensive localization support",
        authors="Civ7 Modding Tools",
    )
    
    # ============================================================================
    # CIVILIZATION WITH LOCALIZATIONS
    # ============================================================================
    
    rome_civ = CivilizationBuilder().fill({
        "civilization_type": "CIVILIZATION_ROME_LOCALIZED",
        "civilization": {
            "base_tourism": 3,
            "base_loyalty": 6,
            "legacy_modifier": True,
        },
        "civilization_traits": [
            "TRAIT_ECONOMIC",
            "TRAIT_DIPLOMATIC",
            "TRAIT_MILITARY",
        ],
        # Localization for English
        "localizations": [
            CivilizationLocalization(
                name="Rome",
                description="Masters of military might and organizational prowess",
                full_name="The Roman Empire",
                adjective="Roman",
                city_names=[
                    "Rome",
                    "Milan",
                    "Venice",
                    "Florence",
                    "Naples",
                    "Palermo",
                    "Genoa",
                    "Bologna",
                    "Ravenna",
                    "Siena",
                    "Pisa",
                    "Verona",
                ],
            ),
        ],
    })
    mod.add(rome_civ)
    
    # ============================================================================
    # UNITS WITH LOCALIZATIONS
    # ============================================================================
    
    # Roman Legion with localization
    legion = UnitBuilder().fill({
        "unit_type": "UNIT_ROMAN_LEGION",
        "unit": {
            "unit_class": "UNIT_CLASS_MELEE",
            "unit_movement_class": "UNIT_MOVEMENT_CLASS_LAND",
            "combat": 30,
            "ranged_combat": 0,
            "range": 0,
            "movement": 2,
            "era_type": "ERA_CLASSICAL",
        },
        "unit_costs": [
            {
                "yield_type": "YIELD_PRODUCTION",
                "amount": 65,
            },
        ],
        "localizations": [
            UnitLocalization(
                name="Legion",
                description="Elite Roman military unit, the backbone of Roman conquest",
                unique_name="Roman Legionnaire",
            ),
        ],
    })
    mod.add(legion)
    
    # Roman Archer with localization
    archer = UnitBuilder().fill({
        "unit_type": "UNIT_ROMAN_ARCHER",
        "unit": {
            "unit_class": "UNIT_CLASS_RANGED",
            "unit_movement_class": "UNIT_MOVEMENT_CLASS_LAND",
            "combat": 18,
            "ranged_combat": 35,
            "range": 2,
            "movement": 2,
            "era_type": "ERA_CLASSICAL",
        },
        "unit_costs": [
            {
                "yield_type": "YIELD_PRODUCTION",
                "amount": 50,
            },
        ],
        "localizations": [
            UnitLocalization(
                name="Archer",
                description="Ranged unit providing tactical flexibility in battle",
                unique_name="Roman Bowman",
            ),
        ],
    })
    mod.add(archer)
    
    # ============================================================================
    # BUILDINGS WITH LOCALIZATIONS
    # ============================================================================
    
    # Roman Forum with localization
    forum = ConstructibleBuilder().fill({
        "constructible_type": "BUILDING_ROMAN_FORUM",
        "constructible": {
            "cost": 150,
            "maintenance": 2,
            "district_type": "DISTRICT_COMMERCIAL_HUB",
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_GOLD",
                "amount": 5,
            },
            {
                "yield_type": "YIELD_CULTURE",
                "amount": 2,
            },
        ],
        "localizations": [
            ConstructibleLocalization(
                name="Roman Forum",
                description="A bustling public square where commerce and culture flourish",
                unique_name="Forum Romanum",
            ),
        ],
    })
    mod.add(forum)
    
    # Roman Temple with localization
    temple = ConstructibleBuilder().fill({
        "constructible_type": "BUILDING_ROMAN_TEMPLE",
        "constructible": {
            "cost": 120,
            "maintenance": 1,
            "district_type": "DISTRICT_HOLY_SITE",
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_FAITH",
                "amount": 4,
            },
            {
                "yield_type": "YIELD_CULTURE",
                "amount": 2,
            },
        ],
        "localizations": [
            ConstructibleLocalization(
                name="Roman Temple",
                description="A sacred sanctuary dedicated to the gods, inspiring spiritual devotion",
                unique_name="Temple of Jupiter",
            ),
        ],
    })
    mod.add(temple)
    
    # Roman Library with localization
    library = ConstructibleBuilder().fill({
        "constructible_type": "BUILDING_ROMAN_LIBRARY",
        "constructible": {
            "cost": 100,
            "maintenance": 1,
            "district_type": "DISTRICT_CAMPUS",
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_SCIENCE",
                "amount": 3,
            },
        ],
        "localizations": [
            ConstructibleLocalization(
                name="Roman Library",
                description="A repository of knowledge, preserving the wisdom of the ages",
                unique_name="Bibliotheca Romana",
            ),
        ],
    })
    mod.add(library)
    
    # Roman Aqueduct with localization
    aqueduct = ConstructibleBuilder().fill({
        "constructible_type": "IMPROVEMENT_ROMAN_AQUEDUCT",
        "constructible": {
            "cost": 80,
            "maintenance": 1,
            "improvement": True,
            "era_type": "ERA_CLASSICAL",
        },
        "yield_changes": [
            {
                "yield_type": "YIELD_PRODUCTION",
                "amount": 3,
            },
        ],
        "localizations": [
            ConstructibleLocalization(
                name="Roman Aqueduct",
                description="An engineering marvel that brings fresh water to distant lands",
                unique_name="Aqua Claudia",
            ),
        ],
    })
    mod.add(aqueduct)
    
    # ============================================================================
    # BUILD AND GENERATE MOD
    # ============================================================================
    
    print("Building localized mod: Roman Empire Expansion")
    print("")
    print("Mod Configuration:")
    print("  - ID: localized-rome")
    print("  - Version: 1.0.0")
    print("  - Builders: 7 (1 civilization, 2 units, 4 buildings)")
    print("  - Localizations: English (can be extended to other languages)")
    print("")
    
    mod.build("./dist", clear=True)
    
    print("✓ Mod built successfully!")
    print("✓ Output: ./dist/")
    print(f"✓ Files: {sum(len(b.build()) for b in mod.builders)} output files")
    print("")
    print("Features:")
    print("  ✓ Civilization with 3 traits and 12 city names")
    print("  ✓ 2 unique units with combat specs")
    print("  ✓ 4 buildings with yield modifiers")
    print("  ✓ Full localization metadata for display names and descriptions")
    print("")
    print("Next: Translate localizations to other languages by adding")
    print("additional localization objects with translated text!")


if __name__ == "__main__":
    main()
