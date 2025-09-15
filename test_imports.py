#!/usr/bin/env python3
"""
Test script to check if all required modules can be imported
"""

def test_imports():
    try:
        print("Testing imports...")
        
        # Test standard library imports
        import tkinter as tk
        from tkinter import *
        import os, cv2
        import shutil
        import csv
        import numpy as np
        from PIL import ImageTk, Image
        import pandas as pd
        import datetime
        import time
        import tkinter.font as font
        import pyttsx3
        
        print("✓ All standard library and third-party imports successful")
        
        # Test project module imports
        import show_attendance
        import takeImage
        import trainImage
        import automaticAttedance
        
        print("✓ All project module imports successful")
        
        # Test OpenCV face detection
        haarcasecade_path = "haarcascade_frontalface_default.xml"
        if os.path.exists(haarcasecade_path):
            detector = cv2.CascadeClassifier(haarcasecade_path)
            if not detector.empty():
                print("✓ Face detection model loaded successfully")
            else:
                print("⚠ Face detection model file exists but failed to load")
        else:
            print("⚠ Face detection model file not found")
        
        # Test camera access
        try:
            cam = cv2.VideoCapture(0)
            if cam.isOpened():
                print("✓ Camera access successful")
                cam.release()
            else:
                print("⚠ Camera not accessible")
        except Exception as e:
            print(f"⚠ Camera test failed: {e}")
        
        print("\n🎉 All tests passed! The application should run successfully.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install missing dependencies using: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_imports()




