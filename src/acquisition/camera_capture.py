import cv2
import yaml

class CameraCapture:
    def __init__(self, config_path='config/camera_config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.camera = cv2.VideoCapture(self.config['camera_index'])
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['width'])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['height'])

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        return frame

    def release(self):
        self.camera.release()

if __name__ == "__main__":
    capture = CameraCapture()
    try:
        while True:
            frame = capture.get_frame()
            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()
