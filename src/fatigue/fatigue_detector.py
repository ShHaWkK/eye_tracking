import time

class FatigueDetector:
    def __init__(self, blink_threshold=0.25, fatigue_duration_threshold=0.25, blink_frequency_threshold=10, check_interval=60, min_blink_duration=0.1):
        """
        Initialise le détecteur de fatigue avec des seuils personnalisables.
        
        - blink_threshold : seuil pour détecter un œil fermé.
        - fatigue_duration_threshold : durée moyenne des clignements au-delà de laquelle la fatigue est suspectée.
        - blink_frequency_threshold : nombre de clignements par intervalle de vérification au-delà duquel la fatigue est suspectée.
        - check_interval : intervalle de temps (en secondes) pour réévaluer la fatigue.
        - min_blink_duration : durée minimale d'un clignement pour être valide.
        """
        
        # Seuils pour la détection
        self.blink_threshold = blink_threshold
        self.fatigue_duration_threshold = fatigue_duration_threshold
        self.blink_frequency_threshold = blink_frequency_threshold
        self.check_interval = check_interval
        self.min_blink_duration = min_blink_duration

        # Variables de suivi des clignements
        self.blink_count = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.blink_durations = []  # Stocke la durée de chaque clignement
        self.last_check_time = time.time()
        self.blinks_in_interval = 0

    def detect_blink(self, eye_aspect_ratio):
        """
        Détecte un clignement en fonction du ratio d'aspect de l'œil (EAR) et de la durée minimum.
        
        Retourne : bool indiquant si un clignement a été détecté.
        """
        # Détection d'un œil fermé
        if eye_aspect_ratio < self.blink_threshold:
            if not self.is_blinking:  # Début d'un clignement
                self.is_blinking = True
                self.blink_start_time = time.time()
        else:
            if self.is_blinking:  # Fin d'un clignement
                blink_duration = time.time() - self.blink_start_time
                if blink_duration >= self.min_blink_duration:
                    # Clignement valide
                    self.blink_count += 1
                    self.blink_durations.append(blink_duration)  # Ajouter la durée à la liste
                    self.blinks_in_interval += 1
                    print(f"Clignement détecté - Durée: {blink_duration:.3f}s")  # Debug
                self.is_blinking = False  # Réinitialiser l'état de clignement

    def calculate_average_blink_duration(self):
        """
        Calcule la durée moyenne des clignements à partir de la liste des durées enregistrées.
        """
        if len(self.blink_durations) == 0:
            return 0
        return sum(self.blink_durations) / len(self.blink_durations)

    def is_fatigued(self):
        """
        Évalue la fatigue basée sur la durée moyenne des clignements et la fréquence des clignements.
        
        Retourne : bool indiquant si l'utilisateur est considéré comme fatigué.
        """
        # Condition 1 : Vérifier la durée moyenne des clignements
        average_blink_duration = self.calculate_average_blink_duration()
        if average_blink_duration > self.fatigue_duration_threshold:
            print("Fatigue détectée en raison de la durée moyenne des clignements élevée")  # Debug
            return True

        # Condition 2 : Vérifier la fréquence des clignements dans l'intervalle de temps
        current_time = time.time()
        if current_time - self.last_check_time >= self.check_interval:
            if self.blinks_in_interval > self.blink_frequency_threshold:
                print("Fatigue détectée en raison de la fréquence élevée des clignements")  # Debug
                # Réinitialiser les compteurs
                self.blinks_in_interval = 0
                self.last_check_time = current_time
                return True
            else:
                # Réinitialiser les compteurs sans fatigue détectée
                self.blinks_in_interval = 0
                self.last_check_time = current_time

        return False

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
        print("Données de détection de fatigue réinitialisées")  # Debug
