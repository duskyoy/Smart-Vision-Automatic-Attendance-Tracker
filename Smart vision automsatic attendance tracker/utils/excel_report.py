import pandas as pd
import sqlite3
from datetime import datetime

class ExcelExport:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")

    def export_to_excel(self):
        date = datetime.now().strftime("%Y-%m-%d")
        query = "SELECT * FROM attendance WHERE date = ?"
        df = pd.read_sql_query(query, self.conn, params=(date,))

        if not df.empty:
            file_path = f"attendance_records/{date}.xlsx"
            df.to_excel(file_path, index=False)
            print(f"Attendance exported successfully to {file_path}")

    def close(self):
        self.conn.close()
