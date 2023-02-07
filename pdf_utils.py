from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab.lib as lib
from reportlab.graphics import renderPM
from blob_utils import *
from os.path import basename
from os import remove
from glob import glob
import cv2

class PDF(Canvas):
    """
    Python PDF generator for ease of use.
    Uses reportlab package to generate PDF documents.
    """

    COLOR = [int, int, int]
    INCH = lib.units.inch
    MM = lib.units.mm
    LETTER_SIZE = lib.pagesizes.letter

    def __init__(self, **kwargs):
        self.path = kwargs.get("path", r"reports/sample.pdf")

        letter_size = kwargs.get("size", self.LETTER_SIZE)

        super().__init__(self.path, pagesize=self.LETTER_SIZE)
        self.page_size = {
            "width": self.LETTER_SIZE[0],
            "height": self.LETTER_SIZE[1]
        }

        file_name = self.get_file_name(self.path)
        self.setTitle(
            self.get_file_name(file_name)
        )

        self.fonts = []
        self.current_font = "Helvetica"
        self.setFont("Helvetica", 12)

        font_dir = kwargs.get("font_dir", "fonts")

        # Grab Fonts From Fonts Folder
        fonts = glob(font_dir + r'\*.ttf')
        for font in fonts:
            font_name = self.get_file_name(font)
            pdfmetrics.registerFont(
                TTFont(name=font_name, filename=font)
            )
            self.fonts.append(font_name)

        self.fonts += self.getAvailableFonts()  # Add built-in fonts to font list

        self.page_number = 1

        self.number_pages = kwargs.get("page_numbers", True)
        self.logo = kwargs.get("logo", None)

        # Append elements onto first page
        self.addLogo()
        self.addPageNumber()

    def addLogo(self):
        if self.logo:
            self.drawImage(self.logo, 20, self.page_size["height"] - 40,
                           width=100, height=20)

    def addLineText(self, text: str, x: int, y: int, **kwargs):

        font = kwargs.get("font", self.current_font)
        font_size = kwargs.get("font_size", 12)
        color = kwargs.get("color", (0, 0, 0))
        centered = kwargs.get("center", True)

        if font in self.fonts:
            self.setFont(font, font_size)
            self.current_font = font

        self.setFillColorRGB(*color)

        if centered:
            self.drawCentredString(x, y, text)
        else:
            temp = self.beginText(x, y, direction="right")
            temp.textOut(text)
            self.drawText(temp)

    def addCVImage(self, data, name, coords=(100, 200), **kwargs):
        path = f"../static/images/{name}.jpg"

        cv2.imwrite(path, data)

        self.drawImage(path, *coords, **kwargs)

        remove(path)

    def drawPNG(self, coords, path, size=72):
        renderPM.drawToFile(self.path, path, 'PNG', dpi=size)

    def change_font(self, font_size: int, font: str) -> None:
        """
        Changes next drawn text to font from ttf or default.
        Also checks if font in registry.
        """

        if font in self.fonts:
            self.setFont(font, font_size)
            self.current_font = font
        else:
            self.setFont(self.current_font, font_size)

    def addHorizontalLine(self, y: int, margin: float = 0.,
                          thickness: float = 0.1, color: COLOR = (0, 0, 0)):
        """
        Adds horizontal line across length of PDF

        int y: Vertical Coordinate (px)

        float margin: Margin (inches)

        float thickness: Line Thickness (inches)

        (int, int, int) color: Color (RGB)

        """

        thickness *= self.INCH
        margin *= self.INCH

        self.setLineWidth(width=thickness)
        self.setFillColorRGB(*color)

        self.line(0 + margin, y,
                  self.page_size["width"] - margin, y)

    def addVerticalLine(self, x: int, margin: float = 0.,
                          thickness: float = 0.1, color: COLOR = (0, 0, 0)):
        """
                Adds vertical line across length of PDF

                int x: Horizontal Coordinate (px)

                float margin: Margin (inches)

                float thickness: Line Thickness (inches)

                (int, int, int) color: Color (RGB)

        """

        thickness *= self.INCH
        margin *= self.INCH

        self.setLineWidth(width=thickness)
        self.setFillColorRGB(*color)

        self.line(x, margin, x, self.page_size["height"] - margin)

    def addDecoratedPage(self):
        self.page_number += 1
        self.showPage()

        self.addLogo()
        self.addPageNumber()

    def adjust_y(self, y, page_number):
        y_offset = (self.page_number - page_number) * self.page_size["height"]

        return y_offset + y

    def addPageNumber(self):
        x = self.page_size["width"] - 40
        y = self.page_size["height"] - 40

        self.setFontSize(15)
        self.drawCentredString(x, y, str(self.page_number))

    def generateSplatterAnalysis(self, aruco_ratio: float, aruco_id: int, img: NDArray = None):
        """
        Generates completed template page and applies blood splatter analysis.
        Simply add aruco ratio / id detected elsewhere and voila! It's done!

        :param img:
        :param aruco_ratio:
        :return:
        """

        # Add static elements
        self.addDecoratedPage()
        self.addLineText("Potential Causes:", x=30, y=175, font_size=16, center=False)
        self.addLineText("Fig. 1: Captured Frame", x=173, y=450)
        self.addLineText("Fig. 2: Low Velocity Splatters", x=446, y=450)
        self.addLineText("Fig. 3: Medium Velocity Splatters", x=173, y=210)
        self.addLineText("Fig. 4: High Velocity Splatters", x=446, y=210)
        self.addLineText(f"Identified ID: {aruco_id}", x=480,
                        y=20, font_size=16)

        # Get picture sample
        if img:
            frame = img
        else:
            cap = cv2.VideoCapture(0)
            _, frame = cap.read()
            cap.release()

        # Detect blobs with default parameters
        blobs = detect_blobs(frame, **default_params)
        blobs = hsv_filter_blobs(frame, blobs, **default_hsv)

        # Categorize Blobs By Size
        circled = annotate_image_blobs(frame, blobs)
        sorted_blobs = categorize_blobs(blobs, aruco_ratio)

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
        aruco_img = cv2.aruco.drawMarker(arucoDict, aruco_id, 500)

        maskWidth = 200
        maskHeight = 200

        # Add Sample Images
        cID = self.page_number
        self.addCVImage(circled, f"circled{cID}", (73, 470), width=maskWidth, height=maskHeight)
        self.addCVImage(low_img, f"lowV{cID}", (346, 470), width=maskWidth, height=maskHeight)
        self.addCVImage(medium_img, f"mediumV{cID}", (73, 230), width=maskWidth, height=maskHeight)
        self.addCVImage(high_img, f"highV{cID}", (346, 230), width=maskWidth, height=maskHeight)
        self.addCVImage(aruco_img, f"Aruco{cID}", (410, 40), width=140, height=140)

        # Add Potential Causes Based On Groupings
        x = 20
        y = 160
        yOff = -15

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
            causes.append("N/A")

        # Display Each Cause Dynamically
        for cause in causes:
            self.addLineText(cause, 40, y, center=False, font_size=13)
            y += yOff

        # Display The Groupings On Top
        self.addLineText(f"Identified Splatter Groups: {', '.join(groups)}",
                        30, 700, center=False, font_size=16)

    def createTitlePage(self, site, date, operator):
        # Adds title page
        pdf.addLineText("Sample Report", x=310, y=620, font_size=50)
        pdf.addLineText("Site 9728-B", x=310, y=430)
        pdf.addLineText("2/3/2023", x=310, y=310)
        pdf.addLineText("Analyst Jacob Rowe", x=310, y=210)

    @staticmethod
    def get_file_name(path: str) -> str:
        """Grabs the basic file name without extensions."""

        base = basename(path)
        if "." in base:
            file_name = ".".join(
                base.split(".")[:-1]
            )
        else:
            file_name = base

        return file_name
