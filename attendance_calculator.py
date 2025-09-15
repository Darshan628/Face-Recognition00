#!/usr/bin/env python3
"""
Attendance Calculator
This script calculates how many days a student needs to attend to achieve target attendance percentage
"""

import pandas as pd
import os
import glob
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class AttendanceCalculator:
    def __init__(self):
        self.attendance_base = "Attendance"
    
    def get_student_attendance(self, enrollment, subject):
        """Get attendance data for a specific student and subject"""
        try:
            subject_dir = os.path.join(self.attendance_base, subject)
            if not os.path.exists(subject_dir):
                return None
            
            # Get all attendance CSV files for this subject
            csv_files = glob.glob(os.path.join(subject_dir, f"{subject}_*.csv"))
            
            if not csv_files:
                return None
            
            # Combine all attendance data
            all_attendance = []
            for file in csv_files:
                try:
                    df = pd.read_csv(file)
                    all_attendance.append(df)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
            
            if not all_attendance:
                return None
            
            # Combine all dataframes
            combined_df = pd.concat(all_attendance, ignore_index=True)
            
            # Filter for specific student
            student_data = combined_df[combined_df['Enrollment'] == str(enrollment)]
            
            if student_data.empty:
                return None
            
            # Calculate attendance statistics
            total_classes = len(student_data)
            present_classes = len(student_data[student_data['Attendance_Status'] == 'Present'])
            absent_classes = total_classes - present_classes
            current_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
            
            return {
                'total_classes': total_classes,
                'present_classes': present_classes,
                'absent_classes': absent_classes,
                'current_percentage': round(current_percentage, 2)
            }
            
        except Exception as e:
            print(f"Error getting student attendance: {e}")
            return None
    
    def calculate_required_days(self, enrollment, subject, target_percentage=70):
        """Calculate how many days student needs to attend to achieve target percentage"""
        try:
            current_stats = self.get_student_attendance(enrollment, subject)
            
            if not current_stats:
                return {
                    'error': f'No attendance data found for enrollment {enrollment} in {subject}'
                }
            
            total_classes = current_stats['total_classes']
            present_classes = current_stats['present_classes']
            current_percentage = current_stats['current_percentage']
            
            # If already above target, no need to attend more
            if current_percentage >= target_percentage:
                return {
                    'current_percentage': current_percentage,
                    'target_percentage': target_percentage,
                    'required_days': 0,
                    'message': f'Congratulations! You already have {current_percentage}% attendance.',
                    'status': 'achieved'
                }
            
            # Calculate required days
            # Formula: (target_percentage * total_classes - present_classes * 100) / (100 - target_percentage)
            required_days = (target_percentage * total_classes - present_classes * 100) / (100 - target_percentage)
            required_days = max(0, int(required_days) + 1)  # Round up and ensure non-negative
            
            # Calculate new total classes and percentage after attending required days
            new_total_classes = total_classes + required_days
            new_present_classes = present_classes + required_days
            new_percentage = (new_present_classes / new_total_classes * 100)
            
            return {
                'current_percentage': current_percentage,
                'target_percentage': target_percentage,
                'required_days': required_days,
                'current_classes': total_classes,
                'current_present': present_classes,
                'new_total_classes': new_total_classes,
                'new_present_classes': new_present_classes,
                'new_percentage': round(new_percentage, 2),
                'message': f'You need to attend {required_days} more days to achieve {target_percentage}% attendance.',
                'status': 'calculation'
            }
            
        except Exception as e:
            return {
                'error': f'Error calculating required days: {e}'
            }

