import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance
import attendance_calculator
import smart_attendance_checker

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

window = Tk()
window.title("CLASS VISION - Face Recognition System")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#2c3e50")  # Modern dark blue theme


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#2c3e50")  # Modern dark background
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="#e74c3c",  # Modern red text
        bg="#2c3e50",  # Modern dark background
        font=("Segoe UI", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="#ecf0f1",  # Light text
        bg="#e74c3c",  # Modern red button
        width=9,
        height=1,
        activebackground="#c0392b",
        activeforeground="#ecf0f1",
        font=("Segoe UI", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


# Try to load logo image, use a placeholder if not found
try:
    logo = Image.open("AMS.ico")
except:
    # Create a simple colored rectangle as logo if image not found
    logo = Image.new('RGB', (50, 47), color='yellow')
logo = logo.resize((50, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="#2c3e50", relief=RIDGE, bd=10, font=("Segoe UI", 30, "bold"))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="#2c3e50",)
l1.place(x=470, y=10)


titl = tk.Label(
    window, text="CLASS VISION", bg="#2c3e50", fg="#ecf0f1", font=("Segoe UI", 27, "bold"),
)
titl.place(x=525, y=12) 

a = tk.Label(
    window,
    text="Welcome to CLASS VISION",
    bg="#2c3e50",  # Modern dark blue background
    fg="#3498db",  # Modern blue text color
    bd=10,
    font=("Segoe UI", 35, "bold"),
)
a.pack()


# Load UI images with error handling
try:
    ri = Image.open("UI_Image/register.png")
    r = ImageTk.PhotoImage(ri)
    label1 = Label(window, image=r)
    label1.image = r
    label1.place(x=100, y=270)
except Exception as e:
    print(f"Could not load register image: {e}")
    # Create a placeholder label if image fails to load
    label1 = Label(window, text="Register", bg="#2c3e50", fg="#e74c3c", font=("Segoe UI", 16, "bold"))
    label1.place(x=100, y=270)

try:
    ai = Image.open("UI_Image/attendance.png")
    a = ImageTk.PhotoImage(ai)
    label2 = Label(window, image=a)
    label2.image = a
    label2.place(x=980, y=270)
except Exception as e:
    print(f"Could not load attendance image: {e}")
    # Create a placeholder label if image fails to load
    label2 = Label(window, text="Attendance", bg="#2c3e50", fg="#27ae60", font=("Segoe UI", 16, "bold"))
    label2.place(x=980, y=270)

try:
    vi = Image.open("UI_Image/verifyy.png")
    v = ImageTk.PhotoImage(vi)
    label3 = Label(window, image=v)
    label3.image = v
    label3.place(x=600, y=270)
except Exception as e:
    print(f"Could not load verify image: {e}")
    # Create a placeholder label if image fails to load
    label3 = Label(window, text="Verify", bg="#2c3e50", fg="#f39c12", font=("Segoe UI", 16, "bold"))
    label3.place(x=600, y=270)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register New Student")
    ImageUI.geometry("780x520")
    ImageUI.configure(background="#34495e")  # Modern dark theme for registration window
    ImageUI.resizable(0, 0)
    ImageUI.iconbitmap("AMS.ico")
    titl = tk.Label(ImageUI, bg="#34495e", relief=RIDGE, bd=10, font=("Segoe UI", 30, "bold"))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#34495e", fg="#2ecc71", font=("Segoe UI", 30, "bold"),
    )
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#34495e",  # Modern dark background
        fg="#ecf0f1",  # Light text color
        bd=10,
        font=("Segoe UI", 24, "bold"),
    )
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#34495e",
        fg="#ecf0f1",
        bd=5,
        relief=RIDGE,
        font=("Segoe UI", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#2c3e50",  # Modern dark input background
        fg="#ecf0f1",  # Light text color for input
        relief=RIDGE,
        font=("Segoe UI", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#34495e",
        fg="#ecf0f1",
        bd=5,
        relief=RIDGE,
        font=("Segoe UI", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#2c3e50",  # Modern dark input background
        fg="#ecf0f1",  # Light text color for input
        relief=RIDGE,
        font=("Segoe UI", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    # Relative Phone
    lbl3 = tk.Label(
        ImageUI,
        text="Relative Phone",
        width=10,
        height=2,
        bg="#34495e",
        fg="#ecf0f1",
        bd=5,
        relief=RIDGE,
        font=("Segoe UI", 14),
    )
    lbl3.place(x=120, y=270)
    txt3 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#2c3e50",  # Modern dark input background
        fg="#ecf0f1",  # Light text color for input
        relief=RIDGE,
        font=("Segoe UI", 18, "bold"),
    )
    txt3.place(x=250, y=270)

    lbl4 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#34495e",
        fg="#ecf0f1",
        bd=5,
        relief=RIDGE,
        font=("Segoe UI", 14),
    )
    lbl4.place(x=120, y=340)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#2c3e50",  # Modern dark background for messages
        fg="#ecf0f1",  # Light text color for messages
        relief=RIDGE,
        font=("Segoe UI", 14, "bold"),
    )
    message.place(x=250, y=340)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        l3 = txt3.get()
        
        # Show processing message
        message.configure(
            text="📸 Taking images... Please wait...",
            bg="blue",
            fg="white"
        )
        message.update()
        
        takeImage.TakeImage(
            l1,
            l2,
            l3,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")
        txt3.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="📸 Take Image",
        command=take_image,
        bd=10,
        font=("Segoe UI", 18, "bold"),
        bg="#27ae60",  # Modern green background
        fg="#ecf0f1",  # Light text color
        height=2,
        width=12,
        relief=RAISED,
        activebackground="#2ecc71",
        activeforeground="#2c3e50",
    )
    takeImg.place(x=130, y=350)

    def train_image():
        # Show training message
        message.configure(
            text="🎯 Training model... Please wait...",
            bg="purple",
            fg="white"
        )
        message.update()
        
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="🎯 Train Image",
        command=train_image,
        bd=10,
        font=("Segoe UI", 18, "bold"),
        bg="#3498db",  # Modern blue background
        fg="#ecf0f1",  # Light text color
        height=2,
        width=12,
        relief=RAISED,
        activebackground="#5dade2",
        activeforeground="#2c3e50",
    )
    trainImg.place(x=360, y=350)


