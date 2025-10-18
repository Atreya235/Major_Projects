# Driver Drowsiness Detection System

This project detects driver drowsiness using Python, OpenCV, dlib, imutils, and Pygame.

## Project Files
- `drowsiness.py` : main Python script
- `shape_predictor_68.dat` : face landmarks model (required by dlib)
- `alert.wav` : alert sound file
- `requirements.txt` : Python libraries required to run the project

## Prerequisites
- Python 3.x
- pip
- [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Windows only, required to install `dlib`)
- Python libraries listed in `requirements.txt`

## Installation

1. **Install Visual C++ Build Tools** (Windows only)
   - Download and install from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - During installation, select "Desktop development with C++"

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
