import sys

import serial

# Serial port configuration
SERIAL_PORT = "COM3"  # Change this to match your Arduino's serial port
BAUD_RATE = 9600

# Initialize previous angles
prev_angle_x = 0
prev_angle_z = 0


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


def position_camera():
    global prev_angle_x, prev_angle_z  # Declare the variables as global

    # Establish serial connection
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Serial connection established.")
    except serial.SerialException as e:
        print("Error: Serial connection failed:", e)
        return

    while True:
        # Read angle from command line
        delta_x = int(input("Enter change in X angle: "))
        delta_z = int(input("Enter change in Z angle: "))

        # Update angles by adding deltas to previous angles
        angle_x = prev_angle_x + delta_x
        angle_z = prev_angle_z + delta_z

        # Constrain angles to specific ranges
        angle_x = max(0, min(angle_x, 120))  # angle_x should be between 0 and 120
        angle_z = max(0, min(angle_z, 320))  # angle_z should be between 0 and 320

        # Convert angle to servo pulse width
        pulse_width_x = map_angle_to_pulse_width_x(angle_x)
        pulse_width_z = map_angle_to_pulse_width_z(angle_z)

        # Send pulse width data to Arduino
        ser.write(f"{pulse_width_x} {pulse_width_z}\n".encode())
        print("Current angle: ", angle_x, angle_z)

        # Update previous angles
        prev_angle_x = angle_x
        prev_angle_z = angle_z

        # Ask user if this is the desired angle
        user_input = input("Is this the desired angle? (yes/no): ").strip().lower()
        if user_input == "yes":
            print(f"Final angles set to: X={angle_x}, Z={angle_z}")
            ser.close()
            # Update previous angles
            prev_angle_x = angle_x
            prev_angle_z = angle_z
            return angle_x, angle_z  # Return the final angles


def rotate_camera(curr_x, curr_z, delta_x, delta_z):
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    # Update angles by adding deltas to previous angles

    angle_x = curr_x + delta_x
    angle_z = curr_z + delta_z

    if angle_x < 0:
        angle_x = 0
    elif angle_x > 210:
        angle_x = 210

    if angle_z < 0:
        angle_z = 0
    elif angle_z > 320:
        angle_z = 320

    # servo X should not hit the ground for protection
    if angle_x > 120:
        angle_x = 120

    # Convert angle to servo pulse width
    pulse_width_x = map_angle_to_pulse_width_x(angle_x)
    pulse_width_z = map_angle_to_pulse_width_z(angle_z)

    # Send pulse width data to Arduino
    ser.write(f"{pulse_width_x} {pulse_width_z}\n".encode())


# if __name__ == "__main__":
#     main()
