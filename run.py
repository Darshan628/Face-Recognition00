#!/usr/bin/env python3
"""
Run script for Face Recognition Attendance Management System
"""

import sys
import os

def main():
    print("Starting Face Recognition Attendance Management System...")
    print("=" * 60)
    
    try:
        # Import and run the main application
        import attendance
        print("✓ Application started successfully!")
        print("The GUI window should now be open.")
        print("Close the window or press Ctrl+C to exit.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run setup.py first to install dependencies:")
        print("python setup.py")
        return False
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Please check the error message above and try again.")
        return False
    
    return True

if __name__ == "__main__":
    main()




