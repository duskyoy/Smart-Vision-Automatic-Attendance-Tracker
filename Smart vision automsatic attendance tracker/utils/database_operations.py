import sqlite3

class DatabaseOperations:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    

    def create_tables(self):
        # Create 'students' table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            Class TEXT NOT NULL                
                            
                            
        )
        """)

        # Create 'attendance' table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            Class TEXT NOT NULL,         
            
            session INTEGER NOT NULL,
            time TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """)

        self.conn.commit()

    def mark_attendance(self, student_id, name, Class, session, time, date):
        """Insert attendance record."""
        self.cursor.execute("""
        INSERT INTO attendance (student_id, name, Class, session, date, time) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, name, Class, session, time, date))
        self.conn.commit()

    def fetch_attendance(self, date):
        """Fetch attendance records for a given date."""
        self.cursor.execute("SELECT * FROM attendance WHERE date = ?", (date,))
        return self.cursor.fetchall()

    def close(self):
        """Close database connection."""
        self.conn.close()

# Initialize database
if __name__ == "__main__":
    db = DatabaseOperations()
    print("Database tables created successfully.")
    db.close()
