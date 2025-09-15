#!/usr/bin/env python3
"""
Script to generate QR codes for all existing students
Run this script after updating the student details with phone numbers
"""

import os
import sys
from qr_attendance import QRAttendanceSystem

def main():
    print("🔧 Generating QR codes for all existing students...")
    
    # Initialize QR system
    qr_system = QRAttendanceSystem()
    
    # Generate QR codes for all students
    success = qr_system.generate_all_qr_codes()
    
    if success:
        print("✅ QR codes generated successfully!")
        print(f"📁 QR codes saved in: {qr_system.qr_codes_dir}")
        print("\n📋 Instructions:")
        print("1. Print QR codes for each student")
        print("2. Students can use QR codes when face recognition fails")
        print("3. QR codes contain student ID, name, and relative phone number")
    else:
        print("❌ Error generating QR codes")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())





