#!/usr/bin/env python3
"""
Subject Management System for Attendance
"""

import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox, ttk

class SubjectManager:
    def __init__(self):
        self.subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]
        self.student_file = "StudentDetails/studentdetails.xlsx"
        self.attendance_dir = "Attendance"
    
    def get_student_data(self):
        """Get student data from Excel file"""
        try:
            if os.path.exists(self.student_file):
                return pd.read_excel(self.student_file)
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error reading student data: {e}")
            return pd.DataFrame()
    
    def update_student_subjects(self, enrollment, subjects_to_enroll):
        """Update student's subject enrollment"""
        try:
            df = self.get_student_data()
            if df.empty:
                return False
            
            # Find student by enrollment
            student_index = df[df['Enrollment'] == str(enrollment)].index
            if len(student_index) == 0:
                print(f"Student with enrollment {enrollment} not found")
                return False
            
            # Update subjects
            for subject in self.subjects:
                if subject in subjects_to_enroll:
                    df.at[student_index[0], subject] = "Enrolled"
                else:
                    df.at[student_index[0], subject] = "Not Enrolled"
            
            # Save updated data
            df.to_excel(self.student_file, index=False)
            df.to_csv("StudentDetails/studentdetails.csv", index=False)
            
            print(f"Updated subjects for student {enrollment}")
            return True
            
        except Exception as e:
            print(f"Error updating student subjects: {e}")
            return False
    
    def get_student_subjects(self, enrollment):
        """Get subjects for a specific student"""
        try:
            df = self.get_student_data()
            if df.empty:
                return []
            
            student = df[df['Enrollment'] == str(enrollment)]
            if len(student) == 0:
                return []
            
            enrolled_subjects = []
            for subject in self.subjects:
                if subject in student.columns and student[subject].iloc[0] == "Enrolled":
                    enrolled_subjects.append(subject)
            
            return enrolled_subjects
            
        except Exception as e:
            print(f"Error getting student subjects: {e}")
            return []
    
    def create_subject_attendance_summary(self, subject):
        """Create attendance summary for a specific subject"""
        try:
            subject_dir = os.path.join(self.attendance_dir, subject)
            if not os.path.exists(subject_dir):
                print(f"No attendance data found for {subject}")
                return None
            
            # Get all attendance files for this subject
            attendance_files = [f for f in os.listdir(subject_dir) if f.endswith('.csv') and f != 'attendance.csv']
            
            if not attendance_files:
                print(f"No attendance files found for {subject}")
                return None
            
            # Combine all attendance data
            all_attendance = []
            for file in attendance_files:
                file_path = os.path.join(subject_dir, file)
                try:
                    df = pd.read_csv(file_path)
                    all_attendance.append(df)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
            
            if not all_attendance:
                return None
            
            # Combine all data
            combined_df = pd.concat(all_attendance, ignore_index=True)
            
            # Create summary
            summary = combined_df.groupby(['Enrollment', 'Name']).agg({
                'Date': 'count',  # Total classes attended
                'Attendance_Status': lambda x: (x == 'Present').sum()  # Present classes
            }).reset_index()
            
            summary.columns = ['Enrollment', 'Name', 'Total_Classes', 'Present_Classes']
            summary['Absent_Classes'] = summary['Total_Classes'] - summary['Present_Classes']
            summary['Attendance_Percentage'] = (summary['Present_Classes'] / summary['Total_Classes'] * 100).round(2)
            
            # Save summary
            summary_file = os.path.join(subject_dir, f"{subject}_summary.xlsx")
            summary.to_excel(summary_file, index=False)
            
            print(f"Created attendance summary for {subject}: {summary_file}")
            return summary
            
        except Exception as e:
            print(f"Error creating attendance summary for {subject}: {e}")
            return None
    
    def create_all_subject_summaries(self):
        """Create attendance summaries for all subjects"""
        print("Creating attendance summaries for all subjects...")
        
        for subject in self.subjects:
            self.create_subject_attendance_summary(subject)
        
        print("All subject summaries created!")
    
    def get_subject_statistics(self):
        """Get statistics for all subjects"""
        stats = {}
        
        for subject in self.subjects:
            subject_dir = os.path.join(self.attendance_dir, subject)
            if os.path.exists(subject_dir):
                attendance_files = [f for f in os.listdir(subject_dir) if f.endswith('.csv') and f != 'attendance.csv']
                stats[subject] = {
                    'total_classes': len(attendance_files),
                    'has_data': True
                }
            else:
                stats[subject] = {
                    'total_classes': 0,
                    'has_data': False
                }
        
        return stats

