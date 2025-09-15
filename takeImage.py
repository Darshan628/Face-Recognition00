import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time



# take Image of user
def TakeImage(l1, l2, l3, haarcasecade_path, trainimage_path, message, err_screen,text_to_speech):
    if (l1 == "") and (l2==""):
        t='Please Enter the your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    elif l3 == "":
        t='Please Enter the Relative Phone Number.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                message.configure(text="Camera not accessible. Please check camera connection.")
                text_to_speech("Camera not accessible. Please check camera connection.")
                return
            
            detector = cv2.CascadeClassifier(haarcasecade_path)
            if detector.empty():
                message.configure(text="Face detection model not found.")
                text_to_speech("Face detection model not found.")
                return
                
            Enrollment = l1
            Name = l2
            Relative_Phone = l3
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            
            if os.path.exists(path):
                message.configure(text="Student data already exists. Please use different enrollment number.")
                text_to_speech("Student data already exists. Please use different enrollment number.")
                return
                
            os.mkdir(path)
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        gray[y : y + h, x : x + w],
                    )
                    cv2.imshow("Frame", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 10:
                    break
            cam.release()
            cv2.destroyAllWindows()
            # Save student details to CSV
            row = [Enrollment, Name, Relative_Phone]
            csv_path = "StudentDetails/studentdetails.csv"
            
            # Create StudentDetails directory if it doesn't exist
            os.makedirs("StudentDetails", exist_ok=True)
            
            # Check if CSV file exists, if not create with headers
            file_exists = os.path.exists(csv_path)
            
            with open(csv_path, "a+", newline='', encoding='utf-8') as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                
                # Write header if file is new
                if not file_exists:
                    writer.writerow(["Enrollment", "Name", "Relative_Phone"])
                
                # Write student data
                writer.writerow(row)
                csvFile.flush()  # Ensure data is written immediately
            
            print(f"Student details saved: {Name} (Enrollment: {Enrollment})")
            
            # Generate QR code for the student
            try:
                from qr_attendance import QRAttendanceSystem
                qr_system = QRAttendanceSystem()
                qr_path = qr_system.generate_qr_code(Enrollment, Name, Relative_Phone)
                if qr_path:
                    print(f"QR Code generated: {qr_path}")
            except Exception as e:
                print(f"Could not generate QR code: {e}")
            
            # Also create Excel file for better viewing
            try:
                df = pd.read_csv(csv_path)
                excel_path = "StudentDetails/studentdetails.xlsx"
                df.to_excel(excel_path, index=False)
                print(f"Excel file updated: {excel_path}")
            except Exception as e:
                print(f"Could not create Excel file: {e}")
            
            res = f"Images Saved for ER No: {Enrollment} Name: {Name} (2 photos captured)"
            message.configure(text=res)
            text_to_speech(res)
        except FileExistsError as F:
            message.configure(text="Student Data already exists")
            text_to_speech("Student Data already exists")
        except Exception as e:
            message.configure(text=f"Error: {str(e)}")
            text_to_speech(f"Error occurred: {str(e)}")
        finally:
            if 'cam' in locals():
                cam.release()
            cv2.destroyAllWindows()
