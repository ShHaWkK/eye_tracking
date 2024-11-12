import cv2
import numpy as np
from src.acquisition.camera_capture import CameraCapture
from src.detection.eye_detection import EyeDetector
from src.calibration.calibration import Calibration

def main():
    capture = CameraCapture()
    screen_size = (1920, 1080)  # Ajustez selon votre écran
    calibration = Calibration(screen_size)
    eye_detector = EyeDetector(calibration)
    
    # Étape de calibration
    while True:
        frame = capture.get_frame()
        frame_with_eyes, eyes_detected = eye_detector.detect_eyes(frame)
        
        calibration_point = calibration.get_next_calibration_point()
        if calibration_point is None:
            break  # Calibration terminée
        
        frame = calibration.draw_calibration_point(frame, calibration_point)
        cv2.imshow('Calibration', frame)
        
        if len(eyes_detected) > 0:
            eye_center, eye_size, filtered_pupil_center = eyes_detected[0]
            gaze_point = eye_detector.estimate_gaze(eye_center, eye_size, filtered_pupil_center)
            calibration.add_calibration_data(gaze_point)
        
        if cv2.waitKey(1000) & 0xFF == ord('q'):  # Attendre 1 seconde ou appuyer sur 'q' pour passer au point suivant
            break
    
    calibration.compute_mapping()
    cv2.destroyAllWindows()
    
    # Suivi du regard après calibration
    try:
        while True:
            frame = capture.get_frame()
            frame_with_eyes, eyes_detected = eye_detector.detect_eyes(frame)
            
            for eye_center, eye_size, filtered_pupil_center in eyes_detected:
                screen_point = eye_detector.estimate_gaze(eye_center, eye_size, filtered_pupil_center)
                
                # Dessiner le point de regard sur l'écran
                cv2.circle(frame_with_eyes, screen_point, 5, (0, 0, 255), -1)
            
            cv2.imshow('Eye Tracking', frame_with_eyes)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
