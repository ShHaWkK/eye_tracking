from src.acquisition.camera_capture import CameraCapture
from src.detection.eye_detection import EyeDetector
import cv2

def main():
    capture = CameraCapture()
    eye_detector = EyeDetector()
    
    try:
        while True:
            frame = capture.get_frame()
            frame_with_eyes = eye_detector.detect_eyes(frame)
            cv2.imshow('Eye Tracking', frame_with_eyes)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
