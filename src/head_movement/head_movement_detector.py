import numpy as np

class HeadMovementDetector:
    def __init__(self):
        self.previous_nose_position = None
        self.movement = "Neutre"
        self.smooth_factor = 0.8
        self.prev_direction_vector = None

    def detect_head_movement(self, nose_point, left_eye, right_eye):
        if nose_point is None or left_eye is None or right_eye is None:
            return "Indéterminé"

        # Calculer le vecteur entre les yeux (base horizontale)
        eye_vector = np.array(right_eye) - np.array(left_eye)
        nose_vector = np.array(nose_point) - (np.array(left_eye) + np.array(right_eye)) / 2

        # Normalisation pour éviter les variations dues à la taille du cadre
        eye_vector /= np.linalg.norm(eye_vector) if np.linalg.norm(eye_vector) != 0 else 1
        nose_vector /= np.linalg.norm(nose_vector) if np.linalg.norm(nose_vector) != 0 else 1

        # Lissage des mouvements
        if self.prev_direction_vector is None:
            self.prev_direction_vector = nose_vector

        smooth_nose_vector = (
            self.smooth_factor * self.prev_direction_vector
            + (1 - self.smooth_factor) * nose_vector
        )
        self.prev_direction_vector = smooth_nose_vector

        # Détection basée sur des seuils
        threshold_x, threshold_y = 0.4, 0.4
        if smooth_nose_vector[1] > threshold_y:
            return "Bas"
        elif smooth_nose_vector[1] < -threshold_y:
            return "Haut"
        elif smooth_nose_vector[0] > threshold_x:
            return "Droite"
        elif smooth_nose_vector[0] < -threshold_x:
            return "Gauche"
        else:
            return "Neutre"
