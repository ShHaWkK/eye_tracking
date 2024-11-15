import time

class FatigueDetector:
    def __init__(self, blink_threshold=0.25, fatigue_duration_threshold=0.3, blink_frequency_threshold=8, check_interval=30, min_blink_duration=0.1, max_blink_duration=0.5, inactivity_timeout=5):
        """
        Initialise le détecteur de fatigue et de clignements avancé.
        
        :param blink_threshold: Seuil EAR pour détecter un œil fermé.
        :param fatigue_duration_threshold: Durée moyenne de clignement pour indiquer la fatigue.
        :param blink_frequency_threshold: Nombre de clignements en un intervalle pour indiquer la fatigue.
        :param check_interval: Intervalle en secondes pour réévaluer la fatigue.
        :param min_blink_duration: Durée minimale d'un clignement pour être comptabilisé.
        :param max_blink_duration: Durée maximale d'un clignement pour éviter de compter les fermetures prolongées.
        :param inactivity_timeout: Temps sans clignements au-delà duquel l'inactivité est suspectée.
        """
        self.blink_threshold = blink_threshold
        self.fatigue_duration_threshold = fatigue_duration_threshold
        self.blink_frequency_threshold = blink_frequency_threshold
        self.check_interval = check_interval
        self.min_blink_duration = min_blink_duration
        self.max_blink_duration = max_blink_duration
        self.inactivity_timeout = inactivity_timeout

        # Variables de comptage et de timing
        self.blink_count = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.blink_durations = []
        self.last_check_time = time.time()
        self.blinks_in_interval = 0
        self.last_blink_time = time.time()
        self.fatigue_alert = False

    def detect_blink(self, eye_aspect_ratio):
        """
        Détecte les clignements basés sur le ratio d'aspect de l'œil (EAR).
        
        :param eye_aspect_ratio: Ratio d'aspect de l'œil pour évaluer s'il est ouvert ou fermé.
        :return: bool - True si un clignement est détecté, sinon False.
        """
        if eye_aspect_ratio < self.blink_threshold:
            # Début d'un clignement
            if not self.is_blinking:
                self.is_blinking = True
                self.blink_start_time = time.time()
        else:
            # Fin d'un clignement
            if self.is_blinking:
                blink_duration = time.time() - self.blink_start_time
                if self.min_blink_duration <= blink_duration <= self.max_blink_duration:
                    # Clignement valide
                    self.blink_count += 1
                    self.blink_durations.append(blink_duration)
                    self.blinks_in_interval += 1
                    self.last_blink_time = time.time()
                    print(f"Clignement détecté - Durée: {blink_duration:.3f}s")
                self.is_blinking = False

        # Détecter une inactivité prolongée
        if time.time() - self.last_blink_time > self.inactivity_timeout:
            print("Inactivité détectée.")
            self.reset()  # Réinitialise en cas d'inactivité

        return self.is_blinking

    def is_fatigued(self):
        """
        Évalue la fatigue de l'utilisateur sur la base de la durée et de la fréquence des clignements.
        
        :return: bool - True si la fatigue est détectée, sinon False.
        """
        # Calcul de la durée moyenne des clignements
        average_blink_duration = sum(self.blink_durations) / len(self.blink_durations) if self.blink_durations else 0

        # Condition de fatigue basée sur la durée moyenne des clignements
        if average_blink_duration > self.fatigue_duration_threshold:
            self.fatigue_alert = True
        else:
            self.fatigue_alert = False

        # Vérification basée sur la fréquence des clignements
        if time.time() - self.last_check_time >= self.check_interval:
            if self.blinks_in_interval > self.blink_frequency_threshold:
                self.fatigue_alert = True
            self.blinks_in_interval = 0
            self.last_check_time = time.time()

        return self.fatigue_alert

    def get_blink_count(self):
        """
        Retourne le nombre total de clignements détectés.
        
        :return: int - Nombre de clignements.
        """
        return self.blink_count

    def calculate_average_blink_duration(self):
        """
        Calcule la durée moyenne des clignements.
        
        :return: float - Durée moyenne des clignements.
        """
        return sum(self.blink_durations) / len(self.blink_durations) if self.blink_durations else 0

    def reset(self):
        """
        Réinitialise les données de fatigue et de clignement pour un nouveau cycle de détection.
        """
        self.blink_count = 0
        self.blink_durations.clear()
        self.blinks_in_interval = 0
        self.last_check_time = time.time()
        self.last_blink_time = time.time()
        self.fatigue_alert = False
        print("Données de détection de fatigue réinitialisées")

    def display_fatigue_status(self):
        """
        Affiche un message indiquant l'état de fatigue.
        """
        if self.is_fatigued():
            print("Fatigue détectée - Faites une pause !")
        else:
            print("État de vigilance stable.")
