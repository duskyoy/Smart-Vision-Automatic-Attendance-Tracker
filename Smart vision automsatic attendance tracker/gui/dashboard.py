import tkinter as tk
from tkinter import Label, Button
import os
import subprocess

import sys

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance dashboard")
        self.root.geometry("500x400")

        Label(root, text="Attendance Dashboard ", font=("Arial", 16, "bold")).pack(pady=20)

        Button(root, text="Add Student", command=self.open_add_student, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)
        #Button(root, text="Add Faculty", command=self.open_add_faculty, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)
        Button(root, text="Mark Attendance", command=self.open_mark_attendance, font=("Arial", 12), bg="green", fg="white").pack(pady=10)
        Button(root, text="View Attendance", command=self.open_view_attendance, font=("Arial", 12), bg="orange", fg="white").pack(pady=10)
        Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="red", fg="white").pack(pady=10)

    def open_add_student(self):
        os.system("python gui/add_student.py")

    def open_add_faculty(self):
        os.system("python gui/add_faculty.py")

    def open_mark_attendance(self):
        os.system("python gui/mark_attendance.py")

    def open_view_attendance(self):
        os.system("python gui/view_attendance.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()  