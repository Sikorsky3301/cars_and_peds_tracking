#!/usr/bin/env python3
"""
Setup script for the Car and Pedestrian Tracking System.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = []
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="cars-and-peds-tracking",
    version="1.0.0",
    author="Rishi Raj",
    author_email="your.email@example.com",
    description="A robust computer vision application for real-time detection and tracking of cars and pedestrians",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cars_and_peds_tracking",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cars-and-peds=cars_and_peds:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.xml", "*.yml", "*.yaml", "*.md"],
    },
    keywords="computer-vision, opencv, object-detection, car-detection, pedestrian-detection, haar-cascade, tracking",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cars_and_peds_tracking/issues",
        "Source": "https://github.com/yourusername/cars_and_peds_tracking",
        "Documentation": "https://yourusername.github.io/cars_and_peds_tracking/",
    },
)
