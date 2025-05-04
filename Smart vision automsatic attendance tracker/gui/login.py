import tkinter as tk
from tkinter import messagebox
import subprocess

# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "hits@123"

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")  # Hide password input
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            messagebox.showinfo("Login Successful", "Welcome to the Attendance System!")
            self.root.destroy()  # Close login window
            subprocess.Popen(["python", "D:/Project AAAS/project AAAS/gui/dashboard.py"])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
