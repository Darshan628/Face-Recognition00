import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image


# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        # Check if training images directory exists
        if not os.path.exists(trainimage_path):
            error_msg = "Training images directory not found!"
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
        
        # Check if there are any subdirectories with images
        subdirs = [d for d in os.listdir(trainimage_path) if os.path.isdir(os.path.join(trainimage_path, d))]
        if not subdirs:
            error_msg = "No student images found! Please register students first."
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
        
        print("Starting face recognition training...")
        
        # Create recognizer with optimized parameters for fewer images
        recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1,      # Smaller radius for fewer images
            neighbors=8,   # Standard neighbors
            grid_x=8,      # Smaller grid for fewer images
            grid_y=8,      # Smaller grid for fewer images
            threshold=100  # Higher threshold for better accuracy with fewer images
        )
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        # Check if detector loaded properly
        if detector.empty():
            error_msg = "Face detection model not found!"
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
        
        # Get faces and labels
        faces, Ids = getImagesAndLables(trainimage_path)
        
        if len(faces) == 0:
            error_msg = "No valid images found for training!"
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
        
        # Create TrainingImageLabel directory if it doesn't exist
        os.makedirs(os.path.dirname(trainimagelabel_path), exist_ok=True)
        
        # Train the recognizer
        print(f"Training with {len(faces)} images...")
        recognizer.train(faces, np.array(Ids))
        
        # Save the trained model
        recognizer.save(trainimagelabel_path)
        
        # Success message
        unique_ids = len(set(Ids))
        res = f"Training completed successfully! Processed {len(faces)} images from {unique_ids} students."
        message.configure(text=res)
        text_to_speech("Training completed successfully!")
        print(res)
        
    except Exception as e:
        error_msg = f"Training failed: {str(e)}"
        message.configure(text=error_msg)
        text_to_speech("Training failed. Please check the error message.")
        print(f"Training error: {e}")


def getImagesAndLables(path):
    # Get all image paths from subdirectories
    newdir = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    imagePath = []
    for directory in newdir:
        for f in os.listdir(directory):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                imagePath.append(os.path.join(directory, f))
    
    faces = []
    Ids = []
    
    print(f"Found {len(imagePath)} images to process...")
    
    for imagePath in imagePath:
        try:
            # Load image
            pilImage = Image.open(imagePath).convert("L")
            imageNp = np.array(pilImage, "uint8")
            
            # Extract ID from filename: Name_Enrollment_sampleNum.jpg
            # We need the Enrollment number (second part after splitting by '_')
            filename = os.path.split(imagePath)[-1]
            parts = filename.split("_")
            if len(parts) >= 2:
                Id = int(parts[1])  # Enrollment number is the second part
                faces.append(imageNp)
                Ids.append(Id)
                print(f"Processed: {filename} -> ID: {Id}")
            else:
                print(f"Warning: Invalid filename format: {filename}")
                
        except Exception as e:
            print(f"Error processing {imagePath}: {e}")
            continue
    
    print(f"Successfully processed {len(faces)} images for {len(set(Ids))} unique IDs")
    return faces, Ids
