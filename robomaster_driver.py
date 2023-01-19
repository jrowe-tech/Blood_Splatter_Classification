# --Time for custom driver-- (:

import sys
import socket


class Robomaster:
    # Popular commands from the API
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

    def __init__(self, port: int = 40923, host: str = "192.168.2.1"):
        self.port = port
        self.host = host

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Connecting...")
        socket.connect((host, port))
        print("Connected Successfully!")

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
                print(**self.robomaster_commands)
            elif msg.lower() == "list_variables":
                print(**self.robomaster_variables)

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
        socket.shutdown(socket.SHUT_WR)
        socket.close()


if __name__ == '__main__':
    driver = Robomaster()
