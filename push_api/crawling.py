import json
from os import path
from typing import List

from pokemon_crawling.pokemon_crawling.spiders.pokemon_spider import (
    PokemonExtractorSpider,
)
from scrapy.crawler import CrawlerProcess

from push_api.pokemon import Pokemon


def get_pokemons() -> List[Pokemon]:
    if not path.exists("pokemons.json"):
        crawl_pokemons()

    with open("pokemons.json", "r") as json_file:
        data = json.load(json_file)
        pokemons = []
        for p in data:
            pokemons.append(Pokemon(**p))
        return pokemons


def crawl_pokemons():
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "pokemons.json": {"format": "json"},
            },
        }
    )
    process.crawl(PokemonExtractorSpider)
    process.start()
