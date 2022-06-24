import sys
from pathlib import Path

from hundred import thumbnail
from hundred.classes import Configuration

from PIL import ImageFont

from hundred.script import ScriptGenerator
from hundred.script.sections import get_default_sections

if __name__ == '__main__':
    print('reading configuration')

    _, info_file, = sys.argv
    font = ImageFont.truetype('font/Montserrat-ExtraBold.ttf', 86)
    cfg = Configuration(str(Path(info_file).absolute()))

    print('generating script')
    generator = ScriptGenerator(cfg, get_default_sections(cfg))
    script = generator.generate_script()
    print(script)

    print('generating thumbnail')

    # TODO: get logo from Wikidata
    thumbnail.generate_thumbnail_from_image_url('https://miro.medium.com/max/1138/1*6-G_o5PZSzppyfdLTbFu-A.png',
                                                font,
                                                is_svg=False)
