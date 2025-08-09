# Robot Hand

## Dependencies

 - `OpenCV` for `Python` -> image processing.
 - `MediaPipe` for `Python` -> hand-detection model.
 - `Arduino.h` for `C++` -> servo control library.

## Platforms and Tools (Non-essential)
 
 - `PlatformIO` for `vscode` -> provides tooling for building and uploading
 gsketches to Arduino board, and library management.
 - `uv` for `Python` -> package manager.

## Instructions

 1. Build and load `main.cpp` sketch onto board.
 2. Run `vision/main.py` to start hand tracking.