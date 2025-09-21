# Examples

This page contains practical examples showing different ways to use the Car and Pedestrian Tracking System.

## Basic Examples

### Video File Processing

```python
from cars_and_peds import CarPedestrianTracker

# Initialize tracker
tracker = CarPedestrianTracker()

# Process video file
tracker.process_video('input.mp4', output_path='output.mp4')
```

### Webcam Processing

```python
# Process webcam stream
tracker.process_video(0)  # 0 for default camera
```

### Custom Cascade Files

```python
# Use custom cascade files
tracker = CarPedestrianTracker(
    car_cascade_path='custom_cars.xml',
    pedestrian_cascade_path='custom_peds.xml'
)
```

## Advanced Examples

### Performance Optimization

```python
# Optimize for speed
tracker.car_params = {
    'scaleFactor': 1.3,      # Larger steps = faster
    'minNeighbors': 2,        # Lower threshold = faster
    'minSize': (50, 50)       # Larger minimum = faster
}
```

### Accuracy Optimization

```python
# Optimize for accuracy
tracker.car_params = {
    'scaleFactor': 1.05,     # Smaller steps = more accurate
    'minNeighbors': 8,        # Higher threshold = fewer false positives
    'minSize': (20, 20)       # Smaller minimum = detect smaller objects
}
```

### Custom Colors

```python
# Customize colors (BGR format)
tracker.colors = {
    'car': (0, 255, 0),          # Green for cars
    'car_shadow': (0, 128, 0),   # Dark green shadow
    'pedestrian': (255, 0, 255)  # Magenta for pedestrians
}
```

## Command Line Examples

### Basic Usage

```bash
# Process default video
python cars_and_peds.py

# Use webcam
python cars_and_peds.py --camera

# Specify video file
python cars_and_peds.py --video path/to/video.mp4

# Save output
python cars_and_peds.py --video input.mp4 --output output.mp4
```

### Advanced Usage

```bash
# Use custom cascade files
python cars_and_peds.py --car-cascade custom_cars.xml --pedestrian-cascade custom_peds.xml

# Enable verbose logging
python cars_and_peds.py --verbose

# Use specific camera
python cars_and_peds.py --camera --video 1
```

## Integration Examples

### With Other Libraries

```python
import cv2
import numpy as np
from cars_and_peds import CarPedestrianTracker

# Initialize tracker
tracker = CarPedestrianTracker()

# Process frame by frame
cap = cv2.VideoCapture('video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect objects
    cars, pedestrians = tracker.detect_objects(frame)
    
    # Custom processing
    for (x, y, w, h) in cars:
        # Extract car region
        car_roi = frame[y:y+h, x:x+w]
        
        # Apply custom processing to car region
        # ... your custom code here ...
    
    # Display result
    cv2.imshow('Custom Processing', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Batch Processing

```python
import os
from pathlib import Path
from cars_and_peds import CarPedestrianTracker

# Initialize tracker
tracker = CarPedestrianTracker()

# Process multiple videos
video_dir = Path('videos')
output_dir = Path('output')

for video_file in video_dir.glob('*.mp4'):
    output_file = output_dir / f'processed_{video_file.name}'
    
    print(f"Processing {video_file.name}...")
    tracker.process_video(str(video_file), str(output_file))
    print(f"Saved to {output_file}")
```

## Performance Examples

### Monitoring Performance

```python
import time
from cars_and_peds import CarPedestrianTracker

tracker = CarPedestrianTracker()

# Track performance
start_time = time.time()
tracker.process_video('input.mp4')
end_time = time.time()

print(f"Processing time: {end_time - start_time:.2f} seconds")
print(f"Total frames: {tracker.frame_count}")
print(f"Average FPS: {tracker.frame_count / (end_time - start_time):.2f}")
```

### Memory Optimization

```python
# For large videos, process in chunks
def process_large_video(video_path, chunk_size=1000):
    tracker = CarPedestrianTracker()
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0
    chunk_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        cars, pedestrians = tracker.detect_objects(frame)
        # ... your processing ...
        
        frame_count += 1
        
        # Reset tracker every chunk_size frames to prevent memory buildup
        if frame_count % chunk_size == 0:
            chunk_count += 1
            print(f"Processed chunk {chunk_count}")
            tracker.frame_count = 0
            tracker.total_cars = 0
            tracker.total_pedestrians = 0
    
    cap.release()
```

## Troubleshooting Examples

### Handling Missing Files

```python
import os
from cars_and_peds import CarPedestrianTracker

def safe_initialize_tracker():
    try:
        # Check if cascade files exist
        if not os.path.exists('cars.xml'):
            print("cars.xml not found. Downloading...")
            # Add download logic here
        
        if not os.path.exists('haarcascade_fullbody.xml'):
            print("haarcascade_fullbody.xml not found. Downloading...")
            # Add download logic here
        
        return CarPedestrianTracker()
    
    except Exception as e:
        print(f"Error initializing tracker: {e}")
        return None

# Use safe initialization
tracker = safe_initialize_tracker()
if tracker:
    tracker.process_video('input.mp4')
```

### Error Handling

```python
import cv2
from cars_and_peds import CarPedestrianTracker

def robust_video_processing(video_path):
    tracker = CarPedestrianTracker()
    
    try:
        # Check if video file exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Try to open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"Video info: {fps} FPS, {frame_count} frames")
        
        # Process video
        tracker.process_video(video_path)
        
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'cap' in locals():
            cap.release()

# Use robust processing
robust_video_processing('input.mp4')
```
