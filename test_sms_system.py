#!/usr/bin/env python3
"""
Test script for SMS notification system
"""

from sms_notification import SMSNotificationSystem

def test_sms_system():
    print("🧪 Testing SMS Notification System...")
    
    # Initialize SMS system
    sms_system = SMSNotificationSystem()
    
    # Test getting all students
    print("\n📋 Getting all students...")
    students = sms_system.get_all_students()
    print(f"Found {len(students)} students")
    
    if len(students) > 0:
        print("\n👥 Student list:")
        for _, student in students.iterrows():
            enrollment = student.get('Enrollment', 'N/A')
            name = student.get('Name', 'N/A')
            phone = student.get('Relative_Phone', 'N/A')
            print(f"  - {name} (ID: {enrollment}, Phone: {phone})")
    
    # Test getting absent students (this will work if there are attendance files)
    print("\n📅 Testing absent student detection...")
    try:
        absent_students = sms_system.get_absent_students("maths", "2025-09-15")
        print(f"Found {len(absent_students)} absent students for maths on 2025-09-15")
        
        if absent_students:
            print("Absent students:")
            for student in absent_students:
                print(f"  - {student['Name']} (ID: {student['Enrollment']})")
    except Exception as e:
        print(f"Error testing absent students: {e}")
    
    print("\n✅ SMS system test completed!")
    print("\n📝 Notes:")
    print("- To send actual SMS, configure Twilio credentials in sms_notification.py")
    print("- Or use the free API (limited to 1 SMS per day)")
    print("- QR codes have been generated for all students")

if __name__ == "__main__":
    test_sms_system()





