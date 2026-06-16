# FileHandler

## Overview

Lightweight Python utilities for common file I/O tasks:

| Package | Purpose |
|---------|---------|
| [`file_handler`](src/file_handler/README.md) | Save and load JSON, Pickle, YAML, and HDF5 with automatic format detection |
| [`txt_writer`](src/txt_writer/README.md) | Append or overwrite text files with buffered flushing |
| [`xml_handler`](src/xml_handler/README.md) | Parse XML and read tag values from nested paths |

## Requirements

- Python 3.10+
- numpy, h5py, PyYAML

## Setup

```bash
pip install -r requirements.txt
```

For development (tests and type checking):

```bash
pip install -e ".[dev]"
```

## Examples

### Structured files (`file_handler`)

```python
from file_handler import FileHandler

data = {
    "name": "demo",
    "values": [1, 2, 3],
}

FileHandler.save(data, "output/sample.json")
loaded = FileHandler.load("output/sample.json")
```

### Text files (`txt_writer`)

```python
from txt_writer import TxtWriter

with TxtWriter(output_path="output/log.txt", is_reset_enabled=True) as writer:
    writer.write("line one", is_new_line=True)
    writer.write("line two", is_new_line=True)
```

### XML files (`xml_handler`)

```python
from xml_handler import XMLHandler

handler = XMLHandler.from_path("config/settings.xml")
version = handler.find("version")
fps = handler.find_nested_tags(["camera", "fps"])
```

## Tests

```bash
pytest
```
