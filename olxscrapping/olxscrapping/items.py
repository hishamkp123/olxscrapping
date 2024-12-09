# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class ProductItem(scrapy.Item):
    property_name = scrapy.Field()
    image_url = scrapy.Field()
    property_type = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    seller_name = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    breadcrumbs = scrapy.Field()