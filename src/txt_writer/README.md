# txt_writer

## Overview

Append or overwrite text files with buffered flushing and context-manager support.

## Components

| File | Role |
|------|------|
| [writer.py](writer.py) | `TxtWriter` implementation (`write`, `close`) |
| [__init__.py](__init__.py) | Package export entrypoint (`TxtWriter`) |

## Examples

Manual open/close:

```python
from txt_writer import TxtWriter

writer = TxtWriter(output_path="tmp.txt")
writer.write(txt="Hello, world!", is_new_line=False)
writer.write(txt="Hello, world!", is_new_line=True)
writer.close()
```

Context manager with file reset:

```python
from txt_writer import TxtWriter

with TxtWriter(output_path="tmp.txt", is_reset_enabled=True) as writer:
    writer.write(txt="Hello, world!", is_new_line=False)
    writer.write(txt="Hello, world!", is_new_line=True)
```
