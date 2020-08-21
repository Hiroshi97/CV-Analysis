import fitz
from PIL import Image
import io
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976

class InvisibleTextFilter():

    __slots__ = 'deltaEThreshold'

    def __init__(self, deltaEThreshold = 20):
        self.deltaEThreshold = deltaEThreshold

    def __getTextDetails(self, page: fitz.Page, zoom_f=3) -> dict:
        """
        Returns a dictionary of text spans including its background color and text color.
        zoom_f = 3 means the page's size and resolution is increased 9 times
        """

        # get content of the page
        page_content = page.getText("dict")

        # Transform PDF page into PIL.Image
        mat = fitz.Matrix(zoom_f, zoom_f)
        pixmap = page.getPixmap(mat)

        img = Image.open(io.BytesIO(pixmap.getPNGData()))

        text_blocks = []

        for block in page_content.get('blocks'):
            # check text block only (type 0)
            if (block.get('type') == 0):
                for line in block.get('lines'):
                    for span in line.get('spans'):
                        # ignore spans having empty string
                        if span.get('text') != ' ':
                            rect = fitz.Rect(
                                *tuple(xy * zoom_f for xy in span.get('bbox')))
                            # background color of the span is the color of 2nd pixel starting from span's border
                            color = img.getpixel((rect.x0 + 2, rect.y0 + 2))
                            span['bg_color'] = color
                            span['color'] = self.__intToRGB(span.get('color'))
                            text_blocks.append(span)

        return text_blocks
        # return page_content

    def __intToRGB(self, colorCode: int) -> tuple:
        """ Return the RGB code (as a tuple) of a color integer code """

        r = (colorCode >> 16) & 255
        g = (colorCode >> 8) & 255
        b = colorCode & 255
        return (r, g, b)


    def __deltaE(self, rgb1: tuple, rgb2: tuple) -> float:
        """ Calculate Delta E value of two RGB colors """

        srgb1 = sRGBColor(*rgb1, True)
        srgb2 = sRGBColor(*rgb2, True)

        lab1 = convert_color(srgb1, LabColor)
        lab2 = convert_color(srgb2, LabColor)

        return delta_e_cie1976(lab1, lab2)

    def GetInvisibleText(self, page: fitz.Page) -> []:
        """ 
        This function returns list of text whose color is similar to its background,
        which is determined by deltaE value between text color and background color.
        """

        page_spans = self.__getTextDetails(page)

        invisible_words = []

        for span in page_spans:
            if self.__deltaE(span.get('bg_color'), span.get('color')) <= self.deltaEThreshold:
                invisible_words.append(span)

        return invisible_words


   
