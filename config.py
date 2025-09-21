"""
Configuration settings for the Car and Pedestrian Tracking System.

This module contains all configurable parameters for the tracking system,
including detection parameters, file paths, and display settings.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CASCADE_DIR = PROJECT_ROOT / "cascades"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create directories if they don't exist
for directory in [DATA_DIR, CASCADE_DIR, OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

# Default cascade file paths
DEFAULT_CAR_CASCADE = CASCADE_DIR / "cars.xml"
DEFAULT_PEDESTRIAN_CASCADE = CASCADE_DIR / "haarcascade_fullbody.xml"

# Detection parameters
DETECTION_CONFIG = {
    'car': {
        'scaleFactor': 1.1,
        'minNeighbors': 3,
        'minSize': (30, 30),
        'maxSize': None
    },
    'pedestrian': {
        'scaleFactor': 1.1,
        'minNeighbors': 5,
        'minSize': (40, 80),
        'maxSize': None
    }
}

# Display settings
DISPLAY_CONFIG = {
    'colors': {
        'car': (255, 0, 0),          # Blue
        'car_shadow': (0, 0, 255),   # Red (for shadow effect)
        'pedestrian': (0, 255, 255)  # Yellow
    },
    'font_scale': 0.6,
    'font_thickness': 2,
    'rectangle_thickness': 2,
    'overlay_alpha': 0.7
}

# Video settings
VIDEO_CONFIG = {
    'default_fps': 30,
    'codec': 'mp4v',
    'extension': '.mp4'
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': PROJECT_ROOT / 'logs' / 'tracker.log'
}

# Create logs directory
LOGGING_CONFIG['file'].parent.mkdir(exist_ok=True)
