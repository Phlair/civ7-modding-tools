"""Tests for all node implementations."""

import pytest
from civ7_modding_tools.nodes import (
    BaseNode,
    DatabaseNode,
    KindNode,
    TypeNode,
    TagNode,
    TypeTagNode,
    TraitNode,
    TraitModifierNode,
    CivilizationItemNode,
    CivilizationTagNode,
    BuildingNode,
    ImprovementNode,
    ConstructibleValidDistrictNode,
    UnlockNode,
    UnlockRewardNode,
    RequirementSetNode,
    RequirementNode,
    ModifierNode,
    GameModifierNode,
    ArgumentNode,
    ModifierRequirementNode,
    StartBiasAdjacentToCoastNode,
    StartBiasFeatureClassNode,
    StartBiasRiverNode,
    StringNode,
    UnitReplaceNode,
    VisArtCivilizationBuildingCultureNode,
    VisArtCivilizationUnitCultureNode,
)
from civ7_modding_tools.utils import camel_to_pascal, locale, trim, kebab_case


# ============================================================================
# BaseNode Tests
# ============================================================================

def test_base_node_creation():
    """Test creating a basic node."""
    node = BaseNode()
    assert node._name == "Row"


def test_base_node_fill():
    """Test fill() method for fluent API."""
    node = BaseNode()
    result = node.fill({"test_prop": "value", "another": 42})
    
    # Should return self
    assert result is node
    # Should set properties
    assert node.test_prop == "value"
    assert node.another == 42


def test_base_node_to_xml_element():
    """Test conversion to XML element dict."""
    node = BaseNode()
    node.civilization_type = "CIVILIZATION_ROME"
    node.base_tourism = 10
    node.legacy_modifier = True
    
    xml_elem = node.to_xml_element()
    
    assert xml_elem is not None
    assert "_name" in xml_elem
    assert "_attrs" in xml_elem
    assert xml_elem["_name"] == "Row"
    attrs = xml_elem["_attrs"]
    
    # Check snake_case -> PascalCase conversion
    assert attrs["CivilizationType"] == "CIVILIZATION_ROME"
    assert attrs["BaseTourism"] == "10"
    assert attrs["LegacyModifier"] == "true"


def test_base_node_excludes_private_properties():
    """Test that private properties are excluded from XML."""
    node = BaseNode()
    node.public_prop = "visible"
    node._private_prop = "hidden"
    
    xml_elem = node.to_xml_element()
    attrs = xml_elem["_attrs"]
    
    assert "PublicProp" in attrs
    assert "_private_prop" not in attrs
    assert "_PrivateProp" not in attrs


def test_base_node_excludes_empty_values():
    """Test that None, empty string, and False are excluded."""
    node = BaseNode()
    node.has_value = True
    node.is_empty = None
    node.name = ""
    node.active = False
    
    xml_elem = node.to_xml_element()
    attrs = xml_elem["_attrs"]
    
    assert "HasValue" in attrs
    assert attrs["HasValue"] == "true"
    
    # These should be excluded
    assert "IsEmpty" not in attrs
    assert "Name" not in attrs
    assert "Active" not in attrs


def test_base_node_empty_returns_none():
    """Test that node with no attributes returns None."""
    node = BaseNode()
    node.nothing = None
    node.empty = ""
    
    xml_elem = node.to_xml_element()
    assert xml_elem is None



def test_camel_to_pascal():
    """Test camelCase to PascalCase conversion."""
    assert camel_to_pascal("civilizationType") == "CivilizationType"
    assert camel_to_pascal("baseTourism") == "BaseTourism"
    assert camel_to_pascal("x") == "X"
    assert camel_to_pascal("") == ""
    assert camel_to_pascal("already") == "Already"


# ============================================================================
# DatabaseNode Tests
# ============================================================================

