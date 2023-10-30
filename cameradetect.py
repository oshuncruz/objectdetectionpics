import subprocess
import cv2
import torch
import time
import pyautogui
import pydirectinput

# Set the path to the Remote Camera Control software executable
REMOTE_CONTROL_EXE = 'C:/Program Files/Sony/Imaging Edge/Remote.exe'

# Set the path where you want to save the captured images
IMAGE_SAVE_PATH = 'C:/captured_images/'

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/Oshun/Desktop/camera/best.pt')

# Set the confidence threshold for object detection
confidence_threshold = 0.35

# Class IDs to filter out
skirt_id = 8
short_sleeved_dress_id = 9
long_sleeved_dress_id = 10
vest_dress_id = 11
sling_dress_id = 12

# Connect to the camera
subprocess.Popen([REMOTE_CONTROL_EXE, '-c'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the camera to connect
time.sleep(5)

# Open the remote camera control tool
subprocess.Popen([REMOTE_CONTROL_EXE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create a capture object for the default camera
cap = cv2.VideoCapture(1)

prev_time = time.time()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Perform object detection on the image
    results = model(frame)
    filtered_detections = [detection for detection in results.xyxy[0] if detection[4] >= confidence_threshold]

    for detection in filtered_detections:
        x1, y1, x2, y2, conf, cls = detection

        # Ignore detections with class IDs for dresses and skirts
        if cls == skirt_id or cls == short_sleeved_dress_id or cls == long_sleeved_dress_id or cls == vest_dress_id or cls == sling_dress_id:
            continue

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        label = f'{conf:.2f}'
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        cv2.rectangle(frame, (int(x1), int(y1 - text_size[1] - 4)), (int(x1 + text_size[0]), int(y1)), (255, 0, 0), -1)
        cv2.putText(frame, label, (int(x1), int(y1 - 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        screen_width, screen_height = frame.shape[1], frame.shape[0]
        screen_center_x, screen_center_y = screen_width / 2, screen_height / 2

        # Check if the object is in the center of the screen
        if (x1 >= 0 and y1 >= 0 and x2 <= screen_width and y2 <= screen_height) and \
   (abs(center_x - screen_center_x) < screen_width * 0.1 and abs(center_y - screen_center_y) < screen_height * 0.1):
            curr_time = time.time()
            if curr_time - prev_time >= 2:
                # Capture an image with the remote camera control tool
                remote_window = pyautogui.getWindowsWithTitle('Remote')[0]
                remote_window.activate()

                # Press the '1' key to capture the image
                pydirectinput.press('1')
                print("Remote camera control tool command executed!")
                prev_time = curr_time

    # Display the captured image with object detection
    cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture object and destroy all windows
cap.release()
cv2.destroyAllWindows()
