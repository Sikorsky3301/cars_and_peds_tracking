#!/usr/bin/env python3
"""
Basic usage examples for the Car and Pedestrian Tracking System.

This script demonstrates various ways to use the tracking system
with different input sources and configurations.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import the main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from cars_and_peds import CarPedestrianTracker


def example_video_file():
    """Example: Process a video file."""
    print("Example 1: Processing a video file")
    
    # Initialize tracker
    tracker = CarPedestrianTracker()
    
    # Process video file
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        tracker.process_video(video_path, output_path="output_with_detections.mp4")
    else:
        print(f"Video file {video_path} not found. Please provide a valid video file.")


def example_webcam():
    """Example: Process webcam stream."""
    print("Example 2: Processing webcam stream")
    
    # Initialize tracker
    tracker = CarPedestrianTracker()
    
    # Process webcam (camera index 0)
    print("Starting webcam processing. Press 'K' or 'Q' to quit.")
    tracker.process_video(0)


def example_custom_parameters():
    """Example: Using custom detection parameters."""
    print("Example 3: Custom detection parameters")
    
    # Initialize tracker with custom cascade files
    tracker = CarPedestrianTracker(
        car_cascade_path='cars.xml',
        pedestrian_cascade_path='haarcascade_fullbody.xml'
    )
    
    # Customize detection parameters for better performance
    tracker.car_params = {
        'scaleFactor': 1.2,      # Faster detection
        'minNeighbors': 4,        # Fewer false positives
        'minSize': (40, 40)       # Larger minimum size
    }
    
    tracker.pedestrian_params = {
        'scaleFactor': 1.15,
        'minNeighbors': 6,
        'minSize': (50, 100)
    }
    
    # Process video with custom parameters
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        tracker.process_video(video_path)
    else:
        print(f"Video file {video_path} not found.")


def example_custom_colors():
    """Example: Using custom colors for detections."""
    print("Example 4: Custom colors")
    
    # Initialize tracker
    tracker = CarPedestrianTracker()
    
    # Customize colors (BGR format)
    tracker.colors = {
        'car': (0, 255, 0),          # Green for cars
        'car_shadow': (0, 128, 0),   # Dark green shadow
        'pedestrian': (255, 0, 255)  # Magenta for pedestrians
    }
    
    # Process video with custom colors
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        tracker.process_video(video_path)
    else:
        print(f"Video file {video_path} not found.")


def example_statistics_tracking():
    """Example: Tracking statistics and performance."""
    print("Example 5: Statistics tracking")
    
    # Initialize tracker
    tracker = CarPedestrianTracker()
    
    # Process video and monitor statistics
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        print("Processing video and tracking statistics...")
        tracker.process_video(video_path)
        
        # Print final statistics
        print(f"\nFinal Statistics:")
        print(f"Total frames processed: {tracker.frame_count}")
        print(f"Total car detections: {tracker.total_cars}")
        print(f"Total pedestrian detections: {tracker.total_pedestrians}")
        
        if tracker.frame_count > 0:
            avg_cars_per_frame = tracker.total_cars / tracker.frame_count
            avg_peds_per_frame = tracker.total_pedestrians / tracker.frame_count
            print(f"Average cars per frame: {avg_cars_per_frame:.2f}")
            print(f"Average pedestrians per frame: {avg_peds_per_frame:.2f}")
    else:
        print(f"Video file {video_path} not found.")


def main():
    """Run all examples."""
    print("Car and Pedestrian Tracking System - Examples")
    print("=" * 50)
    
    # Check if cascade files exist
    if not os.path.exists('cars.xml') or not os.path.exists('haarcascade_fullbody.xml'):
        print("Warning: Required cascade files not found!")
        print("Please download cars.xml and haarcascade_fullbody.xml from OpenCV repository.")
        print("Continuing with examples (will fail if cascade files are missing)...\n")
    
    try:
        # Run examples
        example_video_file()
        print()
        
        example_custom_parameters()
        print()
        
        example_custom_colors()
        print()
        
        example_statistics_tracking()
        print()
        
        # Uncomment to test webcam (requires camera)
        # example_webcam()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have:")
        print("1. OpenCV installed")
        print("2. Cascade files (cars.xml, haarcascade_fullbody.xml)")
        print("3. A sample video file named 'sample_video.mp4'")


if __name__ == "__main__":
    main()
