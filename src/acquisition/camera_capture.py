import cv2

class CameraCapture:
    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise ValueError("Impossible d'ouvrir la caméra")

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Impossible de capturer une image")
        return frame

    def release(self):
        self.camera.release()
