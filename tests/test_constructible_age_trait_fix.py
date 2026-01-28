"""
Test for AGELESS and trait_type fixes in ConstructibleBuilder.

Tests that:
1. age='AGELESS' is converted to AGELESS tag (not set as age)
2. TRAIT_CULTURAL is auto-corrected to TRAIT_ATTRIBUTE_CULTURAL
3. Other trait patterns are also corrected
"""

import tempfile
from pathlib import Path

from civ7_modding_tools import Mod, ConstructibleBuilder


class TestAgelessHandling:
    """Test AGELESS is handled as a tag, not an age."""

    def test_ageless_converted_to_tag(self):
        """Test that age='AGELESS' becomes AGELESS tag with no age set."""
        mod = Mod(
            id='test-ageless',
            version='1.0.0',
            name='Test AGELESS',
            description='Test',
            authors='Test'
        )

        improvement = ConstructibleBuilder()
        improvement.fill({
            'constructible_type': 'IMPROVEMENT_TEST',
            'is_building': False,
            'improvement': {},
            'age': 'AGELESS',  # This should become a tag, not an age
        })

        mod.add(improvement)

        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)

            # Read generated current.xml (constructibles use action group bundles)
            xml_path = Path(tmpdir) / 'constructibles' / 'test' / 'current.xml'
            assert xml_path.exists()
            content = xml_path.read_text()

            # Should have AGELESS tag
            assert 'Tag="AGELESS"' in content

            # Should NOT have Age="AGELESS" in Constructibles
            assert 'Age="AGELESS"' not in content

            # Verify the Constructible row doesn't have Age attribute at all for ageless items
            # (or if it does, it's not "AGELESS")
            import xmltodict
            data = xmltodict.parse(content)
            constructibles = data['Database']['Constructibles']['Row']
            if not isinstance(constructibles, list):
                constructibles = [constructibles]

            for row in constructibles:
                assert row.get('@Age') != 'AGELESS', 'Age should not be set to AGELESS'


class TestTraitTypeAutoCorrection:
    """Test trait_type values are auto-corrected."""

    def test_trait_cultural_corrected(self):
        """Test TRAIT_CULTURAL -> TRAIT_ATTRIBUTE_CULTURAL."""
        mod = Mod(
            id='test-trait',
            version='1.0.0',
            name='Test Trait',
            description='Test',
            authors='Test'
        )

        improvement = ConstructibleBuilder()
        improvement.fill({
            'constructible_type': 'IMPROVEMENT_CULTURAL',
            'is_building': False,
            'improvement': {
                'trait_type': 'TRAIT_CULTURAL'  # Should be auto-corrected
            },
        })

        mod.add(improvement)

        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)

            xml_path = Path(tmpdir) / 'constructibles' / 'cultural' / 'current.xml'
            assert xml_path.exists()
            content = xml_path.read_text()

            # Should have corrected trait
            assert 'TraitType="TRAIT_ATTRIBUTE_CULTURAL"' in content

            # Should NOT have incorrect trait
            assert 'TraitType="TRAIT_CULTURAL"' not in content

    def test_trait_economic_corrected(self):
        """Test TRAIT_ECONOMIC -> TRAIT_ATTRIBUTE_ECONOMIC."""
        mod = Mod(
            id='test-trait-econ',
            version='1.0.0',
            name='Test',
            description='Test',
            authors='Test'
        )

        improvement = ConstructibleBuilder()
        improvement.fill({
            'constructible_type': 'IMPROVEMENT_ECONOMIC',
            'is_building': False,
            'improvement': {
                'trait_type': 'TRAIT_ECONOMIC'
            },
        })

        mod.add(improvement)

        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)

            xml_path = Path(tmpdir) / 'constructibles' / 'economic' / 'current.xml'
            content = xml_path.read_text()

            assert 'TraitType="TRAIT_ATTRIBUTE_ECONOMIC"' in content
            assert 'TraitType="TRAIT_ECONOMIC"' not in content

    def test_trait_scientific_corrected(self):
        """Test TRAIT_SCIENTIFIC -> TRAIT_ATTRIBUTE_SCIENTIFIC."""
        mod = Mod(
            id='test-trait-sci',
            version='1.0.0',
            name='Test',
            description='Test',
            authors='Test'
        )

        improvement = ConstructibleBuilder()
        improvement.fill({
            'constructible_type': 'IMPROVEMENT_SCIENTIFIC',
            'is_building': False,
            'improvement': {
                'trait_type': 'TRAIT_SCIENTIFIC'
            },
        })

        mod.add(improvement)

        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)

            xml_path = Path(tmpdir) / 'constructibles' / 'scientific' / 'current.xml'
            content = xml_path.read_text()

            assert 'TraitType="TRAIT_ATTRIBUTE_SCIENTIFIC"' in content
            assert 'TraitType="TRAIT_SCIENTIFIC"' not in content

    def test_custom_trait_unchanged(self):
        """Test custom civilization traits are not modified."""
        mod = Mod(
            id='test-custom-trait',
            version='1.0.0',
            name='Test',
            description='Test',
            authors='Test'
        )

        improvement = ConstructibleBuilder()
        improvement.fill({
            'constructible_type': 'IMPROVEMENT_CUSTOM',
            'is_building': False,
            'improvement': {
                'trait_type': 'TRAIT_ICENI_ABILITY'  # Custom civ trait, should not change
            },
        })

        mod.add(improvement)

        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)

            xml_path = Path(tmpdir) / 'constructibles' / 'custom' / 'current.xml'
            content = xml_path.read_text()

            # Custom trait should remain unchanged
            assert 'TraitType="TRAIT_ICENI_ABILITY"' in content


class TestAgelessWithTraitType:
    """Test AGELESS and trait_type work together."""

    def test_ageless_improvement_with_trait(self):
        """Test improvement can be both AGELESS and have a trait_type."""
        mod = Mod(
            id='test-ageless-trait',
            version='1.0.0',
            name='Test',
            description='Test',
            authors='Test'
        )

        improvement = ConstructibleBuilder()
        improvement.fill({
            'constructible_type': 'IMPROVEMENT_AGELESS_CULTURAL',
            'is_building': False,
            'improvement': {
                'trait_type': 'TRAIT_CULTURAL'
            },
            'age': 'AGELESS',
        })

        mod.add(improvement)

        with tempfile.TemporaryDirectory() as tmpdir:
            mod.build(tmpdir)

            xml_path = Path(tmpdir) / 'constructibles' / 'ageless-cultural' / 'current.xml'
            content = xml_path.read_text()

            # Should have AGELESS tag
            assert 'Tag="AGELESS"' in content

            # Should have UNIQUE_IMPROVEMENT tag (due to trait_type)
            assert 'Tag="UNIQUE_IMPROVEMENT"' in content

            # Should have corrected trait
            assert 'TraitType="TRAIT_ATTRIBUTE_CULTURAL"' in content

            # Should NOT have Age="AGELESS"
            assert 'Age="AGELESS"' not in content
