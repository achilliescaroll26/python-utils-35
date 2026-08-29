# python-utils-35

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of focused Python utilities that handle repetitive tasks without introducing heavy dependencies. The package targets Python 3.5+ and prioritizes reliability across file operations, configuration, and error handling.

## Features
- Load and validate configuration from JSON, YAML, and environment variables with type checking
- Retry and timing decorators for network calls and background tasks
- Atomic file writes and safe temporary file management
- Cross-platform path normalization and string sanitization helpers

## Installation

```bash
pip install python-utils-35
```

Install the development version directly from the repository:

```bash
pip install git+https://github.com/Developer/python-utils-35.git
```

## Basic Usage

```python
from python_utils_35 import load_config, retry

config = load_config("settings.yaml")

@retry(attempts=3, delay=1.0)
def fetch_data():
    # network or I/O call
    pass
```

## License

MIT