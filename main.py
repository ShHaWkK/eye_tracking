import cv2
import time
from src.detection.eye_detection import AdvancedEyeDetector
from src.engagement.attention import AttentionCalculator
from src.fatigue.fatigue_detector import FatigueDetector

def main():
    screen_size = (640, 480)
    eye_detector = AdvancedEyeDetector()
    attention_calculator = AttentionCalculator(screen_size)
    fatigue_detector = FatigueDetector()
    
    engagement_score = 100  # Valeur initiale du score d'engagement
    blink_count = 0  # Compteur de clignements pour l'augmentation du score
    display_points_animation = False  # Indicateur pour l'animation "+50pts"
    animation_start_time = 0  # Temps de démarrage de l'animation

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Erreur : Impossible de capturer le cadre.")
            break

        # Détecter les yeux et obtenir les informations
        frame_with_eyes, eyes_detected, avg_ear, eyes_hidden = eye_detector.detect_eyes(frame)

        # Si les yeux sont détectés et qu'un clignement est identifié
        if not eyes_hidden and avg_ear:
            blink_detected = fatigue_detector.detect_blink(avg_ear)
            
            if blink_detected:
                blink_count += 1  # Incrémenter le compteur de clignements
                print(f"Clignements détectés : {blink_count}")  # Pour le suivi du compteur en temps réel

                if blink_count >= 10:
                    engagement_score += 50  # Ajouter 50 points au score d'engagement
                    blink_count = 0  # Réinitialiser le compteur après 10 clignements
                    print("Augmentation du score d'engagement de 50 points.")  # Debug

                    # Activer l'animation "+50pts"
                    display_points_animation = True
                    animation_start_time = time.time()

            # Calcul de l'attention basé sur la détection des yeux
            for left_center, right_center in eyes_detected:
                attention_calculator.calculate_attention(left_center)

        # Affichage de l'animation "+50pts" lorsque le score augmente
        if display_points_animation:
            elapsed_time = time.time() - animation_start_time
            if elapsed_time < 1:  # Afficher "+50pts" pendant 1 seconde
                cv2.putText(frame_with_eyes, "+50pts", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            else:
                display_points_animation = False  # Désactiver l'animation après 1 seconde

        # Afficher les scores d'engagement et de fatigue
        fatigue_status = "Fatigué" if fatigue_detector.is_fatigued() else "Non fatigué"
        total_blinks = fatigue_detector.get_blink_count()

        cv2.putText(frame_with_eyes, f'Engagement Score: {engagement_score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame_with_eyes, f'Fatigue Status: {fatigue_status}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame_with_eyes, f'Blinks: {total_blinks}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Afficher la vidéo avec l'animation et les scores
        cv2.imshow('Eye Detection with Engagement and Fatigue Monitoring', frame_with_eyes)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
