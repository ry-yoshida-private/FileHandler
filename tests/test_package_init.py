"""Tests for package public APIs."""

from __future__ import annotations

import file_handler
import txt_writer
import xml_handler


class TestPackageExports:
    """Each package exposes a stable public API."""

    def test_file_handler_exports(self) -> None:
        assert set(file_handler.__all__) == {"FileHandler", "FileType"}
        for name in file_handler.__all__:
            assert hasattr(file_handler, name)

    def test_txt_writer_exports(self) -> None:
        assert set(txt_writer.__all__) == {"TxtWriter"}
        for name in txt_writer.__all__:
            assert hasattr(txt_writer, name)

    def test_xml_handler_exports(self) -> None:
        assert set(xml_handler.__all__) == {"XMLHandler"}
        for name in xml_handler.__all__:
            assert hasattr(xml_handler, name)
