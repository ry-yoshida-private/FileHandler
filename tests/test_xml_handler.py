"""Tests for xml_handler."""

from __future__ import annotations

from pathlib import Path

import pytest

from xml_handler import XMLHandler


@pytest.fixture
def sample_xml_path(tmp_path: Path) -> Path:
    """Create a sample XML file for tests."""
    xml_content = """\
<config>
    <version>1.2.3</version>
    <camera>
        <fps>30</fps>
        <resolution>1920x1080</resolution>
    </camera>
    <empty></empty>
</config>
"""
    path = tmp_path / "settings.xml"
    path.write_text(xml_content, encoding="utf-8")
    return path


class TestXMLHandler:
    """XML parsing and tag lookup."""

    def test_from_path_reads_root_tag(self, sample_xml_path: Path) -> None:
        handler = XMLHandler.from_path(str(sample_xml_path))

        assert handler.find("version") == "1.2.3"

    def test_find_nested_tags_traverses_path(self, sample_xml_path: Path) -> None:
        handler = XMLHandler.from_path(str(sample_xml_path))

        assert handler.find_nested_tags(["camera", "fps"]) == "30"
        assert handler.find_nested_tags(["camera", "resolution"]) == "1920x1080"

    def test_find_returns_empty_string_for_empty_tag(
        self,
        sample_xml_path: Path,
    ) -> None:
        handler = XMLHandler.from_path(str(sample_xml_path))

        assert handler.find("empty") == ""

    def test_find_raises_for_missing_tag(self, sample_xml_path: Path) -> None:
        handler = XMLHandler.from_path(str(sample_xml_path))

        with pytest.raises(ValueError, match="Tag 'missing' not found"):
            handler.find("missing")

    def test_find_nested_tags_raises_for_missing_segment(
        self,
        sample_xml_path: Path,
    ) -> None:
        handler = XMLHandler.from_path(str(sample_xml_path))

        with pytest.raises(ValueError, match="Tag 'missing' not found"):
            handler.find_nested_tags(["camera", "missing"])

    def test_find_nested_tags_raises_for_empty_path(
        self,
        sample_xml_path: Path,
    ) -> None:
        handler = XMLHandler.from_path(str(sample_xml_path))

        with pytest.raises(ValueError, match="tags list is empty"):
            handler.find_nested_tags([])
