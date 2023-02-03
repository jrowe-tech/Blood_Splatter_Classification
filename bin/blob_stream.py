from blob_utils import *
import cv2



class Blob_Window:
    def __init__(self, window_name="Control Panel", size=(500, 500)):
        self.window_name = window_name

        self.window = cv2.namedWindow(self.window_name)
        cv2.resizeWindow(self.window_name, *size)

        # Construct Additional CheckBox Parameters
        self.blob_params = {
            "filterByArea": False,
            "filterByCircularity": False,
            "filterByConvexity": False,
            "filterByInertia": False,
            "minArea": 1,
            "minCircularity": 1,
            "minConvexity": 1,
            "minInertia": 1
        }

        # Define default slider values
        self.hsv_values = [[0, 0, 0], [179, 255, 255]]

        # Construct Trackbar Objects
        cv2.createTrackbar("Hue Min", self.window_name, 0, 179, self.min_hue_call)
        cv2.createTrackbar("Hue Max", self.window_name, 179, 179, self.max_hue_call)
        cv2.createTrackbar("Sat Min", self.window_name, 0, 255, self.min_sat_call)
        cv2.createTrackbar("Sat Max", self.window_name, 255, 255, self.max_sat_call)
        cv2.createTrackbar("Val Min", self.window_name, 0, 255, self.min_val_call)
        cv2.createTrackbar("Val Max", self.window_name, 255, 255, self.max_val_call)

        # Construct Checkbox Objects
        cv2.createTrackbar("Detect Blobs", self.window_name, 0, 1, self.blob_call)
        cv2.createTrackbar("HSV Percentage", self.window_name, 0, 100, self.hsv_filter_call)
        cv2.createTrackbar("Minimum Blob Area", self.window_name, 0, 100, self.area_call)
        cv2.createTrackbar("Minimum Circularity", self.window_name, 0, 100, self.circularity_call)
        cv2.createTrackbar("Minimum Convexity", self.window_name, 0, 100, self.convexity_call)
        cv2.createTrackbar("Minimum Inertia", self.window_name, 0, 100, self.inertia_call)

        self.show_blobs = False
        self.hsv_percent = 0.00


    def blob_call(self, val):
        self.show_blobs = val

    def area_call(self, val):
        self.blob_params["minArea"] = max(val, 1)

        if val == 0:
            self.blob_params["filterByArea"] = False
        else:
            self.blob_params["filterByArea"] = True


    def circularity_call(self, val):
        self.blob_params["minCircularity"] = max(val, 1) / 100

        if val == 0:
            self.blob_params["filterByCircularity"] = False
        else:
            self.blob_params["filterByCircularity"] = True

    def convexity_call(self, val):
        self.blob_params["minConvexity"] = max(val, 1) / 100

        if val == 0:
            self.blob_params["filterByConvexity"] = False
        else:
            self.blob_params["filterByConvexity"] = True

    def inertia_call(self, val):
        self.blob_params["minInertia"] = max(val, 1) / 100

        if val == 0:
            self.blob_params["filterByInertia"] = False
        else:
            self.blob_params["filterByInertia"] = True

    def min_hue_call(self, val):
        self.hsv_values[0][0] = val

    def max_hue_call(self, val):
        self.hsv_values[1][0] = val

    def min_sat_call(self, val):
        self.hsv_values[0][1] = val

    def max_sat_call(self, val):
        self.hsv_values[1][1] = val

    def min_val_call(self, val):
        self.hsv_values[0][2] = val

    def max_val_call(self, val):
        self.hsv_values[1][2] = val

    def hsv_filter_call(self, val):
        self.hsv_percent = val / 100

    def stream(self, exit_keys={'q', 27}):
        ascii_keys = set()

        for key in exit_keys:
            if key is str:
                ascii_keys.add(ord(key))
            else:
                ascii_keys.add(key)

        cam = cv2.VideoCapture(0)
        while True:
            active, frame = cam.read()

            if active:
                formatted_hsv = tuple(tuple(x) for x in self.hsv_values)

                frame = cv2.GaussianBlur(frame, (7, 7), 10)
                hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hsv_mask = overflow_hsv(frame, formatted_hsv)

                if self.show_blobs:
                    blobs = detect_blobs(frame, **self.blob_params)

                    if self.hsv_percent > 0:
                        blobs = hsv_filter_blobs(frame, blobs, formatted_hsv,
                                                 self.hsv_percent)

                    frame = annotate_image_blobs(frame, blobs)

                cv2.imshow("Detection Frame", frame)
                cv2.imshow("HSV Mask", hsv_mask)

            key = cv2.waitKey(1)
            if key in {27, 13}:
                break

        cam.release()
        cv2.destroyAllWindows()


def main():
    window = Blob_Window()
    window.stream()


if __name__ == "__main__":
    main()
