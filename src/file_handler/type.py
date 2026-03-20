from __future__ import annotations
import os
from enum import Enum

class FileType(Enum):
    PICKLE = 'pickle'
    JSON = 'json'
    YAML = 'yaml'
    H5 = 'h5'

    @classmethod
    def from_path(cls, path: str) -> FileType:
        ext = os.path.splitext(path)[1].lower().lstrip('.')
        type_ = {
            'json': cls.JSON,
            'pkl': cls.PICKLE,
            'yml': cls.YAML,
            'yaml': cls.YAML,
            'hdf5': cls.H5,
            'h5': cls.H5,
        }.get(ext)
        if type_ is None:
            raise ValueError(f"Unsupported file extension in path: {path}")
        return type_
