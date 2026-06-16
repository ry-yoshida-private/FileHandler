"""Tests for txt_writer."""

from __future__ import annotations

from pathlib import Path

import pytest

from txt_writer import TxtWriter


class TestTxtWriter:
    """Text file writing behavior."""

    def test_write_appends_by_default(self, tmp_path: Path) -> None:
        path = tmp_path / "log.txt"

        writer = TxtWriter(output_path=str(path))
        writer.write("first", is_new_line=True)
        writer.close()

        with TxtWriter(output_path=str(path)) as append_writer:
            append_writer.write("second", is_new_line=True)

        assert path.read_text(encoding="utf-8") == "first\nsecond\n"

    def test_reset_mode_overwrites_file(self, tmp_path: Path) -> None:
        path = tmp_path / "log.txt"
        path.write_text("old content\n", encoding="utf-8")

        with TxtWriter(output_path=str(path), is_reset_enabled=True) as writer:
            writer.write("new", is_new_line=True)

        assert path.read_text(encoding="utf-8") == "new\n"

    def test_is_new_line_appends_newline_when_missing(self, tmp_path: Path) -> None:
        path = tmp_path / "log.txt"

        with TxtWriter(output_path=str(path), is_reset_enabled=True) as writer:
            writer.write("no newline", is_new_line=True)
            writer.write("already\n", is_new_line=True)

        assert path.read_text(encoding="utf-8") == "no newline\nalready\n"

    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        path = tmp_path / "nested" / "dir" / "log.txt"

        with TxtWriter(output_path=str(path), is_reset_enabled=True) as writer:
            writer.write("created", is_new_line=True)

        assert path.is_file()

    def test_flush_frequency_must_be_positive(self, tmp_path: Path) -> None:
        path = tmp_path / "log.txt"

        with pytest.raises(ValueError, match="flush_frequency must be greater than 0"):
            TxtWriter(output_path=str(path), flush_frequency=0)

    def test_str_representation(self, tmp_path: Path) -> None:
        path = tmp_path / "log.txt"

        with TxtWriter(output_path=str(path), is_reset_enabled=True) as writer:
            assert str(writer) == f"TxtWriter(output_path={path})"