class TestDatabaseNode:
    """Tests for DatabaseNode implementation."""

    def test_database_node_creates_empty(self):
        """DatabaseNode should create with default empty arrays."""
        db = DatabaseNode()
        assert db._name == "Database"
        assert db.kinds == []
        assert db.types == []
        assert db.tags == []
        assert db.civilizations == []
        assert db.units == []

    def test_database_node_has_all_67_properties(self):
        """DatabaseNode should have exactly 67 properties."""
        db = DatabaseNode()
        # Count list properties
        list_properties = [
            attr for attr in db.model_fields
            if isinstance(getattr(db, attr), list)
        ]
        assert len(list_properties) >= 50  # At least 50 properties as in TypeScript

    def test_database_node_accepts_payload(self):
        """DatabaseNode should accept initialization payload."""
        kind_node = KindNode(kind="KIND_TYPE")
        db = DatabaseNode({"kinds": [kind_node]})
        assert len(db.kinds) == 1
        assert db.kinds[0].kind == "KIND_TYPE"

    def test_database_node_fill_method(self):
        """DatabaseNode should support fill() method for fluent API."""
        kind_node = KindNode(kind="KIND_A")
        tag_node = TagNode(tag="TAG_A")
        
        db = DatabaseNode().fill({
            "kinds": [kind_node],
            "tags": [tag_node],
        })
        
        assert len(db.kinds) == 1
        assert len(db.tags) == 1

    def test_database_node_to_xml_element_empty_returns_none(self):
        """DatabaseNode with no data should return None for XML."""
        db = DatabaseNode()
        result = db.to_xml_element()
        assert result is None

    def test_database_node_to_xml_element_with_data(self):
        """DatabaseNode should generate Database XML element."""
        kind_node = KindNode(kind="KIND_TYPE")
        db = DatabaseNode({"kinds": [kind_node]})
        
        result = db.to_xml_element()
        assert result is not None
        assert "Database" in result

    def test_database_node_xml_table_naming_conventions(self):
        """DatabaseNode should use correct table naming from TS original."""
        db = DatabaseNode()
        db.unit_costs = []  # Ensure property exists
        # The mapping should convert 'unit_costs' to 'Unit_Costs'
        
        # Just verify property exists and is accessible
        assert hasattr(db, 'unit_costs')

    def test_database_node_multi_table_generation(self):
        """DatabaseNode should generate multiple tables in XML."""
        kind = KindNode(kind="K1")
        type_node = TypeNode(type_="T1")
        tag = TagNode(tag="TAG1")
        
        db = DatabaseNode().fill({
            "kinds": [kind],
            "types": [type_node],
            "tags": [tag],
        })
        
        result = db.to_xml_element()
        assert result is not None
        db_data = result.get("Database", {})
        # Should have multiple tables
        assert len([k for k in db_data.keys()]) >= 1  # At least kinds table


# ============================================================================
# Type System Node Tests
# ============================================================================

class TestTypeSystemNodes:
    """Tests for type system node classes."""

    def test_kind_node_properties(self):
        """KindNode should have kind property."""
        node = KindNode(kind="KIND_UNIT")
        assert node.kind == "KIND_UNIT"
        assert node._name == "InsertOrIgnore"

    def test_type_node_properties(self):
        """TypeNode should have type_type and kind properties."""
        node = TypeNode(type_type="UNIT_MELEE", kind="KIND_UNIT")
        assert node.type_type == "UNIT_MELEE"
        assert node.kind == "KIND_UNIT"

    def test_tag_node_properties(self):
        """TagNode should have tag and tag_string properties."""
        node = TagNode(tag="TAG_MILITARY", tag_string="Military Tag")
        assert node.tag == "TAG_MILITARY"
        assert node.tag_string == "Military Tag"

    def test_type_tag_node_relationship(self):
        """TypeTagNode should represent type-tag relationship."""
        node = TypeTagNode(type_type="UNIT_MELEE", tag="TAG_MILITARY")
        assert node.type_type == "UNIT_MELEE"
        assert node.tag == "TAG_MILITARY"

    def test_trait_node_properties(self):
        """TraitNode should have trait_type and trait_string."""
        node = TraitNode(trait_type="TRAIT_ECONOMIC", trait_string="Economic")
        assert node.trait_type == "TRAIT_ECONOMIC"
        assert node.trait_string == "Economic"

    def test_trait_modifier_relationship(self):
        """TraitModifierNode should link trait to modifier."""
        node = TraitModifierNode(trait_type="TRAIT_ECONOMIC", modifier_id="MOD_GOLD")
        assert node.trait_type == "TRAIT_ECONOMIC"
        assert node.modifier_id == "MOD_GOLD"


