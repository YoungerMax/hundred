from configparser import ConfigParser
from html.parser import HTMLParser
from colorthief import ColorThief
from PIL import Image


class Configuration:
    def __init__(self, file: str):
        parser = ConfigParser()

        with open(file) as f:
            parser.read_file(f)

        self.name = parser['meta']['name']
        self.wikipedia = parser['apis']['wikipedia']
        self.wikidata = parser['apis']['wikidata']


class WikidataHtmlRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.source: str = ''

    def handle_data(self, data: str) -> None:
        self.source = data


class ExtendedColorThief(ColorThief):
    def __init__(self, image):
        self.image = image
