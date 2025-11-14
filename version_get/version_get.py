#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: version_get/version_get.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2025-11-14
# Description: A robust version management utility for Python projects 
# License: MIT

"""
version_get - A robust version management utility for Python projects
Author: cumulus13
URL: https://github.com/cumulus13/version_get
"""

import os
import re
import sys
import inspect
import argparse
try:
    from licface import CustomRichHelpFormatter
except:
    CustomRichHelpFormatter = argparse.RawTextHelpFormatter
from pathlib import Path
from typing import Optional, Tuple, Union, List

__version__ = "1.0.0"

class VersionGet:
    """
    A class to manage version numbers from various version files.
    
    Supports automatic detection of version files and version manipulation.
    """
    
    # List of possible version file names (in priority order)
    VERSION_FILES = [
        '__version__.py',
        'version.py',
        '__VERSION__.py',
        'VERSION.py',
        '__VER__.py',
        '__ver__.py',
        'version',
        'VERSION',
        '__version__',
        '__VERSION__',
        '__VER__',
        '__ver__',
        'VER',
        'ver',
    ]
    
    # Regex patterns to match version strings
    VERSION_PATTERNS = [
        r'version\s*=\s*["\']([^"\']+)["\']',
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        r'VERSION\s*=\s*["\']([^"\']+)["\']',
        r'^([0-9]+\.[0-9]+\.[0-9]+(?:[a-zA-Z][a-zA-Z0-9]*)?)\s*$',
    ]
    
    def __init__(self, path: Optional[str] = None, create_if_missing: bool = False):
        """
        Initialize VersionGet instance.
        
        Args:
            path: Path to directory containing version file or path to version file itself.
                  If None, uses current directory or caller's directory.
            create_if_missing: If True, creates __version__.py with default version if not found.
        """
        self.path = self._resolve_path(path)
        self.version_file = None
        self.version = "1.0.0"
        self.create_if_missing = create_if_missing
        
        self._find_and_load_version()
    
    def _resolve_path(self, path: Optional[str]) -> Path:
        """
        Resolve the path to search for version files.
        
        Args:
            path: User-provided path or None
            
        Returns:
            Path object pointing to search directory
        """
        if path:
            p = Path(path).resolve()
            if p.is_file():
                return p.parent
            return p
        
        # Try current directory first
        cwd = Path.cwd()
        if self._has_version_file(cwd):
            return cwd
        
        # Try caller's directory using inspect
        try:
            frame = inspect.stack()[2]
            caller_file = frame.filename
            caller_dir = Path(caller_file).parent.resolve()
            if self._has_version_file(caller_dir):
                return caller_dir
        except (IndexError, AttributeError):
            pass
        
        # Try parent of current directory
        parent = cwd.parent
        if self._has_version_file(parent):
            return parent
        
        # Default to current directory
        return cwd
    
    def _has_version_file(self, directory: Path) -> bool:
        """Check if directory contains any version file."""
        for filename in self.VERSION_FILES:
            if (directory / filename).exists():
                return True
        return False
    
    def _find_version_file(self) -> Optional[Path]:
        """
        Find the first existing version file in the path.
        
        Returns:
            Path to version file or None if not found
        """
        for filename in self.VERSION_FILES:
            filepath = self.path / filename
            if filepath.exists():
                return filepath
        return None
    
    def _parse_version(self, content: str) -> Optional[str]:
        """
        Parse version string from file content using regex patterns.
        
        Args:
            content: File content to parse
            
        Returns:
            Version string or None if not found
        """
        for pattern in self.VERSION_PATTERNS:
            match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _find_and_load_version(self) -> None:
        """Find and load version from file."""
        self.version_file = self._find_version_file()
        
        if self.version_file:
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parsed_version = self._parse_version(content)
                if parsed_version:
                    self.version = parsed_version
                else:
                    # File exists but no version found, use default
                    self.version = "1.0.0"
            except (IOError, UnicodeDecodeError) as e:
                print(f"Warning: Could not read {self.version_file}: {e}", file=sys.stderr)
                self.version = "1.0.0"
        else:
            # No version file found
            if self.create_if_missing:
                self._create_default_version_file()
    
    def _create_default_version_file(self) -> None:
        """Create a default __version__.py file with version 1.0.0"""
        version_file = self.path / '__version__.py'
        try:
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write('__version__ = "1.0.0"\n')
            self.version_file = version_file
            self.version = "1.0.0"
            print(f"Created version file: {version_file}")
        except IOError as e:
            print(f"Warning: Could not create version file: {e}", file=sys.stderr)
    
    def _parse_version_parts(self) -> Tuple[int, int, Union[int, str]]:
        """
        Parse version into components (major, minor, patch/suffix).
        
        Returns:
            Tuple of (major, minor, patch_or_suffix)
        """
        # Match x.y.z or x.y.suffix
        match = re.match(r'^(\d+)\.(\d+)\.(.+)$', self.version)
        if match:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch_str = match.group(3)
            
            # Try to parse patch as integer
            try:
                patch = int(patch_str)
                return major, minor, patch
            except ValueError:
                # It's a suffix (alpha, beta, dev, etc.)
                return major, minor, patch_str
        
        # Fallback to default
        return 1, 0, 0
    
    def _write_version(self, new_version: str) -> bool:
        """
        Write new version to the version file.
        
        Args:
            new_version: New version string to write
            
        Returns:
            True if successful, False otherwise
        """
        if not self.version_file:
            print("Error: No version file found. Cannot update version.", file=sys.stderr)
            return False
        
        try:
            # Read current content
            with open(self.version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to replace existing version
            replaced = False
            for pattern in self.VERSION_PATTERNS[:3]:  # Only assignment patterns
                if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                    # Find the assignment pattern and replace
                    new_content = re.sub(
                        pattern,
                        lambda m: m.group(0).replace(self.version, new_version),
                        content,
                        flags=re.MULTILINE | re.IGNORECASE
                    )
                    with open(self.version_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    replaced = True
                    break
            
            if not replaced:
                # No pattern matched, write default format
                with open(self.version_file, 'w', encoding='utf-8') as f:
                    f.write(f'__version__ = "{new_version}"\n')
            
            self.version = new_version
            return True
            
        except IOError as e:
            print(f"Error: Could not write to version file: {e}", file=sys.stderr)
            return False
    
    def get(self) -> str:
        """
        Get current version string.
        
        Returns:
            Version string
        """
        return self.version
    
    def increment_major(self) -> str:
        """
        Increment major version number (x.0.0).
        
        Returns:
            New version string
        """
        major, _, _ = self._parse_version_parts()
        new_version = f"{major + 1}.0.0"
        self._write_version(new_version)
        return new_version
    
    def increment_minor(self) -> str:
        """
        Increment minor version number (x.y.0).
        
        Returns:
            New version string
        """
        major, minor, _ = self._parse_version_parts()
        new_version = f"{major}.{minor + 1}.0"
        self._write_version(new_version)
        return new_version
    
    def increment_patch(self) -> str:
        """
        Increment patch/test number (x.y.z).
        
        Returns:
            New version string
        """
        major, minor, patch = self._parse_version_parts()
        if isinstance(patch, int):
            new_version = f"{major}.{minor}.{patch + 1}"
        else:
            # If patch is a suffix, convert to numeric
            new_version = f"{major}.{minor}.1"
        self._write_version(new_version)
        return new_version
    
    def decrement_major(self) -> str:
        """
        Decrement major version number (min 0).
        
        Returns:
            New version string
        """
        major, _, _ = self._parse_version_parts()
        new_major = max(0, major - 1)
        new_version = f"{new_major}.0.0"
        self._write_version(new_version)
        return new_version
    
    def decrement_minor(self) -> str:
        """
        Decrement minor version number (min 0).
        
        Returns:
            New version string
        """
        major, minor, _ = self._parse_version_parts()
        new_minor = max(0, minor - 1)
        new_version = f"{major}.{new_minor}.0"
        self._write_version(new_version)
        return new_version
    
    def decrement_patch(self) -> str:
        """
        Decrement patch/test number (min 0).
        
        Returns:
            New version string
        """
        major, minor, patch = self._parse_version_parts()
        if isinstance(patch, int):
            new_patch = max(0, patch - 1)
            new_version = f"{major}.{minor}.{new_patch}"
        else:
            new_version = f"{major}.{minor}.0"
        self._write_version(new_version)
        return new_version
    
    def set_version(self, version: str) -> str:
        """
        Set version to specific value.
        
        Args:
            version: Version string to set
            
        Returns:
            New version string
        """
        # Validate version format
        if not re.match(r'^\d+\.\d+\.\w+$', version):
            print(f"Warning: Version '{version}' may not be in standard format", file=sys.stderr)
        
        self._write_version(version)
        return version
    
    def set_suffix(self, suffix: str) -> str:
        """
        Set version suffix (alpha, beta, dev, etc.).
        
        Args:
            suffix: Suffix to set
            
        Returns:
            New version string
        """
        major, minor, _ = self._parse_version_parts()
        new_version = f"{major}.{minor}.{suffix}"
        self._write_version(new_version)
        return new_version
    
    def set_alpha(self) -> str:
        """Set version to alpha. Returns: New version string"""
        return self.set_suffix('alpha')
    
    def set_beta(self) -> str:
        """Set version to beta. Returns: New version string"""
        return self.set_suffix('beta')
    
    def set_dev(self) -> str:
        """Set version to dev. Returns: New version string"""
        return self.set_suffix('dev')
    
    def auto_add(self) -> str:
        """
        Automatically increment patch version.
        Alias for increment_patch().
        
        Returns:
            New version string
        """
        return self.increment_patch()
    
    def __str__(self) -> str:
        """String representation returns version."""
        return self.version
    
    def __repr__(self) -> str:
        """Repr shows class and version."""
        return f"VersionGet(version='{self.version}', file={self.version_file})"


def main():
    """Command-line interface for version_get."""
    parser = argparse.ArgumentParser(
        description='Manage version numbers in Python projects',
        formatter_class=CustomRichHelpFormatter,
        epilog="""
Examples:
  version_get                          # Show current version
  version_get --increment-major        # Increment major version
  version_get --increment-minor        # Increment minor version
  version_get --increment-patch        # Increment patch version
  version_get --set 2.0.0              # Set specific version
  version_get --set-alpha              # Set version to x.y.alpha
  version_get --path /path/to/project  # Specify project path
        """
    )
    
    parser.add_argument('--version', action='version', version=f'version_get {__version__}')
    parser.add_argument('-p', '--path', help='Path to project directory or version file')
    parser.add_argument('--create', action='store_true', 
                       help='Create version file if missing')
    
    # Version display
    parser.add_argument('-g', '--get', action='store_true',
                       help='Get current version (default action)')
    
    # Increment operations
    parser.add_argument('--increment-major', '--inc-major', action='store_true',
                       help='Increment major version (x.0.0)')
    parser.add_argument('--increment-minor', '--inc-minor', action='store_true',
                       help='Increment minor version (x.y.0)')
    parser.add_argument('--increment-patch', '--inc-patch', action='store_true',
                       help='Increment patch version (x.y.z)')
    parser.add_argument('--auto-add', action='store_true',
                       help='Auto-increment patch version')
    
    # Decrement operations
    parser.add_argument('--decrement-major', '--dec-major', action='store_true',
                       help='Decrement major version')
    parser.add_argument('--decrement-minor', '--dec-minor', action='store_true',
                       help='Decrement minor version')
    parser.add_argument('--decrement-patch', '--dec-patch', action='store_true',
                       help='Decrement patch version')
    
    # Set operations
    parser.add_argument('-s', '--set', metavar='VERSION',
                       help='Set specific version (e.g., 2.0.0)')
    parser.add_argument('--set-alpha', action='store_true',
                       help='Set version to x.y.alpha')
    parser.add_argument('--set-beta', action='store_true',
                       help='Set version to x.y.beta')
    parser.add_argument('--set-dev', action='store_true',
                       help='Set version to x.y.dev')
    parser.add_argument('--set-suffix', metavar='SUFFIX',
                       help='Set custom suffix (e.g., rc1, pre)')
    
    # Output options
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Only output version number')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        vg = VersionGet(path=args.path, create_if_missing=args.create)
        
        action_taken = False
        
        # Increment operations
        if args.increment_major:
            version = vg.increment_major()
            action_taken = True
            if not args.quiet:
                print(f"Incremented major version to: {version}")
        
        elif args.increment_minor:
            version = vg.increment_minor()
            action_taken = True
            if not args.quiet:
                print(f"Incremented minor version to: {version}")
        
        elif args.increment_patch or args.auto_add:
            version = vg.increment_patch()
            action_taken = True
            if not args.quiet:
                print(f"Incremented patch version to: {version}")
        
        # Decrement operations
        elif args.decrement_major:
            version = vg.decrement_major()
            action_taken = True
            if not args.quiet:
                print(f"Decremented major version to: {version}")
        
        elif args.decrement_minor:
            version = vg.decrement_minor()
            action_taken = True
            if not args.quiet:
                print(f"Decremented minor version to: {version}")
        
        elif args.decrement_patch:
            version = vg.decrement_patch()
            action_taken = True
            if not args.quiet:
                print(f"Decremented patch version to: {version}")
        
        # Set operations
        elif args.set:
            version = vg.set_version(args.set)
            action_taken = True
            if not args.quiet:
                print(f"Set version to: {version}")
        
        elif args.set_alpha:
            version = vg.set_alpha()
            action_taken = True
            if not args.quiet:
                print(f"Set version to: {version}")
        
        elif args.set_beta:
            version = vg.set_beta()
            action_taken = True
            if not args.quiet:
                print(f"Set version to: {version}")
        
        elif args.set_dev:
            version = vg.set_dev()
            action_taken = True
            if not args.quiet:
                print(f"Set version to: {version}")
        
        elif args.set_suffix:
            version = vg.set_suffix(args.set_suffix)
            action_taken = True
            if not args.quiet:
                print(f"Set version to: {version}")
        
        # Default action: show version
        if not action_taken or args.get:
            if args.quiet:
                print(vg.get())
            elif args.verbose:
                print(f"Version file: {vg.version_file}")
                print(f"Current version: {vg.get()}")
            else:
                print(vg.get())
        else:
            # For modification operations in quiet mode, output new version
            if args.quiet:
                print(vg.get())
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())