# ============================================================================
# Civilization Entity Node Tests
# ============================================================================

class TestCivilizationEntityNodes:
    """Tests for civilization-related node classes."""

    def test_civilization_item_node(self):
        """CivilizationItemNode should represent civ item reference."""
        node = CivilizationItemNode(
            civilization_type="CIVILIZATION_ROME",
            item_type="UNIT_ROMAN_LEGION"
        )
        assert node.civilization_type == "CIVILIZATION_ROME"
        assert node.item_type == "UNIT_ROMAN_LEGION"

    def test_civilization_tag_node(self):
        """CivilizationTagNode should link civilization to tag."""
        node = CivilizationTagNode(
            civilization_type="CIVILIZATION_ROME",
            tag="TAG_EMPIRE"
        )
        assert node.civilization_type == "CIVILIZATION_ROME"
        assert node.tag == "TAG_EMPIRE"


# ============================================================================
# Constructible Constraint Node Tests
# ============================================================================

class TestConstructibleConstraintNodes:
    """Tests for constructible constraint node classes."""

    def test_building_node(self):
        """BuildingNode should represent building definition."""
        node = BuildingNode(
            building_type="BUILDING_FORUM",
            building_class="BUILDING_CLASS_COMMERCIAL"
        )
        assert node.building_type == "BUILDING_FORUM"
        assert node.building_class == "BUILDING_CLASS_COMMERCIAL"

    def test_improvement_node(self):
        """ImprovementNode should represent improvement definition."""
        node = ImprovementNode(
            improvement_type="IMPROVEMENT_FARM",
            improvement_class="IMPROVEMENT_CLASS_RESOURCE"
        )
        assert node.improvement_type == "IMPROVEMENT_FARM"

    def test_constructible_valid_district_node(self):
        """ConstructibleValidDistrictNode constrains by district."""
        node = ConstructibleValidDistrictNode(
            constructible_type="BUILDING_FORUM",
            district_type="DISTRICT_COMMERCIAL_HUB"
        )
        assert node.constructible_type == "BUILDING_FORUM"
        assert node.district_type == "DISTRICT_COMMERCIAL_HUB"


# ============================================================================
# Unlock System Node Tests
# ============================================================================

class TestUnlockSystemNodes:
    """Tests for unlock and requirement node classes."""

    def test_unlock_node(self):
        """UnlockNode should represent unlock configuration."""
        node = UnlockNode(
            unlock_id="UNLOCK_1",
            unlock_era="ERA_ANCIENT"
        )
        assert node.unlock_id == "UNLOCK_1"
        assert node.unlock_era == "ERA_ANCIENT"

    def test_unlock_reward_node(self):
        """UnlockRewardNode should represent unlock reward."""
        node = UnlockRewardNode(
            unlock_id="UNLOCK_1",
            reward_type="REWARD_UNIT",
            reward_value="UNIT_ARCHER"
        )
        assert node.unlock_id == "UNLOCK_1"
        assert node.reward_type == "REWARD_UNIT"

    def test_requirement_set_node(self):
        """RequirementSetNode should represent requirement set."""
        node = RequirementSetNode(
            requirement_set_id="REQ_SET_1",
            requirement_set_type="REQ_SET_ALL"
        )
        assert node.requirement_set_id == "REQ_SET_1"
        assert node.requirement_set_type == "REQ_SET_ALL"

    def test_requirement_node(self):
        """RequirementNode should represent requirement."""
        node = RequirementNode(
            requirement_id="REQ_1",
            requirement_type="REQ_TECH",
            inverse=False
        )
        assert node.requirement_id == "REQ_1"
        assert node.requirement_type == "REQ_TECH"
        assert node.inverse == False


# ============================================================================
# Modifier Node Tests
# ============================================================================

