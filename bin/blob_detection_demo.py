from blob_utils import *
import cv2


def main():
    blood_color = (170, 255, 0)
    blood_hsv = (0, 255, 255)

    blank = create_solid_image(600, 600)
    img = draw_random_blobs(blank, color=(0, 0, 0), amount=40)
    img = draw_random_blobs(blank, color=blood_color, amount=40)
    img = draw_random_blobs(blank, color=(0, 255, 100), amount=50)

    cv2.imshow("Randomly Generated Blob Image", img)
    cv2.waitKey()

    blobs = detect_blobs(img, min_area=10, filterByArea=True)

    if blobs:
        hsv_range = create_hsv_range(blood_hsv, 20, 100, 100)
        unfiltered = annotate_image_blobs(img, blobs, color=(0, 0, 255))
        blobs = hsv_filter_blobs(img, blobs, hsv_range, 0.3)
        filtered = annotate_image_blobs(img, blobs, color=(255, 0, 0))

        results = np.hstack((unfiltered, filtered))
        cv2.imshow("Unfiltered v. Filtered Blobs", results)

        cv2.waitKey()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()