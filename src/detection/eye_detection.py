import cv2
import numpy as np
from sklearn.cluster import KMeans
from src.tracking.kalman_filter import KalmanFilter

class EyeDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.kalman_filters = {}
        self.glasses_user = False

    def set_glasses_user(self, glasses):
        self.glasses_user = glasses

    def detect_eyes(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.glasses_user:
            gray_frame = self.reduce_reflection(gray_frame)

        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
        eyes_detected = []
        for (x, y, w, h) in faces:
            roi_gray = gray_frame[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            for (ex, ey, ew, eh) in eyes:
                eye_center = (int(ex + ew/2), int(ey + eh/2))
                eye_frame = roi_gray[ey:ey+eh, ex:ex+ew]

                pupil_center = self.detect_pupil(eye_frame)
                if pupil_center is not None:
                    pupil_center = (pupil_center[0] + ex, pupil_center[1] + ey)
                    filtered_center = self.apply_kalman_filter(eye_center, pupil_center)
                    eyes_detected.append((eye_center, filtered_center))
                
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        return frame, eyes_detected

    def reduce_reflection(self, frame):
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        _, frame = cv2.threshold(frame, 220, 255, cv2.THRESH_TRUNC)
        return frame

    def detect_pupil(self, eye_frame):
        _, thresh = cv2.threshold(eye_frame, 50 if self.glasses_user else 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        coords = np.column_stack(np.where(sure_fg > 0))
        if len(coords) > 0:
            kmeans = KMeans(n_clusters=1, random_state=0).fit(coords)
            center = kmeans.cluster_centers_[0]
            return int(center[1]), int(center[0])

        return None

    def apply_kalman_filter(self, eye_center, pupil_center):
        eye_id = eye_center
        if eye_id not in self.kalman_filters:
            self.kalman_filters[eye_id] = KalmanFilter(pupil_center)
        
        kf = self.kalman_filters[eye_id]
        kf.predict()
        filtered_center = kf.update(np.array(pupil_center))
        
        return tuple(filtered_center.astype(int))

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
