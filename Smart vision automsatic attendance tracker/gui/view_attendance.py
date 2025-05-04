import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import pandas as pd

def fetch_attendance(selected_date=None):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        if selected_date:
            cursor.execute("SELECT * FROM attendance WHERE Date = ?", (selected_date,))
        else:
            cursor.execute("SELECT * FROM attendance")
        records = cursor.fetchall()
        conn.close()
        return records
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching records: {e}")
        return []

def populate_tree():
    selected_date = date_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    records = fetch_attendance(selected_date)
    for record in records:
        tree.insert("", "end", values=record)

def export_to_excel():
    selected_date = date_entry.get()
    records = fetch_attendance(selected_date)
    if not records:
        messagebox.showwarning("No Data", "No attendance records to export for the selected date.")
        return
    df = pd.DataFrame(records, columns=["ID", "Student Name", "Student ID", "Class", "Session", "Time", "Date"])
    filename = f"attendance_records/{selected_date}.xlsx"
    df.to_excel(filename, index=False)
    messagebox.showinfo("Success", f"Attendance exported to {filename}")

root = tk.Tk()
root.title("View Attendance")
root.geometry("850x550")

frame = tk.Frame(root)
frame.pack(pady=10)

# Date selection
tk.Label(root, text="Select Date:").pack(pady=5)
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry.pack(pady=5)

columns = ("ID", "Student Name", "Student ID", "Class", "Session", "Time", "Date")
tree = ttk.Treeview(frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=110)

tree.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

refresh_btn = tk.Button(btn_frame, text="Filter Attendance", command=populate_tree)
refresh_btn.grid(row=0, column=0, padx=10)

export_btn = tk.Button(btn_frame, text="Export to Excel", command=export_to_excel)
export_btn.grid(row=0, column=1, padx=10)

populate_tree()

root.mainloop()
