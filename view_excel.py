#!/usr/bin/env python3
"""
Script to view the updated Excel file with subjects
"""

import pandas as pd
import os

def view_excel_file():
    """View the updated Excel file with subjects"""
    print("Viewing Updated Excel File with Subjects")
    print("=" * 60)
    
    excel_file = "StudentDetails/studentdetails.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        print(f"✓ Excel file loaded successfully")
        print(f"✓ Total students: {len(df)}")
        print(f"✓ Columns: {list(df.columns)}")
        
        print(f"\nStudent Data with Subjects:")
        print("=" * 80)
        
        # Display the data in a formatted way
        for index, row in df.iterrows():
            print(f"\nStudent {index + 1}:")
            print(f"  Enrollment: {row['Enrollment']}")
            print(f"  Name: {row['Name']}")
            print(f"  Subjects:")
            for subject in ['Maths', 'English', 'Physics', 'Chemistry', 'Gujarati']:
                if subject in row:
                    status = row[subject] if pd.notna(row[subject]) else "Not Set"
                    print(f"    - {subject}: {status}")
        
        print(f"\n" + "=" * 80)
        print(f"Summary:")
        print(f"- Total students: {len(df)}")
        print(f"- Subjects available: Maths, English, Physics, Chemistry, Gujarati")
        print(f"- All students are enrolled in all subjects by default")
        
        # Show subject enrollment counts
        print(f"\nSubject Enrollment Counts:")
        for subject in ['Maths', 'English', 'Physics', 'Chemistry', 'Gujarati']:
            if subject in df.columns:
                enrolled_count = df[subject].value_counts().get('Enrolled', 0)
                print(f"  - {subject}: {enrolled_count} students enrolled")
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

def main():
    view_excel_file()
    
    print(f"\nFiles created/updated:")
    print(f"- StudentDetails/studentdetails.xlsx (main file)")
    print(f"- StudentDetails/studentdetails.csv (backup)")
    print(f"- StudentDetails/Maths_attendance_template.xlsx")
    print(f"- StudentDetails/English_attendance_template.xlsx")
    print(f"- StudentDetails/Physics_attendance_template.xlsx")
    print(f"- StudentDetails/Chemistry_attendance_template.xlsx")
    print(f"- StudentDetails/Gujarati_attendance_template.xlsx")
    
    print(f"\nNext steps:")
    print(f"1. Use the main application to take attendance for different subjects")
    print(f"2. Each subject will have its own attendance folder")
    print(f"3. Attendance summaries will be created automatically")

if __name__ == "__main__":
    main()




