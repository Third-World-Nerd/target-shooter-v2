import cv2
import numpy as np

# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Starting coordinates of rectangle
rectangles = []  # List to store rectangles


def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()  # Create a copy to preserve the original
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Webcam", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        rectangles.append((ix, iy, x, y))


def get_hsv_color_range(image, rectangle):
    roi = image[rectangle[1] : rectangle[3], rectangle[0] : rectangle[2]]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h_values = hsv_roi[:, :, 0]
    s_values = hsv_roi[:, :, 1]
    v_values = hsv_roi[:, :, 2]

    h_min, h_max = np.min(h_values), np.max(h_values)
    s_min, s_max = np.min(s_values), np.max(s_values)
    v_min, v_max = np.min(v_values), np.max(v_values)

    return (h_min, s_min, v_min), (h_max, s_max, v_max)


# Start capturing video from the webcam
cap = cv2.VideoCapture(1)
cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", draw_rectangle)

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Webcam", img)
    key = cv2.waitKey(1)

    if key == ord("s"):
        captured_img = img.copy()
        while True:
            k = cv2.waitKey(1)
            if k == ord("c"):
                # Get HSV color range for each rectangle drawn
                for rect in rectangles:
                    lower_hsv, upper_hsv = get_hsv_color_range(captured_img, rect)
                    print(f"Rectangle {rect}:")
                    print(f"Lower HSV: {lower_hsv}")
                    print(f"Upper HSV: {upper_hsv}")
                rectangles.clear()
                break
            elif k == ord("q"):
                break

cv2.destroyAllWindows()
cap.release()