def quick_register():
    """Quick registration function that opens registration window directly"""
    text_to_speech("Opening student registration window")
    TakeImageUI()


r = tk.Button(
    window,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("Segoe UI", 16, "bold"),
    bg="#e74c3c",  # Modern red background
    fg="#ecf0f1",  # Light text color
    height=2,
    width=17,
    relief=RAISED,
    activebackground="#c0392b",
    activeforeground="#ecf0f1",
)
r.place(x=100, y=520)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


# Take Attendance Button (Regular button)
attendance_btn = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Segoe UI", 16, "bold"),
    bg="#27ae60",  # Modern green background
    fg="#ecf0f1",  # Light text color
    height=2,
    width=17,
    activebackground="#2ecc71",
    activeforeground="#2c3e50",
)
attendance_btn.place(x=600, y=520)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

def open_attendance_calculator():
    """Open attendance calculator window"""
    text_to_speech("Opening attendance calculator")
    attendance_calculator.show_attendance_calculator()

def check_attendance_status():
    """Check if attendance calculator button should be shown"""
    try:
        should_show, message = smart_attendance_checker.check_attendance_status()
        return should_show
    except:
        return True

def refresh_attendance_status():
    """Refresh attendance status and update UI"""
    global calc_btn
    try:
        should_show, message = smart_attendance_checker.check_attendance_status()
        
        if should_show:
            # Show calculator button
            if calc_btn is None:
                calc_btn = tk.Button(
                    window,
                    text="📊 Attendance Calculator",
                    command=open_attendance_calculator,
                    bd=10,
                    font=("Verdana", 16),
                    bg="purple",
                    fg="white",
                    height=2,
                    width=17,
                )
                calc_btn.place(x=600, y=580)
        else:
            # Hide calculator button and show good attendance message
            if calc_btn:
                calc_btn.destroy()
                calc_btn = None
            
            good_attendance_label = tk.Label(
                window,
                text="🎉 Great! All students have good attendance!",
                bg="#2c3e50",
                fg="#2ecc71",
                font=("Segoe UI", 14, "bold"),
            )
            good_attendance_label.place(x=500, y=580)
        
        text_to_speech(message)
        
    except Exception as e:
        print(f"Error refreshing attendance status: {e}")



# View Attendance Button (Regular button)
view_btn = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Segoe UI", 16, "bold"),
    bg="#3498db",  # Modern blue background
    fg="#ecf0f1",  # Light text color
    height=2,
    width=17,
    activebackground="#5dade2",
    activeforeground="#2c3e50",
)
view_btn.place(x=1000, y=520)

