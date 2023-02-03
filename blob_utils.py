import cv2
import numpy as np
from typing import Tuple
from nptyping import NDArray
from random import randint
from math import pi, hypot
from typing import Dict, Union

COLOR = Tuple[int, int, int]

def annotate_image_blobs(img: NDArray, keypoints: Tuple, color: COLOR = (0, 0, 255)) -> NDArray:
    blank = np.zeros((1, 1))
    blobs_image = cv2.drawKeypoints(img, keypoints, blank,
                                    color, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return blobs_image


def detect_blobs(img: NDArray, **kwargs) -> NDArray:

    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = kwargs.get('filterByArea', False)
    params.minArea = kwargs.get('minArea', 20)

    params.filterByCircularity = kwargs.get('filterByCircularity', False)
    params.minCircularity = kwargs.get('minCircularity', 0.8)

    params.filterByConvexity = kwargs.get('filterByConvexity', False)
    params.minConvexity = kwargs.get('minConvexity', 0.2)

    params.filterByInertia = kwargs.get('filterByInertia', False)
    params.minInertiaRatio = kwargs.get('minInertiaRatio', 0.01)

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img)

    return keypoints


def create_solid_image(width: int, height: int, color: COLOR = (255, 255, 255)) -> NDArray:
    img = np.zeros([width, height, 3], dtype=np.uint8)
    img[:] = color

    return img


def draw_random_blobs(img: NDArray, amount: int = 10, blob_size: Tuple = (5, 20), color: COLOR = (0, 0, 0)) -> NDArray:
    min_size, max_size = blob_size
    width, height, _ = img.shape

    # Add Random Black Blobs To Numpy Array
    for _ in range(amount):
        x_pos = randint(0, width)
        y_pos = randint(0, height)
        x_size = randint(min_size, max_size)
        y_size = randint(min_size, max_size)
        cv2.ellipse(img, (x_pos, y_pos), (x_size, y_size), 0, 0, 360, color, -1)

    img = cv2.GaussianBlur(img, (5, 5), 0)

    return img


def overflow_hsv(img: NDArray, hsv_range: Tuple[COLOR, COLOR]) -> NDArray:
    if hsv_range[0] > hsv_range[1]:
        mask1 = cv2.inRange(img, hsv_range[0], (179, 255, 255))
        mask2 = cv2.inRange(img, (0, 0, 0), hsv_range[1])
        results = cv2.bitwise_or(mask1, mask2)

    else:
        results = cv2.inRange(img, hsv_range[0], hsv_range[1])

    return results


def create_hsv_range(hsv: Tuple, hue_range=20, sat_range=20, value_range=20) -> Tuple[COLOR, COLOR]:
    hue, saturation, value = hsv

    high_hue = min(hue + hue_range, 255)
    high_sat = min(saturation + sat_range, 255)
    high_val = min(value + value_range, 255)

    high_range = (high_hue, high_sat, high_val)

    low_hue = min(hue - hue_range, 255)
    low_sat = min(saturation - sat_range, 255)
    low_val = min(value - value_range, 255)

    low_range = (low_hue, low_sat, low_val)

    return (low_range, high_range)


def detect_blobs_verbose(img, mask, **kwargs):
    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = kwargs.get('filterByArea', False)
    params.minArea = kwargs.get('minArea', 20)

    params.filterByCircularity = kwargs.get('filterByCircularity', False)
    params.minCircularity = kwargs.get('minCircularity', 0.8)

    params.filterByConvexity = kwargs.get('filterByConvexity', False)
    params.minConvexity = kwargs.get('minConvexity', 0.2)

    params.filterByInertia = kwargs.get('filterByInertia', False)
    params.minInertiaRatio = kwargs.get('minInertiaRatio', 0.01)

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints, descriptors = detector.detectAndCompute(img)

    return keypoints, descriptors


