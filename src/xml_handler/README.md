# xml_handler

## Overview

Parse XML files and read tag values from the root element or nested tag paths.

## Components

| File | Role |
|------|------|
| [handler.py](handler.py) | `XMLHandler` implementation (`find`, `find_nested_tags`, `from_path`) |
| [__init__.py](__init__.py) | Package export entrypoint (`XMLHandler`) |

## Examples

Load from a file path:

```python
from xml_handler import XMLHandler

handler = XMLHandler.from_path("config/settings.xml")
value = handler.find("version")
nested = handler.find_nested_tags(["camera", "fps"])
```

Build from an existing element tree:

```python
import xml.etree.ElementTree as ET

from xml_handler import XMLHandler

tree = ET.parse("config/settings.xml")
handler = XMLHandler(xml=tree, source="config/settings.xml")
```
