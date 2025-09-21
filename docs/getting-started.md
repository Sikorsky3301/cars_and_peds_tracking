# Getting Started

This guide will help you get up and running with the Car and Pedestrian Tracking System in just a few minutes.

## Prerequisites

- Python 3.8 or higher
- OpenCV 4.8 or higher
- A video file or webcam for testing

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cars_and_peds_tracking.git
   cd cars_and_peds_tracking
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download cascade files**
   - Download `cars.xml` from OpenCV repository
   - Download `haarcascade_fullbody.xml` from OpenCV repository
   - Place them in the project directory

## Your First Detection

### Using Command Line

```bash
# Run with default video file
python cars_and_peds.py

# Use webcam
python cars_and_peds.py --camera

# Specify custom video
python cars_and_peds.py --video path/to/video.mp4
```

### Using Python Code

```python
from cars_and_peds import CarPedestrianTracker

# Create tracker instance
tracker = CarPedestrianTracker()

# Process a video file
tracker.process_video('input.mp4')

# Process webcam stream
tracker.process_video(0)  # 0 for default camera
```

## Interactive Controls

During video processing:
- **K or Q**: Quit the application
- **S**: Save a screenshot
- **R**: Reset statistics

## Next Steps

- Learn about [Configuration](configuration.md) options
- Explore [Examples](examples.md) for different use cases
- Check the [API Reference](api-reference.md) for detailed documentation
