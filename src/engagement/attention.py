import time

class AttentionCalculator:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.engagement_score = 0
        self.start_time = time.time()
        self.total_duration_looking_away = 0

    def calculate_attention(self, fixation_point):
        """
        Calcule l'attention en fonction de la position de fixation de l'utilisateur.
        fixation_point : (x, y) coordonnées de la fixation
        """
        # Détermine si l'utilisateur regarde l'écran ou non
        if self.is_looking_away(fixation_point):
            self.total_duration_looking_away += time.time() - self.start_time
            self.engagement_score -= 1  # Réduit le score d'engagement
        else:
            self.engagement_score += 1  # Augmente le score d'engagement

        # Réinitialiser le chronomètre pour la prochaine analyse
        self.start_time = time.time()

    def is_looking_away(self, fixation_point):
        """
        Vérifie si le point de fixation est hors des limites de l'écran
        """
        x, y = fixation_point
        # Si le point de fixation est hors de l'écran, l'utilisateur regarde ailleurs
        if x < 0 or x > self.screen_width or y < 0 or y > self.screen_height:
            return True
        return False

    def get_engagement_score(self):
        return max(0, self.engagement_score) 

    def reset_engagement_score(self):
        self.engagement_score = 0
        self.total_duration_looking_away = 0
