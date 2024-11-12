from src.acquisition.camera_capture import CameraCapture
import cv2

def main():
    capture = CameraCapture()
    try:
        while True:
            frame = capture.get_frame()
            # Ici,  le traitement pour la détection des yeux et l'estimation du regard
            cv2.imshow('Eye Tracking', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
