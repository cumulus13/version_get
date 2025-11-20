# version_get

A robust and production-ready Python package for managing version numbers in your projects.

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🔍 **Auto-detection**: Automatically finds version files in your project
- 📝 **Multiple formats**: Supports various version file naming conventions
- 🎯 **Flexible parsing**: Handles different version string formats with regex
- 🔢 **Version manipulation**: Increment, decrement, and set version numbers
- 🏷️ **Suffix support**: Manage alpha, beta, dev, and custom suffixes
- 💻 **CLI & API**: Use as command-line tool or import as Python class
- 🔧 **Production-ready**: Robust error handling and type hints
- 📦 **Zero dependencies**: No external dependencies required

## Installation

```bash
pip install version_get
```

Or install from source:

```bash
git clone https://github.com/cumulus13/version_get.git
cd version_get
pip install -e .
```

## Quick Start

### As a Python Module

```python
from version_get import VersionGet

# Initialize (auto-detects version file)
vg = VersionGet() # or vg = VersionGet('/projects/myap')

# Get current version
print(vg.get())  # Output: 1.0.0

# Increment version
vg.increment_major()  # 1.0.0 -> 2.0.0
vg.increment_minor()  # 2.0.0 -> 2.1.0
vg.increment_patch()  # 2.1.0 -> 2.1.1

# Set specific version
vg.set_version("3.0.0")

# Set suffixes
vg.set_alpha()  # 3.0.alpha
vg.set_beta()   # 3.0.beta
vg.set_dev()    # 3.0.dev

# Custom suffix
vg.set_suffix("rc1")  # 3.0.rc1

# Default path is parent directory but
# if version file is not exist then return to current directory

# Specify path
vg = VersionGet(path="/path/to/project")

# Create version file if missing
vg = VersionGet(create_if_missing=True)
```

### Auto-reload
```python
vg = VersionGet()
print(vg.get())  # 1.3.4

# Edit manual file → 2.0.0

vg.increment_patch()  # Auto reload → 2.0.0 → 2.0.1 ✓
print(vg.get())       # 2.0.1
```

```python
vg = VersionGet()
print(vg.get())  # 1.3.4

# Edit manual file → 2.0.0

print(vg.get(True)) # 2.0.0
```

### Manual-reload
```python
vg = VersionGet()
print(vg.get())  # 1.3.4

# Edit manual file → 2.0.0

vg.reload()      # Reload dari file
print(vg.get())  # 2.0.0 ✓
```

### Get from file directly

one-time check

```python
vg = VersionGet()
print(vg.get())  # 1.3.4 (from memory)

# Edit manual file → 2.0.0

print(vg.get(from_file=True))  # 2.0.0 ✓ (langsung dari file)
print(vg.get())                # 2.0.0 (updated memory)
```

### Disable Auto-reload (Optional)
```python
vg.increment_patch(auto_reload=False)  # Just use memory``

### As a Command-Line Tool

```bash
# Show current version
version_get
vget  # Short alias

# Increment versions
version_get --increment-major  # x.0.0
version_get --increment-minor  # x.y.0
version_get --increment-patch  # x.y.z
version_get --auto-add         # Same as --increment-patch

# Decrement versions
version_get --decrement-major
version_get --decrement-minor
version_get --decrement-patch

# Set specific version
version_get --set 2.5.0

# Set suffixes
version_get --set-alpha
version_get --set-beta
version_get --set-dev
version_get --set-suffix rc1

# Specify project path
version_get --path /path/to/project

# Create version file if missing
version_get --create

# Quiet mode (only output version)
version_get --quiet
version_get -q

# Verbose mode
version_get --verbose
```

## Supported Version File Names

The package automatically searches for these files (in priority order):

1. `__version__.py`
2. `version.py`
3. `__VERSION__.py`
4. `VERSION.py`
5. `__VER__.py`
6. `__ver__.py`
7. `version`
8. `VERSION`
9. `__version__`
10. `__VERSION__`
11. `__VER__`
12. `__ver__`
13. `VER`
14. `ver`

## Version File Format

The package supports various version string formats:

```python
# Standard formats
version = "1.0.0"
__version__ = "1.0.0"
VERSION = "1.0.0"

# With or without spaces
version="1.0.0"
version = "1.0.0"

# With suffixes
version = "1.0.alpha"
version = "1.0.beta"
version = "1.0.dev"
version = "1.0.rc1"

# Plain version files (no assignment)
1.0.0
```

## Use in setup.py

```python
from setuptools import setup
from version_get import VersionGet

