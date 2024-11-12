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
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
        
        eyes_detected = []
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (ex, ey, ew, eh) in eyes:
                eye_center = (x + ex + ew//2, y + ey + eh//2)
                eye_frame = frame[y+ey:y+ey+eh, x+ex:x+ex+ew]
                pupil_center = self.detect_pupil(eye_frame)
                if pupil_center is not None:
                    pupil_center = (pupil_center[0] + x + ex, pupil_center[1] + y + ey)
                    filtered_center = self.apply_kalman_filter(eye_center, pupil_center)
                    eyes_detected.append((eye_center, (ew, eh), filtered_center))
                cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)
        
        return frame, eyes_detected

    def detect_pupil(self, eye_frame):
        gray_eye = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un flou pour réduire le bruit
        blurred = cv2.GaussianBlur(gray_eye, (5, 5), 0)
        
        # Utiliser le seuillage adaptatif
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Trouver les contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return (cx, cy)
        
        return None

    def estimate_gaze(self, eye_center, eye_size, pupil_center):
        ex, ey = eye_center
        pw, ph = eye_size
        px, py = pupil_center
        
        gaze_x = (px - ex) / (pw/2)
        gaze_y = (py - ey) / (ph/2)
        
        screen_point = self.calibration.map_gaze_to_screen((gaze_x, gaze_y))
        return screen_point if screen_point is not None else (int(gaze_x * self.calibration.screen_width), int(gaze_y * self.calibration.screen_height))

    def apply_kalman_filter(self, eye_center, pupil_center):
        eye_id = eye_center
        if eye_id not in self.kalman_filters:
            self.kalman_filters[eye_id] = KalmanFilter(pupil_center)
        
        kf = self.kalman_filters[eye_id]
        kf.predict()
        filtered_center = kf.update(np.array(pupil_center))
        
        return tuple(filtered_center.astype(int))