# Attendance Calculator Button (Conditional)
calc_btn = None
if check_attendance_status():
    calc_btn = tk.Button(
        window,
        text="📊 Attendance Calculator",
        command=open_attendance_calculator,
        bd=10,
        font=("Segoe UI", 16, "bold"),
        bg="#9b59b6",  # Modern purple background
        fg="#ecf0f1",  # Light text color
        height=2,
        width=17,
        activebackground="#8e44ad",
        activeforeground="#2c3e50",
    )
    calc_btn.place(x=600, y=580)
else:
    # Show message that attendance is good
    good_attendance_label = tk.Label(
        window,
        text="🎉 Great! All students have good attendance!",
        bg="#2c3e50",
        fg="#2ecc71",
        font=("Segoe UI", 14, "bold"),
    )
    good_attendance_label.place(x=500, y=580)


# Refresh Attendance Status Button
refresh_btn = tk.Button(
    window,
    text="🔄 Refresh Status",
    command=refresh_attendance_status,
    bd=5,
    font=("Segoe UI", 12, "bold"),
    bg="#f39c12",  # Modern orange background
    fg="#2c3e50",  # Dark text color
    height=1,
    width=15,
    activebackground="#e67e22",
    activeforeground="#ecf0f1",
)
refresh_btn.place(x=1000, y=640)

# Excel Summary Button
def open_excel_summary():
    """Open Excel summary with star ratings"""
    text_to_speech("Opening Excel summary with star ratings")
    import os
    import glob
    
    # Get all subject folders
    subject_folders = glob.glob("Attendance/*/")
    if not subject_folders:
        text_to_speech("No attendance data found")
        return
    
    # Show subject selection
    subject_window = tk.Toplevel(window)
    subject_window.title("Select Subject for Excel Summary")
    subject_window.geometry("400x300")
    subject_window.configure(bg="black")
    
    tk.Label(subject_window, text="Select Subject:", bg="black", fg="yellow", font=("Verdana", 14, "bold")).pack(pady=20)
    
    for folder in subject_folders:
        subject_name = folder.split("/")[1]
        btn = tk.Button(
            subject_window,
            text=f"📊 {subject_name.title()}",
            command=lambda s=subject_name: open_subject_excel(s, subject_window),
            bg="green",
            fg="white",
            font=("Verdana", 12),
            width=20,
            height=2
        )
        btn.pack(pady=5)

def open_subject_excel(subject, parent_window):
    """Open Excel file for specific subject"""
    parent_window.destroy()
    excel_file = f"Attendance/{subject}/{subject}_summary.xlsx"
    if os.path.exists(excel_file):
        os.startfile(excel_file)
        text_to_speech(f"Opening Excel summary for {subject}")
    else:
        text_to_speech(f"No Excel summary found for {subject}")

excel_btn = tk.Button(
    window,
    text="📊 Excel Summary",
    command=open_excel_summary,
    bd=10,
    font=("Segoe UI", 16, "bold"),
    bg="#16a085",  # Modern teal background
    fg="#ecf0f1",  # Light text color
    height=2,
    width=17,
    activebackground="#1abc9c",
    activeforeground="#2c3e50",
)
excel_btn.place(x=400, y=660)

# QR Code Attendance Button
def qr_attendance():
    """Take attendance using QR code scanning"""
    text_to_speech("Opening QR code attendance scanner")
    try:
        from qr_attendance import QRAttendanceSystem
        qr_system = QRAttendanceSystem()
        
        # Get subject selection
        subject_window = tk.Toplevel(window)
        subject_window.title("Select Subject for QR Attendance")
        subject_window.geometry("400x300")
        subject_window.configure(bg="black")
        
        tk.Label(subject_window, text="Select Subject for QR Attendance:", 
                bg="black", fg="yellow", font=("Verdana", 14, "bold")).pack(pady=20)
        
        # Get available subjects
        import glob
        subject_folders = glob.glob("Attendance/*/")
        subjects = [folder.split("/")[1] for folder in subject_folders]
        
        if not subjects:
            tk.Label(subject_window, text="No subjects found. Please create attendance folders first.", 
                    bg="black", fg="red", font=("Verdana", 12)).pack(pady=20)
            return
        
        for subject in subjects:
            btn = tk.Button(
                subject_window,
                text=f"📱 {subject.title()}",
                command=lambda s=subject: start_qr_scanning(s, subject_window, qr_system),
                bg="purple",
                fg="white",
                font=("Verdana", 12),
                width=20,
                height=2
            )
            btn.pack(pady=5)
            
    except Exception as e:
        text_to_speech(f"Error opening QR scanner: {str(e)}")

