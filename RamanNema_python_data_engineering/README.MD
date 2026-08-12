# data_processor_task

A simple Python training assignment for member data processing and validation.

## Overview

This project provides utilities to process member records, validate email and phone formats, clean whitespace, and filter members by email domain.

## Features

- Validate and normalize member fields
- Enforce required fields for `name`, `email`, and `phone`
- Validate email addresses and phone numbers
- Filter processed members by email domain
- Print summary output and skip invalid records gracefully

## Installation

Install locally using pip:

```bash
pip install .
```

Or install from source with:

```bash
python setup.py install
```

## Requirements

- Python 3.6+

## Usage

Import the processor and data helpers from the package:

```python
from my_processor.core import process_members, run_processor
from my_processor.utils import InvalidMemberDataError

raw_members = [
    {"name": "John Doe", "email": "john.doe@example.com", "phone": "555-0101"},
    {"name": "Jane Smith", "email": "jane.smith@example.com", "phone": "555-0102"}
]

processed = process_members(raw_members)
for member in processed:
    print(member)
```

The package also includes a runnable example:

```bash
python -m my_processor.core
```

## Package Structure

- `my_processor/core.py` - Main processing logic and example runner
- `my_processor/utils.py` - Validation helpers, formatting, and custom exception
- `setup.py` - Packaging configuration
- `pyproject.toml` - Build metadata

## Validation Rules

- `name` must be a non-empty string and is limited to 50 characters
- `email` must match a basic email pattern
- `phone` must be in the format `###-####`

## Screenshots

#### Folder Structure

![Folder Structure](screenshots/folder_structure.png)

#### Application Execution

![application execution](screenshots/application_execution.png)

#### Wheel Creation

![wheel creation](screenshots/wheel_creation.png)

#### Wheel installation

![wheel installation](screenshots/wheel_installation.png)

#### Package import

![package_import](screenshots/package_import.png)

## Notes

Invalid records are skipped during processing, and the summary reports how many members were successfully processed.
