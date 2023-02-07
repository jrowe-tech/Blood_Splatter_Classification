from pdf_utils import PDF
from blob_utils import *
import cv2


def generate_pdf_example():
    pdf = PDF(path=r'../reports/sample.pdf', logo="../static/images/logo.jpg")
    pdf.current_font = ""

    # Change sample ArUco Here
    aruco_code = 1

    # Caches resused coordinates of PDF
    cX = pdf.page_size["width"] // 2
    cY = pdf.page_size["height"] // 2
    catX = 30

    # Adds title page
    pdf.addLineText("Sample Report", x=cX, y=620, font_size=50)
    pdf.addLineText("Site 9728-B", x=cX, y=430)
    pdf.addLineText("2/3/2023", x=cX, y=310)
    pdf.addLineText("Analyst Jacob Rowe", x=cX, y=210)

    # Add sample ArUco code page (static elements)
    pdf.addDecoratedPage()
    pdf.addLineText("Potential Causes:", x=catX, y=175, font_size=16, center=False)
    pdf.addLineText("Fig. 1: Captured Frame", x=173, y=450)
    pdf.addLineText("Fig. 2: Low Velocity Splatters", x=446, y=450)
    pdf.addLineText("Fig. 3: Medium Velocity Splatters", x=173, y=210)
    pdf.addLineText("Fig. 4: High Velocity Splatters", x=446, y=210)
    pdf.addLineText(f"Identified ID: {aruco_code}", x=480,
                    y=20, font_size=16)

    # Take Sample Frame From Camera
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()

    blobs = detect_blobs(frame, **default_params)
    blobs = hsv_filter_blobs(frame, blobs, **default_hsv)
    assert blobs is not None, "No blobs detected! Retry!"

    # Categorize Blobs By Size
    circled = annotate_image_blobs(frame, blobs)
    sorted_blobs = categorize_blobs(blobs, 0.4)

    # Organize Blob Images By Size
    low_blobs = []
    medium_blobs = []
    high_blobs = []
    low_sizes = []
    medium_sizes = []
    high_sizes = []

    for i, blob in enumerate(blobs):
        name = sorted_blobs[i][0]
        size = sorted_blobs[i][1]

        if name == "Low Velocity":
            low_blobs.append(blob)
            low_sizes.append(size)
        elif name == "Medium Velocity":
            medium_blobs.append(blob)
            medium_sizes.append(size)
        else:
            high_blobs.append(blob)
            high_sizes.append(size)

    # Construct Colored Masks Per Detected
    low_img = create_blob_display(frame, low_blobs, weight=0.9)
    medium_img = create_blob_display(frame, medium_blobs, weight=0.9)
    high_img = create_blob_display(frame, high_blobs, weight=0.9)

    # Append Blob Sizes Onto Images
    low_img = draw_blob_sizes(low_img, low_blobs, low_sizes)
    medium_img = draw_blob_sizes(medium_img, medium_blobs, medium_sizes)
    high_img = draw_blob_sizes(high_img, high_blobs, high_sizes)

    # Construct Numpy array for detected aruco codes
    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_100)
    aruco_img = cv2.aruco.drawMarker(arucoDict, aruco_code, 500)

    maskWidth = 200
    maskHeight = 200


    # Add Sample Images
    pdf.addCVImage(circled, "circled", (73, 470), width=maskWidth, height=maskHeight)
    pdf.addCVImage(low_img, "lowV", (346, 470), width=maskWidth, height=maskHeight)
    pdf.addCVImage(medium_img, "mediumV", (73, 230), width=maskWidth, height=maskHeight)
    pdf.addCVImage(high_img, "highV", (346, 230), width=maskWidth, height=maskHeight)
    pdf.addCVImage(aruco_img, "Aruco", (410, 40), width=140, height=140)

    # Add Potential Causes Based On Groupings
    yOff = -15
    x = 20
    y = 160

    causes = []
    groups = []

    if low_blobs:
        causes += default_categories[2]["causes"]
        groups.append("Low Velocity")
    if medium_blobs:
        causes += default_categories[1]["causes"]
        groups.append("Medium Velocity")
    if high_blobs:
        causes += default_categories[0]["causes"]
        groups.append("High Velocity")

    # Add N/A If No Blobs Detected
    if not groups:
        groups.append("N/A")

    print(f"Groups: {groups}")

    # Display Each Cause Dynamically
    for cause in causes:
        pdf.addLineText(cause, catX + 10, y, center=False, font_size=13)
        y += yOff

    # Display The Groupings On Top
    pdf.addLineText(f"Identified Splatter Groups: {', '.join(groups)}",
                    30, 700, center=False, font_size=16)

    pdf.save()


def generate_pdf_grid(size=PDF.LETTER_SIZE, space: int = 20,
                      thickness: float = 0.01):
    pdf = PDF(path=r'../reports/grid.pdf', size=size)

    x = 0
    # Procedurally generate vertical lines
    while x < size[0]:
        pdf.addVerticalLine(x, thickness=thickness)
        x += space

    y = 0
    while y < size[1]:
        pdf.addHorizontalLine(y, thickness=thickness)
        y += space

    pdf.save()

    return x, y


if __name__ == "__main__":
    generate_pdf_example()
    x, y = generate_pdf_grid()

    print(f"Final Grid: ({x}, {y})")
