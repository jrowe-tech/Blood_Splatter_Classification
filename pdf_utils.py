from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab.lib as lib
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

    def __init__(self, **kwargs):
        path = kwargs.get("path", r"reports/sample.pdf")

        letter_size = lib.pagesizes.letter
        super().__init__(path, pagesize=letter_size)
        self.page_size = {
            "width": letter_size[0],
            "height": letter_size[1]
        }

        file_name = self.get_file_name(path)
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

        # Add Lambda Functions for typing style
        self.addPage = lambda: self.showPage()

    def addLineText(self, text: str, x: int, y: int, **kwargs):

        font = kwargs.get("font", self.current_font)
        font_size = kwargs.get("font_size", 12)
        color = kwargs.get("color", (0, 0, 0))

        if font in self.fonts:
            self.setFont(font, font_size)
            self.current_font = font

        self.setFillColorRGB(*color)

        self.drawCentredString(x, y, text)

    def addCVImage(self, data, **kwargs):
        temp = "static/images/temp.jpg"

        file = cv2.imwrite(temp, data)

        self.drawInlineImage(temp, **kwargs)

        remove(temp)

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
        self.line(0 + margin, y, self.page_size["width"] - margin, y)

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
