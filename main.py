import cv2
import time
from src.detection.eye_detection import EyeDetector
from src.calibration.calibration import Calibration
from src.engagement.attention import AttentionCalculator
from src.fatigue.fatigue_detector import FatigueDetector

def main():
    screen_size = (640, 480)
    calibration = Calibration(screen_size)
    eye_detector = EyeDetector()
    attention_calculator = AttentionCalculator(screen_size)
    fatigue_detector = FatigueDetector()

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Erreur : Impossible de capturer le cadre.")
            break

        frame_with_eyes, eyes_detected = eye_detector.detect_eyes(frame)

        # Analyse de l'engagement et de la fatigue en fonction des yeux détectés
        for eye_center, filtered_center in eyes_detected:
            attention_calculator.calculate_attention(filtered_center)

            # Calcule de la fatigue en fonction de l’aspect de l’œil
            eye_aspect_ratio = eye_detector.calculate_eye_aspect_ratio(eye_center)
            fatigue_detector.detect_blink(eye_aspect_ratio)

        # Affichage des scores de fatigue et d’engagement
        engagement_score = attention_calculator.get_engagement_score()
        fatigue_status = "Fatigué" if fatigue_detector.is_fatigued() else "Non fatigué"
        blink_count = fatigue_detector.get_blink_count()

        cv2.putText(frame_with_eyes, f'Engagement Score: {engagement_score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame_with_eyes, f'Fatigue Status: {fatigue_status}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame_with_eyes, f'Blinks: {blink_count}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow('Eye Detection with Engagement and Fatigue Monitoring', frame_with_eyes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
