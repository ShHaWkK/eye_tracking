import cv2
import numpy as np
import mediapipe as mp

class AdvancedEyeDetector:
    def __init__(self, movement_threshold=5.0, face_size_threshold=200, zoom_factor=1.5):
        # Initialisation de Mediapipe pour la détection des landmarks faciaux
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)
        self.movement_threshold = movement_threshold
        self.face_size_threshold = face_size_threshold
        self.zoom_factor = zoom_factor
        self.frames_without_eyes = 0  # Compteur pour les frames sans détection d'yeux

    def detect_eyes(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        eyes_detected = []
        avg_ear = 0
        eyes_hidden = False  # Indicateur pour les yeux cachés

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_points, right_eye_points = self.get_eye_landmarks(face_landmarks, frame.shape)
                
                # Vérifier si les yeux sont visibles
                if left_eye_points and right_eye_points:
                    left_ear = self.calculate_eye_aspect_ratio(left_eye_points)
                    right_ear = self.calculate_eye_aspect_ratio(right_eye_points)
                    avg_ear = (left_ear + right_ear) / 2.0

                    left_center = self.get_eye_center(left_eye_points)
                    right_center = self.get_eye_center(right_eye_points)
                    eyes_detected.append((left_center, right_center))

                    # Dessiner la forme des yeux pour visualiser les landmarks
                    self.draw_eye_shape(frame, left_eye_points)
                    self.draw_eye_shape(frame, right_eye_points)
                    
                    # Les yeux sont détectés, réinitialiser le compteur
                    self.frames_without_eyes = 0
                else:
                    # Si les yeux ne sont pas détectés, incrémenter le compteur
                    self.frames_without_eyes += 1

                    # Considérer les yeux comme cachés après 10 frames sans détection
                    if self.frames_without_eyes > 10:
                        eyes_hidden = True
                        avg_ear = 0  # Remettre l'EAR à 0 si les yeux sont cachés

        return frame, eyes_detected, avg_ear, eyes_hidden

    # Les autres méthodes restent inchangées
    def get_eye_landmarks(self, landmarks, frame_shape):
        """Récupère les points de repère pour les yeux gauche et droit dans le cadre principal."""
        left_eye_indices = [362, 385, 387, 263, 373, 380]
        right_eye_indices = [33, 160, 158, 133, 153, 144]
        
        left_eye_points = [(int(landmarks.landmark[i].x * frame_shape[1]), int(landmarks.landmark[i].y * frame_shape[0])) for i in left_eye_indices]
        right_eye_points = [(int(landmarks.landmark[i].x * frame_shape[1]), int(landmarks.landmark[i].y * frame_shape[0])) for i in right_eye_indices]
        return left_eye_points, right_eye_points

    def calculate_eye_aspect_ratio(self, eye_points):
        """Calcule le ratio d'aspect de l'œil pour détecter s'il est ouvert ou fermé."""
        if len(eye_points) < 6:
            return 0
        A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
        B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
        C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
        ear = (A + B) / (2.0 * C)
        return ear

    def get_eye_center(self, eye_points):
        """Calcule le centre de l'œil pour un suivi précis."""
        x_center = sum([p[0] for p in eye_points]) // len(eye_points)
        y_center = sum([p[1] for p in eye_points]) // len(eye_points)
        return (x_center, y_center)

    def draw_eye_shape(self, frame, eye_points):
        """Dessine les contours de l'œil en fonction des landmarks."""
        cv2.polylines(frame, [np.array(eye_points, np.int32)], isClosed=True, color=(0, 255, 0), thickness=1)
