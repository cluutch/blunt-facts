from PIL import Image, ImageDraw, ImageFont
# import numpy as np


def remove_background(img: Image, white_threshold: int) -> Image:
    new_img = img.copy()
    img_data = new_img.getdata()
    new_data = []
    for pixel in img_data:
        is_pixel_white = all(rgb > white_threshold for rgb in pixel)
        if is_pixel_white:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(pixel)

    new_img.putdata(new_data)
    return new_img


def load_img_as_rgb(filepath: str) -> Image:
    img = Image.open(filepath)
    return img.convert('RGBA')


def transform_img(img: Image, point_multiplier: float) -> Image:
    new_img = img.copy()
    new_img = new_img.point(lambda i: i * point_multiplier)
    return new_img


def add_text(img: Image, text: str, xpos: int, ypos: int,
             font: ImageFont, color=(0, 0, 0)):
    new_img = img.copy()
    image_draw = ImageDraw.Draw(new_img)
    image_draw.text(
            (xpos, ypos), text, color, font=font)
    return new_img


def add_background(img: Image, color=(255, 255, 255)):
    # Create a white rgba background
    new_img = Image.new("RGBA", img.size, color)
    # Paste the image on the background
    new_img.paste(img, (0, 0), img)
    return new_img


class BluntFactsNft:
    INFO_FIELDS = ['strain_type', 'strain_aroma',
                   'strain_feeling', 'strain_other_attributes']
    BACKGROUND_COLOR = (146, 2, 88)
    TEXT_COLOR = (229, 229, 229)
    OUTPUT_IMG_FILETYPE = "PNG"
    DEFAULT_WHITE_THRESHOLD = 90
    DEFAULT_POINT_MULTIPLIER = 1.9

    NUMBER_WIDTH_PCT = 0.03
    TITLE_WIDTH_PCT = 0.50
    TITLE_HEIGHT_PCT = 0.03

    INFO_HEIGHT_PCT = 0.70

    DEFAULT_FONT_PATH = "laughingbuddha/StickNoBills-Bold.ttf"
    DEFAULT_TITLE_FONT_SIZE = 60

    DEFAULT_PRICE_FONT_PATH = "laughingbuddha/Sunflower-Medium.ttf"
    DEFAULT_PRICE_FONT_SIZE = 45

    DEFAULT_INFO_FONT_PATH = "laughingbuddha/Sunflower-Light.ttf"
    DEFAULT_INFO_FONT_SIZE = 45

    LINE_SPACING = 7

    def __init__(self,
                 strain_info: dict,
                 input_img_filepath: str,
                 output_img_filepath: str,
                 white_threshold: int = DEFAULT_WHITE_THRESHOLD,
                 point_multiplier: float = DEFAULT_POINT_MULTIPLIER,
                 title_font_path: str = DEFAULT_FONT_PATH):

        self.strain_info = strain_info
        self.input_img_filepath = input_img_filepath
        self.output_img_filepath = output_img_filepath
        self.white_threshold = white_threshold
        self.point_multiplier = point_multiplier
        self.title_font = ImageFont.truetype(title_font_path,
                                             size=self.DEFAULT_TITLE_FONT_SIZE)
        self.price_font = ImageFont.truetype(self.DEFAULT_PRICE_FONT_PATH,
                                             size=self.DEFAULT_PRICE_FONT_SIZE)
        self.info_font = ImageFont.truetype(self.DEFAULT_INFO_FONT_PATH,
                                            size=self.DEFAULT_INFO_FONT_SIZE)

    def add_title_to_img(self, xpos, ypos) -> int:
        title = self.strain_info['strain'].title()
        self.img = add_text(self.img, title, xpos, ypos, self.title_font,
                            color=self.TEXT_COLOR)
        return ypos + self.LINE_SPACING + self.DEFAULT_TITLE_FONT_SIZE + 13

    def add_price_to_img(self, xpos, ypos) -> int:
        price = '$' + str(round(self.strain_info['avg_price_per_ounce'], 2))
        self.img = add_text(self.img, price, xpos, ypos, self.price_font,
                            color=self.TEXT_COLOR)
        return ypos + self.LINE_SPACING + self.DEFAULT_PRICE_FONT_SIZE

    def add_info_to_img(self, xpos, ypos) -> int:
        for info_type in self.INFO_FIELDS:
            text = self.strain_info[info_type]['best']
            self.img = add_text(self.img, text, xpos, ypos, self.info_font,
                                color=self.TEXT_COLOR)
            ypos += self.DEFAULT_INFO_FONT_SIZE + self.LINE_SPACING

        return ypos

    def gen_img(self, yoffset=0):
        print("Loading original img")
        self.img = load_img_as_rgb(self.input_img_filepath)

        print("Removing background")
        self.img = remove_background(self.img, self.white_threshold)

        print("Transforming img")
        self.img = transform_img(self.img, self.point_multiplier)

        print("Adding text to image")
        xpos = self.img.width * self.NUMBER_WIDTH_PCT
        ypos = self.img.height * self.TITLE_HEIGHT_PCT + yoffset
        self.img = add_text(self.img, "#3", xpos, ypos, self.title_font,
                                color=self.TEXT_COLOR)

        xpos = self.img.width * self.TITLE_WIDTH_PCT
        ypos = self.add_title_to_img(xpos, ypos)

        self.add_price_to_img(xpos, ypos)

        ypos = self.img.height * self.INFO_HEIGHT_PCT
        self.add_info_to_img(xpos, ypos)

        print("Adding background")
        self.img = add_background(self.img, color=self.BACKGROUND_COLOR)

        print("Saving")
        self.img.save(self.output_img_filepath, self.OUTPUT_IMG_FILETYPE)
