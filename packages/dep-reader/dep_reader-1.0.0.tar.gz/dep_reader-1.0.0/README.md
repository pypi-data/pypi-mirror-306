# Description

Read Data Exfiltration Protocol (DEP) Bytes

# Installation

`pip install dep_reader`

# Usage

**From command line:**

`python -m dep_reader [-h]`

This module does not have any direct functionality usable via command line.
It does provide Reader class for reading Data Exfiltration Protocol bytes.

**Programmatically:**

```python

from dep_reader.reader.Reader import Reader as DEPReader

# Where payload is a DEP formated bytes object
reader = DEPReader()
depMsg = reader.processSystemInformationMessage(payload)
```