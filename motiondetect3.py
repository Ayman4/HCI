import cv2
import time
import numpy as np
import os
# Define video capture object
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or specify a video file path

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Adjust codec if needed
current_time = time.strftime("%d-%m-%y %H-%M-%S")
outputFile='Video'+current_time+'.mp4'
out = cv2.VideoWriter(outputFile, fourcc, 20.0, (640, 480))  # Adjust resolution
max_size=100*1024*1024
output_size=0

# Initialize background frame
_, background = cap.read()
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

background = cv2.GaussianBlur(background, (11, 11), 0)
background = cv2.threshold(background, 30, 255, cv2.THRESH_BINARY)[1]
# Continuously capture frames
MaxBufferedFrames=100
CurrentFrames=0
while True:
    ret, frame = cap.read()

    if not ret:
        break  # End loop if no frame is captured

    # Convert frame to grayscale and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    gray = cv2.threshold(gray,30, 255, cv2.THRESH_BINARY)[1]
    

    # Calculate absolute difference between current frame and background
    diff = cv2.subtract(gray,background)
    diffCount=np.sum(diff==255)
    cv2.imshow('Difference', diff)
    print(diffCount)
    motion_detected = False
    if diffCount > 1000 or CurrentFrames>0:  # Adjust threshold as needed
        CurrentFrames+=1
        motion_detected = True
        current_time = time.strftime("%d - %m- %y %H:%M:%S")
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        color = (0, 0, 255)
        thickness = 2
        # Adjust position as needed
        text_position = (10, 30)
        cv2.putText(frame, current_time, text_position, font, font_scale, color, thickness)
        # Write the current frame to the video file if motion is detected
        out.write(frame)
        output_size=os.path.getsize(outputFile)
        if CurrentFrames==MaxBufferedFrames:
            CurrentFrames=0

    cv2.imshow('Motion Detection', frame)
    if output_size>max_size:
        out.release()
        out=None
        current_time = time.strftime("%d-%m-%y %H-%M-%S")
        outputFile='Video'+current_time+'.mp4'
        out = cv2.VideoWriter(outputFile, fourcc, 20.0, (640, 480)) 

    # Exit if 'q' key is pressed
    background = gray
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