def start_qr_scanning(subject, parent_window, qr_system):
    """Start QR code scanning for attendance"""
    parent_window.destroy()
    text_to_speech(f"Starting QR code scanning for {subject}")
    
    # Scan QR code
    student_info = qr_system.scan_qr_code()
    
    if student_info:
        # Mark attendance
        success = qr_system.mark_attendance_by_qr(subject, student_info)
        if success:
            text_to_speech(f"Attendance marked for {student_info.get('NAME', 'Unknown')}")
        else:
            text_to_speech("Failed to mark attendance")
    else:
        text_to_speech("No QR code detected or scanning cancelled")

qr_btn = tk.Button(
    window,
    text="📱 QR Attendance",
    command=qr_attendance,
    bd=10,
    font=("Segoe UI", 16, "bold"),
    bg="#8e44ad",  # Modern purple background
    fg="#ecf0f1",  # Light text color
    height=2,
    width=17,
    activebackground="#9b59b6",
    activeforeground="#2c3e50",
)
qr_btn.place(x=200, y=660)

# SMS Notification Button
def send_absent_notifications():
    """Send SMS notifications to relatives of absent students"""
    text_to_speech("Opening SMS notification system")
    try:
        from sms_notification import SMSNotificationSystem
        sms_system = SMSNotificationSystem()
        
        # Get subject and date selection
        notification_window = tk.Toplevel(window)
        notification_window.title("Send Absent Notifications")
        notification_window.geometry("500x400")
        notification_window.configure(bg="black")
        
        tk.Label(notification_window, text="Send SMS to Absent Students", 
                bg="black", fg="yellow", font=("Verdana", 16, "bold")).pack(pady=20)
        
        # Subject selection
        tk.Label(notification_window, text="Select Subject:", 
                bg="black", fg="white", font=("Verdana", 12, "bold")).pack(pady=10)
        
        import glob
        subject_folders = glob.glob("Attendance/*/")
        subjects = [folder.split("/")[1] for folder in subject_folders]
        
        if not subjects:
            tk.Label(notification_window, text="No subjects found.", 
                    bg="black", fg="red", font=("Verdana", 12)).pack(pady=20)
            return
        
        subject_var = tk.StringVar(value=subjects[0])
        subject_frame = tk.Frame(notification_window, bg="black")
        subject_frame.pack(pady=10)
        
        for subject in subjects:
            rb = tk.Radiobutton(subject_frame, text=subject.title(), variable=subject_var, 
                              value=subject, bg="black", fg="white", font=("Verdana", 10))
            rb.pack(anchor="w")
        
        # Date selection
        tk.Label(notification_window, text="Select Date:", 
                bg="black", fg="white", font=("Verdana", 12, "bold")).pack(pady=10)
        
        date_var = tk.StringVar(value=datetime.datetime.now().strftime('%Y-%m-%d'))
        date_entry = tk.Entry(notification_window, textvariable=date_var, 
                            font=("Verdana", 12), width=15)
        date_entry.pack(pady=5)
        
        # Send button
        send_btn = tk.Button(
            notification_window,
            text="📱 Send Notifications",
            command=lambda: send_notifications(sms_system, subject_var.get(), date_var.get(), notification_window),
            bg="red",
            fg="white",
            font=("Verdana", 12, "bold"),
            width=20,
            height=2
        )
        send_btn.pack(pady=20)
        
    except Exception as e:
        text_to_speech(f"Error opening SMS system: {str(e)}")

def send_notifications(sms_system, subject, date, parent_window):
    """Send notifications for absent students"""
    parent_window.destroy()
    text_to_speech(f"Sending notifications for {subject} on {date}")
    
    try:
        sms_system.notify_absent_students(subject, date)
        text_to_speech("Notifications sent successfully")
    except Exception as e:
        text_to_speech(f"Error sending notifications: {str(e)}")

sms_btn = tk.Button(
    window,
    text="📱 SMS Notify",
    command=send_absent_notifications,
    bd=10,
    font=("Segoe UI", 16, "bold"),
    bg="#e74c3c",  # Modern red background
    fg="#ecf0f1",  # Light text color
    height=2,
    width=17,
    activebackground="#c0392b",
    activeforeground="#ecf0f1",
)
sms_btn.place(x=600, y=660)

# Exit Button (Regular button)
exit_btn = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("Segoe UI", 16, "bold"),
    bg="#95a5a6",  # Modern gray background
    fg="#2c3e50",  # Dark text color
    height=2,
    width=17,
    activebackground="#7f8c8d",
    activeforeground="#ecf0f1",
)
exit_btn.place(x=1000, y=660)


window.mainloop()
