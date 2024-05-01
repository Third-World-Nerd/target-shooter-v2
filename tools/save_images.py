import os

import cv2

# Initialize the camera
cap = cv2.VideoCapture(1)  # 0 is usually the default camera

num = 0  # Counter for image filenames

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, "../assets/images")  # Path for the "images" folder

# Create the "images" folder if it doesn't exist
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Main loop to capture images
while cap.isOpened():
    success, img = cap.read()  # Read frame from camera

    if not success:
        print("Failed to capture image")
        break

    k = cv2.waitKey(1)  # Use a small delay in waitKey

    if k == ord("q"):  # Quit on 'q' key press
        break
    elif k == ord("s"):  # Save on 's' key press
        image_path = os.path.join(
            image_dir, f"img{num}.png"
        )  # Use f-string for clarity
        cv2.imwrite(image_path, img)  # Save the image
        print(f"Image saved at {image_path}")
        num += 1  # Increment image counter

    cv2.imshow("Img", img)  # Display the captured frame

# Release the camera and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
