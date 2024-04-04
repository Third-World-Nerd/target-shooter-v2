import pickle

import cv2
import numpy as np

# from arduino import position_camera
# from arduino import rotate_camera
from constants import CALIBRATION_FILE
from constants import CAMERA_INDEX
from constants import FRAME_HEIGHT
from constants import FRAME_WIDTH
from constants import HFOV
from constants import VFOV
from utils import get_target
from utils import limit_angles
from utils import shoot_target

servoX_angle = 0
servoZ_angle = 0

with open(CALIBRATION_FILE, "rb") as file:
    camera_matrix, dist_coeffs = pickle.load(file)


def undistort_points(points):
    global camera_matrix, dist_coeffs
    points = np.array(points, dtype=np.float32).reshape(-1, 1, 2)
    undistorted_points = cv2.undistortPoints(
        points, camera_matrix, dist_coeffs, P=camera_matrix
    )
    return undistorted_points.reshape(-1, 2)


def calculate_rotation_angles(
    object_center_x,
    object_center_y,
):
    pixel_offset_x = object_center_x - FRAME_WIDTH // 2
    degrees_per_pixel_x = HFOV / FRAME_WIDTH
    rotation_angle_hor = pixel_offset_x * degrees_per_pixel_x

    pixel_offset_y = object_center_y - FRAME_HEIGHT // 2
    degrees_per_pixel_y = VFOV / FRAME_HEIGHT
    rotation_angle_ver = pixel_offset_y * degrees_per_pixel_y

    return rotation_angle_hor, rotation_angle_ver


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        target_x, target_y = (
            x,
            y,
        )  # Assuming x, y are the coordinates where the mouse was clicked
        direct_camera(target_x, target_y)


def direct_camera(target_center_x, target_center_y):
    global servoX_angle, servoZ_angle
    # Undistort the center point
    undistorted_point = undistort_points([(target_center_x, target_center_y)])
    print(target_center_x, target_center_y, undistorted_point)
    undistorted_target_center_x, undistorted_target_center_y = undistorted_point[0]

    rotation_angle_hor, rotation_angle_ver = calculate_rotation_angles(
        undistorted_target_center_x,
        undistorted_target_center_y,
    )

    servoZ_angle += -rotation_angle_hor
    servoX_angle += rotation_angle_ver

    servoX_angle, servoZ_angle = limit_angles(servoX_angle, servoZ_angle)

    shoot_target(servoX_angle, servoZ_angle, 0)


def shoot():
    print("Shooting at target")
    shoot_target(servoX_angle, servoZ_angle, 1)


if __name__ == "__main__":
    # Initialize previous angles
    prev_angle_x = 0
    prev_angle_z = 0

    cap = cv2.VideoCapture(CAMERA_INDEX)

    cv2.namedWindow("Tracking")
    cv2.setMouseCallback("Tracking", mouse_click)

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            exit()
        key = cv2.waitKey(1)
        # Track the color and get the center of the largest bounding box
        target_bounding_box = get_target(img)
        if target_bounding_box is not None:
            target_center_x, target_center_y, w, h = target_bounding_box
            # Draw bounding box on the image
            cv2.rectangle(
                img,
                (target_center_x, target_center_y),
                (target_center_x + w, target_center_y + h),
                (0, 255, 0),
                2,
            )
            if key == ord(" "):
                direct_camera(target_center_x, target_center_y)

        if key == ord("q"):
            break

        if key == ord("s"):
            shoot()

        cv2.imshow("Tracking", img)
