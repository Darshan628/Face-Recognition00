# Face Recognition Attendance Management System - Setup Instructions

## Quick Start

1. **Install Dependencies:**
   ```bash
   python setup.py
   ```

2. **Run the Application:**
   ```bash
   python run.py
   ```
   OR
   ```bash
   python attendance.py
   ```

## Manual Setup

If the automatic setup doesn't work, follow these steps:

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Required Files
Make sure these files are present in the project directory:
- `haarcascade_frontalface_default.xml` (OpenCV face detection model)
- `AMS.ico` (Application icon)

### 3. Directory Structure
The following directories will be created automatically:
- `TrainingImage/` - Stores student face images
- `TrainingImageLabel/` - Stores trained model
- `StudentDetails/` - Stores student information
- `Attendance/` - Stores attendance records
- `UI_Image/` - UI images (optional)

## Features

1. **Register New Student:** Capture and train face images for new students
2. **Take Attendance:** Use face recognition to mark attendance
3. **View Attendance:** Check attendance records and statistics

## Troubleshooting

### Common Issues:

1. **Camera not working:**
   - Make sure your camera is connected and not being used by another application
   - Check camera permissions in your system settings

2. **Face detection not working:**
   - Ensure `haarcascade_frontalface_default.xml` is in the project directory
   - Make sure you have good lighting when capturing images

3. **Import errors:**
   - Run `python setup.py` to install all dependencies
   - Make sure you're using Python 3.6 or higher

4. **UI images not loading:**
   - The application will work without UI images (placeholders will be shown)
   - Make sure `UI_Image/` directory contains the required PNG files

## System Requirements

- Python 3.6 or higher
- Webcam/Camera
- Windows/Linux/macOS
- At least 4GB RAM recommended

## Usage Instructions

1. **First Time Setup:**
   - Click "Register a new student"
   - Enter enrollment number and name
   - Click "Take Image" and position your face in the camera
   - Press 'q' to stop capturing (or wait for 50 images)
   - Click "Train Image" to create the face recognition model

2. **Taking Attendance:**
   - Click "Take Attendance"
   - Enter subject name
   - Click "Fill Attendance"
   - Position faces in front of camera for 20 seconds
   - Attendance will be automatically recorded

3. **Viewing Attendance:**
   - Click "View Attendance"
   - Enter subject name
   - Click "View Attendance" to see records

## Support

If you encounter any issues:
1. Check the console output for error messages
2. Ensure all dependencies are installed
3. Verify camera and file permissions
4. Make sure all required files are present

---
**Note:** This application uses OpenCV for face detection and recognition. Make sure you have a good quality camera and proper lighting for best results.




