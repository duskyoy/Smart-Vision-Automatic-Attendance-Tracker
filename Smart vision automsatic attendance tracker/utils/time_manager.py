import datetime

class TimeManager:
    def __init__(self):
        self.sessions = {
            "Session 1": ("08:30", "09:20"),
            "Session 2": ("09:20", "10:10"),
            "Session 3": ("10:30", "11:20"),
            "Session 4": ("11:20", "12:10"),
            "Session 5": ("13:00", "13:50"),
            "Session 6": ("13:50", "14:40"),
        }

    def get_current_session(self):
        current_time = datetime.datetime.now().strftime("%H:%M")

        for session, (start, end) in self.sessions.items():
            if start <= current_time <= end:
                return session
        return None
