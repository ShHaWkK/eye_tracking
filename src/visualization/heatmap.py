import cv2
import numpy as np

class HeatmapGenerator:
    def __init__(self, screen_size, point_radius=30, intensity=1, blur_kernel_size=(101, 101)):
        """
        Initializes the HeatmapGenerator class.

        :param screen_size: Tuple representing the screen size (width, height).
        :param point_radius: Radius of the fixation points for the heatmap.
        :param intensity: Intensity of each fixation point.
        :param blur_kernel_size: Kernel size for Gaussian blur applied to smooth the heatmap.
        """
        self.screen_width, self.screen_height = screen_size
        self.fixation_points = []
        self.point_radius = point_radius
        self.intensity = intensity
        self.blur_kernel_size = blur_kernel_size

    def add_fixation_point(self, point):
        """
        Adds a fixation point to the list of points for the heatmap.

        :param point: Tuple (x, y) representing the fixation point.
        """
        if 0 <= point[0] < self.screen_width and 0 <= point[1] < self.screen_height:
            self.fixation_points.append(point)

    def generate_heatmap(self):
        """
        Generates a heatmap based on accumulated fixation points.

        :return: Colored heatmap applied to an image with the JET colormap.
        """
        # Create a blank image for the heatmap
        heatmap = np.zeros((self.screen_height, self.screen_width), dtype=np.float32)

        # Add density around each fixation point
        for point in self.fixation_points:
            int_point = (int(point[0]), int(point[1]))
            cv2.circle(heatmap, int_point, self.point_radius, color=self.intensity, thickness=-1)

        # Apply Gaussian blur to smooth the heatmap
        heatmap = cv2.GaussianBlur(heatmap, self.blur_kernel_size, 0)

        # Normalize the heatmap for better representation
        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = np.uint8(heatmap)

        # Apply the JET colormap to obtain a colored heatmap
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        return heatmap_color

    def overlay_heatmap(self, frame):
        """
        Overlays the generated heatmap on the video frame.

        :param frame: Image on which to overlay the heatmap.
        :return: Image with the heatmap overlay.
        """
        # Generate the heatmap
        heatmap = self.generate_heatmap()

        # Resize the heatmap to match the frame size
        heatmap_resized = cv2.resize(heatmap, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_LINEAR)

        # Overlay the heatmap with transparency onto the frame
        overlay = cv2.addWeighted(frame, 0.6, heatmap_resized, 0.4, 0)
        
        return overlay
