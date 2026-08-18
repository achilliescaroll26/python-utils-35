# python-utils-35

A collection of general-purpose utilities for Python 3.5 and beyond, designed to simplify daily coding tasks and improve productivity. This project provides a set of streamlined functions and classes that enhance common operations, including text processing, data manipulation, and file handling.

## Features

- **Text Manipulation:** Effortlessly format and clean strings, including trimming whitespace, converting cases, and validating emails.
- **Data Handling:** Fast and efficient methods for reading, writing, and filtering data in CSV and JSON formats.
- **File Operations:** Simplified functions for checking file existence, creating directories, and reading file contents with context management.
- **Simple Caching:** An easy-to-use caching decorator that speeds up repetitive function calls without complicating your code.

## Installation

To install `python-utils-35`, simply use pip:

```bash
pip install python-utils-35
```

For the latest development version, clone the repository and install it locally:

```bash
git clone https://github.com/Developer/python-utils-35.git
cd python-utils-35
pip install -e .
```

## Basic Usage Example

Here’s a quick example to illustrate how to use the utility functions in your project:

```python
from utils import StringUtils, FileUtils

# Using StringUtils to clean an email address
email = "   ExAmPle@Domain.Com  "
clean_email = StringUtils.clean_email(email)
print(f"Cleaned Email: {clean_email}")

# Using FileUtils to read content from a file
file_path = 'sample.txt'
content = FileUtils.read_file(file_path)
print(f"File Content:\n{content}")

# Caching example
@StringUtils.cache
def expensive_function(x):
    return x ** 2

print(expensive_function(4))  # Outputs: 16 (Calculates)
print(expensive_function(4))  # Outputs: 16 (Cached)
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-green)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 

---

Start using `python-utils-35` today to streamline your Python code and enhance your programming efficiency!