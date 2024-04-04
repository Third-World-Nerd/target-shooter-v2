import time

import cv2
import numpy as np
from serial import Serial
from serial import SerialException

from constants import BAUD_RATE
from constants import CAMERA_NOZZLE_ANGLE_OFFSET
from constants import LOWER_HSV_LIMIT
from constants import SERIAL_PORT
from constants import UPPER_HSV_LIMIT

# Establish serial connection
try:
    ser = Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Serial connection established.")
except SerialException as e:
    print("Error: Serial connection failed:", e)


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


# Function to map angle to servo pulse width for servo X (range: 0-210)
def map_angle_to_pulse_width_x(angle):
    min_angle = 0
    max_angle = 210
    min_pulse_width = 500
    max_pulse_width = 2500
    return int(
        (angle - min_angle)
        * (max_pulse_width - min_pulse_width)
        / (max_angle - min_angle)
        + min_pulse_width
    )


# Function to map angle to servo pulse width for servo Y (range: 0-320)
def map_angle_to_pulse_width_z(angle):
    min_angle = 0
    max_angle = 320
    min_pulse_width = 500
    max_pulse_width = 2500
    return int(
        (angle - min_angle)
        * (max_pulse_width - min_pulse_width)
        / (max_angle - min_angle)
        + min_pulse_width
    )


def shoot_target(servoX_angle, servoZ_angle, isShoot):
    # Update angles by adding deltas to previous angles

    # Convert angle to servo pulse width
    pulse_width_x = map_angle_to_pulse_width_x(
        servoX_angle + CAMERA_NOZZLE_ANGLE_OFFSET
    )
    pulse_width_z = map_angle_to_pulse_width_z(servoZ_angle)

    # Send pulse width data to Arduino
    ser.write(f"{pulse_width_x} {pulse_width_z} {isShoot}\n".encode())


def limit_angles(servoX_angle, servoZ_angle):
    if servoX_angle < 0:
        servoX_angle = 0
    elif servoX_angle > 210:
        servoX_angle = 210

    if servoZ_angle < 0:
        servoZ_angle = 0
    elif servoZ_angle > 320:
        servoZ_angle = 320

    # servo X should not hit the ground for protection
    if servoX_angle > 120:
        servoX_angle = 120

    return servoX_angle, servoZ_angle
