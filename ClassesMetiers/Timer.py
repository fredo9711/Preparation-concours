from datetime import datetime

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        self.end_time = datetime.now()

    def get_duration_seconds(self) -> int:
        if self.start_time and self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        else:
            raise ValueError("Le Timer n'a pas été correctement démarré ou arrêté.")
