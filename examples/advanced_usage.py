#!/usr/bin/env python3
"""
Advanced usage examples for the Car and Pedestrian Tracking System.

This script demonstrates advanced features like custom detection algorithms,
performance optimization, and integration with other libraries.
"""

import sys
import os
import time
import cv2
import numpy as np
from pathlib import Path

# Add parent directory to path to import the main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from cars_and_peds import CarPedestrianTracker


class AdvancedTracker(CarPedestrianTracker):
    """Extended tracker with additional features."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detection_history = []
        self.performance_metrics = {
            'fps': [],
            'detection_time': [],
            'frame_processing_time': []
        }
    
    def detect_objects_with_tracking(self, frame):
        """Enhanced detection with basic tracking."""
        start_time = time.time()
        
        # Get detections
        cars, pedestrians = self.detect_objects(frame)
        
        # Store detection history for simple tracking
        current_detections = {
            'frame': self.frame_count,
            'cars': cars,
            'pedestrians': pedestrians,
            'timestamp': time.time()
        }
        self.detection_history.append(current_detections)
        
        # Keep only last 30 frames for tracking
        if len(self.detection_history) > 30:
            self.detection_history.pop(0)
        
        # Calculate detection time
        detection_time = time.time() - start_time
        self.performance_metrics['detection_time'].append(detection_time)
        
        return cars, pedestrians
    
    def draw_detections_with_tracking(self, frame, cars, pedestrians):
        """Enhanced drawing with tracking information."""
        # Draw standard detections
        frame = self.draw_detections(frame, cars, pedestrians)
        
        # Add tracking information
        if len(self.detection_history) > 1:
            # Calculate movement for cars
            for i, (x, y, w, h) in enumerate(cars):
                # Simple tracking: find closest car in previous frame
                if len(self.detection_history) > 1:
                    prev_cars = self.detection_history[-2]['cars']
                    if prev_cars:
                        # Find closest previous detection
                        min_dist = float('inf')
                        for px, py, pw, ph in prev_cars:
                            dist = np.sqrt((x - px)**2 + (y - py)**2)
                            if dist < min_dist:
                                min_dist = dist
                        
                        # Draw movement indicator if car moved significantly
                        if min_dist < 100:  # Within reasonable tracking distance
                            cv2.putText(frame, f'Moving', (x, y-30), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        return frame
    
    def add_performance_overlay(self, frame):
        """Add performance metrics overlay."""
        # Calculate current FPS
        if len(self.performance_metrics['detection_time']) > 0:
            avg_detection_time = np.mean(self.performance_metrics['detection_time'][-10:])
            current_fps = 1.0 / avg_detection_time if avg_detection_time > 0 else 0
            self.performance_metrics['fps'].append(current_fps)
        
        # Create overlay
        overlay = frame.copy()
        
        # Performance metrics text
        fps_text = f"FPS: {current_fps:.1f}" if 'current_fps' in locals() else "FPS: --"
        detection_time_text = f"Detection: {avg_detection_time*1000:.1f}ms" if 'avg_detection_time' in locals() else "Detection: --ms"
        
        performance_text = [
            "Performance Metrics:",
            fps_text,
            detection_time_text,
            f"Total Detections: {len(self.detection_history)}",
            "",
            "Advanced Features:",
            "- Object tracking",
            "- Performance monitoring",
            "- Movement detection"
        ]
        
        # Draw semi-transparent background
        cv2.rectangle(overlay, (frame.shape[1] - 300, 10), (frame.shape[1] - 10, 200), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw text
        y_offset = 30
        for text in performance_text:
            if text:  # Skip empty strings
                cv2.putText(frame, text, (frame.shape[1] - 290, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            y_offset += 20
        
        return frame
    
    def process_video_with_advanced_features(self, video_source, output_path=None):
        """Process video with advanced features enabled."""
        # Initialize video capture
        if isinstance(video_source, str) and video_source.isdigit():
            video_source = int(video_source)
        
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"Error: Could not open video source {video_source}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Video properties: {width}x{height} @ {fps} FPS")
        print("Advanced features enabled: tracking, performance monitoring")
        
        # Setup video writer if output path is provided
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"Output video will be saved to: {output_path}")
        
        try:
            while True:
                frame_start_time = time.time()
                ret, frame = cap.read()
                
                if not ret:
                    print("End of video stream")
                    break
                
                self.frame_count += 1
                
                # Detect objects with tracking
                cars, pedestrians = self.detect_objects_with_tracking(frame)
                
                # Update statistics
                self.total_cars += len(cars)
                self.total_pedestrians += len(pedestrians)
                
                # Draw detections with tracking info
                frame = self.draw_detections_with_tracking(frame, cars, pedestrians)
                
                # Add performance overlay
                frame = self.add_performance_overlay(frame)
                
                # Add standard statistics overlay
                frame = self.add_statistics_overlay(frame)
                
                # Write frame to output video if writer is available
                if writer:
                    writer.write(frame)
                
                # Display frame
                cv2.imshow('Advanced Car and Pedestrian Detector', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key in [ord('k'), ord('K'), ord('q'), ord('Q')]:
                    print("Quit requested by user")
                    break
                elif key in [ord('s'), ord('S')]:
                    screenshot_path = f"advanced_screenshot_frame_{self.frame_count}.jpg"
                    cv2.imwrite(screenshot_path, frame)
                    print(f"Advanced screenshot saved: {screenshot_path}")
                elif key in [ord('r'), ord('R')]:
                    self.frame_count = 0
                    self.total_cars = 0
                    self.total_pedestrians = 0
                    self.detection_history.clear()
                    self.performance_metrics = {
                        'fps': [],
                        'detection_time': [],
                        'frame_processing_time': []
                    }
                    print("Statistics and tracking data reset")
                
                # Calculate frame processing time
                frame_time = time.time() - frame_start_time
                self.performance_metrics['frame_processing_time'].append(frame_time)
        
        except KeyboardInterrupt:
            print("Interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()
            
            # Print final performance statistics
            print(f"\nFinal Performance Statistics:")
            print(f"Total frames processed: {self.frame_count}")
            print(f"Total car detections: {self.total_cars}")
            print(f"Total pedestrian detections: {self.total_pedestrians}")
            
            if self.performance_metrics['fps']:
                avg_fps = np.mean(self.performance_metrics['fps'])
                print(f"Average FPS: {avg_fps:.2f}")
            
            if self.performance_metrics['detection_time']:
                avg_detection_time = np.mean(self.performance_metrics['detection_time'])
                print(f"Average detection time: {avg_detection_time*1000:.2f}ms")
            
            if self.performance_metrics['frame_processing_time']:
                avg_frame_time = np.mean(self.performance_metrics['frame_processing_time'])
                print(f"Average frame processing time: {avg_frame_time*1000:.2f}ms")


def example_advanced_tracking():
    """Example: Advanced tracking with performance monitoring."""
    print("Advanced Example: Enhanced tracking with performance monitoring")
    
    # Initialize advanced tracker
    tracker = AdvancedTracker()
    
    # Process video with advanced features
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        tracker.process_video_with_advanced_features(
            video_path, 
            output_path="advanced_output.mp4"
        )
    else:
        print(f"Video file {video_path} not found.")


def example_optimized_detection():
    """Example: Optimized detection for better performance."""
    print("Optimized Example: Performance-optimized detection")
    
    # Initialize tracker with optimized parameters
    tracker = CarPedestrianTracker()
    
    # Optimize for speed
    tracker.car_params = {
        'scaleFactor': 1.3,      # Larger steps = faster
        'minNeighbors': 2,        # Lower threshold = faster
        'minSize': (50, 50)       # Larger minimum = faster
    }
    
    tracker.pedestrian_params = {
        'scaleFactor': 1.3,
        'minNeighbors': 3,
        'minSize': (60, 120)
    }
    
    print("Optimized parameters for speed:")
    print(f"Car params: {tracker.car_params}")
    print(f"Pedestrian params: {tracker.pedestrian_params}")
    
    # Process video
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        tracker.process_video(video_path, output_path="optimized_output.mp4")
    else:
        print(f"Video file {video_path} not found.")


def example_accuracy_optimized():
    """Example: Accuracy-optimized detection."""
    print("Accuracy Example: High-accuracy detection")
    
    # Initialize tracker with accuracy-optimized parameters
    tracker = CarPedestrianTracker()
    
    # Optimize for accuracy
    tracker.car_params = {
        'scaleFactor': 1.05,     # Smaller steps = more accurate
        'minNeighbors': 8,        # Higher threshold = fewer false positives
        'minSize': (20, 20)       # Smaller minimum = detect smaller objects
    }
    
    tracker.pedestrian_params = {
        'scaleFactor': 1.05,
        'minNeighbors': 10,
        'minSize': (30, 60)
    }
    
    print("Accuracy-optimized parameters:")
    print(f"Car params: {tracker.car_params}")
    print(f"Pedestrian params: {tracker.pedestrian_params}")
    
    # Process video
    video_path = "sample_video.mp4"
    if os.path.exists(video_path):
        tracker.process_video(video_path, output_path="accuracy_output.mp4")
    else:
        print(f"Video file {video_path} not found.")


def main():
    """Run advanced examples."""
    print("Advanced Car and Pedestrian Tracking System - Examples")
    print("=" * 60)
    
    # Check if cascade files exist
    if not os.path.exists('cars.xml') or not os.path.exists('haarcascade_fullbody.xml'):
        print("Warning: Required cascade files not found!")
        print("Please download cars.xml and haarcascade_fullbody.xml from OpenCV repository.")
        print("Continuing with examples (will fail if cascade files are missing)...\n")
    
    try:
        # Run advanced examples
        example_advanced_tracking()
        print()
        
        example_optimized_detection()
        print()
        
        example_accuracy_optimized()
        print()
        
    except Exception as e:
        print(f"Error running advanced examples: {e}")
        print("Make sure you have:")
        print("1. OpenCV installed")
        print("2. Cascade files (cars.xml, haarcascade_fullbody.xml)")
        print("3. A sample video file named 'sample_video.mp4'")


if __name__ == "__main__":
    main()
