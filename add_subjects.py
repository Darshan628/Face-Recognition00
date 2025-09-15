#!/usr/bin/env python3
"""
Script to add subjects to the student details Excel file
"""

import pandas as pd
import os

def add_subjects_to_excel():
    """Add subjects to the student details Excel file"""
    print("Adding subjects to Excel file...")
    print("=" * 50)
    
    # Define the subjects
    subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]
    
    # File paths
    csv_path = "StudentDetails/studentdetails.csv"
    excel_path = "StudentDetails/studentdetails.xlsx"
    
    try:
        # Check if CSV file exists
        if not os.path.exists(csv_path):
            print(f"❌ CSV file not found: {csv_path}")
            print("Please register some students first.")
            return False
        
        # Read existing data
        df = pd.read_csv(csv_path)
        print(f"✓ Found {len(df)} students in CSV file")
        
        # Add subject columns to the dataframe
        for subject in subjects:
            if subject not in df.columns:
                df[subject] = ""  # Initialize with empty string
                print(f"✓ Added subject column: {subject}")
            else:
                print(f"ℹ Subject column already exists: {subject}")
        
        # Save updated data to both CSV and Excel
        df.to_csv(csv_path, index=False)
        print(f"✓ Updated CSV file: {csv_path}")
        
        df.to_excel(excel_path, index=False)
        print(f"✓ Updated Excel file: {excel_path}")
        
        # Display the updated structure
        print(f"\nUpdated Excel structure:")
        print(f"Columns: {list(df.columns)}")
        print(f"Total students: {len(df)}")
        
        # Show sample data
        print(f"\nSample data:")
        print(df.head().to_string(index=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_subject_attendance_template():
    """Create a template for subject-wise attendance tracking"""
    print("\nCreating subject attendance template...")
    
    subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]
    
    # Create a template for each subject
    for subject in subjects:
        template_data = {
            'Student_ID': [],
            'Student_Name': [],
            'Total_Classes': [],
            'Present_Classes': [],
            'Absent_Classes': [],
            'Attendance_Percentage': []
        }
        
        template_df = pd.DataFrame(template_data)
        template_path = f"StudentDetails/{subject}_attendance_template.xlsx"
        template_df.to_excel(template_path, index=False)
        print(f"✓ Created template: {template_path}")

def update_student_details_with_subjects():
    """Update existing student details with subject information"""
    print("\nUpdating student details with subjects...")
    
    csv_path = "StudentDetails/studentdetails.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        
        # Add subjects if they don't exist
        subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]
        for subject in subjects:
            if subject not in df.columns:
                df[subject] = "Enrolled"  # Mark all students as enrolled by default
        
        # Save updated file
        df.to_csv(csv_path, index=False)
        df.to_excel("StudentDetails/studentdetails.xlsx", index=False)
        
        print(f"✓ Updated student details with subjects")
        print(f"✓ All students marked as 'Enrolled' in all subjects")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating student details: {e}")
        return False

def main():
    print("Subject Management for Attendance System")
    print("=" * 50)
    
    # Add subjects to Excel
    success = add_subjects_to_excel()
    
    if success:
        # Create subject templates
        create_subject_attendance_template()
        
        # Update student details
        update_student_details_with_subjects()
        
        print("\n🎉 Subjects added successfully!")
        print("\nSubjects added:")
        print("- Maths")
        print("- English") 
        print("- Physics")
        print("- Chemistry")
        print("- Gujarati")
        
        print(f"\nFiles updated:")
        print(f"- StudentDetails/studentdetails.xlsx")
        print(f"- StudentDetails/studentdetails.csv")
        
        print(f"\nTemplates created:")
        for subject in ["Maths", "English", "Physics", "Chemistry", "Gujarati"]:
            print(f"- StudentDetails/{subject}_attendance_template.xlsx")
        
    else:
        print("\n❌ Failed to add subjects. Please check the error messages above.")

if __name__ == "__main__":
    main()




