import json

import requests

from hundred.classes import WikidataHtmlRemover


def make_request_wikidata(url: str) -> dict:
    data = requests.get(url).text
    html_remover = WikidataHtmlRemover()
    html_remover.feed(data)
    print(html_remover.source)
    return json.loads(html_remover.source)


def make_request_json(url: str) -> dict:
    return requests.get(url).json()
