"""Phase 8: Modifier preview strings tests.

Tests for preview text and tooltip strings in ModifierBuilder,
enabling descriptive UI display of game modifiers.
"""

import pytest
from civ7_modding_tools.builders import ModifierBuilder, GameModifierBuilder
from civ7_modding_tools.nodes import (
    ModifierNode, GameModifierNode, StringNode
)
from civ7_modding_tools.files import XmlFile


class TestModifierPreviewStrings:
    """Test modifier preview strings in ModifierBuilder."""

    def test_modifier_with_preview_description(self):
        """Test modifier can have preview description for UI."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_COURAGE"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_COURAGE",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Increases unit morale and combat effectiveness"
            }
        ]
        builder.localizations = [{"name": "Gondor Courage"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_modifier_with_tooltip_text(self):
        """Test modifier can have tooltip text."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_SHIELD"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_SHIELD",
        }
        builder.modifier_strings = [
            {
                "string_type": "TOOLTIP",
                "text": "Defensive bonus: +25% to armor"
            }
        ]
        builder.localizations = [{"name": "Gondor Shield"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        mod_strings = xml["Database"]["ModifierStrings"]
        if isinstance(mod_strings, list):
            string_row = mod_strings[0]
        else:
            string_row = mod_strings

        attrs = string_row["_attrs"]
        assert attrs["ModifierType"] == "MODIFIER_GONDOR_SHIELD"

    def test_modifier_with_multiple_preview_strings(self):
        """Test modifier with multiple preview strings."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_MIGHTY"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_MIGHTY",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Enhanced combat capabilities"
            },
            {
                "string_type": "TOOLTIP",
                "text": "Increases melee damage by 20%"
            },
            {
                "string_type": "EFFECTS_TOOLTIP",
                "text": "Active in all terrains"
            }
        ]
        builder.localizations = [{"name": "Gondor Mighty"}]

        builder.migrate()
        xml = builder._current.to_xml_element()
        assert "Database" in xml

    def test_modifier_with_fill_method(self):
        """Test modifier preview strings via fill() method."""
        builder = ModifierBuilder().fill({
            "modifier_type": "MODIFIER_GONDOR_VALOR",
            "modifier": {
                "modifier_type": "MODIFIER_GONDOR_VALOR",
            },
            "modifier_strings": [
                {
                    "string_type": "PREVIEW_DESCRIPTION",
                    "text": "Honor in battle"
                },
                {
                    "string_type": "TOOLTIP",
                    "text": "+30% experience gain"
                }
            ],
            "localizations": [{"name": "Gondor Valor"}],
        })

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_modifier_preview_strings_optional(self):
        """Test preview strings are optional (backward compatible)."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_ROME_LEGACY"
        builder.modifier = {
            "modifier_type": "MODIFIER_ROME_LEGACY",
        }
        builder.localizations = [{"name": "Roman Legacy"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # Should return None or empty database when no modifier_strings
        if xml is not None:
            assert isinstance(xml, dict)


class TestGameModifierPreviewStrings:
    """Test preview strings in GameModifierBuilder."""

    def test_game_modifier_with_preview_description(self):
        """Test game modifier can have preview description."""
        builder = GameModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_STRATEGY"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_STRATEGY",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Strategic advantage in warfare"
            }
        ]
        builder.localizations = [{"name": "Gondor Strategy"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_game_modifier_with_multiple_strings(self):
        """Test game modifier with multiple preview strings."""
        builder = GameModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_DOMINION"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_DOMINION",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Extended military dominion"
            },
            {
                "string_type": "TOOLTIP",
                "text": "+1 diplomatic favor per turn"
            },
            {
                "string_type": "FLAVOR_TEXT",
                "text": "A kingdom united in purpose"
            }
        ]
        builder.localizations = [{"name": "Gondor Dominion"}]

        builder.migrate()
        xml = builder._current.to_xml_element()
        assert "Database" in xml


class TestCarthageModifierPattern:
    """Test that preview strings match Carthage modifier patterns."""

    def test_carthage_trade_modifier_pattern(self):
        """Test trade modifier matches Carthage pattern."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_CARTHAGE_TRADE"
        builder.modifier = {
            "modifier_type": "MODIFIER_CARTHAGE_TRADE",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Enhanced trade routes"
            },
            {
                "string_type": "TOOLTIP",
                "text": "+25% to trade yields"
            }
        ]
        builder.localizations = [{"name": "Carthage Trade"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_carthage_military_modifier_pattern(self):
        """Test military modifier pattern."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_CARTHAGE_NAVY"
        builder.modifier = {
            "modifier_type": "MODIFIER_CARTHAGE_NAVY",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Naval supremacy enhancement"
            }
        ]
        builder.localizations = [{"name": "Carthage Navy"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db


class TestModifierStringIntegration:
    """Test preview strings integrated with other modifier features."""

    def test_modifier_with_strings_and_requirements(self):
        """Test preview strings work with modifier requirements."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_DEFENSE"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_DEFENSE",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Defensive fortification"
            }
        ]
        builder.requirements = [
            {"requirement_type": "REQ_GONDOR_ACTIVE"}
        ]
        builder.localizations = [{"name": "Gondor Defense"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_modifier_builder_fluent_api(self):
        """Test fluent API with preview strings."""
        builder = (
            ModifierBuilder()
            .fill({
                "modifier_type": "MODIFIER_GONDOR_UNITED",
                "modifier": {
                    "modifier_type": "MODIFIER_GONDOR_UNITED",
                },
                "modifier_strings": [
                    {
                        "string_type": "PREVIEW_DESCRIPTION",
                        "text": "Unity among people"
                    }
                ],
                "localizations": [{"name": "Gondor United"}],
            })
        )

        builder.migrate()
        xml = builder._current.to_xml_element()
        assert "Database" in xml

    def test_modifier_with_all_string_types(self):
        """Test comprehensive modifier with all string types."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_COMPLETE"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_COMPLETE",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Complete enhancement package"
            },
            {
                "string_type": "TOOLTIP",
                "text": "All game aspects improved"
            },
            {
                "string_type": "EFFECTS_TOOLTIP",
                "text": "Effects vary by context"
            },
            {
                "string_type": "FLAVOR_TEXT",
                "text": "A comprehensive advantage"
            }
        ]
        builder.localizations = [{"name": "Gondor Complete"}]

        builder.migrate()
        xml = builder._current.to_xml_element()
        assert "Database" in xml


class TestModifierStringEdgeCases:
    """Test edge cases for modifier preview strings."""

    def test_modifier_with_empty_string(self):
        """Test modifier with empty preview string."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_EMPTY"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_EMPTY",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": ""
            }
        ]
        builder.localizations = [{"name": "Gondor Empty"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        # Should still generate valid structure
        assert "ModifierStrings" in db

    def test_modifier_with_long_description(self):
        """Test modifier with very long preview description."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_LONG"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_LONG",
        }
        long_text = "A" * 500  # 500 character string
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": long_text
            }
        ]
        builder.localizations = [{"name": "Gondor Long"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_modifier_with_special_characters(self):
        """Test modifier string with special characters."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_SPECIAL"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_SPECIAL",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Bonus: +25% & -10% <Special> [Effect]"
            }
        ]
        builder.localizations = [{"name": "Gondor Special"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_modifier_with_partial_strings(self):
        """Test modifier with only some string types specified."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_PARTIAL"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_PARTIAL",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Partial description"
            }
        ]
        builder.localizations = [{"name": "Gondor Partial"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        db = xml["Database"]
        assert "ModifierStrings" in db

    def test_modifier_empty_strings_list(self):
        """Test modifier with empty strings list."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_NOSTRINGS"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_NOSTRINGS",
        }
        builder.modifier_strings = []
        builder.localizations = [{"name": "Gondor No Strings"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # Should return None when empty
        if xml is not None:
            db = xml["Database"]
            # Might not have ModifierStrings if list was empty
            assert isinstance(db, dict)

    def test_modifier_without_strings_attribute(self):
        """Test modifier without modifier_strings attribute at all."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_GONDOR_BASIC"
        builder.modifier = {
            "modifier_type": "MODIFIER_GONDOR_BASIC",
        }
        builder.localizations = [{"name": "Gondor Basic"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # Should return None or valid empty database when no modifier_strings
        if xml is not None:
            assert isinstance(xml, dict)


class TestModifierStringTypes:
    """Test correct handling of different string type values."""

    def test_preview_description_type(self):
        """Test PREVIEW_DESCRIPTION string type."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_TEST_PREVIEW"
        builder.modifier = {
            "modifier_type": "MODIFIER_TEST_PREVIEW",
        }
        builder.modifier_strings = [
            {
                "string_type": "PREVIEW_DESCRIPTION",
                "text": "Test preview"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_tooltip_type(self):
        """Test TOOLTIP string type."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_TEST_TOOLTIP"
        builder.modifier = {
            "modifier_type": "MODIFIER_TEST_TOOLTIP",
        }
        builder.modifier_strings = [
            {
                "string_type": "TOOLTIP",
                "text": "Test tooltip"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_effects_tooltip_type(self):
        """Test EFFECTS_TOOLTIP string type."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_TEST_EFFECTS"
        builder.modifier = {
            "modifier_type": "MODIFIER_TEST_EFFECTS",
        }
        builder.modifier_strings = [
            {
                "string_type": "EFFECTS_TOOLTIP",
                "text": "Test effects"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_flavor_text_type(self):
        """Test FLAVOR_TEXT string type."""
        builder = ModifierBuilder()
        builder.modifier_type = "MODIFIER_TEST_FLAVOR"
        builder.modifier = {
            "modifier_type": "MODIFIER_TEST_FLAVOR",
        }
        builder.modifier_strings = [
            {
                "string_type": "FLAVOR_TEXT",
                "text": "Test flavor"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
