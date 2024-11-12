import time

class FatigueDetector:
    def __init__(self):
        self.blink_count = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.average_blink_duration = 0
        self.total_blink_duration = 0

    def detect_blink(self, eye_aspect_ratio):
        """
        Détecte un clignement en fonction du rapport d'aspect de l'œil (eye_aspect_ratio).
        eye_aspect_ratio : Un rapport basé sur la distance entre les points de l'œil
        """
        if eye_aspect_ratio < 0.2: 
            if not self.is_blinking:
                self.is_blinking = True
                self.blink_start_time = time.time()
        else:
            if self.is_blinking:
                self.is_blinking = False
                blink_duration = time.time() - self.blink_start_time
                self.blink_count += 1
                self.total_blink_duration += blink_duration
                self.average_blink_duration = self.total_blink_duration / self.blink_count

    def get_blink_count(self):
        return self.blink_count

    def get_average_blink_duration(self):
        return self.average_blink_duration

    def is_fatigued(self):
        """
        Détermine si l'utilisateur est fatigué en fonction de la fréquence et de la durée moyenne des clignements.
        """
        return self.average_blink_duration > 0.25
