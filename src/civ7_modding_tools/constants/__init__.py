"""Game constants for Civilization 7 mods."""

from enum import Enum


# ============================================================================
# CIVILIZATION & ENTITY TYPES
# ============================================================================


class Trait(Enum):
    """Civilization traits."""
    ECONOMIC = "TRAIT_ECONOMIC"
    CULTURAL = "TRAIT_CULTURAL"
    MILITARY = "TRAIT_MILITARY"
    DIPLOMATIC = "TRAIT_DIPLOMATIC"
    SCIENTIFIC = "TRAIT_SCIENTIFIC"
    RELIGIOUS = "TRAIT_RELIGIOUS"


class TagTrait(Enum):
    """Trait tags for categorization."""
    ECONOMIC = "TAG_TRAIT_ECONOMIC"
    CULTURAL = "TAG_TRAIT_CULTURAL"
    MILITARY = "TAG_TRAIT_MILITARY"
    DIPLOMATIC = "TAG_TRAIT_DIPLOMATIC"
    SCIENTIFIC = "TAG_TRAIT_SCIENTIFIC"
    RELIGIOUS = "TAG_TRAIT_RELIGIOUS"


# ============================================================================
# UNITS
# ============================================================================


class UnitClass(Enum):
    """Unit classifications."""
    MELEE = "UNIT_CLASS_MELEE"
    RANGED = "UNIT_CLASS_RANGED"
    SUPPORT = "UNIT_CLASS_SUPPORT"
    RECON = "UNIT_CLASS_RECON"
    HEAVY_CAVALRY = "UNIT_CLASS_HEAVY_CAVALRY"
    LIGHT_CAVALRY = "UNIT_CLASS_LIGHT_CAVALRY"
    SIEGE = "UNIT_CLASS_SIEGE"
    NAVAL_MELEE = "UNIT_CLASS_NAVAL_MELEE"
    NAVAL_RANGED = "UNIT_CLASS_NAVAL_RANGED"
    TRADER = "UNIT_CLASS_TRADER"
    RELIGIOUS = "UNIT_CLASS_RELIGIOUS"
    DIPLOMAT = "UNIT_CLASS_DIPLOMAT"
    SPY = "UNIT_CLASS_SPY"
    GOVERNOR = "UNIT_CLASS_GOVERNOR"


class UnitMovementClass(Enum):
    """Unit movement classifications."""
    LAND = "UNIT_MOVEMENT_CLASS_LAND"
    WATER = "UNIT_MOVEMENT_CLASS_WATER"
    AIR = "UNIT_MOVEMENT_CLASS_AIR"
    HOVER = "UNIT_MOVEMENT_CLASS_HOVER"


class UnitCulture(Enum):
    """Unit cultural classifications."""
    BARBARIAN = "UNIT_CULTURE_BARBARIAN"
    UNIQUE = "UNIT_CULTURE_UNIQUE"
    ELITE = "UNIT_CULTURE_ELITE"


# ============================================================================
# CONSTRUCTIBLES (BUILDINGS, IMPROVEMENTS, DISTRICTS)
# ============================================================================


class ConstructibleTypeTag(Enum):
    """Constructible type tags."""
    BUILDING = "CONSTRUCTIBLE_TYPE_TAG_BUILDING"
    IMPROVEMENT = "CONSTRUCTIBLE_TYPE_TAG_IMPROVEMENT"
    QUARTER = "CONSTRUCTIBLE_TYPE_TAG_QUARTER"
    UNIQUE_QUARTER = "CONSTRUCTIBLE_TYPE_TAG_UNIQUE_QUARTER"


