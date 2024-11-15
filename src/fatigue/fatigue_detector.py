import time

class FatigueDetector:
    def __init__(self, blink_threshold=0.25, fatigue_duration_threshold=0.3, blink_frequency_threshold=8,
                 check_interval=30, min_blink_duration=0.1, inactivity_timeout=5):
        """
        Initializes the advanced fatigue and blink detector.

        :param blink_threshold: EAR threshold for detecting a closed eye.
        :param fatigue_duration_threshold: Average blink duration indicating fatigue.
        :param blink_frequency_threshold: Blink count in a given interval indicating fatigue.
        :param check_interval: Time interval in seconds for re-evaluating fatigue.
        :param min_blink_duration: Minimum blink duration to be counted.
        :param inactivity_timeout: Time without blinks after which inactivity is detected.
        """
        self.blink_threshold = blink_threshold
        self.fatigue_duration_threshold = fatigue_duration_threshold
        self.blink_frequency_threshold = blink_frequency_threshold
        self.check_interval = check_interval
        self.min_blink_duration = min_blink_duration
        self.inactivity_timeout = inactivity_timeout

        # Tracking and timing variables
        self.blink_count = 0
        self.blink_start_time = None
        self.is_blinking = False
        self.blink_durations = []
        self.last_check_time = time.time()
        self.blinks_in_interval = 0
        self.last_blink_time = time.time()
        self.fatigue_alert = False
        self.previous_ear = None  # To track EAR stability
        self.consistent_blink_time = 0.05  # Minimum time for a consistent blink (in seconds)

    def detect_blink(self, eye_aspect_ratio, eye_vertical_movement=None):
        """
        Detects blinks based on EAR and eye vertical movement consistency.

        :param eye_aspect_ratio: EAR value to assess if the eye is closed.
        :param eye_vertical_movement: Optional, vertical movement of the eye center to avoid false blinks.
        :return: bool - True if a blink is detected, otherwise False.
        """
        current_time = time.time()

        # Check if EAR is consistently below the threshold for a set duration
        if eye_aspect_ratio < self.blink_threshold:
            # Begin tracking the blink duration if starting a new blink
            if not self.is_blinking:
                self.is_blinking = True
                self.blink_start_time = current_time
            else:
                # Check if the duration below the threshold is long enough
                blink_duration = current_time - self.blink_start_time
                if blink_duration >= self.consistent_blink_time:
                    # Confirm blink only if no significant eye vertical movement indicates looking down
                    if eye_vertical_movement is None or eye_vertical_movement < 5:
                        # Register a blink if duration and movement are within thresholds
                        if blink_duration >= self.min_blink_duration:
                            self.blink_count += 1
                            self.blink_durations.append(blink_duration)
                            self.blinks_in_interval += 1
                            self.last_blink_time = current_time
                            self.is_blinking = False  # Reset for next blink
                            return True  # Blink detected
        else:
            # Reset if EAR goes above threshold without meeting blink duration
            if self.is_blinking:
                self.is_blinking = False

        # Detect prolonged inactivity
        if current_time - self.last_blink_time > self.inactivity_timeout:
            print("Inactivity detected - Possible sign of fatigue.")
            self.reset()  # Reset due to inactivity

        return False

    def is_fatigued(self):
        """
        Determines fatigue based on blink duration and frequency.

        :return: bool - True if fatigue is detected, otherwise False.
        """
        if self.blink_durations:
            avg_blink_duration = sum(self.blink_durations) / len(self.blink_durations)
        else:
            avg_blink_duration = 0

        # Check fatigue based on blink duration
        if avg_blink_duration > self.fatigue_duration_threshold:
            self.fatigue_alert = True
        else:
            self.fatigue_alert = False

        # Check blink frequency in the given interval
        current_time = time.time()
        if current_time - self.last_check_time >= self.check_interval:
            if self.blinks_in_interval > self.blink_frequency_threshold:
                self.fatigue_alert = True
            self.blinks_in_interval = 0
            self.last_check_time = current_time

        return self.fatigue_alert

    def get_blink_count(self):
        """
        Returns the total blink count.
        """
        return self.blink_count

    def reset(self):
        """
        Resets fatigue and blink data for a new detection cycle.
        """
        self.blink_count = 0
        self.blink_durations.clear()
        self.blinks_in_interval = 0
        self.last_check_time = time.time()
        self.last_blink_time = time.time()
        self.fatigue_alert = False
        print("Fatigue detection data reset.")

    def display_fatigue_status(self):
        """
        Displays a message indicating the current fatigue state.
        """
        if self.is_fatigued():
            print("Fatigue detected - Consider taking a break.")
        else:
            print("Alertness is stable.")
