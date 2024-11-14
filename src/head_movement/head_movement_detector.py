import cv2
import numpy as np

class HeadMovementDetector:
    def __init__(self):
        self.previous_nose_position = None
        self.head_direction = "Neutre"
        self.smooth_factor = 0.9  # Plus la valeur est proche de 1, plus le mouvement est lissé
        self.prev_direction_vector = None

    def detect_head_movement(self, left_eye, right_eye, nose_point):
        if nose_point is None or left_eye is None or right_eye is None:
            return "Indéterminé"

        # Calcul des vecteurs pour l'orientation de la tête
        eye_vector = np.array(right_eye) - np.array(left_eye)
        nose_vector = np.array(nose_point) - (np.array(left_eye) + np.array(right_eye)) / 2

        # Normalisation pour la comparaison des vecteurs de direction
        eye_vector /= np.linalg.norm(eye_vector) if np.linalg.norm(eye_vector) != 0 else 1
        nose_vector /= np.linalg.norm(nose_vector) if np.linalg.norm(nose_vector) != 0 else 1

        # Appliquer le lissage pour éviter des changements brusques
        if self.prev_direction_vector is None:
            self.prev_direction_vector = nose_vector

        smooth_nose_vector = (
            self.smooth_factor * self.prev_direction_vector
            + (1 - self.smooth_factor) * nose_vector
        )
        self.prev_direction_vector = smooth_nose_vector

        # Détection des mouvements
        threshold_x, threshold_y = 0.3, 0.3
        direction = "Neutre"

        # Détecter les mouvements basés sur les vecteurs et les seuils
        if smooth_nose_vector[1] > threshold_y:
            direction = "Bas"
        elif smooth_nose_vector[1] < -threshold_y:
            direction = "Haut"
        elif smooth_nose_vector[0] > threshold_x:
            direction = "Droite"
        elif smooth_nose_vector[0] < -threshold_x:
            direction = "Gauche"

        self.head_direction = direction
        return direction
