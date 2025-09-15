#!/usr/bin/env python3
"""
Subject selector for attendance system
"""

import tkinter as tk
from tkinter import ttk
import os

def create_subject_selector(text_to_speech):
    """Create a subject selection window with predefined subjects"""
    
    # Predefined subjects
    subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]
    
    def on_subject_select():
        """Handle subject selection"""
        selected_subject = subject_var.get()
        if selected_subject:
            print(f"Selected subject: {selected_subject}")
            text_to_speech(f"Selected subject: {selected_subject}")
            # Close the window and return the selected subject
            subject_window.destroy()
            return selected_subject
        else:
            text_to_speech("Please select a subject")
    
    def on_custom_subject():
        """Handle custom subject entry"""
        custom_subject = custom_entry.get().strip()
        if custom_subject:
            print(f"Custom subject: {custom_subject}")
            text_to_speech(f"Custom subject: {custom_subject}")
            subject_window.destroy()
            return custom_subject
        else:
            text_to_speech("Please enter a subject name")
    
    # Create the subject selection window
    subject_window = tk.Tk()
    subject_window.title("Select Subject")
    subject_window.geometry("500x400")
    subject_window.configure(background="#1c1c1c")
    subject_window.resizable(0, 0)
    
    # Title
    title_label = tk.Label(
        subject_window,
        text="Select Subject for Attendance",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 20, "bold")
    )
    title_label.pack(pady=20)
    
    # Subject selection frame
    selection_frame = tk.Frame(subject_window, bg="#1c1c1c")
    selection_frame.pack(pady=20)
    
    # Predefined subjects
    tk.Label(
        selection_frame,
        text="Choose from predefined subjects:",
        bg="#1c1c1c",
        fg="white",
        font=("Verdana", 14, "bold")
    ).pack(pady=10)
    
    subject_var = tk.StringVar()
    
    # Create radio buttons for each subject
    for i, subject in enumerate(subjects):
        rb = tk.Radiobutton(
            selection_frame,
            text=subject,
            variable=subject_var,
            value=subject,
            bg="#1c1c1c",
            fg="yellow",
            font=("Verdana", 12),
            selectcolor="#333333",
            activebackground="#1c1c1c",
            activeforeground="yellow"
        )
        rb.pack(anchor="w", padx=20, pady=5)
    
    # Custom subject entry
    tk.Label(
        selection_frame,
        text="Or enter custom subject:",
        bg="#1c1c1c",
        fg="white",
        font=("Verdana", 14, "bold")
    ).pack(pady=(20, 10))
    
    custom_entry = tk.Entry(
        selection_frame,
        width=20,
        font=("Verdana", 12),
        bg="#333333",
        fg="yellow",
        relief="ridge",
        bd=5
    )
    custom_entry.pack(pady=10)
    
    # Buttons frame
    button_frame = tk.Frame(subject_window, bg="#1c1c1c")
    button_frame.pack(pady=20)
    
    # Select button
    select_btn = tk.Button(
        button_frame,
        text="Select Subject",
        command=on_subject_select,
        bg="#333333",
        fg="yellow",
        font=("Verdana", 12, "bold"),
        relief="ridge",
        bd=5,
        width=15,
        height=2
    )
    select_btn.pack(side="left", padx=10)
    
    # Custom button
    custom_btn = tk.Button(
        button_frame,
        text="Use Custom",
        command=on_custom_subject,
        bg="#333333",
        fg="yellow",
        font=("Verdana", 12, "bold"),
        relief="ridge",
        bd=5,
        width=15,
        height=2
    )
    custom_btn.pack(side="left", padx=10)
    
    # Instructions
    instructions = tk.Label(
        subject_window,
        text="Instructions:\n1. Select a predefined subject OR\n2. Enter a custom subject name\n3. Click the appropriate button",
        bg="#1c1c1c",
        fg="lightgray",
        font=("Verdana", 10),
        justify="left"
    )
    instructions.pack(pady=20)
    
    # Center the window
    subject_window.update_idletasks()
    x = (subject_window.winfo_screenwidth() // 2) - (subject_window.winfo_width() // 2)
    y = (subject_window.winfo_screenheight() // 2) - (subject_window.winfo_height() // 2)
    subject_window.geometry(f"+{x}+{y}")
    
    # Start the window
    subject_window.mainloop()

def get_available_subjects():
    """Get list of available subjects from the system"""
    subjects = ["Maths", "English", "Physics", "Chemistry", "Gujarati"]
    
    # Check if there are any attendance files for these subjects
    available_subjects = []
    for subject in subjects:
        subject_path = f"Attendance/{subject}"
        if os.path.exists(subject_path):
            available_subjects.append(subject)
    
    return available_subjects if available_subjects else subjects

if __name__ == "__main__":
    def dummy_text_to_speech(text):
        print(f"TTS: {text}")
    
    create_subject_selector(dummy_text_to_speech)