def show_attendance_calculator():
    """Show attendance calculator window"""
    calc_window = tk.Tk()
    calc_window.title("Attendance Calculator")
    calc_window.geometry("600x500")
    calc_window.configure(background="#1c1c1c")
    calc_window.resizable(0, 0)
    
    # Title
    title_label = tk.Label(
        calc_window,
        text="📊 Attendance Calculator",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 20, "bold")
    )
    title_label.pack(pady=20)
    
    # Subtitle
    subtitle_label = tk.Label(
        calc_window,
        text="Calculate how many days you need to attend for 70% attendance",
        bg="#1c1c1c",
        fg="lightgreen",
        font=("Verdana", 12)
    )
    subtitle_label.pack(pady=10)
    
    # Input frame
    input_frame = tk.Frame(calc_window, bg="#1c1c1c")
    input_frame.pack(pady=20)
    
    # Enrollment input
    enrollment_label = tk.Label(
        input_frame,
        text="Enrollment Number:",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 12, "bold")
    )
    enrollment_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    enrollment_entry = tk.Entry(
        input_frame,
        width=20,
        font=("Verdana", 12),
        bg="#333333",
        fg="white"
    )
    enrollment_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # Subject selection
    subject_label = tk.Label(
        input_frame,
        text="Subject:",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 12, "bold")
    )
    subject_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    subject_var = tk.StringVar()
    subject_combo = ttk.Combobox(
        input_frame,
        textvariable=subject_var,
        values=["Maths", "English", "Physics", "Chemistry", "Gujarati"],
        width=18,
        font=("Verdana", 12)
    )
    subject_combo.grid(row=1, column=1, padx=10, pady=10)
    subject_combo.set("Maths")  # Default value
    
    # Target percentage
    target_label = tk.Label(
        input_frame,
        text="Target %:",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 12, "bold")
    )
    target_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    target_entry = tk.Entry(
        input_frame,
        width=20,
        font=("Verdana", 12),
        bg="#333333",
        fg="white"
    )
    target_entry.grid(row=2, column=1, padx=10, pady=10)
    target_entry.insert(0, "70")  # Default 70%
    
    # Calculate button
    calc_button = tk.Button(
        input_frame,
        text="📊 Calculate",
        command=lambda: calculate_attendance(),
        bg="green",
        fg="white",
        font=("Verdana", 12, "bold"),
        width=15,
        height=2
    )
    calc_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    # Result frame
    result_frame = tk.Frame(calc_window, bg="#1c1c1c")
    result_frame.pack(pady=20, fill="both", expand=True)
    
    result_text = tk.Text(
        result_frame,
        height=12,
        width=60,
        bg="#333333",
        fg="white",
        font=("Verdana", 11),
        wrap=tk.WORD
    )
    result_text.pack(padx=20, pady=10)
    
    def calculate_attendance():
        """Calculate attendance and show results"""
        try:
            enrollment = enrollment_entry.get().strip()
            subject = subject_var.get().strip()
            target = float(target_entry.get().strip())
            
            if not enrollment:
                messagebox.showerror("Error", "Please enter enrollment number")
                return
            
            if not subject:
                messagebox.showerror("Error", "Please select a subject")
                return
            
            if target < 0 or target > 100:
                messagebox.showerror("Error", "Target percentage must be between 0 and 100")
                return
            
            # Create calculator instance
            calculator = AttendanceCalculator()
            
            # Calculate required days
            result = calculator.calculate_required_days(enrollment, subject, target)
            
            # Clear previous results
            result_text.delete(1.0, tk.END)
            
            if 'error' in result:
                result_text.insert(tk.END, f"❌ Error: {result['error']}\n", "error")
            else:
                # Display results
                result_text.insert(tk.END, f"📊 ATTENDANCE CALCULATION RESULTS\n", "title")
                result_text.insert(tk.END, "=" * 50 + "\n\n", "separator")
                
                result_text.insert(tk.END, f"🎯 Target Attendance: {result['target_percentage']}%\n", "target")
                result_text.insert(tk.END, f"📈 Current Attendance: {result['current_percentage']}%\n", "current")
                result_text.insert(tk.END, f"📚 Total Classes: {result['current_classes']}\n", "info")
                result_text.insert(tk.END, f"✅ Present Classes: {result['current_present']}\n", "info")
                
                if result['status'] == 'achieved':
                    result_text.insert(tk.END, f"\n🎉 {result['message']}\n", "success")
                else:
                    result_text.insert(tk.END, f"\n📅 Required Days: {result['required_days']}\n", "required")
                    result_text.insert(tk.END, f"📊 New Total Classes: {result['new_total_classes']}\n", "info")
                    result_text.insert(tk.END, f"✅ New Present Classes: {result['new_present_classes']}\n", "info")
                    result_text.insert(tk.END, f"📈 New Percentage: {result['new_percentage']}%\n", "new")
                    result_text.insert(tk.END, f"\n💡 {result['message']}\n", "message")
                
                # Add motivational message
                if result['required_days'] > 0:
                    if result['required_days'] <= 5:
                        result_text.insert(tk.END, f"\n🔥 You're almost there! Just {result['required_days']} more days!\n", "motivation")
                    elif result['required_days'] <= 10:
                        result_text.insert(tk.END, f"\n💪 Keep going! {result['required_days']} days to reach your goal!\n", "motivation")
                    else:
                        result_text.insert(tk.END, f"\n🎯 Stay consistent! You can do it!\n", "motivation")
            
            # Configure text tags for colors
            result_text.tag_configure("title", foreground="yellow", font=("Verdana", 12, "bold"))
            result_text.tag_configure("separator", foreground="gray")
            result_text.tag_configure("target", foreground="blue", font=("Verdana", 11, "bold"))
            result_text.tag_configure("current", foreground="green", font=("Verdana", 11, "bold"))
            result_text.tag_configure("required", foreground="red", font=("Verdana", 11, "bold"))
            result_text.tag_configure("new", foreground="orange", font=("Verdana", 11, "bold"))
            result_text.tag_configure("info", foreground="lightblue")
            result_text.tag_configure("success", foreground="green", font=("Verdana", 11, "bold"))
            result_text.tag_configure("message", foreground="yellow", font=("Verdana", 11, "italic"))
            result_text.tag_configure("motivation", foreground="pink", font=("Verdana", 11, "bold"))
            result_text.tag_configure("error", foreground="red", font=("Verdana", 11, "bold"))
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    # Close button
    close_button = tk.Button(
        calc_window,
        text="❌ Close",
        command=calc_window.destroy,
        bg="red",
        fg="white",
        font=("Verdana", 12, "bold"),
        width=15,
        height=2
    )
    close_button.pack(pady=10)
    
    calc_window.mainloop()

if __name__ == "__main__":
    show_attendance_calculator()






