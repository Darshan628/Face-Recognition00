#!/usr/bin/env python3
"""
Startup script for Web Attendance System
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all requirements are installed"""
    print("Checking requirements...")
    
    required_packages = [
        'flask', 'opencv-python', 'pandas', 'numpy', 
        'pillow', 'openpyxl', 'pyttsx3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", "requirements_web.txt"
            ])
            print("✓ All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            return False
    
    return True

def check_files():
    """Check if required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        "TrainingImageLabel/Trainner.yml",
        "haarcascade_frontalface_default.xml",
        "StudentDetails/studentdetails.xlsx"
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            missing_files.append(file)
            print(f"❌ {file}")
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        print("Please ensure you have:")
        print("1. Trained the face recognition model")
        print("2. Added students to the system")
        print("3. All required files are in place")
        return False
    
    return True

def main():
    print("=" * 60)
    print("Web Attendance System Startup")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed!")
        return False
    
    # Check files
    if not check_files():
        print("\n❌ File check failed!")
        print("\nPlease run the following first:")
        print("1. python setup.py")
        print("2. Register some students")
        print("3. Train the model")
        return False
    
    print("\n✅ All checks passed!")
    print("\n🚀 Starting Web Attendance System...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("📱 Or use: http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the web application
    try:
        import web_attendance
    except KeyboardInterrupt:
        print("\n\n👋 Web server stopped!")
    except Exception as e:
        print(f"\n❌ Error starting web server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()




