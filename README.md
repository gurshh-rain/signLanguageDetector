# Real-Time Sign Language Detector

This project is a computer vision and machine learning application designed to recognize sign language gestures through a standard webcam. By analyzing the shape and positioning of your hands, the system instantly translates physical signs into digital text on your screen.

## How It Works

The system bridges the gap between physical gestures and text using a multi-step pipeline:

1. **Hand Landmark Extraction**: The application captures a live video frame and scans it for a human hand. It identifies key points on the hand (such as knuckle joints and fingertips) and turns them into numeric coordinates.
2. **Feature Normalization**: The raw hand coordinates are adjusted so that it doesn't matter how close or far your hand is from the webcam.
3. **Machine Learning Classification**: A trained model evaluates the position of the hand joints and matches them against known sign language patterns to predict the correct letter or word.

## Features

- **Instant Recognition**: Translates hand movements into letters or phrases with low latency.
- **Robust Coordinate Tracking**: Relies on relative hand structural points instead of raw image pixels, making the tracking less sensitive to changes in background lighting.
- **Dynamic Text Overlay**: Draws a live boundary box around your hand and displays the predicted sign directly on the video feed.
- **Custom Training Pipeline**: Includes scripts to capture your own images, create custom datasets, and train the model on new signs.

## System Workflow

1. **Video Capture**: Streams frame-by-frame live footage from your local camera.
2. **Keypoint Mapping**: Maps the exact structural landmarks of your hand joints.
3. **Pattern Prediction**: Compares the active hand layout against the trained classification rules.
4. **Interface Output**: Prints the resulting translation onto the screen overlay.