class ConstructibleClass(Enum):
    """Constructible classifications."""
    ECONOMIC = "CONSTRUCTIBLE_CLASS_ECONOMIC"
    CULTURAL = "CONSTRUCTIBLE_CLASS_CULTURAL"
    MILITARY = "CONSTRUCTIBLE_CLASS_MILITARY"
    SCIENTIFIC = "CONSTRUCTIBLE_CLASS_SCIENTIFIC"
    RELIGIOUS = "CONSTRUCTIBLE_CLASS_RELIGIOUS"
    DIPLOMATIC = "CONSTRUCTIBLE_CLASS_DIPLOMATIC"


class District(Enum):
    """Districts for quarters."""
    COMMERCIAL_HUB = "DISTRICT_COMMERCIAL_HUB"
    HOLY_SITE = "DISTRICT_HOLY_SITE"
    CAMPUS = "DISTRICT_CAMPUS"
    ENCAMPMENT = "DISTRICT_ENCAMPMENT"
    THEATER_SQUARE = "DISTRICT_THEATER_SQUARE"
    HARBOR = "DISTRICT_HARBOR"
    GOVERNMENT_PLAZA = "DISTRICT_GOVERNMENT_PLAZA"
    AQUEDUCT = "DISTRICT_AQUEDUCT"
    SEASIDE_RESORT = "DISTRICT_SEASIDE_RESORT"
    INDUSTRIAL_ZONE = "DISTRICT_INDUSTRIAL_ZONE"
    DAM = "DISTRICT_DAM"
    WATER_SPORTS_COMPLEX = "DISTRICT_WATER_SPORTS_COMPLEX"


# ============================================================================
# RESOURCES & YIELDS
# ============================================================================


class Yield(Enum):
    """Resource yields."""
    PRODUCTION = "YIELD_PRODUCTION"
    GOLD = "YIELD_GOLD"
    CULTURE = "YIELD_CULTURE"
    SCIENCE = "YIELD_SCIENCE"
    FAITH = "YIELD_FAITH"
    GREAT_GENERAL_POINTS = "YIELD_GREAT_GENERAL_POINTS"
    GREAT_ARTIST_POINTS = "YIELD_GREAT_ARTIST_POINTS"
    GREAT_SCIENTIST_POINTS = "YIELD_GREAT_SCIENTIST_POINTS"
    GREAT_MERCHANT_POINTS = "YIELD_GREAT_MERCHANT_POINTS"
    GREAT_ENGINEER_POINTS = "YIELD_GREAT_ENGINEER_POINTS"
    GREAT_DIPLOMAT_POINTS = "YIELD_GREAT_DIPLOMAT_POINTS"
    HOUSING = "YIELD_HOUSING"
    AMENITY = "YIELD_AMENITY"
    LOYALTY = "YIELD_LOYALTY"
    TOURISM = "YIELD_TOURISM"


class Resource(Enum):
    """Game resources."""
    FOOD = "RESOURCE_FOOD"
    PRODUCTION = "RESOURCE_PRODUCTION"
    GOLD = "RESOURCE_GOLD"
    CULTURE = "RESOURCE_CULTURE"
    SCIENCE = "RESOURCE_SCIENCE"
    FAITH = "RESOURCE_FAITH"


# ============================================================================
# PROGRESSION & AGES
# ============================================================================


class Age(Enum):
    """Game ages/eras."""
    ANTIQUITY = "AGE_ANTIQUITY"
    CLASSICAL = "AGE_CLASSICAL"
    MEDIEVAL = "AGE_MEDIEVAL"
    RENAISSANCE = "AGE_RENAISSANCE"
    INDUSTRIAL = "AGE_INDUSTRIAL"
    MODERN = "AGE_MODERN"
    ATOMIC = "AGE_ATOMIC"
    INFORMATION = "AGE_INFORMATION"
    FUTURE = "AGE_FUTURE"


