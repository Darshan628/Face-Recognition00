#!/usr/bin/env python3
"""
Test script for student registration and Excel saving
"""

import os
import pandas as pd
import csv

def test_student_registration():
    """Test student registration and Excel saving functionality"""
    print("Testing Student Registration and Excel Saving...")
    print("=" * 60)
    
    # Test CSV file creation and reading
    csv_path = "StudentDetails/studentdetails.csv"
    excel_path = "StudentDetails/studentdetails.xlsx"
    
    print(f"1. Checking CSV file: {csv_path}")
    if os.path.exists(csv_path):
        print("✓ CSV file exists")
        
        # Read and display CSV content
        try:
            df = pd.read_csv(csv_path)
            print(f"✓ CSV has {len(df)} students")
            print("Current students:")
            for index, row in df.iterrows():
                print(f"  - {row['Name']} (Enrollment: {row['Enrollment']})")
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
    else:
        print("⚠ CSV file does not exist")
    
    print(f"\n2. Checking Excel file: {excel_path}")
    if os.path.exists(excel_path):
        print("✓ Excel file exists")
        
        # Read and display Excel content
        try:
            df_excel = pd.read_excel(excel_path)
            print(f"✓ Excel has {len(df_excel)} students")
            print("Excel content:")
            print(df_excel.to_string(index=False))
        except Exception as e:
            print(f"❌ Error reading Excel: {e}")
    else:
        print("⚠ Excel file does not exist")
    
    print(f"\n3. Checking Training Images Directory")
    train_path = "TrainingImage"
    if os.path.exists(train_path):
        subdirs = [d for d in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, d))]
        print(f"✓ Found {len(subdirs)} student directories")
        
        for subdir in subdirs:
            image_count = len([f for f in os.listdir(os.path.join(train_path, subdir)) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"  - {subdir}: {image_count} images")
            
            # Check if it has exactly 2 images as expected
            if image_count == 2:
                print(f"    ✓ Perfect! {subdir} has exactly 2 images")
            elif image_count < 2:
                print(f"    ⚠ {subdir} has only {image_count} images (less than 2)")
            else:
                print(f"    ℹ {subdir} has {image_count} images (more than 2)")
    else:
        print("❌ Training images directory does not exist")
    
    print(f"\n4. Testing Excel Creation")
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_excel(excel_path, index=False)
            print("✓ Excel file created/updated successfully")
        else:
            print("⚠ No CSV file to convert to Excel")
    except Exception as e:
        print(f"❌ Error creating Excel file: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")

def create_sample_data():
    """Create sample student data for testing"""
    print("Creating sample student data...")
    
    # Create StudentDetails directory
    os.makedirs("StudentDetails", exist_ok=True)
    
    # Sample data
    sample_students = [
        ["12345", "John Doe"],
        ["67890", "Jane Smith"],
        ["11111", "Test Student"]
    ]
    
    csv_path = "StudentDetails/studentdetails.csv"
    
    # Write sample data to CSV
    with open(csv_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Enrollment", "Name"])
        writer.writerows(sample_students)
    
    print(f"✓ Created sample CSV with {len(sample_students)} students")
    
    # Create Excel file
    try:
        df = pd.read_csv(csv_path)
        excel_path = "StudentDetails/studentdetails.xlsx"
        df.to_excel(excel_path, index=False)
        print(f"✓ Created Excel file: {excel_path}")
    except Exception as e:
        print(f"❌ Error creating Excel: {e}")

def main():
    print("Student Registration Test")
    print("=" * 60)
    
    # Ask user if they want to create sample data
    response = input("Do you want to create sample data for testing? (y/n): ").lower()
    if response == 'y':
        create_sample_data()
        print()
    
    # Run the test
    test_student_registration()
    
    print("\nInstructions:")
    print("1. Register students using the main application")
    print("2. Each student will have exactly 2 photos captured")
    print("3. Student details will be saved to both CSV and Excel files")
    print("4. Excel file will be automatically updated after each registration")

if __name__ == "__main__":
    main()




