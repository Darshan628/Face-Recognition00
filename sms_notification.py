import pandas as pd
import datetime
import os
import requests
import json
import time

# Try to import twilio, but make it optional
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("Warning: twilio not available. SMS via Twilio will be disabled.")

class SMSNotificationSystem:
    def __init__(self):
        self.student_details_path = "StudentDetails/studentdetails.csv"
        self.absent_students_file = "absent_students_log.csv"
        
        # Twilio configuration (you need to add your credentials)
        self.account_sid = "YOUR_TWILIO_ACCOUNT_SID"  # Replace with your Twilio Account SID
        self.auth_token = "YOUR_TWILIO_AUTH_TOKEN"    # Replace with your Twilio Auth Token
        self.twilio_phone = "YOUR_TWILIO_PHONE_NUMBER"  # Replace with your Twilio phone number
        
        # Alternative: Use a free SMS API (like TextBelt or similar)
        self.use_free_api = True  # Set to False if using Twilio
        
    def send_sms_twilio(self, phone_number, message):
        """Send SMS using Twilio"""
        if not TWILIO_AVAILABLE:
            print("Twilio not available. Please install twilio package.")
            return False
            
        try:
            client = Client(self.account_sid, self.auth_token)
            
            message = client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=phone_number
            )
            
            print(f"SMS sent successfully to {phone_number}: {message.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending SMS via Twilio: {e}")
            return False
    
    def send_sms_free_api(self, phone_number, message):
        """Send SMS using free API (TextBelt or similar)"""
        try:
            # Using TextBelt API (free tier available)
            url = "https://textbelt.com/text"
            data = {
                'phone': phone_number,
                'message': message,
                'key': 'textbelt'  # Free key, limited to 1 SMS per day
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get('success'):
                print(f"SMS sent successfully to {phone_number}")
                return True
            else:
                print(f"SMS failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"Error sending SMS via free API: {e}")
            return False
    
    def send_sms(self, phone_number, message):
        """Send SMS using configured method"""
        if self.use_free_api:
            return self.send_sms_free_api(phone_number, message)
        else:
            return self.send_sms_twilio(phone_number, message)
    
    def get_absent_students(self, subject, date):
        """Get list of students who were absent on a specific date"""
        try:
            attendance_dir = f"Attendance/{subject}"
            if not os.path.exists(attendance_dir):
                return []
            
            absent_students = []
            all_students = self.get_all_students()
            
            # Get present students from attendance files
            present_students = set()
            
            for filename in os.listdir(attendance_dir):
                if filename.endswith('.csv') and date in filename:
                    filepath = os.path.join(attendance_dir, filename)
                    try:
                        df = pd.read_csv(filepath)
                        for _, row in df.iterrows():
                            if row.get('Attendance_Status') == 'Present':
                                present_students.add(str(row['Enrollment']))
                    except Exception as e:
                        print(f"Error reading attendance file {filename}: {e}")
            
            # Find absent students
            for _, student in all_students.iterrows():
                enrollment = str(student['Enrollment'])
                if enrollment not in present_students:
                    absent_students.append({
                        'Enrollment': enrollment,
                        'Name': student['Name'],
                        'Relative_Phone': student.get('Relative_Phone', ''),
                        'Subject': subject,
                        'Date': date
                    })
            
            return absent_students
            
        except Exception as e:
            print(f"Error getting absent students: {e}")
            return []
    
    def get_all_students(self):
        """Get all registered students"""
        try:
            if os.path.exists(self.student_details_path):
                return pd.read_csv(self.student_details_path)
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error reading student details: {e}")
            return pd.DataFrame()
    
    def notify_absent_students(self, subject, date=None):
        """Send SMS notifications to relatives of absent students"""
        try:
            if date is None:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            absent_students = self.get_absent_students(subject, date)
            
            if not absent_students:
                print(f"No absent students found for {subject} on {date}")
                return
            
            print(f"Found {len(absent_students)} absent students for {subject} on {date}")
            
            notifications_sent = 0
            
            for student in absent_students:
                relative_phone = student.get('Relative_Phone', '')
                student_name = student.get('Name', '')
                
                if relative_phone and relative_phone != 'nan' and relative_phone.strip():
                    # Create SMS message
                    message = f"અભિવાદન! {student_name} આજે ({date}) {subject} વિષયમાં હાજર નથી. કૃપા કરીને સંપર્ક કરો."
                    
                    # Send SMS
                    if self.send_sms(relative_phone, message):
                        notifications_sent += 1
                        print(f"Notification sent to {relative_phone} for {student_name}")
                    
                    # Add delay to avoid rate limiting
                    time.sleep(2)
                else:
                    print(f"No phone number available for {student_name}")
            
            # Log the notifications
            self.log_notifications(absent_students, notifications_sent)
            
            print(f"Notifications sent: {notifications_sent}/{len(absent_students)}")
            
        except Exception as e:
            print(f"Error notifying absent students: {e}")
    
    def log_notifications(self, absent_students, notifications_sent):
        """Log notification details"""
        try:
            log_data = []
            for student in absent_students:
                log_data.append({
                    'Date': student['Date'],
                    'Subject': student['Subject'],
                    'Student_Name': student['Name'],
                    'Enrollment': student['Enrollment'],
                    'Relative_Phone': student.get('Relative_Phone', ''),
                    'Notification_Sent': 'Yes' if student.get('Relative_Phone', '') else 'No',
                    'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            log_df = pd.DataFrame(log_data)
            
            # Append to log file
            if os.path.exists(self.absent_students_file):
                existing_df = pd.read_csv(self.absent_students_file)
                log_df = pd.concat([existing_df, log_df], ignore_index=True)
            
            log_df.to_csv(self.absent_students_file, index=False)
            print(f"Notification log updated: {self.absent_students_file}")
            
        except Exception as e:
            print(f"Error logging notifications: {e}")
    
    def setup_twilio_credentials(self, account_sid, auth_token, phone_number):
        """Setup Twilio credentials"""
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_phone = phone_number
        self.use_free_api = False
        print("Twilio credentials configured")

# Test the SMS system
if __name__ == "__main__":
    sms_system = SMSNotificationSystem()
    
    # Test with a sample notification
    test_phone = "1234567890"  # Replace with a test phone number
    test_message = "Test message from Attendance Management System"
    
    print("Testing SMS notification system...")
    # sms_system.send_sms(test_phone, test_message)  # Uncomment to test
