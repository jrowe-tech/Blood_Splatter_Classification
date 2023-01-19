from blob_utils import *
import cv2


def main():
    cam = cv2.VideoCapture(0)

    detector = generate_aruco_detector(cv2.aruco.DICT_7X7_100)

    while (cam.isOpened()):
        active, frame = cam.read()

        if active:
            frame = cv2.GaussianBlur(frame, (5, 5), 0)

            detected, ratio = aruco_ratio(frame, detector, 100)

            if detected:
                # Test 100 Pixels To mm With Ratio
                print(ratio * 100)

            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key in {13, 27}:
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
