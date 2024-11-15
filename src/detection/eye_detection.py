import cv2
import numpy as np
import mediapipe as mp

class AdvancedEyeDetector:
    def __init__(self, movement_threshold=5.0, face_size_threshold=200, zoom_factor=1.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True, min_detection_confidence=0.5)
        self.frames_without_eyes = 0

    def detect_eyes(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        eyes_detected = []
        avg_ear = 0
        eyes_hidden = False
        nose_point = None

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_points, right_eye_points = self.get_eye_landmarks(face_landmarks, frame.shape)
                
                if left_eye_points and right_eye_points:
                    left_ear = self.calculate_eye_aspect_ratio(left_eye_points)
                    right_ear = self.calculate_eye_aspect_ratio(right_eye_points)
                    avg_ear = (left_ear + right_ear) / 2.0

                    left_center = self.get_eye_center(left_eye_points)
                    right_center = self.get_eye_center(right_eye_points)
                    eyes_detected.append({'left_eye': left_center, 'right_eye': right_center})

                    self.draw_eye_shape(frame, left_eye_points)
                    self.draw_eye_shape(frame, right_eye_points)

                    self.frames_without_eyes = 0
                else:
                    self.frames_without_eyes += 1
                    if self.frames_without_eyes > 10:
                        eyes_hidden = True
                        avg_ear = 0

                nose_index = 1
                nose_landmark = face_landmarks.landmark[nose_index]
                nose_point = (int(nose_landmark.x * frame.shape[1]), int(nose_landmark.y * frame.shape[0]))

        return frame, eyes_detected, avg_ear, eyes_hidden, nose_point

    def get_eye_landmarks(self, face_landmarks, frame_shape):
        left_eye_indices = [362, 385, 387, 263, 373, 380]
        right_eye_indices = [33, 160, 158, 133, 153, 144]
        
        left_eye_points = [(int(face_landmarks.landmark[i].x * frame_shape[1]), int(face_landmarks.landmark[i].y * frame_shape[0])) for i in left_eye_indices]
        right_eye_points = [(int(face_landmarks.landmark[i].x * frame_shape[1]), int(face_landmarks.landmark[i].y * frame_shape[0])) for i in right_eye_indices]
        return left_eye_points, right_eye_points

    def calculate_eye_aspect_ratio(self, eye_points):
        if len(eye_points) < 6:
            return 0
        A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
        B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
        C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
        ear = (A + B) / (2.0 * C)
        return ear

    def get_eye_center(self, eye_points):
        x_center = sum([p[0] for p in eye_points]) // len(eye_points)
        y_center = sum([p[1] for p in eye_points]) // len(eye_points)
        return (x_center, y_center)

    def draw_eye_shape(self, frame, eye_points):
        cv2.polylines(frame, [np.array(eye_points, np.int32)], isClosed=True, color=(0, 255, 0), thickness=1)
