import numpy as np
from scipy.interpolate import griddata
import json

class Calibration:
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.calibration_points = [
            (0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
            (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
            (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)
        ]
        self.collected_data = []
        self.mapping_function = None

    def get_next_calibration_point(self):
        if len(self.collected_data) < len(self.calibration_points):
            return self.calibration_points[len(self.collected_data)]
        return None

    def add_calibration_data(self, gaze_point):
        if len(self.collected_data) < len(self.calibration_points):
            screen_point = self.calibration_points[len(self.collected_data)]
            self.collected_data.append((gaze_point, screen_point))

    def compute_mapping(self):
        if len(self.collected_data) == len(self.calibration_points):
            gaze_points = np.array([d[0] for d in self.collected_data])
            screen_points = np.array([d[1] for d in self.collected_data])
            self.mapping_function = lambda x: griddata(gaze_points, screen_points, x, method='cubic')

    def map_gaze_to_screen(self, gaze_point):
        if self.mapping_function is not None:
            mapped_point = self.mapping_function(np.array([gaze_point]))
            if not np.isnan(mapped_point).any():
                return (
                    int(mapped_point[0][0] * self.screen_width),
                    int(mapped_point[0][1] * self.screen_height)
                )
        return None
