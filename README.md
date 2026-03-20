# FileHandler

## Overview

Lightweight utility for reading and writing common file formats with one API.
`FileHandler` chooses the serializer automatically from the file extension.

See the [package README](src/file_handler/README.md) for module details.

## Requirements

- Python 3.x
- numpy, h5py, pyyaml

## Setup

```bash
pip install -r requirements.txt
```

## Example

Save and load data with automatic format handling:

```python
from file_handler.handler import FileHandler

data = {
    "name": "demo",
    "values": [1, 2, 3]
}

# JSON
FileHandler.save(data, "output/sample.json")
json_obj = FileHandler.load("output/sample.json")
print(json_obj)

# Pickle
FileHandler.save(data, "output/sample.pkl")
pkl_obj = FileHandler.load("output/sample.pkl")
print(pkl_obj)

# YAML
FileHandler.save(data, "output/sample.yaml")
yaml_obj = FileHandler.load("output/sample.yaml")
print(yaml_obj)
```
