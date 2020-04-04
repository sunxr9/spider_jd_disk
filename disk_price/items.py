# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiskPriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    interface = scrapy.Field()
    rotate_speed = scrapy.Field()
    capacity = scrapy.Field()
    cache = scrapy.Field()
    price = scrapy.Field()
    shop_name = scrapy.Field()
    shop_address = scrapy.Field()





