import cv2
from src.detection.eye_detection import EyeDetector
from src.calibration.calibration import Calibration
from src.visualization.heatmap import HeatmapGenerator

def main():
    screen_size = (640, 480)
    calibration = Calibration(screen_size)
    eye_detector = EyeDetector()
    heatmap_generator = HeatmapGenerator(screen_size)

    # Interface simple pour sélectionner l’option lunettes
    glasses_user = input("Est-ce que vous portez des lunettes ? (oui/non) : ").strip().lower() == "oui"
    eye_detector.set_glasses_user(glasses_user)

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Erreur : Impossible de capturer le cadre.")
            break

        # Détection des yeux et récupération des points
        frame_with_eyes, eyes_detected = eye_detector.detect_eyes(frame)

        # Ajouter des points de fixation pour générer la carte de chaleur
        for _, filtered_center in eyes_detected:
            heatmap_generator.add_fixation_point(filtered_center)

        # Générer et afficher la carte de chaleur
        heatmap = heatmap_generator.generate_heatmap()
        overlay = cv2.addWeighted(frame_with_eyes, 0.6, heatmap, 0.4, 0)
        cv2.imshow('Eye Detection with Heatmap', overlay)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
