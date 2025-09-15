# 🆕 New Features Guide - QR Code & SMS Notifications

## 📱 QR Code Attendance System

### What's New:
- **QR Code Generation**: Each student gets a unique QR code containing their ID, name, and relative's phone number
- **QR Code Scanning**: When face recognition fails, students can scan their QR code for attendance
- **Fallback System**: Provides reliable attendance marking when face detection is not working

### How to Use:

#### 1. QR Code Generation
- QR codes are automatically generated when new students register
- For existing students, run: `python generate_all_qr_codes.py`
- QR codes are saved in the `QR_Codes/` folder

#### 2. QR Code Attendance
- Click the **"📱 QR Attendance"** button in the main interface
- Select the subject for attendance
- Point camera at student's QR code
- Press 's' to scan or 'q' to quit
- Attendance is automatically marked

#### 3. QR Code Format
Each QR code contains:
```
STUDENT_ID:123|NAME:John|PHONE:9876543210
```

## 📲 SMS Notification System

### What's New:
- **Relative Contact**: Student registration now includes relative's phone number
- **Absent Notifications**: Automatically send SMS to relatives when students are absent
- **Multiple SMS Providers**: Supports both Twilio (paid) and free APIs

### How to Use:

#### 1. Student Registration
- When registering new students, enter the relative's phone number
- Phone number is required for SMS notifications

#### 2. Send Absent Notifications
- Click the **"📱 SMS Notify"** button in the main interface
- Select subject and date
- Click "Send Notifications"
- SMS will be sent to relatives of absent students

#### 3. SMS Message Format
```
અભિવાદન! [Student Name] આજે ([Date]) [Subject] વિષયમાં હાજર નથી. કૃપા કરીને સંપર્ક કરો.
```

## 🔧 Setup Instructions

### Required Packages:
```bash
pip install qrcode
pip install requests
# Optional for QR scanning:
pip install pyzbar
# Optional for SMS via Twilio:
pip install twilio
```

### SMS Configuration:

#### Option 1: Free SMS API (Default)
- No setup required
- Limited to 1 SMS per day
- Uses TextBelt API

#### Option 2: Twilio SMS (Recommended for Production)
1. Sign up for Twilio account
2. Get Account SID, Auth Token, and Phone Number
3. Update `sms_notification.py`:
```python
self.account_sid = "YOUR_TWILIO_ACCOUNT_SID"
self.auth_token = "YOUR_TWILIO_AUTH_TOKEN"
self.twilio_phone = "YOUR_TWILIO_PHONE_NUMBER"
self.use_free_api = False
```

## 📁 File Structure

### New Files:
- `qr_attendance.py` - QR code generation and scanning
- `sms_notification.py` - SMS notification system
- `generate_all_qr_codes.py` - Generate QR codes for existing students
- `test_sms_system.py` - Test SMS functionality
- `QR_Codes/` - Folder containing all student QR codes

### Updated Files:
- `attendance.py` - Added QR and SMS buttons
- `takeImage.py` - Added relative phone field
- `StudentDetails/studentdetails.csv` - Added Relative_Phone column
- `requirements.txt` - Added new dependencies

## 🎯 Features Summary

### QR Code System:
✅ Generate unique QR codes for each student  
✅ Scan QR codes for attendance fallback  
✅ Automatic QR generation during registration  
✅ QR codes contain student ID, name, and phone  

### SMS Notification System:
✅ Add relative phone numbers during registration  
✅ Send SMS to relatives of absent students  
✅ Support for multiple SMS providers  
✅ Gujarati language SMS messages  
✅ Log all notification attempts  

### Integration:
✅ Seamless integration with existing attendance system  
✅ New buttons in main interface  
✅ Fallback when face recognition fails  
✅ Automatic attendance marking via QR codes  

## 🚀 Usage Examples

### Scenario 1: Face Recognition Fails
1. Student's face is not recognized
2. Student shows their QR code
3. Teacher scans QR code using "📱 QR Attendance"
4. Attendance is marked automatically

### Scenario 2: Daily Absent Notifications
1. After taking attendance for the day
2. Click "📱 SMS Notify"
3. Select subject and date
4. System automatically identifies absent students
5. SMS sent to their relatives

### Scenario 3: New Student Registration
1. Click "Register a new student"
2. Enter enrollment number, name, and relative's phone
3. Take photos for face recognition
4. QR code is automatically generated
5. Student can use either face recognition or QR code

## 🔍 Troubleshooting

### QR Code Issues:
- **QR codes not generating**: Check if qrcode package is installed
- **QR scanning not working**: Install pyzbar and its dependencies
- **Camera not accessible**: Check camera permissions

### SMS Issues:
- **SMS not sending**: Check internet connection and API credentials
- **Free API limit reached**: Switch to Twilio or wait 24 hours
- **Phone numbers not found**: Ensure relative phone numbers are entered during registration

## 📞 Support

For issues or questions:
1. Check the error messages in the console
2. Verify all required packages are installed
3. Ensure camera and internet access
4. Check file permissions for QR_Codes folder

---

**Note**: The system is designed to work even if some optional packages (pyzbar, twilio) are not installed. QR code generation will work without pyzbar, and SMS will use free APIs if Twilio is not available.





