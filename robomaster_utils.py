from robomaster import robot
from typing import Union
from time import sleep


class Robomaster:

    def __init__(self):
        # Configure Robomaster From Wifi
        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type="ap", proto_type="udp")
        self.camera = self.ep_robot.camera
        self.camera.start_video_stream(display=True)
        self.chassis = self.ep_robot.chassis

    def get_version(self) -> str:
        version = self.ep_robot.get_version()
        return f"Robomaster EP Version: {version}"

    def get_frame(self):
        return self.camera.read_video_frame()

    def move_left(self, dX: float, speed: float = 1.0, blocking=False):
        self.chassis.move(x=-(dX / 1000), xy_speed=speed)

        if blocking:
            self.speed_distance_sleep(dX, speed)

        return

    def move_right(self, dX: float, speed: float = 1.0, blocking=False):
        self.chassis.move(x=(dX / 1000), xy_speed=speed)

        if blocking:
            self.speed_distance_sleep(dX, speed)

        return

    def move_forward(self, dY: float, speed: float = 1.0, blocking=False):
        self.chassis.move(y=(dY / 1000), xy_speed=speed)

        if blocking:
            self.speed_distance_sleep(dY, speed)

        return

    def move_backwards(self, dY: float, speed: float = 1.0, blocking=False):
        self.chassis.move(y=-(dY / 1000), xy_speed=speed)

        if blocking:
            self.speed_distance_sleep(dY, speed)

        return

    @staticmethod
    def speed_distance_sleep(distance: Union[int, float], speed: Union[int, float]):
        sleep((distance / speed) * 100)
        return