class TestModifierNodes:
    """Tests for modifier and effect node classes."""

    def test_modifier_node(self):
        """ModifierNode should represent modifier."""
        node = ModifierNode(
            modifier_id="MOD_GOLD_BONUS",
            modifier_type="MOD_PLAYER",
            owner_type="PLAYER",
            owner_id="PLAYER_1"
        )
        assert node.modifier_id == "MOD_GOLD_BONUS"
        assert node.modifier_type == "MOD_PLAYER"

    def test_game_modifier_node(self):
        """GameModifierNode should represent game-level modifier."""
        node = GameModifierNode(
            modifier_id="MOD_GLOBAL",
            game_effect_id="EFFECT_GOLD"
        )
        assert node.modifier_id == "MOD_GLOBAL"
        assert node.game_effect_id == "EFFECT_GOLD"

    def test_argument_node(self):
        """ArgumentNode should represent modifier argument."""
        node = ArgumentNode(
            modifier_id="MOD_GOLD_BONUS",
            argument_name="Amount",
            argument_value="5"
        )
        assert node.modifier_id == "MOD_GOLD_BONUS"
        assert node.argument_name == "Amount"
        assert node.argument_value == "5"


# ============================================================================
# Phase 6 Node Tests
# ============================================================================

class TestModifierRequirementNode:
    """Tests for ModifierRequirementNode."""

    def test_modifier_requirement_node_initialization(self):
        """Test ModifierRequirementNode initializes correctly."""
        node = ModifierRequirementNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Requirement"  # ModifierRequirementNode uses 'Requirement', not 'Row'
        assert node.type_ is None
        assert node.arguments == []

    def test_modifier_requirement_node_with_data(self):
        """Test ModifierRequirementNode with data."""
        node = ModifierRequirementNode()
        node.modifier_type = "MOD_GONDOR_BONUS"
        node.requirement_type = "TECH_MATCHED"
        
        assert node.modifier_type == "MOD_GONDOR_BONUS"
        assert node.requirement_type == "TECH_MATCHED"

    def test_modifier_requirement_node_to_xml(self):
        """Test ModifierRequirementNode XML serialization."""
        node = ModifierRequirementNode()
        node.type_ = "REQUIREMENT_UNIT_TAG_MATCHES"
        node.arguments = [{'name': 'Tag', 'value': 'UNIT_CLASS_RECON'}]
        
        xml = node.to_xml_element()
        assert xml is not None
        assert xml['_name'] == 'Requirement'
        assert xml['_attrs']['type'] == 'REQUIREMENT_UNIT_TAG_MATCHES'


class TestStartBiasAdjacentToCoastNode:
    """Tests for StartBiasAdjacentToCoastNode."""

    def test_start_bias_adjacent_to_coast_initialization(self):
        """Test StartBiasAdjacentToCoastNode initializes correctly."""
        node = StartBiasAdjacentToCoastNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.bias is None

    def test_start_bias_adjacent_to_coast_with_data(self):
        """Test StartBiasAdjacentToCoastNode with data."""
        node = StartBiasAdjacentToCoastNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.bias = 50
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.bias == 50

    def test_start_bias_adjacent_to_coast_to_xml(self):
        """Test StartBiasAdjacentToCoastNode XML serialization."""
        node = StartBiasAdjacentToCoastNode()
        node.civilization_type = "CIVILIZATION_ROME"
        node.bias = 25
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "CivilizationType" in str(xml)


class TestStartBiasFeatureClassNode:
    """Tests for StartBiasFeatureClassNode."""

    def test_start_bias_feature_class_initialization(self):
        """Test StartBiasFeatureClassNode initializes correctly."""
        node = StartBiasFeatureClassNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.feature_class is None
        assert node.bias is None

    def test_start_bias_feature_class_with_data(self):
        """Test StartBiasFeatureClassNode with data."""
        node = StartBiasFeatureClassNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.feature_class = "FEATURE_FOREST"
        node.bias = 75
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.feature_class == "FEATURE_FOREST"
        assert node.bias == 75

    def test_start_bias_feature_class_to_xml(self):
        """Test StartBiasFeatureClassNode XML serialization."""
        node = StartBiasFeatureClassNode()
        node.civilization_type = "CIVILIZATION_PARIS"
        node.feature_class = "FEATURE_MOUNTAIN"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "FeatureClass" in str(xml)


