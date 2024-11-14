import numpy as np

class KalmanFilter:
    def __init__(self, initial_state):
        self.state = np.array(initial_state, dtype=np.float32).reshape(2, 1)
        self.error_covariance = np.eye(2, dtype=np.float32) * 1000
        self.process_noise = np.eye(2, dtype=np.float32) * 0.001
        self.measurement_noise = np.eye(2, dtype=np.float32) * 0.1

    def predict(self):
        self.error_covariance += self.process_noise

    def update(self, measurement):
        measurement = np.array(measurement, dtype=np.float32).reshape(2, 1)
        # Ajout de vérification pour éviter la division par zéro
        noise_sum = self.error_covariance + self.measurement_noise
        kalman_gain = self.error_covariance @ np.linalg.inv(noise_sum) if np.linalg.det(noise_sum) != 0 else np.zeros_like(self.error_covariance)
        
        self.state += kalman_gain @ (measurement - self.state)
        self.error_covariance = (np.eye(2) - kalman_gain) @ self.error_covariance
        return self.state.flatten()
