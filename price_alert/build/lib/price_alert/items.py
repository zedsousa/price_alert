from scrapy import Item, Field

class AmazonItem(Item):
    asin = Field()
    title = Field()
    image = Field()
    price = Field()
    best_offer = Field()
