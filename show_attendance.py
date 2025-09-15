import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject=="":
            t='Please enter the subject name.'
            text_to_speech(t)
    
        filenames = glob(
            f"Attendance/{Subject}/{Subject}*.csv"
        )
        df = []
        for f in filenames:
            try:
                temp_df = pd.read_csv(f)
                # Remove empty rows and ensure consistent data types
                temp_df = temp_df.dropna()
                if len(temp_df) > 0:
                    # Ensure all columns are string type for consistent merging
                    temp_df = temp_df.astype(str)
                    df.append(temp_df)
            except Exception as e:
                print(f"Error reading {f}: {e}")
                continue
        
        if len(df) == 0:
            print("No valid data found")
            return
            
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        # Calculate attendance percentage based on present records
        if len(newdf) > 0:
            # Convert numeric columns back to proper types
            newdf['Enrollment'] = pd.to_numeric(newdf['Enrollment'], errors='coerce')
            newdf = newdf.dropna(subset=['Enrollment'])
            
            # Count total records per student
            student_counts = newdf.groupby(['Enrollment', 'Name']).size().reset_index(name='Total_Records')
            # Count present records per student
            present_counts = newdf[newdf['Attendance_Status'] == 'Present'].groupby(['Enrollment', 'Name']).size().reset_index(name='Present_Records')
            # Merge counts
            attendance_summary = student_counts.merge(present_counts, on=['Enrollment', 'Name'], how='left')
            attendance_summary['Present_Records'] = attendance_summary['Present_Records'].fillna(0)
            attendance_summary['Attendance_Percentage'] = (attendance_summary['Present_Records'] / attendance_summary['Total_Records'] * 100).round(0).astype(int).astype(str) + '%'
            
            # Add star for students who come daily (100% attendance)
            attendance_summary['Name'] = attendance_summary.apply(
                lambda row: f"⭐ {row['Name']}" if row['Attendance_Percentage'] == '100%' else row['Name'], 
                axis=1
            )
            
            # Sort by attendance percentage (descending) to show top students first
            attendance_summary = attendance_summary.sort_values('Attendance_Percentage', ascending=False)
            
            newdf = attendance_summary
        newdf.to_csv(f"Attendance/{Subject}/attendance.csv", index=False)
        
        # Also save to Excel with star formatting
        excel_file = f"Attendance/{Subject}/{Subject}_summary.xlsx"
        newdf.to_excel(excel_file, index=False, sheet_name='Attendance_Summary')

        root = tkinter.Tk()
        root.title("Attendance of "+Subject)
        root.configure(background="#2c3e50")  # Modern dark background
        cs = f"Attendance/{Subject}/attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="#ecf0f1",  # Light text color
                        font=("Segoe UI", 15, " bold "),
                        bg="#2c3e50",  # Modern dark background
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="#34495e")  # Modern dark background
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="#34495e", relief=RIDGE, bd=10, font=("Segoe UI", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="#34495e",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="#34495e",
        fg="#2ecc71",  # Modern green text
        font=("Segoe UI", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
            f"Attendance/{sub}"
            )


    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("Segoe UI", 15, "bold"),
        bg="#3498db",  # Modern blue background
        fg="#ecf0f1",  # Light text
        height=2,
        width=10,
        relief=RIDGE,
        activebackground="#5dade2",
        activeforeground="#2c3e50",
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="#34495e",
        fg="#ecf0f1",
        bd=5,
        relief=RIDGE,
        font=("Segoe UI", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="#2c3e50",  # Modern dark input background
        fg="#ecf0f1",  # Light text
        relief=RIDGE,
        font=("Segoe UI", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("Segoe UI", 15, "bold"),
        bg="#27ae60",  # Modern green background
        fg="#ecf0f1",  # Light text
        height=2,
        width=12,
        relief=RIDGE,
        activebackground="#2ecc71",
        activeforeground="#2c3e50",
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
