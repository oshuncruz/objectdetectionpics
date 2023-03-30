import torch
import cv2
import subprocess
import time

last_capture_time = time.time()

capture_interval = 3
# Load the YOLOv5 PyTorch model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/oshun/OneDrive/Desktop/T-shirt-Object-Detection-master/yolov5/best2.pt')


def run_gphoto2():
    global last_capture_time
    
    # Check if the minimum time between captures has passed
    if time.time() - last_capture_time >= capture_interval:
        # Define the command to run in the mingw64 terminal
        cmd = 'C:/msys64/mingw64.exe gphoto2 --capture-image'
        
        # Open a new process with the command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Read the output and error messages from the process
        output, error = process.communicate()
        
        # Print the output and error messages
        print(output.decode('utf-8'))
        print(error.decode('utf-8'))
        
        # Update the last_capture_time variable to the current time
        last_capture_time = time.time()


# Define the video capture device (in this case, the default webcam)
cap = cv2.VideoCapture(0)

confidence_threshold = 0.5

while True:
    # Read a frame from the video capture device
    ret, frame = cap.read()

    # Perform object detection on the frame using the YOLOv5 model
    results = model(frame)

    # Filter detections based on confidence level
    filtered_detections = [detection for detection in results.xyxy[0] if detection[4] >= confidence_threshold]

    # Draw bounding boxes around the detected objects
    for detection in filtered_detections:
        x1, y1, x2, y2, conf, cls = detection
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

            # Draw the confidence score next to the bounding box
        label = f'{conf:.2f}'
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        cv2.rectangle(frame, (int(x1), int(y1 - text_size[1] - 4)), (int(x1 + text_size[0]), int(y1)), (255, 0, 0), -1)
        cv2.putText(frame, label, (int(x1), int(y1 - 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        # Get the center point of the screen
        screen_width, screen_height = frame.shape[1], frame.shape[0]
        screen_center_x, screen_center_y = screen_width / 2, screen_height / 2

        # Calculate the distance between the bounding box center and the screen center
        distance_to_center = ((center_x - screen_center_x) ** 2 + (center_y - screen_center_y) ** 2) ** 0.5

        # If the distance is small enough, run the function
        if distance_to_center < 50:
            run_gphoto2()




    # Display the frame with the bounding boxes

    cv2.imshow('Object Detection', frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()