class ActionGroup(Enum):
    """Action groups for mod loading."""
    ALWAYS = "ACTION_GROUP_ALWAYS"
    AGE_ANTIQUITY = "ACTION_GROUP_AGE_ANTIQUITY"
    AGE_CLASSICAL = "ACTION_GROUP_AGE_CLASSICAL"
    AGE_MEDIEVAL = "ACTION_GROUP_AGE_MEDIEVAL"
    AGE_RENAISSANCE = "ACTION_GROUP_AGE_RENAISSANCE"
    AGE_INDUSTRIAL = "ACTION_GROUP_AGE_INDUSTRIAL"
    AGE_MODERN = "ACTION_GROUP_AGE_MODERN"
    AGE_ATOMIC = "ACTION_GROUP_AGE_ATOMIC"
    AGE_INFORMATION = "ACTION_GROUP_AGE_INFORMATION"
    AGE_FUTURE = "ACTION_GROUP_AGE_FUTURE"


class ActionGroupAction(Enum):
    """Action group actions."""
    UPDATE_DATABASE = "UpdateDatabase"
    LOAD_IMPORT = "LoadImport"
    UNLOAD_IMPORT = "UnloadImport"


# ============================================================================
# MAP & ENVIRONMENT
# ============================================================================


class Terrain(Enum):
    """Terrain types."""
    OCEAN = "TERRAIN_OCEAN"
    COAST = "TERRAIN_COAST"
    GRASS = "TERRAIN_GRASS"
    GRASS_HILL = "TERRAIN_GRASS_HILL"
    GRASS_MOUNTAIN = "TERRAIN_GRASS_MOUNTAIN"
    PLAINS = "TERRAIN_PLAINS"
    PLAINS_HILL = "TERRAIN_PLAINS_HILL"
    PLAINS_MOUNTAIN = "TERRAIN_PLAINS_MOUNTAIN"
    DESERT = "TERRAIN_DESERT"
    DESERT_HILL = "TERRAIN_DESERT_HILL"
    DESERT_MOUNTAIN = "TERRAIN_DESERT_MOUNTAIN"
    SNOW = "TERRAIN_SNOW"
    SNOW_HILL = "TERRAIN_SNOW_HILL"
    SNOW_MOUNTAIN = "TERRAIN_SNOW_MOUNTAIN"
    TUNDRA = "TERRAIN_TUNDRA"
    TUNDRA_HILL = "TERRAIN_TUNDRA_HILL"
    TUNDRA_MOUNTAIN = "TERRAIN_TUNDRA_MOUNTAIN"


class Biome(Enum):
    """Biome types."""
    GRASSLAND = "BIOME_GRASSLAND"
    PLAINS = "BIOME_PLAINS"
    DESERT = "BIOME_DESERT"
    TUNDRA = "BIOME_TUNDRA"
    SNOW = "BIOME_SNOW"
    TEMPERATE_FOREST = "BIOME_TEMPERATE_FOREST"
    TROPICAL_FOREST = "BIOME_TROPICAL_FOREST"
    BOREAL_FOREST = "BIOME_BOREAL_FOREST"
    COAST = "BIOME_COAST"
    OCEAN = "BIOME_OCEAN"


class Feature(Enum):
    """Map features."""
    FOREST = "FEATURE_FOREST"
    JUNGLE = "FEATURE_JUNGLE"
    MARSH = "FEATURE_MARSH"
    OASIS = "FEATURE_OASIS"
    RIVER = "FEATURE_RIVER"
    REEF = "FEATURE_REEF"
    FLOOD_PLAINS = "FEATURE_FLOOD_PLAINS"
    GEOTHERMAL = "FEATURE_GEOTHERMAL"
    VOLCANIC_SOIL = "FEATURE_VOLCANIC_SOIL"
    CLIFFS = "FEATURE_CLIFFS"


class FeatureClass(Enum):
    """Feature classifications."""
    FOREST = "FEATURE_CLASS_FOREST"
    JUNGLE = "FEATURE_CLASS_JUNGLE"
    WATER = "FEATURE_CLASS_WATER"
    MOUNTAIN = "FEATURE_CLASS_MOUNTAIN"
    FLOODPLAIN = "FEATURE_CLASS_FLOODPLAIN"


