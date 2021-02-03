import scrapy
from w3lib.html import remove_tags


class Pokemon(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    poke_type = scrapy.Field()
    generation = scrapy.Field()
    number = scrapy.Field()
    image_link = scrapy.Field()
    weight = scrapy.Field()
    height = scrapy.Field()
    species = scrapy.Field()
    description = scrapy.Field()


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
        pokemon = Pokemon()
        pokemon["link"] = response.url
        pokemon["name"] = response.css("h1::text").extract_first()
        pokemon["image_link"] = response.xpath("//img/@src").extract_first()
        pokemon["number"] = int(
            remove_tags(
                response.xpath(
                    "//*[contains(text(),'National №')]/../td"
                ).extract_first()
            )
        )
        pokemon["generation"] = int(
            remove_tags(
                response.xpath("//*[contains(text(),'Generation ')]").extract_first()
            )[11:]
        )
        pokemon["poke_type"] = [
            t
            for t in response.xpath(
                "//div[@class='sv-tabs-panel active']//table[@class='vitals-table']/tbody/tr/th[text()='Type']/../td/a/text()"
            ).extract()
        ]
        pokemon["weight"] = float(
            response.xpath(
                "//div[@class='sv-tabs-panel active']//table[@class='vitals-table']/tbody/tr/th[text()='Weight']/../td/text()"
            )
            .extract_first()
            .split("\xa0")[0]
        )
        pokemon["height"] = float(
            response.xpath(
                "//div[@class='sv-tabs-panel active']//table[@class='vitals-table']/tbody/tr/th[text()='Height']/../td/text()"
            )
            .extract_first()
            .split("\xa0")[0]
        )
        pokemon["species"] = response.xpath(
            "//div[@class='sv-tabs-panel active']//table[@class='vitals-table']/tbody/tr/th[text()='Species']/../td/text()"
        ).extract_first()
        pokemon["description"] = remove_tags(response.xpath('//p').extract_first())

        yield pokemon
