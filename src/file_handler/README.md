# file_handler

## Overview

Core file I/O utilities for saving and loading Python objects with automatic
format detection from file extensions.

## Supported formats

| Extension | Format | Notes |
|-----------|--------|-------|
| `.json` | JSON | Best for simple, human-readable dict/list data |
| `.pkl` | Pickle | Supports general Python objects |
| `.yml`, `.yaml` | YAML | Human-readable config/data files |
| `.h5`, `.hdf5` | HDF5 | Supports arrays and dict-like dataset storage |

## Components

| File | Role |
|------|------|
| [handler.py](handler.py) | `FileHandler` implementation (`save`, `load`) |
| [type.py](type.py) | `FileType` enum and extension-to-type mapping |
| [__init__.py](__init__.py) | Package export entrypoint |


