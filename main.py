import cv2
import numpy as np

class EyeDetector:
    def __init__(self):
        # Charger les classificateurs en cascade pour les visages et les yeux
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def detect_eyes(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

        eyes_detected = []
        for (x, y, w, h) in faces:
            roi_gray = gray_frame[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                eyes_detected.append((ex + x, ey + y, ew, eh))  # Ajout des coordonnées des yeux

        return frame, eyes_detected

def main():
    capture = cv2.VideoCapture(0)  # Ouvrir la caméra
    eye_detector = EyeDetector()

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Erreur : Impossible de capturer le cadre.")
            break

        frame_with_eyes, eyes_detected = eye_detector.detect_eyes(frame)  # Passer l'image à la détection des yeux

        cv2.imshow('Eye Detection', frame_with_eyes)  # Afficher le cadre avec les yeux détectés

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quitter avec 'q'
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
