import pickle

import cv2
import numpy as np

# from arduino import position_camera
# from arduino import rotate_camera
from constants import FRAME_HEIGHT
from constants import FRAME_WIDTH
from constants import HFOV
from constants import VFOV
from utils import get_target


def load_calibration_data(calibration_file):
    with open(calibration_file, "rb") as file:
        camera_matrix, dist_coeffs = pickle.load(file)
    return camera_matrix, dist_coeffs


def undistort_points(points, camera_matrix, dist_coeffs):
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


if __name__ == "__main__":
    # Load camera calibration data
    calibration_file = "assets/calibration.pkl"  # Adjust the filename/path as necessary
    camera_matrix, dist_coeffs = load_calibration_data(calibration_file)

    # Initialize previous angles
    prev_angle_x = 0
    prev_angle_z = 0

    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            exit()

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

        cv2.imshow("Tracking", img)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
            # Undistort the center point
            undistorted_point = undistort_points(
                [(target_center_x, target_center_y)], camera_matrix, dist_coeffs
            )
            undistorted_target_center_x, undistorted_target_center_y = (
                undistorted_point[0]
            )

            frame_center_x = FRAME_WIDTH // 2
            frame_center_y = FRAME_HEIGHT // 2
            rotation_angle_hor, rotation_angle_ver = calculate_rotation_angles(
                undistorted_target_center_x,
                undistorted_target_center_y,
            )

            print(
                f"Rotation Angle Vertical: {rotation_angle_ver} degrees, Rotation Angle Horizontal: {rotation_angle_hor} degrees"
            )
            # # Here, you can add code to rotate the camera based on the calculated rotation angles.

            # curr_x, curr_z = position_camera()

            # rotate_camera(curr_x, curr_z, rotation_angle_ver, rotation_angle_hor)

        else:
            print("No color detected within the specified time frame.")
