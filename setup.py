#!/usr/bin/env python3
"""
Setup script for Face Recognition Attendance Management System
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "TrainingImage",
        "TrainingImageLabel", 
        "StudentDetails",
        "Attendance",
        "UI_Image"
    ]
    
    print("Creating necessary directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory already exists: {directory}")

def check_files():
    """Check if required files exist"""
    required_files = [
        "haarcascade_frontalface_default.xml",
        "AMS.ico"
    ]
    
    print("Checking required files...")
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ Found: {file}")
        else:
            print(f"⚠ Missing: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠ Warning: {len(missing_files)} files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print("The application may not work properly without these files.")
    
    return len(missing_files) == 0

def main():
    print("=" * 60)
    print("Face Recognition Attendance Management System Setup")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return False
    
    # Create directories
    create_directories()
    
    # Check files
    files_ok = check_files()
    
    print("\n" + "=" * 60)
    if files_ok:
        print("🎉 Setup completed successfully!")
        print("You can now run the application with: python attendance.py")
    else:
        print("⚠ Setup completed with warnings.")
        print("Some files are missing, but the application should still work.")
        print("You can run the application with: python attendance.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()




