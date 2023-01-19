# -*- encoding: utf-8 -*-
# Test environment: Python 3.6

import socket
import sys

host = "192.168.2.1"  # IP grab the Robomaster
control_port = 40923  # Default IP Address
video_port = 40921


def test_video_stream():
    TCP_IP = '193.168.2.1'
    TCP_PORT = 40921
    BUFFER_SIZE = 2056

    f = open('stream.h264', 'wb')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    while True:
        data = sock.recv(BUFFER_SIZE)
        f.write(data)
        print("Writing")
    sock.close()
    f.close()


# Save some commands for the class
robomaster_commands = {
    "command": "Activates SDK override mode. Returns ok if connected properly.",
    "quit": "Exits SDK override mode. Returns ok if connected properly.",
    "robot mode [mode_enum]": "Changes the movement mode.",
    "robot mode ?": "Returns the current movement mode.",
    "robot battery ?": "Returns the current battery charge.",
    "chassis speed x [float] y [float] z [float]": "Changes chassis movement speed. \n X / Y must be between -3.5 to 3.5 m/s. Z must be between -600 to 600 deg/s.",
    "chassis speed ?": "Returns the current chassis speed + wheel speeds.",
    "chassis position ?": "Returns comparative position from when robot was turned on in meters.",
    "chassis attitude ?": "Returns pitch, roll, yaw information in degrees.",
    "chassis status ?": "Returns 1 if true, 0 if false for several chassis queries. See values in variables as chassis_status",
    "gimbal susped": "Puts the gimbal in the sleeping state.",
    "Plaintext function API": "\nhttps://robomaster-dev.readthedocs.io/en/latest/text_sdk/protocol_api.html",
    "Plaintext variable API": "https://robomaster-dev.readthedocs.io/en/latest/text_sdk/data_define.html",
    "It's official": "This API sucks."
}

# Save these god-awful enumeration variables
robomaster_variables = {
    "move_enum": "chassis_lead / gimbal_lead / free",
    "switch_enum": "on / off",
    "chasis_push_attr_enum": "position / attitude / status",
    "gimbal_push_attr_enum": "attitude",
    "armor_event_attr_enum": "hit",
    "sound_event_attr_enum": "applause",
    "led_comp_enum": "all / top_all / top_right / bottom_all / bottom_front / bottom_back / bottom_left / bottom_right",
    "led_effect_enum": "solid / off / pulse / blink / scrolling",
    "line_color_enum": "red / blue / green",
    "marker_color_enum": "red / blue",
    "ai_push_attr_enum": "person / gesture / line / marker / robot",
    "ai_pose_id_enum": "4 / 5 / 6",
    "ai_marker_id_enum": "1 / 4 / 5 / 6 / 8 / 10 - 19 / 20 - 45",
    "camera_ev_enum": "default / small / medium / large",
    "chassis_status": """11 Bit List Of True / False (0 / 1). Each bit's check:
        1) static: Whether the chassis is still.
        2) uphill: Whether the chassis is going uphill.
        3) downhill: Whether the chassis is going downhill.
        4) on_slope: Whether the chassis is on a slope.
        5) pick_up: Whether the chassis is picked up.
        6) slip: Whether the chassis is slipping
        7) impact_x: Whether the x-axis senses an impact
        8) impact_y: Whether the y-axis senses an impact
        9) impact_z: Whether the z-axis senses an impact
        10) roll_over: Whether the chassis is rolled over.
        11) hill_static: Whether the chassis is still on a slope.""",
}


def main():
    address = (host, int(control_port))

    # Establish a TCP connection with the control command port of the robot.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting...")

    s.connect(address)

    print("""Connected!\n
        Enter q to quit program (send quit to Robomaster first for proper disconnection)!
        Enter command to start connection!
        Enter list_commands / list_variables to get a list of functions and variables (by Jake)!\n""")

    while True:

        # Wait for the user to enter control commands.
        msg = input(">>> please input SDK cmd: ")

        # When the user enters Q or q, exit the current program.
        if msg.upper() == 'Q':
            break
        elif msg.lower() == "list_commands":
            print(robomaster_commands)
        elif msg.lower() == "list_variables":
            print(robomaster_variables)
        elif msg.lower() == "test_video":
            print("Turned Video Stream On")
            test_video_stream()
            break

        # Add the ending character.
        msg += ';'

        # Send control commands to the robot.
        s.send(msg.encode('utf-8'))

        try:
            # Wait for the robot to return the execution result.
            buf = s.recv(1024)

            print(buf.decode('utf-8'))
        except socket.error as e:
            print("Error receiving :", e)
            sys.exit(1)
        if not len(buf):
            break

    # Disconnect the port connection.
    s.shutdown(socket.SHUT_WR)
    s.close()


if __name__ == '__main__':
    main()