def create_subject_management_gui():
    """Create a GUI for subject management"""
    root = tk.Tk()
    root.title("Subject Management")
    root.geometry("800x600")
    root.configure(background="#1c1c1c")
    
    # Title
    title_label = tk.Label(
        root,
        text="Subject Management System",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 20, "bold")
    )
    title_label.pack(pady=20)
    
    # Subject manager instance
    manager = SubjectManager()
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Tab 1: Subject Overview
    overview_frame = ttk.Frame(notebook)
    notebook.add(overview_frame, text="Subject Overview")
    
    # Subject statistics
    stats = manager.get_subject_statistics()
    
    stats_text = tk.Text(overview_frame, height=15, width=70, bg="#333333", fg="yellow", font=("Courier", 10))
    stats_text.pack(pady=20)
    
    stats_content = "Subject Statistics:\n" + "="*50 + "\n\n"
    for subject, stat in stats.items():
        status = "✓ Has Data" if stat['has_data'] else "✗ No Data"
        stats_content += f"{subject:12} | Classes: {stat['total_classes']:3} | {status}\n"
    
    stats_text.insert("1.0", stats_content)
    stats_text.config(state="disabled")
    
    # Tab 2: Create Summaries
    summary_frame = ttk.Frame(notebook)
    notebook.add(summary_frame, text="Create Summaries")
    
    tk.Label(
        summary_frame,
        text="Create attendance summaries for all subjects",
        bg="#1c1c1c",
        fg="white",
        font=("Verdana", 14)
    ).pack(pady=20)
    
    create_btn = tk.Button(
        summary_frame,
        text="Create All Summaries",
        command=manager.create_all_subject_summaries,
        bg="#333333",
        fg="yellow",
        font=("Verdana", 12, "bold"),
        relief="ridge",
        bd=5,
        width=20,
        height=2
    )
    create_btn.pack(pady=20)
    
    # Tab 3: Student Subjects
    student_frame = ttk.Frame(notebook)
    notebook.add(student_frame, text="Student Subjects")
    
    tk.Label(
        student_frame,
        text="View student subject enrollments",
        bg="#1c1c1c",
        fg="white",
        font=("Verdana", 14)
    ).pack(pady=20)
    
    # Student data display
    student_data = manager.get_student_data()
    if not student_data.empty:
        # Create treeview for student data
        columns = list(student_data.columns)
        tree = ttk.Treeview(student_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for index, row in student_data.iterrows():
            tree.insert("", "end", values=list(row))
        
        tree.pack(pady=20, padx=20, fill="both", expand=True)
    else:
        tk.Label(
            student_frame,
            text="No student data found",
            bg="#1c1c1c",
            fg="red",
            font=("Verdana", 12)
        ).pack(pady=20)
    
    root.mainloop()

def main():
    print("Subject Management System")
    print("=" * 40)
    
    manager = SubjectManager()
    
    # Create summaries for all subjects
    manager.create_all_subject_summaries()
    
    # Show statistics
    stats = manager.get_subject_statistics()
    print("\nSubject Statistics:")
    for subject, stat in stats.items():
        status = "Has Data" if stat['has_data'] else "No Data"
        print(f"{subject:12} | Classes: {stat['total_classes']:3} | {status}")
    
    print("\nSubject management system ready!")

if __name__ == "__main__":
    # Uncomment the line below to run the GUI
    # create_subject_management_gui()
    
    # Or run the command line version
    main()




