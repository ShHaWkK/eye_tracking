import cv2
import numpy as np
import mediapipe as mp

class EyeDetector:
    def __init__(self):
        # Initialisation de Mediapipe pour la détection des visages et des landmarks
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)

    def detect_eyes(self, frame):
        # Conversion en RGB car Mediapipe utilise l'espace colorimétrique RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        eyes_detected = []
        avg_ear = 0

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Obtenez les points de repère pour les deux yeux (indices selon Mediapipe)
                left_eye_points = [
                    (int(face_landmarks.landmark[i].x * frame.shape[1]), int(face_landmarks.landmark[i].y * frame.shape[0]))
                    for i in [362, 385, 387, 263, 373, 380]
                ]
                right_eye_points = [
                    (int(face_landmarks.landmark[i].x * frame.shape[1]), int(face_landmarks.landmark[i].y * frame.shape[0]))
                    for i in [33, 160, 158, 133, 153, 144]
                ]

                # Calculer le ratio d'aspect pour chaque œil
                left_ear = self.calculate_eye_aspect_ratio(left_eye_points)
                right_ear = self.calculate_eye_aspect_ratio(right_eye_points)
                avg_ear = (left_ear + right_ear) / 2.0

                # Ajouter les centres des yeux pour la détection de l’attention
                left_center = (left_eye_points[0][0] + left_eye_points[3][0]) // 2, (left_eye_points[1][1] + left_eye_points[4][1]) // 2
                right_center = (right_eye_points[0][0] + right_eye_points[3][0]) // 2, (right_eye_points[1][1] + right_eye_points[4][1]) // 2
                eyes_detected.append((left_center, right_center))

                # Afficher les contours des yeux pour la visualisation
                for pt in left_eye_points + right_eye_points:
                    cv2.circle(frame, pt, 2, (0, 255, 0), -1)

        return frame, eyes_detected, avg_ear

    def calculate_eye_aspect_ratio(self, eye_points):
        """
        Calcul du ratio d'aspect de l'œil pour détecter s'il est ouvert ou fermé.
        eye_points : Liste des points (x, y) de l'œil
        """
        if len(eye_points) < 6:
            return 0  # Retourne 0 si nous n'avons pas assez de points

        # Calcul des distances verticales entre les points de l'œil
        A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
        B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
        
        # Distance horizontale entre les points de l'œil
        C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))

        # Calcul du ratio d'aspect de l'œil
        ear = (A + B) / (2.0 * C)
        return ear
