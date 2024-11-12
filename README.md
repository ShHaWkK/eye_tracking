# Eye Tracking Project

This project aims to develop a real-time eye tracking system using only the computer camera.

This **eye tracking** project uses blink detection to estimate the status of **fatigue** and measure a user’s **engagement score** in real time. 

## In progress for: 

- The program detects blinking and increases the engagement score every 10 blinks with an animation `"+50pts". 
- It also includes a fatigue alert, based on the duration and frequency of blinking.

## Features

-**Eye Tracking**: Uses eye landmarks to detect blinking and movement.
- **Fatigue Detection** Analyses average blink time and frequency to indicate fatigue.
- **Engagement Score**: Increases the score after each series of 10 blinks with a visual animation. (in progress...)
- **Real-time display** shows fatigue status, engagement score and blink count directly in the video.

## Prerequisites

- **Python 3.7+**
- **Packages** : opencv-python, numpy, mediapipe

Make sure the necessary packages are installed by running the following command:
`bash
pip install opencv-python numpy mediapipe
`
## Installation

1. Clone this repository
2. Create a virtual environment: ‘python -m venv venv’
3. Enable virtual environment: ‘venv Scripts Activate’
4. Install dependencies: ‘pip install -r requirements.txt’

## Usage

Run the main script: ‘python main.py’

Press 'q' to exit.

## Project Structure

## Explanation of the Parameters

The project uses multiple parameters to adjust the sensitivity of fatigue detection and engagement. These parameters are configurable in the ‘FatigueDetector’ class and can be modified to meet specific user needs.

| Parameter   | Description   | Default value |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------|--------------------|
| **`blink_threshold`**   | EAR (Eye Aspect Ratio) minimum to consider an eye closed. This determines when a blink is detected.   | `0.25`   |
| **‘fatigue_duration_threshold’** | Average blink time (in seconds) above which fatigue is indicated.   | `0.3‘   |
| **`blink_frequency_threshold`**   | Number of blinks in the interval `check_interval`to indicate fatigue.   | `8‘   |
| **`check_interval`**   | Time interval (in seconds) to check blink frequency and assess fatigue.   | `30‘   |
| **`min_blink_duration`**   | Minimum blink time (in seconds) to be considered valid.   | `0.1‘   |
| ***`zoom_factor`**   | Zoom factor used in ‘AdvancedEyeDetector’ to adjust the size of the detected face when there is movement.   | `1.5‘   |
| **`face_size_threshold`**   | Minimum face size to zoom in when user moves away from camera.   | `200‘   |


### Example of Customization of Parameters

If the system is too sensitive (detecting too much blinking or reporting fatigue too quickly), you can increase the values of fatigue_duration_threshold` and `check_interval`. An example of a fit configuration is:

``python
fatiguee_detector = FatigueDetector(
    blink_threshold=0.25,
    fatigue_duration_threshold=0.4,  # Increased to make fatigue detection less sensitive
    blink_frequency_threshold=10,   # Increased to reduce frequency of fatigue alerts
    check_interval=60,   # Double the blink check time
    min_blink_duration=0.12   # Adjusted to filter for very fast blinking
)
``

## Next steps

- Develop the eye estimation
- Dynamic Fit for Users with Glasses