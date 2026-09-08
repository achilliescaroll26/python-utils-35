# python-utils-35

A curated collection of robust, production-ready Python utility functions designed to streamline daily development tasks. This library focuses on performance, type safety, and reducing boilerplate code in data processing and system operations.

## Features

*   **Robust File Operations:** Enhanced wrappers for atomic file writing, recursive directory navigation, and smart path resolution.
*   **Data Transformation:** Efficient helpers for flattening nested dictionaries and converting complex data structures into normalized formats.
*   **Async Task Helpers:** Lightweight utilities for managing concurrent task execution and graceful timeouts.
*   **Type-Safe Validation:** A set of strict validators for ensuring configuration inputs and environment variables meet expected schema requirements.

## Installation

Install `python-utils-35` directly via pip:

```bash
pip install python-utils-35
```

For development installations, clone the repository and run:

```bash
git clone https://github.com/Developer/python-utils-35.git
cd python-utils-35
pip install -e .
```

## Basic Usage

Quickly simplify your workflow with built-in data transformation and path utilities:

```python
from pyutils35 import dict_utils, path_utils

# Flatten nested JSON/Dict structures
data = {"user": {"profile": {"id": 1}}}
flat = dict_utils.flatten(data)
# Output: {'user.profile.id': 1}

# Securely find absolute paths
config_path = path_utils.resolve_path("config/settings.yaml")
print(f"Loading config from: {config_path}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.