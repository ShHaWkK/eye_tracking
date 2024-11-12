import cv2
import numpy as np
import dlib
from sklearn.cluster import KMeans
from src.tracking.kalman_filter import KalmanFilter

class EyeDetector:
    def __init__(self, calibration):
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_predictor = dlib.shape_predictor("C:/Dossier_GitHub/eye_tracking/src/dat/shape_predictor_68_face_landmarks.dat")
        self.calibration = calibration
        self.kalman_filters = {}
    def detect_eyes(self, gray_frame):
        # Vérifiez si gray_frame est bien une image en niveaux de gris
        if len(gray_frame.shape) != 2:
            print("Erreur : l'image fournie n'est pas en niveaux de gris.")
            return gray_frame, []

        faces = self.face_detector(gray_frame)
        
        eyes_detected = []
        for face in faces:
            landmarks = self.landmark_predictor(gray_frame, face)
            
            left_eye = self.get_eye_coordinates(landmarks, 36, 41)
            right_eye = self.get_eye_coordinates(landmarks, 42, 47)
            
            for eye in [left_eye, right_eye]:
                eye_center = eye['center']
                eye_frame = gray_frame[eye['top']:eye['bottom'], eye['left']:eye['right']]
                pupil_center = self.detect_pupil(eye_frame)
                if pupil_center is not None:
                    pupil_center = (pupil_center[0] + eye['left'], pupil_center[1] + eye['top'])
                    filtered_center = self.apply_kalman_filter(eye_center, pupil_center)
                    eyes_detected.append((eye_center, (eye['width'], eye['height']), filtered_center))
                cv2.rectangle(gray_frame, (eye['left'], eye['top']), (eye['right'], eye['bottom']), (0, 255, 0), 2)
        
        return gray_frame, eyes_detected

    def get_eye_coordinates(self, landmarks, start, end):
        points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(start, end+1)]
        left = min(points, key=lambda p: p[0])[0]
        right = max(points, key=lambda p: p[0])[0]
        top = min(points, key=lambda p: p[1])[1]
        bottom = max(points, key=lambda p: p[1])[1]
        width = right - left
        height = bottom - top
        center = (left + width//2, top + height//2)
        return {'left': left, 'right': right, 'top': top, 'bottom': bottom, 'width': width, 'height': height, 'center': center}

    def detect_pupil(self, eye_frame):
        gray_eye = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un filtre de Gabor pour améliorer les bords de l'iris
        kernel = cv2.getGaborKernel((21, 21), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        filtered = cv2.filter2D(gray_eye, cv2.CV_8UC3, kernel)
        
        # Appliquer un seuillage adaptatif
        _, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Appliquer une transformation de distance
        dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
        
        # Utiliser K-means pour trouver le centre de la pupille
        coords = np.column_stack(np.where(sure_fg > 0))
        if len(coords) > 0:
            kmeans = KMeans(n_clusters=1, random_state=0).fit(coords)
            center = kmeans.cluster_centers_[0]
            return (int(center[1]), int(center[0]))  # Inverser x et y pour correspondre au format OpenCV
        
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