def hsv_filter_blobs(img: NDArray, keypoints, hsv_range, percentage: float) -> NDArray:
    valid_blobs = []

    # Convert Image To HSV For Better Filtering
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Construct Binary Mask From HSV Range
    mask = cv2.inRange(hsv_img, *hsv_range)

    # Grab Configuration Paramaters From Image
    height, width, _ = img.shape

    for pt in keypoints:
        # Configure Base Area
        radius = int(pt.size // 2)
        diameter = int(radius * 2)

        area =  pi * (radius ** 2)

        # Get Clamped Parameters For Edges
        left = int(pt.pt[0]) - radius
        right = int(pt.pt[0] + radius)
        bottom = int(pt.pt[1]) - radius
        top = int(pt.pt[1] + radius)

        # Generate Cropped Coordinates From Image Size
        crop_left = max(left, 0)
        crop_right = min(right, width)
        crop_top = min(top, height)
        crop_bottom = max(bottom, 0)

        # Cache Displacement For Cropping
        dL = crop_left - left
        dB = crop_bottom - bottom

        if crop_right != right:
            dR = crop_right - right
        else:
            dR = None

        if crop_top != top:
            dT = crop_top - top
        else:
            dT = None

        # Construct Blob Binary Cookie
        blank = np.zeros([right-left, top-bottom, 3], dtype=np.uint8)

        x = blank.shape[0] // 2
        y = blank.shape[1] // 2

        blob = cv2.ellipse(blank, (x, y), (radius, radius), 0, 0, 360, (255, 255, 255), thickness=-1)
        blob = cv2.cvtColor(blob, cv2.COLOR_BGR2GRAY)

        # Crop Generated Cookie
        blob = blob[dB:dT, dL:dR]

        # Crop Blob Segment From HSV Mask
        hsv_mask = mask[crop_bottom: crop_top, crop_left: crop_right]

        # Overlap Both Masks
        overlay = cv2.bitwise_and(blob, blob, mask=hsv_mask)
        valid_pixels = cv2.countNonZero(overlay)

        #Filter Blobs
        if valid_pixels / area >= percentage:
            valid_blobs.append(pt)

    cv2.imshow("Masked HSV Values", mask)

    return tuple(valid_blobs)


def aruco_ratio(img, detector, marker_length) -> Tuple[bool, float]:
    # Detect AruCo Stickers
    corners, ids, rejected = detector.detectMarkers(img)

    if corners:
        # Modify Existing Image With Markers
        detected_image = cv2.aruco.drawDetectedMarkers(img, corners, ids)

        # Format Into Most Salient Marker Corners
        corners = [corner for corner in corners[0][0]]

        # Use Hypotenuse Calculation To Calculate Each Side Length
        sizes = [0.0] * 4
        for i in range(4):
            p1 = corners[i]

            if i < 3:
                p2 = corners[i + 1]
            else:
                p2 = corners[0]

            # Calculate Line Length Between Corners
            deltaX = abs(p1[0] - p2[0])
            deltaY = abs(p1[1] - p2[1])

            sizes[i] = hypot(deltaX, deltaY)

        # Average Corner Sizes To Account For Rotation
        avg_size = np.average(sizes)

        # Return mm To Pixel Ratio
        ratio = marker_length / avg_size

        return (True, ratio)

    return (False, 0.0)


def generate_aruco_detector(type):
    dict = cv2.aruco.getPredefinedDictionary(type)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dict, params)

    return detector


def categorize_blobs(blobs, categories: Dict) -> Dict:
    sorted = filter(categories, key=lambda x: int(x[0]))

    results = dict()
    for i, blob in enumerate(blobs):
        id = binary_range_search(blob.size, categories)


def binary_range_search(key: Union[float, int], target: Tuple, **kwargs) -> Tuple:
    """Uses Binary Search Algorithm To Clamp Value Into Range In O(log n)"""

    # Grab cached left/right if recursion
    left = kwargs.get("left", 0)
    right = kwargs.get("right", len(target) - 1)

    if left == right:
        if right == 0:
            return (None, target[0])
        else:
            return (target[-1], None)

    mid = (left + right) // 2
    if target[mid] <= key:
        if target[mid + 1] > key:
            return (target[mid], target[mid + 1])
        else:
            return binary_range_search(key, target, left=mid + 1, right=right)
    else:
        return binary_range_search(key, target, left=left, right=mid)
