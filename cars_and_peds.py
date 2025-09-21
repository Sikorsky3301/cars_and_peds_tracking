#!/usr/bin/env python3
"""
Car and Pedestrian Tracking System

A computer vision application that detects and tracks cars and pedestrians 
in video streams using OpenCV and Haar Cascade classifiers.

Author: Rishi Raj
License: MIT
"""

import cv2
import argparse
import sys
import os
from pathlib import Path
from typing import Tuple, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CarPedestrianTracker:
    """
    A class for tracking cars and pedestrians in video streams.
    
    This class provides functionality to detect and track vehicles and pedestrians
    using Haar Cascade classifiers with OpenCV.
    """
    
    def __init__(self, car_cascade_path: str = 'cars.xml', 
                 pedestrian_cascade_path: str = 'haarcascade_fullbody.xml'):
        """
        Initialize the tracker with cascade classifier files.
        
        Args:
            car_cascade_path: Path to the car Haar cascade XML file
            pedestrian_cascade_path: Path to the pedestrian Haar cascade XML file
        """
        self.car_cascade_path = car_cascade_path
        self.pedestrian_cascade_path = pedestrian_cascade_path
        
        # Initialize cascade classifiers
        self.car_tracker = self._load_cascade(car_cascade_path, "Car")
        self.pedestrian_tracker = self._load_cascade(pedestrian_cascade_path, "Pedestrian")
        
        # Detection parameters
        self.car_params = {
            'scaleFactor': 1.1,
            'minNeighbors': 3,
            'minSize': (30, 30)
        }
        
        self.pedestrian_params = {
            'scaleFactor': 1.1,
            'minNeighbors': 5,
            'minSize': (40, 80)
        }
        
        # Colors for bounding boxes (BGR format)
        self.colors = {
            'car': (255, 0, 0),      # Blue
            'car_shadow': (0, 0, 255),  # Red (for shadow effect)
            'pedestrian': (0, 255, 255)  # Yellow
        }
        
        # Statistics
        self.frame_count = 0
        self.total_cars = 0
        self.total_pedestrians = 0
    
    def _load_cascade(self, cascade_path: str, detector_type: str) -> cv2.CascadeClassifier:
        """
        Load a Haar cascade classifier from file.
        
        Args:
            cascade_path: Path to the cascade XML file
            detector_type: Type of detector (for logging purposes)
            
        Returns:
            Loaded cascade classifier
            
        Raises:
            FileNotFoundError: If cascade file doesn't exist
            RuntimeError: If cascade fails to load
        """
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"{detector_type} cascade file not found: {cascade_path}")
        
        cascade = cv2.CascadeClassifier(cascade_path)
        if cascade.empty():
            raise RuntimeError(f"Failed to load {detector_type} cascade: {cascade_path}")
        
        logger.info(f"Successfully loaded {detector_type} cascade: {cascade_path}")
        return cascade
    
    def detect_objects(self, frame: cv2.Mat) -> Tuple[List[Tuple], List[Tuple]]:
        """
        Detect cars and pedestrians in a frame.
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Tuple of (car_detections, pedestrian_detections)
        """
        # Convert to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect cars and pedestrians
        cars = self.car_tracker.detectMultiScale(gray, **self.car_params)
        pedestrians = self.pedestrian_tracker.detectMultiScale(gray, **self.pedestrian_params)
        
        return cars, pedestrians
    
    def draw_detections(self, frame: cv2.Mat, cars: List[Tuple], 
                       pedestrians: List[Tuple]) -> cv2.Mat:
        """
        Draw bounding boxes around detected objects.
        
        Args:
            frame: Input frame
            cars: List of car detections (x, y, w, h)
            pedestrians: List of pedestrian detections (x, y, w, h)
            
        Returns:
            Frame with drawn bounding boxes
        """
        # Draw car bounding boxes with shadow effect
        for (x, y, w, h) in cars:
            # Shadow effect
            cv2.rectangle(frame, (x+1, y+1), (x+w, y+h), self.colors['car_shadow'], 2)
            # Main rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), self.colors['car'], 2)
            # Label
            cv2.putText(frame, 'Car', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['car'], 2)
        
        # Draw pedestrian bounding boxes
        for (x, y, w, h) in pedestrians:
            cv2.rectangle(frame, (x, y), (x+w, y+h), self.colors['pedestrian'], 2)
            # Label
            cv2.putText(frame, 'Pedestrian', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['pedestrian'], 2)
        
        return frame
    
    def add_statistics_overlay(self, frame: cv2.Mat) -> cv2.Mat:
        """
        Add statistics overlay to the frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Frame with statistics overlay
        """
        # Create overlay
        overlay = frame.copy()
        
        # Statistics text
        stats_text = [
            f"Frame: {self.frame_count}",
            f"Cars: {len(self.detect_objects(frame)[0])}",
            f"Pedestrians: {len(self.detect_objects(frame)[1])}",
            "",
            "Controls:",
            "K/Q - Quit",
            "S - Save screenshot",
            "R - Reset statistics"
        ]
        
        # Draw semi-transparent background
        cv2.rectangle(overlay, (10, 10), (250, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw text
        y_offset = 30
        for text in stats_text:
            if text:  # Skip empty strings
                cv2.putText(frame, text, (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
        
        return frame
    
    def process_video(self, video_source: str, output_path: Optional[str] = None):
        """
        Process a video file or webcam stream.
        
        Args:
            video_source: Path to video file or camera index (0 for default webcam)
            output_path: Optional path to save output video
        """
        # Initialize video capture
        if isinstance(video_source, str) and video_source.isdigit():
            video_source = int(video_source)
        
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            logger.error(f"Error: Could not open video source {video_source}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Video properties: {width}x{height} @ {fps} FPS")
        
        # Setup video writer if output path is provided
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            logger.info(f"Output video will be saved to: {output_path}")
        
        logger.info("Starting video processing. Press 'K' or 'Q' to quit, 'S' to save screenshot")
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    logger.info("End of video stream")
                    break
                
                self.frame_count += 1
                
                # Detect objects
                cars, pedestrians = self.detect_objects(frame)
                
                # Update statistics
                self.total_cars += len(cars)
                self.total_pedestrians += len(pedestrians)
                
                # Draw detections and statistics
                frame = self.draw_detections(frame, cars, pedestrians)
                frame = self.add_statistics_overlay(frame)
                
                # Write frame to output video if writer is available
                if writer:
                    writer.write(frame)
                
                # Display frame
                cv2.imshow('Car and Pedestrian Detector', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key in [ord('k'), ord('K'), ord('q'), ord('Q')]:
                    logger.info("Quit requested by user")
                    break
                elif key in [ord('s'), ord('S')]:
                    screenshot_path = f"screenshot_frame_{self.frame_count}.jpg"
                    cv2.imwrite(screenshot_path, frame)
                    logger.info(f"Screenshot saved: {screenshot_path}")
                elif key in [ord('r'), ord('R')]:
                    self.frame_count = 0
                    self.total_cars = 0
                    self.total_pedestrians = 0
                    logger.info("Statistics reset")
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()
            
            # Print final statistics
            logger.info(f"Processing completed. Total frames: {self.frame_count}")
            logger.info(f"Total car detections: {self.total_cars}")
            logger.info(f"Total pedestrian detections: {self.total_pedestrians}")


def main():
    """Main function to run the car and pedestrian tracker."""
    parser = argparse.ArgumentParser(description='Car and Pedestrian Detection System')
    parser.add_argument('--video', '-v', default='peds_and_cars.mp4',
                       help='Path to input video file (default: peds_and_cars.mp4)')
    parser.add_argument('--camera', '-c', action='store_true',
                       help='Use webcam instead of video file')
    parser.add_argument('--output', '-o', 
                       help='Path to save output video')
    parser.add_argument('--car-cascade', default='cars.xml',
                       help='Path to car cascade file (default: cars.xml)')
    parser.add_argument('--pedestrian-cascade', default='haarcascade_fullbody.xml',
                       help='Path to pedestrian cascade file (default: haarcascade_fullbody.xml)')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Determine video source
    video_source = 0 if args.camera else args.video
    
    try:
        # Create tracker instance
        tracker = CarPedestrianTracker(args.car_cascade, args.pedestrian_cascade)
        
        # Process video
        tracker.process_video(video_source, args.output)
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
