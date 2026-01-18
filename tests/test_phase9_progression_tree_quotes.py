"""Phase 9: Progression tree quotes tests.

Tests for narrative and flavor text in ProgressionTreeBuilder,
enabling story-driven progression narratives.
"""

import pytest
from civ7_modding_tools.builders import ProgressionTreeBuilder
from civ7_modding_tools.nodes import ProgressionTreeNodeNode
from civ7_modding_tools.files import XmlFile


class TestProgressionTreeQuotes:
    """Test progression tree quotes in ProgressionTreeBuilder."""

    def test_progression_tree_with_intro_quote(self):
        """Test progression tree can have intro narrative."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_JOURNEY"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_JOURNEY",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "The journey of a great kingdom begins..."
            }
        ]
        builder.localizations = [{"name": "Gondor Journey"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_with_conclusion_quote(self):
        """Test progression tree can have conclusion narrative."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_LEGACY"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_LEGACY",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "CONCLUSION",
                "text": "A legacy that will endure for ages to come"
            }
        ]
        builder.localizations = [{"name": "Gondor Legacy"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_with_multiple_quotes(self):
        """Test progression tree with multiple narrative quotes."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_SAGA"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_SAGA",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "Chapter I: The Rise Begins"
            },
            {
                "quote_type": "MILESTONE",
                "text": "The turning point of our destiny"
            },
            {
                "quote_type": "CONCLUSION",
                "text": "Chapter X: The Final Triumph"
            }
        ]
        builder.localizations = [{"name": "Gondor Saga"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_with_fill_method(self):
        """Test progression tree quotes via fill() method."""
        builder = ProgressionTreeBuilder().fill({
            "progression_tree_type": "PROGRESSION_GONDOR_EPIC",
            "progression_tree": {
                "progression_tree_type": "PROGRESSION_GONDOR_EPIC",
            },
            "progression_tree_quotes": [
                {
                    "quote_type": "INTRO",
                    "text": "An epic tale unfolds"
                },
                {
                    "quote_type": "CONCLUSION",
                    "text": "The legend is complete"
                }
            ],
            "localizations": [{"name": "Gondor Epic"}],
        })

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_quotes_optional(self):
        """Test quotes are optional (backward compatible)."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_ROME_STANDARD"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_ROME_STANDARD",
        }
        builder.localizations = [{"name": "Roman Standard"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        # Should still work without quotes
        if xml is not None:
            assert isinstance(xml, dict)


class TestCarthageProgressionTreeQuotes:
    """Test that quotes match Carthage progression patterns."""

    def test_carthage_naval_progression_quotes(self):
        """Test naval progression with narrative quotes."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_CARTHAGE_NAVAL"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_CARTHAGE_NAVAL",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "The Carthaginian fleet takes to the seas"
            },
            {
                "quote_type": "CONCLUSION",
                "text": "Carthaginian naval dominance secured"
            }
        ]
        builder.localizations = [{"name": "Carthage Naval"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_carthage_trade_progression_quotes(self):
        """Test trade progression narrative."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_CARTHAGE_TRADE"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_CARTHAGE_TRADE",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "A commercial empire begins"
            }
        ]
        builder.localizations = [{"name": "Carthage Trade"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml


class TestProgressionTreeQuoteIntegration:
    """Test quotes integrated with other progression tree features."""

    def test_progression_tree_with_quotes_and_nodes(self):
        """Test quotes work with progression tree nodes."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_COMPLETE"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_COMPLETE",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "The complete story"
            }
        ]
        builder.progression_tree_nodes = [
            {
                "progression_tree_node_type": "NODE_GONDOR_START",
            }
        ]
        builder.localizations = [{"name": "Gondor Complete"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_builder_fluent_api(self):
        """Test fluent API with progression tree quotes."""
        builder = (
            ProgressionTreeBuilder()
            .fill({
                "progression_tree_type": "PROGRESSION_GONDOR_FLUENT",
                "progression_tree": {
                    "progression_tree_type": "PROGRESSION_GONDOR_FLUENT",
                },
                "progression_tree_quotes": [
                    {
                        "quote_type": "INTRO",
                        "text": "Fluent building begins"
                    }
                ],
                "localizations": [{"name": "Gondor Fluent"}],
            })
        )

        builder.migrate()
        xml = builder._current.to_xml_element()
        assert "Database" in xml

    def test_progression_tree_with_all_features(self):
        """Test comprehensive progression tree with quotes."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_FULL"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_FULL",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "The full story unfolds"
            },
            {
                "quote_type": "MILESTONE",
                "text": "A crucial moment"
            },
            {
                "quote_type": "CONCLUSION",
                "text": "The journey complete"
            }
        ]
        builder.progression_tree_nodes = [
            {"progression_tree_node_type": "NODE_GONDOR_1"},
            {"progression_tree_node_type": "NODE_GONDOR_2"}
        ]
        builder.localizations = [{"name": "Gondor Full"}]

        files = builder.build()
        assert len(files) > 0


class TestProgressionTreeQuoteEdgeCases:
    """Test edge cases for progression tree quotes."""

    def test_progression_tree_with_empty_quote(self):
        """Test progression tree with empty quote text."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_EMPTY"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_EMPTY",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": ""
            }
        ]
        builder.localizations = [{"name": "Gondor Empty"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        if xml is not None:
            assert isinstance(xml, dict)

    def test_progression_tree_with_long_quote(self):
        """Test progression tree with very long quote."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_LONG"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_LONG",
        }
        long_quote = "A" * 1000  # 1000 character quote
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": long_quote
            }
        ]
        builder.localizations = [{"name": "Gondor Long"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_with_special_characters_in_quote(self):
        """Test progression tree quote with special characters."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_SPECIAL"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_SPECIAL",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "\"For honor!\" & 'For glory!' <and more> [achievements]"
            }
        ]
        builder.localizations = [{"name": "Gondor Special"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_with_partial_quotes(self):
        """Test progression tree with only some quote types."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_PARTIAL"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_PARTIAL",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "Begin"
            }
        ]
        builder.localizations = [{"name": "Gondor Partial"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_progression_tree_empty_quotes_list(self):
        """Test progression tree with empty quotes list."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_NOQUOTES"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_NOQUOTES",
        }
        builder.progression_tree_quotes = []
        builder.localizations = [{"name": "Gondor No Quotes"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        if xml is not None:
            assert isinstance(xml, dict)

    def test_progression_tree_without_quotes_attribute(self):
        """Test progression tree without quotes attribute."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_GONDOR_BASIC"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_GONDOR_BASIC",
        }
        builder.localizations = [{"name": "Gondor Basic"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        if xml is not None:
            assert isinstance(xml, dict)


class TestProgressionTreeQuoteTypes:
    """Test different quote type values."""

    def test_intro_quote_type(self):
        """Test INTRO quote type."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_TEST_INTRO"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_TEST_INTRO",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "INTRO",
                "text": "Introduction"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_milestone_quote_type(self):
        """Test MILESTONE quote type."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_TEST_MILESTONE"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_TEST_MILESTONE",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "MILESTONE",
                "text": "A milestone achieved"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_conclusion_quote_type(self):
        """Test CONCLUSION quote type."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_TEST_CONCLUSION"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_TEST_CONCLUSION",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "CONCLUSION",
                "text": "The conclusion"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml

    def test_flavor_quote_type(self):
        """Test FLAVOR quote type."""
        builder = ProgressionTreeBuilder()
        builder.progression_tree_type = "PROGRESSION_TEST_FLAVOR"
        builder.progression_tree = {
            "progression_tree_type": "PROGRESSION_TEST_FLAVOR",
        }
        builder.progression_tree_quotes = [
            {
                "quote_type": "FLAVOR",
                "text": "Flavor text"
            }
        ]
        builder.localizations = [{"name": "Test"}]

        builder.migrate()
        xml = builder._current.to_xml_element()

        assert "Database" in xml
