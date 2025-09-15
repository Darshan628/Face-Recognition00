#!/usr/bin/env python3
"""
Web-based Attendance Management System
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import cv2
import numpy as np
import pandas as pd
import os
import datetime
import time
import base64
from io import BytesIO
from PIL import Image
import json

app = Flask(__name__)

# Global variables for face recognition
recognizer = None
detector = None
student_df = None
subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]

def initialize_face_recognition():
    """Initialize face recognition components"""
    global recognizer, detector, student_df
    
    try:
        # Load face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel/Trainner.yml")
        
        # Load face detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
        # Load student data
        student_df = pd.read_excel("StudentDetails/studentdetails.xlsx")
        
        print("✓ Face recognition initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing face recognition: {e}")
        return False

def recognize_face(image_data):
    """Recognize face from image data"""
    global recognizer, detector, student_df
    
    try:
        # Convert base64 image to OpenCV format
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = detector.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return {"success": False, "message": "No face detected"}
        
        # Get the first face
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        # Recognize the face
        id, confidence = recognizer.predict(face_roi)
        
        if confidence < 70:
            # Find student name
            student = student_df[student_df['Enrollment'] == str(id)]
            if len(student) > 0:
                student_name = student['Name'].iloc[0]
                return {
                    "success": True,
                    "student_id": str(id),
                    "student_name": student_name,
                    "confidence": float(confidence)
                }
            else:
                return {"success": False, "message": "Student not found in database"}
        else:
            return {"success": False, "message": "Face not recognized (low confidence)"}
            
    except Exception as e:
        return {"success": False, "message": f"Recognition error: {str(e)}"}

def save_attendance(student_id, student_name, subject, date, time_str):
    """Save attendance to Excel file"""
    try:
        # Create attendance record
        attendance_record = {
            'Enrollment': student_id,
            'Name': student_name,
            'Subject': subject,
            'Date': date,
            'Time': time_str,
            'Attendance_Status': 'Present'
        }
        
        # Create attendance directory for subject
        attendance_dir = f"Attendance/{subject}"
        os.makedirs(attendance_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{attendance_dir}/{subject}_{timestamp}.csv"
        
        # Check if file exists
        if os.path.exists(filename):
            # Append to existing file
            df = pd.read_csv(filename)
            df = pd.concat([df, pd.DataFrame([attendance_record])], ignore_index=True)
        else:
            # Create new file
            df = pd.DataFrame([attendance_record])
        
        # Save to CSV
        df.to_csv(filename, index=False)
        
        # Also save to main attendance file
        main_attendance_file = f"{attendance_dir}/attendance.csv"
        if os.path.exists(main_attendance_file):
            main_df = pd.read_csv(main_attendance_file)
            main_df = pd.concat([main_df, pd.DataFrame([attendance_record])], ignore_index=True)
        else:
            main_df = pd.DataFrame([attendance_record])
        
        main_df.to_csv(main_attendance_file, index=False)
        
        print(f"✓ Attendance saved: {student_name} - {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving attendance: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', subjects=subjects)

@app.route('/take_attendance')
def take_attendance():
    """Take attendance page"""
    return render_template('attendance.html', subjects=subjects)

@app.route('/recognize', methods=['POST'])
def recognize():
    """Recognize face from uploaded image"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        subject = data.get('subject')
        
        if not image_data or not subject:
            return jsonify({"success": False, "message": "Missing image or subject"})
        
        # Recognize face
        result = recognize_face(image_data)
        
        if result["success"]:
            # Save attendance
            current_time = datetime.datetime.now()
            date_str = current_time.strftime("%Y-%m-%d")
            time_str = current_time.strftime("%H:%M:%S")
            
            save_success = save_attendance(
                result["student_id"],
                result["student_name"],
                subject,
                date_str,
                time_str
            )
            
            if save_success:
                result["message"] = f"Attendance marked for {result['student_name']} in {subject}"
            else:
                result["success"] = False
                result["message"] = "Failed to save attendance"
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/view_attendance')
def view_attendance():
    """View attendance page"""
    return render_template('view_attendance.html', subjects=subjects)

@app.route('/get_attendance/<subject>')
def get_attendance(subject):
    """Get attendance data for a subject"""
    try:
        attendance_file = f"Attendance/{subject}/attendance.csv"
        if os.path.exists(attendance_file):
            df = pd.read_csv(attendance_file)
            return jsonify({
                "success": True,
                "data": df.to_dict('records')
            })
        else:
            return jsonify({
                "success": True,
                "data": []
            })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/students')
def get_students():
    """Get list of all students"""
    try:
        if student_df is not None:
            students = student_df[['Enrollment', 'Name']].to_dict('records')
            return jsonify({"success": True, "students": students})
        else:
            return jsonify({"success": False, "message": "Student data not loaded"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == '__main__':
    # Initialize face recognition
    if initialize_face_recognition():
        print("🚀 Starting Web Attendance System...")
        print("📱 Open your browser and go to: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize face recognition. Please check your setup.")