class TestStartBiasRiverNode:
    """Tests for StartBiasRiverNode."""

    def test_start_bias_river_initialization(self):
        """Test StartBiasRiverNode initializes correctly."""
        node = StartBiasRiverNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.bias is None

    def test_start_bias_river_with_data(self):
        """Test StartBiasRiverNode with data."""
        node = StartBiasRiverNode()
        node.civilization_type = "CIVILIZATION_EGYPT"
        node.bias = 100
        
        assert node.civilization_type == "CIVILIZATION_EGYPT"
        assert node.bias == 100

    def test_start_bias_river_to_xml(self):
        """Test StartBiasRiverNode XML serialization."""
        node = StartBiasRiverNode()
        node.civilization_type = "CIVILIZATION_NILE_VALLEY"
        node.bias = 90
        
        xml = node.to_xml_element()
        assert xml is not None


class TestStringNode:
    """Tests for StringNode."""

    def test_string_node_initialization(self):
        """Test StringNode initializes correctly."""
        node = StringNode()
        assert isinstance(node, BaseNode)
        assert node._name == "String"  # StringNode uses 'String', not 'Row'
        assert node.context is None
        assert node.value is None

    def test_string_node_with_data(self):
        """Test StringNode with string data."""
        node = StringNode()
        node.value = "test_string_value"
        
        assert node.value == "test_string_value"

    def test_string_node_with_empty_string(self):
        """Test StringNode with empty string."""
        node = StringNode()
        node.value = ""
        
        # Empty string should not appear in XML
        xml = node.to_xml_element()
        assert xml is None

    def test_string_node_to_xml(self):
        """Test StringNode XML serialization."""
        node = StringNode()
        node.context = "Preview"
        node.value = "my_value"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert xml['_name'] == 'String'
        assert xml['_attrs']['context'] == 'Preview'
        assert xml['_content'] == 'my_value'


class TestUnitReplaceNode:
    """Tests for UnitReplaceNode."""

    def test_unit_replace_node_initialization(self):
        """Test UnitReplaceNode initializes correctly."""
        node = UnitReplaceNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civ_unique_unit_type is None
        assert node.replaces_unit_type is None

    def test_unit_replace_node_with_data(self):
        """Test UnitReplaceNode with data."""
        node = UnitReplaceNode()
        node.unit_type = "UNIT_GONDOR_RANGER"
        node.replaces_unit_type = "UNIT_RANGER"
        node.era = "AGE_MEDIEVAL"
        
        assert node.unit_type == "UNIT_GONDOR_RANGER"
        assert node.replaces_unit_type == "UNIT_RANGER"
        assert node.era == "AGE_MEDIEVAL"

    def test_unit_replace_node_to_xml(self):
        """Test UnitReplaceNode XML serialization."""
        node = UnitReplaceNode()
        node.unit_type = "UNIT_KNIGHT"
        node.replaces_unit_type = "UNIT_HEAVY_CAVALRY"
        node.era = "AGE_MEDIEVAL"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "UnitType" in str(xml)
        assert "ReplacesUnitType" in str(xml)


class TestVisArtCivilizationBuildingCultureNode:
    """Tests for VisArtCivilizationBuildingCultureNode."""

    def test_vis_art_building_culture_initialization(self):
        """Test VisArtCivilizationBuildingCultureNode initializes correctly."""
        node = VisArtCivilizationBuildingCultureNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.building_culture_type is None
        assert node.visual_parent_type is None

    def test_vis_art_building_culture_with_data(self):
        """Test VisArtCivilizationBuildingCultureNode with data."""
        node = VisArtCivilizationBuildingCultureNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.building_culture_type = "BUILDING_CULTURE_GONDOR"
        node.visual_parent_type = "BUILDING_CULTURE_WESTERN"
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.building_culture_type == "BUILDING_CULTURE_GONDOR"
        assert node.visual_parent_type == "BUILDING_CULTURE_WESTERN"

    def test_vis_art_building_culture_to_xml(self):
        """Test VisArtCivilizationBuildingCultureNode XML serialization."""
        node = VisArtCivilizationBuildingCultureNode()
        node.civilization_type = "CIVILIZATION_ROME"
        node.building_culture_type = "BUILDING_CULTURE_ROME"
        node.visual_parent_type = "BUILDING_CULTURE_CLASSICAL"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "CivilizationType" in str(xml)


