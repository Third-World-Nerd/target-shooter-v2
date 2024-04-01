import cv2
import numpy as np

from constants import LOWER_HSV_LIMIT
from constants import UPPER_HSV_LIMIT


def get_target(img: np.ndarray):
    # blurred_frame = cv2.GaussianBlur(image, (5, 5), 0)
    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_limit = np.array(LOWER_HSV_LIMIT, dtype=np.uint8)
    upper_limit = np.array(UPPER_HSV_LIMIT, dtype=np.uint8)
    mask = cv2.inRange(hsv_frame, lower_limit, upper_limit)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_area = 0
    largest_box = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            if area > largest_area:
                largest_area = area
                largest_box = (x, y, w, h)

    return largest_box
