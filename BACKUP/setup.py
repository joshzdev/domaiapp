#!/usr/bin/env python3
"""
DōmAI - Intelligent Security Alliance
Setup script for package installation
"""

import os
from setuptools import setup, find_packages

setup(
    name="domai",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography>=3.4.7",
        "psutil>=5.8.0",
        "pyobjc-core>=9.2",
        "pyobjc-framework-Cocoa>=9.2",
        "pyobjc-framework-Security>=9.2",
        "pyobjc-framework-SystemConfiguration>=9.2",
        "bcrypt>=3.2.0",
        "pydantic>=1.8.2",
        "watchdog>=2.1.0",
        "scapy>=2.4.5",
        "pyOpenSSL>=20.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-asyncio>=0.15.1",
            "pytest-cov>=2.12.1",
            "black>=21.7b0",
            "flake8>=3.9.2",
            "mypy>=0.910",
            "isort>=5.9.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "domai=domai.cli:main",
        ],
    },
    author="DōmAI Security Alliance",
    author_email="humans@domai.dev",
    description="Native macOS security & maintenance with natural language interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/domai-security/domai",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
) 