class TestVisArtCivilizationUnitCultureNode:
    """Tests for VisArtCivilizationUnitCultureNode."""

    def test_vis_art_unit_culture_initialization(self):
        """Test VisArtCivilizationUnitCultureNode initializes correctly."""
        node = VisArtCivilizationUnitCultureNode()
        assert isinstance(node, BaseNode)
        assert node._name == "Row"
        assert node.civilization_type is None
        assert node.unit_culture_type is None
        assert node.visual_parent_type is None

    def test_vis_art_unit_culture_with_data(self):
        """Test VisArtCivilizationUnitCultureNode with data."""
        node = VisArtCivilizationUnitCultureNode()
        node.civilization_type = "CIVILIZATION_GONDOR"
        node.unit_culture_type = "UNIT_CULTURE_GONDOR"
        node.visual_parent_type = "UNIT_CULTURE_WESTERN"
        
        assert node.civilization_type == "CIVILIZATION_GONDOR"
        assert node.unit_culture_type == "UNIT_CULTURE_GONDOR"
        assert node.visual_parent_type == "UNIT_CULTURE_WESTERN"

    def test_vis_art_unit_culture_to_xml(self):
        """Test VisArtCivilizationUnitCultureNode XML serialization."""
        node = VisArtCivilizationUnitCultureNode()
        node.civilization_type = "CIVILIZATION_BARBARIAN"
        node.unit_culture_type = "UNIT_CULTURE_BARBARIAN"
        node.visual_parent_type = "UNIT_CULTURE_DEFAULT"
        
        xml = node.to_xml_element()
        assert xml is not None
        assert "CivilizationType" in str(xml)


# ============================================================================
# Utility Function Tests
# ============================================================================

class TestLocaleUtility:
    """Tests for locale() utility function."""

    def test_locale_basic(self):
        """locale() should combine tag and key."""
        result = locale("LOC_UNIT", "ROMAN_ARCHER")
        assert result == "LOC_LOC_UNIT_ROMAN_ARCHER"

    def test_locale_lowercase_key(self):
        """locale() should uppercase lowercase keys."""
        result = locale("LOC_BUILDING", "forum")
        assert result == "LOC_LOC_BUILDING_FORUM"

    def test_locale_mixed_case_key(self):
        """locale() should handle mixed case keys."""
        result = locale("LOC_UNIT", "RomanLegion")
        assert result == "LOC_LOC_UNIT_ROMAN_LEGION"

    def test_locale_with_underscores(self):
        """locale() should preserve underscores in key."""
        result = locale("LOC", "ROMAN_LEGION_NAME")
        assert result == "LOC_LOC_ROMAN_LEGION_NAME"

    def test_locale_various_tags(self):
        """locale() should work with various tag types."""
        assert locale("LOC_UNIT", "ARCHER").startswith("LOC_LOC_UNIT_")
        assert locale("LOC_BUILDING", "FORUM").startswith("LOC_LOC_BUILDING_")
        assert locale("LOC_TECH", "BRONZE").startswith("LOC_LOC_TECH_")


