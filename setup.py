#!/usr/bin/env python3
"""
DōmAI - Intelligent Security Alliance
Setup script for package installation
"""

import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="domai",
    version="1.0.0",
    author="Joshua",
    author_email="joshua@domai.ai",
    description="MacOS Security Assistant with AI-powered guidance and education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshua/domai-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring"
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "mistralai>=0.0.7",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
        "rich>=10.0.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0"
    ],
    entry_points={
        "console_scripts": [
            "domai=domai.cli:cli"
        ]
    },
    package_data={
        "domai": [
            "config/*.json",
            "templates/*.md"
        ]
    },
    include_package_data=True,
    zip_safe=False
) 