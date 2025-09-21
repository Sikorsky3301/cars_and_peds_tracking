"""
Unit tests for the Car and Pedestrian Tracking System.

This module contains comprehensive tests for the CarPedestrianTracker class
and related functionality.
"""

import pytest
import cv2
import numpy as np
import tempfile
import os
from pathlib import Path

# Import the main module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from cars_and_peds import CarPedestrianTracker


class TestCarPedestrianTracker:
    """Test cases for CarPedestrianTracker class."""
    
    @pytest.fixture
    def sample_frame(self):
        """Create a sample frame for testing."""
        # Create a 640x480 BGR image
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        return frame
    
    @pytest.fixture
    def mock_cascade_files(self, tmp_path):
        """Create mock cascade files for testing."""
        car_cascade = tmp_path / "cars.xml"
        ped_cascade = tmp_path / "haarcascade_fullbody.xml"
        
        # Create minimal valid cascade files
        car_cascade.write_text("""<?xml version="1.0"?>
<opencv_storage>
<cascade type_id="opencv-cascade-classifier">
  <stageType>BOOST</stageType>
  <featureType>HAAR</featureType>
  <height>20</height>
  <width>20</width>
  <stageParams>
    <maxWeakCount>3</maxWeakCount>
  </stageParams>
  <featureParams>
    <maxCatCount>0</maxCatCount>
    <featSize>1</featSize>
    <mode>BASIC</mode>
  </featureParams>
  <stageNum>1</stageNum>
  <stages>
    <_>
      <maxWeakCount>3</maxWeakCount>
      <stageThreshold>-1.0</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>0 -1 0 -67108864</internalNodes>
          <leafValues>-1.0 1.0</leafValues>
        </_>
      </weakClassifiers>
    </_>
  </stages>
  <features>
    <_>
      <rects>
        <_>
          0 0 20 20 -1.
        </_>
      </rects>
      <tilted>0</tilted>
    </_>
  </features>
</cascade>
</opencv_storage>""")
        
        ped_cascade.write_text("""<?xml version="1.0"?>
<opencv_storage>
<cascade type_id="opencv-cascade-classifier">
  <stageType>BOOST</stageType>
  <featureType>HAAR</featureType>
  <height>20</height>
  <width>20</width>
  <stageParams>
    <maxWeakCount>3</maxWeakCount>
  </stageParams>
  <featureParams>
    <maxCatCount>0</maxCatCount>
    <featSize>1</featSize>
    <mode>BASIC</mode>
  </featureParams>
  <stageNum>1</stageNum>
  <stages>
    <_>
      <maxWeakCount>3</maxWeakCount>
      <stageThreshold>-1.0</stageThreshold>
      <weakClassifiers>
        <_>
          <internalNodes>0 -1 0 -67108864</internalNodes>
          <leafValues>-1.0 1.0</leafValues>
        </_>
      </weakClassifiers>
    </_>
  </stages>
  <features>
    <_>
      <rects>
        <_>
          0 0 20 20 -1.
        </_>
      </rects>
      <tilted>0</tilted>
    </_>
  </features>
</cascade>
</opencv_storage>""")
        
        return str(car_cascade), str(ped_cascade)
    
    def test_tracker_initialization(self, mock_cascade_files):
        """Test tracker initialization with valid cascade files."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        
        assert tracker.car_cascade_path == car_cascade
        assert tracker.pedestrian_cascade_path == ped_cascade
        assert tracker.car_tracker is not None
        assert tracker.pedestrian_tracker is not None
        assert tracker.frame_count == 0
        assert tracker.total_cars == 0
        assert tracker.total_pedestrians == 0
    
    def test_tracker_initialization_missing_cascade(self):
        """Test tracker initialization with missing cascade files."""
        with pytest.raises(FileNotFoundError):
            CarPedestrianTracker("nonexistent_cars.xml", "nonexistent_peds.xml")
    
    def test_detect_objects(self, mock_cascade_files, sample_frame):
        """Test object detection functionality."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        
        cars, pedestrians = tracker.detect_objects(sample_frame)
        
        # Should return lists (may be empty due to random image)
        assert isinstance(cars, list)
        assert isinstance(pedestrians, list)
    
    def test_draw_detections(self, mock_cascade_files, sample_frame):
        """Test drawing detections on frame."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        
        # Mock detections
        cars = [(100, 100, 50, 30)]  # x, y, w, h
        pedestrians = [(200, 200, 40, 80)]
        
        result_frame = tracker.draw_detections(sample_frame, cars, pedestrians)
        
        # Should return a frame with same dimensions
        assert result_frame.shape == sample_frame.shape
        assert result_frame.dtype == sample_frame.dtype
    
    def test_add_statistics_overlay(self, mock_cascade_files, sample_frame):
        """Test adding statistics overlay to frame."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        tracker.frame_count = 10
        
        result_frame = tracker.add_statistics_overlay(sample_frame)
        
        # Should return a frame with same dimensions
        assert result_frame.shape == sample_frame.shape
        assert result_frame.dtype == sample_frame.dtype
    
    def test_color_configuration(self, mock_cascade_files):
        """Test color configuration."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        
        # Check that colors are properly configured
        assert 'car' in tracker.colors
        assert 'car_shadow' in tracker.colors
        assert 'pedestrian' in tracker.colors
        
        # Colors should be BGR tuples
        for color in tracker.colors.values():
            assert len(color) == 3
            assert all(isinstance(c, int) for c in color)
    
    def test_detection_parameters(self, mock_cascade_files):
        """Test detection parameters configuration."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        
        # Check car parameters
        assert 'scaleFactor' in tracker.car_params
        assert 'minNeighbors' in tracker.car_params
        assert 'minSize' in tracker.car_params
        
        # Check pedestrian parameters
        assert 'scaleFactor' in tracker.pedestrian_params
        assert 'minNeighbors' in tracker.pedestrian_params
        assert 'minSize' in tracker.pedestrian_params
        
        # Parameter values should be reasonable
        assert tracker.car_params['scaleFactor'] > 1.0
        assert tracker.pedestrian_params['scaleFactor'] > 1.0
        assert tracker.car_params['minNeighbors'] > 0
        assert tracker.pedestrian_params['minNeighbors'] > 0


class TestUtilityFunctions:
    """Test utility functions and edge cases."""
    
    def test_frame_processing_edge_cases(self, mock_cascade_files):
        """Test frame processing with edge cases."""
        car_cascade, ped_cascade = mock_cascade_files
        tracker = CarPedestrianTracker(car_cascade, ped_cascade)
        
        # Test with empty frame
        empty_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        cars, pedestrians = tracker.detect_objects(empty_frame)
        assert isinstance(cars, list)
        assert isinstance(pedestrians, list)
        
        # Test with very small frame
        small_frame = np.zeros((10, 10, 3), dtype=np.uint8)
        cars, pedestrians = tracker.detect_objects(small_frame)
        assert isinstance(cars, list)
        assert isinstance(pedestrians, list)


if __name__ == "__main__":
    pytest.main([__file__])