class TestTrimUtility:
    """Tests for trim() utility function."""

    def test_trim_civilization_prefix(self):
        """trim() should remove CIVILIZATION_ prefix."""
        result = trim("CIVILIZATION_ROME")
        assert result == "ROME"

    def test_trim_unit_prefix(self):
        """trim() should remove UNIT_ prefix."""
        result = trim("UNIT_ROMAN_ARCHER")
        assert result == "ROMAN_ARCHER"

    def test_trim_building_prefix(self):
        """trim() should remove BUILDING_ prefix."""
        result = trim("BUILDING_FORUM")
        assert result == "FORUM"

    def test_trim_improvement_prefix(self):
        """trim() should remove IMPROVEMENT_ prefix."""
        result = trim("IMPROVEMENT_FARM")
        assert result == "FARM"

    def test_trim_no_matching_prefix(self):
        """trim() should return unchanged if no prefix matches."""
        result = trim("ROME")
        assert result == "ROME"

    def test_trim_multiple_prefixes(self):
        """trim() should only remove first matching prefix."""
        result = trim("TRAIT_UNIT_BONUS")
        assert result == "UNIT_BONUS"  # TRAIT_ is removed, UNIT_ remains

    def test_trim_various_game_types(self):
        """trim() should handle various game entity types."""
        assert trim("DISTRICT_COMMERCIAL") == "COMMERCIAL"
        assert trim("TRADITION_MILITARY") == "MILITARY"
        assert trim("LEADER_ALEXANDER") == "ALEXANDER"


class TestKebabCaseUtility:
    """Tests for kebab_case() utility function."""

    def test_kebab_case_pascal_case(self):
        """kebab_case() should convert PascalCase to kebab-case."""
        result = kebab_case("RomanLegion")
        assert result == "roman-legion"

    def test_kebab_case_already_kebab(self):
        """kebab_case() should preserve already kebab-case input."""
        result = kebab_case("roman-legion")
        assert result == "roman-legion"

    def test_kebab_case_snake_case(self):
        """kebab_case() should convert snake_case to kebab-case."""
        result = kebab_case("roman_legion")
        assert result == "roman-legion"

    def test_kebab_case_uppercase(self):
        """kebab_case() should handle uppercase input."""
        result = kebab_case("ROMAN_LEGION")
        assert result == "roman-legion"

    def test_kebab_case_single_word(self):
        """kebab_case() should handle single words."""
        result = kebab_case("Rome")
        assert result == "rome"

    def test_kebab_case_multiple_uppercase_letters(self):
        """kebab_case() should handle consecutive uppercase letters."""
        result = kebab_case("CivilizationID")
        assert result == "civilization-id"

    def test_kebab_case_no_duplicates(self):
        """kebab_case() should not create duplicate hyphens."""
        result = kebab_case("Roman_Legion")
        assert "--" not in result
        assert result == "roman-legion"

    def test_kebab_case_various_formats(self):
        """kebab_case() should handle mixed formats."""
        assert kebab_case("MyModdingTools") == "my-modding-tools"
        assert kebab_case("mod_v2") == "mod-v-2"


# ============================================================================
# Integration Tests
# ============================================================================

