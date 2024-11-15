import cv2
import time
from src.acquisition.camera_capture import CameraCapture
from src.detection.eye_detection import AdvancedEyeDetector
from src.engagement.attention import AttentionCalculator
from src.fatigue.fatigue_detector import FatigueDetector
from src.visualization.heatmap import HeatmapGenerator
from src.calibration.auto_calibration import AutoCalibration
from src.tracking.kalman_filter import KalmanFilter
from src.head_movement.head_movement_detector import HeadMovementDetector

def main():
    # Initialize modules and variables
    screen_size = (640, 480)
    eye_detector = AdvancedEyeDetector()
    attention_calculator = AttentionCalculator(screen_size)
    fatigue_detector = FatigueDetector(blink_threshold=0.25)  # Adjust threshold if necessary
    heatmap_generator = HeatmapGenerator(screen_size)
    calibration = AutoCalibration(screen_size)
    kalman_filter = KalmanFilter(initial_state=[0, 0])
    head_movement_detector = HeadMovementDetector()

    camera = CameraCapture(0)
    engagement_score = 100
    blink_count = 0
    display_points_animation = False
    animation_start_time = 0
    previous_eye_center_y = None  # Track previous eye center y-coordinate

    while True:
        # Capture frame
        frame = camera.get_frame()
        frame_with_eyes, eyes_detected, avg_ear, eyes_hidden, nose_point = eye_detector.detect_eyes(frame)

        # If eyes are visible, continue processing
        if not eyes_hidden and avg_ear:
            for eye_data in eyes_detected:
                left_center = eye_data['left_eye']
                right_center = eye_data['right_eye']

                # Stabilize coordinates with KalmanFilter
                stabilized_left = kalman_filter.update(left_center)
                stabilized_right = kalman_filter.update(right_center)

                # Automatic calibration
                if not calibration.is_calibrated:
                    calibration.collect_calibration_data(stabilized_left, stabilized_right)

                # Add fixation points for heatmap
                attention_calculator.calculate_attention(stabilized_left)
                heatmap_generator.add_fixation_point(stabilized_left)

                # Advanced head movement detection
                head_direction = head_movement_detector.detect_head_movement(
                    nose_point, stabilized_left, stabilized_right
                )
                cv2.putText(
                    frame_with_eyes,
                    f'Tête orientée : {head_direction}',
                    (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2,
                )

                # Calculate eye vertical movement
                current_eye_center_y = (left_center[1] + right_center[1]) / 2
                if previous_eye_center_y is not None:
                    eye_vertical_movement = abs(current_eye_center_y - previous_eye_center_y)
                else:
                    eye_vertical_movement = 0  # Initialize movement for the first frame
                previous_eye_center_y = current_eye_center_y  # Update for next frame

                # Blink detection and engagement score management
                blink_detected = fatigue_detector.detect_blink(avg_ear, eye_vertical_movement)
                if blink_detected:
                    blink_count += 1
                    print(f"Clignements détectés : {blink_count}")  # Debug
                    if blink_count >= 10:
                        engagement_score += 50
                        blink_count = 0
                        display_points_animation = True
                        animation_start_time = time.time()

        # Display "+50pts" animation
        if display_points_animation and time.time() - animation_start_time < 1:
            cv2.putText(
                frame_with_eyes,
                "+50pts",
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 255),
                3,
            )
        else:
            display_points_animation = False

        # Display scores, fatigue status, and other information
        cv2.putText(
            frame_with_eyes,
            f'Engagement Score: {engagement_score}',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            frame_with_eyes,
            f'Fatigue Status: {"Fatigué" if fatigue_detector.is_fatigued() else "Non fatigué"}',
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        # Display visual field (heatmap)
        frame_with_eyes = heatmap_generator.overlay_heatmap(frame_with_eyes)
        # Show video with data
        cv2.imshow('Eye Tracking with Engagement and Fatigue Monitoring', frame_with_eyes)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
