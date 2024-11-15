import cv2
import numpy as np

class HeatmapGenerator:
    def __init__(self, screen_size, point_radius=30, intensity=1, blur_kernel_size=(101, 101)):
        """
        Initialise la classe HeatmapGenerator.

        :param screen_size: Tuple de la taille de l'écran (width, height).
        :param point_radius: Rayon des points de fixation pour la heatmap.
        :param intensity: Intensité de chaque point de fixation.
        :param blur_kernel_size: Taille du noyau pour le flou gaussien appliqué.
        """
        self.screen_width, self.screen_height = screen_size
        self.fixation_points = []
        self.point_radius = point_radius
        self.intensity = intensity
        self.blur_kernel_size = blur_kernel_size

    def add_fixation_point(self, point):
        """
        Ajoute un point de fixation à la liste des points pour la heatmap.

        :param point: Tuple (x, y) représentant le point de fixation.
        """
        if 0 <= point[0] < self.screen_width and 0 <= point[1] < self.screen_height:
            self.fixation_points.append(point)

    def generate_heatmap(self):
        """
        Génère une heatmap en fonction des points de fixation accumulés.

        :return: Heatmap en couleur appliquée sur une image avec le colormap JET.
        """
        # Création d'une image vierge pour la heatmap
        heatmap = np.zeros((self.screen_height, self.screen_width), dtype=np.float32)

        # Ajout de densité autour de chaque point de fixation
        for point in self.fixation_points:
            int_point = (int(point[0]), int(point[1]))
            cv2.circle(heatmap, int_point, self.point_radius, color=self.intensity, thickness=-1)

        # Application d'un flou gaussien pour lisser la heatmap
        heatmap = cv2.GaussianBlur(heatmap, self.blur_kernel_size, 0)

        # Normalisation de la heatmap pour une meilleure représentation
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = np.uint8(heatmap)

        # Application du colormap JET pour obtenir une heatmap colorée
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        return heatmap_color

    def overlay_heatmap(self, frame):
        """
        Superpose la heatmap générée sur le cadre de la vidéo.

        :param frame: Image sur laquelle superposer la heatmap.
        :return: Image avec la heatmap superposée.
        """
        heatmap = self.generate_heatmap()

        # Redimensionne la heatmap pour correspondre à la taille du cadre
        heatmap_resized = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_LINEAR)

        # Superpose la heatmap avec transparence sur le cadre
        overlay = cv2.addWeighted(frame, 0.6, heatmap_resized, 0.4, 0)
        
        return overlay