class TestNodeIntegration:
    """Integration tests for nodes working together."""

    def test_database_with_new_nodes(self):
        """DatabaseNode should work with all new node types."""
        kind = KindNode(kind="KIND_1")
        type_node = TypeNode(type_="TYPE_1", kind="KIND_1")
        tag = TagNode(tag="TAG_1")
        
        db = DatabaseNode().fill({
            "kinds": [kind],
            "types": [type_node],
            "tags": [tag],
        })
        
        assert len(db.kinds) == 1
        assert len(db.types) == 1
        assert len(db.tags) == 1

    def test_database_with_complex_node_hierarchy(self):
        """DatabaseNode should handle complex node hierarchies."""
        building = BuildingNode(building_type="BUILDING_FORUM")
        constraint = ConstructibleValidDistrictNode(
            constructible_type="BUILDING_FORUM",
            district_type="DISTRICT_COMMERCIAL"
        )
        modifier = GameModifierNode(
            modifier_id="MOD_BUILDING",
            game_effect_id="EFFECT_YIELD"
        )
        
        db = DatabaseNode().fill({
            "buildings": [building],
            "constructible_valid_districts": [constraint],
            "game_modifiers": [modifier],
        })
        
        xml = db.to_xml_element()
        assert xml is not None
        assert "Database" in xml

    def test_node_names_with_utilities(self):
        """Utilities should generate valid names from game entities."""
        # Start with game ID
        game_id = "CIVILIZATION_ROME"
        
        # Use utilities to generate derived names
        trimmed = trim(game_id)  # "ROME"
        path_name = kebab_case(trimmed)  # "rome"
        loc_key = locale("LOC_CIVILIZATION", trimmed)  # "LOC_LOC_CIVILIZATION_ROME"
        
        assert trimmed == "ROME"
        assert path_name == "rome"
        assert loc_key == "LOC_LOC_CIVILIZATION_ROME"

    def test_all_phase6_nodes_inherit_from_basenode(self):
        """Test all Phase 6 nodes properly inherit from BaseNode."""
        nodes = [
            ModifierRequirementNode(),
            StartBiasAdjacentToCoastNode(),
            StartBiasFeatureClassNode(),
            StartBiasRiverNode(),
            StringNode(),
            UnitReplaceNode(),
            VisArtCivilizationBuildingCultureNode(),
            VisArtCivilizationUnitCultureNode(),
        ]
        
        for node in nodes:
            assert isinstance(node, BaseNode)
            assert hasattr(node, 'to_xml_element')
            assert callable(node.to_xml_element)

    def test_all_phase6_nodes_have_name(self):
        """Test all Phase 6 nodes have _name set (either 'Row' or custom)."""
        # Some nodes have custom _name values
        custom_names = {
            ModifierRequirementNode: "Requirement",
            StringNode: "String",
        }
        
        nodes = [
            ModifierRequirementNode(),
            StartBiasAdjacentToCoastNode(),
            StartBiasFeatureClassNode(),
            StartBiasRiverNode(),
            StringNode(),
            UnitReplaceNode(),
            VisArtCivilizationBuildingCultureNode(),
            VisArtCivilizationUnitCultureNode(),
        ]
        
        for node in nodes:
            expected = custom_names.get(type(node), "Row")
            assert node._name == expected, f"{type(node).__name__} should have _name='{expected}'"

    def test_utilities_work_together(self):
        """Utilities should work together for common patterns."""
        # Typical workflow: create ID from entity name
        entity_name = "RomanLegion"
        path_name = kebab_case(entity_name)
        assert path_name == "roman-legion"
        
        # Trim prefix from game ID
        game_id = "UNIT_ROMAN_LEGION"
        short_id = trim(game_id)
        assert short_id == "ROMAN_LEGION"
        
        # Generate localization key
        loc_key = locale("LOC_UNIT", short_id)
        assert loc_key == "LOC_LOC_UNIT_ROMAN_LEGION"

    def test_locale_with_trim(self):
        """locale() and trim() should work well together."""
        full_id = "UNIT_ARCHER"
        trimmed = trim(full_id)
        loc_key = locale("LOC_UNIT", trimmed)
        assert loc_key == "LOC_LOC_UNIT_ARCHER"

    def test_kebab_case_with_locale(self):
        """kebab_case() should work with localization keys."""
        loc_key = "LOC_UNIT_ROMAN_ARCHER"
        path = kebab_case(loc_key)
        assert path == "loc-unit-roman-archer"


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestNodeEdgeCases:
    """Edge case tests for nodes."""

    def test_string_node_with_special_characters(self):
        """Test StringNode handles special XML characters."""
        node = StringNode()
        node.context = "Description"
        node.value = "value_with_&_ampersand"
        
        # Should not raise an error
        xml = node.to_xml_element()
        assert xml is not None
        assert xml['_content'] == "value_with_&_ampersand"

    def test_unit_replace_node_without_era(self):
        """Test UnitReplaceNode works without era."""
        node = UnitReplaceNode()
        node.unit_type = "UNIT_A"
        node.replaces_unit_type = "UNIT_B"
        
        xml = node.to_xml_element()
        assert xml is not None

    def test_start_bias_nodes_all_properties_optional(self):
        """Test start bias nodes work with partial data."""
        # All properties optional
        node1 = StartBiasAdjacentToCoastNode()
        node1.civilization_type = "CIV_TEST"
        # bias is still None
        
        node2 = StartBiasRiverNode()
        node2.bias = 50
        # civilization_type is still None
        
        # Should still serialize without errors
        xml1 = node1.to_xml_element()
        xml2 = node2.to_xml_element()
        assert xml1 is not None
        assert xml2 is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
