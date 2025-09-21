# API Reference

Complete API documentation for the Car and Pedestrian Tracking System.

## CarPedestrianTracker Class

The main class for detecting and tracking cars and pedestrians in video streams.

### Constructor

```python
CarPedestrianTracker(car_cascade_path='cars.xml', pedestrian_cascade_path='haarcascade_fullbody.xml')
```

**Parameters**:
- `car_cascade_path` (str): Path to the car Haar cascade XML file
- `pedestrian_cascade_path` (str): Path to the pedestrian Haar cascade XML file

**Raises**:
- `FileNotFoundError`: If cascade files don't exist
- `RuntimeError`: If cascade files fail to load

**Example**:
```python
tracker = CarPedestrianTracker(
    car_cascade_path='custom_cars.xml',
    pedestrian_cascade_path='custom_peds.xml'
)
```

### Properties

#### `car_params`
Dictionary containing car detection parameters.

```python
tracker.car_params = {
    'scaleFactor': 1.1,      # Scale factor for image pyramid
    'minNeighbors': 3,        # Minimum neighbors for detection
    'minSize': (30, 30)       # Minimum object size (width, height)
}
```

#### `pedestrian_params`
Dictionary containing pedestrian detection parameters.

```python
tracker.pedestrian_params = {
    'scaleFactor': 1.1,      # Scale factor for image pyramid
    'minNeighbors': 5,        # Minimum neighbors for detection
    'minSize': (40, 80)       # Minimum object size (width, height)
}
```

#### `colors`
Dictionary containing colors for bounding boxes (BGR format).

```python
tracker.colors = {
    'car': (255, 0, 0),          # Blue for cars
    'car_shadow': (0, 0, 255),   # Red shadow effect
    'pedestrian': (0, 255, 255)  # Yellow for pedestrians
}
```

#### `frame_count`
Current frame number being processed.

#### `total_cars`
Total number of car detections across all frames.

#### `total_pedestrians`
Total number of pedestrian detections across all frames.

### Methods

#### `detect_objects(frame)`

Detect cars and pedestrians in a frame.

**Parameters**:
- `frame` (cv2.Mat): Input frame in BGR format

**Returns**:
- `Tuple[List[Tuple], List[Tuple]]`: (car_detections, pedestrian_detections)
  - Each detection is a tuple of (x, y, width, height)

**Example**:
```python
cars, pedestrians = tracker.detect_objects(frame)
for (x, y, w, h) in cars:
    print(f"Car detected at ({x}, {y}) with size {w}x{h}")
```

#### `draw_detections(frame, cars, pedestrians)`

Draw bounding boxes around detected objects.

**Parameters**:
- `frame` (cv2.Mat): Input frame
- `cars` (List[Tuple]): List of car detections (x, y, w, h)
- `pedestrians` (List[Tuple]): List of pedestrian detections (x, y, w, h)

**Returns**:
- `cv2.Mat`: Frame with drawn bounding boxes

**Example**:
```python
cars, pedestrians = tracker.detect_objects(frame)
frame_with_boxes = tracker.draw_detections(frame, cars, pedestrians)
cv2.imshow('Detections', frame_with_boxes)
```

#### `add_statistics_overlay(frame)`

Add statistics overlay to the frame.

**Parameters**:
- `frame` (cv2.Mat): Input frame

**Returns**:
- `cv2.Mat`: Frame with statistics overlay

**Example**:
```python
frame_with_stats = tracker.add_statistics_overlay(frame)
```

#### `process_video(video_source, output_path=None)`

Process a video file or webcam stream.

**Parameters**:
- `video_source` (Union[str, int]): Path to video file or camera index
- `output_path` (Optional[str]): Path to save output video

**Example**:
```python
# Process video file
tracker.process_video('input.mp4', output_path='output.mp4')

# Process webcam
tracker.process_video(0)

# Process specific camera
tracker.process_video(1)
```

## Command Line Interface

### Basic Usage

