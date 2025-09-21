# Configuration

This guide covers all configuration options available in the Car and Pedestrian Tracking System.

## Detection Parameters

### Car Detection

```python
car_params = {
    'scaleFactor': 1.1,      # Scale factor for image pyramid
    'minNeighbors': 3,        # Minimum neighbors for detection
    'minSize': (30, 30)       # Minimum object size (width, height)
}
```

### Pedestrian Detection

```python
pedestrian_params = {
    'scaleFactor': 1.1,      # Scale factor for image pyramid
    'minNeighbors': 5,        # Minimum neighbors for detection
    'minSize': (40, 80)       # Minimum object size (width, height)
}
```

## Visual Customization

### Colors

```python
colors = {
    'car': (255, 0, 0),          # Blue for cars (BGR format)
    'car_shadow': (0, 0, 255),   # Red shadow effect
    'pedestrian': (0, 255, 255)  # Yellow for pedestrians
}
```

### Display Settings

```python
display_settings = {
    'font_scale': 0.6,           # Text size
    'font_thickness': 2,          # Text thickness
    'rectangle_thickness': 2,     # Bounding box thickness
    'overlay_alpha': 0.7         # Statistics overlay transparency
}
```

## Performance Tuning

### For Better Performance

1. **Increase `minNeighbors`**: Reduces false positives but may miss some objects
2. **Increase `minSize`**: Skip smaller objects for faster processing
3. **Adjust `scaleFactor`**: Smaller values = more detection scales = slower but more accurate

### For Higher Accuracy

1. **Decrease `minNeighbors`**: More sensitive detection
2. **Decrease `minSize`**: Detect smaller objects
3. **Use smaller `scaleFactor`**: More detection scales

## Cascade Files

### Custom Cascade Files

```python
tracker = CarPedestrianTracker(
    car_cascade_path='custom_cars.xml',
    pedestrian_cascade_path='custom_peds.xml'
)
```

### Cascade File Sources

- OpenCV repository: Contains standard cascade files
- Custom training: Train your own cascades for specific scenarios
- Third-party: Use community-contributed cascade files

## Logging Configuration

```python
import logging

# Set log level
logging.getLogger().setLevel(logging.DEBUG)

# Or use command line
python cars_and_peds.py --verbose
```

## Environment Variables

```bash
# Set default video source
export DEFAULT_VIDEO_SOURCE="path/to/video.mp4"

# Set output directory
export OUTPUT_DIR="path/to/output"

# Set log level
export LOG_LEVEL="DEBUG"
```
