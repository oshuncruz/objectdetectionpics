# Object Detection with Remote Camera Control

This Python script utilizes YOLOv5 for real-time object detection using your camera, with the ability to capture images when specific conditions are met. The captured images are saved locally. Below is a step-by-step guide on how to use the code.

## Prerequisites

1. You need to have Python installed on your system.
2. Ensure that you have the required libraries installed. You can install them using `pip` if not already installed:
   - `subprocess`
   - `cv2` (OpenCV)
   - `torch` (PyTorch)
   - `time`
   - `pyautogui`
   - `pydirectinput`

## Configuration

Before running the script, there are a few settings you should configure:

- `REMOTE_CONTROL_EXE`: Set the path to the Remote Camera Control software executable.
- `IMAGE_SAVE_PATH`: Set the path where you want to save the captured images.
- `confidence_threshold`: Define the confidence threshold for object detection.
- `skirt_id`, `short_sleeved_dress_id`, `long_sleeved_dress_id`, `vest_dress_id`, `sling_dress_id`: Define the class IDs to filter out (ignore) during object detection.

## Usage

1. Run the script. It will perform the following actions:
   - Connect to the camera using the Remote Camera Control software.
   - Start the Remote Camera Control tool.
   - Continuously capture frames from the camera and perform object detection using YOLOv5.
   - When objects are detected, it filters them based on class IDs and displays bounding boxes around them.

2. If an object is detected, and it is located in the center of the screen (within 10% of the screen width and height), the script will:
   - Activate the Remote Camera Control tool.
   - Simulate pressing the '1' key to capture an image.

3. Press the 'q' key to exit the script and close the object detection window.

## Notes

- You should have the Remote Camera Control software installed and set up correctly.
- Ensure your camera is connected and properly configured.
- The script assumes that your camera is accessible via the `cv2.VideoCapture` interface. You may need to adjust the camera index (currently set to 1) if you have multiple cameras.

Please note that this script was designed for a specific use case and may require further customization to fit your specific needs.

