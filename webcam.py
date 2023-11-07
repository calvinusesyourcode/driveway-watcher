import cv2, time
from datetime import datetime

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Define the region of interest (ROI) variables
x, y, width, height = 350, 180, 250, 120  # Customize these values for your setup
threshold = 7000  # Customize this threshold for motion sensitivity

# Function to display the ROI on the frame
def draw_roi(frame, x, y, width, height):
    cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

# Function to save the image when motion is detected
def save_screenshot(roi):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"motion_{timestamp}.png"
    cv2.imwrite(filename, roi)
    print(f"Saved {filename}")

# Initialize prev_frame as None
prev_frame = None
time_of_last_detection = time.time()
starttime = time.time()
motion_detected = False

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Define the region of interest
    roi = gray[y:y + height, x:x + width]

    # Initialize prev_frame with the first roi
    if prev_frame is None:
        prev_frame = roi
        continue # Skip the rest of the loop to prevent detecting motion on initialization

    # Compute the absolute difference between the current frame and the previous frame
    frame_delta = cv2.absdiff(prev_frame, roi)
    # Apply a binary threshold to the delta image
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    # Calculate the number of white pixels in the threshold image
    motion_level = cv2.countNonZero(thresh)

    # If the number of white pixels is greater than the threshold, motion is detected \ unless it's the first three seconds of the script running
    if motion_level > threshold and not (time.time() - starttime) < 3:
        time_of_last_detection = time.time()
        print("Motion detected!")
        if motion_detected == True:
            save_screenshot(frame[y:y + height, x:x + width])
            print("Car!")
        motion_detected = True
    else:
        motion_detected = False

    # Display the resulting frame with the ROI
    draw_roi(frame, x, y, width, height)
    cv2.imshow('Frame', frame)

    # Save the current ROI as the previous frame for the next iteration
    prev_frame = roi

    # Wait for 1 second (1000 milliseconds)
    if cv2.waitKey(1500) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
