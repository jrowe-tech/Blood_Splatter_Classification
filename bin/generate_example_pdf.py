from pdf_utils import PDF
from blob_utils import *
from time import sleep
import cv2


def generate_pdf_example():
    pdf = PDF(path=r'../reports/sample.pdf', logo="../static/images/logo.jpg")

    # Adds title page
    pdf.addLineText("Sample Report", x=310, y=620, font_size=50)
    pdf.addLineText("Site 9728-B", x=310, y=430)
    pdf.addLineText("2/3/2023", x=310, y=310)
    pdf.addLineText("Analyst Jacob Rowe", x=310, y=210)

    # Change sample ArUco Here
    aruco_code = 1
    aruco_ratio = 0.4

    pdf.generateSplatterAnalysis(aruco_ratio, aruco_code)

    sleep(3)

    pdf.generateSplatterAnalysis(aruco_ratio, 3)
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
