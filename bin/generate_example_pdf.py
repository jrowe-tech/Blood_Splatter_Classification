from pdf_utils import PDF
from blob_utils import *
from time import sleep
import cv2


def generate_pdf_example():
    pdf = PDF(logo=r"../static/images/logo.jpg", font_dir="../static/fonts")

    # Prints Active Fonts
    print(f"Active Fonts: ")
    print(f"{pdf.fonts}", sep="/n")


    # Adds title page
    pdf.addLineText("Sample Report", x=310, y=pdf.adjust_y(620, 1), font_size=50)
    pdf.addLineText("Site 9728-B", x=310, y=pdf.adjust_y(430, 1))
    pdf.addLineText("2/3/2023", x=310, y=pdf.adjust_y(310, 1))
    pdf.addLineText("Analyst Jacob Rowe", x=310, y=pdf.adjust_y(210, 1))

    # Change sample ArUco Here
    aruco_code = 1
    aruco_ratio = 0.4

    # print(f"Aruco Dir: {dir(cv2.aruco)}")
    pdf.generateSplatterAnalysis(aruco_ratio, aruco_code)
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
