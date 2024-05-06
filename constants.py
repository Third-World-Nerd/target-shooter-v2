HFOV = 30  # Horizontal Field of View of the camera in degrees
VFOV = 22.5  # Vertical Field of View of the camera in degrees (adjust based on your camera)
FRAME_WIDTH = 1280  # Should match the frame width used in camera calibration
FRAME_HEIGHT = 960  # Should match the frame height used in camera calibration

# Define the BGR color to track (example: yellow)
YELLOW_BGR = [0, 255, 255]
# Serial port configuration
SERIAL_PORT = "COM12"  # Change this to match your Arduino's serial port
BAUD_RATE = 9600

LOWER_HSV_LIMIT = [0, 34, 92]  # Lower HSV values for color range detection
UPPER_HSV_LIMIT = [179, 110, 137]  # Upper HSV values for color range detection

CALIBRATION_FILE = "assets/calibration.pkl"

CAMERA_INDEX = 1
CAMERA_NOZZLE_ANGLE_OFFSET = 0
