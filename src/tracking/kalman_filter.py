import numpy as np

class KalmanFilter:
    def __init__(self, initial_state):
        self.state = np.array(initial_state, dtype=np.float32).reshape(2, 1)
        self.error_covariance = np.eye(2, dtype=np.float32) * 1000  # Grande incertitude initiale
        self.process_noise = np.eye(2, dtype=np.float32) * 0.001
        self.measurement_noise = np.eye(2, dtype=np.float32) * 0.1

    def predict(self):
        # Prédiction simple : l'état reste le même
        self.error_covariance += self.process_noise

    def update(self, measurement):
        measurement = np.array(measurement, dtype=np.float32).reshape(2, 1)
        
        # Calcul du gain de Kalman
        kalman_gain = self.error_covariance @ np.linalg.inv(self.error_covariance + self.measurement_noise)

        # Mise à jour de l'état
        self.state += kalman_gain @ (measurement - self.state)

        # Mise à jour de la covariance d'erreur
        self.error_covariance = (np.eye(2) - kalman_gain) @ self.error_covariance

        return self.state.flatten()
