import time

class FatigueDetector:
    def __init__(self, blink_threshold=0.2, fatigue_threshold=0.25):
        self.blink_threshold = blink_threshold  # Seuil EAR pour détecter un clignement
        self.fatigue_threshold = fatigue_threshold  # Durée moyenne indiquant la fatigue
        self.blink_count = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.average_blink_duration = 0
        self.total_blink_duration = 0

    def detect_blink(self, eye_aspect_ratio):
        """
        Détecte un clignement en fonction du ratio d'aspect de l'œil (EAR).
        """
        if eye_aspect_ratio < self.blink_threshold:  # Si EAR < seuil, l'œil est considéré fermé
            if not self.is_blinking:
                self.is_blinking = True
                self.blink_start_time = time.time()
        else:
            if self.is_blinking:  # Clignement terminé lorsque EAR repasse au-dessus du seuil
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
        Détermine si l'utilisateur est fatigué en fonction de la durée moyenne des clignements.
        """
        return self.average_blink_duration > self.fatigue_threshold