# ============================================================================
# GAME MECHANICS
# ============================================================================


class Effect(Enum):
    """Game effects and modifiers."""
    UNIT_ADJUST_MOVEMENT = "EFFECT_UNIT_ADJUST_MOVEMENT"
    UNIT_ADJUST_COMBAT_STRENGTH = "EFFECT_UNIT_ADJUST_COMBAT_STRENGTH"
    UNIT_ADJUST_RANGED_COMBAT_STRENGTH = "EFFECT_UNIT_ADJUST_RANGED_COMBAT_STRENGTH"
    BUILDING_ADJUST_YIELD = "EFFECT_BUILDING_ADJUST_YIELD"
    BUILDING_ADJUST_MAINTENANCE = "EFFECT_BUILDING_ADJUST_MAINTENANCE"
    CITY_ADJUST_GROWTH = "EFFECT_CITY_ADJUST_GROWTH"
    CITY_ADJUST_CULTURE = "EFFECT_CITY_ADJUST_CULTURE"
    CITY_ADJUST_SCIENCE = "EFFECT_CITY_ADJUST_SCIENCE"
    CITY_ADJUST_FAITH = "EFFECT_CITY_ADJUST_FAITH"
    CITY_ADJUST_LOYALTY = "EFFECT_CITY_ADJUST_LOYALTY"
    PLAYER_ADJUST_GREAT_PERSON_RATE = "EFFECT_PLAYER_ADJUST_GREAT_PERSON_RATE"
    PLAYER_ADJUST_TRADE_ROUTE_CAPACITY = "EFFECT_PLAYER_ADJUST_TRADE_ROUTE_CAPACITY"
    TECH_COST_ADJUSTMENT = "EFFECT_TECH_COST_ADJUSTMENT"
    CIVIC_COST_ADJUSTMENT = "EFFECT_CIVIC_COST_ADJUSTMENT"


class Requirement(Enum):
    """Game requirements/conditions."""
    UNIT_TAG_MATCHES = "REQUIREMENT_UNIT_TAG_MATCHES"
    UNIT_CLASS_MATCHES = "REQUIREMENT_UNIT_CLASS_MATCHES"
    PLAYER_HAS_TECH = "REQUIREMENT_PLAYER_HAS_TECH"
    PLAYER_HAS_CIVIC = "REQUIREMENT_PLAYER_HAS_CIVIC"
    PLAYER_IS_AGE = "REQUIREMENT_PLAYER_IS_AGE"
    GAME_ERA_IS = "REQUIREMENT_GAME_ERA_IS"
    BUILDING_EXISTS = "REQUIREMENT_BUILDING_EXISTS"
    TERRAIN_MATCHES = "REQUIREMENT_TERRAIN_MATCHES"
    DISTRICT_MATCHES = "REQUIREMENT_DISTRICT_MATCHES"
    FEATURE_MATCHES = "REQUIREMENT_FEATURE_MATCHES"


class RequirementSet(Enum):
    """Requirement set logic."""
    ALL = "REQUIREMENT_SET_ALL"
    ANY = "REQUIREMENT_SET_ANY"


class Collection(Enum):
    """Entity collections for modifiers."""
    PLAYER_UNITS = "COLLECTION_PLAYER_UNITS"
    PLAYER_BUILDINGS = "COLLECTION_PLAYER_BUILDINGS"
    PLAYER_IMPROVEMENTS = "COLLECTION_PLAYER_IMPROVEMENTS"
    PLAYER_CITIES = "COLLECTION_PLAYER_CITIES"
    ALL_UNITS = "COLLECTION_ALL_UNITS"
    ALL_BUILDINGS = "COLLECTION_ALL_BUILDINGS"
    ENEMY_UNITS = "COLLECTION_ENEMY_UNITS"
    UNIT_CLASS = "COLLECTION_UNIT_CLASS"


