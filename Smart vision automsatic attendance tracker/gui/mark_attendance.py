import cv2
import sqlite3
import datetime
import time
from tkinter import Tk, Label, Button, Entry
from face_recognition_module import load_known_faces, recognize_faces

# Load known face encodings before starting attendance
known_encodings, known_ids = load_known_faces()

# Function to connect to SQLite Database
def connect_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            name TEXT,
            Class TEXT,
            session TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    return conn, cursor

# Function to check if a student has already been marked present
def is_already_marked(cursor, student_id, session, date):
    cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND session = ? AND date = ?", 
                   (student_id, session, date))
    return cursor.fetchone() is not None

# Function to get student details from database
def get_student_details(cursor, student_id):
    cursor.execute("SELECT name, class FROM students WHERE student_id = ?", (student_id,))
    result = cursor.fetchone()
    return result if result else (f"Unknown-{student_id}", "Unknown")  # Default if name/class not found

# Function to mark attendance
def mark_attendance():
    session = session_entry.get().strip()
    if not session or not session.isdigit() or int(session) not in range(1, 7):
        notification_label.config(text="⚠ Invalid Session! Enter 1-6.", fg="red")
        return

    cam = cv2.VideoCapture(0)  # Open webcam
    start_time = time.time()
    timeout = 50  # Set time limit for recognition

    conn, cursor = connect_db()
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")

    recognized_students = set()  # Store recognized student IDs to avoid duplicate processing

    while time.time() - start_time < timeout:
        ret, frame = cam.read()
        if not ret:
            continue

        recognized_ids = recognize_faces(frame, known_encodings, known_ids)

        if recognized_ids:
            for student_index in recognized_ids:
                student_id = student_index  # No need to look up again, it's already the ID
                
                # Ensure each student is processed only once per session
                if student_id in recognized_students:
                    continue
                
                student_name, student_Class = get_student_details(cursor, student_id)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Check if already marked
                if not is_already_marked(cursor, student_id, session, date_today):
                    cursor.execute("INSERT INTO attendance (student_id, name, Class, session, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                                   (student_id, student_name, student_Class, session, date_today, timestamp.split()[1]))
                    conn.commit()
                    recognized_students.add(student_id)  # Store marked student ID
                    
                    cv2.putText(frame, f"{student_name} Marked", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Removed '???'
                else:
                    cv2.putText(frame, f"{student_name} Already Marked", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Advance Automated Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break

    cam.release()
    cv2.destroyAllWindows()
    conn.close()
    
    notification_label.config(text="✅ Attendance Successfully Saved!", fg="green")

# GUI Setup
root = Tk()
root.title("Mark Attendance")
root.geometry("400x250")

Label(root, text="Enter Session (1-6):", font=("Arial", 14)).pack(pady=10)
session_entry = Entry(root, font=("Arial", 14))
session_entry.pack(pady=5)

Button(root, text="Mark Attendance", font=("Arial", 14), command=mark_attendance).pack(pady=20)
notification_label = Label(root, text="", font=("Arial", 12))
notification_label.pack()

root.mainloop()
