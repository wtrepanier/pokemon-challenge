import scrapy
from w3lib.html import remove_tags


class Pokemon(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    generation = scrapy.Field()
    number = scrapy.Field()
    image_link = scrapy.Field()


class PokemonExtractorSpider(scrapy.Spider):
    name = "pokemon"
    start_urls = ["https://pokemondb.net/pokedex/national"]

    BASE_URL = "https://pokemondb.net"

    def parse(self, response):
        links = response.xpath("//a[@class='ent-name']/@href").extract()
        for link in links:
            abs_url = self.BASE_URL + link
            yield scrapy.Request(abs_url, callback=self.parse_pokemon)

    def parse_pokemon(self, response):
        item = Pokemon()
        item["link"] = response.url
        item["name"] = response.css("h1::text").extract_first()
        item["image_link"] = response.xpath("//img/@src").extract_first()
        item["number"] = int(
            remove_tags(
                response.xpath(
                    "//*[contains(text(),'National №')]/../td"
                ).extract_first()
            )
        )
        item["generation"] = int(
            remove_tags(
                response.xpath("//*[contains(text(),'Generation ')]").extract_first()
            )[11:]
        )
        item["type"] = [
            t
            for t in response.xpath(
                "//table[@class='vitals-table']/tbody/tr/th[text()='Type']/../td/a/text()"
            ).extract()
        ]

        yield item
