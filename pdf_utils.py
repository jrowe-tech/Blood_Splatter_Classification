from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab.lib as lib
from reportlab.graphics import renderPM
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

        print(f"PATH: {path}")

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

        return y_offset * y

    def addPageNumber(self):
        x = self.page_size["width"] - 40
        y = self.page_size["height"] - 40

        self.setFontSize(15)
        self.drawCentredString(x, y, str(self.page_number))

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
