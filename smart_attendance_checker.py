#!/usr/bin/env python3
"""
Smart Attendance Checker
This script checks if attendance calculator button should be shown based on attendance status
"""

import pandas as pd
import os
import glob
from datetime import datetime

class SmartAttendanceChecker:
    def __init__(self):
        self.attendance_base = "Attendance"
        self.target_percentage = 70  # Default target percentage
    
    def get_all_students_attendance(self):
        """Get attendance data for all students across all subjects"""
        try:
            all_students_data = {}
            
            # Get all subject directories
            if not os.path.exists(self.attendance_base):
                return all_students_data
            
            for subject_dir in os.listdir(self.attendance_base):
                subject_path = os.path.join(self.attendance_base, subject_dir)
                if os.path.isdir(subject_path):
                    # Get all attendance CSV files for this subject
                    csv_files = glob.glob(os.path.join(subject_path, f"{subject_dir}_*.csv"))
                    
                    if csv_files:
                        # Combine all attendance data for this subject
                        all_attendance = []
                        for file in csv_files:
                            try:
                                df = pd.read_csv(file)
                                all_attendance.append(df)
                            except Exception as e:
                                print(f"Error reading {file}: {e}")
                        
                        if all_attendance:
                            # Combine all dataframes
                            combined_df = pd.concat(all_attendance, ignore_index=True)
                            
                            # Group by enrollment to get student-wise data
                            for enrollment, student_data in combined_df.groupby('Enrollment'):
                                if enrollment not in all_students_data:
                                    all_students_data[enrollment] = {}
                                
                                # Calculate attendance for this subject
                                total_classes = len(student_data)
                                present_classes = len(student_data[student_data['Attendance_Status'] == 'Present'])
                                attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
                                
                                all_students_data[enrollment][subject_dir] = {
                                    'total_classes': total_classes,
                                    'present_classes': present_classes,
                                    'attendance_percentage': round(attendance_percentage, 2)
                                }
            
            return all_students_data
            
        except Exception as e:
            print(f"Error getting all students attendance: {e}")
            return {}
    
    def should_show_calculator(self):
        """Check if attendance calculator should be shown"""
        try:
            all_students_data = self.get_all_students_attendance()
            
            if not all_students_data:
                # If no attendance data, show calculator
                return True, "No attendance data found. Calculator available for new students."
            
            # Check if any student has attendance below target
            students_below_target = []
            for enrollment, subjects_data in all_students_data.items():
                for subject, data in subjects_data.items():
                    if data['attendance_percentage'] < self.target_percentage:
                        students_below_target.append({
                            'enrollment': enrollment,
                            'subject': subject,
                            'percentage': data['attendance_percentage']
                        })
            
            if students_below_target:
                return True, f"Found {len(students_below_target)} students below {self.target_percentage}% attendance"
            else:
                return False, f"All students have {self.target_percentage}% or above attendance"
                
        except Exception as e:
            print(f"Error checking attendance status: {e}")
            return True, "Error checking attendance. Calculator available."
    
    def get_attendance_summary(self):
        """Get summary of attendance status"""
        try:
            all_students_data = self.get_all_students_attendance()
            
            if not all_students_data:
                return "No attendance data available"
            
            total_students = len(all_students_data)
            students_below_target = 0
            students_above_target = 0
            
            for enrollment, subjects_data in all_students_data.items():
                student_below_target = False
                for subject, data in subjects_data.items():
                    if data['attendance_percentage'] < self.target_percentage:
                        student_below_target = True
                        break
                
                if student_below_target:
                    students_below_target += 1
                else:
                    students_above_target += 1
            
            summary = f"""
📊 ATTENDANCE SUMMARY:
• Total Students: {total_students}
• Students Below {self.target_percentage}%: {students_below_target}
• Students Above {self.target_percentage}%: {students_above_target}
• Calculator Status: {'Available' if students_below_target > 0 else 'Not Needed'}
            """
            
            return summary.strip()
            
        except Exception as e:
            return f"Error generating summary: {e}"

def check_attendance_status():
    """Main function to check if calculator should be shown"""
    checker = SmartAttendanceChecker()
    should_show, message = checker.should_show_calculator()
    return should_show, message

def get_attendance_summary():
    """Get attendance summary"""
    checker = SmartAttendanceChecker()
    return checker.get_attendance_summary()

if __name__ == "__main__":
    # Test the checker
    should_show, message = check_attendance_status()
    print(f"Should show calculator: {should_show}")
    print(f"Message: {message}")
    
    summary = get_attendance_summary()
    print(f"\nSummary:\n{summary}")






