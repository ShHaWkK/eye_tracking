import time

class FatigueDetector:
    def __init__(self, blink_threshold=0.25, fatigue_duration_threshold=0.3, blink_frequency_threshold=8, check_interval=30, min_blink_duration=0.1, inactivity_timeout=5):
        self.blink_threshold = blink_threshold
        self.fatigue_duration_threshold = fatigue_duration_threshold
        self.blink_frequency_threshold = blink_frequency_threshold
        self.check_interval = check_interval
        self.min_blink_duration = min_blink_duration
        self.inactivity_timeout = inactivity_timeout

        self.blink_count = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.blink_durations = []
        self.last_check_time = time.time()
        self.blinks_in_interval = 0
        self.last_blink_time = time.time()

    def detect_blink(self, eye_aspect_ratio):
        if eye_aspect_ratio < self.blink_threshold:
            if not self.is_blinking:
                self.is_blinking = True
                self.blink_start_time = time.time()
        else:
            if self.is_blinking:
                blink_duration = time.time() - self.blink_start_time
                if blink_duration >= self.min_blink_duration:
                    self.blink_count += 1
                    self.blink_durations.append(blink_duration)
                    self.blinks_in_interval += 1
                    self.last_blink_time = time.time()
                self.is_blinking = False

    def is_fatigued(self):
        average_blink_duration = sum(self.blink_durations) / len(self.blink_durations) if self.blink_durations else 0
        if average_blink_duration > self.fatigue_duration_threshold:
            return True

        if time.time() - self.last_check_time >= self.check_interval:
            if self.blinks_in_interval > self.blink_frequency_threshold:
                self.blinks_in_interval = 0
                self.last_check_time = time.time()
                return True
            self.blinks_in_interval = 0
            self.last_check_time = time.time()

        if time.time() - self.last_blink_time > self.inactivity_timeout:
            print("Inactivité prolongée détectée")
            return True

        return False


    def calculate_average_blink_duration(self):
        return sum(self.blink_durations) / len(self.blink_durations) if self.blink_durations else 0


    def get_blink_count(self):
        """
        Retourne le nombre total de clignements détectés.
        """
        return self.blink_count

    def reset(self):
        """
        Réinitialise les données de fatigue et de clignement pour un nouveau cycle de détection.
        """
        self.blink_count = 0
        self.blink_durations.clear()
        self.blinks_in_interval = 0
        self.last_check_time = time.time()
        self.fatigue_alert_shown = False
        print("Données de détection de fatigue réinitialisées")  # Debug
