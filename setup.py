#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for version_get
"""

from setuptools import setup, find_packages
import os
import re

def get_version() -> str:
    """Get version from __version__.py file"""
    from pathlib import Path
    try:
        version_file = Path(__file__).parent / "__version__.py"
        if version_file.is_file():
            with open(version_file, "r") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        parts = line.split("=")
                        if len(parts) == 2:
                            return parts[1].strip().strip('"').strip("'")
    except:
        pass
    return "2.0.0"

def get_long_description():
    """Get long description from README"""
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name='version_get',
    version=get_version(),
    description='A robust version management utility for Python projects',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='cumulus13',
    author_email='cumulus13@gmail.com',
    url='https://github.com/cumulus13/version_get',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.9',
            'mypy>=0.900',
        ],
    },
    entry_points={
        'console_scripts': [
            'version_get=version_get.version_get:main',
            'vget=version_get.version_get:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control',
        'Topic :: Utilities',
    ],
    keywords='version versioning semver semantic-versioning version-management',
    project_urls={
        'Bug Reports': 'https://github.com/cumulus13/version_get/issues',
        'Source': 'https://github.com/cumulus13/version_get',
    },
)