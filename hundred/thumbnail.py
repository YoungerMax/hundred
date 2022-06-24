import io
import tempfile

import requests
from PIL import Image, ImageColor, ImageDraw
from PIL.ImageFont import FreeTypeFont
from cairosvg import svg2png

from hundred import utils
from hundred.classes import ExtendedColorThief


def generate_thumbnail_from_image(
        image_path: str,
        font: FreeTypeFont,
        is_svg: bool,
        bar_height: int = 150,
        background_color_hex: str = '#222f3e',
        image_size: tuple[int, int] = (1920, 1080),
        text_color_primary=(255, 255, 255),
        text_color_secondary=(128, 128, 128),
        text='100 SECONDS OF',
        output_file: str = 'output.png',
        output_format: str = 'png',
        color_mode: str = 'RGBA'
):
    with open(image_path, 'rb') as logo_file:
        # read the file
        if is_svg:
            # convert svg to png
            logo_file_bytes = io.BytesIO(svg2png(bytestring=logo_file.read()))
            logo_image = Image.open(logo_file_bytes)
        else:
            logo_image = Image.open(logo_file)

        # make sure the image has an alpha channel
        logo_image = logo_image.convert(color_mode)

        # TODO: crop image so that there is no surrounding transparent space

        # get palette
        color_thief = ExtendedColorThief(logo_image)
        palette = color_thief.get_palette(2, 1)
        rgb_bg_color = ImageColor.getcolor(background_color_hex, color_mode)

        if utils.max_iterable(palette[0]) > utils.max_iterable(palette[1]):
            primary = palette[1]
            secondary = palette[0]
        else:
            primary = palette[0]
            secondary = palette[1]

        # create the final image
        img = Image.new(color_mode, image_size, rgb_bg_color)
        d = ImageDraw.Draw(img)

        # draw rectangle
        d.rectangle(((0, 0), (img.width, bar_height)), fill=primary)
        d.rectangle(((0, bar_height), (img.width, bar_height + bar_height / 10)), fill=secondary)

        # draw title text
        text_width, text_height = font.getsize(text)

        d.text((img.width / 2 - text_width / 2, (bar_height - bar_height / 10) / 2 - text_height / 2 + 6), text,
               font=font, fill=text_color_secondary)
        d.text((img.width / 2 - text_width / 2, (bar_height - bar_height / 10) / 2 - text_height / 2), text, font=font,
               fill=text_color_primary)

        # draw logo
        # calculate resize multiplier
        target_width, target_height = 1024 + 128, 512
        multiplier_width = target_width / logo_image.width
        multiplier_height = target_height / logo_image.height
        multiplier = min(multiplier_width, multiplier_height)

        # draw the resized logo
        logo_image = logo_image.resize((int(logo_image.width * multiplier), int(logo_image.height * multiplier)))
        pos = (int(img.width / 2 - logo_image.width / 2), int((img.height + bar_height) / 2 - logo_image.height / 2))
        img.alpha_composite(logo_image, pos)

        # write out
        with open(output_file, 'wb') as output_file:
            img.save(output_file, output_format)

        # close io buffer if it was an svg
        if is_svg:
            logo_file_bytes.close()


def generate_thumbnail_from_image_url(
        image_url: str,
        font: FreeTypeFont,
        is_svg: bool,
        bar_height: int = 150,
        background_color_hex: str = '#222f3e',
        image_size: tuple[int, int] = (1920, 1080),
        text_color_primary=(255, 255, 255),
        text_color_secondary=(128, 128, 128),
        text='100 SECONDS OF',
        output_file: str = 'output.png',
        output_format: str = 'png',
        color_mode: str = 'RGBA'
):
    with tempfile.NamedTemporaryFile(mode='wb') as file:
        file.write(requests.get(image_url).content)
        file.flush()

        generate_thumbnail_from_image(file.name, font, is_svg, bar_height, background_color_hex, image_size,
                                      text_color_primary, text_color_secondary, text, output_file, output_format,
                                      color_mode)


def generate_thumbnail_from_lang(
        programming_language: str,
        font: FreeTypeFont,
        bar_height: int = 150,
        background_color_hex: str = '#222f3e',
        image_size: tuple[int, int] = (1920, 1080),
        text_color_primary=(255, 255, 255),
        text_color_secondary=(128, 128, 128),
        text='100 SECONDS OF',
        output_file: str = 'output.png',
        output_format: str = 'png',
        color_mode: str = 'RGBA'
):
    generate_thumbnail_from_image_url(
        f'https://raw.githubusercontent.com/abrudz/logos/main/{programming_language}.svg',
        font,
        True,
        bar_height,
        background_color_hex,
        image_size,
        text_color_primary,
        text_color_secondary,
        text,
        output_file,
        output_format,
        color_mode
    )
