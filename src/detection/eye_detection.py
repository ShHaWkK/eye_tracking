import cv2
import numpy as np
from src.tracking.kalman_filter import KalmanFilter

class EyeDetector:
    def __init__(self, calibration):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.kalman_filters = {}
        self.calibration = calibration

    def detect_eyes(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        eyes_detected = []
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (ex, ey, ew, eh) in eyes:
                eye_center = (x + ex + ew//2, y + ey + eh//2)
                eye_frame = roi_color[ey:ey+eh, ex:ex+ew]
                pupil_center = self.detect_pupil(eye_frame)
                if pupil_center is not None and len(pupil_center) == 2:
                    pupil_center = (pupil_center[0] + x + ex, pupil_center[1] + y + ey)
                    filtered_center = self.apply_kalman_filter(eye_center, pupil_center)
                    eyes_detected.append((eye_center, (ew, eh), filtered_center))

                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        return frame, eyes_detected

    def detect_pupil(self, eye_frame):
        gray_eye = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un flou pour réduire le bruit
        blurred = cv2.GaussianBlur(gray_eye, (7, 7), 0)
        
        # Utiliser la détection de cercles de Hough pour trouver la pupille
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                   param1=50, param2=30, minRadius=5, maxRadius=30)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                return (i[0], i[1])  # Retourner le centre du premier cercle détecté
        
        return None

    def estimate_gaze(self, eye_center, eye_size, pupil_center):
        ex, ey = eye_center
        pw, ph = eye_size
        px, py = pupil_center
        
        # Calculer le déplacement de la pupille par rapport au centre de l'œil
        gaze_x = (px - ex) / (pw/2)  # Normaliser entre -1 et 1
        gaze_y = (py - ey) / (ph/2)  # Normaliser entre -1 et 1
        
        # Appliquer la calibration
        screen_point = self.calibration.map_gaze_to_screen((gaze_x, gaze_y))
        return screen_point if screen_point is not None else (gaze_x, gaze_y)

    def apply_kalman_filter(self, eye_center, pupil_center):
        eye_id = eye_center  # Utiliser le centre de l'œil comme identifiant unique
        if eye_id not in self.kalman_filters:
            self.kalman_filters[eye_id] = KalmanFilter(pupil_center)
        
        kf = self.kalman_filters[eye_id]
        kf.predict()
        filtered_center = kf.update(np.array(pupil_center))
        
        return tuple(filtered_center.astype(int))
