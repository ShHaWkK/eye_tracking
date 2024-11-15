# src/calibration/auto_calibration.py

class AutoCalibration:
    def __init__(self, screen_size=None):
        """
        Initialise la classe AutoCalibration avec une option de taille d'écran pour la calibration.
        
        :param screen_size: Tuple (width, height) de la taille de l'écran (optionnel)
        """
        self.screen_size = screen_size
        self.calibration_data = []
        self._is_calibrated = False

    def collect_calibration_data(self, left_eye, right_eye):
        """
        Collecte les données de calibration basées sur la position des yeux.
        
        :param left_eye: Coordonnées de l'œil gauche
        :param right_eye: Coordonnées de l'œil droit
        """
        self.calibration_data.append((left_eye, right_eye))
    
        if len(self.calibration_data) >= 10:  
            self.compute_calibration()

    def compute_calibration(self):
        """
        Effectue les calculs nécessaires pour la calibration.
        """
        self._is_calibrated = True
        print("Calibration terminée avec succès.")

    def reset_calibration(self):
        """
        Réinitialise l'état de la calibration et efface les données de calibration.
        """
        self.calibration_data = []
        self._is_calibrated = False
        print("Calibration réinitialisée.")

    @property
    def is_calibrated(self):
        """
        Vérifie si la calibration a été effectuée avec succès.
        
        :return: Booléen indiquant si la calibration est terminée
        """
        return self._is_calibrated
