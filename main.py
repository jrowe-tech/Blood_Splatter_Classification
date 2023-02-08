from blob_utils import *
from robomaster_utils import Robomaster
import datetime
from pdf_utils import PDF
from time import sleep
import cv2


# Add Driver Code Here
def main():
    # Initialize Variables
    detector = generate_aruco_detector(cv2.aruco.DICT_7X7_100)

    # Construct PDF Report
    # path = f"report/{input('Name of generated pdf (include extensions): ')}"
    path='report/test.pdf'
    pdf = PDF(path=path, logo="static/images/logo.jpg")

    # Initialize Robomaster UDP Stream
    # robot = Robomaster()

    while True:
        # Ask For Input
        # input("Hit Enter To Begin Blood Splatter Analysis")

        cap = cv2.VideoCapture(0)
        while True:
            # Detect Aruco Code + Ratio
            # frame = robot.get_frame()
            _, frame = cap.read()
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            detected, ratio = aruco_ratio(frame, detector, 100)

            # Signal aruco code detection
            if detected:
                break
            else:
                # Make not detected sound here
                # robot.ep_robot.
                pass

            sleep(3.0)

        # Move robot to blood splatter scene
        robot.move_left(100, blocking=True)

        # Run detection algorithm
        pdf.generateSplatterAnalysis(ratio, detected)

        repeat = input("Run again? (y/n) >>> ").lower()
        if repeat not in {"y", "yes"}:
            break
        else:
            robot.move_right(500, speed=0.4, blocking=True)

    # Ask For Credentials

    name = input("Enter your operator title >>> ")
    site = input("Enter the name of the site >>> ")
    date = date.strftime(date.today(), "%mm/dd/YYYY%")

    # Construct Title Page
    pdf.createTitlePage(site, date, name)

    # Save Completed PDF
    pdf.save()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