# Get version from version file
vg = VersionGet()
version = vg.get()

setup(
    name='myproject',
    version=version,
    # ... other setup parameters
)
```

Or using the recommended approach:

```python
import os
import re

def get_version():
    """Get version from __version__.py"""
    version_file = os.path.join(os.path.dirname(__file__), '__version__.py')
    with open(version_file, 'r') as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "1.0.0"

setup(
    name='myproject',
    version=get_version(),
    # ... other setup parameters
)
```

## Advanced Usage

### Working with Different Paths

```python
from version_get import VersionGet

# Auto-detect from current or parent directory
vg = VersionGet()

# Specify directory
vg = VersionGet(path="/path/to/project")

# Specify exact file
vg = VersionGet(path="/path/to/project/__version__.py")
```

### Path Resolution

The package uses intelligent path resolution:

1. If path is provided, use that path
2. Check current working directory
3. Check caller's directory (using `inspect`)
4. Check parent of current directory
5. Default to current directory

### Version Manipulation

```python
vg = VersionGet()

# Current: 1.2.3
vg.increment_major()  # -> 2.0.0
vg.increment_minor()  # -> 2.1.0
vg.increment_patch()  # -> 2.1.1

# Decrement (minimum 0)
vg.decrement_patch()  # -> 2.1.0
vg.decrement_minor()  # -> 2.0.0
vg.decrement_major()  # -> 1.0.0

# Set custom version
vg.set_version("3.5.7")

# Work with suffixes
vg.set_suffix("pre-release")  # -> 3.5.pre-release
```

### String Representation

```python
vg = VersionGet()

# Get as string
print(str(vg))  # Output: 1.0.0

# Repr shows more info
print(repr(vg))  # Output: VersionGet(version='1.0.0', file=/path/to/__version__.py)
```

## API Reference

### Class: VersionGet

#### Constructor

```python
VersionGet(path=None, create_if_missing=False)
```

**Parameters:**
- `path` (str, optional): Path to directory or version file
- `create_if_missing` (bool): Create `__version__.py` if not found

#### Methods

- `get()` → str: Get current version
- `increment_major()` → str: Increment major version (x.0.0)
- `increment_minor()` → str: Increment minor version (x.y.0)
- `increment_patch()` → str: Increment patch version (x.y.z)
- `decrement_major()` → str: Decrement major version
- `decrement_minor()` → str: Decrement minor version
- `decrement_patch()` → str: Decrement patch version
- `set_version(version)` → str: Set specific version
- `set_suffix(suffix)` → str: Set version suffix
- `set_alpha()` → str: Set to alpha version
- `set_beta()` → str: Set to beta version
- `set_dev()` → str: Set to dev version
- `auto_add()` → str: Auto-increment patch (alias for increment_patch)

## Examples

### Example 1: CI/CD Integration

```python
# bump_version.py
from version_get import VersionGet

vg = VersionGet()
current = vg.get()
print(f"Current version: {current}")

# Bump patch version for releases
new_version = vg.increment_patch()
print(f"New version: {new_version}")
```

### Example 2: Pre-release Management

```python
from version_get import VersionGet

vg = VersionGet()

# Create alpha release
vg.set_alpha()
print(f"Alpha: {vg.get()}")  # 1.0.alpha

# Move to beta
vg.set_beta()
print(f"Beta: {vg.get()}")   # 1.0.beta

# Final release
vg.increment_patch()
print(f"Release: {vg.get()}") # 1.0.1
```

### Example 3: Automated Versioning

```bash
# In your CI/CD pipeline
# For feature branches
version_get --increment-minor --set-dev

# For release candidates
version_get --increment-major --set-suffix rc1

# For production releases
version_get --increment-patch
```

## Error Handling

The package includes robust error handling:

- File not found: Uses default version "1.0.0"
- Parse errors: Falls back to default version
- Write errors: Prints error message and returns False
- Invalid formats: Shows warning but attempts to proceed

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=version_get tests/
```

### Code Formatting

```bash
# Format code
black version_get/

# Check style
flake8 version_get/

# Type checking
mypy version_get/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [documentation](https://github.com/cumulus13/version_get#readme)
2. Search [existing issues](https://github.com/cumulus13/version_get/issues)
3. Create a [new issue](https://github.com/cumulus13/version_get/issues/new)

## Acknowledgments

- Inspired by semantic versioning best practices
- Built with Python's standard library for zero dependencies

## 👤 Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)
