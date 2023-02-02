from pdf_utils import PDF
import cv2


def generate_pdf_example():
    pdf = PDF(path=r'../reports/sample.pdf')

    pdf.addLineText("Title", 300, 300, width=20, height=20)
    pdf.addHorizontalLine(200, thickness=0.2, margin=0.1)

    cam = cv2.VideoCapture(0)
    while True:
        active, frame = cam.read()
        if active:
            pdf.addCVImage(frame, width=100, height=100)
            break

    pdf.save()


if __name__ == "__main__":
    generate_pdf_example()
