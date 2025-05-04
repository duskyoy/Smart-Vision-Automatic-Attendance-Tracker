import tkinter as tk
from tkinter import messagebox
import cv2
import os
import sqlite3

class AddStudent:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Student")
        self.root.geometry("300x300")

        tk.Label(self.root, text="Student ID").pack()
        self.entry_id = tk.Entry(self.root)
        self.entry_id.pack()

        tk.Label(self.root, text="Name").pack()
        self.entry_name = tk.Entry(self.root)
        self.entry_name.pack()

        tk.Label(self.root, text="Class").pack()
        self.entry_Class = tk.Entry(self.root)
        self.entry_Class.pack()

        

        self.capture_btn = tk.Button(self.root, text="Capture Face", command=self.capture_face)
        self.capture_btn.pack()

        self.save_btn = tk.Button(self.root, text="Train and Save", command=self.save_student)
        self.save_btn.pack()

    def capture_face(self):
        student_id = self.entry_id.get()
        student_name = self.entry_name.get()
        student_Class = self.entry_Class.get()
        
        if not student_id or not student_name or not student_Class:
            messagebox.showerror("Error", "Please enter Student ID and Name")
            return
        
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)

        count = 0
        student_dir = f"dataset/students/{student_id}" 
        os.makedirs(student_dir, exist_ok=True)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                count += 1
                face_img = frame[y:y+h, x:x+w]
                cv2.imwrite(f"{student_dir}/{count}.jpg", face_img)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            cv2.imshow("Capturing Faces", frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 10:
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", "Face images captured successfully")

    def save_student(self):
        student_id = self.entry_id.get()
        student_name = self.entry_name.get()
        student_Class=self.entry_Class.get()

        if not student_id or not student_name:
            messagebox.showerror("Error", "Please enter Student ID and Name")
            return
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, name TEXT, Class TEXT)")
        cursor.execute("INSERT INTO students (student_id, name, Class) VALUES (?, ?, ?)", (student_id, student_name, student_Class))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Student faces trained and added successfully")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AddStudent(root)
    root.mainloop()
