import time

class FusionEngine:
    def __init__(self):
        self.start_time = None
        self.trigger_time = 5  # seconds

    def update(self, face_score, voice_score):
        if face_score > 25 and voice_score > 15:
            if self.start_time is None:
                self.start_time = time.time()

            if time.time() - self.start_time > self.trigger_time:
                return True
        else:
            self.start_time = None

        return False
