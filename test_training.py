#!/usr/bin/env python3
"""
Test script for the training functionality
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

def test_training():
    """Test the training functionality"""
    print("Testing Face Recognition Training...")
    print("=" * 50)
    
    try:
        # Import the training module
        import trainImage
        
        # Create a simple test GUI for the message widget
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Create a message widget for testing
        message = tk.Label(root, text="Testing...", width=50, height=2)
        
        def dummy_text_to_speech(text):
            print(f"TTS: {text}")
        
        # Test parameters
        haarcasecade_path = "haarcascade_frontalface_default.xml"
        trainimage_path = "TrainingImage"
        trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
        
        print(f"Haar cascade path: {haarcasecade_path}")
        print(f"Training images path: {trainimage_path}")
        print(f"Model output path: {trainimagelabel_path}")
        
        # Check if files exist
        if not os.path.exists(haarcasecade_path):
            print(f"❌ Haar cascade file not found: {haarcasecade_path}")
            return False
        
        if not os.path.exists(trainimage_path):
            print(f"❌ Training images directory not found: {trainimage_path}")
            return False
        
        # Check if there are any training images
        subdirs = [d for d in os.listdir(trainimage_path) if os.path.isdir(os.path.join(trainimage_path, d))]
        if not subdirs:
            print(f"❌ No student directories found in {trainimage_path}")
            print("Please register some students first using the main application.")
            return False
        
        print(f"✓ Found {len(subdirs)} student directories:")
        for subdir in subdirs:
            image_count = len([f for f in os.listdir(os.path.join(trainimage_path, subdir)) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"  - {subdir}: {image_count} images")
        
        # Test the getImagesAndLables function
        print("\nTesting image loading...")
        faces, Ids = trainImage.getImagesAndLables(trainimage_path)
        
        if len(faces) == 0:
            print("❌ No images could be loaded")
            return False
        
        print(f"✓ Successfully loaded {len(faces)} images")
        print(f"✓ Found {len(set(Ids))} unique student IDs: {sorted(set(Ids))}")
        
        # Test the training function
        print("\nTesting training...")
        trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, dummy_text_to_speech)
        
        # Check if model was created
        if os.path.exists(trainimagelabel_path):
            print(f"✓ Training model saved successfully: {trainimagelabel_path}")
            file_size = os.path.getsize(trainimagelabel_path)
            print(f"✓ Model file size: {file_size} bytes")
        else:
            print(f"❌ Training model was not created")
            return False
        
        print("\n🎉 Training test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Training test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            root.destroy()
        except:
            pass

def main():
    print("Face Recognition Training Test")
    print("=" * 50)
    
    success = test_training()
    
    if success:
        print("\n✅ All tests passed! Training functionality is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have registered some students first")
        print("2. Check that haarcascade_frontalface_default.xml exists")
        print("3. Ensure TrainingImage directory has student subdirectories with images")
        print("4. Verify all required Python packages are installed")

if __name__ == "__main__":
    main()




