import cv2
import numpy as np

class HeatmapGenerator:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.fixation_points = []

    def add_fixation_point(self, point):
        if 0 <= point[0] < self.screen_width and 0 <= point[1] < self.screen_height:
            self.fixation_points.append(point)

    def generate_heatmap(self):
        heatmap = np.zeros((self.screen_height, self.screen_width), dtype=np.float32)
        
        # Ajouter de la densité autour de chaque point de fixation
        for point in self.fixation_points:
            # Convertir les coordonnées du point en entiers pour éviter les erreurs
            int_point = (int(point[0]), int(point[1]))
            cv2.circle(heatmap, int_point, radius=30, color=1, thickness=-1)

        heatmap = cv2.GaussianBlur(heatmap, (101, 101), 0)
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = np.uint8(heatmap)
        
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        return heatmap_color

    def display_visual_field(self, frame):
        heatmap = self.generate_heatmap()
        overlay = cv2.addWeighted(frame, 0.6, heatmap, 0.4, 0)
        return overlay
