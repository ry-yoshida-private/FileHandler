"""Tests for file_handler."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from file_handler import FileHandler, FileType


class TestFileType:
    """Extension-to-format mapping."""

    @pytest.mark.parametrize(
        ("path", "expected"),
        [
            ("data.json", FileType.JSON),
            ("data.pkl", FileType.PICKLE),
            ("data.yml", FileType.YAML),
            ("data.yaml", FileType.YAML),
            ("data.h5", FileType.H5),
            ("data.hdf5", FileType.H5),
        ],
    )
    def test_from_path_recognizes_supported_extensions(
        self,
        path: str,
        expected: FileType,
    ) -> None:
        assert FileType.from_path(path) == expected

    def test_from_path_rejects_unsupported_extension(self) -> None:
        with pytest.raises(ValueError, match="Unsupported file extension"):
            FileType.from_path("data.txt")


class TestFileHandler:
    """Save and load round-trips."""

    @pytest.mark.parametrize(
        "extension",
        ["json", "pkl", "yaml"],
    )
    def test_save_and_load_round_trip(
        self,
        tmp_path: Path,
        extension: str,
    ) -> None:
        data = {"name": "demo", "values": [1, 2, 3]}
        path = tmp_path / f"sample.{extension}"

        FileHandler.save(data, str(path))
        loaded = FileHandler.load(str(path))

        assert loaded == data

    def test_save_creates_parent_directory(self, tmp_path: Path) -> None:
        path = tmp_path / "nested" / "dir" / "sample.json"
        data = {"ok": True}

        FileHandler.save(data, str(path))

        assert path.is_file()
        assert FileHandler.load(str(path)) == data

    def test_load_raises_when_file_missing(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing.json"

        with pytest.raises(FileNotFoundError, match="File not found"):
            FileHandler.load(str(missing))

    def test_save_and_load_h5_dict(self, tmp_path: Path) -> None:
        path = tmp_path / "arrays.h5"
        data = {"a": [1, 2], "b": [3.0, 4.0]}

        FileHandler.save(data, str(path))
        h5_file = FileHandler.load(str(path))
        try:
            assert np.array_equal(h5_file["a"][:], np.array([1, 2]))
            assert np.array_equal(h5_file["b"][:], np.array([3.0, 4.0]))
        finally:
            h5_file.close()

    def test_save_and_load_h5_array(self, tmp_path: Path) -> None:
        path = tmp_path / "vector.h5"
        data = [10, 20, 30]

        FileHandler.save(data, str(path))
        h5_file = FileHandler.load(str(path))
        try:
            assert np.array_equal(h5_file["data"][:], np.array(data))
        finally:
            h5_file.close()
