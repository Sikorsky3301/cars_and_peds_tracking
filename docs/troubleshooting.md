# Troubleshooting

This guide helps you resolve common issues when using the Car and Pedestrian Tracking System.

## Common Issues

### 1. Cascade Files Not Found

**Error**: `FileNotFoundError: Car cascade file not found: cars.xml`

**Solution**:
1. Download the required cascade files:
   - `cars.xml` from OpenCV repository
   - `haarcascade_fullbody.xml` from OpenCV repository
2. Place them in the project directory
3. Or specify custom paths:
   ```python
   tracker = CarPedestrianTracker(
       car_cascade_path='path/to/cars.xml',
       pedestrian_cascade_path='path/to/haarcascade_fullbody.xml'
   )
   ```

### 2. OpenCV Installation Issues

**Error**: `ImportError: No module named 'cv2'`

**Solution**:
```bash
# Install OpenCV
pip install opencv-python

# Or with contrib modules
pip install opencv-contrib-python

# For specific version
pip install opencv-python==4.8.0
```

### 3. Video File Cannot Be Opened

**Error**: `Error: Could not open video source`

**Solutions**:
1. Check file path is correct
2. Verify video file is not corrupted
3. Try different video formats (MP4, AVI, MOV)
4. Check file permissions
5. Use absolute paths:
   ```python
   tracker.process_video('/absolute/path/to/video.mp4')
   ```

### 4. Webcam Not Working

**Error**: `Error: Could not open video source 0`

**Solutions**:
1. Check if camera is connected and working
2. Try different camera indices:
   ```python
   tracker.process_video(1)  # Try camera index 1
   tracker.process_video(2)  # Try camera index 2
   ```
3. Close other applications using the camera
4. Check camera permissions (especially on macOS/Linux)

### 5. Poor Detection Performance

**Symptoms**: Missing detections, false positives, slow performance

**Solutions**:

**For Better Accuracy**:
```python
tracker.car_params = {
    'scaleFactor': 1.05,     # Smaller steps
    'minNeighbors': 8,        # Higher threshold
    'minSize': (20, 20)       # Smaller minimum size
}
```

**For Better Performance**:
```python
tracker.car_params = {
    'scaleFactor': 1.3,      # Larger steps
    'minNeighbors': 2,        # Lower threshold
    'minSize': (50, 50)       # Larger minimum size
}
```

### 6. Memory Issues

**Error**: Out of memory, slow performance

**Solutions**:
1. Process videos in smaller chunks
2. Reduce video resolution
3. Use more efficient parameters
4. Close other applications
5. Add memory monitoring:
   ```python
   import psutil
   
   def monitor_memory():
       memory = psutil.virtual_memory()
       print(f"Memory usage: {memory.percent}%")
   ```

### 7. Output Video Issues

**Error**: Output video not saved or corrupted

**Solutions**:
1. Check write permissions in output directory
2. Use different codec:
   ```python
   # In process_video method, change:
   fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Instead of 'mp4v'
   ```
3. Ensure output directory exists
4. Use absolute paths for output

### 8. Import Errors

**Error**: `ModuleNotFoundError`

**Solutions**:
1. Install missing dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Check Python version (requires 3.8+)
3. Use virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Performance Optimization

### Hardware Recommendations

**Minimum Requirements**:
- CPU: 2+ cores, 2.0+ GHz
- RAM: 4GB+
- Storage: 1GB free space

**Recommended**:
- CPU: 4+ cores, 3.0+ GHz
- RAM: 8GB+
- GPU: Optional, but improves performance with CUDA

### Software Optimization

1. **Use appropriate parameters**:
   ```python
   # For real-time processing
   tracker.car_params = {'scaleFactor': 1.2, 'minNeighbors': 3}
   
   # For batch processing
   tracker.car_params = {'scaleFactor': 1.05, 'minNeighbors': 8}
   ```

2. **Resize input video**:
   ```python
   import cv2
   
   def resize_video(input_path, output_path, scale=0.5):
       cap = cv2.VideoCapture(input_path)
       width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
       height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
       
       fourcc = cv2.VideoWriter_fourcc(*'mp4v')
       out = cv2.VideoWriter(output_path, fourcc, 30, (width, height))
       
       while True:
           ret, frame = cap.read()
           if not ret:
               break
           resized = cv2.resize(frame, (width, height))
           out.write(resized)
       
       cap.release()
       out.release()
   ```

3. **Use multiprocessing for batch processing**:
   ```python
   from multiprocessing import Pool
   
   def process_video_file(video_path):
       tracker = CarPedestrianTracker()
       output_path = f"processed_{video_path}"
       tracker.process_video(video_path, output_path)
       return output_path
   
   # Process multiple videos in parallel
   video_files = ['video1.mp4', 'video2.mp4', 'video3.mp4']
   with Pool() as pool:
       results = pool.map(process_video_file, video_files)
   ```

## Debug Mode

Enable debug mode for detailed logging:

```python
import logging

# Enable debug logging
logging.getLogger().setLevel(logging.DEBUG)

# Or use command line
python cars_and_peds.py --verbose
```

## Getting Help

1. **Check the logs**: Look for error messages in the console output
2. **Test with sample data**: Try with a simple video file first
3. **Verify installation**: Run `python -c "import cv2; print(cv2.__version__)"`
4. **Check GitHub issues**: Look for similar problems in the repository
5. **Create an issue**: Provide detailed error information and system details

## System-Specific Issues

### Windows

- Install Visual C++ Redistributable
- Use Windows Subsystem for Linux (WSL) if needed
- Check antivirus software blocking camera access

### macOS

- Grant camera permissions in System Preferences
- Install Xcode command line tools: `xcode-select --install`
- Use Homebrew for easier package management

### Linux

- Install OpenCV dependencies:
  ```bash
  sudo apt-get install python3-opencv
  sudo apt-get install libopencv-dev
  ```
- Check camera permissions: `ls /dev/video*`
- Install missing codecs if needed

## Reporting Issues

When reporting issues, include:

1. **System information**:
   - Operating system and version
   - Python version
   - OpenCV version
   - Hardware specifications

2. **Error details**:
   - Complete error message
   - Steps to reproduce
   - Sample video file (if applicable)

3. **Environment**:
   - Virtual environment used
   - Dependencies installed
   - Configuration files

Use the issue template provided in the repository for best results.