# ============================================================================
# DISPLAY & LOCALIZATION
# ============================================================================


class Icon(Enum):
    """Icon identifiers for UI display."""
    UNIT_GENERIC = "ICON_UNIT_GENERIC"
    BUILDING_GENERIC = "ICON_BUILDING_GENERIC"
    IMPROVEMENT_GENERIC = "ICON_IMPROVEMENT_GENERIC"
    TECH_GENERIC = "ICON_TECH_GENERIC"
    CIVIC_GENERIC = "ICON_CIVIC_GENERIC"


class Language(Enum):
    """Supported languages."""
    ENGLISH = "LANGUAGE_ENGLISH"
    FRENCH = "LANGUAGE_FRENCH"
    SPANISH = "LANGUAGE_SPANISH"
    GERMAN = "LANGUAGE_GERMAN"
    ITALIAN = "LANGUAGE_ITALIAN"
    PORTUGUESE = "LANGUAGE_PORTUGUESE"
    RUSSIAN = "LANGUAGE_RUSSIAN"
    CHINESE_SIMPLIFIED = "LANGUAGE_CHINESE_SIMPLIFIED"
    CHINESE_TRADITIONAL = "LANGUAGE_CHINESE_TRADITIONAL"
    JAPANESE = "LANGUAGE_JAPANESE"
    KOREAN = "LANGUAGE_KOREAN"


# ============================================================================
# DOMAIN & CIVILIZATION DOMAINS
# ============================================================================


class Domain(Enum):
    """Unit domains."""
    LAND = "DOMAIN_LAND"
    SEA = "DOMAIN_SEA"
    AIR = "DOMAIN_AIR"
    IMMATERIAL = "DOMAIN_IMMATERIAL"


class CivilizationDomain(Enum):
    """Civilization domain types."""
    POLITICAL = "CIVILIZATION_DOMAIN_POLITICAL"
    CULTURAL = "CIVILIZATION_DOMAIN_CULTURAL"
    MILITARY = "CIVILIZATION_DOMAIN_MILITARY"
    RELIGIOUS = "CIVILIZATION_DOMAIN_RELIGIOUS"
    SCIENTIFIC = "CIVILIZATION_DOMAIN_SCIENTIFIC"


# ============================================================================
# OTHER CATEGORIES
# ============================================================================


class Plunder(Enum):
    """Plunder types for conquered entities."""
    PRODUCTION = "PLUNDER_PRODUCTION"
    GOLD = "PLUNDER_GOLD"
    CULTURE = "PLUNDER_CULTURE"
    SCIENCE = "PLUNDER_SCIENCE"
    FAITH = "PLUNDER_FAITH"


class Advisory(Enum):
    """Advisory indicators."""
    ECONOMIC = "ADVISORY_ECONOMIC"
    MILITARY = "ADVISORY_MILITARY"
    DIPLOMATIC = "ADVISORY_DIPLOMATIC"
    SCIENTIFIC = "ADVISORY_SCIENTIFIC"
    CULTURAL = "ADVISORY_CULTURAL"
    RELIGIOUS = "ADVISORY_RELIGIOUS"


__all__ = [
    # Traits & Categories
    "Trait",
    "TagTrait",
    # Units
    "UnitClass",
    "UnitMovementClass",
    "UnitCulture",
    # Constructibles
    "ConstructibleTypeTag",
    "ConstructibleClass",
    "District",
    # Resources & Yields
    "Yield",
    "Resource",
    # Progression
    "Age",
    "ActionGroup",
    "ActionGroupAction",
    # Map
    "Terrain",
    "Biome",
    "Feature",
    "FeatureClass",
    # Mechanics
    "Effect",
    "Requirement",
    "RequirementSet",
    "Collection",
    # Display
    "Icon",
    "Language",
    # Domains
    "Domain",
    "CivilizationDomain",
    # Other
    "Plunder",
    "Advisory",
]