```bash
python cars_and_peds.py [OPTIONS]
```

### Options

#### `--video`, `-v`
Path to input video file.

**Default**: `peds_and_cars.mp4`

**Example**:
```bash
python cars_and_peds.py --video path/to/video.mp4
```

#### `--camera`, `-c`
Use webcam instead of video file.

**Example**:
```bash
python cars_and_peds.py --camera
```

#### `--output`, `-o`
Path to save output video.

**Example**:
```bash
python cars_and_peds.py --video input.mp4 --output output.mp4
```

#### `--car-cascade`
Path to car cascade file.

**Default**: `cars.xml`

**Example**:
```bash
python cars_and_peds.py --car-cascade custom_cars.xml
```

#### `--pedestrian-cascade`
Path to pedestrian cascade file.

**Default**: `haarcascade_fullbody.xml`

**Example**:
```bash
python cars_and_peds.py --pedestrian-cascade custom_peds.xml
```

#### `--verbose`
Enable verbose logging.

**Example**:
```bash
python cars_and_peds.py --verbose
```

### Interactive Controls

During video processing:

- **K or Q**: Quit the application
- **S**: Save a screenshot of the current frame
- **R**: Reset statistics counters

## Configuration Module

The `config.py` module provides centralized configuration settings.

### Paths

```python
from config import PROJECT_ROOT, DATA_DIR, CASCADE_DIR, OUTPUT_DIR

# Project directories
PROJECT_ROOT    # Project root directory
DATA_DIR        # Data files directory
CASCADE_DIR     # Cascade files directory
OUTPUT_DIR      # Output files directory
```

### Detection Configuration

```python
from config import DETECTION_CONFIG

# Car detection parameters
car_config = DETECTION_CONFIG['car']

# Pedestrian detection parameters
pedestrian_config = DETECTION_CONFIG['pedestrian']
```

### Display Configuration

```python
from config import DISPLAY_CONFIG

# Colors for bounding boxes
colors = DISPLAY_CONFIG['colors']

# Display settings
font_scale = DISPLAY_CONFIG['font_scale']
font_thickness = DISPLAY_CONFIG['font_thickness']
```

### Video Configuration

```python
from config import VIDEO_CONFIG

# Default FPS
default_fps = VIDEO_CONFIG['default_fps']

# Video codec
codec = VIDEO_CONFIG['codec']
```

## Error Handling

### Common Exceptions

#### `FileNotFoundError`
Raised when cascade files or video files are not found.

```python
try:
    tracker = CarPedestrianTracker('missing_file.xml')
except FileNotFoundError as e:
    print(f"Cascade file not found: {e}")
```

#### `RuntimeError`
Raised when cascade files fail to load or video cannot be opened.

```python
try:
    tracker.process_video('corrupted_video.mp4')
except RuntimeError as e:
    print(f"Video processing error: {e}")
```

#### `KeyboardInterrupt`
Raised when user interrupts the program (Ctrl+C).

```python
try:
    tracker.process_video('long_video.mp4')
except KeyboardInterrupt:
    print("Processing interrupted by user")
```

## Type Hints

The module uses type hints for better code documentation and IDE support.

```python
from typing import Tuple, List, Optional
import cv2

def detect_objects(self, frame: cv2.Mat) -> Tuple[List[Tuple], List[Tuple]]:
    """
    Detect cars and pedestrians in a frame.
    
    Args:
        frame: Input frame in BGR format
        
    Returns:
        Tuple of (car_detections, pedestrian_detections)
    """
    pass
```

## Logging

The module uses Python's logging system for debugging and monitoring.

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about program execution
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for serious problems

### Configuration

```python
import logging

# Set log level
logging.getLogger().setLevel(logging.DEBUG)

# Custom formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
```

### Usage

```python
logger = logging.getLogger(__name__)

logger.info("Starting video processing")
logger.debug(f"Frame {frame_count} processed")
logger.error(f"Failed to load cascade: {e}")
```
