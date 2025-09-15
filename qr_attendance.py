import cv2
import qrcode
import pandas as pd
import os
import datetime
import numpy as np

# pyzbar will be imported inside the scan_qr_code function to avoid import errors

class QRAttendanceSystem:
    def __init__(self):
        self.student_details_path = "StudentDetails/studentdetails.csv"
        self.qr_codes_dir = "QR_Codes"
        os.makedirs(self.qr_codes_dir, exist_ok=True)
    
    def generate_qr_code(self, enrollment, name, relative_phone=""):
        """Generate QR code for a student"""
        try:
            # Create QR code data
            qr_data = f"STUDENT_ID:{enrollment}|NAME:{name}|PHONE:{relative_phone}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code
            qr_filename = f"{enrollment}_{name}_qr.png"
            qr_path = os.path.join(self.qr_codes_dir, qr_filename)
            qr_img.save(qr_path)
            
            print(f"QR Code generated: {qr_path}")
            return qr_path
            
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
    
    def scan_qr_code(self):
        """Scan QR code from camera for attendance"""
        try:
            from pyzbar import pyzbar
        except ImportError:
            print("QR code scanning not available. Please install pyzbar and its dependencies.")
            return None
            
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Camera not accessible")
                return None
            
            print("Point camera at QR code. Press 'q' to quit, 's' to scan")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Decode QR codes
                qr_codes = pyzbar.decode(frame)
                
                # Draw rectangles around detected QR codes
                for qr_code in qr_codes:
                    (x, y, w, h) = qr_code.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Decode QR code data
                    qr_data = qr_code.data.decode('utf-8')
                    cv2.putText(frame, qr_data, (x, y - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                cv2.imshow('QR Code Scanner', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s') and qr_codes:
                    # Process the first detected QR code
                    qr_data = qr_codes[0].data.decode('utf-8')
                    cap.release()
                    cv2.destroyAllWindows()
                    return self.parse_qr_data(qr_data)
            
            cap.release()
            cv2.destroyAllWindows()
            return None
            
        except Exception as e:
            print(f"Error scanning QR code: {e}")
            if 'cap' in locals():
                cap.release()
            cv2.destroyAllWindows()
            return None
    
    def parse_qr_data(self, qr_data):
        """Parse QR code data to extract student information"""
        try:
            # Expected format: STUDENT_ID:123|NAME:John|PHONE:9876543210
            parts = qr_data.split('|')
            student_info = {}
            
            for part in parts:
                if ':' in part:
                    key, value = part.split(':', 1)
                    student_info[key] = value
            
            return student_info
            
        except Exception as e:
            print(f"Error parsing QR data: {e}")
            return None
    
    def mark_attendance_by_qr(self, subject, student_info):
        """Mark attendance using QR code data"""
        try:
            enrollment = student_info.get('STUDENT_ID', '')
            name = student_info.get('NAME', '')
            
            if not enrollment or not name:
                print("Invalid QR code data")
                return False
            
            # Create attendance record
            now = datetime.datetime.now()
            attendance_data = {
                'Enrollment': enrollment,
                'Name': name,
                'Subject': subject,
                'Date': now.strftime('%Y-%m-%d'),
                'Time': now.strftime('%H:%M:%S'),
                'Attendance_Status': 'Present',
                'Method': 'QR_Code'
            }
            
            # Save to CSV
            attendance_file = f"Attendance/{subject}/{subject}_{now.strftime('%Y-%m-%d_%H-%M-%S')}_qr.csv"
            os.makedirs(os.path.dirname(attendance_file), exist_ok=True)
            
            df = pd.DataFrame([attendance_data])
            df.to_csv(attendance_file, index=False)
            
            print(f"Attendance marked via QR: {name} ({enrollment}) - {subject}")
            return True
            
        except Exception as e:
            print(f"Error marking QR attendance: {e}")
            return False
    
    def generate_all_qr_codes(self):
        """Generate QR codes for all existing students"""
        try:
            if not os.path.exists(self.student_details_path):
                print("Student details file not found")
                return False
            
            df = pd.read_csv(self.student_details_path)
            generated_count = 0
            
            for _, row in df.iterrows():
                enrollment = str(row['Enrollment'])
                name = str(row['Name'])
                relative_phone = str(row.get('Relative_Phone', ''))
                
                if enrollment and name and enrollment != 'nan' and name != 'nan':
                    qr_path = self.generate_qr_code(enrollment, name, relative_phone)
                    if qr_path:
                        generated_count += 1
            
            print(f"Generated {generated_count} QR codes")
            return True
            
        except Exception as e:
            print(f"Error generating QR codes: {e}")
            return False

# Test the QR system
if __name__ == "__main__":
    qr_system = QRAttendanceSystem()
    qr_system.generate_all_qr_codes()
